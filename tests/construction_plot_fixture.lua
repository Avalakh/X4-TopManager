-- Whole native licence boundary with value-copy receipts; no game effects.
local station = newproxy(true)
local sectorID = newproxy(true)
local board, money, credit, transfers, licences = {}, 1000, 100, 0, 0
local partial, badLicence, owned = false, false, true
local operational = true
local positionChanged = false
local sectorOwner, sectorOwned = 'argon', false
local size, center = {x=1000,y=1000,z=1000}, {x=0,y=0,z=0}
local paidSize, paidCenter = size, center
local function copy(value)
    if type(value) ~= 'table' then return value end
    local out = {}; for key, item in pairs(value) do out[key] = copy(item) end; return out
end
local native = {
    GetPlayerID=function() return 7 end,
    IsComponentOperational=function() return operational end,
    GetContextByClass=function() error('Use stock sectorid bridge for Lua component data') end,
    GetBuildPlotSize=function() return size end,
    GetBuildPlotCenterOffset=function() return center end,
    GetBuildPlotPayment=function(_, changed) changed[0]=positionChanged; return credit end,
    GetBuildPlotPrice=function() return 200 end,
    GetObjectPositionInSector=function() return {} end,
    GetSectorControlStation=function() return 30 end,
    GetPaidBuildPlotSize=function() return paidSize end,
    GetPaidBuildPlotCenterOffset=function() return paidCenter end,
    PayBuildPlotSize=function()
        licences=licences+1
        if not badLicence then
            positionChanged=false
            credit=(sectorOwner=='ownerless' or sectorOwner=='xenon' or sectorOwned) and 0 or 200
            paidSize, paidCenter=size, center
        else paidSize={x=1,y=1,z=1} end
    end,
}
package.preload.ffi=function() return {C=native,cdef=function() end,
    new=function() return {[0]=false} end} end
ConvertStringToLuaID=function(value) return tonumber(value) end
ConvertStringTo64Bit=function(value) return tonumber(value) end
ConvertIDTo64Bit=function(value) if value==sectorID then return 20 end; assert(value==station); return 10 end
IsSameComponent=function(left,right) return left==right end
GetComponentData=function(component,field)
    assert(type(component)=='userdata', 'GetComponentData requires a Lua component ID')
    if component==sectorID then assert(field=='owner'); return sectorOwner, sectorOwned end
    assert(component==station); if field=='sectorid' then return sectorID end; return owned
end
GetNPCBlackboard=function(_, key) return copy(board[key]) end
SetNPCBlackboard=function(_, key, value) board[key]=copy(value) end
GetPlayerMoney=function() return money end
TransferPlayerMoneyTo=function(price, recipient)
    assert(price==100 and recipient==30); transfers=transfers+1
    money=money-(partial and price/2 or price)
end
local registeredPlot
Register_Require_With_Init=function(name, module, init)
    assert(name=='extensions.tm_empire_management.ui.construction_plot')
    registeredPlot=module; init()
end
local plot=dofile('X4_TopManager/ui/construction_plot.lua')
assert(registeredPlot==plot)
local function req(key) return {key=key,station=station,budget=200} end
local receipt=plot.license(req('ok'),function() return true end)
assert(receipt.state=='reconciled' and receipt.paid==100 and money==900 and licences==1)
assert(receipt.amount==100 and receipt.moneybefore==1000 and receipt.moneyafter==900)
assert(not plot.license(req('ok'),function() return true end) and transfers==1)
board={}; credit=100; money=50
assert(not plot.license(req('poor'),function() return true end) and transfers==1)
money=1000; local checks=0
assert(not plot.license(req('revoked'),function() checks=checks+1; return checks==1 end))
assert(transfers==1 and licences==1)
owned=false; assert(not plot.license(req('foreign'),function() return true end)); owned=true
partial=true; receipt=plot.license(req('partial'),function() return true end)
assert(receipt.state=='unknown' and transfers==2 and licences==1)
assert(receipt.amount==100 and receipt.paid==0 and receipt.moneybefore==1000 and receipt.moneyafter==950)
assert(not plot.license(req('retry'),function() return true end) and transfers==2)
board={}; money=1000; partial=false; badLicence=true
receipt=plot.license(req('licence_missing'),function() return true end)
assert(receipt.state=='unknown' and transfers==3 and licences==2)
assert(receipt.paid==100 and receipt.moneybefore==1000 and receipt.moneyafter==900)
assert(not plot.license(req('licence_retry'),function() return true end) and transfers==3)
-- Stock free licence rule: no recipient payment in own/ownerless/xenon space.
badLicence=false; paidSize=size; paidCenter=center
for _, owner in ipairs({'ownerless','xenon','player'}) do
    board={}; sectorOwner=owner; sectorOwned=(owner=='player'); money=0; credit=0
    receipt=plot.license({key='free_'..owner,station=station,budget=0},function() return true end)
    assert(receipt.state=='reconciled' and receipt.paid==0 and credit==0 and transfers==3)
end
-- Extension quote is read-only and must agree with the post-MD geometry.
board={}; sectorOwner='argon'; sectorOwned=false; money=1000; credit=100
local quote=plot.quote({station=station,budget=200,extend=true})
assert(quote.size.x==3000 and quote.size.y==2000 and quote.size.z==3000)
assert(size.x==1000 and transfers==3)
assert(not plot.license({key='unextended',station=station,budget=200,expected=quote},function() return true end))
assert(transfers==3)
size=quote.size; paidSize=size
receipt=plot.license({key='extended',station=station,budget=200,expected=quote},function() return true end)
assert(receipt.state=='reconciled' and transfers==4)
-- Exercise the registered quote -> MD-approved -> licence bridge as well.
-- Geometry/approval below represent the MD boundary, not live MD execution.
package.preload['extensions.tm_empire_management.ui.construction_plot']=function() return plot end
local dispatch, events
RegisterEvent=function() end
Register_Require_With_Init=function(_, module) dispatch=module end
AddUITriggeredEvent=function(screen, event)
    assert(screen=='TM_Empire_Construction'); events=event
end
dofile('X4_TopManager/ui/construction_plot_dispatch.lua')
board={}; credit=100; money=1000
board['$tm_empire_plot_request']={schema=1,key='dispatch',station=station,budget=200,
    state='quote_requested',extend=1}
dispatch.quote()
assert(events=='PlotQuoteReady' and transfers==4)
assert(board['$tm_empire_plot_request'].state=='quote_ready')
size=copy(board['$tm_empire_plot_request'].quote.size)
board['$tm_empire_plot_request'].state='licence_approved'
dispatch.license()
assert(events=='PlotLicenceSubmitted' and transfers==5)
assert(board['$tm_empire_plot_receipt'].state=='reconciled')
dispatch.license(); assert(transfers==5)
-- Licence for the exact adopted new-station approval; no extension or replay.
board={}; credit=100; money=1000; operational=false
assert(not plot.quote({station=station,budget=200,newconstruction=0}))
assert(not plot.quote({station=station,budget=200,newconstruction=2}))
assert(not plot.quote({station=station,budget=200,newconstruction=1,extend=1}))
board['$tm_empire_plot_request']={schema=1,key='new_station',station=station,budget=200,
    state='quote_requested',extend=0,newconstruction=1}
dispatch.quote(); assert(board['$tm_empire_plot_request'].state=='quote_ready')
board['$tm_empire_plot_request'].quote.free=0
board['$tm_empire_plot_request'].state='licence_approved'
dispatch.license(); assert(transfers==6 and board['$tm_empire_plot_receipt'].state=='reconciled')
dispatch.license(); assert(transfers==6)
board={}; credit=100; money=1000; operational=true
board['$tm_empire_plot_request']={schema=1,key='revoked_dispatch',station=station,budget=200,
    state='quote_requested',extend=false}
dispatch.quote(); board['$tm_empire_plot_request'].state='revoked'
dispatch.license(); assert(transfers==6)
-- A moved native plot may be purchased at its fresh price, as in MapMenu.
board={}; credit=100; money=1000; operational=false; positionChanged=true
board['$tm_empire_plot_request']={schema=1,key='moved_new_station',station=station,
    budget=200,state='quote_requested',extend=0,newconstruction=1}
dispatch.quote(); assert(board['$tm_empire_plot_request'].state=='quote_ready')
assert(board['$tm_empire_plot_request'].quote.price==100 and transfers==6)
board['$tm_empire_plot_request'].state='licence_approved'
dispatch.license()
assert(transfers==7 and money==900 and not positionChanged)
assert(board['$tm_empire_plot_receipt'].state=='reconciled')
dispatch.license(); assert(transfers==7)
