-- Native ship-configuration preset and price boundary; no purchase effects.
-- Sources: menu_ship_configuration dropdownLoadout, insertWare/checkEquipment.
local ffi = require('ffi')
ffi.cdef[[
bool CanGenerateValidLoadout(UniverseID containerid, const char* macroname);
void GenerateShipLoadout2(UILoadout2* result, UniverseID containerid, UniverseID shipid, const char* macroname, float level);
void GenerateShipLoadoutCounts2(UILoadoutCounts2* result, UniverseID containerid, UniverseID shipid, const char* macroname, float level);
int64_t GetBuildWarePrice(UniverseID containerid, const char* warename);
float GetContainerBuildPriceFactor(UniverseID containerid);
bool IsComponentClass(UniverseID componentid, const char* classname);
WorkForceInfo GetWorkForceInfo(UniverseID containerid, const char* raceid);
uint32_t GetNumSoftwareSlots(UniverseID controllableid, const char* macroname);
uint32_t GetSoftwareSlots(SoftwareSlot* result, uint32_t resultlen, UniverseID controllableid, const char* macroname);
const char* GetSoftwareMaxCompatibleVersion(UniverseID controllableid, const char* macroname, const char* softwarename);
uint32_t GetNumSoftwarePredecessors(const char* softwarename);
uint32_t GetSoftwarePredecessors(const char** result, uint32_t resultlen, const char* softwarename);
bool IsSoftwareDefault(UniverseID controllableid, const char* macroname, const char* softwarename);
]]
local M = {}
local categories = {'weapons', 'turrets', 'shields', 'engines',
                    'turretgroups', 'shieldgroups', 'ammo', 'units', 'software', 'crew'}
local function finite(value)
    return type(value) == 'number' and value == value and value >= 0
        and value <= 9007199254740991
end
local function discount(entries, salesonly)
    assert(type(entries) == 'table', 'discounts_missing')
    local factor = 1
    for _, entry in ipairs(entries) do
        if not salesonly or entry.applytoshipsales then
            assert(finite(entry.amount), 'discount_invalid')
            factor = factor - entry.amount / 100
        end
    end
    assert(finite(factor), 'discount_factor_invalid')
    return factor
end
local quotes = setmetatable({}, {__mode='k'})
local function calculate_price(shipyard, wares, software, crewcount)
    local yardid = ConvertIDTo64Bit(shipyard)
    assert(yardid ~= 0 and ffi.C.IsComponentClass(yardid, 'station'), 'shipyard_unavailable')
    local owned = GetComponentData(shipyard, 'isplayerowned')
    local price, crewprice, parts = 0, 0, {}
    if owned ~= true and owned ~= 1 then
        for ware, amount in pairs(wares) do
            -- Native UI omits prices for volatile consumables.
            local unitprice = GetWareData(ware, 'volatile') and 0 or tonumber(ffi.C.GetBuildWarePrice(yardid, ware))
            assert(finite(unitprice), 'ware_price_invalid')
            parts[#parts+1]={ware=ware,amount=amount,price=unitprice,kind='equipment'}
            price = price + amount * unitprice
        end
        local buildfactor = tonumber(ffi.C.GetContainerBuildPriceFactor(yardid))
        assert(finite(buildfactor), 'build_factor_invalid')
        local salesfactor = discount(GetComponentData(shipyard, 'discounts'), true)
        for ware, amount in pairs(software) do
            local unitprice = salesfactor * buildfactor * GetContainerWarePrice(shipyard, ware, false)
            assert(finite(unitprice), 'software_price_invalid')
            parts[#parts+1]={ware=ware,amount=amount,price=unitprice,kind='software'}
            price = price + amount * unitprice
        end
        if crewcount > 0 then
            local workforce = ffi.C.GetWorkForceInfo(yardid, '')
            local available, maximum = tonumber(workforce.available), tonumber(workforce.maxavailable)
            assert(finite(available) and finite(maximum) and maximum > 0 and available <= maximum, 'workforce_unknown')
            local minprice, maxprice = GetWareData('crew', 'minprice', 'maxprice')
            assert(finite(minprice) and finite(maxprice) and maxprice >= minprice, 'crew_price_invalid')
            crewprice = crewcount * Helper.round(discount(GetComponentData(shipyard, 'hiringdiscounts'))
                * buildfactor * (maxprice - available / maximum * (maxprice - minprice)))
        end
        assert(finite(price) and price > 0 and finite(crewprice) and finite(price + crewprice), 'total_price_invalid')
    end
    -- checkEquipment applies the native trade rounding to both totals before
    -- AddBuildTask6. An FFI integer cast would underquote fractional discounts.
    local rawprice = price
    price = RoundTotalTradePrice(price)
    crewprice = RoundTotalTradePrice(crewprice)
    assert(finite(price) and finite(crewprice) and price % 1 == 0 and crewprice % 1 == 0, 'rounded_price_invalid')
    return price, crewprice, rawprice, parts
end
local function generate(shipyard, macro, level)
    local yardid = ConvertIDTo64Bit(shipyard)
    assert(yardid ~= 0 and ffi.C.IsComponentClass(yardid, 'station')
        and ffi.C.CanGenerateValidLoadout(yardid, macro), 'loadout_unavailable')
    -- Preserve the complete native payload, including software, groups and crew.
    -- Validate counts before Helper allocates arrays from them.
    local function counts(result, ...)
        ffi.C.GenerateShipLoadoutCounts2(result, ...)
        for _, category in ipairs(categories) do
            local n = tonumber(result['num' .. category])
            assert(finite(n) and n <= 2048 and n % 1 == 0, 'loadout_count_invalid')
        end
    end
    assert(type(Helper.ffiTempStorage) == 'table', 'native_loadout_storage_missing')
    local firstallocation = #Helper.ffiTempStorage + 1
    local loadout = Helper.getLoadoutHelper2(ffi.C.GenerateShipLoadout2, counts,
                                            'UILoadout2', yardid, 0, macro, level)
    -- Helper clears ffiTempStorage on UI updates. A quote may survive those
    -- updates; retain every native array referenced by its loadout pointers.
    local keepalive = {}
    for index = firstallocation, #Helper.ffiTempStorage do
        keepalive[#keepalive+1] = Helper.ffiTempStorage[index]
    end
    local wares, software, crewcount = {}, {}, 0
    -- Native ship hulls may already include basic software. The ordinary
    -- purchase menu charges only the difference from these current slots.
    local baseline, softwareslots = {}, {}
    local numslots = tonumber(ffi.C.GetNumSoftwareSlots(0, macro))
    assert(finite(numslots) and numslots <= 128 and numslots % 1 == 0, 'software_slots_invalid')
    local slots = ffi.new('SoftwareSlot[?]', numslots)
    local actualslots = tonumber(ffi.C.GetSoftwareSlots(slots, numslots, 0, macro))
    assert(finite(actualslots) and actualslots <= numslots, 'software_slots_invalid')
    for index = 0, actualslots - 1 do
        local maxware, current = ffi.string(slots[index].max), ffi.string(slots[index].current)
        assert(not baseline[maxware], 'software_slot_duplicate')
        baseline[maxware] = current
        softwareslots[#softwareslots+1] = {maxsoftware=maxware, currentsoftware=current}
    end
    local selected, softwarewares = {}, {}
    for index = 0, tonumber(loadout.numsoftware) - 1 do
        local ware = ffi.string(loadout.software[index].ware)
        if ware ~= '' then
            local maxware = ffi.string(ffi.C.GetSoftwareMaxCompatibleVersion(0, macro, ware))
            assert(baseline[maxware] ~= nil and not selected[maxware], 'software_slot_invalid')
            selected[maxware] = ware
            softwarewares[#softwarewares+1] = ware
        end
    end
    -- getDataAndDisplay fills missing software slots with native defaults.
    -- Reuse its IsSoftwareDefault/predecessor path, keeping the same payload
    -- for subsequent pricing and the ordinary build call.
    for index = 0, actualslots - 1 do
        local maxware = ffi.string(slots[index].max)
        if not selected[maxware] then
            local n = tonumber(ffi.C.GetNumSoftwarePredecessors(maxware))
            assert(finite(n) and n <= 32 and n % 1 == 0, 'software_predecessors_invalid')
            local predecessors = ffi.new('const char*[?]', n)
            local actual = tonumber(ffi.C.GetSoftwarePredecessors(predecessors, n, maxware))
            assert(finite(actual) and actual <= n, 'software_predecessors_invalid')
            local default
            for predecessor = 0, actual - 1 do
                local ware = ffi.string(predecessors[predecessor])
                if ffi.C.IsSoftwareDefault(0, macro, ware) then default = ware end
            end
            if ffi.C.IsSoftwareDefault(0, macro, maxware) then default = maxware end
            if default then selected[maxware]=default; softwarewares[#softwarewares+1]=default end
        end
    end
    assert(#softwarewares <= 2048, 'software_count_invalid')
    local normalized = ffi.new('UILoadoutSoftwareData[?]', #softwarewares)
    for index, ware in ipairs(softwarewares) do normalized[index-1].ware=ware end
    loadout.software=normalized; loadout.numsoftware=#softwarewares
    keepalive[#keepalive+1]=normalized; keepalive[#keepalive+1]=softwarewares
    local function add(ware, amount, issoftware)
        if amount == 0 then return end
        assert(type(ware) == 'string' and #ware > 0 and #ware <= 256, 'ware_missing')
        assert(finite(amount) and amount % 1 == 0, 'amount_invalid')
        local basket = issoftware and software or wares
        basket[ware] = (basket[ware] or 0) + amount
    end
    add(GetMacroData(macro, 'ware'), 1)
    for _, category in ipairs(categories) do
        for index = 0, tonumber(loadout['num' .. category]) - 1 do
            local entry = loadout[category][index]
            if category == 'crew' then
                crewcount = crewcount + tonumber(entry.count)
            elseif category == 'software' then
                local ware = ffi.string(entry.ware)
                if ware ~= '' then
                    add(ware, 1, true)
                    local maxware = ffi.string(ffi.C.GetSoftwareMaxCompatibleVersion(0, macro, ware))
                    assert(baseline[maxware] ~= nil, 'software_slot_missing')
                    if baseline[maxware] ~= '' then
                        local current = baseline[maxware]
                        software[current] = (software[current] or 0) - 1
                    end
                end
            else
                local item = ffi.string(entry.macro)
                if item ~= '' then
                    local amount = (category == 'ammo' or category == 'units') and tonumber(entry.amount)
                        or ((category == 'turretgroups' or category == 'shieldgroups') and tonumber(entry.count) or 1)
                    add(GetMacroData(item, 'ware'), amount)
                end
            end
        end
    end
    local thruster = ffi.string(loadout.thruster.macro)
    if thruster ~= '' then add(GetMacroData(thruster, 'ware'), 1) end
    assert(finite(crewcount) and crewcount <= 2048 and crewcount % 1 == 0, 'crew_count_invalid')
    local price, crewprice, rawprice, parts = calculate_price(shipyard, wares, software, crewcount)
    return {price=price, crewprice=crewprice, paid=price + crewprice,
            loadout=loadout, wares=wares, software=software, crewcount=crewcount, _ffi=keepalive,
            rawprice=rawprice, price_parts=parts, software_slots=softwareslots, macro=macro}
end
function M.generate(shipyard, macro, level)
    if type(shipyard) ~= 'userdata' or type(macro) ~= 'string' or #macro == 0 or #macro > 256
       or not finite(level) or level > 1 then return nil, 'invalid_quote_request' end
    local ok, result = pcall(generate, shipyard, macro, level)
    if not ok then return nil, 'native_quote_error', tostring(result):sub(1, 256) end
    quotes[result] = {shipyard=shipyard, wares=result.wares, software=result.software, crewcount=result.crewcount,
        macro=macro, loadout=result.loadout, software_slots=result.software_slots, keepalive=result._ffi}
    return result
end
function M.to_plan(shipyard, quote)
    local context = quotes[quote]
    if not context or not IsSameComponent(context.shipyard, shipyard) then return nil, 'invalid_quote_request' end
    local ok, plan = pcall(function()
        local softwaredata = {}
        for _, upgrade in ipairs(Helper.upgradetypes) do
            if upgrade.supertype == 'software' then softwaredata[upgrade.type] = context.software_slots end
        end
        return Helper.convertLoadout(0, context.macro, context.loadout, softwaredata, 'UILoadout2')
    end)
    if not ok then return nil, 'native_plan_error', tostring(plan):sub(1, 256) end
    return plan
end
function M.reprice(shipyard, quote)
    local context = quotes[quote]
    if not context or not IsSameComponent(context.shipyard, shipyard) then return nil, 'invalid_quote_request' end
    local ok, price, crewprice, rawprice, parts = pcall(calculate_price, shipyard,
        context.wares, context.software, context.crewcount)
    if not ok then return nil, 'native_quote_error', tostring(price):sub(1, 256) end
    return {price=price, crewprice=crewprice, paid=price+crewprice, rawprice=rawprice, price_parts=parts}
end
-- Та же цена игрового меню для пополнения конкретных расходников.
-- Этот путь не генерирует полный loadout и не меняет оснащение корабля.
local supplyquotes = setmetatable({}, {__mode='k'})
function M.quote_supply(shipyard, wares)
    if type(shipyard) ~= 'userdata' or type(wares) ~= 'table' then
        return nil, 'invalid_supply_quote_request'
    end
    local items, count = {}, 0
    for ware, amount in pairs(wares) do
        if type(ware) ~= 'string' or #ware == 0 or #ware > 256
            or not finite(amount) or amount <= 0 or amount % 1 ~= 0 then
            return nil, 'invalid_supply_amount'
        end
        count = count + 1
        if count > 32 then return nil, 'supply_quote_batch_exceeded' end
        items[ware] = amount
    end
    if count == 0 then return nil, 'empty_supply_quote' end
    local ok, price, crewprice, rawprice, parts = pcall(calculate_price,
        shipyard, items, {}, 0)
    if not ok then return nil, 'native_supply_quote_error', tostring(price):sub(1, 256) end
    local quote = {price=price, paid=price, rawprice=rawprice, price_parts=parts,
        requires_resources=true}
    supplyquotes[quote] = {shipyard=shipyard, items=items}
    return quote
end
function M.reprice_supply(shipyard, quote)
    local context = supplyquotes[quote]
    if not context or not IsSameComponent(context.shipyard, shipyard) then
        return nil, 'invalid_supply_quote_request'
    end
    return M.quote_supply(shipyard, context.items)
end
Register_Require_With_Init('extensions.tm_empire_management.ui.purchase_quote', M, function() end)
