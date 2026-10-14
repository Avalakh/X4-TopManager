local playerOrderReason
package.preload['extensions.tm_empire_management.ui.player_order_guard']=function() return {reason=function() return playerOrderReason end} end
local ship, yard, build = newproxy(true), newproxy(true), newproxy(true)
local bb, money, transfers, records, events = {}, 1000, 0, 0, 0
local controlled = 0
local quotedWares
local C = {GetPlayerID=function() return 1 end,
    GetTopLevelContainer=function(id) assert(id==2); return 3 end,
    GetBuildTaskInfo=function(id) return {id=id, component=2, buildingcontainer=3, price=100, factionid='player'} end,
    SetBuildTaskTransferredMoney=function(id, paid) assert(id==4 and paid==100); records=records+1 end}
package.preload.ffi=function() return {C=C,cdef=function() end,string=function(v) return v end} end
C.GetPlayerControlledShipID=function() return controlled end
package.preload['extensions.tm_empire_management.ui.purchase_quote']=function()
    return {quote_supply=function(_, wares) quotedWares=wares; return {price=100,requires_resources=true} end,
        reprice_supply=function() return {price=100} end}
end
function ConvertStringToLuaID() return 1 end
function ConvertIDTo64Bit(v) return v==ship and 2 or v==yard and 3 or 4 end
function IsSameComponent(left, right) return left==right end
function GetNPCBlackboard(_,key) return bb[key] end
function SetNPCBlackboard(_,key,value) bb[key]=value end
function GetComponentData(value) assert(value==ship, 'GetComponentData requires the Lua component ID'); return true end
C.IsComponentOperational=function() return true end
function GetPlayerMoney() return money end
function TransferPlayerMoneyTo(paid,id)
    assert(bb['$tm_empire_supply_payment'].state=='payment_sent' and id==3)
    transfers=transfers+1; money=money-paid
end
function AddUITriggeredEvent() events=events+1 end
function RegisterEvent() end
local api
function Register_Require_With_Init(_,module) api=module end
dofile('X4_TopManager/ui/purchase_dispatch.lua')
local function prepare(key)
    bb['$tm_empire_supply_request']={schema=1,state='quote_requested',key=key,
        ship=ship,shipyard=yard,wares={satellite=1},budget=100}
    api.prepare_supply()
    bb['$tm_empire_supply_request'].state='payment_approved'
end
prepare('helm'); controlled=2; api.pay_supply()
assert(transfers==0 and bb['$tm_empire_supply_request'].reason=='player_helm')
controlled=0 -- A passenger does not change GetPlayerControlledShipID.
prepare('one'); api.pay_supply(); api.pay_supply()
assert(transfers==1 and money==900 and bb['$tm_empire_supply_payment'].state=='paid')
bb['$tm_empire_supply_payment'].build=build
bb['$tm_empire_supply_payment'].buildtoken='0x4'
api.record_supply_payment(); api.record_supply_payment()
assert(records==1 and bb['$tm_empire_supply_payment'].state=='build_recorded'
    and bb['$tm_empire_supply_payment'].recordedbuild=='0x4')
prepare('two'); api.pay_supply(); assert(transfers==1)
bb['$tm_empire_supply_payment'].state='consumed'
TransferPlayerMoneyTo=function() transfers=transfers+1; error('unknown payment outcome') end
api.pay_supply(); api.pay_supply()
assert(transfers==2 and bb['$tm_empire_supply_payment'].state=='unknown')
prepare('three'); api.pay_supply(); assert(transfers==2)
-- Reload loses the in-memory quote cache but retains the durable payment.
dofile('X4_TopManager/ui/purchase_dispatch.lua')
prepare('three'); api.pay_supply(); assert(transfers==2)
bb['$tm_empire_supply_payment']={schema=1,key='three',state='payment_sent'}
api.pay_supply(); assert(transfers==2)
print('PASS: durable supply payment, single record, unresolved payment blocks replay')

bb['$tm_empire_supply_payment']=nil; prepare('queued_manual')
local beforeGuard=transfers; playerOrderReason='manual_or_priority_order'; api.pay_supply()
assert(transfers==beforeGuard and bb['$tm_empire_supply_request'].reason==playerOrderReason)

-- A real MD wire request carries the ware ID as a value, not a table key.
bb['$tm_empire_supply_request']={schema=1,state='quote_requested',key='md_wire',
    ship=ship,shipyard=yard,ware='satellite_mk1',amount=1,budget=100}
api.prepare_supply()
assert(quotedWares.satellite_mk1==1 and next(quotedWares,'satellite_mk1')==nil)
assert(bb['$tm_empire_supply_request'].state=='quote_ready')
print('PASS: MD ware value converted to native supply price map')
