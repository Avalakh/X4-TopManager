# Незакрытые границы оценки станций

Проверка текущих источников в прогоне380; задачи5.1–5.6 и6.5 не приняты.
Штатный Upkeep используется как источник потребностей, производства, запасов,
счёта и подчинённых. Второй поиск торговых сделок и отдельный исполнитель не нужны.

## Обнаруженная несовместимость данных подчинённых

`tools/adapt_native_manager.py` формировал ship.cargo.capacity/ship.cargo.free.
`examples/x4_unpacked/libraries/scriptproperties.xml` (containercargolist) требует
capacity.all/free.all; bare capacity/free определены для modulecargolist.
Это тот же тип несовместимости, который ранее наблюдался в diagnostic326.
Исправлены генератор и воспроизводимые adapted источники. check_adapted_manager
и install_mod --include-adapted --dry-run PASS. Runtime packet373 не менялся:
installed economy SHA02D7698092CA1C65B8DA7141B38C3BE93F607DC65D59AD819409AAAD98939E75,
source economy SHA04C0B808983ECDD33D737C41614A85E3B1AED8A831DBC252197FB1EFF7511909.
Установить вместе со следующим общим пакетом; затем проверить реальную станцию
с подчинёнными, а не считать отсутствие ошибки на станции без кораблей приёмкой.

## Что текущий классификатор действительно доказывает

`md/tm_empire_assets.xml/AssessStationResponsibility` выдаёт unknown либо
insufficient_provision из штатного miningtypes/underfunded. Это состояние
обеспечения, влияние на потерю результата явно не доказано. ReadStationConditions
сохраняет одновременно нехватку шахтёров, бюджет, ручную паузу, нападение и
ограничения торговли; нападение или idle сами по себе не обвиняют менеджера.
AssessStationResults учитывает purpose и не считает отсутствие прибыли плохой
оценкой строящейся/складской/снабжающей станции, но часть результатов пока unknown.

Для полного требования5.3 ещё нужны доказательства доступной пригодной возможности,
конкретного решения её не использовать и связи с проблемой. Простая сумма idle/
shortage не удовлетворяет этому контракту. Нужны также подтверждённые внешняя и
смешанная причины; список внешних условий с impact unknown не заменяет их.
Не добавлять фиктивную manager_decision ветку, которая никогда не получает
проверенные наблюдения, и не помечать искусственную ручную настройку решением NPC.
Собирать недостающие факты из существующих native orders/trade events/Upkeep;
новый слой ограничить наблюдением и причинной проекцией без конкурирующего AI.

## SOURCE-ONLY: конкретное прерывание доставки

В адаптер штатного Upkeep добавлено пассивное наблюдение существующих подчинённых,
а не новый поиск сделок. Не более32 кораблей и8 shortage wares на кандидата;
сохраняется один пример. Требуются одновременно production resources wait,
own/operational ship с commander этой станции и assignment.trade, игрок не за
штурвалом, текущий Flee, нападение за последние5min (не из будущего), известный
живой противник с enemy relation. Недостающий производственный ресурс должен
быть в native InsufficientProductionWares, иметь нулевой запас станции и
положительный груз этого корабля. Сохраняются имена корабля/ресурса/противника,
объём, время нападения и наблюдения; скрытые объекты не раскрываются.

AssessStationResponsibility при таком свидетельстве выдаёт external в scope
provision — прервана конкретная поставка, общий ущерб выпуску не измерен.
При одновременно подтверждённой нехватке обеспечения выдаёт mixed, сохраняя
обе причины и рекомендации. Conditions содержит отдельный delivery_interrupted;
просто факт нападения остаётся impact unknown. UI расширен до6 независимых
условий, различает внешнюю/смешанную причину и не объявляет их ошибкой сотрудника.

MD/XSD/scheduling, воспроизводимый13-script closure и UI fixture PASS.
Installed packet373 не менялся; игровая положительная/отрицательная проба этой
границы ещё не выполнена. Это не общий детектор блокады и не доказательство
manager_decision: полный пункт5.3 остаётся открытым.

## Посторонние ошибки текущего журнала

В текущем debuglog trade.find.commander/$homebase.type на NPC станциях
«АРГ Арг. Порт» и «АРГ Арг. Верфь» соответствует строке14 diff расширения
mobile_space_station_ru/aiscripts/trade.find.commander.xml. В исходной vanilla
реализации такой добавленной проверки нет. Файл чужого мода не изменён.
Эти строки нельзя приписывать управляющему TopManager или менеджерам наших станций;
при причинной приёмке учитывать только точное совпадение объекта/периода/контракта.

## Аудит штатного возврата дефицита, Autonomy412/002

Оценка использует завершённый Report из собственного ProcessStations. Тот же
OwnerReports.$InsufficientProductionWares в штатном EvaluateShortages агрегируется
по сектору (native/adapted/md/tm_factionlogic_economy.xml:573) и рассматривается
экономическим алгоритмом. Отдельные покупки из окна оценки не добавлены: это
дублировало бы уже рассматриваемую потребность. Это подтверждает путь ресурсов,
но не завершает5.4: miningtypes и underfunded пока служат наблюдениями оценки;
положительное штатное рассмотрение соответствующих кадровых/корабельных и
бюджетных потребностей ещё требует отдельного подтверждения.

AssessStationResults различает production/building/ship_support/trading.
Для ship_support/trading результат unknown с объяснением отсутствующих данных;
отсутствие производства не превращается в плохую оценку сотрудника.
Полная причинная приёмка5.2/5.3 остаётся открытой.

Autonomy412/002: runtime active, age397833.909, market deferred4 с завершённым
report/index null. Расширение1 queued/native_construction_in_progress,
строительный бюджет463702Cr, builder1 sent/deployment pending. Новый purchase7
оплачен7649467Cr, building; отдельная доставка корабля ещё не подтверждена.
Это наблюдение текущего раннего тестового мира, не разрешение старой unknown
лицензии7 в сохранённом позднем save_004. Frozen установленный пакет не изменён.

## Строительный перевод: факты вместо намерения, staged413

ui/construction_funding.lua теперь сохраняет amount отдельно от paid=0 до
эффекта; после вызова сохраняет оба фактических баланса. paid задаётся только
при точном полном списании, состояние paid — после точного зачисления в
build storage. При частичном списании amount500/paid0/before1000/after750;
при полном списании и неполном зачислении paid500/storageafter350, state unknown.
Оба unknown блокируют повтор; никакого исправления денег или сброса квитанции.
construction_funding_fixture.lua проверяет границы и replay; Lua51 fixture PASS.
Изменения только source/test: frozen установленный408 не менялся, live новый
финансовый контракт ещё не проверен.

Первичные Upkeep_Management392–401 и455–460 подтверждают отдельные потребности
производственного бюджета и шахтёров. Они создают upkeep missions игроку;
вызов этих Start cues сам по себе не исполнит автоматическое обеспечение.
RequestProductionFreighter собственного native economy после завершения
производства использует minable/resource transport tags, Request_Freighter
принимает station requester и выбирает обычный платный miner. Нужно связать
текущие потребности существующих станций с рассмотрением этого пути в одном
стратегическом цикле, с existing-action coverage и квитанциями; выдача миссии
игроку не является приёмкой5.4. Этот разрыв не закрыт одним секторным отчётом.

## Возврат потребности в шахтёрах, staged414

adapt_station_mining_provision добавляет обработку после штатного
CheckRunningActions в EvaluateShortages. До8 станций за цикл с вращающимся
cursor; только собственные operational станции и native minable shortage.
Потребность вычисляет md.Upkeep.Needs_Subordinate_Mining_Ship_Lib. Не более128
ресурсов/подчинённых/существующих sector actions; превышение не считается
отсутствием обеспечения. Сначала stock Request_Commandeerable_Freighter,
затем существующий оплачиваемый Request_Freighter с station requester/priority.
Оба проходят имеющиеся guards/claims/обычные assignment и purchase receipts.

Успешный запрос регистрируется в существующем ActionReports со штатным
InsufficientProductionWares score, без выдуманного приоритета/нового dispatch.
Requester и ResourceTransport добавлены в definitions обоих штатных запросов,
включая прежний RequestProductionFreighter: pending/unknown текущего назначения
закрывает тот же station/transport. Для старых definitions учитывается также
реальная незавершённая claim.assignment.commander; неизвестное не повторяется.
Stock CheckRunningActions сохраняет cost незавершённых purchases и снимает
утраченные/завершённые потребности по прежним правилам. Только cursor сохраняется
между циклами; временные reports/definitions освобождаются.

13-script генерация, check_adapted_manager, MD/XSD/AI/scheduling PASS;
validate414.txt. Это source-only пакет после frozen408: новый путь ещё не
установлен/не подтверждён игрой. Бюджет операционной станции остаётся отдельной
незавершённой границей;5.4 остаётся открытой. Следующий пакет объединит её с
413 финансовыми фактами и414 mining needs перед игровым прогоном.

Autonomy412/003 старого frozen408: age398132.326, purchase7 реально delivered,
construction1 queued, builder1 ещё sent. Collector80242 подтверждён live;
четыре выборки за903.0196345s, полного двухчасового свидетельства ещё нет.

## Рабочий бюджет станции, staged415

TM_Empire_Supply.RequestStationFunding вызывается из того же bounded прохода
EvaluateShortages, до mining needs. Штатное условие Upkeep: operational owned
station/tradenpc/own account/not restricted, баланс<=90% productionmoney.
Полный gap оплачивается только при наличии денег; нет новых миссий/dispatch.
MD повторно проверяет governor/goal и сериализует одну Receipt. Lua использует
stock GetComponentData money/productionmoney и TransferPlayerMoneyTo(station).
При изменившейся цене/балансе, недостатке денег, потере собственности/оперативности
или revoked approval нет эффекта. До перевода persisted payment_sent/amount/paid0;
после сохраняются player before/after и station before/after; debit и credit
согласуются отдельно. Unknown/payment_sent блокируют любое повторное пополнение.
MD согласует обе суммы, station/key/wanted и помечает observed/reconciled.
RevokeGoalApprovals включает новую approval; общая UI projection показывает
рабочий бюджет и факт подтверждённого пополнения с именем станции/суммой.

Новый station_funding_fixture Lua51 PASS: полный debit/credit, same-key и
unreconciled replay, изменившаяся quote, cap/poor/foreign/lost/revoked,
частичный debit и credit, payment_sent после load. UI registration и полный
MD/XSD/AI/scheduling PASS (validate415.txt). Это staged source: installed408
сохраняется frozen для Autonomy412; игровая финансовая приёмка ещё открыта.

## Границы подготовленного пакета, staged416 / Autonomy412/004

Budget рассмотрение отделено от mining-cap: owned operational станция с более128
подчинёнными/ресурсами не теряет возможность обычного финансирования.
Mining cap сохраняется до вызова native Upkeep, сверх лимита не выдаётся
ложная потребность. ReadGoalLifetime проходит cue ancestry; RevokeGoalApprovals
включает station approval и отзывает ещё approved callback при отмене любой
родительской цели. После реального перевода наблюдение сохраняет факт независимо
от последующей утраты объекта; текст не читает knownname несуществующей станции.
Diagnostic Lua source дополнен read-only station_funding_lua для request/payment:
key/state/reason/amount/paid/balances. В installed диагностике этого ещё нет.
Lua syntax и полный MD/XSD/AI/scheduling PASS (validate416.txt).

Autonomy412/004 frozen408: age398432.603, builder_hire1_397163.919 теперь
observed/native_hired_builder_arrival_observed, observed398307.292. Ранее sent
в003. Fee50000/paid50000 в Lua квитанции, текущая storage builder0x117a7.
Expansion1 всё ещё queued/native_construction_in_progress. Осталось2 типа
строительных ресурсов; budget/wanted327430Cr, processing1. Lua builder_result
остаётся историческим sent, новый фактический arrival хранится в MD Receipt;
это не повторный найм. Collector80242 live; samples5/1203.27638s. Игровое
приёмочное окно пока не завершено; источник416 и runtime408 различаются явно.

## Штатный выбор сделки и период, Autonomy412/005

Primary trade.find.commander.xml590–596 сортирует native buy offers по stocklevel
и признаку primary resource.604–633 учитывает buyspaces, относительную цену
собственного buyoffer, фактическую совместимую вместимость, известность продавца,
торговые ограничения и objectactivity blacklist.635–653 исключает same owner и
нелегальный груз, выбирает лучший native tradevalue.655–658 принимает конкретную
пару только при available/positive amounts; возвращает buyoffer/selloffer/failure
в конце script. Поэтому наличие публичного продавца/idle корабля не равно
пригодной альтернативе для конкретного управляющего: native filters и capacity
должны совпасть, а выбранное решение — наблюдаться. Готовые generic shortage
reports не содержат этот decision trace. Не добавлена фиктивная manager_decision
ветка и не изменён чужой trade.find.commander. Для дальнейшего причинного пути
нужны read-only факты native выбранной/отвергнутой пары с её constraints и
привязкой к station employee/period;5.3 остаётся открытой.

Проверка периода не выявила подозреваемого сброса от обычного изменения cargo:
SameProvision сравнивает stock capacity/owner_only, не count, и сохраняет до16
предыдущих observations. Actual005: KMT485 и HQ XZS342 имеют samples2/from397511.821
и observed398494.926; finance samples2 с теми же сотрудниками, без ложного
переноса старого периода. KMT работ0/1/resources1, не manager fault; HQ purpose
building, торговая прибыль не критерий. Это реальное подтверждение продолжения
периода на двух native analyses, не полная смена сотрудника/load приёмка5.1.
Runtime active age398727.079/economy_last_run398494.926/deferred4/report-index null.
Builder1 observed, expansion1 queued. Collector80242 live; samples6/1504.7016479s.

## Доли кредита, staged417

station_funding и construction_funding теперь принимают native Money с точностью
до0.01Cr, вместо integer-only Cr. Gap нормализуется до целых сотых; debit/credit
сравниваются с допуском строго менее0.005Cr для бинарной арифметики, поэтому
недостающая0.01Cr не проходит. MD StationFunding преобразует каждый исходный
баланс отдельно в Money до вычитания, а не превращает неточную double разность
в деньги. Quotes и budget cap сохраняются, partial/unknown не повторяются.

Оба Lua51 fixtures PASS: before1000.07/balance100.01/wanted600.03 ->paid500.02,
after500.05/destination600.03. Отдельная недостача0.01 debit даёт unknown/paid0
и блокирует retry. Точность не заменена большим допустимым финансовым расхождением.
MD/XSD/AI/scheduling PASS, validate417.txt. Изменения staged/source only;
frozen installed408 и текущий Autonomy412 не менялись. Игровая cents приёмка
нового пакета ещё не выполнена.

## Общий Lua пакет418 / исправление сценария419

Пакет всех13 tests/*fixture.lua на Lua51 текущей игры:12 PASS, один supply
сценарий упал на dofile('ui/purchase_dispatch.lua') из workspace root.
В fixture было два таких загрузчика; оба приведены к общему пути
X4_TopManager/ui/purchase_dispatch.lua. Повтор supply419 PASS: durable payment,
single record и unresolved replay. Production снабжение не менялось; остальные12
сценариев после их успешного исполнения также не менялись. Первоначальный FAIL
сохранён в fixtures418.json, отдельный успешный повтор — supply419.txt.
Это пакетная Lua проверка13 сценариев, не игровая приёмка всех доменов6.1.
Collector80242 подтверждён live; установленный408 не изменён.

## Сборка420 / Autonomy412/006

install_mod --include-adapted --dry-run PASS:47 файлов, staged Manager включён,
установка не выполнена. Новый файл station_funding добавлен в ui.xml и прошёл
registration/dependency validation. Основной пакет413–417 подготовлен вместе,
а не частичной заменой установленного runtime. Первоначальный обычный доступ
к game path дал WinError5; повтор с read-capable escalation успешно проверил
dry-run. Автоматического отклонения разрешения не было.

Actual006: runtime active age399026.449, native economy last_run398494.926.
Новый purchase8_398497.083 delivered, ship0x21b3c65 capacity25500/water;
purchase7 также delivered/capacity37000. Шесть различных native actions имеют
ships/claims; секторная оценка не повторяет один оплаченный ключ. Builder1
observed, expansion1 всё ещё queued/native_construction_in_progress. Это
подтверждение следующей доставки текущего frozen408, не игровой успех нового
station budget/mining path. Collector80242 live, samples7/1804.0846326s;
полное двухчасовое окно и последующий новый пакет ещё не приняты.

## Финансовые причины в UI, staged421

station_funding/construction_funding отделяют стабильный reason code от detail
Lua traceback. Для unknown сохраняется исходная detail до256 символов, а UI
получает различимые debit_unconfirmed/credit_unconfirmed/effect_unconfirmed.
Добавлены русские объяснения удержания повтора, изменившейся quote/недостатка
бюджета/отзыва approval. Технический путь файла больше не является основным
объяснением финансовой ошибки пользователю. Фактические суммы и состояние
квитанции не менялись. Оба financial fixtures и empire_status fixture PASS.
Source-only: installed408 и collector80242 не менялись. Проверка stale callback
не выявила подтверждённого сценария выдачи нового MD approval до согласования
предыдущей Receipt; дополнительный конкурентный исполнитель не вводился.

## Подготовка игровой финансовой пробы, diagnostic422

Добавлена отдельная diagnostic station_budget_setup (MD cue/Lua pipe routing/
probe CLI), не входит в product install. Только operational owned KMT485 с
обычным tradenpc/own account, sunriseflowers, положительной productionmoney,
unrestricted trade и достаточным исходным балансом; активный governor и отсутствие
предыдущего StationFunding receipt обязательны. Однократно переводит существующие
деньги из station account обратно faction.player до половины productionmoney;
сохраняет before/after/player balances и exact transferred read-back. Создания
денег, прямого продукта payment approval или изменения менеджера нет.
Любой previous_attempt удерживается, включая unknown; загрузка исходного тестового
мира отделяет fixture. При restricted factory возвращает unavailable без эффекта:
этот guard не отменяет вручную торговые правила ради положительной приёмки.
После успешной fixture пополнение должно рассмотреть обычное EvaluateShortages,
а diagnostic только читать station_funding_lua и MD/UI. Никакая оплата этой
fixture не считается автономным результатом: автономный результат — последующее
пополнение самим Manager, подтверждённое debit/credit и unchanged employee.
MD/XSD/scheduling/Python syntax PASS. Команда ещё не установлена/не исполнена;
collector80242/frozen408 сохраняются единственными владельцами live runtime.

## Прошлые периоды и принадлежность сотруднику, staged425

Native observation сохраняет employee_name и строковый employee_seed в момент
наблюдения: удаление/перенос/переименование текущей actor entity не меняет имя
уже сохранённого снимка. ReadPreviousPeriods просматривает текущий observation и
до16 предыдущих, выдаёт максимум4 различных прежних period tuples. Дубликаты
сверяются по employee/seed/session/manager/from; текущий tuple исключён,
future после rollback не показывается. Rows сохраняют сотрудника/seed/from/to/
samples/session; прежняя загрузка отделена текстом от прежнего назначения или
обеспечения. Старый формат без snapshot имени явно показывает «имя не сохранено»,
а не угадывает имя по текущему manager. Основные finance/production summaries
по-прежнему используют только текущий tuple.

UI валидирует bounded4 строки, порядок времени<=observed, целые samples/session,
строковые employee/seed/reason и показывает «Прошлый период» отдельно от нового
сотрудника. Fixture PASS: прежнее и новое имя различаются, historical row
отрисована, future/дробная session/>4 rows отвергнуты. Генерация13-script closure
и полный MD/XSD/scheduling PASS, validate425. Это source-only; живой сценарий
смены сотрудника/load с новым history UI ещё не принят,5.1/5.6 остаются открытыми.
Collector80242/frozen408 продолжается, installation не менялась.
# Source439: наблюдаемые результаты торговой станции

Оценка trading/storage использует уже записанные native TradeEvents текущего
employee/manager/session/period. При complete потоке с положительным incoming
или outgoing она показывает observed результат движения товаров, число видов
каждого направления и период. Разные wares не суммируются в условные единицы.
Нулевое движение, неполный поток или отсутствующий период остаются unknown;
нет автоматического обвинения из-за отсутствия прибыли. Производственная оценка
дополнительно сообщает confirmed finished cycles за период из native events.
Циклы разных модулей не объявляются объёмом выпуска или effective utilisation.
Проверки439 MD/XSD/scheduling и UI fixture PASS, live пока install432.
Полное5.2 (в частности ship-support заказы) и5.3 остаются открыты.

