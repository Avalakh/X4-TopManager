local ship,station,storage=newproxy(true),newproxy(true),newproxy(true)
local board,money,fee,transfers,orders={},1000,100,0,0
local busy,partial,failOrder,revoked=false,false,false,false
local function copy(v) if type(v)~='table' then return v end local r={} for k,x in pairs(v) do r[k]=copy(x) end return r end
package.preload.ffi=function() return {cdef=function() end,C={
 GetPlayerID=function() return 7 end,IsComponentOperational=function() return true end,
 IsBuilderBusy=function() return busy end,GetNumOrders=function() return 0 end,
 IsOrderSelectableFor=function() return true end,GetBuilderHiringFee=function() return fee end,
 CreateDeployToStationOrder=function() orders=orders+1; if failOrder then return 0 end return 1 end,
 EnableOrder=function() return true end}} end
ConvertStringToLuaID=function(v) return tonumber(v) end
ConvertIDTo64Bit=function(v) if v==ship then return 10 elseif v==station then return 11 elseif v==storage then return 12 end error('bad id') end
IsSameComponent=function(a,b) return a==b end
GetComponentData=function(id,...) assert(id==ship or id==station or id==storage); local r={} for i=1,select('#',...) do local k=select(i,...) r[i]=k=='isplayerowned' and id~=ship or false end return unpack(r) end
GetNPCBlackboard=function(_,k) local r=copy(board[k]); if revoked and k=='$tm_empire_builder_request' and r then if revoked=='next' then r.state='revoked' else revoked='next' end end return r end
SetNPCBlackboard=function(_,k,v) board[k]=copy(v) end
GetPlayerMoney=function() return money end
TransferPlayerMoneyTo=function(amount,id) assert(id==10 and board['$tm_empire_builder_result'].state=='unknown'); transfers=transfers+1; money=money-(partial and amount/2 or amount) end
SetOrderParam=function(component,index,param,_,destination)
 assert(board['$tm_empire_builder_result'].paid==fee)
 assert(component==ship and index==1 and param==1 and destination==station)
end
AddUITriggeredEvent=function() end; RegisterEvent=function() end
local module; Register_Require_With_Init=function(_,m) module=m end
dofile('X4_TopManager/ui/construction_builder.lua')
local function prepare(key)
 board={}; money=1000
 board['$tm_empire_builder_request']={schema=1,state='check_requested',key=key,ship=ship,station=station,storage=storage,budget=500}
 module.quote(); local r=board['$tm_empire_builder_request']; r.state='approved'; r.fee=100
end
prepare('success'); module.submit(); assert(transfers==1 and orders==1 and money==900 and board['$tm_empire_builder_result'].state=='sent')
module.submit(); assert(transfers==1)
prepare('fee_change'); fee=101; module.submit(); assert(transfers==1 and board['$tm_empire_builder_result'].state=='rejected_before_effect'); fee=100
prepare('busy'); busy=true; module.submit(); busy=false; assert(transfers==1)
prepare('revoked'); revoked=true; module.submit(); revoked=false; assert(transfers==1)
prepare('partial'); partial=true; module.submit(); partial=false; assert(transfers==2 and orders==1 and board['$tm_empire_builder_result'].state=='unknown'); module.submit(); assert(transfers==2)
prepare('order_failure'); failOrder=true; module.submit(); failOrder=false; assert(transfers==3 and board['$tm_empire_builder_result'].paid==100 and board['$tm_empire_builder_result'].state=='unknown'); module.submit(); assert(transfers==3)
prepare('fractional_budget'); board['$tm_empire_builder_request'].budget=500.25; module.submit(); assert(transfers==4 and board['$tm_empire_builder_result'].state=='sent')
local function legacy(key)
 prepare(key); module.submit()
 local r=board['$tm_empire_builder_result']; r.destination_version=nil
 board['$tm_empire_builder_request'].state='recovery_approved'
 return r
end
local r=legacy('legacy_paid'); local paidTransfers,oldOrders,balance=transfers,orders,money
module.recover(); assert(transfers==paidTransfers and money==balance and orders==oldOrders+1)
assert(board['$tm_empire_builder_result'].state=='sent' and board['$tm_empire_builder_result'].recovery_attempted)
module.recover(); assert(orders==oldOrders+1 and transfers==paidTransfers)
r=legacy('legacy_partial'); r.paid=fee/2; oldOrders=orders; module.recover(); assert(orders==oldOrders)
r=legacy('legacy_busy'); busy=true; oldOrders=orders; module.recover(); busy=false; assert(orders==oldOrders and not r.recovery_attempted)
r=legacy('legacy_failed'); failOrder=true; oldOrders=orders; paidTransfers=transfers
module.recover(); failOrder=false; module.recover()
assert(orders==oldOrders+1 and transfers==paidTransfers and board['$tm_empire_builder_result'].state=='unknown')
r=legacy('legacy_wrong_key'); r.key='other'; oldOrders=orders; module.recover(); assert(orders==oldOrders)
r=legacy('legacy_revoked'); board['$tm_empire_builder_request'].state='revoked'
oldOrders=orders; paidTransfers=transfers; module.recover()
assert(orders==oldOrders and transfers==paidTransfers and not r.recovery_attempted)
prepare('current_paid'); module.submit(); board['$tm_empire_builder_request'].state='recovery_approved'; oldOrders=orders
module.recover(); assert(orders==oldOrders)
-- Native MD/UI boundaries may expose boolean flags as 0/1.
local nativeData=GetComponentData
GetComponentData=function(id,...)
 local values={nativeData(id,...)}
 for i=1,select('#',...) do values[i]=values[i] and 1 or 0 end
 return unpack(values)
end
prepare('numeric_flags'); local oldTransfers=transfers; oldOrders=orders
module.submit(); assert(transfers==oldTransfers+1 and orders==oldOrders+1 and board['$tm_empire_builder_result'].state=='sent')
local numericData=GetComponentData
GetComponentData=function(id,...)
 if id==station then return 0 end
 return numericData(id,...)
end
board={}; board['$tm_empire_builder_request']={schema=1,state='check_requested',key='numeric_unowned',ship=ship,station=station,storage=storage,budget=500}
oldTransfers=transfers; oldOrders=orders; module.quote()
assert(board['$tm_empire_builder_result'].state=='rejected_before_effect' and transfers==oldTransfers and orders==oldOrders)
