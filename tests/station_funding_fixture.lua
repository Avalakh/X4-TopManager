local station=newproxy(true)
local board,money,balance,wanted,transfers={},1000,100,600,0
local owned,operational,partialDebit,partialCredit,revoked=true,true,false,false,false
local function copy(value)
    if type(value)~='table' then return value end
    local result={}; for k,v in pairs(value) do result[k]=copy(v) end; return result
end
package.preload.ffi=function() return {C={GetPlayerID=function() return 7 end,
    IsComponentOperational=function() return operational end}} end
ConvertStringToLuaID=function(v) return tonumber(v) end
ConvertIDTo64Bit=function(v) assert(v==station); return 11 end
IsSameComponent=function(a,b) return a==b end
GetComponentData=function(id,...)
    assert(id==station, 'GetComponentData requires the Lua component ID'); local result={}
    for i=1,select('#',...) do
        local key=select(i,...)
        if key=='isplayerowned' then result[i]=owned
        elseif key=='money' then result[i]=balance
        elseif key=='productionmoney' then result[i]=wanted
        else error(key) end
    end
    return unpack(result)
end
GetNPCBlackboard=function(_,key)
    local result=copy(board[key])
    if revoked and key=='$tm_empire_station_funding' then
        if revoked=='next' then result.state='revoked' else revoked='next' end
    end
    return result
end
SetNPCBlackboard=function(_,key,value) board[key]=copy(value) end
GetPlayerMoney=function() return money end
TransferPlayerMoneyTo=function(amount,id)
    assert(id==11 and board['$tm_empire_station_payment'].state=='payment_sent'
        and board['$tm_empire_station_payment'].paid==0)
    transfers=transfers+1
    money=money-(partialDebit and amount/2 or amount)
    balance=balance+(partialCredit and amount/2 or amount)
end
AddUITriggeredEvent=function(screen,event) assert(screen=='TM_Empire_Supply' and event=='StationFundingSubmitted') end
RegisterEvent=function() end
local module
Register_Require_With_Init=function(_,v) module=v end
dofile('X4_TopManager/ui/station_funding.lua')
local function request(key,budget)
    board['$tm_empire_station_funding']={schema=1,state='approved',key=key,
        station=station,balance=balance,wanted=wanted,budget=budget or 1000}
end
request('success'); module.fund()
local receipt=board['$tm_empire_station_payment']
assert(transfers==1 and money==500 and balance==600 and receipt.state=='paid'
    and receipt.amount==500 and receipt.paid==500 and receipt.before==1000
    and receipt.after==500 and receipt.stationbefore==100 and receipt.stationafter==600)
module.fund(); request('unreconciled'); module.fund(); assert(transfers==1)
board={}; balance=100; money=1000
request('quote'); wanted=601; module.fund(); wanted=600; assert(transfers==1)
request('cap',499); module.fund(); assert(transfers==1)
request('poor'); money=200; module.fund(); money=1000; assert(transfers==1)
request('foreign'); owned=false; module.fund(); owned=true; assert(transfers==1)
request('lost'); operational=false; module.fund(); operational=true; assert(transfers==1)
request('revoked'); revoked=true; module.fund(); revoked=false; assert(transfers==1)
board={}; request('partial_debit'); partialDebit=true; module.fund(); partialDebit=false
receipt=board['$tm_empire_station_payment']
assert(transfers==2 and receipt.state=='unknown' and receipt.paid==0
    and receipt.after==750 and receipt.stationafter==600)
request('retry'); module.fund(); assert(transfers==2)
board={}; money=1000; balance=100; request('partial_credit'); partialCredit=true; module.fund()
receipt=board['$tm_empire_station_payment']
assert(transfers==3 and receipt.state=='unknown' and receipt.paid==500
    and receipt.after==500 and receipt.stationafter==350)
receipt.state='payment_sent'; board['$tm_empire_station_payment']=receipt
request('after_load'); module.fund(); assert(transfers==3)
board={}; partialCredit=false; money=1000.07; balance=100.01; wanted=600.03
request('fractional',1000.03); module.fund()
receipt=board['$tm_empire_station_payment']
assert(transfers==4 and receipt.state=='paid' and receipt.paid==500.02
    and math.abs(receipt.after-500.05)<0.001 and math.abs(receipt.stationafter-600.03)<0.001)
board={}; money=1000.07; balance=100.01
local nativeTransfer=TransferPlayerMoneyTo
TransferPlayerMoneyTo=function(amount,id) nativeTransfer(amount,id); money=money+0.01 end
request('one_cent_debit_missing'); module.fund()
receipt=board['$tm_empire_station_payment']
assert(transfers==5 and receipt.state=='unknown' and receipt.paid==0)
request('one_cent_retry'); module.fund(); assert(transfers==5)
board={}; money=1000.07; balance=100.01; wanted=600.03
TransferPlayerMoneyTo=nativeTransfer
request('currency_roundtrip'); board['$tm_empire_station_funding'].wanted=wanted+1e-10
board['$tm_empire_station_funding'].balance=balance+1e-11
module.fund(); receipt=board['$tm_empire_station_payment']
assert(transfers==6 and receipt.state=='paid' and receipt.paid==500.02)
