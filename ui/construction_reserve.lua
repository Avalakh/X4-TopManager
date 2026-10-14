-- MapMenu.onRenderTargetSelect: reserve an empty player plot, never modules.
-- The MD caller must approve native placement and blueprint validation first.
local ffi = require('ffi')
ffi.cdef[[UniverseID ReserveBuildPlot(UniverseID sectorid, const char* factionid, const char* set, UIPosRot location, float x, float y, float z);]]
local M = {}
local function finite(value)
    return type(value) == 'number' and value == value and math.abs(value) < math.huge
end
local function vector(value, positive)
    if type(value) ~= 'table' then return false end
    for _, axis in ipairs({'x', 'y', 'z'}) do
        if not finite(value[axis]) or (positive and value[axis] <= 0) then return false end
    end
    return true
end
function M.reserve(request, canAct)
    if type(request) ~= 'table' or type(request.key) ~= 'string'
        or type(request.sector) ~= 'userdata' or type(request.set) ~= 'string'
        or not vector(request.position) or not vector(request.size, true)
        or type(canAct) ~= 'function' then return nil, 'invalid_reservation_request' end
    local player = ConvertStringToLuaID(tostring(ffi.C.GetPlayerID()))
    local previous = GetNPCBlackboard(player, '$tm_empire_reservation_receipt')
    if type(previous) == 'table' then
        if previous.key == request.key then return previous, 'reservation_already_issued' end
        if previous.state ~= 'reconciled' then return nil, 'previous_reservation_unreconciled' end
    end
    if not canAct() then return nil, 'reservation_approval_revoked' end
    local sector = ConvertIDTo64Bit(request.sector)
    local position = ffi.new('UIPosRot')
    position.x, position.y, position.z = request.position.x, request.position.y, request.position.z
    -- Persist intent before crossing the engine boundary; unknown never retries.
    local receipt = {schema=1, key=request.key, state='reservation_sent', sector=request.sector,
        position=request.position, size=request.size, set=request.set}
    SetNPCBlackboard(player, '$tm_empire_reservation_receipt', receipt)
    local ok, station = pcall(ffi.C.ReserveBuildPlot, sector, 'player', request.set,
        position, request.size.x, request.size.y, request.size.z)
    if ok and station ~= nil and station ~= 0 then
        receipt.station = ConvertStringToLuaID(tostring(station))
        local observed, own, actualSector, size, actualPosition = pcall(function()
            return GetComponentData(receipt.station, 'isplayerowned'),
                ffi.C.GetContextByClass(station, 'sector', false), ffi.C.GetBuildPlotSize(station),
                ffi.C.GetObjectPositionInSector(station)
        end)
        if observed and (own == true or own == 1) and actualSector == sector
            and size.x == request.size.x and size.y == request.size.y and size.z == request.size.z
            and actualPosition.x == position.x and actualPosition.y == position.y and actualPosition.z == position.z then
            receipt.state = 'reserved'
        else
            receipt.state, receipt.reason = 'unknown', 'reserved_plot_not_confirmed'
        end
    else
        receipt.state, receipt.reason = 'unknown', 'native_reservation_unconfirmed'
    end
    SetNPCBlackboard(player, '$tm_empire_reservation_receipt', receipt)
    return receipt
end
Register_Require_With_Init('extensions.tm_empire_management.ui.construction_reserve', M, function() end)
return M
