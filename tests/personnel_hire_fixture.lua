local playerOrderReason
package.preload['extensions.tm_empire_management.ui.player_order_guard']=function() return {reason=function() return playerOrderReason end} end
-- Native hiring financial boundary; real Lua5.1, mocked engine only.
local actor, source = newproxy(true), newproxy(true)
local target = newproxy(true)
local controlled, targetOwned, targetOperational = 0, true, true
local actorAlias, sourceAlias = newproxy(true), newproxy(true)
IsSameComponent = function(left,right)
    return left==right or (left==actorAlias and right==actor)
        or (left==sourceAlias and right==source)
end
local board, money, transfers, events, raw, partial = {}, 1000, 0, 0, 100, false
local approvalChanges, approvalReads = nil, 0
local function clone(value)
    if type(value) ~= 'table' then return value end
    local result = {}; for key, item in pairs(value) do result[key] = clone(item) end
    return result
end
package.preload.ffi = function() return {cdef=function() end,C={GetPlayerID=function() return 7 end,
    GetPlayerControlledShipID=function() return controlled end,
    IsComponentOperational=function(id) assert(id==11); return targetOperational end}} end
ConvertStringToLuaID = function(value) return tonumber(value) end
ConvertIDTo64Bit = function(value) if value==target then return 11 end; assert(value == source); return 10 end
GetContextByClass = function(value) assert(value == actor); return source end
GetComponentData = function(value, field)
    assert(type(value)=='userdata')
    if value==target then assert(field=='isplayerowned'); return targetOwned end
    assert(value == source); return {{amount=20}}
end
GetNPCBlackboard = function(value, key)
    if value == actor then assert(key == '$HiringFee'); return raw end
    if key=='$tm_empire_hire_request' then
        approvalReads=approvalReads+1
        if approvalChanges and approvalReads==2 then
            board[key][approvalChanges.field]=approvalChanges.value
        end
    end
    return clone(board[key])
end
SetNPCBlackboard = function(_, key, value) board[key] = clone(value) end
RoundTotalTradePrice = function(value) return value end
GetPlayerMoney = function() return money end
TransferPlayerMoneyTo = function(amount, destination)
    assert(destination == 10); transfers = transfers + 1
    money = money - (partial and amount / 2 or amount)
end
AddUITriggeredEvent = function(screen, control)
    assert(screen == 'TM_Empire_Personnel' and control == 'HirePaid'); events = events + 1
end
RegisterEvent = function() end
local hire
Register_Require_With_Init = function(_, module) hire = module end
dofile('X4_TopManager/ui/personnel_hire.lua')
local function request(key)
    approvalReads=0
    board['$tm_empire_hire_request'] = {schema=1, state='approved', key=key,
        actor=actor, source=source, target=target, fee=100, budget=100}
end
request('helm'); controlled=11; hire.pay()
assert(transfers==0 and board['$tm_empire_hire_request'].reason=='player_helm')
controlled=0; request('lost'); targetOwned=false; hire.pay()
assert(transfers==0 and board['$tm_empire_hire_request'].reason=='hiring_destination_lost')
targetOwned=true; targetOperational=false; request('inactive'); hire.pay()
assert(transfers==0 and board['$tm_empire_hire_request'].reason=='hiring_destination_lost')
targetOperational=true; events=0; request('first'); hire.pay()
assert(transfers == 1 and money == 920 and events == 1)
assert(board['$tm_empire_hire_payment'].state == 'paid')
hire.pay(); request('second'); hire.pay(); assert(transfers == 1)
board['$tm_empire_hire_payment'].state = 'reconciled'
request('first'); hire.pay(); assert(transfers == 1) -- exact-key replay
request('fee_changed'); raw = 101; hire.pay(); raw = 100
assert(transfers == 1 and board['$tm_empire_hire_request'].state == 'rejected_before_payment')
request('poor'); money = 20; hire.pay(); assert(transfers == 1)
request('revoked'); board['$tm_empire_hire_request'].state = 'revoked'; hire.pay()
assert(transfers == 1)
request('partial'); money = 1000; partial = true; hire.pay()
assert(transfers == 2 and board['$tm_empire_hire_payment'].state == 'unknown')
assert(board['$tm_empire_hire_payment'].paid==0 and board['$tm_empire_hire_payment'].amount==80)
request('retry_unknown'); hire.pay(); assert(transfers == 2)
board['$tm_empire_hire_payment'].state = 'reconciled'
request('free'); raw = 0; money = 0; partial = false
board['$tm_empire_hire_request'].fee = 0
board['$tm_empire_hire_request'].budget = 0
hire.pay()
assert(board['$tm_empire_hire_payment'].state == 'paid')
assert(board['$tm_empire_hire_payment'].paid == 0 and money == 0)
local after_free = transfers
hire.pay(); assert(transfers == after_free)
board['$tm_empire_hire_payment'].state='reconciled'
request('fractional_discount'); raw=101; money=1000
board['$tm_empire_hire_request'].fee=101
hire.pay()
assert(board['$tm_empire_hire_payment'].state=='paid')
assert(math.abs(board['$tm_empire_hire_payment'].paid-80.8)<0.005)
local after_fractional=transfers
board['$tm_empire_hire_payment'].state='reconciled'
request('nan_budget'); board['$tm_empire_hire_request'].budget=0/0; hire.pay()
assert(transfers==after_fractional)
for _,change in ipairs({{field='actor',value=newproxy(true)},
    {field='source',value=newproxy(true)},{field='target',value=newproxy(true)},{field='fee',value=999},
    {field='budget',value=99}}) do
    request('changed_'..change.field)
    board['$tm_empire_hire_request'].fee=raw
    approvalChanges=change
    hire.pay()
    assert(transfers==after_fractional)
    assert(board['$tm_empire_hire_request'].reason=='hire_approval_revoked')
end
approvalChanges=nil
for _,change in ipairs({{field='actor',value=actorAlias},{field='source',value=sourceAlias}}) do
    request('same_component_'..change.field)
    board['$tm_empire_hire_request'].fee=raw
    approvalChanges=change
    hire.pay()
    assert(board['$tm_empire_hire_payment'].state=='paid')
    board['$tm_empire_hire_payment'].state='reconciled'
end
approvalChanges=nil

request('queued_manual'); board['$tm_empire_hire_request'].fee=raw
local beforeGuard=transfers; playerOrderReason='manual_or_priority_order'; hire.pay()
assert(transfers==beforeGuard and board['$tm_empire_hire_request'].reason==playerOrderReason)
