-- MapMenu.buttonBuyPlot: native price/payment/licence for an existing plot.
-- Geometry selection and the Manager's construction decisions stay in MD.
local ffi = require('ffi')
ffi.cdef[[UniverseID GetSectorControlStation(UniverseID sectorid);]]
local M = {}
local function enabled(value) return value == true or value == 1 end
local function integer(value)
    return type(value) == 'number' and value >= 0 and value <= 9007199254740991 and value % 1 == 0
end
-- Read-only native quote. MD then rechecks its unchanged plot snapshot and
-- can_safely_extend_build_plot immediately before the geometry effect.
function M.quote(request)
    if type(request) ~= 'table' or type(request.station) ~= 'userdata'
        or not integer(request.budget) then return nil, 'invalid_plot_quote_request' end
    local own = GetComponentData(request.station, 'isplayerowned')
    if own ~= true and own ~= 1 then return nil, 'plot_not_player_owned' end
    local station = ConvertIDTo64Bit(request.station)
    if not ffi.C.IsComponentOperational(station) and not enabled(request.newconstruction) then return nil, 'plot_station_unavailable' end
    if enabled(request.newconstruction) and enabled(request.extend) then return nil, 'new_station_plot_extension_not_allowed' end
    local sectorID = GetComponentData(request.station, 'sectorid')
    if not sectorID then return nil, 'plot_sector_unavailable' end
    local sector = ConvertIDTo64Bit(sectorID)
    if sector == 0 then return nil, 'plot_sector_unavailable' end
    local owner = GetComponentData(sectorID, 'owner')
    if type(owner) ~= 'string' then return nil, 'plot_sector_owner_unavailable' end
    -- Helper.getPlotData/updatePlotSize use the same native free-licence rule.
    local free = owner == 'ownerless' or owner == 'xenon' or owner == 'player'
    local current = ffi.C.GetBuildPlotSize(station)
    local center = ffi.C.GetBuildPlotCenterOffset(station)
    if current.x <= 0 or current.y <= 0 or current.z <= 0 then return nil, 'native_plot_geometry_unavailable' end
    local size = {x=current.x, y=current.y, z=current.z}
    if enabled(request.extend) then size.x, size.y, size.z = size.x+2000, size.y+1000, size.z+2000 end
    local changed = ffi.new('bool[1]', false)
    local credit = tonumber(ffi.C.GetBuildPlotPayment(station, changed))
    -- Stock MapMenu.plotModeUpdatePrice still quotes a moved plot. The flag
    -- describes the old payment's position; it does not prohibit buying the
    -- current geometry. Native credit and the fresh price determine the gap.
    local full = tonumber(ffi.C.GetBuildPlotPrice(sector,
        ffi.C.GetObjectPositionInSector(station), size.x, size.y, size.z, 'player'))
    if not integer(full) or not integer(credit) then return nil, 'native_plot_quote_invalid' end
    local price = free and 0 or math.max(0, full-credit)
    if price > request.budget or GetPlayerMoney() < price then return nil, 'plot_licence_budget_missing' end
    return {fullprice=full, credit=credit, price=price, free=free, owner=owner,
        size=size, center={x=center.x,y=center.y,z=center.z},
        oldsize={x=current.x,y=current.y,z=current.z}}
end
function M.license(request, canAct)
    if type(request) ~= 'table' or type(request.key) ~= 'string'
        or #request.key == 0 or #request.key > 128
        or type(request.station) ~= 'userdata' or type(request.budget) ~= 'number'
        or request.budget < 0 or request.budget > 9007199254740991
        or request.budget % 1 ~= 0 or type(canAct) ~= 'function' then
        return nil, 'invalid_plot_licence_request'
    end
    local player = ConvertStringToLuaID(tostring(ffi.C.GetPlayerID()))
    local previous = GetNPCBlackboard(player, '$tm_empire_plot_receipt')
    if type(previous) == 'table' and (previous.key == request.key
        or previous.state ~= 'reconciled') then return nil, 'previous_plot_effect_unreconciled' end
    if not canAct(request) then return nil, 'plot_goal_unavailable' end
    local owned = GetComponentData(request.station, 'isplayerowned')
    if owned ~= true and owned ~= 1 then return nil, 'plot_not_player_owned' end
    local station = ConvertIDTo64Bit(request.station)
    if not ffi.C.IsComponentOperational(station) and not enabled(request.newconstruction) then return nil, 'plot_station_unavailable' end
    local sectorID = GetComponentData(request.station, 'sectorid')
    if not sectorID then return nil, 'plot_sector_unavailable' end
    local sector = ConvertIDTo64Bit(sectorID)
    -- Geometry was already committed in MD. Always quote the current size.
    local quote, failure = M.quote({station=request.station,budget=request.budget,newconstruction=request.newconstruction})
    if not quote then return nil, failure end
    local size, center = quote.size, quote.center
    if type(request.expected) == 'table' then
        local expected = request.expected
        if type(expected.size) ~= 'table' or type(expected.center) ~= 'table'
            or expected.fullprice ~= quote.fullprice or expected.credit ~= quote.credit
            or (expected.free ~= true and expected.free ~= false and expected.free ~= 0 and expected.free ~= 1)
            or enabled(expected.free) ~= quote.free or expected.owner ~= quote.owner
            or expected.size.x ~= size.x or expected.size.y ~= size.y or expected.size.z ~= size.z
            or expected.center.x ~= center.x or expected.center.y ~= center.y or expected.center.z ~= center.z then
            return nil, 'quoted_plot_geometry_or_price_changed'
        end
    end
    local changed = ffi.new('bool[1]', false)
    local full, credit, price = quote.fullprice, quote.credit, quote.price
    -- Recheck lifecycle and unchanged geometry immediately before effects.
    local current = ffi.C.GetBuildPlotSize(station)
    local offset = ffi.C.GetBuildPlotCenterOffset(station)
    if not canAct(request) or current.x ~= size.x or current.y ~= size.y or current.z ~= size.z
        or offset.x ~= center.x or offset.y ~= center.y or offset.z ~= center.z then
        return nil, 'plot_geometry_or_goal_changed'
    end
    local control = ffi.C.GetSectorControlStation(sector)
    if price > 0 and control == 0 then return nil, 'plot_licence_recipient_unavailable' end
    local receipt = {schema=1, key=request.key, station=request.station, state='licence_sent',
        amount=price, paid=0, fullprice=full, credit=credit, free=quote.free,
        size={x=size.x,y=size.y,z=size.z}, center={x=center.x,y=center.y,z=center.z}}
    SetNPCBlackboard(player, '$tm_empire_plot_receipt', receipt)
    local ok, reason = pcall(function()
        if price > 0 then
            local before = GetPlayerMoney()
            receipt.moneybefore=before
            receipt.state = 'payment_sent'
            SetNPCBlackboard(player, '$tm_empire_plot_receipt', receipt)
            TransferPlayerMoneyTo(price, ConvertStringTo64Bit(tostring(control)))
            receipt.moneyafter=GetPlayerMoney()
            assert(before - receipt.moneyafter == price, 'plot_payment_unknown')
            receipt.paid=price
        end
        ffi.C.PayBuildPlotSize(station, size, center)
        local payment = tonumber(ffi.C.GetBuildPlotPayment(station, changed))
        local paidSize = ffi.C.GetPaidBuildPlotSize(station)
        local paidCenter = ffi.C.GetPaidBuildPlotCenterOffset(station)
        assert(not changed[0] and (quote.free or payment >= full) and paidSize.x == size.x
            and paidSize.y == size.y and paidSize.z == size.z
            and paidCenter.x == center.x and paidCenter.y == center.y and paidCenter.z == center.z,
            'native_plot_licence_unconfirmed')
        receipt.state = 'reconciled'
    end)
    if not ok then receipt.state, receipt.reason = 'unknown', tostring(reason):sub(1,256) end
    SetNPCBlackboard(player, '$tm_empire_plot_receipt', receipt)
    return receipt
end
Register_Require_With_Init('extensions.tm_empire_management.ui.construction_plot', M, function() end)
return M
