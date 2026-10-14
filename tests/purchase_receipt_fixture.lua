local actor, build, other = newproxy(true), newproxy(true), newproxy(true)
local ids={[actor]=10,[build]=20,[other]=30}
local pending, info, api, callback
local writes=0
package.preload.ffi=function() return {
    cdef=function() end, string=function(s) return s end,
    C={GetPlayerID=function() return 7 end,
       GetBuildTaskInfo=function(id) assert(id==20); return info end,
       SetBuildTaskTransferredMoney=function(id,value) assert(id==20 and value==pending.paid); writes=writes+1 end}
} end
ConvertIDTo64Bit=function(id) assert(ids[id]); return ids[id] end
ConvertStringToLuaID=function(id) return tonumber(id) end
GetNPCBlackboard=function(id,key) assert(id==7 and key=='$tm_empire_purchase'); return pending end
RegisterEvent=function(name, fn) assert(name=='TM_Empire.RecordPaidBuild'); callback=fn end
Register_Require_With_Init=function(_, module, init) api=module; init() end
assert(loadfile('X4_TopManager/ui/purchase_receipt.lua'))()
pending={schema=1,state='payment_sent',build=build,shipyard=actor,paid=500,price=500,crewprice=0,macro='ship_macro'}
info={id=20,buildingcontainer=10,price=500,factionid='player',macro='ship_macro'}
assert(callback(nil,actor) and writes==1)
-- Native build.price excludes paid crew; transferredamount includes it.
pending.crewprice=50; pending.paid=550
assert(callback(nil,actor) and writes==2)
pending.price=550; assert(not callback(nil,actor)); pending.price=500
pending.crewprice=-50; assert(not callback(nil,actor))
pending.crewprice=0; pending.paid=500
-- No raw numeric identifiers, no wrong shipyard/faction/amount or duplicates
-- through a stage that has already been reconciled by MD.
assert(not callback(nil,other))
info.factionid='argon'; assert(not callback(nil,actor)); info.factionid='player'
info.price=499; assert(not callback(nil,actor)); info.price=500
pending.state='observed'; assert(not callback(nil,actor)); pending.state='payment_sent'
pending.paid=499; assert(not callback(nil,actor)); pending.paid=500
pending.build=20; assert(not callback(nil,actor)); pending.build=build
info.id=0; assert(not callback(nil,actor)); info.id=20
pending.paid=0/0; assert(not api.valid(pending))
assert(writes==2)
