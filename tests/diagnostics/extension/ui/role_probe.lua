-- Только чтение собственных объектов и точного UI-контракта.
local Pipes = require('extensions.sn_mod_support_apis.ui.named_pipes.Interface')
local Presence = require('extensions.tm_empire_diagnostics.ui.pipe_presence')
local Time = require('extensions.sn_mod_support_apis.ui.time.Interface')
local PIPE = 'tm_empire_role_probe'
local arm
local compareQuoteUI = false
local dialogChoicesSent = {}
local function respond(_, data)
    local phase = tostring(data):match('^priority_fixture|phase=([^|]+)')
    if phase then
        local ok, reason = pcall(function()
            local player = ConvertStringToLuaID(tostring(require('ffi').C.GetPlayerID()))
            local context = GetNPCBlackboard(player, '$tm_empire_priority_probe')
            if type(context) ~= 'table' or context.phase ~= phase or type(context.ship) ~= 'userdata' then
                return 'priority_context_unavailable'
            end
            return require('extensions.tm_empire_management.ui.player_order_guard').reason(context.ship) or 'available'
        end)
        data = tostring(data) .. '\nlua_order_guard|phase=' .. phase .. '|ok=' .. tostring(ok)
            .. '|reason=' .. tostring(reason):gsub('[|\r\n]', ' ') .. '|effects=false'
    end
    local menu = Helper.getMenu('PlayerInfoMenu')
    local statusOk, status = pcall(require, 'extensions.tm_empire_management.ui.empire_status')
    if not statusOk then status = nil end
    local hooks = menu and type(menu.registerCallback) == 'function'
    local projection = status and status.snapshot and status.snapshot()
    local raw = GetNPCBlackboard(ConvertStringToLuaID(tostring(require('ffi').C.GetPlayerID())), '$tm_empire_projection')
    local shape = type(raw)
    if tostring(data):match('^trade_quote_probe|') or tostring(data):match('^domain|phase=market_') then
        local ok, result = pcall(function()
            local player = ConvertStringToLuaID(tostring(require('ffi').C.GetPlayerID()))
            local context = GetNPCBlackboard(player, '$tm_empire_diagnostic_trade_quote')
            if type(context) ~= 'table' or type(context.source) ~= 'userdata'
                or type(context.ship) ~= 'userdata' then return 'trade_quote|context_unavailable' end
            local ship, source = ConvertIDTo64Bit(context.ship), ConvertIDTo64Bit(context.source)
            local offers = GetTradeList(source, ship, false)
            if type(offers) ~= 'table' then return 'trade_quote|list_unavailable' end
            local lines, count = {}, 0
            local function fields(value)
                if type(value) ~= 'table' then return 'type=' .. type(value) end
                local keys, parts = {}, {}
                for key in pairs(value) do if type(key) == 'string' then keys[#keys+1] = key end end
                table.sort(keys)
                for i=1, math.min(#keys, 24) do
                    local key, item = keys[i], value[keys[i]]
                    if type(item) == 'number' or type(item) == 'boolean' or type(item) == 'string' then
                        parts[#parts+1] = key .. '=' .. tostring(item):gsub('[|\r\n]', ' '):sub(1, 80)
                    else parts[#parts+1] = key .. ':type=' .. type(item) end
                end
                return table.concat(parts, '|')
            end
            for _, offer in pairs(offers) do
                if type(offer) == 'table' then
                    count = count + 1
                    lines[#lines+1] = 'trade_quote_list|' .. fields(offer)
                    if offer.id and IsValidTrade(offer.id) then
                        lines[#lines+1] = 'trade_quote_ship|' .. fields(GetTradeData(offer.id, ship))
                        lines[#lines+1] = 'trade_quote_plain|' .. fields(GetTradeData(offer.id))
                    end
                    if count >= (tostring(data):match('^domain|phase=market_') and 16 or 4) then break end
                end
            end
            return 'trade_quote|sample=' .. count .. '\n' .. table.concat(lines, '\n')
        end)
        data = tostring(data) .. '\n' .. (ok and result or ('trade_quote|error=' .. tostring(result)))
    end
    local owner = ConvertStringToLuaID(tostring(require('ffi').C.GetPlayerID()))
    local purchase = GetNPCBlackboard(owner, '$tm_empire_purchase_submission')
    local match = GetNPCBlackboard(owner, '$tm_empire_purchase_match')
    local plotPayment=GetNPCBlackboard(owner,'$tm_empire_plot_receipt')
    if type(plotPayment)=='table' and type(plotPayment.key)=='string' then
        local ok,details=pcall(function()
            local ffi=require('ffi')
            local issued=tonumber(plotPayment.key:match('_([%d%.]+)$'))
            assert(issued,'plot_time_unavailable')
            local count=tonumber(ffi.C.GetNumTransactionLog(ffi.C.GetPlayerID(),issued-1,issued+10))
            local result='plot_transactions|key='..plotPayment.key..'|count='..tostring(count)
            if count>256 then return result..'|complete=false' end
            local rows=ffi.new('TransactionLogEntry[?]',math.max(1,count))
            local read=tonumber(ffi.C.GetTransactionLog(rows,count,ffi.C.GetPlayerID(),issued-1,issued+10))
            result=result..'|read='..read..'|complete='..tostring(read==count and read<=64)
            for i=0,math.min(read,64)-1 do
                result=result..'\nplot_transaction|time='..tonumber(rows[i].time)
                    ..'|money_Cr='..tonumber(rows[i].money)/100
                    ..'|event='..ffi.string(rows[i].eventtype)..'|partner='..tostring(rows[i].partnerid)
                    ..'|entry='..tostring(rows[i].entryid)..'|complete='..tostring(rows[i].complete)
            end
            return result
        end)
        data=tostring(data)..'\n'..(ok and details or ('plot_transactions|error='..tostring(details)))
    end
    for _,key in ipairs({'$tm_empire_supply_request','$tm_empire_supply_payment'}) do
        local value=GetNPCBlackboard(owner,key)
        if type(value)=='table' then
            data=tostring(data)..'\nsupply_lua|board='..key
            for _,field in ipairs({'key','state','reason','ware','amount','price','repriced','budget','available','paid'}) do
                data=data..'|'..field..'='..tostring(value[field])
            end
            data=data..'|effects=false'
        end
    end
    for _,key in ipairs({'$tm_empire_station_funding','$tm_empire_station_payment'}) do
        local value=GetNPCBlackboard(owner,key)
        if type(value)=='table' then
            data=tostring(data)..'\nstation_funding_lua|board='..key
            for _,field in ipairs({'key','state','reason','amount','paid','balance','wanted','budget',
                'before','after','stationbefore','stationafter'}) do
                data=data..'|'..field..'='..tostring(value[field])
            end
            if key=='$tm_empire_station_funding' and type(value.station)=='userdata' then
                local ok, observed=pcall(function()
                    local owned,balance,wanted=GetComponentData(value.station,
                        'isplayerowned','money','productionmoney')
                    return '\nstation_funding_observation|key='..tostring(value.key)
                        ..'|owned='..tostring(owned)..'|balance='..tostring(balance)
                        ..'|wanted='..tostring(wanted)..'|balance_type='..type(balance)
                        ..'|wanted_type='..type(wanted)..'|effects=false'
                end)
                data=data..(ok and observed or ('\nstation_funding_observation|error='
                    ..tostring(observed)..'|effects=false'))
            end
        end
    end
    for _,key in ipairs({'$tm_empire_plot_request','$tm_empire_construction_funding'}) do
        local value=GetNPCBlackboard(owner,key)
        if type(value)=='table' then
            data=tostring(data)..'\nconstruction_lua|board='..key..'|key='..tostring(value.key)
                ..'|state='..tostring(value.state)..'|budget='..tostring(value.budget)
                ..'|reason='..tostring(value.reason)..'|wanted='..tostring(value.wanted)..'|balance='..tostring(value.balance)
                ..'|observedwanted='..tostring(value.observedwanted)..'|observedbalance='..tostring(value.observedbalance)
                ..'|newconstruction='..tostring(value.newconstruction)..'|newconstruction_type='..type(value.newconstruction)
                ..'|extend='..tostring(value.extend)..'|extend_type='..type(value.extend)
            if key=='$tm_empire_plot_request' and type(value.station)=='userdata' then
                local ok,details=pcall(function()
                    local ffi=require('ffi')
                    local station64=ConvertIDTo64Bit(value.station)
                    local context64=ffi.C.GetContextByClass(station64,'sector',false)
                    local sectorID=GetComponentData(value.station,'sectorid')
                    local contextID=ConvertStringToLuaID(tostring(context64))
                    local nativeOwner=GetComponentData(contextID,'owner')
                    local stockOwner=sectorID and GetComponentData(sectorID,'owner')
                    return '|context_sector='..tostring(context64)..'|stock_sector='..tostring(sectorID)
                        ..'|context_owner='..tostring(nativeOwner)..'|context_owner_type='..type(nativeOwner)
                        ..'|stock_owner='..tostring(stockOwner)..'|stock_owner_type='..type(stockOwner)
                end)
                data=tostring(data)..'\nplot_context|'..(ok and details or tostring(details))
            end
        end
    end
    for _,key in ipairs({'$tm_empire_builder_request','$tm_empire_builder_result'}) do
        local value=GetNPCBlackboard(owner,key)
        if type(value)=='table' then
            data=tostring(data)..'\nbuilder_lua|board='..key..'|key='..tostring(value.key)
                ..'|state='..tostring(value.state)..'|reason='..tostring(value.reason)
                ..'|fee='..tostring(value.fee)..'|paid='..tostring(value.paid)
                ..'|ship_type='..type(value.ship)..'|station_type='..type(value.station)
                ..'|storage_type='..type(value.storage)..'|budget_type='..type(value.budget)
        end
    end
    if type(purchase)=='table' then
        data = tostring(data) .. '\npurchase_lua|state=' .. tostring(purchase.state)
            .. '|id=' .. tostring(purchase.id) .. '|price=' .. tostring(purchase.price)
            .. '|paid=' .. tostring(purchase.paid) .. '|money=' .. tostring(GetPlayerMoney())
            .. '|match_reason=' .. tostring(purchase.match_reason) .. '|candidateid=' .. tostring(purchase.candidateid)
            .. '|matched_index=' .. tostring(type(match)=='table' and match.candidateindex)
    end
    if projection and projection.inventory then
        local inventory = projection.inventory
        shape = shape .. '|assets=' .. inventory.counts.total .. '|stations=' .. inventory.counts.station
            .. '|waiting=' .. inventory.states.waiting .. '|excluded=' .. inventory.states.excluded
            .. '|rows=' .. #projection.rows .. '|snapshot_from=' .. inventory.from .. '|snapshot_to=' .. inventory.to
        for _, kind in ipairs({'station','ship_s','ship_m','ship_l','ship_xl','other'}) do
            shape = shape .. '|count_' .. kind .. '=' .. inventory.counts[kind]
        end
        for _, state in ipairs({'waiting','sent','unknown','excluded'}) do
            shape = shape .. '|state_' .. state .. '=' .. inventory.states[state]
        end
    end
    if projection and projection.observations then
        shape = shape .. '|station_statuses=' .. #projection.observations
        for index, station in ipairs(projection.observations) do
            if index > 32 then break end
            shape = shape .. '\nstation_status|station=' .. tostring(station.station)
                .. '|employee=' .. tostring(station.employee)
                .. '|state=' .. tostring(station.workstate or 'unknown')
                .. '|reason=' .. tostring(station.reason)
                .. '|assessment_present=' .. tostring(station.assessment ~= nil)
                .. '|history_present=' .. tostring(station.previous_periods ~= nil)
        end
    end
    if projection and projection.tasks then
        shape = shape .. '|tasks=' .. #projection.tasks
        for i = 1, math.min(8, #projection.tasks) do
            local task = projection.tasks[i]
            shape = shape .. '|task' .. i .. '=' .. task.name:gsub('[|\r\n]', ' ')
                .. ':' .. task.state:gsub('[|\r\n]', ' ') .. ':' .. task.reason:gsub('[|\r\n]', ' ')
            for _, key in ipairs({'source','target','person'}) do
                if task[key] then shape = shape .. '|task' .. i .. '_' .. key .. '=' .. task[key]:gsub('[|\r\n]', ' ') end
            end
        end
    end
    if type(raw) == 'table' then
        shape = shape .. '|schema=' .. tostring(raw.schema) .. '|governor=' .. tostring(raw.has_governor)
            .. ':' .. type(raw.has_governor) .. '|active=' .. tostring(raw.active) .. ':' .. type(raw.active)
        shape = shape .. '|reason=' .. tostring(raw.reason):gsub('[|\r\n]', ' ')
    end
    Pipes.Schedule_Write(PIPE, function() arm() end, tostring(data) .. '\nui_hook|' .. tostring(hooks)
        .. '|projection=' .. tostring(projection ~= nil) .. '|raw=' .. shape)
end
arm = function()
    Presence.when_ready(PIPE, function()
        Pipes.Schedule_Read(PIPE, function(message)
            local scenarioSlot = type(message) == 'string' and (message:match('^save_scenario_checkpoint|preflight_(save_01[5-9])_absent$') or message:match('^save_scenario_checkpoint|preflight_(save_02[0-9])_absent$') or message:match('^save_scenario_checkpoint|preflight_(save_03[0-9])_absent$'))
            local cleanShutdownSlot = type(message) == 'string' and message:match('^save_clean_shutdown|preflight_(save_04[01])_absent$') or nil
            if message == 'ERROR' then
                Time.Set_Alarm('tm_empire_probe_retry', 2, function() arm() end)
            elseif message == 'projection_raw' then
                local status = require('extensions.tm_empire_management.ui.empire_status')
                local player = ConvertStringToLuaID(tostring(require('ffi').C.GetPlayerID()))
                local raw = GetNPCBlackboard(player, '$tm_empire_projection')
                local lines = {'projection_raw|effects=false|type=' .. type(raw)}
                if type(raw) == 'table' then
                    local base = {}
                    for _, key in ipairs({'schema','has_governor','active','governor_name','station_name','module_name','reason','updated'}) do
                        local value = raw[key]
                        if key == 'has_governor' or key == 'active' then
                            if value == 0 then value = false elseif value == 1 then value = true end
                        end
                        base[key] = value
                        lines[#lines+1] = 'field|' .. key .. '|type=' .. type(value) .. '|value=' .. tostring(value):sub(1,160):gsub('[|\r\n]', ' ')
                    end
                    base.rows = {}
                    lines[#lines+1] = 'base|valid=' .. tostring(status.validate(base) ~= nil)
                    for _, key in ipairs({'rows','inventory','tasks','observations'}) do
                        local candidate = {}
                        for name,value in pairs(base) do candidate[name] = value end
                        candidate[key] = raw[key]
                        lines[#lines+1] = 'section|' .. key .. '|type=' .. type(raw[key]) .. '|valid=' .. tostring(status.validate(candidate) ~= nil) .. '|count=' .. tostring(type(raw[key])=='table' and #raw[key] or -1)
                        if type(raw[key]) == 'table' and key ~= 'inventory' then
                            for index = 1, math.min(64, #raw[key]) do
                                local item = raw[key][index]
                                candidate[key] = {item}
                                if status.validate(candidate) == nil and type(item) == 'table' then
                                    lines[#lines+1] = 'invalid_item|' .. key .. '|index=' .. index
                                    local count = 0
                                    for name,value in pairs(item) do
                                        count = count+1
                                        if count <= 24 then lines[#lines+1] = 'item_field|' .. tostring(name) .. '|type=' .. type(value) .. '|length=' .. (type(value)=='string' and #value or 0) .. '|value=' .. tostring(value):sub(1,160):gsub('[|\r\n]', ' ') end
                                    end
                                end
                            end
                        end
                    end
                end
                respond(nil, table.concat(lines, '\n'))
            elseif message == 'status_asset_read' then
                local projection = require('extensions.tm_empire_management.ui.empire_status').snapshot()
                local rows = type(projection) == 'table' and projection.rows or nil
                local lines = {'status_asset_read|rows=' .. tostring(type(rows) == 'table' and #rows or -1) .. '|effects=false'}
                if type(rows) == 'table' then
                    for index, row in ipairs(rows) do
                        if type(row) == 'table' and type(row.reason) == 'string' and
                           (row.reason:find('Ручной', 1, true) or row.reason:find('приоритетный', 1, true)
                            or row.reason:find('нет капитана', 1, true)) then
                            lines[#lines+1] = 'status_asset|index=' .. index .. '|name=' .. tostring(row.name)
                                .. '|state=' .. tostring(row.state) .. '|reason=' .. row.reason:gsub('[|\r\n]', ' ')
                        end
                    end
                end
                respond(nil, table.concat(lines, '\n'))
            elseif message == 'crew_service_preflight' then
                AddUITriggeredEvent('TM_Empire_Probe', 'CrewServicePreflight')
            elseif message == 'crew_service_bulk_fixture' then
                AddUITriggeredEvent('TM_Empire_Probe', 'CrewServiceBulkFixture')
            elseif message == 'crew_service_bulk_large_fixture' then
                AddUITriggeredEvent('TM_Empire_Probe', 'CrewServiceBulkLargeFixture')
            elseif message == 'crew_service_bulk_fixture_read' then
                AddUITriggeredEvent('TM_Empire_Probe', 'CrewServiceBulkFixtureRead')
            elseif message == 'crew_service_bulk_trigger' then
                AddUITriggeredEvent('TM_Empire_Probe', 'CrewServiceBulkTrigger')
            elseif message == 'crew_service_bulk_queue' then
                AddUITriggeredEvent('TM_Empire_Probe', 'CrewServiceBulkQueue')
            elseif message == 'crew_service_bulk_isolate' then
                AddUITriggeredEvent('TM_Empire_Probe', 'CrewServiceBulkIsolate')
            elseif message == 'crew_service_exhaust' then
                AddUITriggeredEvent('TM_Empire_Probe', 'CrewServiceExhaust')
            elseif message == 'crew_service_md_state' then
                AddUITriggeredEvent('TM_Empire_Probe', 'CrewServiceMDState')
            elseif message == 'crew_service_carriers' then
                AddUITriggeredEvent('TM_Empire_Probe', 'CrewServiceCarriers')
            elseif message == 'crew_service_assign_cap' then
                AddUITriggeredEvent('TM_Empire_Probe', 'CrewServiceAssignCaptain')
            elseif message == 'crew_service_pause_personnel' then
                AddUITriggeredEvent('TM_Empire_Probe', 'CrewServicePausePersonnel')
            elseif message == 'crew_service_trial_md_read' or message == 'crew_service_bulk_md_read' then
                AddUITriggeredEvent('TM_Empire_Probe', 'CrewServiceTrialMDRead')
            elseif message == 'crew_service_trial_warp' or message == 'crew_service_bulk_warp' then
                AddUITriggeredEvent('TM_Empire_Probe', 'CrewServiceTrialWarp')
            elseif message == 'crew_service_bulk_dock' then
                AddUITriggeredEvent('TM_Empire_Probe', 'CrewServiceTrialDock')
            elseif message == 'crew_service_state' then
                local ffi = require('ffi')
                local owner = ConvertStringToLuaID(tostring(ffi.C.GetPlayerID()))
                local request = GetNPCBlackboard(owner, '$tm_empire_crew_service_request')
                local receipt = GetNPCBlackboard(owner, '$tm_empire_crew_service_receipt')
                local function field(row, key)
                    return type(row) == 'table' and tostring(row[key]) or 'nil'
                end
                respond(nil, 'crew_service_state|request=' .. field(request, 'state')
                    .. '|request_key=' .. field(request, 'key')
                    .. '|request_reason=' .. field(request, 'reason')
                    .. '|ship=' .. field(request, 'ship')
                    .. '|yard=' .. field(request, 'yard')
                    .. '|amount=' .. field(request, 'amount')
                    .. '|receipt=' .. field(receipt, 'state')
                    .. '|receipt_key=' .. field(receipt, 'key')
                    .. '|receipt_id=' .. field(receipt, 'id')
                    .. '|receipt_reason=' .. field(receipt, 'reason')
                    .. '|payment_called=' .. tostring(type(receipt) == 'table'
                        and receipt.state ~= 'prepared'))
            elseif message == 'crew_service_plan_probe' then
                local ffi = require('ffi')
                local owner = ConvertStringToLuaID(tostring(ffi.C.GetPlayerID()))
                local fixture = GetNPCBlackboard(owner, '$tm_empire_crew_service_probe')
                local ships = type(fixture) == 'table' and fixture.ships or {}
                local yards = type(fixture) == 'table' and fixture.yards or {}
                local ok, answer = pcall(function()
                    local builder = require('extensions.tm_empire_management.ui.crew_service_plan')
                    local errors = {}
                    for _, ship in ipairs(ships) do
                        local shipid = ConvertIDTo64Bit(ship)
                        local plan, reason, detail = builder.snapshot(ship, 1)
                        if plan then
                            for _, yard in ipairs(yards) do
                                if ffi.C.CanContainerEquipShip(ConvertIDTo64Bit(yard), shipid) then
                                    return 'crew_service_plan_probe|ship=' .. tostring(ship)
                                        .. '|yard=' .. tostring(yard)
                                        .. '|engine=' .. detail.engine
                                        .. '|engines=' .. #plan.engine
                                        .. '|weapons=' .. #plan.weapon
                                        .. '|shields=' .. #plan.shield
                                        .. '|turrets=' .. #plan.turret
                                        .. '|groups=' .. #plan.shieldgroup
                                        .. '|software=' .. detail.software
                                        .. '|service_after=' .. detail.crew
                                        .. '|payment_called=false'
                                end
                            end
                        else
                            table.insert(errors, tostring(reason))
                        end
                    end
                    return 'crew_service_plan_probe|state=no_compatible_safe_pair|errors='
                        .. table.concat(errors, ','):sub(1, 200) .. '|payment_called=false'
                end)
                respond(nil, ok and answer or ('crew_service_plan_probe|error=' .. tostring(answer)))
            elseif message == 'crew_service_trial' or message == 'crew_service_bulk_trial' then
                local ffi = require('ffi')
                require('extensions.tm_empire_management.ui.purchase_quote')
                require('extensions.tm_empire_management.ui.purchase_receipt')
                local owner = ConvertStringToLuaID(tostring(ffi.C.GetPlayerID()))
                local bulk = message == 'crew_service_bulk_trial'
                local label = bulk and 'crew_service_bulk_trial' or 'crew_service_trial'
                local receiptBoard = bulk and '$tm_empire_crew_service_bulk_trial'
                    or '$tm_empire_crew_service_trial'
                -- This probe runs only after CrewServiceBulkFixture confirmed
                -- exactly 14 free seats on the freshly created test frigate.
                local amount = bulk and 14 or 1
                local prior = GetNPCBlackboard(owner, receiptBoard)
                if type(prior) == 'table' then
                    respond(nil, label .. '|state=previous_trial|payment_called=false')
                else
                    local fixture = GetNPCBlackboard(owner, '$tm_empire_crew_service_probe')
                    local ships = type(fixture) == 'table'
                        and (bulk and fixture.bulkships or fixture.ships) or {}
                    local yards = type(fixture) == 'table' and fixture.yards or {}
                    local ok, result = pcall(function()
                        for _, ship in ipairs(ships) do
                            local plan, planreason, planDetail =
                                require('extensions.tm_empire_management.ui.crew_service_plan')
                                    .snapshot(ship, amount)
                            for _, yard in ipairs(yards) do
                                local shipid, yardid = ConvertIDTo64Bit(ship), ConvertIDTo64Bit(yard)
                                if plan and ffi.C.CanContainerEquipShip(yardid, shipid) then
                                    local workforce = ffi.C.GetWorkForceInfo(yardid, '')
                                    local available, maximum = tonumber(workforce.available), tonumber(workforce.maxavailable)
                                    assert(maximum > 0 and available >= 0 and available <= maximum, 'workforce_unknown')
                                    local minprice, maxprice = GetWareData('crew', 'minprice', 'maxprice')
                                    local discount = 1
                                    for _, entry in ipairs(GetComponentData(yard, 'hiringdiscounts') or {}) do
                                        discount = discount - entry.amount / 100
                                    end
                                    local price = RoundTotalTradePrice(Helper.round(discount
                                        * ffi.C.GetContainerBuildPriceFactor(yardid)
                                        * (maxprice - available / maximum * (maxprice - minprice))))
                                    assert(price > 0 and price <= 100000
                                        and price * amount <= 300000
                                        and GetPlayerMoney() >= price * amount,
                                        'trial_price_or_money_invalid')
                                    local engine = planDetail.engine
                                    local receipt = {state='payment_sent', ship=ship, yard=yard,
                                        price=price, amount=amount, before=GetPlayerMoney(),
                                        loadout='full_current_equipment', engine_before=engine}
                                    SetNPCBlackboard(owner, receiptBoard, receipt)
                                    TransferPlayerMoneyTo(price * amount, yardid)
                                    assert(receipt.before - GetPlayerMoney() == price * amount,
                                        'trial_payment_unknown')
                                    local crewplan = {hireddetails={{newrole='service', amount=amount, price=price}},
                                        fired={}, transferdetails={}}
                                    local id = Helper.callLoadoutFunction(plan, crewplan, function(loadout, crew)
                                        assert(tonumber(loadout.numengines) > 0 and tonumber(crew.numadded) == 1
                                            and tonumber(crew.added[0].amount) == amount,
                                            'trial_crew_plan_invalid')
                                        return ffi.C.AddBuildTask6(yardid, shipid, '', loadout,
                                            0, crew, false, '', ffi.new('AddBuildTask6Container'))
                                    end, nil, 'UILoadout2')
                                    assert(id ~= 0, 'trial_build_unknown_after_payment')
                                    receipt.id = tostring(id)
                                    SetNPCBlackboard(owner, receiptBoard, receipt)
                                    local info = ffi.C.GetBuildTaskInfo(id)
                                    assert(info.id == id and info.buildingcontainer == yardid,
                                        'trial_build_identity_unknown')
                                    ffi.C.SetBuildTaskTransferredMoney(id, price)
                                    receipt.state = 'built'
                                    SetNPCBlackboard(owner, receiptBoard, receipt)
                                    return label .. '|state=built|ship=' .. tostring(ship)
                                        .. '|yard=' .. tostring(yard) .. '|price=' .. price
                                        .. '|amount=' .. amount
                                        .. '|build=' .. tostring(id) .. '|engine_before=' .. engine
                                        .. '|payment_called=true'
                                end
                            end
                        end
                        return label .. '|state=no_compatible_pair|payment_called=false'
                    end)
                    respond(nil, ok and result or (label .. '|state=unknown|reason=' .. tostring(result)))
                end
            elseif message == 'crew_service_trial_read' or message == 'crew_service_bulk_read' then
                local ffi = require('ffi')
                require('extensions.tm_empire_management.ui.purchase_receipt')
                local owner = ConvertStringToLuaID(tostring(ffi.C.GetPlayerID()))
                local bulk = message == 'crew_service_bulk_read'
                local label = bulk and 'crew_service_bulk_read' or 'crew_service_trial_read'
                local receipt = GetNPCBlackboard(owner, bulk and '$tm_empire_crew_service_bulk_trial'
                    or '$tm_empire_crew_service_trial')
                if type(receipt) ~= 'table' then
                    receipt = GetNPCBlackboard(owner, '$tm_empire_crew_service_receipt')
                end
                local ok, answer = pcall(function()
                    assert(type(receipt) == 'table' and receipt.ship and receipt.yard and receipt.id,
                        'trial_receipt_missing')
                    local shipid = ConvertIDTo64Bit(receipt.ship)
                    local build = ffi.new('BuildTaskID', tonumber(tostring(receipt.id):match('^%d+')))
                    local info = ffi.C.GetBuildTaskInfo(build)
                    local engine = ffi.string(ffi.C.GetUpgradeSlotCurrentMacro(shipid, 0, 'engine', 1))
                    local n = ffi.C.GetNumAllRoles()
                    local people = ffi.new('PeopleInfo[?]', n)
                    n = ffi.C.GetPeople2(people, n, shipid, true)
                    local service = 0
                    for i=0,n-1 do
                        if ffi.string(people[i].id) == 'service' then service = service + people[i].amount end
                    end
                    return label .. '|receipt=' .. receipt.state
                        .. '|amount=' .. tostring(receipt.amount)
                        .. '|build_id=' .. tostring(info.id)
                        .. '|build_component=' .. tostring(info.component)
                        .. '|build_yard=' .. tostring(info.buildingcontainer)
                        .. '|queue=' .. tonumber(info.queueposition)
                        .. '|missing_resources=' .. tostring(info.ismissingresources)
                        .. '|service=' .. service
                        .. '|engine_before=' .. tostring(receipt.engine_before)
                        .. '|engine_now=' .. engine
                        .. '|money_after=' .. GetPlayerMoney()
                        .. '|effects=false'
                end)
                respond(nil, ok and answer or (label .. '|error=' .. tostring(answer)))
            elseif message == 'read' then
                AddUITriggeredEvent('TM_Empire_Probe', 'Read')
            elseif message == 'governor_remote_prepare' then
                AddUITriggeredEvent('TM_Empire_Probe', 'GovernorRemotePrepare')
            elseif message == 'governor_dialog_cancel' then
                -- Native Helper.closeMenuAndCancelConversation uses this API.
                -- Cancel only the test conversation, not an assignment/journey.
                if type(CancelConversation) == 'function' then
                    CancelConversation()
                    respond(nil, 'governor_dialog|cancel_requested|assignment_effects=false')
                else
                    respond(nil, 'governor_dialog|cancel_unavailable|assignment_effects=false')
                end
            elseif message == 'governor_dialog_open' or message == 'governor_dialog_default' or message == 'governor_dialog_remote' then
                dialogChoicesSent = {}
                AddUITriggeredEvent('TM_Empire_Probe', 'GovernorDialogOpen', message == 'governor_dialog_default' and 'default' or message == 'governor_dialog_remote' and 'remote' or 'tm_empire_roles')
            elseif message == 'governor_dialog_read' or message == 'governor_dialog_release' or message == 'governor_dialog_assign' or message == 'governor_dialog_back' or message == 'governor_dialog_more' or message == 'governor_dialog_roles' or message == 'governor_dialog_goodbye' then
                if type(GetDialogOption) ~= 'function' or type(SelectDialogOption) ~= 'function' then
                    respond(nil, 'governor_dialog|native_functions_unavailable|effects=false')
                    return
                end
                local context = GetNPCBlackboard(ConvertStringToLuaID(tostring(require('ffi').C.GetPlayerID())), '$tm_empire_diagnostic_dialog')
                local lines, selected = {'governor_dialog|command=' .. message}, nil
                local expected = message == 'governor_dialog_release' and ReadText(98761, 11)
                    or message == 'governor_dialog_goodbye' and ReadText(1002, 2)
                    or message == 'governor_dialog_more' and ReadText(1002, 12025)
                    or message == 'governor_dialog_roles' and ReadText(98761, 10)
                    or message == 'governor_dialog_back' and ReadText(1002, 20)
                    or message == 'governor_dialog_assign' and type(context) == 'table' and context.assigntext
                for index = 1, 6 do
                    local text, selectable = GetDialogOption(index)
                    lines[#lines + 1] = 'dialog_option|index=' .. index .. '|selectable=' .. tostring(selectable)
                        .. '|text=' .. tostring(text):gsub('[|\r\n]', ' ')
                    if expected and text == expected and selectable then
                        if selected then selected = false; break end
                        selected = index
                    end
                end
                -- Exact option text only; never select an arbitrary active item.
                if message ~= 'governor_dialog_read' then
                    local ownerobject = type(context) == 'table' and context.actor
                    if type(ownerobject) == 'table' then ownerobject = ownerobject[1] end
                    local owned = type(ownerobject) == 'userdata' and GetComponentData(ownerobject, 'isplayerowned')
                    if selected and type(context) == 'table' and type(ownerobject) == 'userdata'
                        and (owned == true or owned == 1) and (message == 'governor_dialog_back' or not dialogChoicesSent[message]) then
                        dialogChoicesSent[message] = true
                        SelectDialogOption(selected)
                        lines[#lines + 1] = 'dialog_choice|state=sent|index=' .. selected
                    else
                        lines[#lines + 1] = 'dialog_choice|state=rejected_before_effect|reason=expected_option_unavailable'
                    end
                end
                respond(nil, table.concat(lines, '\n'))
            elseif message == 'governor_roles_setup' then
                AddUITriggeredEvent('TM_Empire_Probe', 'GovernorRolesSetup')
            elseif message == 'governor_roles_check' then
                AddUITriggeredEvent('TM_Empire_Probe', 'GovernorRolesCheck')
            elseif message == 'governor_roles_read' then
                AddUITriggeredEvent('TM_Empire_Probe', 'GovernorRolesRead')
            elseif message == 'hire_candidates' then
                AddUITriggeredEvent('TM_Empire_Probe', 'HireCandidates')
            elseif message == 'personnel_prerequisite' then
                AddUITriggeredEvent('TM_Empire_Probe', 'PersonnelPrerequisite')
            elseif message == 'personnel_autonomous_read' then
                AddUITriggeredEvent('TM_Empire_Probe', 'PersonnelAutonomousRead')
            elseif message == 'personnel_sources_read' then
                AddUITriggeredEvent('TM_Empire_Probe', 'PersonnelSourcesRead')
            elseif message == 'hire_setup' then
                AddUITriggeredEvent('TM_Empire_Probe', 'HireScenarioSetup')
            elseif message == 'hire_candidate_next' then
                AddUITriggeredEvent('TM_Empire_Probe', 'HireCandidateNext')
            elseif message == 'trade_quote_probe' then
                AddUITriggeredEvent('TM_Empire_Probe', 'TradeQuoteProbe')
            elseif message == 'trade_decision_fixture' then
                AddUITriggeredEvent('TM_Empire_Probe', 'TradeDecisionFixture')
            elseif message == 'assessment_fixture' then
                AddUITriggeredEvent('TM_Empire_Probe', 'StationAssessmentFixture')
            elseif message == 'crew_attention' or message == 'crew_attention_restore' then
                AddUITriggeredEvent('TM_Empire_Probe', 'CrewAttention', message)
            elseif message == 'builder_near' then
                AddUITriggeredEvent('TM_Empire_Probe', 'BuilderNearSetup')
            elseif message == 'local_builder' or message == 'local_owned_builder' then
                AddUITriggeredEvent('TM_Empire_Probe', 'LocalBuilderSetup', message == 'local_owned_builder' and 'owned' or 'npc')
            elseif message == 'construction_resources' then
                AddUITriggeredEvent('TM_Empire_Probe', 'ConstructionResourcesSetup')
            elseif message:match('^priority_') then
                local phase=message:sub(10)
                if ({setup=true,passenger=true,helm=true,manual=true,priority=true,restore=true,read=true})[phase] then
                    AddUITriggeredEvent('TM_Empire_Probe', 'ShipPriorityFixture', phase)
                end
            elseif message == 'supply_setup' or message == 'supply_quote' or message == 'supply_step' or message == 'supply_read' then
                AddUITriggeredEvent('TM_Empire_Probe', ({supply_setup='SupplyScenarioSetup', supply_quote='SupplyScenarioQuote', supply_step='SupplyScenarioStep', supply_read='SupplyScenarioRead'})[message])
            elseif message == 'service_setup' then
                AddUITriggeredEvent('TM_Empire_Probe', 'ServiceStationSetup')
            elseif message == 'mining_setup' or message == 'mining_read' then
                AddUITriggeredEvent('TM_Empire_Probe', message == 'mining_setup' and 'MiningStationSetup' or 'MiningStationRead')
            elseif message == 'factory_build_start' then
                AddUITriggeredEvent('TM_Empire_Probe', 'FactoryBuildStart')
            elseif message == 'repair_setup' then
                AddUITriggeredEvent('TM_Empire_Probe', 'RepairScenarioSetup')
            elseif message == 'repair_scenario' then
                AddUITriggeredEvent('TM_Empire_Probe', 'RepairScenarioRun')
            elseif message == 'repair_read' then
                AddUITriggeredEvent('TM_Empire_Probe', 'RepairScenarioRead')
            elseif message == 'military_fleet_prepare' then
                AddUITriggeredEvent('TM_Empire_Probe', 'MilitaryFleetPrepare')
            elseif message == 'military_refresh_report' then
                AddUITriggeredEvent('TM_Empire_Probe', 'MilitaryRefreshReport')
            elseif message == 'military_visibility_probe' then
                AddUITriggeredEvent('TM_Empire_Probe', 'MilitaryVisibilityProbe')
            elseif message == 'military_setup' then
                AddUITriggeredEvent('TM_Empire_Probe', 'MilitaryTerritorySetup')
            elseif message == 'hire_scenario' then
                AddUITriggeredEvent('TM_Empire_Probe', 'HireScenarioRun')
            elseif message == 'trade_fixture' then
                AddUITriggeredEvent('TM_Empire_Probe', 'TradeFixture')
            elseif message == 'native_analysis' then
                AddUITriggeredEvent('TM_Empire_Probe', 'NativeAnalysis')
            elseif message == 'economic_search_start' or message == 'economic_search_read' then
                AddUITriggeredEvent('TM_Empire_Probe', 'EconomicSearchProbe', message == 'economic_search_start' and 'start' or 'read')
            elseif message == 'economic_transport_prepare' then
                AddUITriggeredEvent('TM_Empire_Probe', 'EconomicTransportPrepare')
            elseif message == 'lifecycle_prepare' or message == 'lifecycle_bind'
                or message == 'lifecycle_module_loss' or message == 'lifecycle_station_loss'
                or message == 'lifecycle_actor_loss' or message == 'lifecycle_rebind'
                or message == 'lifecycle_restore' or message == 'lifecycle_read' then
                AddUITriggeredEvent('TM_Empire_Probe', 'LifecycleProbe', message:sub(11))
            elseif message == 'mining_trace_arm' or message == 'mining_trace_read' then
                AddUITriggeredEvent('TM_Empire_Probe', 'MiningDeliveryTrace', message == 'mining_trace_arm' and 'arm' or 'read')
            elseif message == 'crew_capacity_check' then
                AddUITriggeredEvent('TM_Empire_Probe', 'CrewCapacityProbe')
            elseif message == 'station_manager_vacate' or message == 'station_manager_replace' or message == 'station_manager_restore_prepare' or message == 'station_manager_restore' or message == 'station_manager_read' then
                AddUITriggeredEvent('TM_Empire_Probe', 'StationManagerPeriodProbe', ({station_manager_vacate='vacate', station_manager_replace='replace', station_manager_restore_prepare='restore_vacate', station_manager_restore='restore', station_manager_read='read'})[message])
            elseif message == 'governor_ownership_loss' or message == 'governor_ownership_restore' or message == 'governor_ownership_read' then
                AddUITriggeredEvent('TM_Empire_Probe', 'GovernorOwnershipProbe', ({governor_ownership_loss='loss', governor_ownership_restore='restore', governor_ownership_read='read'})[message])
            elseif message == 'domain_threat_retire' or message == 'domain_buyer_support' or message == 'domain_threat_distress' or message == 'domain_threat_provoke' or message == 'domain_large_asset_loss' or message == 'domain_large_assets' or message == 'domain_threat_range' or message == 'domain_mining_resources' or message == 'domain_surplus_prepare' or message == 'domain_threat_prepare' or message == 'domain_complete_crews' or message == 'domain_read'
                or message == 'domain_builder_repath' or message == 'domain_threat_resume' or message == 'domain_surplus_watch'
                or message == 'domain_market_source' or message == 'domain_market_buyer' or message == 'domain_builder_position' or message == 'domain_threat_transport' or message == 'domain_seta_begin' or message == 'domain_seta_end' or message == 'domain_surplus_open' then
                AddUITriggeredEvent('TM_Empire_Probe', 'DomainProbe', message:sub(8))
            elseif message == 'crew_blocked_prepare' or message == 'crew_blocked_transfer'
                or message == 'crew_blocked_destination_loss' or message == 'crew_blocked_read' then
                AddUITriggeredEvent('TM_Empire_Probe', 'BlockedCrewProbe', message:sub(14))
            elseif message == 'crew_remote_prepare' or message == 'crew_remote_transfer' or message == 'crew_remote_read' then
                AddUITriggeredEvent('TM_Empire_Probe', 'CrewRemoteProbe', ({crew_remote_prepare='prepare', crew_remote_transfer='transfer', crew_remote_read='read'})[message])
            elseif message == 'economic_search_priority' or message == 'economic_search_priority_read' then
                AddUITriggeredEvent('TM_Empire_Probe', 'EconomicSearchProbe', message == 'economic_search_priority' and 'start_priority' or 'read_priority')
            elseif message == 'training_fixture' then
                AddUITriggeredEvent('TM_Empire_Probe', 'TrainingFixture')
            elseif message == 'expansion_fixture' then
                AddUITriggeredEvent('TM_Empire_Probe', 'ExpansionFixture')
            elseif message == 'expansion_native_fixture' then
                AddUITriggeredEvent('TM_Empire_Probe', 'ExpansionFixture', 'native')
            elseif message == 'construction_handoff' then
                AddUITriggeredEvent('TM_Empire_Probe', 'ConstructionHandoffFixture')
            elseif message == 'personnel_transfer_fixture' then
                AddUITriggeredEvent('TM_Empire_Probe', 'PersonnelTransferFixture')
            elseif message == 'crew_docked_prepare' then
                AddUITriggeredEvent('TM_Empire_Probe', 'CrewDockedPrepare')
            elseif message == 'personnel_transfer_prepare' then
                AddUITriggeredEvent('TM_Empire_Probe', 'PersonnelTransferPrepare')
            elseif message == 'idle_orders_read' then
                AddUITriggeredEvent('TM_Empire_Probe', 'IdleOrdersRead')
            elseif message == 'idle_courier_prepare' then
                AddUITriggeredEvent('TM_Empire_Probe', 'IdleCourierPrepare')
            elseif message == 'idle_courier_seek' then
                AddUITriggeredEvent('TM_Empire_Probe', 'IdleCourierSeek')
            elseif message == 'idle_courier_relocate' then
                AddUITriggeredEvent('TM_Empire_Probe', 'IdleCourierRelocate')
            elseif message == 'idle_courier_yield' then
                AddUITriggeredEvent('TM_Empire_Probe', 'IdleCourierYield')
            elseif message == 'idle_fallback_fixture' then
                AddUITriggeredEvent('TM_Empire_Probe', 'IdleFallbackFixture')
            elseif message == 'idle_fallback_read' then
                AddUITriggeredEvent('TM_Empire_Probe', 'IdleFallbackRead')
            elseif message == 'idle_mining_nearby_read' then
                AddUITriggeredEvent('TM_Empire_Probe', 'IdleMiningNearbyRead')
            elseif message == 'idle_fallback_eligibility_read' then
                AddUITriggeredEvent('TM_Empire_Probe', 'IdleFallbackEligibilityRead')
            elseif message == 'idle_fallback_seek_miner' then
                AddUITriggeredEvent('TM_Empire_Probe', 'IdleFallbackSeekMiner')
            elseif message == 'idle_fallback_seek_scout' then
                AddUITriggeredEvent('TM_Empire_Probe', 'IdleFallbackSeekScout')
            elseif message == 'idle_fallback_manual' then
                AddUITriggeredEvent('TM_Empire_Probe', 'IdleFallbackManual')
            elseif message == 'station_supply_setup' then
                AddUITriggeredEvent('TM_Empire_Probe', 'StationSupplySetup')
            elseif message == 'station_budget_setup' then
                AddUITriggeredEvent('TM_Empire_Probe', 'StationBudgetSetup')
            elseif message == 'station_budget_retry' then
                AddUITriggeredEvent('TM_Empire_Probe', 'StationBudgetRetry')
            elseif message == 'supply_boundary_retry' then
                AddUITriggeredEvent('TM_Empire_Probe', 'SupplyBoundaryRetry')
            elseif message == 'supply_boundary_step' then
                AddUITriggeredEvent('TM_Empire_Probe', 'SupplyBoundaryStep')
            elseif message == 'provision_read' then
                AddUITriggeredEvent('TM_Empire_Probe', 'ProvisionRead')
            elseif message == 'module_fixture' then
                AddUITriggeredEvent('TM_Empire_Probe', 'AddModule')
            elseif message == 'assign_fixture' then
                AddUITriggeredEvent('TM_Empire_Probe', 'Assign')
            elseif message == 'place_fixture' then
                AddUITriggeredEvent('TM_Empire_Probe', 'Place')
            elseif message == 'check_roles' then
                AddUITriggeredEvent('TM_Empire_Probe', 'CheckRoles')
            elseif message == 'release_fixture' then
                AddUITriggeredEvent('TM_Empire_Probe', 'Release')
            elseif message == 'shutdown_read' then
                AddUITriggeredEvent('TM_Empire_Probe', 'ShutdownRead')
            elseif message == 'shutdown_fixture' then
                AddUITriggeredEvent('TM_Empire_Probe', 'ShutdownFixture')
            elseif message == 'role_contract' then
                AddUITriggeredEvent('TM_Empire_Probe', 'RoleContract')
            elseif message == 'training_positive_fixture' then
                AddUITriggeredEvent('TM_Empire_Probe', 'TrainingPositiveFixture')
            elseif message == 'build_contract' then
                AddUITriggeredEvent('TM_Empire_Probe', 'BuildContract')
            elseif message == 'station_fixture' then
                AddUITriggeredEvent('TM_Empire_Probe', 'StationFixture')
            elseif message == 'construction_blueprint_prepare' then
                AddUITriggeredEvent('TM_Empire_Probe', 'ConstructionBlueprintPrepare')
            elseif message == 'blueprint' then
                AddUITriggeredEvent('TM_Empire_Probe', 'BlueprintFixture')
            elseif message == 'trade_candidate' then
                AddUITriggeredEvent('TM_Empire_Probe', 'TradeCandidate')
            elseif message == 'quote_contract' or message == 'quote_ui' or message == 'purchase_fixture' or message == 'purchase_native' then
                compareQuoteUI = message == 'quote_ui' or message == 'purchase_fixture'
                AddUITriggeredEvent('TM_Empire_Probe', message == 'purchase_native' and 'PurchaseNative'
                    or (message == 'purchase_fixture' and 'PurchaseFixture' or 'QuoteContract'))
            elseif message == 'ui_scroll_prepare' or message == 'ui_scroll_read' then
                local current = Helper.getMenu('PlayerInfoMenu')
                if not current or current.mode ~= 'tm_empire_status' or not current.infoTable then
                    respond(nil, 'ui_scroll|unavailable|effects=false')
                else
                    if message == 'ui_scroll_prepare' then current.refreshInfoFrame(27,29) end
                    Helper.addDelayedOneTimeCallbackOnUpdate(function()
                        local page = Helper.getMenu('PlayerInfoMenu')
                        if not page or page.mode ~= 'tm_empire_status' or not page.infoTable then
                            respond(nil, 'ui_scroll|unavailable|effects=false')
                            return
                        end
                        respond(nil, 'ui_scroll|top=' .. tostring(GetTopRow(page.infoTable))
                            .. '|selected=' .. tostring(Helper.currentTableRow[page.infoTable])
                            .. '|frame=' .. tostring(page.infoFrame and page.infoFrame.id))
                    end, true, getElapsedTime() + .5)
                end
            elseif message == 'ui_status' or message == 'ui_empire' or message == 'ui_stats' then
                local mode = ({ui_status='tm_empire_status',ui_empire='empire',ui_stats='stats'})[message]
                local current = Helper.getMenu('PlayerInfoMenu')
                if current and current.infoFrame and current.infoFrame.id then
                    if current.mode ~= mode then current.buttonTogglePlayerInfo(mode) end
                else
                    OpenMenu('PlayerInfoMenu', {0, 0, mode}, nil)
                end
                Helper.addDelayedOneTimeCallbackOnUpdate(function()
                    local current = Helper.getMenu('PlayerInfoMenu')
                    local frame = current and current.infoFrame
                    local body = frame and frame.content and frame.content[2]
                    local props = body and body.properties or {}
                    respond(nil, 'ui|mode=' .. tostring(current and current.mode)
                        .. '|frame=' .. tostring(frame and frame.id)
                        .. '|tables=' .. tostring(frame and #frame.content)
                        .. '|body_rows=' .. tostring(body and body.rows and #body.rows)
                        .. '|body_width=' .. tostring(props.width)
                        .. '|body_x=' .. tostring(props.x)
                        .. '|body_y=' .. tostring(props.y)
                        .. '|body_max_height=' .. tostring(props.maxVisibleHeight))
                end, true, getElapsedTime() + .5)
            elseif message == 'save_current_status|preflight_save_011_absent'
                or message == 'save_station_package|preflight_save_012_absent'
                or message == 'save_boundary_package|preflight_save_013_absent'
                or message == 'save_domain_checkpoint|preflight_save_014_absent'
                or scenarioSlot or cleanShutdownSlot then
                -- Diagnostic client checks the physical folder immediately before
                -- this exact request. The stock ten slots are never selected.
                local ffi = require('ffi')
                local player = ConvertStringToLuaID(tostring(ffi.C.GetPlayerID()))
                local stationPackage = message == 'save_station_package|preflight_save_012_absent'
                local boundaryPackage = message == 'save_boundary_package|preflight_save_013_absent'
                local domainCheckpoint = message == 'save_domain_checkpoint|preflight_save_014_absent'
                local scenarioCheckpoint = scenarioSlot
                local saveCommand = cleanShutdownSlot and 'save_clean_shutdown' or scenarioCheckpoint and 'save_scenario_checkpoint' or domainCheckpoint and 'save_domain_checkpoint' or boundaryPackage and 'save_boundary_package' or stationPackage and 'save_station_package' or 'save_current_status'
                local marker = cleanShutdownSlot and '$tm_empire_clean_shutdown_' .. cleanShutdownSlot or scenarioCheckpoint and (scenarioSlot == 'save_015' and '$tm_empire_scenario_checkpoint_save' or '$tm_empire_scenario_checkpoint_' .. scenarioSlot) or domainCheckpoint and '$tm_empire_domain_checkpoint_save' or boundaryPackage and '$tm_empire_boundary_package_save' or stationPackage and '$tm_empire_station_package_save' or '$tm_empire_current_status_save'
                local slot = cleanShutdownSlot or scenarioCheckpoint and scenarioSlot or domainCheckpoint and 'save_014' or boundaryPackage and 'save_013' or stationPackage and 'save_012' or 'save_011'
                if GetNPCBlackboard(player, marker) then
                    respond(nil, saveCommand .. '|previous_attempt|effects=false')
                else
                    ffi.C.ReloadSaveList()
                    Helper.addDelayedOneTimeCallbackOnUpdate(function()
                        if not ffi.C.IsSaveListLoadingComplete() then
                            respond(nil, saveCommand .. '|list_not_ready|effects=false'); return
                        end
                        local files = {[slot]=true}
                        for _, entry in ipairs(GetSaveList(files)) do
                            if entry.filename == slot then
                                respond(nil, saveCommand .. '|slot_occupied|effects=false'); return
                            end
                        end
                        local projection = GetNPCBlackboard(player, '$tm_empire_projection')
                        if cleanShutdownSlot then
                            if type(projection) ~= 'table' or (projection.active ~= false and projection.active ~= 0) or (projection.has_governor ~= false and projection.has_governor ~= 0) or projection.reason ~= 'Работа управляющего завершена; модуль разобран' then
                                respond(nil, saveCommand .. '|shutdown_not_clean|effects=false'); return
                            end
                        elseif type(projection) ~= 'table' or (projection.active ~= true and projection.active ~= 1) then
                            respond(nil, saveCommand .. '|governor_not_active|effects=false'); return
                        end
                        if GetNPCBlackboard(player, marker) then
                            respond(nil, saveCommand .. '|previous_attempt|effects=false'); return
                        end
                        SetNPCBlackboard(player, marker, {slot=slot, state='requested'})
                        SaveGame(slot, cleanShutdownSlot and 'TM Empire clean shutdown' or scenarioCheckpoint and 'TM Empire scenario checkpoint' or domainCheckpoint and 'TM Empire domain checkpoint' or boundaryPackage and 'TM Empire boundary package' or stationPackage and 'TM Empire station package' or 'TM Empire current station status')
                        local current = Helper.getMenu('PlayerInfoMenu')
                        if current and current.infoFrame and current.infoFrame.id then current.closeMenu('close') end
                        respond(nil, saveCommand .. '|requested|slot=' .. slot .. '|overwrite=false')
                    end, true, getElapsedTime() + .5)
                end
            elseif message == 'save_current_status' or message == 'save_station_package' or message == 'save_boundary_package' or message == 'save_validation'
                or message == 'save_scenario_checkpoint' or message == 'save_clean_shutdown' or message == 'save_domain_checkpoint' or message == 'save_checkpoint' or message == 'save_remote_personnel' then
                respond(nil, message .. '|preflight_required|effects=false')
            elseif message == 'save_fixture' then
                respond(nil, 'save_fixture|retired|reason=unsafe_fixed_slot|effects=false')
            else
                respond(nil, 'rejected|unsupported')
            end
        end, false)
    end)
end
local function init()
    RegisterEvent('TM_Empire_Probe.Result', respond)
    RegisterEvent('TM_Empire_Probe.BlueprintFixture', function()
        local ffi = require('ffi')
        local player = ConvertStringToLuaID(tostring(ffi.C.GetPlayerID()))
        local data = GetNPCBlackboard(player, '$tm_empire_blueprint_probe')
        local prior = GetNPCBlackboard(player, '$tm_empire_blueprint_submission')
        if type(prior)=='table' then
            respond(nil, 'blueprint_fixture|previous=' .. tostring(prior.state) .. '|repeated=false'); return
        end
        if type(data)~='table' or type(data.representative)~='userdata'
            or data.ware~='tm_module_empire_control_arg' then
            respond(nil, 'blueprint_fixture|invalid_request'); return
        end
        OpenMenu('BlueprintOrLicenceTraderMenu', {0, 0, data.representative, 'blueprint'}, nil)
        Helper.addDelayedOneTimeCallbackOnUpdate(function()
            local trader = Helper.getMenu('BlueprintOrLicenceTraderMenu')
            local ware = data.ware
            if not trader or trader.mode~='blueprint' or trader.trader~=ConvertIDTo64Bit(data.representative) then
                respond(nil, 'blueprint_fixture|native_menu_unavailable'); return
            end
            if trader.blueprintlist[ware] then
                respond(nil, 'blueprint_fixture|already_owned|payment_called=false'); return
            end
            local price = trader.table_wares.module and trader.table_wares.module[ware]
            local licence = GetWareData(ware, 'tradelicence')
            if licence and not HasLicence('player', licence, trader.traderfaction) then
                local entry=GetLibraryEntry('licences', trader.traderfaction .. '.' .. licence)
                local precursor=type(entry)=='table' and entry.precursor or nil
                local minimum=type(entry)=='table' and entry.minrelation or nil
                respond(nil, 'blueprint_fixture|licence_missing|licence=' .. tostring(licence)
                    .. '|faction=' .. tostring(trader.traderfaction)
                    .. '|precursor=' .. tostring(precursor)
                    .. '|precursor_owned=' .. tostring(precursor and HasLicence('player', precursor, trader.traderfaction) or false)
                    .. '|relation=' .. tostring(GetUIRelation(trader.traderfaction))
                    .. '|minrelation=' .. tostring(minimum) .. '|payment_called=false'); return
            end
            if type(price)~='number' or price<=0 or not HasLicence('player', licence, trader.traderfaction)
                or GetPlayerMoney()<price or trader.totalprice~=0 then
                respond(nil, 'blueprint_fixture|native_purchase_conditions_missing|price=' .. tostring(price)); return
            end
            local before = GetPlayerMoney()
            SetNPCBlackboard(player, '$tm_empire_blueprint_submission', {state='unknown', ware=ware, price=price, before=before})
            trader.buttonSelectBlueprint(ware, price)
            if trader.totalprice~=price or not trader.blueprintstopurchase[ware] then
                respond(nil, 'blueprint_fixture|native_selection_unconfirmed'); return
            end
            trader.buttonConfirm()
            local after = GetPlayerMoney()
            local owned = false
            local count = ffi.C.GetNumBlueprints('', '', '')
            local entries = ffi.new('UIBlueprint[?]', count)
            count = ffi.C.GetBlueprints(entries, count, '', '', '')
            for i=0,count-1 do if ffi.string(entries[i].ware)==ware then owned=true; break end end
            local state = owned and before-after==price and 'observed' or 'unknown'
            SetNPCBlackboard(player, '$tm_empire_blueprint_submission', {state=state, ware=ware, price=price, before=before, after=after, owned=owned})
            respond(nil, 'blueprint_fixture|state=' .. state .. '|price=' .. tostring(price)
                .. '|before=' .. tostring(before) .. '|after=' .. tostring(after) .. '|owned=' .. tostring(owned))
        end, false, getElapsedTime() + .2)
    end)
    RegisterEvent('TM_Empire_Probe.QuoteContract', function()
        local ffi = require('ffi')
        local data = GetNPCBlackboard(ConvertStringToLuaID(tostring(ffi.C.GetPlayerID())), '$tm_empire_quote_probe')
        if type(data) ~= 'table' or not data.shipyard then
            respond(nil, 'quote_contract|candidate=none|purchase_called=false')
            return
        end
        local quote = require('extensions.tm_empire_management.ui.purchase_quote')
        local result, reason, detail = quote.generate(data.shipyard, data.macro, .5)
        local plan
        if result then
            plan, reason, detail = quote.to_plan(data.shipyard, result)
            if not plan then
                respond(nil, 'quote_contract|reason=' .. tostring(reason) .. '|detail=' .. tostring(detail))
                return
            end
        end
        if result and (data.native == true or data.native == 1) then
            local ok, answer = pcall(function()
                require('extensions.tm_empire_management.ui.purchase_receipt')
                local player = ConvertStringToLuaID(tostring(ffi.C.GetPlayerID()))
                local price = assert(quote.reprice(data.shipyard, result))
                assert(price.price > 0 and price.paid <= 2000000 and price.crewprice == 0, 'fixture_budget_invalid')
                assert(GetPlayerMoney() >= price.paid, 'fixture_money_insufficient')
                local yard = ConvertIDTo64Bit(data.shipyard)
                local additional = ffi.new('AddBuildTask6Container')
                local create, record = ffi.C.AddBuildTask6, ffi.C.SetBuildTaskTransferredMoney
                return Helper.callLoadoutFunction(plan, nil, function(loadout, crewtransfer)
                    assert(tonumber(loadout.numsoftware) == tonumber(result.loadout.numsoftware), 'software_roundtrip_mismatch')
                    local before = GetPlayerMoney()
                    local receipt = {state='payment_sent', price=price.price, paid=price.paid, macro=data.macro, shipyard=data.shipyard}
                    SetNPCBlackboard(player, '$tm_empire_native_receipt', receipt)
                    TransferPlayerMoneyTo(price.paid, yard)
                    assert(before - GetPlayerMoney() == price.paid, 'fixture_payment_unknown')
                    local id = create(yard, 0, data.macro, loadout, price.price, crewtransfer, false, '', additional)
                    assert(id ~= 0, 'fixture_build_unknown_after_payment')
                    local info = ffi.C.GetBuildTaskInfo(id)
                    assert(info.id == id and info.buildingcontainer == yard and tonumber(info.price) == price.price
                        and ffi.string(info.factionid) == 'player' and ffi.string(info.macro) == data.macro, 'fixture_build_identity_unknown')
                    record(id, price.paid)
                    receipt.id=tostring(id); receipt.state='built'; receipt.matched=false
                    SetNPCBlackboard(player, '$tm_empire_native_receipt', receipt)
                    return 'purchase_native|id=' .. receipt.id .. '|price=' .. price.price
                        .. '|money_before=' .. before .. '|money_after=' .. GetPlayerMoney() .. '|menu_opened=false'
                end, nil, 'UILoadout2')
            end)
            respond(nil, ok and answer or ('purchase_native|error=' .. tostring(answer)))
            return
        end
        if result and compareQuoteUI then
            compareQuoteUI = false
            -- Render the ordinary purchase screen and price the SAME payload.
            -- No shopping-list confirmation, payment or build task is called.
            OpenMenu('ShipConfigurationMenu', {0, 0, data.shipyard, 'purchase', {}}, nil)
            Helper.addDelayedOneTimeCallbackOnUpdate(function()
                local ok, answer = pcall(function()
                    local configuration = Helper.getMenu('ShipConfigurationMenu')
                    assert(configuration and configuration.mode == 'purchase'
                        and configuration.container == ConvertIDTo64Bit(data.shipyard), 'native_purchase_menu_missing')
                    configuration.dropdownShipClass(nil, 'ship_s')
                    configuration.dropdownShip(nil, data.macro)
                    configuration.getDataAndDisplay(plan, nil)
                    local initialprice = result.price
                    result = assert(quote.reprice(data.shipyard, result))
                    if data.purchase == true or data.purchase == 1 then
                        assert(result.price == math.floor(configuration.total) and result.crewprice == 0 and configuration.crewtotal == 0, 'fixture_price_changed')
                        assert(result.price > 0 and result.price <= 2000000 and GetPlayerMoney() >= result.paid, 'fixture_budget_invalid')
                        assert(#configuration.shoppinglist == 0 and not configuration.editingshoppinglist, 'fixture_shoppinglist_not_empty')
                        local before = GetPlayerMoney()
                        configuration.buttonAddPurchase(true, false)
                        assert(#configuration.shoppinglist == 1 and configuration.shoppinglist[1].amount == 1, 'fixture_order_count_invalid')
                        configuration.buttonConfirm()
                        return 'purchase_fixture|native_confirm_called=true|price=' .. result.price .. '|money_before=' .. before .. '|money_after=' .. GetPlayerMoney()
                    end
                    local answer = 'quote_ui|price=' .. result.price .. '|native_price=' .. tostring(configuration.total)
                        .. '|matches=' .. tostring(result.price == math.floor(configuration.total))
                        .. '|crewprice=' .. result.crewprice .. '|native_crewprice=' .. tostring(configuration.crewtotal)
                        .. '|initial_price=' .. initialprice .. '|purchase_called=false'
                    if result.price ~= math.floor(configuration.total) then
                        local removed, current, added, repaired = {}, {}, {}, {}
                        configuration.checkEquipment(removed, current, added, repaired)
                        answer = answer .. '\nquote_raw|' .. string.format('%.17g', result.rawprice)
                        local hull = tonumber(ffi.C.GetBuildWarePrice(configuration.container, GetMacroData(data.macro, 'ware')))
                        answer = answer .. '\nnative_hull|' .. hull
                        for _, item in ipairs(result.price_parts) do
                            answer = answer .. '\nquote_part|' .. item.ware .. '|' .. item.amount .. '|'
                                .. string.format('%.17g', item.price) .. '|' .. item.kind
                        end
                        for kind, groups in pairs({native_added=added,native_removed=removed}) do
                            for _, group in pairs(groups) do
                                for _, item in ipairs(group) do
                                    answer = answer .. '\n' .. kind .. '|' .. item.ware .. '|' .. item.amount
                                        .. '|' .. string.format('%.17g', item.price)
                                end
                            end
                        end
                    end
                    return answer
                end)
                respond(nil, ok and answer or ('quote_ui|error=' .. tostring(answer)))
            end, true, getElapsedTime() + .5)
            return
        end
        local roundtrip
        if result then
            local ok, nativecounts = pcall(function()
                return Helper.callLoadoutFunction(plan, nil, function(loadout, crewtransfer)
                    assert(tonumber(loadout.numsoftware) == tonumber(result.loadout.numsoftware), 'software_roundtrip_mismatch')
                    return '|roundtrip=true|software=' .. tonumber(loadout.numsoftware)
                        .. '|engines=' .. tonumber(loadout.numengines) .. '|crew=' .. tonumber(loadout.numcrew)
                end, nil, 'UILoadout2')
            end)
            if not ok then respond(nil, 'quote_contract|roundtrip_error=' .. tostring(nativecounts)); return end
            roundtrip = nativecounts
        end
        respond(nil, result and ('quote_contract|price=' .. result.price
            .. '|crewprice=' .. result.crewprice .. '|crewcount=' .. result.crewcount
            .. roundtrip .. '|purchase_called=false') or ('quote_contract|reason=' .. tostring(reason) .. '|detail=' .. tostring(detail)))
    end)
    RegisterEvent('TM_Empire_Probe.MatchNativeBuild', function()
        local ffi = require('ffi')
        local player = ConvertStringToLuaID(tostring(ffi.C.GetPlayerID()))
        local receipt = GetNPCBlackboard(player, '$tm_empire_native_receipt')
        local candidate = GetNPCBlackboard(player, '$tm_empire_native_candidate')
        if type(receipt) ~= 'table' or receipt.state ~= 'built' or type(candidate) ~= 'table'
            or type(candidate.build) ~= 'userdata' or type(candidate.shipyard) ~= 'userdata' then return end
        local purchase = require('extensions.tm_empire_management.ui.purchase_submit')
        local matched, reason, actualid = purchase.match(receipt, candidate)
        receipt.candidateid=actualid
        if not matched then
            receipt.match_reason=reason
            SetNPCBlackboard(player, '$tm_empire_native_receipt', receipt)
            return
        end
        receipt.matched=true
        SetNPCBlackboard(player, '$tm_empire_native_receipt', receipt)
        AddUITriggeredEvent('TM_Empire_Probe', 'NativeBuildMatched')
    end)
    RegisterEvent('TM_Empire_Probe.BuildContract', function()
        local receipt = require('extensions.tm_empire_management.ui.purchase_receipt')
        local ffi = require('ffi')
        local data = GetNPCBlackboard(ConvertStringToLuaID(tostring(ffi.C.GetPlayerID())), '$tm_empire_build_probe')
        if type(data) == 'table' and data.state == 'ready' and type(data.ship) == 'userdata' then
            local owned, macro = GetComponentData(data.ship, 'isplayerowned', 'macro')
            respond(nil, 'build_contract|state=ready|tracking=' .. tostring(data.tracking)
                .. '|ship_type=' .. type(data.ship) .. '|playerowned=' .. tostring(owned)
                .. '|operational=' .. tostring(ffi.C.IsComponentOperational(ConvertIDTo64Bit(data.ship)))
                .. '|macro=' .. tostring(macro) .. '|paid=' .. tostring(data.paid)
                .. '|reason=' .. tostring(data.reason) .. '|native_match=' .. tostring(data.native_match) .. '|payment_called=false')
            return
        end
        if type(data) ~= 'table' or not data.build then
            respond(nil, 'build_contract|candidate=none|payment_called=false')
            return
        end
        local ok, result = pcall(function()
            local id = ConvertIDTo64Bit(data.build)
            local info = ffi.C.GetBuildTaskInfo(id)
            return 'build_contract|userdata=' .. type(data.build) .. '|id=' .. tostring(info.id)
                .. '|component=' .. tostring(info.component) .. '|macro=' .. ffi.string(info.macro)
                .. '|identity=' .. tostring(info.id == id and info.id ~= 0)
                .. '|container=' .. tostring(info.buildingcontainer == ConvertIDTo64Bit(data.shipyard))
                .. '|tracking=' .. tostring(data.tracking) .. '|state=' .. tostring(data.state)
                .. '|native_match=' .. tostring(data.native_match)
                .. '|price=' .. tostring(tonumber(info.price)) .. '|ready_ship=' .. tostring(data.ship ~= nil)
                .. '|paid=' .. tostring(data.paid) .. '|reason=' .. tostring(data.reason)
                .. '|missing_resources=' .. tostring(info.ismissingresources) .. '|queue=' .. tostring(tonumber(info.queueposition))
                .. '|payment_called=false'
        end)
        respond(nil, ok and result or ('build_contract|error=' .. tostring(result)))
    end)
    RegisterEvent('TM_Empire_Probe.CrewServiceCandidateReady', function()
        local ffi = require('ffi')
        pcall(ffi.cdef, 'bool CanContainerEquipShip(UniverseID containerid, UniverseID shipid);')
        pcall(ffi.cdef, 'uint32_t GetLoadoutCounts2(UILoadoutCounts2* result, UniverseID defensibleid, const char* macroname, const char* loadoutid);')
        pcall(ffi.cdef, 'void GetLoadout2(UILoadout2* result, UniverseID defensibleid, const char* macroname, const char* loadoutid);')
        pcall(ffi.cdef, 'void GetCurrentLoadout(UILoadout* result, UniverseID defensibleid, UniverseID moduleid);')
        pcall(ffi.cdef, 'void GetCurrentLoadoutCounts(UILoadoutCounts* result, UniverseID defensibleid, UniverseID moduleid);')
        local owner = ConvertStringToLuaID(tostring(ffi.C.GetPlayerID()))
        local fixture = GetNPCBlackboard(owner, '$tm_empire_crew_service_probe')
        local ships = type(fixture) == 'table' and fixture.ships or {}
        local yards = type(fixture) == 'table' and fixture.yards or {}
        local checked = 0
        for _, ship in ipairs(ships) do
            for _, yard in ipairs(yards) do
                checked = checked + 1
                local ok, result = pcall(function()
                    local shipid, yardid = ConvertIDTo64Bit(ship), ConvertIDTo64Bit(yard)
                    if not ffi.C.CanContainerEquipShip(yardid, shipid) then return nil end
                    local macro = GetComponentData(ship, 'macro') or ''
                    local function counts(label, component, candidateMacro, loadoutid)
                        local loadout = Helper.getLoadoutHelper2(ffi.C.GetLoadout2, ffi.C.GetLoadoutCounts2,
                            'UILoadout2', component, candidateMacro, loadoutid)
                        local value = label .. ':' .. tonumber(loadout.numengines) .. '/'
                            .. tonumber(loadout.numweapons) .. '/' .. tonumber(loadout.numsoftware)
                        Helper.ffiClearNewHelper()
                        return value
                    end
                    local answer = 'crew_service_preflight|ship=' .. tostring(ship)
                        .. '|yard=' .. tostring(yard) .. '|checked=' .. checked
                        .. '|macro=' .. macro
                        .. '|loadouts=' .. counts('blank', shipid, '', '')
                        .. ',' .. counts('macro', shipid, macro, '')
                        .. ',' .. counts('current', shipid, macro, 'current')
                        .. '|actual=' .. (function()
                            local current = Helper.getLoadoutHelper(ffi.C.GetCurrentLoadout,
                                ffi.C.GetCurrentLoadoutCounts, shipid, 0)
                            local value = tonumber(current.numengines) .. '/'
                                .. tonumber(current.numweapons) .. '/' .. tonumber(current.numsoftware)
                            Helper.ffiClearNewHelper()
                            return value
                        end)()
                        .. '|payment_called=false'
                    return answer
                end)
                if ok and result then respond(nil, result); return end
                if not ok then respond(nil, 'crew_service_preflight|error=' .. tostring(result)); return end
            end
        end
        respond(nil, 'crew_service_preflight|ships=' .. #ships .. '|yards=' .. #yards
            .. '|checked=' .. checked .. '|compatible=false|payment_called=false')
    end)
    arm()
end
Register_Require_With_Init('extensions.tm_empire_diagnostics.ui.role_probe', {}, init)

