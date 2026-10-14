local playerOrderReason
package.preload['extensions.tm_empire_management.ui.player_order_guard']=function() return {reason=function() return playerOrderReason end} end
-- Contract-level negative/replay checks; native game success is tested separately.
local realffi=require('ffi')
local seed=realffi.new('uint64_t',123)
local source,target,player=newproxy(true),newproxy(true),newproxy(true)
local bb,events={},{}
local effects,checks,controlled,owns,allowed=0,0,0,true,true
local operational=true
local C={
 GetPlayerID=function() return 9 end,
 GetPlayerControlledShipID=function() return controlled end,
 IsComponentOperational=function() return operational end,
 IsPerson=function(person,ship) return ship==1 and person==seed end,
 IsPersonTransferScheduled=function() return false end,
 GetPersonRole=function() return 'service' end,
 PerformCrewExchange2=function(s,t,people,n,reverse,rn,lc,rc,exchange,check)
  assert(s==1 and t==2 and n==1 and rn==0 and lc==0 and rc==0 and not exchange)
  assert(people[0]==seed)
  if check then checks=checks+1 else effects=effects+1 end
  return {reason=allowed and '' or 'destination_full'}
 end,
}
local proxy=setmetatable({C=C},{__index=realffi})
local originalrequire=require
require=function(name) if name=='ffi' then return proxy end return originalrequire(name) end
ConvertStringToLuaID=function() return player end
ConvertIDTo64Bit=function(v) return v==source and 1 or v==target and 2 or 0 end
IsSameComponent=function(left,right) return left==right end
GetComponentData=function() return owns end
GetNPCBlackboard=function(p,k) assert(p==player); return bb[k] end
SetNPCBlackboard=function(p,k,v) assert(p==player); bb[k]=v end
AddUITriggeredEvent=function(s,e) assert(s=='TM_Empire_Personnel'); events[#events+1]=e end
RegisterEvent=function() end
local api
Register_Require_With_Init=function(_,m) api=m end
dofile('X4_TopManager/ui/personnel_transfer.lua')
local function request(key)
 bb['$tm_empire_crew_exchange_request']={schema=1,state='check_requested',key=key,source=source,target=target,seed='123',role='service'}
 return bb['$tm_empire_crew_exchange_request']
end
local function state() return bb['$tm_empire_crew_exchange_result'].state end
local r=request('helm'); controlled=1; api.check(); assert(state()=='rejected_before_effect' and effects==0)
controlled=0; owns=false; request('ownership'); api.check(); assert(state()=='rejected_before_effect' and effects==0)
owns=true; allowed=false; request('capacity'); api.check(); assert(state()=='rejected_before_effect' and effects==0)
allowed=true; r=request('approval'); api.check(); assert(state()=='checked' and effects==0)
operational=false; r.state='approved'; api.submit(); assert(state()=='rejected_before_effect' and effects==0)
operational=true; r=request('approval_restored'); api.check(); assert(state()=='checked' and effects==0)
api.submit(); assert(effects==0) -- MD authorization is required.
r.state='approved'; controlled=2; api.submit(); assert(state()=='rejected_before_effect' and effects==0)
controlled=0; r=request('once'); api.check(); r.state='approved'; api.submit(); assert(state()=='sent' and effects==1)
api.submit(); api.check(); assert(effects==1) -- Duplicate events cannot repeat an effect.
r=request('uncertain'); api.check(); r.state='approved'; bb['$tm_empire_crew_exchange_result'].state='unknown'; api.submit(); assert(effects==1)
assert(checks>=4)
require=originalrequire
owns=0; request('numeric_unowned'); api.check(); assert(state()=='rejected_before_effect' and effects==1)
owns=true
for _,field in ipairs({'source','target','seed','role'}) do
 r=request('changed_'..field); api.check(); r.state='approved'
 r[field]=field=='seed' and '124' or field=='role' and 'marine' or newproxy(true)
 api.submit()
 assert(state()=='rejected_before_effect' and effects==1)
 assert(bb['$tm_empire_crew_exchange_result'].reason=='crew_approval_binding_changed')
end

r=request('queued_after_check'); api.check(); r.state='approved'
playerOrderReason='manual_or_priority_order'; api.submit()
assert(state()=='rejected_before_effect' and effects==1)
assert(bb['$tm_empire_crew_exchange_result'].reason=='manual_or_priority_order')
playerOrderReason=nil
r=request('revoked_after_check'); api.check(); assert(state()=='checked')
r.state='revoked'; api.submit(); api.check()
assert(state()=='checked' and effects==1) -- A queued Lua event cannot use revoked MD approval.
