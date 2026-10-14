-- Stock PlayerInfo/StationConfiguration account transfer; MD chooses the need.
local ffi = require('ffi')
local M = {}
local function moneyValue(value)
    return type(value)=='number' and value>=0 and value<=90071992547409
        and math.abs(value*100-math.floor(value*100+0.5))<0.01
end
local function sameMoney(left,right)
    return type(left)=='number' and type(right)=='number' and math.abs(left-right)<0.005
end
function M.fund()
    local player=ConvertStringToLuaID(tostring(ffi.C.GetPlayerID()))
    local request=GetNPCBlackboard(player, '$tm_empire_station_funding')
    if type(request)~='table' or request.schema~=1 or request.state~='approved'
        or type(request.key)~='string' or #request.key==0 or #request.key>128
        or type(request.station)~='userdata' or not moneyValue(request.balance)
        or not moneyValue(request.wanted) or not moneyValue(request.budget) then return end
    local previous=GetNPCBlackboard(player, '$tm_empire_station_payment')
    if type(previous)=='table' and (previous.key==request.key or previous.state~='reconciled') then return end
    local function reject(reason)
        request.state, request.reason='rejected_before_payment', reason
        SetNPCBlackboard(player, '$tm_empire_station_funding', request)
        AddUITriggeredEvent('TM_Empire_Supply', 'StationFundingSubmitted')
    end
    local station=ConvertIDTo64Bit(request.station)
    local owned, balance, wanted=GetComponentData(request.station, 'isplayerowned', 'money', 'productionmoney')
    if (owned~=true and owned~=1) or not ffi.C.IsComponentOperational(station)
        or not moneyValue(balance) or not moneyValue(wanted) or not sameMoney(balance,request.balance)
        or not sameMoney(wanted,request.wanted) or wanted==0 or balance*10>wanted*9 then
        return reject('station_production_quote_changed')
    end
    local amount, before=math.floor((wanted-balance)*100+0.5)/100, GetPlayerMoney()
    if amount>request.budget or before<amount then return reject('station_budget_missing') end
    local current=GetNPCBlackboard(player, '$tm_empire_station_funding')
    if type(current)~='table' or current.state~='approved' or current.key~=request.key
        or not IsSameComponent(current.station, request.station) or not sameMoney(current.balance,balance)
        or not sameMoney(current.wanted,wanted) or current.budget~=request.budget then
        return reject('station_funding_revoked')
    end
    local receipt={schema=1,key=request.key,station=request.station,state='payment_sent',
        wanted=wanted,amount=amount,paid=0,before=before,stationbefore=balance}
    SetNPCBlackboard(player, '$tm_empire_station_payment', receipt)
    local ok, reason=pcall(function()
        TransferPlayerMoneyTo(amount, station)
        receipt.after=GetPlayerMoney()
        receipt.stationafter=GetComponentData(request.station, 'money')
        assert(sameMoney(before-receipt.after,amount), 'station_debit_unconfirmed')
        receipt.paid=amount
        assert(sameMoney(receipt.stationafter,balance+amount), 'station_credit_unconfirmed')
        receipt.state='paid'
    end)
    if not ok then
        receipt.state,receipt.detail='unknown',tostring(reason):sub(1,256)
        receipt.reason=receipt.detail:find('station_debit_unconfirmed',1,true) and 'station_debit_unconfirmed'
            or receipt.detail:find('station_credit_unconfirmed',1,true) and 'station_credit_unconfirmed'
            or 'station_funding_effect_unconfirmed'
    end
    SetNPCBlackboard(player, '$tm_empire_station_payment', receipt)
    request.state=receipt.state
    SetNPCBlackboard(player, '$tm_empire_station_funding', request)
    AddUITriggeredEvent('TM_Empire_Supply', 'StationFundingSubmitted')
end
function M.init() RegisterEvent('TM_Empire.FundStation', M.fund) end
Register_Require_With_Init('extensions.tm_empire_management.ui.station_funding', M, M.init)
