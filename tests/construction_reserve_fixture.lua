-- Real Lua 5.1, mocked native reservation boundary; no engine qualification.
local sector, station = newproxy(true), newproxy(true)
local board, calls, throws, wrongsize = {}, 0, false, false
local function clone(value)
    if type(value) ~= 'table' then return value end
    local result = {}; for key, item in pairs(value) do result[key] = clone(item) end
    return result
end
local C = {
    GetPlayerID=function() return 7 end,
    ReserveBuildPlot=function(id, faction, set, position, x, y, z)
        calls = calls + 1
        assert(board['$tm_empire_reservation_receipt'].state == 'reservation_sent')
        assert(id == 10 and faction == 'player' and set == 'argon')
        assert(position.x == 123 and x == 2000 and y == 1000 and z == 2000)
        if throws then error('lost response') end
        return 20
    end,
    GetContextByClass=function() return 10 end,
    GetBuildPlotSize=function() return {x=wrongsize and 3000 or 2000, y=1000, z=2000} end,
    GetObjectPositionInSector=function() return {x=123,y=0,z=0} end,
}
package.preload.ffi=function() return {C=C, cdef=function() end, new=function() return {} end} end
ConvertStringToLuaID=function(value) return value == '20' and station or 7 end
ConvertIDTo64Bit=function(value) assert(value == sector); return 10 end
GetComponentData=function(value) assert(value == station); return true end
GetNPCBlackboard=function(_, key) return clone(board[key]) end
SetNPCBlackboard=function(_, key, value) board[key] = clone(value) end
local registeredReserve
Register_Require_With_Init=function(name, module, init)
    assert(name=='extensions.tm_empire_management.ui.construction_reserve')
    registeredReserve=module; init()
end
local reserve = dofile('X4_TopManager/ui/construction_reserve.lua')
assert(registeredReserve==reserve)
local function request(key)
    return {key=key, sector=sector, set='argon', position={x=123,y=0,z=0}, size={x=2000,y=1000,z=2000}}
end
assert(reserve.reserve(request('revoked'), function() return false end) == nil and calls == 0)
local receipt = reserve.reserve(request('first'), function() return true end)
assert(receipt.state == 'reserved' and receipt.station == station and calls == 1)
reserve.reserve(request('first'), function() return true end); assert(calls == 1)
assert(reserve.reserve(request('blocked'), function() return true end) == nil and calls == 1)
board['$tm_empire_reservation_receipt'].state = 'reconciled'
wrongsize = true
assert(reserve.reserve(request('size_changed'), function() return true end).state == 'unknown')
reserve.reserve(request('size_changed'), function() return true end); assert(calls == 2)
board['$tm_empire_reservation_receipt'].state = 'reconciled'
throws = true
assert(reserve.reserve(request('lost'), function() return true end).state == 'unknown')
reserve.reserve(request('lost'), function() return true end); assert(calls == 3)
local invalid = request('invalid'); invalid.position.x = 0/0
assert(reserve.reserve(invalid, function() return true end) == nil and calls == 3)
-- Exercise the registered MD dispatcher, including an approval changed after read.
package.loaded['extensions.tm_empire_management.ui.construction_reserve'] = reserve
local dispatcher, registrations, events = nil, {}, 0
RegisterEvent=function(name, callback) registrations[name] = callback end
Register_Require_With_Init=function(_, module, init) dispatcher = module; init() end
AddUITriggeredEvent=function(screen, control)
    assert(screen == 'TM_Empire_Construction' and control == 'StationPlotSubmitted')
    events = events + 1
end
dofile('X4_TopManager/ui/construction_plot_dispatch.lua')
assert(registrations['TM_Empire.ReserveStationPlot'] == dispatcher.reserve)
board = {}; throws = false; wrongsize = false
local approved = request('dispatcher'); approved.schema, approved.state = 1, 'approved'
board['$tm_empire_reservation_request'] = approved
dispatcher.reserve()
assert(board['$tm_empire_reservation_request'].state == 'reserved' and calls == 4 and events == 1)
dispatcher.reserve(); assert(calls == 4 and events == 1)
board = {}; approved = request('changed'); approved.schema, approved.state = 1, 'approved'
board['$tm_empire_reservation_request'] = approved
local reads = 0
GetNPCBlackboard=function(_, key)
    if key == '$tm_empire_reservation_request' then
        reads = reads + 1
        if reads == 2 then board[key].position.x = 456 end
    end
    return clone(board[key])
end
dispatcher.reserve()
assert(calls == 4 and board['$tm_empire_reservation_request'].state == 'revoked')
board = {}
C.GetObjectPositionInSector=function() return {x=124,y=0,z=0} end
assert(reserve.reserve(request('wrong_position'), function() return true end).state == 'unknown')
local after_position = calls
reserve.reserve(request('wrong_position'), function() return true end)
assert(calls == after_position)
