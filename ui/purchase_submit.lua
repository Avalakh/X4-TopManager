-- Штатная оплаченная постройка. Выбор macro/верфи остаётся у Manager.
-- Пока не зарегистрирован как event: подключение требует MD lifecycle guard.
local ffi = require('ffi')
local M = {}
local pendingKey

function M.submit(request, quote, canAct)
    if type(request) ~= 'table' or type(request.key) ~= 'string'
        or #request.key == 0 or #request.key > 128
        or type(request.shipyard) ~= 'userdata' or type(request.macro) ~= 'string'
        or type(request.budget) ~= 'number' or request.budget <= 0
        or request.budget > 9007199254740991 or request.budget % 1 ~= 0
        or type(canAct) ~= 'function' then return nil, 'invalid_purchase_request' end
    local player = ConvertStringToLuaID(tostring(ffi.C.GetPlayerID()))
    local previous = GetNPCBlackboard(player, '$tm_empire_purchase_submission')
    if pendingKey == request.key or (type(previous) == 'table'
        and (previous.key == request.key or previous.state ~= 'reconciled')) then
        return nil, 'previous_purchase_unreconciled'
    end
    if not canAct(request) then return nil, 'manager_unavailable' end
    local pricing = require('extensions.tm_empire_management.ui.purchase_quote')
    local plan, reason = pricing.to_plan(request.shipyard, quote)
    if not plan then return nil, reason end
    local price
    price, reason = pricing.reprice(request.shipyard, quote)
    if not price then return nil, reason end
    if quote.macro ~= request.macro or price.paid > request.budget
        or price.paid <= 0 then return nil, 'purchase_budget_or_macro_changed' end
    if GetPlayerMoney() < price.paid then return nil, 'insufficient_money' end
    -- Resolve native ABI and retain arrays before any payment effect.
    require('extensions.tm_empire_management.ui.purchase_receipt')
    local yard = ConvertIDTo64Bit(request.shipyard)
    local additional = ffi.new('AddBuildTask6Container')
    local create, record = ffi.C.AddBuildTask6, ffi.C.SetBuildTaskTransferredMoney
    pendingKey = request.key
    local receipt = {schema=1, key=request.key, state='prepared',
        macro=request.macro, shipyard=request.shipyard,
        price=price.price, crewprice=price.crewprice, paid=price.paid}
    local ok, err = pcall(function()
        Helper.callLoadoutFunction(plan, nil, function(loadout, crewtransfer)
            assert(canAct(request), 'manager_changed_before_payment')
            assert(GetPlayerMoney() >= price.paid, 'money_changed_before_payment')
            assert(tonumber(loadout.numsoftware) == tonumber(quote.loadout.numsoftware),
                'software_roundtrip_mismatch')
            local before = GetPlayerMoney()
            receipt.state = 'payment_sent'
            SetNPCBlackboard(player, '$tm_empire_purchase_submission', receipt)
            TransferPlayerMoneyTo(price.paid, yard)
            assert(before - GetPlayerMoney() == price.paid, 'payment_unknown')
            local id = create(yard, 0, request.macro, loadout, price.price,
                crewtransfer, false, '', additional)
            assert(id ~= 0, 'build_unknown_after_payment')
            receipt.id = tostring(id)
            SetNPCBlackboard(player, '$tm_empire_purchase_submission', receipt)
            local info = ffi.C.GetBuildTaskInfo(id)
            assert(info.id == id and info.buildingcontainer == yard
                and tonumber(info.price) == price.price
                and ffi.string(info.factionid) == 'player'
                and ffi.string(info.macro) == request.macro, 'build_identity_unknown')
            record(id, price.paid)
            receipt.state = 'built'
            SetNPCBlackboard(player, '$tm_empire_purchase_submission', receipt)
        end, nil, 'UILoadout2')
    end)
    if not ok then
        receipt.reason = tostring(err):sub(1, 256)
        if receipt.state == 'prepared' then
            pendingKey = nil
            return nil, receipt.reason
        end
        receipt.state = 'unknown'
        SetNPCBlackboard(player, '$tm_empire_purchase_submission', receipt)
    end
    return receipt
end

-- Exact native BuildTaskID, never a floating point conversion or a macro-only
-- match. Called after the engine delivers the MD build handle.
function M.match(receipt, candidate)
    if type(receipt) ~= 'table' or receipt.state ~= 'built'
        or type(receipt.id) ~= 'string' or type(candidate) ~= 'table'
        or type(candidate.build) ~= 'userdata'
        or type(candidate.shipyard) ~= 'userdata'
        or type(receipt.shipyard) ~= 'userdata' then
        return false, 'invalid_build_correlation'
    end
    local function canonical(id)
        local value = tostring(id):gsub('ULL$', ''):gsub('LL$', '')
        if not value:match('^%d+$') then return nil end
        value = value:gsub('^0+', '')
        return value == '' and '0' or value
    end
    local id = ffi.cast('BuildTaskID', ConvertIDTo64Bit(candidate.build))
    local actual, expected = canonical(id), canonical(receipt.id)
    if not actual or not expected or actual ~= expected or actual == '0' then
        return false, 'build_id_mismatch', actual
    end
    local info = ffi.C.GetBuildTaskInfo(id)
    if info.id ~= id or info.buildingcontainer ~= ConvertIDTo64Bit(receipt.shipyard)
        or info.buildingcontainer ~= ConvertIDTo64Bit(candidate.shipyard)
        or tonumber(info.price) ~= receipt.price
        or ffi.string(info.factionid) ~= 'player'
        or ffi.string(info.macro) ~= receipt.macro then
        return false, 'native_build_identity_mismatch', actual
    end
    return true, 'matched', actual
end

Register_Require_With_Init('extensions.tm_empire_management.ui.purchase_submit', M, function() end)
return M
