-- MD owns the request and lifecycle; Lua only calls native equipment helpers.
local ffi = require('ffi')
local playerOrders = require('extensions.tm_empire_management.ui.player_order_guard')
ffi.cdef[[uint64_t GetPlayerControlledShipID(void);]]
local M = {}
local quotes = {}
local supplyquotes = {}
local function player()
    return ConvertStringToLuaID(tostring(ffi.C.GetPlayerID()))
end
function M.prepare()
    local owner = player()
    local request = GetNPCBlackboard(owner, '$tm_empire_purchase_request')
    if type(request) ~= 'table' or request.schema ~= 1
        or request.state ~= 'quote_requested' or type(request.key) ~= 'string'
        or quotes[request.key] then return end
    local quote = require('extensions.tm_empire_management.ui.purchase_quote')
    local result, reason = quote.generate(request.shipyard, request.macro, request.level)
    if result then
        quotes = {}
        quotes[request.key] = result
        request.state = 'quote_ready'
        request.price, request.crewprice, request.paid = result.price, result.crewprice, result.paid
    else
        request.state, request.reason = 'quote_failed', reason
    end
    SetNPCBlackboard(owner, '$tm_empire_purchase_request', request)
    AddUITriggeredEvent('TM_Empire_Purchase', 'QuoteReady')
end
function M.submit()
    local owner = player()
    local request = GetNPCBlackboard(owner, '$tm_empire_purchase_request')
    if type(request) ~= 'table' or request.schema ~= 1
        or request.state ~= 'approved' or not quotes[request.key] then return end
    local function canAct()
        local current = GetNPCBlackboard(owner, '$tm_empire_purchase_request')
        return type(current) == 'table' and current.schema == 1
            and current.state == 'approved' and current.key == request.key
            and IsSameComponent(current.shipyard, request.shipyard) and current.macro == request.macro
            and current.budget == request.budget
    end
    local purchase = require('extensions.tm_empire_management.ui.purchase_submit')
    local receipt, reason = purchase.submit(request, quotes[request.key], canAct)
    -- Approval is single-use regardless of a receipt or an unknown effect.
    quotes[request.key] = nil
    request.state = receipt and receipt.state or 'submission_failed'
    request.reason = receipt and receipt.reason or reason
    SetNPCBlackboard(owner, '$tm_empire_purchase_request', request)
    AddUITriggeredEvent('TM_Empire_Purchase', 'PurchaseSubmitted')
end
function M.match()
    local owner = player()
    local request = GetNPCBlackboard(owner, '$tm_empire_purchase_request')
    local receipt = GetNPCBlackboard(owner, '$tm_empire_purchase_submission')
    local candidates = GetNPCBlackboard(owner, '$tm_empire_purchase_candidates')
    if type(request) ~= 'table' or type(receipt) ~= 'table'
        or receipt.state ~= 'built' or receipt.key ~= request.key
        or type(candidates) ~= 'table' then return end
    local purchase = require('extensions.tm_empire_management.ui.purchase_submit')
    for index = 1, math.min(#candidates, 16) do
        local candidate = candidates[index]
        local matched, reason, actual = purchase.match(receipt, candidate)
        if matched then
            SetNPCBlackboard(owner, '$tm_empire_purchase_match', {
                key=receipt.key, candidateindex=index, shipyard=candidate.shipyard,
                macro=receipt.macro, price=receipt.price, crewprice=receipt.crewprice,
                id=receipt.id})
            AddUITriggeredEvent('TM_Empire_Purchase', 'BuildMatched')
            return
        end
        receipt.match_reason, receipt.candidateid = reason, actual
    end
    SetNPCBlackboard(owner, '$tm_empire_purchase_submission', receipt)
end
function M.reconcile()
    local owner = player()
    local receipt = GetNPCBlackboard(owner, '$tm_empire_purchase_submission')
    local delivery = GetNPCBlackboard(owner, '$tm_empire_purchase_delivery')
    if type(receipt) ~= 'table' or receipt.state ~= 'built'
        or type(delivery) ~= 'table' or delivery.schema ~= 1
        or receipt.key ~= delivery.key or receipt.id ~= delivery.id
        or receipt.macro ~= delivery.macro or receipt.paid ~= delivery.paid
        or type(delivery.ship) ~= 'userdata' then return end
    local owned, macro = GetComponentData(delivery.ship, 'isplayerowned', 'macro')
    if (owned ~= true and owned ~= 1) or macro ~= receipt.macro
        or not ffi.C.IsComponentOperational(ConvertIDTo64Bit(delivery.ship)) then return end
    receipt.state = 'reconciled'
    receipt.ship = delivery.ship
    SetNPCBlackboard(owner, '$tm_empire_purchase_submission', receipt)
    AddUITriggeredEvent('TM_Empire_Purchase', 'PurchaseReconciled')
end
function M.prepare_supply()
    local owner = player()
    local request = GetNPCBlackboard(owner, '$tm_empire_supply_request')
    if type(request) ~= 'table' or request.schema ~= 1 or request.state ~= 'quote_requested'
        or type(request.key) ~= 'string' or #request.key == 0 or #request.key > 128
        or type(request.ship) ~= 'userdata' or type(request.shipyard) ~= 'userdata' then return end
    local ship = ConvertIDTo64Bit(request.ship)
    local owned = GetComponentData(request.ship, 'isplayerowned')
    if (owned ~= true and owned ~= 1) or not ffi.C.IsComponentOperational(ship) then return end
    -- MD table keys cannot be arbitrary strings. Carry the single requested
    -- ware as a value and construct the native Lua price map at this boundary.
    -- Keep legacy Lua maps readable; durable receipts still prevent replay.
    local wares = request.wares
    if request.ware ~= nil or request.amount ~= nil then
        wares = type(request.ware) == 'string' and type(request.amount) == 'number'
            and {[request.ware] = request.amount} or nil
    end
    local quote, reason = require('extensions.tm_empire_management.ui.purchase_quote')
        .quote_supply(request.shipyard, wares)
    local current = GetNPCBlackboard(owner, '$tm_empire_supply_request')
    if type(current) ~= 'table' or current.state ~= 'quote_requested'
        or current.key ~= request.key or not IsSameComponent(current.ship, request.ship)
        or not IsSameComponent(current.shipyard, request.shipyard) then return end
    if quote then
        supplyquotes = {[request.key]=quote}
        current.state, current.price = 'quote_ready', quote.price
        current.requires_resources = quote.requires_resources
    else
        current.state, current.reason = 'quote_failed', reason
    end
    SetNPCBlackboard(owner, '$tm_empire_supply_request', current)
    AddUITriggeredEvent('TM_Empire_Supply', 'QuoteReady')
end
function M.pay_supply()
    local owner = player()
    local request = GetNPCBlackboard(owner, '$tm_empire_supply_request')
    local previous = GetNPCBlackboard(owner, '$tm_empire_supply_payment')
    if type(request) ~= 'table' or request.schema ~= 1
        or request.state ~= 'payment_approved' or not supplyquotes[request.key]
        or (type(previous) == 'table' and (previous.key == request.key
            or previous.state ~= 'consumed')) then return end
    local quote, reason = require('extensions.tm_empire_management.ui.purchase_quote')
        .reprice_supply(request.shipyard, supplyquotes[request.key])
    if not quote or quote.price ~= request.price or quote.price > request.budget
        or quote.price > GetPlayerMoney() then
        request.repriced = quote and quote.price or nil
        request.available = GetPlayerMoney()
        request.state, request.reason = 'payment_rejected', reason or 'supply_price_or_budget_changed'
        SetNPCBlackboard(owner, '$tm_empire_supply_request', request)
        return
    end
    local current = GetNPCBlackboard(owner, '$tm_empire_supply_request')
    if type(current) ~= 'table' or current.state ~= 'payment_approved'
        or current.key ~= request.key or not IsSameComponent(current.ship, request.ship)
        or not IsSameComponent(current.shipyard, request.shipyard) or current.price ~= request.price
        or current.budget ~= request.budget then return end
    local ship = ConvertIDTo64Bit(request.ship)
    local owned = GetComponentData(request.ship, 'isplayerowned')
    if (owned ~= true and owned ~= 1) or not ffi.C.IsComponentOperational(ship)
        or ffi.C.GetTopLevelContainer(ship) ~= ConvertIDTo64Bit(request.shipyard) then return end
    if ffi.C.GetPlayerControlledShipID() == ship then
        current.state, current.reason = 'payment_rejected', 'player_helm'
        SetNPCBlackboard(owner, '$tm_empire_supply_request', current)
        AddUITriggeredEvent('TM_Empire_Supply', 'PaymentSubmitted')
        return
    end
    local protected = playerOrders.reason(request.ship)
    if protected then
        current.state, current.reason = 'payment_rejected', protected
        SetNPCBlackboard(owner, '$tm_empire_supply_request', current)
        AddUITriggeredEvent('TM_Empire_Supply', 'PaymentSubmitted')
        return
    end
    local receipt = {schema=1, key=request.key, state='payment_sent',
        ship=request.ship, builder=request.shipyard, paid=quote.price, before=GetPlayerMoney()}
    -- Persist before the effect. A replay, including after reload, cannot pay again.
    SetNPCBlackboard(owner, '$tm_empire_supply_payment', receipt)
    supplyquotes[request.key] = nil
    local ok, err = pcall(function()
        if receipt.paid > 0 then TransferPlayerMoneyTo(receipt.paid, ConvertIDTo64Bit(receipt.builder)) end
        assert(receipt.before - GetPlayerMoney() == receipt.paid, 'supply_payment_unconfirmed')
    end)
    receipt.state = ok and 'paid' or 'unknown'
    receipt.reason = not ok and tostring(err):sub(1,256) or nil
    SetNPCBlackboard(owner, '$tm_empire_supply_payment', receipt)
    AddUITriggeredEvent('TM_Empire_Supply', 'PaymentSubmitted')
end
function M.record_supply_payment()
    local owner = player()
    local receipt = GetNPCBlackboard(owner, '$tm_empire_supply_payment')
    if type(receipt) ~= 'table' or receipt.schema ~= 1 or receipt.state ~= 'paid'
        or type(receipt.build) ~= 'userdata' or type(receipt.buildtoken) ~= 'string'
        or #receipt.buildtoken < 1 or #receipt.buildtoken > 128 or type(receipt.ship) ~= 'userdata'
        or type(receipt.builder) ~= 'userdata' or type(receipt.paid) ~= 'number'
        or receipt.paid < 0 or receipt.paid > 9007199254740991
        or receipt.paid % 1 ~= 0 then return end
    local build = ConvertIDTo64Bit(receipt.build)
    local info = ffi.C.GetBuildTaskInfo(build)
    if info.id == 0 or info.id ~= build
        or info.component ~= ConvertIDTo64Bit(receipt.ship)
        or info.buildingcontainer ~= ConvertIDTo64Bit(receipt.builder)
        or tonumber(info.price) ~= receipt.paid or ffi.string(info.factionid) ~= 'player' then return end
    ffi.C.SetBuildTaskTransferredMoney(build, receipt.paid)
    receipt.recordedbuild = receipt.buildtoken
    receipt.state = 'build_recorded'
    SetNPCBlackboard(owner, '$tm_empire_supply_payment', receipt)
    AddUITriggeredEvent('TM_Empire_Supply', 'PaymentRecorded')
end
function M.init()
    RegisterEvent('TM_Empire.PaySupply', M.pay_supply)
    RegisterEvent('TM_Empire.RecordSupplyPayment', M.record_supply_payment)
    RegisterEvent('TM_Empire.QuoteSupply', M.prepare_supply)
    RegisterEvent('TM_Empire.ClearPreparedPurchase', function() quotes = {} end)
    RegisterEvent('TM_Empire.PreparePurchase', M.prepare)
    RegisterEvent('TM_Empire.SubmitPurchase', M.submit)
    RegisterEvent('TM_Empire.MatchPurchase', M.match)
    RegisterEvent('TM_Empire.ReconcilePurchase', M.reconcile)
end
Register_Require_With_Init('extensions.tm_empire_management.ui.purchase_dispatch', M, M.init)
