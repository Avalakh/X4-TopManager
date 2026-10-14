-- Recruit stock service crew through the same ship-configuration build order
-- used by equipment docks. MD selects/guards the donor and owns the receipt.
local ffi = require('ffi')
ffi.cdef[[uint64_t GetPlayerControlledShipID(void);]]
local planBuilder = require('extensions.tm_empire_management.ui.crew_service_plan')
local playerOrders = require('extensions.tm_empire_management.ui.player_order_guard')
local M = {}

local function owner()
    return ConvertStringToLuaID(tostring(ffi.C.GetPlayerID()))
end

local function sameRequest(a, b)
    return type(a) == 'table' and a.schema == 1 and a.state == 'approved'
        and a.key == b.key and a.amount == b.amount and a.budget == b.budget
        and type(a.ship) == 'userdata' and type(a.yard) == 'userdata'
        and IsSameComponent(a.ship, b.ship) and IsSameComponent(a.yard, b.yard)
end

local function reject(player, request, reason)
    request.state, request.reason = 'rejected_before_payment', reason
    SetNPCBlackboard(player, '$tm_empire_crew_service_request', request)
    AddUITriggeredEvent('TM_Empire_Personnel', 'CrewServiceSubmitted')
end

function M.submit()
    local player = owner()
    local request = GetNPCBlackboard(player, '$tm_empire_crew_service_request')
    if type(request) ~= 'table' or request.schema ~= 1 or request.state ~= 'approved'
        or type(request.key) ~= 'string' or #request.key > 128
        or type(request.ship) ~= 'userdata' or type(request.yard) ~= 'userdata'
        or type(request.amount) ~= 'number' or request.amount < 1
        or request.amount > 16 or request.amount % 1 ~= 0
        or type(request.budget) ~= 'number' or request.budget < 1 then return end
    local previous = GetNPCBlackboard(player, '$tm_empire_crew_service_receipt')
    if type(previous) == 'table' and previous.state ~= 'observed' then
        return reject(player, request, 'previous_crew_service_unreconciled')
    end
    local shipid = ConvertIDTo64Bit(request.ship)
    local owned = GetComponentData(request.ship, 'isplayerowned')
    if (owned ~= true and owned ~= 1) or not ffi.C.IsComponentOperational(shipid)
        or ffi.C.GetPlayerControlledShipID() == shipid
        or playerOrders.reason(request.ship) then
        return reject(player, request, 'crew_service_ship_unavailable')
    end
    local yard
    local candidates = {request.yard}
    if type(request.yards) == 'table' then
        for _, candidate in ipairs(request.yards) do
            if type(candidate) == 'userdata' then candidates[#candidates+1] = candidate end
        end
    end
    for _, candidate in ipairs(candidates) do
        local id = ConvertIDTo64Bit(candidate)
        if ffi.C.IsComponentOperational(id) and ffi.C.CanContainerEquipShip(id, shipid) then
            yard = candidate
            break
        end
    end
    if not yard then
        return reject(player, request, 'no_compatible_equipment_dock')
    end
    request.yard = yard
    SetNPCBlackboard(player, '$tm_empire_crew_service_request', request)
    local yardid = ConvertIDTo64Bit(yard)
    local plan, reason, detail = planBuilder.snapshot(request.ship, request.amount)
    if not plan then return reject(player, request, reason) end
    local workforce = ffi.C.GetWorkForceInfo(yardid, '')
    local available, maximum = tonumber(workforce.available), tonumber(workforce.maxavailable)
    if not maximum or maximum <= 0 or not available or available < 0
        or available > maximum then return reject(player, request, 'dock_workforce_unknown') end
    local minprice, maxprice = GetWareData('crew', 'minprice', 'maxprice')
    if type(minprice) ~= 'number' or type(maxprice) ~= 'number'
        or minprice <= 0 or maxprice < minprice then
        return reject(player, request, 'crew_price_unknown')
    end
    local discount = 1
    local discounts = GetComponentData(request.yard, 'hiringdiscounts')
    if type(discounts) ~= 'table' then return reject(player, request, 'hiring_discount_unknown') end
    for _, entry in ipairs(discounts) do
        if type(entry.amount) ~= 'number' or entry.amount < 0 or entry.amount > 100 then
            return reject(player, request, 'hiring_discount_invalid')
        end
        discount = discount - entry.amount / 100
    end
    if discount < 0 or discount > 1 then return reject(player, request, 'hiring_discount_invalid') end
    local unit = RoundTotalTradePrice(Helper.round(discount
        * ffi.C.GetContainerBuildPriceFactor(yardid)
        * (maxprice - available / maximum * (maxprice - minprice))))
    local paid = unit * request.amount
    if paid <= 0 or paid > request.budget or paid > 1000000
        or GetPlayerMoney() < paid then return reject(player, request, 'crew_service_budget') end
    require('extensions.tm_empire_management.ui.purchase_receipt')
    local crewplan = {hireddetails={{newrole='service', amount=request.amount,
        price=unit}}, fired={}, transferdetails={}}
    local receipt = {schema=1, key=request.key, state='prepared', ship=request.ship,
        yard=request.yard, amount=request.amount, paid=paid, before=GetPlayerMoney(),
        engine=detail.engine, servicebefore=detail.crew - request.amount}
    local ok, err = pcall(function()
        Helper.callLoadoutFunction(plan, crewplan, function(loadout, crew)
            assert(sameRequest(GetNPCBlackboard(player, '$tm_empire_crew_service_request'), request),
                'crew_service_approval_revoked')
            assert(ffi.C.GetPlayerControlledShipID() ~= shipid
                and ffi.C.CanContainerEquipShip(yardid, shipid)
                and not playerOrders.reason(request.ship), 'crew_service_ship_changed')
            assert(tonumber(loadout.numengines) > 0 and tonumber(crew.numadded) == 1
                and tonumber(crew.added[0].amount) == request.amount,
                'crew_service_loadout_incomplete')
            assert(GetPlayerMoney() >= paid, 'crew_service_money_changed')
            receipt.state = 'payment_sent'
            SetNPCBlackboard(player, '$tm_empire_crew_service_receipt', receipt)
            TransferPlayerMoneyTo(paid, yardid)
            assert(receipt.before - GetPlayerMoney() == paid, 'crew_service_payment_unknown')
            local id = ffi.C.AddBuildTask6(yardid, shipid, '', loadout, 0, crew,
                false, '', ffi.new('AddBuildTask6Container'))
            assert(id ~= 0, 'crew_service_build_unknown_after_payment')
            receipt.id = tostring(id)
            SetNPCBlackboard(player, '$tm_empire_crew_service_receipt', receipt)
            local info = ffi.C.GetBuildTaskInfo(id)
            assert(info.id == id and info.buildingcontainer == yardid,
                'crew_service_build_identity_unknown')
            ffi.C.SetBuildTaskTransferredMoney(id, paid)
            receipt.state = 'built'
            SetNPCBlackboard(player, '$tm_empire_crew_service_receipt', receipt)
        end, nil, 'UILoadout2')
    end)
    if not ok then
        receipt.reason = tostring(err):sub(1, 256)
        if receipt.state == 'prepared' then
            return reject(player, request, receipt.reason)
        end
        receipt.state = 'unknown'
        SetNPCBlackboard(player, '$tm_empire_crew_service_receipt', receipt)
    end
    request.state = receipt.state
    request.reason = receipt.reason
    SetNPCBlackboard(player, '$tm_empire_crew_service_request', request)
    AddUITriggeredEvent('TM_Empire_Personnel', 'CrewServiceSubmitted')
end

function M.init()
    RegisterEvent('TM_Empire.HireServiceCrew', M.submit)
end
Register_Require_With_Init('extensions.tm_empire_management.ui.crew_service_hire', M, M.init)
return M
