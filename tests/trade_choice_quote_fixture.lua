-- Historical fixture: station-manager decision evaluation was removed.
-- This is a retired scenario, not a passing release gate.
print('SKIP retired station-manager trade-choice quote fixture')
do return end
local player, ship, station, seller, offer = newproxy(), newproxy(), newproxy(), newproxy(), newproxy()
local board, module, permitted, revoked = {}, nil, true, false
package.preload.ffi = function() return {C={GetPlayerID=function() return player end}} end
function ConvertStringToLuaID() return player end
local nativeShip = {}
function ConvertIDTo64Bit(value) assert(value==ship); return nativeShip end
function IsSameComponent(a,b) return a==b end
function GetComponentData(value) assert(value==ship, 'GetComponentData requires the Lua component ID'); return true, station end
function IsValidTrade() return true end
function CanTradeWith(_, value) assert(value==nativeShip); return permitted end
function GetTradeData(_, value) assert(value==nativeShip); return {isselloffer=true, station=seller, price=80.8, amount=12, minamount=1} end
function GetNPCBlackboard(_, key)
    if revoked and key=='$tm_empire_trade_quote_request' then
        local request=board[key]
        if request and request.seen then return {state='pending',key='changed',ship=ship,station=station} end
        if request then request.seen=true end
    end
    return board[key]
end
function SetNPCBlackboard(_, key, value) board[key]=value end
function AddUITriggeredEvent(screen,control)
    assert(screen=='TM_Empire_Assets' and control=='TradeQuotesObserved')
end
function Register_Require_With_Init(_, value) module=value end
function RegisterEvent() end
local function prepare()
    board={['$tm_empire_trade_quote_request']={state='pending',key='choice_1',ship=ship,station=station,
        offers={{offer=offer,seller=seller,amount=10}}}}
    permitted,revoked=true,false
end
dofile('X4_TopManager/ui/trade_choice_quote.lua')
prepare(); module.quote()
local response=board['$tm_empire_trade_quote_response']
assert(response.key=='choice_1' and response.quotes[1].state=='observed' and response.quotes[1].price==80.8)
prepare(); permitted=false; module.quote()
assert(board['$tm_empire_trade_quote_response'].quotes[1].state=='unknown')
prepare(); revoked=true; module.quote()
assert(not board['$tm_empire_trade_quote_response'])
prepare(); GetTradeData=function() return {isselloffer=true,station=seller,price=0/0,amount=12,minamount=1} end
module.quote(); assert(board['$tm_empire_trade_quote_response'].quotes[1].state=='unknown')
prepare(); GetTradeData=function() return {isselloffer=true,station=station,price=80.8,amount=12,minamount=1} end
module.quote(); assert(board['$tm_empire_trade_quote_response'].quotes[1].state=='unknown')
print('PASS: native quoted price, permission, binding, NaN and seller identity; no trade effects')
