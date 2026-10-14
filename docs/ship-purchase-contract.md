# Граница штатной покупки корабля

Исходники текущей игры, оригиналы не изменяются:

- `ui/addons/ego_detailmonitor/menu_ship_configuration.lua`, buttonConfirm,
  строки 1800–1812: проверка бюджета всей корзины и TransferPlayerMoneyTo
  для чужого shipyard до создания build task.
- Тот же файл, строки 11444–11455: Helper.callLoadoutFunction создаёт обычный
  UILoadout2/crewtransfer, AddBuildTask6 возвращает BuildTaskID; после
  успешного создания SetBuildTaskTransferredMoney записывает сумму оплаты.
- `libraries/common.xsd`, add_build_to_construct_ship: price задаёт цену
  объекта; документация не утверждает, что действие списывает деньги.
- `aiscripts/build.shiptrader.xml`, строки 684–731: missingpayment и
  transfer_money относятся к ветке equip/upgrade/repair, их нельзя
  переносить как доказательство автоматической оплаты нового корабля.
- `libraries/scriptproperties.xml`, datatype build: price и
  transferredamount — разные наблюдения; base/construction/buildobject
  связывают заказ с реальным строящимся объектом.

Следствие: замена NPC price=0Cr на ShipCostTable без подтверждённого
платежа не удовлетворяет требованию покупки игрока. Также waiting job
ships из Job_Helper нельзя использовать как бесплатные player ships.

Минимальный адаптер должен использовать штатный price/loadout/build путь,
не переписывать алгоритм выбора shipyard по доступности, цене и расстоянию.
Если необходим Lua вызов AddBuildTask6/SetBuildTaskTransferredMoney, это
внутриигровой адаптер фиксированной покупки, а не внешний исполнитель.
Транспорт диагностики и внешний Python в покупке не участвуют.

Перед эффектом: Registry lifecycle; актуальные права/репутация/доступность
shipyard, macro/loadout; точная стоимость; claim денег/потребности. Оплата
должна подтверждаться фактической суммой. Sent записывается до отправки;
неизвестный исход сохраняет claim и не вызывает вторую оплату/покупку.
Недостаточная сумма не выдаётся за успешную оплату. Ошибка после оплаты
требует согласования и штатного возврата, а не молчаливого повторения.

Обычная собственная верфь в штатном UI имеет денежную цену заказа 0, но
использует обычные ресурсы/очередь. Это отличается от NPC бесплатного
заказа на чужой верфи; расходы на материалы и personnel остаются реальными.
Нельзя ни требовать лишнюю оплату самому себе, ни обходить ресурсы.

Queued/paid/inprogress не означают ready. Готовность подтверждается
штатным build/ship read-back с фактической собственностью, operational и
связью заказа с нужным кораблём; задача/назначение после покупки отдельно.

Статус: контракт источников найден; платёжный адаптер и его игровая
проверка не реализованы. Задача 3.5 остаётся открытой.

Подготовлен read-only `TM_Empire_Purchase.ReadBuild`: проверяет native build
handle/type/cancelled, shipyard/faction/macro/price и transferredamount.
Возвращает queued/building/ready, cancelled или unknown с причиной.
Ready требует связанного build.construction, фактической ownership,
macro и operational. Отсутствующий handle не считается завершением.
Это чтение очереди ещё не подключено к платёжному адаптеру; после удаления
готового build необходимо сохранить подтверждённую связь с ship из штатного
события, а не повторно создавать заказ. XSD проходит; игровая проверка
этой библиотеки пока отсутствует.

Подготовлен `ui/purchase_receipt.lua`, узкая запись уже переведённой суммы:
читает собственный player blackboard `$tm_empire_purchase`, принимает
только native userdata build/shipyard и фиксированную стадию payment_sent.
GetBuildTaskInfo сверяет ID/верфь/фракцию/macro/цену перед
SetBuildTaskTransferredMoney. При несовпадении эффект не вызывается.
Источник структуры BuildTaskInfo и сигнатур — штатный ship configuration UI.
Fixture на Lua 5.1 текущей игры проверяет отказы по чужой фракции/верфи,
несовпадению цены/платежа, недействительному handle, сырым числовым IDs,
неподходящей стадии и NaN; это не проверка ABI или передачи userdata в игре.

Адаптер включён в ui.xml, но не вызывается production MD: требуется
адресная проверка передачи BuildTask через blackboard, MD платёж/claim,
read-back transferredamount и обработка неудачи после оплаты. Для own
shipyard запись положительной оплаты не нужна; обычные ресурсы обязательны.
Задача 3.5 по-прежнему не закрыта.

load-20/build-contract-02: регистрация purchase_receipt исправлена после
ошибки require в build-contract-01; модуль загружается в игре. В сохранении
нет подходящего native build, поэтому userdata/ABI конкретного заказа ещё
не квалифицированы; платёж не вызывался.

Штатная цена AddBuildTask6 исключает экипаж, а transferredamount включает
price + crewprice. Receipt и ReadBuild теперь проверяют эти величины отдельно.
Fixture покрывает оба случая, включая несогласованную сумму и отрицательный
расход экипажа. Наличие оплаченного заказа по-прежнему не означает ready.

purchase_quote использует штатные GenerateShipLoadout2/Counts2 и
Helper.getLoadoutHelper2: полный native payload сохраняется без собственного
подбора оборудования и без потери software. Цена оборудования берётся из
GetBuildWarePrice, software — из обычной цены верфи с её factor и discounts,
crew — из штатной формулы workforce/hiringdiscounts. Своя верфь сохраняет
денежную цену 0 и обычный ресурсный build. Адаптер не создаёт build, не платит,
не устанавливает чёрные списки/приказы и не является вторым планировщиком.
Проверка counts предшествует выделению массивов; неизвестные цены/workforce
не заменяются нулём. Его текущая граница — station shipyard, не ship resupplier.
Fixture проверяет группы/расходники/software/crew, own price 0 и отказы.
load-21/quote-contract-01 подтверждает native генерацию/расчёт на известной
доступной верфи: price=1210593, crewprice=0, crewcount=0; purchase_called=false.
Совпадение со штатным UI проверяется отдельно на том же payload. Права покупки,
native build, платёж и конечный корабль должны быть подтверждены следующим слоем.

quote-ui-06 уточнила нормализацию комплектации: пропущенные software slots
заполняются штатными IsSoftwareDefault/predecessor, как в getDataAndDisplay.
Native arrays удерживаются отдельно от очищаемого Helper.ffiTempStorage;
обе суммы округляются штатным RoundTotalTradePrice. Первоначальная цена
1233995 и цена меню 1233996 различались только оружием: 108760 против
108761. Между расчётами изменились цены верфи; это не основание для допуска
расхождения при оплате. Остальные позиции совпали, покупка не вызывалась.

Добавлен reprice для того же зарегистрированного quote и той же верфи:
обновляет цены существующей корзины, не генерирует другую комплектацию
и не меняет начальный quote. Fixture подтверждает изменение цены,
сохранение payload и отказ для чужой верфи/незарегистрированного quote.
Диагностическое сравнение со штатным меню теперь пересчитывает корзину
после подготовки меню. load-28/quote-ui-07 подтвердили в игре совпадение:
price=1233996, native_price=1233996, matches=true, обе crewprice=0,
initial_price=1233995, purchase_called=false. Новый пересчёт учитывает
изменившуюся цену того же оборудования; платёж не вызывался.
Пересчёт сам по себе не подтверждает права покупки, оплату или ready.

Продолжение native lifecycle: TrackBuild принимает только точный native
handle после успешного ReadBuild и удерживает его до согласования.
Другой заказ отклоняется как previous_build_unreconciled. ObserveTracked
читает очередь и сохраняет terminal наблюдение. Штатные события
event_player_built_ship (ship=param, build=param2) и
event_player_build_cancelled (build=param) связываются сравнением native
handle. Готовый ship сохраняется после удаления build из очереди;
read-back повторно проверяет существование, player ownership, macro и
operational. Cancelled не означает возврат денег, unknown не освобождает
заказ для повторной покупки. Отслеживание не создаёт build и не платит.

В диагностике ObserveNativeBuild удерживает один последний ship build из
event_player_build_added, включая заказы на чужой верфи. BuildContract
может проверить его userdata/ID/контейнер, вместо поиска только в очередях
станций игрока. XSD и scheduling проходят; настоящая передача native handle,
события ready/cancelled и их сохранение/load ещё требуют игровой проверки.
Вызов TrackBuild из копированного Manager пока не подключён.

load-29/purchase-fixture-01: штатные buttonAddPurchase/buttonConfirm заказали
один курьер на известной чужой верфи. price=1233996; баланс изменился
72431853 → 71197857, разница точно равна цене. Исходный save не перезаписан.
build-contract-03 подтвердил native userdata build, GetBuildTaskInfo.id
совпал с ConvertIDTo64Bit(handle), buildingcontainer совпал с native верфью,
native info.price=1233996. ABI и передача конкретного build теперь проверены.

TrackBuild в самом event_player_build_added вернул payment_unconfirmed:
событие произошло внутри AddBuildTask6 до последующего штатного
SetBuildTaskTransferredMoney. ReadBuild корректно не принял отсутствие
подтверждённой оплаты. Диагностическое чтение того же handle перенесено
в дочерний cue с delay=1s; нет повторной оплаты/создания задания.
Новый порядок прошёл XSD, его игровая проверка ещё впереди. Production
покупка должна согласовывать native added и payment receipt, а не считать
added доказательством оплаты. Путь копированного AI и ready ещё не приняты.

load-30/purchase-fixture-02: тот же исходный тестовый save, штатная покупка
1233996Cr. build-contract-05 подтвердил tracking=tracked, state=building,
paid=price=1233996, missing_resources=false, queue=0, ID/container совпали.
purchase-fixture-repeat-01 отклонена previous_attempt_unreconciled без новой
покупки. build-contract-06 подтвердил ready из native_built_event после
удаления заказа из очереди: ship userdata, playerowned=true,
operational=true, macro=ship_arg_s_trans_container_01_a_macro, paid=1233996.
Снимок собственности увеличился ровно на один объект: 69 → 70.

Поздняя TrackingResult стала previous_build_unreconciled: несколько
событий смогли пройти sent до первого отложенного чтения. TrackBuild
сохранил исходный handle, ready связь не заменена. В source первая
совпавшая native добавка теперь мгновенно переводит fixture в added;
дочерний read-back допускается только из added, затем observed. Новый
порядок блокирует перезапись результата другой добавкой и прошёл XSD;
его игровая проверка ещё не выполнена. Production адаптер должен связывать
MD handle с точным ID, возвращённым AddBuildTask6, а не первым совпадением.
Доказан обычный UI purchase/build/ready, но 3.5 остаётся открытой: этот путь
ещё не подключён к копированному AI без открывания UI.

Следующий шаг без UI: purchase_quote.to_plan использует штатный
Helper.convertLoadout с native software slots того же macro и удерживаемым
payload зарегистрированного quote. Не меняет комплектацию и не выполняет
покупку. План предназначен для обычного Helper.callLoadoutFunction перед
AddBuildTask6. Fixture проверяет native metadata и отказы для чужой верфи/
незарегистрированного quote; ABI check проходит. quote_contract дополнена
native преобразованием план → UILoadout2 без открытия меню и без эффекта;
проверка в игре нового пути ещё нужна. Полный purchase adapter остаётся впереди.

11.10.2026, полный пакет PID 84800 (07:30:45), load-15 accepted/save_004:
purchase-native-58 создал штатный заказ ID 34253ULL без меню, цена 1233995 Cr,
деньги 72431853 → 71197858 (точный расход). build-contract-59 подтвердил ID/container,
price=1233995, queue=0, missing_resources=false, но tracking=nil/state=unknown,
reason=no_tracked_build. Журнал age=388828.95: MatchNativeBuild не нашёл модуль
extensions.tm_empire_management.ui.purchase_submit. Файл был установлен, но
отсутствовал в ui.xml и не вызывал Register_Require_With_Init. Source исправлен
по шаблону остальных адаптеров: файл включён перед purchase_dispatch, модуль
регистрируется, return M сохранён для fixtures. purchase_submit_fixture теперь
проверяет регистрацию того же модуля и проходит; dry-run/strict OpenSpec проходят.
В PID 84800 исправление ещё не установлено. Покупка не повторялась; этот заказ
пока не принят как успешно связанный/доставленный, 3.5 остаётся открытой.

Сверка всех require собственных UI-модулей обнаружила ту же отсутствующую
регистрацию у construction_plot и construction_reserve. Оба helper-файла включены
в ui.xml перед construction_plot_dispatch и регистрируют свой M через штатный
Register_Require_With_Init. Их существующие fixtures теперь проверяют регистрацию
того же модуля и проходят. Эти source-исправления пока не установлены в PID 84800;
не доказывают реальную оплату участка или резервирование ресурсов.

Следующий пакет установлен в PID 102984 (11.10.2026 07:38:58), все 44 installed
SHA совпадают с манифестом. Установщик теперь до первого копирования проверяет
ui.xml, регистрацию каждого объявленного Lua-модуля и наличие всех собственных
require-зависимостей. Реальный пакет и две повреждённые копии проверяются
tests/ui_module_registration.py: 3 теста проходят; временные копии создаются
под .cache/tmp/ui-module-registration. Запрос load-16 ожидает подключения
(unified session 91014); повторная игровая проверка покупки ещё не выполнена.

11.10.2026, PID 74016 после сравнения времени запуска: оба расширения возвращены,
44 production SHA совпадают с installed-manifest. load-17 accepted/save_004.
purchase-native-62 один раз создал заказ 34298ULL за 1233995 Cr; баланс
72431853 → 71197858. build-contract-63: identity=true, container=true,
native_match=1, tracking=tracked, state=building, paid=1233995,
ready_ship=false, missing_resources=false, queue=0. Регистрация purchase_submit
теперь проверена реальным MatchNativeBuild, прежняя ошибка загрузки Lua устранена.
Оплата и готовность корректно различаются. Заказ не повторяется; доставка и
автономный выбор покупки самим Manager пока не доказаны, задача 3.5 открыта.
Свидетельства: .cache/tmp/station-boundary-20261011/purchase-native-20261011-62.json
и build-contract-20261011-63.json. Запуск до заставки с расширениями 101 s,
без обоих 103 s; результат в .cache/tmp/startup-ab-20261011/result.json относится
только к запуску, не к загрузке сохранения.

Тот же PID 74016, build-contract-65 без повторной покупки: state=ready,
tracking=tracked, ship_type=userdata, playerowned=true, operational=true,
macro=ship_arg_s_trans_container_01_a_macro, paid=1233995,
reason=native_built_event, native_match=1, payment_called=false. Штатное событие
постройки доставило реальный корабль после состояния building; готовность не
подменяется оплатой. Свидетельство: build-contract-20261011-65.json в том же
каталоге. Это диагностический заказ через native API; автономный выбор Manager,
передача корабля его конкретной цели и восстановление заказа после save/load
этим сценарием не доказаны. Поэтому checkbox 3.5 остаётся открытым.

Следующий source-пакет: в adapt_static_purchase разделены выдача приказа
купленному инженеру и подтверждение доставки. Ранее TM_LastEngineerKey
записывался до AcknowledgeDelivery: отказ подтверждения оставлял доставку
непринятой, но исключал её из следующих проверок. Теперь TM_EngineerOrderKey
фиксируется после штатного order receipt; повторные проверки этого ключа
выполняют только AcknowledgeDelivery, не создавая новый приказ и не добавляя
корабль в группу повторно. TM_LastEngineerKey записывается только при accepted;
при отказе сохраняется TM_WaitReason. Генератор, check_adapted_manager и полный
MD XSD/scheduling проходят. Это изменение пока не установлено в PID 74016;
игровая проверка конкретной цели статической обороны остаётся открытой.

В PID 74016 analysis-66 запустил доступный штатный GenerateShortageData.
ui-status-67 подтверждает native_shortages_evaluated/observed, но выбранных
экономических действий в проекции по-прежнему нет. Это не доказательство
автономной покупки или отсутствия потребностей.

Следующий согласованный SOURCE-пакет: native EvaluateSectorShortage и RequestProductionFreighter принимают ключ обычной оплачиваемой покупки как ожидающее действие, сохраняя штатный ActionReports/cost. Раньше они принимали только немедленно полученный NPC Ship; async quote/build оставался вне учёта. Request_Freighter записывает ключ до ожидания, delivered только после реального handoff/ack и штатный срок2h/4h из исходного Built handler. CheckRunningActions проверяет фактическую собственность вместо NPC isrequestedjobship; pending/unknown не снимает стоимость действия и не разрешает повтор. Терминальный отказ допускает обычный следующий цикл. Истечение штатного периода снимает запись действия, не уничтожает собственность. UI различает запрос/unknown и фактически полученный корабль. Выбор нужды и пороги остаются штатными. Игровая приёмка этого пакета ещё не выполнена.

11.10, analysis30/role31: штатная экономика сама выбрала request_priority_freighter для sunflower. Ключ purchase_21_392153.789; до оплаты отказ purchase_offer_budget_changed. Model совпадает, expected_budget7243185300 MD money против offered_budget72431853 Lua credits. scriptproperties.xml: money имеет suffix ct; player.money хранится в сотых долях кредита. GetNPCBlackboard передаёт money в Lua как кредиты, SetNPCBlackboard возвращает обычное число. Следовательно, при входе Lua→MD бюджет, paid, price и crewprice умножаются на1Cr, до сравнения с собственным budget, player.money и build.price/transferredamount. Исходящие money-поля, цены штатных Lua/API и платёжные функции не масштабируются повторно.

Эта же граница проверена в источниках plot quote, construction funding, supply quote/payment и hire paid receipt. Исправления внесены общей группой; положительная игровая приёмка ещё нужна. Доказанный отказ теперь записан непосредственно в ActionDefinition (failed/WaitReason) до освобождения Pending; UI role31 показывает waiting с точной причиной вместо прежнего unknown. Предыдущий положительный fixture/read-build подтверждал фактическую оплату и объект, но не эту автономную ветку с её Lua→MD ExpectedPrice.

### Приёмка 3.5 — автономная покупка, 11.10.2026

Analysis40/role41: обычный Manager самостоятельно выбрал request_priority_freighter для sunflower, key purchase_23_392649.211. Единственный обычный заказ стоимостью8370545Cr: Lua банк72431853→64061308, Build50 actual paid8370545, building, materials present. После save/load сохранён исходный MD build, точный pre-load C ID34384 ремапится в12345: восстановление идёт по сохранённой типизированной candidate list, а не по номеру component или поиску похожего корабля. Повторной оплаты нет.

Build52: ready по native_built_event, actual ship playerowned=true/operational=true, ship_arg_l_trans_container_04_a_macro. Role54: LastResult delivered, submission reconciled, Pending/Tracked очищены; ActionDefinition delivered/ship0x766df/expires407484.329. Та же собственность HBL-445 получила реальный TradeRoutine, один queued/tracked order, claim sent, goal Econ_Manager, controlled0. Завершение Request_Freighter после handoff штатно оставляет его cue invalid; собственность и действующий экономический приказ сохраняются. Это закрывает 3.5, но не двухчасовой прогон, кадровое обеспечение корабля или прочие обязательные домены.

Raw: .cache/tmp/station-boundary-20261011/reboot-batch-{analysis-40,role-41,load-47,role-49,build-50,build-52,role-54}.json. Legacy restoration требует одного кандидата с точной сохранённой квитанцией/верфью/macro/owner/ценой/оплатой; после восстановления index сохраняется. Нет спавна, выставления оплаты задним числом или повторного заказа.

### Повторная автономная покупка на quicksave

Load83/role96/build99/read104: свежий purchase_1_389791.137, exact289752ULL/ship_tel_l_trans_container_03_a_macro,5301758Cr, native typed MD build/index1 largefloat. Delivered YNL892/0x219d429, real TradeRoutine/Econ_Manager claim/order1/TTL404537.318. Следующий самостоятельный purchase_2_390142.584: scout1076355Cr, exact268345ULL, настоящий typedbuild, missing_resourcesfalse/queue0. Bank72431853→67130095→66053740. Первая квитанция не оплачивается повторно. Готовность второго заказа и сохранение этого прогона ещё не приняты; save102 только requested, файл не обновился.
