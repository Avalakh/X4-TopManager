local yard, api = newproxy(true), nil
local owned, available, maxavailable, valid, calls = false, 50, 100, true, 0
local oversized, negative = false, false
local pricechange = 0
local baseline, default = '', false
local payload = {thruster={macro='thruster'}}
for _, category in ipairs({'weapons','turrets','shields','engines','turretgroups','shieldgroups','ammo','units','software','crew'}) do
    payload['num' .. category]=0; payload[category]={}
end
payload.numengines=1; payload.engines[0]={macro='engine'}
payload.numturretgroups=1; payload.turretgroups[0]={macro='turret',count=2}
payload.numammo=1; payload.ammo[0]={macro='ammo',amount=4}
payload.numsoftware=1; payload.software[0]={ware='software'}
payload.numcrew=1; payload.crew[0]={roleid='service',count=3}
local C={
    IsComponentClass=function(id,class) assert(id==10 and class=='station'); return true end,
    CanGenerateValidLoadout=function(id,macro) assert(id==10 and macro=='ship'); return valid end,
    GenerateShipLoadoutCounts2=function(counts)
        for key,value in pairs(payload) do if key:sub(1,3)=='num' then counts[key]=value end end
        if oversized then counts.numengines=2049 end
    end,
    GenerateShipLoadout2=function() calls=calls+1 end,
    GetBuildWarePrice=function(_,ware)
        assert(ware~='software' and ware~='ammo'); return negative and -1 or (({ship=1000,engine=100,turret=50,thruster=40})[ware] + (ware=='engine' and pricechange or 0))
    end,
    GetContainerBuildPriceFactor=function() return 1.2 end,
    GetWorkForceInfo=function() return {available=available,maxavailable=maxavailable} end,
    GetNumSoftwareSlots=function() return 1 end,
    GetSoftwareSlots=function(buf) buf[0]={max='software',current=baseline}; return 1 end,
    GetSoftwareMaxCompatibleVersion=function() return 'software' end,
    GetNumSoftwarePredecessors=function() return 0 end,
    GetSoftwarePredecessors=function() return 0 end,
    IsSoftwareDefault=function() return default end,
}
package.preload.ffi=function() return {C=C,cdef=function() end,string=function(s) return s end,
    new=function(ctype,n)
        if ctype=='SoftwareSlot[?]' or ctype=='const char*[?]' then return {} end
        if ctype=='UILoadoutSoftwareData[?]' then local t={}; for i=0,n-1 do t[i]={} end; return t end
        assert(ctype=='int64_t'); return math.floor(n)
    end} end
ConvertIDTo64Bit=function(id) assert(id==yard); return 10 end
IsSameComponent=function(left, right) return left==right end
GetMacroData=function(macro,key) assert(key=='ware'); return macro end
GetWareData=function(ware,key,second)
    if key=='volatile' then return ware=='ammo' end
    assert(ware=='crew' and key=='minprice' and second=='maxprice'); return 100,200
end
GetContainerWarePrice=function(id,ware,sell) assert(id==yard and ware=='software' and sell==false); return 100 end
GetComponentData=function(id,key)
    assert(id==yard)
    if key=='isplayerowned' then return owned end
    if key=='discounts' then return {{amount=10,applytoshipsales=true},{amount=50,applytoshipsales=false}} end
    assert(key=='hiringdiscounts'); return {{amount=20}}
end
Helper={ffiTempStorage={},round=function(n) return math.floor(n+.5) end,
    upgradetypes={{type='software',supertype='software'}},
    convertLoadout=function(object,macro,loadout,softwaredata,kind)
        assert(object==0 and macro=='ship' and loadout==payload and kind=='UILoadout2')
        assert(softwaredata.software[1].maxsoftware=='software')
        return {software={loadout.software[0].ware}}
    end,
    getLoadoutHelper2=function(generator,counts,kind,id,object,macro,level)
        assert(kind=='UILoadout2' and id==10 and object==0 and macro=='ship' and level==.5)
        counts({},id,object,macro,level); generator()
        Helper.ffiTempStorage[#Helper.ffiTempStorage+1]=payload
        return payload
    end}
Register_Require_With_Init=function(_,module,init) api=module; init() end
RoundTotalTradePrice=function(price) return math.ceil(price) end
assert(loadfile('X4_TopManager/ui/purchase_quote.lua'))()
local quote, reason, detail=api.generate(yard,'ship',.5)
assert(quote, detail or reason)
assert(quote.loadout==payload and quote.wares.turret==2 and quote.wares.ammo==4)
assert(quote.software.software==1 and quote.price==1348 and quote.crewprice==432 and quote.paid==1780)
assert(quote._ffi[1]==payload)
assert(api.to_plan(yard,quote).software[1]=='software')
assert(not api.to_plan(newproxy(true),quote)); assert(not api.to_plan(yard,{}))
Helper.ffiTempStorage={}; assert(quote._ffi[1]==payload)
pricechange=1
local fresh=assert(api.reprice(yard,quote))
assert(fresh.price==1349 and fresh.paid==1781 and quote.price==1348)
assert(quote.loadout==payload and calls==1)
assert(not api.reprice(newproxy(true),quote)); assert(not api.reprice(yard,{}))
pricechange=0
payload.numsoftware=0; default=true
quote=assert(api.generate(yard,'ship',.5)); assert(quote.price==1348 and quote.loadout.numsoftware==1)
default=false
baseline='software'; quote=assert(api.generate(yard,'ship',.5))
assert(quote.software.software==0 and quote.price==1240 and quote.paid==1672)
baseline=''
owned=true; quote=assert(api.generate(yard,'ship',.5)); assert(quote.price==0 and quote.paid==0)
owned=false; maxavailable=0; assert(not api.generate(yard,'ship',.5)); maxavailable=100
negative=true; assert(not api.generate(yard,'ship',.5)); negative=false
local before=calls; oversized=true; assert(not api.generate(yard,'ship',.5)); assert(calls==before); oversized=false
valid=false; assert(not api.generate(yard,'ship',.5)); valid=true
assert(not api.generate(10,'ship',.5)); assert(not api.generate(yard,'ship',0/0))
assert(not api.generate(yard,'ship',2)); assert(not api.generate(yard,'',.5))
local supplycalls=calls
local supply=assert(api.quote_supply(yard,{engine=1}))
assert(supply.price==100 and supply.requires_resources and calls==supplycalls)
pricechange=1
assert(api.reprice_supply(yard,supply).price==101 and supply.price==100)
pricechange=0
assert(not api.quote_supply(yard,{}))
assert(not api.quote_supply(yard,{engine=.5}))
assert(not api.reprice_supply(newproxy(true),supply))
owned=true
assert(api.quote_supply(yard,{engine=1}).paid==0)
owned=false
