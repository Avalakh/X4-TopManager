-- UI является только читателем bounded MD-проекции.
local ffi = require('ffi')
ffi.cdef[[typedef unsigned long long UniverseID; UniverseID GetPlayerID(void);]]
local MODE = 'tm_empire_status'
local menu
local sidebarVisible = false
local M = {}
local states = {planned=true, sent=true, observed=true, unknown=true, waiting=true, excluded=true}
local inventoryTypes = {'station','ship_s','ship_m','ship_l','ship_xl','other'}
local inventoryStates = {'waiting','sent','unknown','excluded'}

local function text(value, limit)
    return type(value) == 'string' and #value <= (limit or 1024) and value or nil
end

function M.validate(data)
    if type(data) ~= 'table' or data.schema ~= 1 or type(data.has_governor) ~= 'boolean'
       or type(data.active) ~= 'boolean' then return nil end
    if not data.has_governor then
        if data.reason ~= nil and not text(data.reason) then return nil end
        return {has_governor=false, active=false, reason=data.reason}
    end
    if not text(data.governor_name, 256) or not text(data.station_name, 256)
       or not text(data.module_name, 256) or not text(data.reason)
       or type(data.updated) ~= 'number' or data.updated < 0 or data.updated ~= data.updated or data.updated == math.huge
       or type(data.rows) ~= 'table' or #data.rows > 64 then return nil end
    local result = {has_governor=true, active=data.active, governor_name=data.governor_name,
                    station_name=data.station_name, module_name=data.module_name,
                    reason=data.reason, updated=data.updated, rows={}}
    if data.inventory ~= nil then
        local inventory = data.inventory
        local function nonnegative(value)
            return type(value) == 'number' and value == value and value >= 0 and value <= 9007199254740991
        end
        if type(inventory) ~= 'table' or not nonnegative(inventory.from) or not nonnegative(inventory.to)
           or inventory.from > inventory.to or inventory.to > data.updated
           or type(inventory.counts) ~= 'table' or type(inventory.states) ~= 'table' then return nil end
        local totals = {}
        for _, pair in ipairs({{inventory.counts,inventoryTypes},{inventory.states,inventoryStates}}) do
            local total = 0
            for _, key in ipairs(pair[2]) do
                local count = pair[1][key]
                if not nonnegative(count) or count % 1 ~= 0 then return nil end
                total = total + count
            end
            totals[#totals+1] = total
        end
        if not nonnegative(inventory.counts.total) or totals[1] ~= inventory.counts.total
           or totals[1] ~= totals[2] then return nil end
        result.inventory = {from=inventory.from,to=inventory.to,counts={},states={}}
        for _, key in ipairs(inventoryTypes) do result.inventory.counts[key]=inventory.counts[key] end
        result.inventory.counts.total=inventory.counts.total
        for _, key in ipairs(inventoryStates) do result.inventory.states[key]=inventory.states[key] end
    end
    for i, row in ipairs(data.rows) do
        if type(row) ~= 'table' or not text(row.name, 256) or not text(row.reason)
           or not states[row.state] then return nil end
        result.rows[i] = {name=row.name, reason=row.reason, state=row.state}
    end
    if data.tasks ~= nil then
        for _,field in ipairs({'economic_tasks_complete','military_tasks_complete'}) do
          if data[field] ~= nil then
            local complete=data[field]
            if complete==0 then complete=false elseif complete==1 then complete=true end
            if type(complete)~='boolean' then return nil end
            result[field]=complete
          end
        end
        if type(data.tasks) ~= 'table' or #data.tasks > 32 then return nil end
        result.tasks = {}
        -- Military reasons include several status clauses and up to four ship
        -- names. Lua counts UTF-8 bytes; 1024 rejected valid Russian reports.
        for i, task in ipairs(data.tasks) do
            if type(task) ~= 'table' or not text(task.name, 256)
               or not text(task.state, 128) or not text(task.reason, 4096)
               or (task.issued==nil and task.observed==nil) then return nil end
            for _,field in ipairs({'issued','observed'}) do
                local timestamp=task[field]
                if timestamp~=nil and (type(timestamp)~='number' or timestamp~=timestamp
                    or timestamp<0 or timestamp>data.updated) then return nil end
            end
            result.tasks[i] = {name=task.name,state=task.state,reason=task.reason,issued=task.issued,observed=task.observed}
            if task.paid ~= nil then
                if type(task.paid) ~= 'number' or task.paid ~= task.paid or task.paid < 0
                   or task.paid > 90071992547409
                   or math.abs(task.paid*100-math.floor(task.paid*100+0.5)) >= 0.01 then return nil end
                result.tasks[i].paid = task.paid
            end
            for _, key in ipairs({'source','target','person'}) do
                if task[key] ~= nil then
                    if not text(task[key],256) then return nil end
                    result.tasks[i][key] = task[key]
                end
            end
        end
    end
    if data.observations ~= nil then
        if type(data.observations) ~= 'table' or #data.observations > 32 then return nil end
        result.observations = {}
        for i, item in ipairs(data.observations) do
            if type(item) ~= 'table' or not text(item.station,256) or not text(item.employee,256)
               or item.state ~= 'unknown' or not text(item.reason)
               or type(item.observed) ~= 'number' or item.observed ~= item.observed
               or item.observed < 0 or item.observed > data.updated then return nil end
            result.observations[i] = {station=item.station,employee=item.employee,
                reason=item.reason,observed=item.observed,state=item.state}
            if item.workstate ~= nil then
                local states={working=true,needs_attention=true,paused=true,ready=true,unknown=true,missing_manager=true}
                if not states[item.workstate] then return nil end
                result.observations[i].workstate=item.workstate
            end
            if item.subordinates ~= nil then
                local source=item.subordinates
                if type(source)~='table' then return nil end
                local complete=source.complete
                if complete==0 then complete=false elseif complete==1 then complete=true end
                if type(complete)~='boolean' then return nil end
                local summary={complete=complete}
                for _, key in ipairs({'total','observed','operational','controlled'}) do
                    local value=source[key]
                    if type(value)~='number' or value~=value or value<0 or value%1~=0 or value>9007199254740991 then return nil end
                    summary[key]=value
                end
                if summary.observed>32 or summary.observed>summary.total
                   or summary.operational>summary.observed or summary.controlled>summary.observed
                   or (complete and summary.observed~=summary.total) then return nil end
                result.observations[i].subordinates=summary
            end
            if item.utilization~=nil then
                local source=item.utilization
                if type(source)~='table' or not result.observations[i].subordinates then return nil end
                local complete=source.complete
                if complete==0 then complete=false elseif complete==1 then complete=true end
                if type(complete)~='boolean' then return nil end
                local summary={complete=complete}
                for _,key in ipairs({'sampled','busy','idle','cargo_capacity','cargo_used'}) do
                    local value=source[key]
                    if type(value)~='number' or value~=value or value<0 or value%1~=0 or value>9007199254740991 then return nil end
                    summary[key]=value
                end
                local ships=result.observations[i].subordinates
                if summary.sampled>ships.observed or summary.busy+summary.idle~=summary.sampled
                   or summary.cargo_used>summary.cargo_capacity
                   or (complete and (not ships.complete or summary.sampled~=ships.total)) then return nil end
                result.observations[i].utilization=summary
            end
            if item.purpose ~= nil then
                local purposes = {building=true,ship_support=true,production=true,trading=true,other=true}
                if not purposes[item.purpose] then return nil end
                result.observations[i].purpose = item.purpose
            end
            if item.production ~= nil then
                local source = item.production
                if type(source) ~= 'table' then return nil end
                local complete = source.complete
                if complete == 0 then complete = false elseif complete == 1 then complete = true end
                if type(complete) ~= 'boolean' then return nil end
                local production, sum = {complete=complete}, 0
                for _, key in ipairs({'total','producing','resources','storage','manual','paused','other'}) do
                    local value = source[key]
                    if type(value) ~= 'number' or value ~= value or value < 0
                       or value % 1 ~= 0 or value > 9007199254740991 then return nil end
                    production[key] = value
                    if key ~= 'total' then sum = sum + value end
                end
                if sum > 32 or sum > production.total or (complete and sum ~= production.total) then return nil end
                result.observations[i].production = production
            end
            if item.external~=nil then
                local e=item.external
                if type(e)~='table' or type(e.last_attack)~='number'
                   or e.last_attack~=e.last_attack or e.last_attack<0 or e.last_attack>item.observed
                   or (e.attacker~=nil and not text(e.attacker,256)) then return nil end
                result.observations[i].external={last_attack=e.last_attack,attacker=e.attacker}
            end
            if item.trade_restricted ~= nil then
                local restricted = item.trade_restricted
                if restricted == 0 then restricted = false elseif restricted == 1 then restricted = true end
                if type(restricted) ~= 'boolean' then return nil end
                result.observations[i].trade_restricted = restricted
            end
            if item.problems ~= nil or item.problems_complete ~= nil then
                local complete=item.problems_complete
                if complete==0 then complete=false elseif complete==1 then complete=true end
                if type(item.problems)~='table' or #item.problems>32 or type(complete)~='boolean'
                   then return nil end
                result.observations[i].problems={}
                result.observations[i].problems_complete=complete
                for j, problem in ipairs(item.problems) do
                    if type(problem)~='table' or not text(problem.category,256)
                       or not text(problem.ware,256) then return nil end
                    result.observations[i].problems[j]={category=problem.category,ware=problem.ware}
                end
            end
            if item.money ~= nil or item.productionmoney ~= nil then
                for _, key in ipairs({'money','productionmoney'}) do
                    local amount = item[key]
                    if type(amount) ~= 'number' or amount ~= amount or amount < 0
                       or amount > 9007199254740991 then return nil end
                    result.observations[i][key] = amount
                end
            end
            if item.stocks ~= nil or item.stocks_complete ~= nil then
                local complete=item.stocks_complete
                if complete==0 then complete=false elseif complete==1 then complete=true end
                if type(item.stocks)~='table' or #item.stocks>32 or type(complete)~='boolean'
                   then return nil end
                result.observations[i].stocks={}
                result.observations[i].stocks_complete=complete
                for j, stock in ipairs(item.stocks) do
                    if type(stock)~='table' or not text(stock.name,256) then return nil end
                    for _, key in ipairs({'count','capacity'}) do
                        local value=stock[key]
                        if type(value)~='number' or value~=value or value<0
                           or value>9007199254740991 then return nil end
                    end
                    result.observations[i].stocks[j]={name=stock.name,count=stock.count,capacity=stock.capacity}
                end
            end
            if item.provision ~= nil then
                if item.provision ~= 'insufficient_provision' or not text(item.provisionreason)
                   or result.observations[i].trade_restricted == true
                   or not text(item.recommendation)
                   or not item.money or not item.productionmoney
                   or item.productionmoney <= 0 or item.money * 10 > item.productionmoney * 9 then return nil end
                result.observations[i].provision = item.provision
                result.observations[i].provisionreason = item.provisionreason
                result.observations[i].recommendation = item.recommendation
            end
            if item.miningreason ~= nil or item.miningrecommendation ~= nil then
                if not text(item.miningreason) or not text(item.miningrecommendation)
                   then return nil end
                result.observations[i].miningreason = item.miningreason
                result.observations[i].miningrecommendation = item.miningrecommendation
            end
            if item.tradereason ~= nil or item.traderecommendation ~= nil then
                if not text(item.tradereason) or not text(item.traderecommendation) then return nil end
                result.observations[i].tradereason = item.tradereason
                result.observations[i].traderecommendation = item.traderecommendation
            end
        end
    end
    return result
end

local function rawProjection()
    local player = ffi.C.GetPlayerID()
    if player == 0 then return nil end
    local raw = GetNPCBlackboard(ConvertStringToLuaID(tostring(player)), '$tm_empire_projection')
    if type(raw) ~= 'table' then return nil end
    return raw
end

-- Report rows may be unavailable without invalidating the role itself.
function M.hasGovernor()
    local raw = rawProjection()
    return raw ~= nil and raw.schema == 1
        and (raw.has_governor == true or raw.has_governor == 1)
end

function M.snapshot()
    local raw = rawProjection()
    if not raw then return nil end
    -- MD booleans arrive through the native blackboard as 0/1.
    local data = {}
    for key, value in pairs(raw) do data[key] = value end
    for _, key in ipairs({'has_governor', 'active'}) do
        if data[key] == 0 then data[key] = false
        elseif data[key] == 1 then data[key] = true end
    end
    return M.validate(data)
end

function M.sidebar(config)
    local empireIndex
    for i, entry in ipairs(config.leftBar) do
        if entry.mode == MODE then return end
        if entry.mode == 'empire' then empireIndex = i end
    end
    if not empireIndex then return end
    table.insert(config.leftBar, empireIndex + 1, {mode=MODE, icon='tm_empire_status', name='Статус империи',
        active=true, helpOverlayID='tm_empire_status', helpOverlayText='Статус управляющего',
        condition=function()
            sidebarVisible = M.hasGovernor()
            return sidebarVisible
        end})
end

function M.render(frame, properties)
    if menu.mode ~= MODE then return end
    -- Match the native empire page; the callback receives the narrow width
    -- because the game does not recognize our additional mode in its switch.
    local width = properties.width
    if type(menu.playerInfoFullWidth) == 'number' and type(menu.sideBarWidth) == 'number'
        and type(Helper.borderSize) == 'number' then
        width = menu.playerInfoFullWidth - menu.sideBarWidth - Helper.borderSize
    end
    local tableHandle = frame:addTable(3, {
        tabOrder=1, borderEnabled=true, highlightMode='grey',
        width=width, x=properties.x, y=properties.y,
        maxVisibleHeight=properties.height,
    })
    tableHandle:setColWidth(1, width * .32, false)
    tableHandle:setColWidth(2, width * .24, false)
    -- refreshInfoFrame already captures these values from the native widget.
    tableHandle:setTopRow(menu.settoprow)
    tableHandle:setSelectedRow(menu.setselectedrow)
    menu.settoprow = nil
    menu.setselectedrow = nil
    local function row(a, b, c)
        -- Selectable rows let the native widget scroll the long report.
        local handle = tableHandle:addRow(true, {})
        handle[1]:createText(a, {wordwrap=true, mouseOverText=a})
        handle[2]:createText(b or '', {wordwrap=true, mouseOverText=b or ''})
        handle[3]:createText(c or '', {wordwrap=true, mouseOverText=c or ''})
    end
    local data = M.snapshot()
    if not data and M.hasGovernor() then
        row('Отчёт временно недоступен', 'Управляющий назначен',
            'Снимок данных не прошёл проверку; ожидается следующее обновление')
        return
    end
    if not data or not data.has_governor then
        row('Управление остановлено', (data and data.reason) or 'Действующий управляющий отсутствует')
        return
    end
    row('Управляющий', data.governor_name, data.active and 'Действует' or 'Остановлен')
    row('Расположение', data.station_name, data.module_name)
    row('Причина', data.reason, 'Наблюдение: ' .. tostring(data.updated))
    if data.inventory then
        local counts, states = data.inventory.counts, data.inventory.states
        row('Наблюдаемая собственность', 'Всего: ' .. counts.total, 'Станций: ' .. counts.station)
        row('Корабли по размеру', 'S: ' .. counts.ship_s .. ' · M: ' .. counts.ship_m,
            'L: ' .. counts.ship_l .. ' · XL: ' .. counts.ship_xl .. ' · Прочие: ' .. counts.other)
        row('Состояния', 'Ожидают: ' .. states.waiting .. ' · Отправлено: ' .. states.sent,
            'Исключено: ' .. states.excluded .. ' · Неизвестно: ' .. states.unknown)
        row('Период снимка', tostring(data.inventory.from) .. ' — ' .. tostring(data.inventory.to),
            'Показано объектов: ' .. #data.rows .. ' из ' .. counts.total)
    else
        row('Собственность', 'Наблюдения собираются')
    end
    local labels={planned='План',sent='Отправлено',observed='Подтверждено',unknown='Исход неизвестен',
                  waiting='Ожидание',excluded='Исключено',quote_requested='Запрос цены',
                  quote_ready='Цена получена',quoted='Цена получена',approved='Покупка одобрена',
                  checking_blueprints='Проверка чертежей',payment_approved='Оплата одобрена',
                  payment_sent='Проверка оплаты',paid='Оплачено',build_sent='Проверка заказа',
                  build_observed='Заказ подтверждён',build_recorded='Оплата заказа учтена',
                  delivered='Корабль получен',completed='Завершено',consumed='Результат принят',
                  rejected='Отклонено',rejected_before_effect='Отклонено до исполнения',
                  revoked='Отозвано',queued='В очереди строительства',queue_sent='Проверка очереди',
                  validating='Проверка строительного плана',check_requested='Проверка условий'}
    for _, item in ipairs(data.rows) do row(item.name, labels[item.state], item.reason) end
    if data.tasks and #data.tasks > 0 then
        local reasons={
            supply_authority_lost_before_payment='Снабжение отменено до оплаты: полномочия управляющего или его цели прекращены',
            known_supply_builder_unavailable='Поставщик оборудования утрачен, недоступен или больше не известен',
            native_supply_quote_refresh_after_docking='Корабль состыковался; пересчитывается цена снабжения до оплаты',
            supply_previous_payment_intent='Оплата этого снабжения уже отправлялась; результат проверяется без повторного списания',
            supply_inventory_changed='Инвентарь корабля изменился после расчёта снабжения; требуется новый запрос',
            supply_authority_lost_with_payment_intent='Полномочия прекращены после отправки оплаты снабжения; результат проверяется без повторной оплаты',
            native_crew_assignment_pending='Штатное назначение сотрудника в экипаж отправлено; прибытие проверяется',
            military_ship_sample_incomplete='В этом цикле рассмотрена часть боевых кораблей; следующие циклы проверят другие выборки',
            economic_ship_search_incomplete='Продолжается поиск подходящего собственного корабля; отсутствие транспорта ещё не установлено',
            crew_exchange_authorization_changed='Условия перевода экипажа изменились; назначение остановлено до сверки',
            crew_exchange_employee_unavailable='Первоначальный сотрудник больше недоступен для перевода; замена не отправлялась',
            recycling_manager_transfer_pending='Штатный перевод менеджера на перерабатывающую станцию отправлен; прибытие проверяется',
            recycling_manager_transfer_unconfirmed='Назначение менеджера перерабатывающей станции не подтверждено; повтор удерживается',
            native_supply_delivery_observed='Оплаченное снабжение завершено: оборудование на корабле, заказ верфи закончен',
            native_supply_build_in_progress='Оплаченное снабжение выполняется верфью; оборудование и окончание заказа проверяются',
            previous_construction_goal_still_active='Стройкой ещё управляет действующая цель; передача не выполнялась',
            native_supply_build_identity_unconfirmed='Оплата снабжения записана, но исходный заказ не подтверждён; повтор удерживается',
            empty_supply_quote='Список оборудования для расчёта цены пуст; оплата не выполнялась',
            invalid_supply_quote_request='Данные поставщика или оборудования для расчёта цены недоступны',
            native_supply_quote_error='Штатная цена снабжения не получена; оплата не выполнялась',
            native_shortages_evaluated='Штатный цикл рассмотрел дефицит и переполнение; исполнение решений проверяется отдельно',
            native_builder_quote_pending='Проверяются доступность строительного корабля и штатная стоимость найма',
            native_hired_builder_deployment_pending='Строитель нанят; ожидается его прибытие и назначение на стройку',
            native_hired_builder_arrival_observed='Нанятый строитель прибыл и назначен на эту стройку',
            native_hired_builder_arrival_pending='Прибытие нанятого строителя ещё не подтверждено',
            builder_arrival_pending='Строитель направлен на станцию; прибытие проверяется',
            known_idle_builder_unavailable='Среди известных кораблей не найден свободный подходящий строитель',
            builder_budget_missing='Оставшегося строительного бюджета недостаточно для найма',
            builder_destination_lost='Станция или её строительное хранилище недоступны',
            builder_unavailable='Выбранный строитель больше недоступен для найма',
            builder_busy='Строитель уже занят другим поручением',
            builder_order_unavailable='Штатное назначение этого строителя недоступно',
            builder_fee_unavailable='Штатный тариф найма превышает доступные деньги или бюджет',
            builder_fee_changed='Тариф найма изменился; оплата не выполнялась',
            builder_authorization_changed='Условия назначения изменились; разрешение на оплату отозвано',
            native_builder_payment_unconfirmed='Результат оплаты строителя не подтверждён; повтор удерживается',
            native_builder_order_unconfirmed='После оплаты не подтверждён приказ строителю; повтор удерживается',
            native_builder_order_not_enabled='Оплата выполнена, но запуск приказа не подтверждён; повтор удерживается',
            native_builder_hire_unconfirmed='Исход штатного найма строителя неизвестен; повтор удерживается',
            native_builder_recovery_pending='Для оплаченного строителя восстанавливается штатный приказ; повторная оплата удерживается',
            destination_post_transfer_unreconciled='На эту должность уже направлен сотрудник; его прибытие ещё не подтверждено',
            destination_post_hire_unreconciled='Для этой должности уже начат найм; второй сотрудник не назначается',
            hiring_destination_lost='Наём удерживается: цель назначения утрачена или недоступна',
            hire_approval_revoked='Наём отменён до оплаты: изменилось назначение или одобрение',
            hiring_source_changed='Кандидат больше не находится в указанном месте найма',
            native_hiring_fee_changed='Стоимость найма изменилась; требуется новое решение',
            hiring_discounts_unavailable='Штатные условия оплаты найма недоступны',
            invalid_hiring_discount='Штатная скидка на найм не подтверждена; оплата удерживается',
            native_hiring_price_outside_budget='Стоимость найма превышает доступный бюджет',
            insufficient_hiring_money='Недостаточно денег для оплаты найма',
            native_hire_payment_pending='Наём отправлен; проверяется оплата и последующее назначение',
            builder_or_station_lost='Строитель или станция недоступны; результат назначения неизвестен',
            native_construction_in_progress='Штатное строительство выполняется; завершение модулей ещё не подтверждено',
            native_resources_or_processor_pending='Ожидаются строительные ресурсы или начало работы строителя',
            native_expansion_modules_observed='Все модули этого этапа расширения построены и работают',
            construction_authority_reconciled='Новый управляющий продолжает существующий строительный заказ',
            construction_goal_missing_after_queue='Прежнее поручение завершилось; строительный заказ ожидает передачи управляющему',
            construction_handoff_effect_unreconciled='Ожидается подтверждение ранее отправленного действия по этой стройке перед передачей управления',
            previous_construction_goal_still_active='Стройка остаётся закреплена за действующим поручением управляющего',
            construction_handoff_native_queue_changed='Очередь строительства изменилась; передача управления приостановлена',
            construction_handoff_claim_changed='Строительное поручение изменилось; его принадлежность требует проверки',
            construction_handoff_provenance_changed='Происхождение строительного заказа не подтверждено; передача управления приостановлена',
            construction_handoff_payment_evidence_missing='Оплата строительного заказа не подтверждена; повторная оплата удерживается',
            plot_licence_budget_missing='Для покупки лицензии участка недостаточно доступного бюджета или денег',
            plot_station_unavailable='Лицензия участка не оформлена: готовность станции или разрешение на её строительство не подтверждены',
            construction_asset_unavailable='Финансирование удерживается: станция или строительное хранилище недоступны',
            station_production_quote_changed='Перевод удерживается: потребность станции или баланс изменились',
            station_budget_missing='Недостаточно денег для производственного бюджета станции',
            station_funding_revoked='Разрешение на пополнение счёта станции отозвано; перевод не выполнен',
            station_debit_unconfirmed='Списание на рабочий счёт станции не подтверждено; повтор удерживается',
            station_credit_unconfirmed='Зачисление на рабочий счёт станции не подтверждено; повтор удерживается',
            station_funding_effect_unconfirmed='Результат пополнения рабочего счёта неизвестен; повтор удерживается',
            native_construction_debit_unconfirmed='Списание строительного бюджета не подтверждено; повтор удерживается',
            native_construction_credit_unconfirmed='Зачисление строительного бюджета не подтверждено; повтор удерживается',
            construction_asset_or_quote_unavailable='Строительная оценка недоступна: требуется действующая собственная станция и хранилище',
            native_construction_quote_unavailable='Штатная строительная котировка не получена; оплата не отправлялась',
            construction_native_quote_or_budget_changed='Строительная котировка или доступный бюджет изменились; требуется новое решение',
            construction_funding_effect_unconfirmed='Результат финансирования строительства неизвестен; повтор удерживается',
            native_station_plot_licence_pending='Ожидается оформление штатной лицензии строительного участка',
            known_market_input_incomplete='Снимок известных торговых предложений превышает предел обработки; отсутствие поставщиков не предполагается',
            player_helm='Корабль под личным управлением игрока; выбрана другая доступная работа',
            ship_pilot_arrival_required='Для выполнения задачи требуется прибывший капитан; назначение или перевод ещё не подтверждены',
            manual_or_priority_order='Ручной или приоритетный приказ игрока сохранён; автономное действие отложено',
            order_queue_inspection_incomplete='Очередь приказов проверена не полностью; автономное действие отложено',
            order_queue_inspection_unavailable='Очередь приказов сейчас недоступна; автономное действие отложено',
            native_transfer_pending='Назначение отправлено; ожидается фактическое прибытие сотрудника',
            native_post_arrival_observed='Тот же сотрудник прибыл и занял назначенную должность',
            native_arrival_not_observed='Прибытие сотрудника на должность не подтверждено; повторное назначение удерживается',
            transfer_destination_lost='Место назначения утрачено или недоступно; результат перевода требует сверки',
            source_membership_not_reconciled='Сотрудник обнаружен в месте назначения, но ещё числится в исходном составе; перевод не подтверждён',
            native_crew_arrival_observed='Тот же сотрудник прибыл и занял назначенную роль экипажа',
            native_crew_arrival_not_observed='Прибытие экипажа не подтверждено; повторный перевод удерживается',
            native_transport_resumed_arrival_unconfirmed='Штатный транспорт для уже назначенного сотрудника возобновлён; прибытие проверяется',
            build_handle_missing='Связь заказа с готовым кораблём не сохранилась; повторная оплата удерживается',
            typed_build_candidate_missing='Исходный объект строительства не сопоставлен; повторная оплата удерживается',
            native_existing_actions_cover_need='После учёта текущей потребности и уже выбранных действий штатный алгоритм не добавляет новое',
            native_need_below_action_threshold='Потребность ниже штатного порога для нового действия',
            native_no_viable_economic_action='Штатный алгоритм не нашёл допустимого действия при текущих условиях',
            native_seminar_pending='Проверяется расход семинара и изменение навыка',
            native_seminar_consumption_and_skill_observed='Семинар израсходован, повышение навыка подтверждено',
            seminar_consumption_or_skill_unconfirmed='Расход семинара или изменение навыка не подтверждены',
            training_employee_identity_changed='Сотрудник сменился: результат обучения первоначального сотрудника не подтверждён',
            hire_employee_identity_changed='Сотрудник в должности сменился: прибытие оплаченного кандидата не подтверждено',
            transfer_employee_identity_changed='Сотрудник сменился: прибытие первоначального сотрудника не подтверждено',
            required_seminar_missing='Для необходимого обучения нет подходящего семинара',
            native_experience_required_for_combined_skill='Для требуемого навыка нужен штатный опыт работы',
            required_control_posts_present='Необходимые должности заняты; потребность в обучении не обнаружена',
            no_available_employee_in_current_batch='В проверенной группе нет подходящего свободного сотрудника',
            crew_exchange_revoked_before_effect='Перемещение экипажа отменено до отправки: разрешение управляющего или его цели отозвано',
            paid_hire_governor_changed='После оплаты управляющий или его модуль изменился; назначение остановлено до сверки',
            paid_hire_goal_unavailable='После оплаты кадровая задача недоступна; назначение ожидает сверки',
            hire_approval_revoked_before_payment='Наём отменён до отправки оплаты; сотрудник не назначался',
            no_owned_personnel_targets='Нет собственных объектов для кадровой задачи',
            personnel_target_lost='Кадровая цель больше недоступна',
            native_transfer_pending='Перевод сотрудника отправлен; ожидается прибытие',
            player_helm='Корабль под личным управлением игрока',
            previous_training_unreconciled='Предыдущее обучение ещё не согласовано с игровым результатом',
            training_person_busy='Сотрудник занят или участвует в другой задаче',
            training_person_in_transfer='Сотрудник ещё находится в переводе',
            training_person_unavailable='Сотрудник для обучения недоступен',
            required_skill_already_observed='Требуемый навык уже достигнут'}
        row('Поручения управляющего', 'Состояние', 'Причина / результат')
        if data.economic_tasks_complete==false then
            row('Показана часть экономических действий','','Остальные действия не оценены в этом снимке')
        end
        if data.military_tasks_complete==false then
            row('Показана часть военных целей','','Остальные цели не оценены в этом снимке')
        end
        for _, task in ipairs(data.tasks) do
            row(task.name, labels[task.state] or task.state, reasons[task.reason] or task.reason)
            if task.paid ~= nil then
                row('Подтверждённая оплата', tostring(task.paid) .. ' Cr',
                    task.observed and ('Время наблюдения: ' .. task.observed)
                        or 'Оплата подтверждена; назначение и прибытие проверяются отдельно')
            end
            if task.source or task.target or task.person then
                row('Участники поручения', task.person or '',
                    (task.source and 'Откуда: ' .. task.source or '')
                    .. (task.source and task.target and '; ' or '')
                    .. (task.target and 'Куда / объект: ' .. task.target or ''))
            end
        end
    end
    if data.observations and #data.observations > 0 then
        row('Наблюдения станций', 'Менеджер', 'Проблемы / время наблюдения')
        if data.inventory and data.inventory.counts.station > #data.observations then
            row('Показана часть станций', tostring(#data.observations) .. ' из ' .. tostring(data.inventory.counts.station),
                'Статусы собираются порциями; остальные станции появятся в следующих снимках')
        end
        for _, item in ipairs(data.observations) do
            row(item.station,item.employee,item.reason .. ' · ' .. tostring(item.observed))
            local states={working='Производство работает',needs_attention='Есть потребность / препятствие',paused='Производство приостановлено',ready='Штатный отчёт без выявленных проблем',unknown='Состояние ещё не подтверждено',missing_manager='Нужен менеджер станции'}
            row('Текущий статус',states[item.workstate or 'unknown'],item.reason)
            if item.purpose then
                local purposes = {building='Строительство',ship_support='Строительство / оснащение кораблей',
                    production='Производство',trading='Торговая станция',other='Иное назначение'}
                row('Назначение станции', purposes[item.purpose],
                    'Текущее штатное назначение станции')
            end
            if item.production then
                local p = item.production
                row('Производственные модули', 'Работает: ' .. p.producing .. ' из ' .. p.total,
                    p.complete and 'Текущее состояние всех модулей; длительность простоев не измерена'
                    or 'Неполный снимок; остальные модули не оценены')
                row('Ожидание производства', 'Ресурсы: ' .. p.resources .. '; склад: ' .. p.storage,
                    'Ручная пауза: ' .. p.manual .. '; другая пауза: ' .. p.paused .. '; прочее: ' .. p.other)
            end
            if item.subordinates then
                local s=item.subordinates
                row('Подчинённые станции', 'Кораблей: ' .. s.total .. '; исправных: ' .. s.operational,
                    'Проверено: ' .. s.observed .. '; под управлением игрока: ' .. s.controlled
                    .. (s.complete and '. Полный снимок; производительность ещё не измерена' or '. Неполный снимок; остальные корабли не оценены'))
            end
            if item.utilization then
                local u=item.utilization
                row('Работа подчинённых', 'С приказами: ' .. u.busy .. '; ожидают: ' .. u.idle,
                    'Проверено: ' .. u.sampled .. '; груз: ' .. u.cargo_used .. '/' .. u.cargo_capacity .. ' м³'
                    .. (u.complete and '. Полный снимок' or '. Неполный снимок')
                    .. '')
            end
            if item.money then
                row('Производственный счёт', tostring(item.money) .. ' Cr',
                    'Расчётная потребность: ' .. tostring(item.productionmoney) .. ' Cr')
            end
            if item.external then
                row('Внешнее воздействие', 'Последняя атака: ' .. item.external.last_attack,
                    'Нападавший: ' .. (item.external.attacker or 'неизвестен')
                    .. '. Факт атаки зарегистрирован игрой; длительность угрозы и влияние на результат требуют отдельных наблюдений')
            end
            if item.trade_restricted ~= nil then
                row('Торговля станции', item.trade_restricted and 'Только со своей фракцией' or 'Разрешена с другими фракциями',
                    item.trade_restricted and 'Штатное глобальное ограничение. Низкий счёт сам по себе не доказывает нехватку снабжения; доступность внутренних поставок ещё не оценена'
                    or 'Остальные торговые правила и доступность поставщиков ещё не оценены')
            end
            if item.stocks then
                row('Запасы ресурсов и продукции', 'Количество / вместимость',
                    item.stocks_complete and 'Полный снимок выбранных товаров' or 'Неполный снимок; остальные товары не оценены')
                for _, stock in ipairs(item.stocks) do
                    row(stock.name, tostring(stock.count), tostring(stock.capacity))
                end
            end
            if item.provision then
                -- Provision remains independent of the purpose-specific result.
                row('Недостаток обеспечения', 'Производственный бюджет', item.provisionreason)
                row('Рекомендация', '', item.recommendation)
            end
            if item.miningreason then
                row('Недостаток обеспечения', 'Добывающие корабли', item.miningreason)
                row('Рекомендация', '', item.miningrecommendation)
            end
            if item.tradereason then
                row('Недостаток обеспечения', 'Торговые корабли', item.tradereason)
                row('Рекомендация', '', item.traderecommendation)
            end
            if item.problems and #item.problems>0 then
                row('Штатный экономический отчёт', 'Товар',
                    item.problems_complete and 'Полный перечень проблем отчёта' or 'Перечень обрезан; остальные товары не оценены')
                for _, problem in ipairs(item.problems) do
                    row(problem.category,problem.ware,'Текущая потребность станции')
                end
            end
        end
    end
end

function M.init()
    menu = Helper.getMenu('PlayerInfoMenu')
    if not menu or type(menu.registerCallback) ~= 'function' then
        DebugError('TM_Empire: отсутствует проверенный PlayerInfoMenu UI-hook')
        return
    end
    -- Новый createLeftBar_on_start в установленном UIX содержит ошибку ccreate...
    menu.registerCallback('createPlayerInfo_on_start', M.sidebar, 'tm_empire_sidebar')
    menu.registerCallback('createInfoFrame_on_info_frame_mode', M.render, 'tm_empire_status')
    RegisterEvent('TM_Empire.StatusUpdated', function()
        local visible = M.hasGovernor()
        local changed = visible ~= sidebarVisible
        sidebarVisible = visible
        -- The left bar belongs to mainFrame; refreshInfoFrame only rebuilds
        -- the page body. Late MD data must refresh the native main frame once.
        if changed and menu.mainFrame and menu.mainFrame.id
            and type(menu.createMainFrame)=='function' then
            menu.createMainFrame()
        end
        if menu.mode == MODE and menu.infoFrame and menu.infoFrame.id then
            menu.refresh = getElapsedTime() + .1
        end
    end)
end

Register_Require_With_Init('extensions.tm_empire_management.ui.empire_status', M, M.init)
