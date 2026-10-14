-- Штатная оплата найма из MapMenu.buttonHire; назначение выполняет MD.
local ffi = require('ffi')
local playerOrders = require('extensions.tm_empire_management.ui.player_order_guard')
ffi.cdef[[uint64_t GetPlayerControlledShipID(void);]]
local M = {}
local function moneyValue(value)
    return type(value)=='number' and value>=0 and value<=90071992547409
        and math.abs(value*100-math.floor(value*100+0.5))<0.01
end
local function sameMoney(left,right)
    return moneyValue(left) and moneyValue(right) and math.abs(left-right)<0.005
end
local function owner()
    return ConvertStringToLuaID(tostring(ffi.C.GetPlayerID()))
end
function M.pay()
    local player = owner()
    local request = GetNPCBlackboard(player, '$tm_empire_hire_request')
    if type(request) ~= 'table' or request.schema ~= 1 or request.state ~= 'approved'
        or type(request.key) ~= 'string' or type(request.actor) ~= 'userdata'
        or type(request.source) ~= 'userdata' or type(request.target) ~= 'userdata'
        or not moneyValue(request.budget) then return end
    local previous = GetNPCBlackboard(player, '$tm_empire_hire_payment')
    if type(previous) == 'table' and (previous.key == request.key
        or previous.state ~= 'reconciled') then return end
    local function failed(reason)
        request.state, request.reason = 'rejected_before_payment', reason
        SetNPCBlackboard(player, '$tm_empire_hire_request', request)
        AddUITriggeredEvent('TM_Empire_Personnel', 'HirePaid')
    end
    local raw = GetNPCBlackboard(request.actor, '$HiringFee')
    if not moneyValue(raw) or raw ~= request.fee then
        return failed('native_hiring_fee_changed')
    end
    local source = GetContextByClass(request.actor, 'container', true)
    if ConvertIDTo64Bit(source) ~= ConvertIDTo64Bit(request.source) then
        return failed('hiring_source_changed')
    end
    local discounts = GetComponentData(source, 'hiringdiscounts')
    if type(discounts) ~= 'table' then return failed('hiring_discounts_unavailable') end
    local factor = 1
    for _, discount in ipairs(discounts) do
        if type(discount.amount) ~= 'number' or discount.amount ~= discount.amount
            or discount.amount < 0 or discount.amount > 100 then return failed('invalid_hiring_discount') end
        factor = factor - discount.amount / 100
    end
    local paid = RoundTotalTradePrice(raw) * factor
    if factor < 0 or factor > 1 or not moneyValue(paid) or paid > request.budget then
        return failed('native_hiring_price_outside_budget')
    end
    local current = GetNPCBlackboard(player, '$tm_empire_hire_request')
    if type(current) ~= 'table' or current.key ~= request.key
        or current.state ~= 'approved' or type(current.actor) ~= 'userdata'
        or type(current.source) ~= 'userdata' or type(current.target) ~= 'userdata'
        or not IsSameComponent(current.target, request.target) or not IsSameComponent(current.actor, request.actor)
        or not IsSameComponent(current.source, request.source) or current.fee ~= request.fee
        or current.budget ~= request.budget then return failed('hire_approval_revoked') end
    local target = ConvertIDTo64Bit(request.target)
    local owned = GetComponentData(request.target, 'isplayerowned')
    if (owned ~= true and owned ~= 1) or not ffi.C.IsComponentOperational(target) then
        return failed('hiring_destination_lost')
    end
    if ffi.C.GetPlayerControlledShipID() == target then return failed('player_helm') end
    local protected = playerOrders.reason(request.target)
    if protected then return failed(protected) end
    local before = GetPlayerMoney()
    if not moneyValue(before) or before < paid then return failed('insufficient_hiring_money') end
    local receipt = {schema=1, key=request.key, actor=request.actor, source=request.source,
        state='payment_sent', amount=paid, paid=0, before=before}
    SetNPCBlackboard(player, '$tm_empire_hire_payment', receipt)
    local ok, reason = pcall(TransferPlayerMoneyTo, paid, ConvertIDTo64Bit(source))
    receipt.after = GetPlayerMoney()
    if ok and moneyValue(receipt.after) and sameMoney(before - receipt.after, paid) then
        receipt.state, receipt.paid = 'paid', paid
    else
        receipt.state, receipt.reason = 'unknown', tostring(reason or 'hiring_payment_unconfirmed'):sub(1, 256)
    end
    SetNPCBlackboard(player, '$tm_empire_hire_payment', receipt)
    AddUITriggeredEvent('TM_Empire_Personnel', 'HirePaid')
end
function M.init()
    RegisterEvent('TM_Empire.PayHire', M.pay)
end
Register_Require_With_Init('extensions.tm_empire_management.ui.personnel_hire', M, M.init)
