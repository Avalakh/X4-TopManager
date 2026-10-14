# Пакетная игровая проверка после перезагрузки

PID 36596; Steam без дополнительных параметров; save_004 принят штатным загрузчиком. Свидетельства: `.cache/tmp/station-boundary-20261011/reboot-batch-*.json`.

Проверено: независимость должностей (existing_post / bound / manager_unchanged=1); активный собственный Manager; 69 активов, две станции; вкладка 1205 px, 76–96 строк; переходы empire/stats/status; отрицательное обучение required_seminar_missing, management 8 без изменения. Визуальная читаемость ещё не принята.

Независимые ошибки общего прогона:
- Экономический счётчик обращается к удалённому OwnerReports: журнал EvaluateSectorShortage line1286. В генераторе заменено чтением собственного GlobalStorageData по текущей фракции. Остальные результаты анализа и две записи отказа от нового действия сохранились.
- Person summary не сохраняется как отдельный MD объект: RequestTransfer line536 и null Entry. Исправлены чтения свойств напрямую через Source/Target.people.{Person} в переводе, наблюдении прибытия, обучении и диагностике. Это адаптация по образцу штатного Conversations; не новый кадровый алгоритм.

Отправлен ровно один перевод существующего service crew GYU-115 → MZK-812, template 9873631311134785487, target 0x4aaa6. Receipt sent не доказывает прибытие. Перевод не повторять; сохранить текущую тестовую сессию, установить общую группу исправлений и проверить эту же квитанцию после load.

MD XSD/scheduling и аудит адаптированного замыкания проходят. Исправления ошибок пока SOURCE, текущий PID содержит предыдущую версию. Задачи не закрываются этим отчётом.

Повторный пакет установлен после штатного CloseMainWindow (True/WaitForExit True). Новая сессия PID6452, load05 accepted/save_004. Штатное сохранение 89 834 825 байт содержит native_transfer_pending, тот же template и PersonnelTransferAttempted. Arrival06 выявил смену component handle после load; это ошибка тестового наблюдателя, не исчезновение receipt. Arrival07 использует постоянный idcode MZK-812: реальная target запись того же template существует, роль service соответствует, source_member=0, intransit=1; observed пока не подтверждён. Источник штатного пути: Conversations NPCAssigned и LaunchCrewTransferPod, собственный маршрут не добавляется.

В следующий source UI-пакет включены русские причины player_helm и sent/observed/unknown перемещения экипажа. Проверка no-action records использует штатный оператор существования без suppress-префикса на уже проверенной Economy cue. Живой эффект этой правки ещё не доказан.

Arrival07 завершён unverified после десяти минут наблюдения: та же запись на MZK-812, source_member0, intransit1; production receipt unknown/native_crew_arrival_not_observed. Повтор не отправлен; Manager active, независимая кадровая цель продолжает проверки. Анализ08/UI09 подтверждает исправленный report_stations=1 вместо null, product_sectors1/action_sectors0/no_action_records2. Единственная новая MD ошибка относится к diagnostic Read: sector=null у исчезающего корабля; source формирует явное неизвестен вместо обращения к knownname. Для следующего пакета добавлен crew_actor read-back реального roleentity/container/ship/station/roleobject, без изменяющих действий.

Корневая причина пустого UI подтверждена игровым журналом: Vertical space left621, required min height1643, Table will not be displayed. Все строки создавались с rowdata=false; Helper отмечает их неселектируемыми, widget_fullscreen включает scrollbar только для interactive table. Исправлено на штатное addRow(true); fixture теперь проверяет эту границу. Это исправление реального отказа рендера, а прежний body_rows не был доказательством видимости. Общий пакет с ролью станции, русскими кадровыми причинами, no-action guard и crew_actor установлен; load11 выполняется.

Экономический пакет установлен: load15 accepted, PID32672; 44 SHA манифеста совпали с установленными файлами. Analysis16/UI17: action_sectors1, явный unknown для заказа, неполный публичный рынок sunflower; UI82 rows/1205x621. Это ещё не успешная приёмка: debug.log выявил FillKnownSellOffers/$TM_KnownMarketWares undefined. run_actions получает отдельную область переменных, поэтому MarketCache и SectorSellOfferAmountsTable теперь передаются явными параметрами по штатному образцу CheckRunningActions. Источники повторно сгенерированы; XSD/scheduling и closure audit проходят. Сохранено то же test save_004 (09:28:19, 90 946 905 байт), X4 штатно завершён, исправленные 44 файла установлены. Load20 accepted; повторная analysis21 выполняется. Ни отсутствие ошибок XSD, ни строки UI не закрывают живые сценарии.

Analysis21/UI22–23: FillKnownSellOffers больше не выдаёт ошибок MD; нет Vertical space/Table will not. UI98 rows/1205x621, реальная визуальная видимость/прокрутка остаётся открытой: средство захвата показало перекрывающее окно другой игры. Другие приложения не управлялись. Сохранение24 (09:36:37) и отдельная диагностика role27 показали LastResult waiting/purchase_offer_changed с прежним ключом purchase_20_391567.911 и invalid goal; Pending отсутствует, экономических action rows в этом read-back нет. Дооплатный отказ не является покупкой. Причины отказа теперь разделены на shipyard/macro/budget, diagnostic read дополнен ключами и полями ожидаемого/полученного предложения.

Следующий общий пакет установлен после сохранения28 (09:42:53, 91 201 069 байт): публичные предложения считываются по известным секторам в штатном радиусе5 переходов, а не по всей галактике с общей отсечкой128. Используется штатный find_sector_in_range и неизменённые коэффициенты/пороги; соседняя таблица включает известные внешние секторы без частных отчётов NPC. Границы32 секторов и128 предложений на сектор явно дают incomplete; каждый сектор/товар учитывается один раз за analysis. PreparePurchase получает необязательную ссылку на штатную ActionDefinition, записывает ключ до Lua event и передаёт гарантированный дооплатный отказ прямо в неё: он не теряется между callbacks и 15s watcher и не превращается в вечное unknown. По старым неоднозначным квитанциям повтор не разрешается. XSD/scheduling, closure audit и существующий Lua fixture проходят. Load29 выполняется; живые эффекты нового пакета ещё не приняты.

Analysis30/role31: новая штатная request_priority_freighter/sunflower, purchase_21_392153.789 failed/purchase_offer_budget_changed, UI waiting. Подтверждено точное расхождение MD money7243185300 и Lua credits72431853 при совпадающей модели. Исправления всех входящих денежных величин через1Cr установлены общим пакетом purchase/construction/supply/personnel, load33 принят. Analysis36/role37 прошёл бюджет, но следующая попытка22 завершилась manager_unavailable до оплаты. Сравнение обёрток одной верфи заменено на штатный IsSameComponent; то же сделано для quote context, supply и construction authorization. Существующий purchase_submit fixture расширен настоящим dispatch: разные wrappers одного ID проходят, другой ID до оплаты не проходит. purchase quote, funding и supply fixtures проходят.

Load39/analysis40/role41: одна автономная оплаченная покупка purchase_23_392649.211 дошла до обычного build. Build42 (только read-back, payment_called=false) показывает цену8370545Cr, native identity/container=true, queue0/missing_resources=false. Production ReadBuild получил component cargo_gen_buildstorage вместо build: при возврате Lua userdata потерян тип, числовой BuildTaskID разрешился как component ID. Подтверждены MD lookup errors именно этой границы; post-purchase повтор заблокирован Pending, readiness не подтверждена. Save43 (10:01:39, 91 393 051 байт) содержит уже оплаченную постройку. Match теперь возвращает только candidateindex/точный ID, а MD берёт исходный typed build из собственной неизменённой candidate list с key/id/yard/macro/типом/границами индекса. CompletePurchase/orphan используют этот же путь. ReadBuild явно отклоняет не-build. Существующий fixture подтверждает отсутствие build userdata в возвращённом payload. Числовой индекс проверяется штатным cast(... )i; незадокументированный floor-property исключён. Load45 того же save43 выполняется с установленным исправлением и read-only диагностикой типов/квитанции; новая оплата не выполнялась.

Load47/role48–49/build50: восстановлена исходная единственная native candidate после remap BuildTaskID34384→12345. Legacy migration требует совпадения key/Submission.id/Match.id, ровно одного typed build, player ownership, верфи, macro, цены и фактической оплаты; world search отсутствует. Индекс1 сохранён, tracked_type=build, recovery=saved_native_build_recovered, building/paid8370545Cr, bank64061308Cr неизменён. Watch15s только восстанавливает уже оплаченный receipt, новую оплату не вызывает. Save51 завершён: 10:19:50, 91 328 410 байт. Build52: native_built_event, ready, playerowned/operational=true, cargo ship_arg_l_trans_container_04_a_macro; payment_called=false. Role53: LastResult delivered того же ключа, Submission reconciled, Pending/Tracked очищены. Экономический handoff ещё pending: получение готового корабля не доказывает принятие назначения.

SOURCE следующего согласованного пакета: готовые MD production flags (isproducing/ispausedmanually/ispaused/iswaitingforresources/iswaitingforstorage) считываются один раз за native analysis, максимум32 модуля; incomplete явно сохраняется. UI показывает снимок работы/ожидания/пауз, не выдумывает длительность простоя и не обвиняет сотрудника. XSD/scheduling, closure audit и существующий UI fixture с проверкой ложной полноты/unknown проходят. Этот пакет ещё не установлен, живой read-back production остаётся открытым.

Role54 подтвердил handoff первой покупки: HBL-445/0x766df, actual TradeRoutine, claim sent, goal Econ_Manager, queued_orders1/tracked_orders1, controlled0. ActionDefinition delivered с native expires407484.329. Задача3.5 принята по этой полной цепочке.

Продолжение автономной сессии выбрало следующий заказ24 стоимостью1135669Cr. Role57 выявил candidateindex1/typeof largefloat, что старый guard integer/float отклонял. Исправлено принятие всех четырёх штатных числовых типов с сохранением integral cast/range1..16/typed original candidate. До установки фикса второе строительство завершилось и build handle был удалён: Load59/role60 candidate0x0. Его исход остаётся unknown, Pending блокирует повтор; поиском похожего корабля не подменяется. TrackBuild больше не сравнивает два отсутствующих handle как build_already_delivered; missing явно unknown/build_handle_missing. Native matching после удаления build не является readiness failure первого принятого заказа. Требуется свежая общая проверка следующих покупок с исправленным числовым guard; релиз не квалифицирован.

UI61 + визуальная проверка средствами computer-use: actual X4 window1773598, body83 rows/1205x621, текст собственности/статусов виден, sidebar между empire/stats. Scroll1480 показал поручения, строки unknown кадрового перевода и наблюдения двух станций; страницы доступны по штатной прокрутке. Никакое другое приложение не управлялось. Это подтверждает исправление пустой вкладки, но не закрывает причинные оценки или весь5.5/5.6.

Save64: 11.10 10:34:17, 92 081 793 байт. Новый общий пакет44 файлов и diagnostic MD/Lua установлен штатным CloseMainWindow/WaitForExit; load65 accepted. Дополнен bounded event observer штатными production_started/finished/cancelled research=false, не более32 станций; запись требует текущего owner/manager/employee/session/provision period. Первый event открывает отдельное покрытие: нулевые события до него не выдумываются, циклы не выданы за объём выпуска/idle duration. UI fixture отклоняет чужой период и события из будущего после rollback. Живое завершение производственного цикла ещё не проверено.

Training66: seeded1 тестовый семинар (только diagnostic extension, production inventory/spawn logic не добавлена), RequestSeminar result/state observed, KMT-485 manager0x191b7 skill.management8→11, inventory_before1/inventory_after0, manager_unchanged1. Применены те же add_skill/inventory-consumption действия семинара из stock Conversations.g_seminar_management, с собственной receipt/read-back; прямого выставления заданных звёзд вне потребления предмета нет. Replay67: training|already_attempted|state=observed, нового семинара/обучения не было. Предшествующий отрицательный training с отсутствующим предметом сохранял skill8. Задача4.3 принята, paid hire/crew arrival/двухчасовое управление и полноценная оценка остаются открытыми.

Save69: 11.10 10:45:50, 92 394 528 байт; обучение сохранено. Load70/arrival71: старое назначение Source0/Target1/template9873631311134785487/role service подтверждено, отсутствуют actor/pod-arrival/scheduled, остаточные flags intransit|temporary. Однократно возобновлён только stock Conversations.LaunchCrewTransferPod после owner/operational/helm/manager/role/membership проверки, assignmentobserved=transportattempted394278.115. Stock helper сам оценил10s; live reads003–004 подтвердили pod_arrival394288.116 и temporary0, затем005+ pod_arrivalnull. Исходное assign_hired_actor не повторялось, employee не создавался. Однако intransit остаётся1: arrival71 unverified,4.2 не закрыта. Чистка этого флага ради observed не выполнена. Дополнены arrival/availability/training guards явной проверкой podarrivaltime: наличие назначенного person и отсутствие общего scheduled-флага сами по себе не доказывают прибытие.

Независимые ошибки того же прогона: HoldSpace считал $EconomicCue.TM_RequestSectorFactory динамическим свойством, которого cue API не имеет (scriptproperties cue содержит только стандартные свойства и $variables). В SOURCE хранится прямой типизированный $tm_empire_factory_receiver в локальном namespace Econ_Manager, регистрируется при init/load; HoldSpace сигналит этот указатель. NPC-only RedeployJobShips читает jobmainsector/isvalidjobspace у обычных player ships: SOURCE дополнен faction!=player guard именно для этой job/quota ветки; управление собственными кораблями остаётся в copied HoldSpace/DefendArea с claims. Originals не изменены. Перегенерация13+3, XSD/scheduling и closure audit проходят. Этот последний пакет ещё не установлен/не принят в игре.

Save72 завершён: 11.10 10:57:28, 92 633 680 байт, однократный transportattempted сохранён. Последний общий пакет44 файлов установлен штатным CloseMainWindow/WaitForExit, load73 выполняется. Именно этот пакет включает factory receiver typed pointer, NPC-only job redeploy gate, podarrivaltime в arrival/availability/training guards. Strict OpenSpec проходит, принято8/32, release unqualified. Однократное возобновление транспорта не повторять; stale physical intransit пока не снят и4.2 открыта.

Load73/role74–75: runtime active, economy_exists1, первый HBL-445 продолжает TradeRoutine; второй purchase24 unknown/build_handle_missing удерживается, transportattempted394278.115 сохраняется без нового запуска. Source0/Target1/role service, pod_arrivalnull/temporary0, intransit1 — перенос не принят. В свежем debug.log не найдены свои MD errors, factory receiver/job-space errors; это проверка отсутствия повторной ошибки, не положительная приёмка строительства/флотов.

SOURCE: ReadStationEvidence передаёт stock observation.restricted; UI показывает глобальную торговлю только со своей фракцией либо её отсутствие, не делает вывода об остальных правилах или доступности рынка. UI validator запрещает недостаток бюджета по штатному underfunded при restricted=true; unknown поле не превращается в false. Existing UI fixture и MD XSD/scheduling проходят. Диагностический arrival observer дополнен pod_arrivalnull как обязательной частью read-back. Новые UI/diagnostic поля ещё не установлены.

Save76 завершён11:14:30/92769262bytes; пакет44 файлов установлен, load77 accepted. Ранний read78 до5s-регистрации показывал factory_receivernull и ещё отсутствующий новый snapshot — это не выдавалось за полноценные наблюдения. Role79: active, factory_receiver_exists1; snapshot69owned assets/2stations/26S/30M/10L/1XL/other0, states4waiting/2sent/0unknown/63excluded, rows64 явно ограничены. Независимый find_station/find_ship read даёт2+67=69. Семинар и оба purchase receipts сохранены, повторной оплаты/транспортировки нет. Analysis80 запрашивает только штатный анализ для нового периода; это не двухчасовая автономная приёмка.

Provison81: stock restricted1 у KMT-485/HQ; бюджетный underfunded не выдаётся при глобальной внутренней торговле. KMT stocks воды/энергоэлементов0 и native waiting_resources1 наблюдаются отдельно от ответственности менеджера. HQ productionmoney0 не получает плохую оценку за отсутствие прибыли.

Следующий SOURCE-пакет: кадровые/доменые receipts проецируют source/target/person только из действительных собственных ссылок и существующего person summary (его документированное name), без подмены generic reason-code; UI показывает участников отдельной строкой и проверяет тип/длину. Guards найма/оплаченного назначения/его принятия теперь тоже учитывают native podarrivaltime. Для production sample summary используется существующая history16: максимум текущий+15 прошлых, exact manager/employee/session/provision period, отсутствие future/duplicate/incomplete samples. Счётчики обозначают снимки, не часы простоя/продуктивность/вину. UI reject другого периода/future/числа снимков и fixture отображения проходят; MD XSD/scheduling проходят. Пока не установлено, задачи5.1/5.2/5.3 и4.1/4.2 не закрываются.

## Свежая исходная точка — load83

Пользователь разрешил любое нужное сохранение; выбрано quicksave time388755.473 до старого transfer388848.534 и заказов23/24. Исходный слот не перезаписывается. Новая группа44 файлов установлена после успешных XML/XSD/scheduling и UI fixture. В signal CaptureCrewPod исправлен недопустимый атрибут param заменой на штатный signal_cue_instantly; также capture вызывается после успешного assign_hired_actor. Записанные actual native deadline и identity служат предпосылкой однократного восстановления физического экземпляра существующего person, последующий read-back обязателен. Старый unknown без deadline не объявляется успешным. Игровая проверка начата, приёмка этой группы остаётся открытой.

### Load83 / назначение85 / module87–UI97

Load83 accepted quicksave. Role84: runtime inactive, нет управляющего/квитанций.
Модуль module87 observed0x4ac99 на HQ/XZS342; place88 тот же existing employee
seed3697903391642939190, station manager0x4ac2f unchanged. Read89 bound,
read94 active, factory receiver exists1, единственная регистрация player manager.
UI97: mode tm_empire_status, frame1249, rows82, width1205/maxHeight621.
Исчезновение кнопки объяснено условием has_governor, подтверждённым ранним save;
после назначения кнопка/вкладка возвращены. Human разрешил module command.
Native analysis91: current period samples1, stocks воды/энергоэлементов0,
обе станции trade_restricted1, history_samples1; ложного бюджетного обвинения нет.
Автономная покупка purchase_1_389791.137 оплачена5301758Cr, bank67130095Cr;
read96 candidate index1 typeoflargefloat, tracked_type build, native build289752ULL.
Пока building, готовность/назначение остаются непринятыми.
Transfer95 sent существующий person9873631311134785487 GYU115→MZK812,
source0/target1. Arrival98 наблюдает actual native pod389822.438, но production
receipt его не успела зафиксировать: штатный actor запускает короткий timer
несколько секунд после assignment. Новый source CaptureCrewPod повторяет только
наблюдение до30 раз/1s, без dispatch; XML/XSD/scheduling прошли. Этот патч
пока не установлен. Actual intransit1/temporary1 и podnull не считаются успехом.
Diagnostic CheckRoles до fixture readiness выдала missing State.Employee;
source теперь возвращает явный binding_fixture_not_ready через do_if/do_else,
не меняя состояние. Полная приёмка по-прежнему8/32.

### Продолжение104/105

Read104: первый свежий purchase_1_389791.137 delivered, YNL892/0x219d429,
TradeRoutine, Econ_Manager claim/order1, exact action Ship link/TTL404537.318.
Bank67130095 после5301758Cr; следующий самостоятельный stock scout order
purchase_2_390142.584 paid1076355Cr, bank66053740Cr. Build105 exact268345ULL,
ship_arg_s_scout_01_a_macro, missing_resourcesfalse/queue0, typedindexlargefloat
tracked_typebuild. Повторной оплаты первой квитанции нет. UI103109rows.
Arrival98 timeout180s, crew flags intransit1/temporary1, native actor disappeared,
source0/target1; dispatch не повторён. Capture patch ещё не установлен.
Save102 только requested: файл save_004 остаётся11:29:15/93365301bytes;
успешного сохранения этой исходной точки не заявляем. Diagnostic save source
теперь использует stock SaveGame+closeMenu в одном callback, устраняя deferred
UI callback; реальная запись файла всё равно обязательна. Снимок sky окна X4
оказался визуально несогласован с игровым read-back; ввода по нему не было.
Source UI дополнен bounded счётчиком подчинённых из готового native observation:
total/observed/operational/playercontrolled/coverage. Это не измерение throughput.
XML/XSD/scheduling и расширенный существующий UI fixture прошли до save Lua правки.

### Установленный повторный пакет106–111

Новая группа44 файлов и diagnostic MD/Lua установлены, XSD/scheduling/UI fixture,
diagnostic Lua5.1 syntax и OpenSpec strict прошли. Load106 quicksave accepted.
Fresh107 назначил реального отдельного сотрудникаseed-9126173547698565463,
HQ module0x4b9a8; station manager0x4b93e сохранён, runtime active/goals1.
Штатный scout purchase_1_388784.415 paid1213332Cr/build35119ULL завершён delivered,
bank71218521; фронтовая Scout/Recon цель не является проверкой всей военной ветки.
UI fresh107/03380rows, width1205/maxHeight621. Transfer sent388785.862,
точный person9873631311134785487/sourceGYU115/targetMZK812;120s не подтвердили
arrival. Actor исчез, target-member1/source0/intransit1/temporary1/podnull.
Реального native timer в этом отрезке не наблюдали; deadline не выдумывается.
Arrival111 наблюдает этот же receipt до900s без повторного assign_hired_actor.
Save fresh107/035 действительно записан12:15:20,94534284bytes,
header game.time388907.261 / bank71218521 / same GUID C45BAA91-B465-4CF8-B9F7-3B8AF5303AC3.
Исправление deferred diagnostic save на stock SaveGame+closeMenu подтверждено.
Analysis108/109: fresh period388946.361/samples1 обе станции, history_samples1,
productionwaitingresources наKMT485, globaltrade_restricted1, provisionnull.
Новые UI subordinate summary ещё требуют живого read-back и не закрывают полную
оценку или throughput. По-прежнему8/32; release unqualified.
