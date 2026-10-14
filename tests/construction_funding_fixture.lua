-- Native account boundary: durable receipt, exact debit/credit, no replay.
local station, storage = newproxy(true), newproxy(true)
local board, money, balance, wanted, transfers = {}, 1000, 100, 600, 0
local partial, unavailable, revoked, quoteChanges = false, false, false, false
local newStation = false
local partialDebit = false
local function copy(value)
    if type(value) ~= 'table' then return value end
    local result = {}; for key, item in pairs(value) do result[key] = copy(item) end; return result
end
package.preload.ffi = function() return {C={
    GetPlayerID=function() return 7 end,
    IsComponentOperational=function(id) return not unavailable and (id ~= 10 or not newStation) end,
}} end
ConvertStringToLuaID=function(value) return tonumber(value) end
ConvertIDTo64Bit=function(value) if value==station then return 10 end; assert(value==storage); return 11 end
IsSameComponent=function(left, right) return left==right end
GetComponentData=function(id, ...)
    assert(id==station or id==storage)
    local result = {}
    for index=1, select('#', ...) do
        local key=select(index, ...)
        if key=='isplayerowned' then result[index]=true
        elseif key=='money' then assert(id==storage); result[index]=balance
        elseif key=='wantedmoney' then assert(id==storage); result[index]=wanted+(quoteChanges and 1 or 0)
        else error(key) end
    end
    return unpack(result)
end
GetNPCBlackboard=function(_, key)
    local result=copy(board[key])
    if revoked and key=='$tm_empire_construction_funding' and result then
        if revoked=='next' then result.state='revoked' else revoked='next' end
    end
    return result
end
SetNPCBlackboard=function(_, key, value) board[key]=copy(value) end
GetPlayerMoney=function() return money end
TransferPlayerMoneyTo=function(amount, id)
    assert(id==11 and board['$tm_empire_construction_payment'].state=='payment_sent')
    assert(board['$tm_empire_construction_payment'].paid==0)
    assert(board['$tm_empire_construction_payment'].amount==amount)
    transfers=transfers+1; money=money-(partialDebit and amount/2 or amount)
    balance=balance+(partial and amount/2 or amount)
end
AddUITriggeredEvent=function(screen, event) assert(screen=='TM_Empire_Construction' and (event=='FundingSubmitted' or event=='FundingQuoted')) end
local module
RegisterEvent=function() end
Register_Require_With_Init=function(_, value) module=value end
dofile('X4_TopManager/ui/construction_funding.lua')
local function request(key, budget)
    board['$tm_empire_construction_funding']={schema=1,state='approved',key=key,
        station=station,storage=storage,wanted=wanted,balance=balance,budget=budget or 1000}
end
request('success'); module.fund()
assert(transfers==1 and money==500 and balance==600)
assert(board['$tm_empire_construction_payment'].state=='paid')
assert(board['$tm_empire_construction_payment'].amount==500
    and board['$tm_empire_construction_payment'].paid==500
    and board['$tm_empire_construction_payment'].after==500
    and board['$tm_empire_construction_payment'].storageafter==600)
module.fund(); assert(transfers==1)
request('unreconciled'); module.fund(); assert(transfers==1)
board['$tm_empire_construction_payment'].state='reconciled'
request('enough'); module.fund()
assert(transfers==1 and board['$tm_empire_construction_payment'].paid==0)
assert(board['$tm_empire_construction_payment'].state=='paid')
board={}; balance=100; money=200; request('poor'); module.fund()
assert(transfers==1 and board['$tm_empire_construction_funding'].state=='rejected_before_payment')
money=1000; request('cap',499); module.fund(); assert(transfers==1)
request('quote'); quoteChanges=true; module.fund(); quoteChanges=false; assert(transfers==1)
request('lost'); unavailable=true; module.fund(); unavailable=false; assert(transfers==1)
request('revoked'); revoked=true; module.fund(); revoked=false; assert(transfers==1)
board={}; request('partial'); partial=true; module.fund()
assert(transfers==2 and board['$tm_empire_construction_payment'].state=='unknown')
assert(board['$tm_empire_construction_payment'].paid==500
    and board['$tm_empire_construction_payment'].after==500
    and board['$tm_empire_construction_payment'].storageafter==350)
request('retry'); module.fund(); assert(transfers==2)
-- Simulate a saved payment_sent before the Lua callback returns: never debit again.
board['$tm_empire_construction_payment'].state='payment_sent'
request('after_load'); module.fund(); assert(transfers==2)
-- A native station under construction has no operational station yet.
-- Only the exact MD adoption approval permits funding its operational storage.
board={}; partial=false; money=1000; balance=100; newStation=true
request('unadopted_station'); module.fund(); assert(transfers==2)
assert(board['$tm_empire_construction_funding'].state=='rejected_before_payment')
request('false_adoption'); board['$tm_empire_construction_funding'].newconstruction=0
module.fund(); assert(transfers==2)
request('invalid_adoption'); board['$tm_empire_construction_funding'].newconstruction=2
module.fund(); assert(transfers==2)
request('adopted_station'); board['$tm_empire_construction_funding'].newconstruction=1
module.fund(); assert(transfers==3 and money==500 and balance==600)
module.fund(); assert(transfers==3)
-- Partial debit preserves actual balances and blocks replay without claiming
-- the intended amount was paid, even when the destination was fully credited.
board={}; money=1000; balance=100; newStation=false; partialDebit=true
request('partial_debit'); module.fund()
local receipt=board['$tm_empire_construction_payment']
assert(transfers==4 and receipt.state=='unknown' and receipt.amount==500
    and receipt.paid==0 and receipt.before==1000 and receipt.after==750
    and receipt.storagebefore==100 and receipt.storageafter==600)
request('partial_debit_retry'); module.fund(); assert(transfers==4)
board={}; partialDebit=false; money=1000.07; balance=100.01; wanted=600.03
request('fractional',1000.03); module.fund()
receipt=board['$tm_empire_construction_payment']
assert(transfers==5 and receipt.state=='paid' and receipt.paid==500.02
    and math.abs(receipt.after-500.05)<0.001 and math.abs(receipt.storageafter-600.03)<0.001)
board={}; money=1000.07; balance=100.01
local nativeTransfer=TransferPlayerMoneyTo
TransferPlayerMoneyTo=function(amount,id) nativeTransfer(amount,id); money=money+0.01 end
request('one_cent_debit_missing'); module.fund()
receipt=board['$tm_empire_construction_payment']
assert(transfers==6 and receipt.state=='unknown' and receipt.paid==0)
request('one_cent_retry'); module.fund(); assert(transfers==6)
-- MD currency and Lua doubles may encode the same cent differently.
board={}; money=1000.07; balance=100.01; wanted=600.03
TransferPlayerMoneyTo=nativeTransfer
request('currency_roundtrip'); board['$tm_empire_construction_funding'].wanted=wanted+1e-10
board['$tm_empire_construction_funding'].balance=balance+1e-11
module.fund(); receipt=board['$tm_empire_construction_payment']
assert(transfers==7 and receipt.state=='paid' and receipt.paid==500.02)
-- Native Lua quote can differ from MD's cent-valued estimate. Quote without
-- effects, then simulate MD approval of that exact native snapshot.
board={}; money=2000000; balance=0; wanted=1211198
request('native_rounded_estimate',2000000)
local pending=board['$tm_empire_construction_funding']
pending.state='quote_requested'; pending.wanted=1211197.8
module.quote(); pending=board['$tm_empire_construction_funding']
assert(transfers==7 and pending.state=='quote_ready' and pending.reason==nil and pending.quotedwanted==1211198 and pending.quotedbalance==0)
pending.state='approved'; pending.wanted=pending.quotedwanted; pending.balance=pending.quotedbalance
module.fund(); assert(transfers==8 and board['$tm_empire_construction_payment'].paid==1211198)
board={}; money=2000000; balance=0; wanted=1211198
request('quote_moves_after_approval',2000000); pending=board['$tm_empire_construction_funding']
pending.state='quote_requested'; module.quote(); pending=board['$tm_empire_construction_funding']
pending.state='approved'; pending.wanted=pending.quotedwanted; pending.balance=pending.quotedbalance
wanted=wanted+1; module.fund()
assert(transfers==8 and board['$tm_empire_construction_funding'].reason=='native_construction_quote_changed')
