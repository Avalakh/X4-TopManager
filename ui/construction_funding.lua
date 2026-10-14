-- StationConfiguration.buttonSetMoneyToEstimate: fund real build storage.
-- The native wantedmoney quote includes remaining resources and equipment.
local ffi = require('ffi')
local M = {}
local function owner()
    return ConvertStringToLuaID(tostring(ffi.C.GetPlayerID()))
end
local function moneyValue(value)
    return type(value) == 'number' and value >= 0
        and value <= 90071992547409
        and math.abs(value * 100 - math.floor(value * 100 + 0.5)) < 0.01
end
local function sameMoney(left, right)
    return type(left) == 'number' and type(right) == 'number' and math.abs(left - right) < 0.005
end
-- The stock Lua estimate is rounded independently of MD's cent-valued money.
-- Quote it without effects; MD approves this exact native snapshot afterwards.
function M.quote()
    local player = owner()
    local request = GetNPCBlackboard(player, '$tm_empire_construction_funding')
    if type(request) ~= 'table' or request.schema ~= 1 or request.state ~= 'quote_requested'
        or type(request.key) ~= 'string' or #request.key == 0 or #request.key > 128
        or type(request.station) ~= 'userdata' or type(request.storage) ~= 'userdata'
        or not moneyValue(request.budget) then return end
    local ownStation = GetComponentData(request.station, 'isplayerowned')
    local ownStorage, balance, wanted = GetComponentData(request.storage, 'isplayerowned', 'money', 'wantedmoney')
    local valid = (ownStation == true or ownStation == 1) and (ownStorage == true or ownStorage == 1)
        and (ffi.C.IsComponentOperational(ConvertIDTo64Bit(request.station))
             or request.newconstruction == true or request.newconstruction == 1)
        and ffi.C.IsComponentOperational(ConvertIDTo64Bit(request.storage))
        and moneyValue(balance) and moneyValue(wanted)
    local current = GetNPCBlackboard(player, '$tm_empire_construction_funding')
    if type(current) ~= 'table' or current.key ~= request.key or current.state ~= 'quote_requested'
        or not IsSameComponent(current.station, request.station) or not IsSameComponent(current.storage, request.storage)
        or current.newconstruction ~= request.newconstruction or current.budget ~= request.budget then return end
    current.state = valid and 'quote_ready' or 'quote_failed'
    current.reason = nil
    if not valid then current.reason = 'construction_asset_or_quote_unavailable' end
    if valid then current.quotedwanted, current.quotedbalance = wanted, balance end
    SetNPCBlackboard(player, '$tm_empire_construction_funding', current)
    AddUITriggeredEvent('TM_Empire_Construction', 'FundingQuoted')
end
function M.fund()
    local player = owner()
    local request = GetNPCBlackboard(player, '$tm_empire_construction_funding')
    if type(request) ~= 'table' or request.schema ~= 1 or request.state ~= 'approved'
        or type(request.key) ~= 'string' or #request.key == 0 or #request.key > 128
        or type(request.station) ~= 'userdata' or type(request.storage) ~= 'userdata'
        or not moneyValue(request.budget) or not moneyValue(request.wanted)
        or not moneyValue(request.balance) then return end
    local previous = GetNPCBlackboard(player, '$tm_empire_construction_payment')
    if type(previous) == 'table' and (previous.key == request.key
        or previous.state ~= 'reconciled') then return end
    local function rejected(reason)
        request.state, request.reason = 'rejected_before_payment', reason
        SetNPCBlackboard(player, '$tm_empire_construction_funding', request)
        AddUITriggeredEvent('TM_Empire_Construction', 'FundingSubmitted')
    end
    local station, storage = ConvertIDTo64Bit(request.station), ConvertIDTo64Bit(request.storage)
    local ownStation = GetComponentData(request.station, 'isplayerowned')
    local ownStorage, balance, wanted = GetComponentData(request.storage, 'isplayerowned', 'money', 'wantedmoney')
    if (ownStation ~= true and ownStation ~= 1) or (ownStorage ~= true and ownStorage ~= 1)
        or (not ffi.C.IsComponentOperational(station) and request.newconstruction ~= true and request.newconstruction ~= 1)
        or not ffi.C.IsComponentOperational(storage) then
        return rejected('construction_asset_unavailable')
    end
    if not moneyValue(balance) or not moneyValue(wanted) or not sameMoney(wanted, request.wanted)
        or not sameMoney(balance, request.balance) then
        request.observedwanted, request.observedbalance = wanted, balance
        return rejected('native_construction_quote_changed')
    end
    local amount = math.max(0, math.floor((wanted - balance) * 100 + 0.5) / 100)
    local before = GetPlayerMoney()
    if amount > request.budget or before < amount then return rejected('construction_budget_missing') end
    -- No Lua goal planner: approval comes from the exact owned MD build claim.
    local current = GetNPCBlackboard(player, '$tm_empire_construction_funding')
    if type(current) ~= 'table' or current.state ~= 'approved' or current.key ~= request.key
        or not IsSameComponent(current.station, request.station) or not IsSameComponent(current.storage, request.storage)
        or current.newconstruction ~= request.newconstruction
        or current.budget ~= request.budget or not sameMoney(current.wanted, wanted)
        or not sameMoney(current.balance, balance) then return rejected('construction_funding_revoked') end
    local receipt = {schema=1, key=request.key, station=request.station, storage=request.storage,
        state='payment_sent', wanted=wanted, amount=amount, paid=0, before=before, storagebefore=balance}
    SetNPCBlackboard(player, '$tm_empire_construction_payment', receipt)
    local ok, reason = pcall(function()
        if amount > 0 then TransferPlayerMoneyTo(amount, storage) end
        receipt.after = GetPlayerMoney()
        receipt.storageafter = GetComponentData(request.storage, 'money')
        assert(sameMoney(before - receipt.after, amount), 'native_construction_debit_unconfirmed')
        receipt.paid = amount
        assert(sameMoney(receipt.storageafter, balance + amount), 'native_construction_credit_unconfirmed')
        receipt.state = 'paid'
    end)
    if not ok then
        receipt.state, receipt.detail = 'unknown', tostring(reason):sub(1,256)
        receipt.reason = receipt.detail:find('native_construction_debit_unconfirmed', 1, true) and 'native_construction_debit_unconfirmed'
            or receipt.detail:find('native_construction_credit_unconfirmed', 1, true) and 'native_construction_credit_unconfirmed'
            or 'construction_funding_effect_unconfirmed'
    end
    SetNPCBlackboard(player, '$tm_empire_construction_payment', receipt)
    request.state = receipt.state
    SetNPCBlackboard(player, '$tm_empire_construction_funding', request)
    AddUITriggeredEvent('TM_Empire_Construction', 'FundingSubmitted')
end
function M.init()
    RegisterEvent('TM_Empire.QuoteConstructionFunding', M.quote)
    RegisterEvent('TM_Empire.FundConstruction', M.fund)
end
Register_Require_With_Init('extensions.tm_empire_management.ui.construction_funding', M, M.init)
