local playerOrderReason
package.preload['extensions.tm_empire_management.ui.player_order_guard']=function() return {reason=function() return playerOrderReason end} end
-- Whole acquisition transaction boundary; no engine payment/build effects.
local yard, build, wrongbuild = newproxy(true), newproxy(true), newproxy(true)
local ids = {[yard]=10, [build]=20, [wrongbuild]=21}
local board, money, transfers, builds, records = {}, 1000, 0, 0, 0
local failBuild, partialPayment, wrongIdentity = false, false, false
local quote = {macro='ship', loadout={numsoftware=2}}
local function clone(value)
    if type(value) ~= 'table' then return value end
    local copy = {}; for key, item in pairs(value) do copy[key]=clone(item) end
    return copy
end
local native = {
    GetPlayerID=function() return 7 end,
    AddBuildTask6=function(y, ship, macro, loadout, price)
        assert(y==10 and ship==0 and macro=='ship' and price==100)
        builds=builds+1; return failBuild and 0 or 20
    end,
    GetBuildTaskInfo=function(id)
        return {id=id, buildingcontainer=10, price=100,
            factionid=wrongIdentity and 'argon' or 'player', macro='ship'}
    end,
    SetBuildTaskTransferredMoney=function(id, amount)
        assert(id==20 and amount==100); records=records+1
    end,
}
package.preload.ffi=function() return {C=native, cdef=function() end, new=function() return {} end,
    string=function(value) return value end, cast=function(_, value) return value end} end
package.preload['extensions.tm_empire_management.ui.purchase_receipt']=function() return {} end
package.preload['extensions.tm_empire_management.ui.purchase_quote']=function() return {
    to_plan=function(y, q) assert(y==yard and q==quote); return {} end,
    reprice=function(y, q) assert(y==yard and q==quote); return {price=100,crewprice=0,paid=100} end,
} end
ConvertStringToLuaID=function(value) return tonumber(value) end
ConvertIDTo64Bit=function(value) assert(ids[value]); return ids[value] end
GetNPCBlackboard=function(_, key) return clone(board[key]) end
SetNPCBlackboard=function(_, key, value) board[key]=clone(value) end
GetPlayerMoney=function() return money end
TransferPlayerMoneyTo=function(amount, y)
    assert(y==10); transfers=transfers+1
    money=money-(partialPayment and amount/2 or amount)
end
Helper={callLoadoutFunction=function(_, _, callback) return callback(quote.loadout,{}) end}
local registeredPurchase
function Register_Require_With_Init(name, module, init)
    assert(name=='extensions.tm_empire_management.ui.purchase_submit')
    registeredPurchase=module
    init()
end
local purchase=assert(loadfile('X4_TopManager/ui/purchase_submit.lua'))()
assert(registeredPurchase==purchase)
local function request(key) return {key=key, shipyard=yard, macro='ship', budget=500} end
local receipt=assert(purchase.submit(request('ok'), quote, function() return true end))
assert(receipt.state=='built' and money==900 and transfers==1 and builds==1 and records==1)
local duplicate, reason=purchase.submit(request('another'),quote,function() return true end)
assert(not duplicate and reason=='previous_purchase_unreconciled' and transfers==1)
assert(purchase.match(receipt,{build=build,shipyard=yard}))
local matched, mismatch=purchase.match(receipt,{build=wrongbuild,shipyard=yard})
assert(not matched and mismatch=='build_id_mismatch')
wrongIdentity=true; assert(not purchase.match(receipt,{build=build,shipyard=yard})); wrongIdentity=false
board['$tm_empire_purchase_submission']=nil
money=50
assert(not purchase.submit(request('poor'),quote,function() return true end) and transfers==1)
money=1000
local checks=0
assert(not purchase.submit(request('lost-governor'),quote,function() checks=checks+1; return checks==1 end))
assert(transfers==1 and builds==1 and not board['$tm_empire_purchase_submission'])
failBuild=true
receipt=assert(purchase.submit(request('build-failure'),quote,function() return true end))
assert(receipt.state=='unknown' and transfers==2 and builds==2 and records==1)
assert(not purchase.submit(request('retry-after-unknown'),quote,function() return true end))
assert(transfers==2)
board['$tm_empire_purchase_submission']=nil
failBuild=false; partialPayment=true; money=1000
receipt=assert(purchase.submit(request('partial-payment'),quote,function() return true end))
assert(receipt.state=='unknown' and transfers==3 and builds==2)
assert(not purchase.submit(request('retry-partial'),quote,function() return true end) and transfers==3)

-- Each blackboard read may return a distinct wrapper for the same engine ID.
-- Exercise the real dispatch authorization before the payment/build boundary.
partialPayment=false; money=1000; board={}
local function wrapped(value)
    if type(value)=='userdata' then
        local proxy=newproxy(true); ids[proxy]=ids[value]; return proxy
    end
    if type(value)~='table' then return value end
    local out={}; for k,v in pairs(value) do out[k]=wrapped(v) end; return out
end
GetNPCBlackboard=function(_, key) return wrapped(board[key]) end
IsSameComponent=function(left,right) return ids[left] and ids[left]==ids[right] end
local pricing= require('extensions.tm_empire_management.ui.purchase_quote')
pricing.generate=function(y, macro) assert(ids[y]==10 and macro=='ship'); return quote end
pricing.to_plan=function(y, q) assert(ids[y]==10 and q==quote); return {} end
pricing.reprice=function(y, q) assert(ids[y]==10 and q==quote); return {price=100,crewprice=0,paid=100} end
package.loaded['extensions.tm_empire_management.ui.purchase_submit']=purchase
local dispatch
Register_Require_With_Init=function(_, module, init) dispatch=module; init() end
RegisterEvent=function() end
AddUITriggeredEvent=function() end
assert(loadfile('X4_TopManager/ui/purchase_dispatch.lua'))()
board['$tm_empire_purchase_request']=request('dispatch-wrapper'); board['$tm_empire_purchase_request'].schema=1
board['$tm_empire_purchase_request'].state='quote_requested'
dispatch.prepare(); board['$tm_empire_purchase_request'].state='approved'; dispatch.submit()
assert(board['$tm_empire_purchase_submission'].state=='built' and transfers==4 and builds==3 and money==900)
board['$tm_empire_purchase_candidates']={{build=build,shipyard=yard}}
dispatch.match()
local match=board['$tm_empire_purchase_match']
assert(match.candidateindex==1 and match.id=='20' and match.build==nil)
board['$tm_empire_purchase_submission']=nil
board['$tm_empire_purchase_request']=request('dispatch-changed-yard')
board['$tm_empire_purchase_request'].schema=1; board['$tm_empire_purchase_request'].state='quote_requested'
dispatch.prepare(); board['$tm_empire_purchase_request'].state='approved'
local reads=0
GetNPCBlackboard=function(_, key)
    local value=wrapped(board[key])
    if key=='$tm_empire_purchase_request' then
        reads=reads+1
        if reads>1 then local wrong=newproxy(true); ids[wrong]=11; value.shipyard=wrong end
    end
    return value
end
dispatch.submit()
assert(board['$tm_empire_purchase_request'].reason=='manager_unavailable' and transfers==4 and builds==3)
