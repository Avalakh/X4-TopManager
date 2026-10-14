# Актуальное состояние 13.10.2026: выпуск v2 квалифицирован

Change `assign-idle-empire-ships` завершён: свободные торговые, добывающие и разведывательные корабли получают ограниченные штатные задачи с сохранением ручных и приоритетных приказов. Короткие игровые сценарии и итоговый 20-минутный прогон приняты; свидетельства — `idle-ships-v2-acceptance-20261013.md`. Архив `dist/tm_empire_management-v2.zip` содержит 51 файл и совпадает с установленной копией; SHA и признаки выпуска — в `dist/tm_empire_management-v2.manifest.json`. Диагностическое расширение оставлено отдельно по просьбе пользователя.

## История квалификации v1

# Актуальное состояние 13.10.2026: 32/32, выпуск квалифицирован

Предыдущие записи ниже описывают историю разработки и прогона; актуальная приёмка — в `final-acceptance-20261013.md` и `release-acceptance-matrix-20261013.md`. Финальный p-прогон завершён: 7205 секунд/121 наблюдение, checkpoint032 физически проверен и реально загружен после чистой установки. Устойчивые ID управляющего, менеджера станции, капитана, заказа и оплат совпали; три вкладки прочитаны. Чистый запуск только с производственным модом был проверен; затем по просьбе пользователя `tm_empire_diagnostics` восстановлено для дальнейшей отладки (11 файлов, исправлен `domain_probe.xml`), X4 запущен через Steam с обоими расширениями. 32/32 задач приняты; архив, manifest, инструкция, release notes и строгая OpenSpec-проверка завершены. Старое сообщение о текущем pipe owner96914, несозданном save032 и запущенном V2 ниже уже не является текущим состоянием.

---
# Текущее13.10: заключительный прогон p запущен, один владелец pipe

УТОЧНЕНИЕ p007–009: purchase12/id56223 после промежуточного cancelled из006 завершился без новой покупки в403149.538 (+15 игровых секунд); UFP-742, accepted1/currentManager1/одинRecon/samegoal1, Pendingnull, Lua reconciled/paid1699493. Баланс006→007 одинаков35286793. Новый purchase12-cancel-then-built-sequence-20261013.json хранит SHA/последовательность. Это не подтверждённый постоянный отменённый заказ: прежний план править Pending по одному006 отозван, source/install НЕ менялись. docs/final-p-issues-20261013.md уточнён; точная причина внутреннего перехода/refund не заявляется. Прогон96914 остаётся единственным владельцем pipe. verify-save032-final-p-20261013.py подготовлен, py_compile PASS; ещё НЕ исполнен (слот032 не создан).

Новый локальный случай p006: purchase12_403044.514 paid1699493/id56223, Completion cancelled/native_build_cancelled observed403134.531, но Pending building. Причина native cancellation/refund не установлена; не выдавать его за бесплатную/повторную оплату. Source CancelledBuild→Observation cancelled, CompletePurchase→Delivery cancelled, Pending обновляется лишь для delivered; Runtime status читает Pending. Документ docs/final-p-issues-20261013.md. Source/install пока НЕ изменены: collector продолжает независимые сценарии. После terminal необходимо исправить достоверность публикации отмены и проверить расчёты/границы повторов; старый p не квалифицировать по одному времени.

Подготовлены, но НЕ исполнены clean-install-current-p-20261013.py и post-full-p-checkpoint-20261013.py в том же run-каталоге. Оба требуют summary state collection_finished/elapsed≥7200; clean также требует закрытую X4 и точное соответствие собственного content ID/51 SHA/состава. Clean перемещает только прежнюю собственную папку расширения в run-каталог вне игры и устанавливает архив с проверкой, сохраняет обратимость; чужие папки не изменяет. Post-full выполняет семь read-back, проверяет текущую p/active и сохраняет в новый032 лишь после физической проверки отсутствия всех четырёх вариантов файла; slot032 заранее не считается созданным. Синтаксис обоих скриптов PASS. После сохранения032 потребуется отдельная gzipCRC/SHA/identity проверка: старый verifier CLI ограничен028–031 и для032 ещё не адаптирован. Последнее write_stdin96914/55s подтвердило live; functions cell1840 terminal только для ожидания, collector96914 НЕ завершён.

Collector unified session96914, X4 PID135444/path проверен; autonomy-final-p-20261013,120min/interval60s/domains. Первый полный sample записан. НЕ открывать параллельный role/menu pipe, не устанавливать/загружать/сохранять/перезапускать пока collector live. functions cell1831 завершён и вернул session96914; для наблюдения использовать write_stdin96914 до terminal, timeout не завершает работу. Текущий archive current-p-candidate-20261013.zip SHA55c6f1e0460ee9dcb17dfd36444ade6990aef7599f57e1d24d98e87f5d369eb2,51 production файлов; installed parity PASS. Общая source/fixtures проверка PASS:14 действующих Lua, retired trade-choice SKIP,9 Python,5 check tools. Подробный аудит предыдущего2h и текущего кандидата docs/autonomy-domain-review-20261013.md. Документы/release notes обновлены; все6.1/6.4/6.6 остаются открыты. После штатного terminal≥7200s проверить новые квитанции/ошибки/общие границы, затем clean install/reopen и выпуск. Не считать старый ZIP или прежние события приёмкой текущего кандидата.

# История13.10: короткая проверка p завершена, сохранение031 проверено

Controller55892 terminal exit0; установленная production51 и diagnostic p11 завершили реальную поставку supply_5_402355.355: YDU-207, paid5392 Cr, stock0→1, consumed/completed, orders0/claimnull. Первичная запись load029-p-supply-refresh-short-20261013.json; промежуточный пересчёт котировки после стыковки отдельно не наблюдался. save031 gzipCRC PASS, size90796566, SHA748732e534ade86994ced8567401579430b909822586930a010a0dfeb61cd6fc, оба Control сохранены. Новая приёмка docs/supply-boundaries-acceptance-20261013.md. check_md_scheduling и четыре fixtures (supply payment, station funding, player order guards, empire status) PASS. Единого активного pipe нет; X4 может оставаться запущена, PID перед следующей операцией проверять заново. Производственные исправления runtime/supply/purchase_dispatch/empire_status установлены; старый ZIP V2 не представляет текущий source. 29/32: общая приёмка6.1, квалификация двухчасового прогона6.4 и выпуск6.6 остаются открыты. Следующее: свести общий аудит реальных доменов/регрессий и подготовить свежий пакет, не повторять уже принятые отдельные проверки штатного AI.

Ниже исторические записи предыдущих итераций; их source-only/live статусы не описывают текущее состояние.

# История13.10: full V2 завершён; диагностический k загружен из028

Короткая supply o PASS для нового docked quote: PID97536, controller63337 terminal exit0; load030-o-supply-short-20261013.json exact030/versiono. Quote6_402536.391 price5068, paid5068/native build_recorded, shipYDU-207 stock0→1, native Equip ready→critical→completed; consumed outcome completed/reason native_supply_delivery_observed/claimnull/orders0. Funding8 observed retained. Это настоящая новая оплата/инвентарь, не free result. Непосредственные repriced/available поля в failure branch не заполнились, потому что fresh quote успешно оплачен; НЕ выдавать это за измерение цены в момент предыдущего отказа5. Current ship has paid satellite1, но этот результат ещё не checkpoint; base030 содержит только docked failed5 и paid funding8.

save030 protected receipt: size90989038/mtime_ns1791866024373528600/SHA11bcc5ec935f48b03b2549aca2dc9aa4bb79f2260d52f72f0c1596805d4e14ab; CRC/marker/funding8 PASSED. Source-only дальнейшая доработка: QuoteRestock сохраняет quote_docked, StepRestockDelivery один раз повторно рассчитывает quote на реальном supplier после arrival ДО payment intent, identity/key/wares/budget сохраняются; ужесуществующий payment samekey переводит unknown без повторного effect. Lua reprice/price equality/budget guards неизменны. XML parse PASS, эти MD/UI source изменения ещё НЕ installed. Нужен короткий путь от029 через travel/docking→refresh→actual paid/inventory. Для новых checkpoints текущий diagnostic o поддерживает только030; перед следующей установкой расширить безопасные новые slots031–039, не перезаписывать030. Активного pipe нет; текущая оплаченная supply6 world X4 остаётся live.

Native DockAt граница исправлена и положительно проверена n: текущие packed order.dock.wait.xml357–371 создают DockAt с dockandwaitid=точный Parent, refs/MD5/SHA в dock-boundary-references-20261013/receipt.json; GalaxyTrader overlay только TradePerform failurehandling, originals не менялись. CanUseOwnedShip теперь записывает child через существующий RecordOwnedOrder только если точный живой owned Parent DockAndWait, sameShip/destination/script order.dock, ни parent ни child не override/priority. Installed51+diagnostic n11, PID158388, controller85893 terminal exit0; load029-n-supply-short-20261013.json подтверждает child0x8786→parent0x8785, recorded0→1, parent_recorded1/destinationmatch1; critical docking не прервано, ship реально docked. Quote5_402355.359 price5392; дальше payment_rejected/supply_price_or_budget_changed, paid5 отсутствует/stock0, consumed exact outcome/reason/claimnull, old funding8 observed retained. Это НЕ положительная поставка спутника. Next: точные quoted/currentprice/budget values перед отказом или новый quote для уже docked ship, не ослаблять reprice/identity guards. Активного pipe нет. Проверенный paid base029 сохранён; docked/currentfailedprobe ещё не checkpoint. Free030. Исторические строки ниже source-only/UI ещёнеinstalled устарели: эти source UI и точные MD reason уже installed.

Новая short supply m: installed51 (float funding + original reason preservation + granular quote refusal), installed diagnostic m11. PID172268; controller15777 terminal exit0; exact029 load accepted/versionm. Native quote5_402355.342 YDU-207 price5392, native DockAndWait order0x8946 создан/recorded1, но ship.orders2. Следующий Step отказал existing_orders ДО оплаты; original reason сохранялся отдельно от releasereason=owned_orders_stopping, затем consumed outcome=rejected_before_effect/claimnull/orders0/ship реально docked/stock0. Paid funding8 reconciled retained. Первичный load029-m-supply-short-20261013.json. Это доказанная очередь unrecorded второго приказа после DockAndWait; происхождение второго ещё НЕ установлено. Нельзя разрешать любой unrecorded order, нужен exact native child provenance/guard. Активного pipe нет. Source UI переводы двух новых причин добавлены ПОСЛЕ установки — UI source/installed отличаются, новые строки ещё не installed. Диагностическая подготовка бесплатно перемещала свободный корабль к тому же поставщику; спутники/результат НЕ добавляла. Сохранение029 остаётся оплаченной protected базой; текущее docked тестовое состояние ещё не сохранено. Следующий free030.

Оплата сохранена029: paid-budget-checkpoint029-20261013.json read MD observed8, native save requested overwritefalse; save029-post-full-checkpoint-20261013.json CRC/marker/key/SHA PASS, size90799391/mtime_ns1791864947479023200/sha256 d481df5d792549294e3826910a4bdd6d3c36958c48e717a8cb3fe38f63a2b8b1. Теперь следующий restart/load использовать029, чтобы сохранить реальный оплаченный результат. Следующий свободный slot030. Нет активного pipe. Source-only уточнение ReadRestockQuote reason ещё не installed; диагностика l текущая. Новая короткая supply проба должна запускать обычную QuoteRestock/StepRestockDelivery с точными текущими Ship/Builder/Manager, а не подменять outcome. Общий120minV2 terminal не квалифицирует новый supply source.

Повторная игровая проверка float-формулы PASS: controller48652 terminal exit0, load028-l-budget-repeat-20261013.json, diagnostic l. funding8_402266.623 paid846330 Cr: player37834492→36988162, station638413→1484743; Lua reconciled/MD observed. После15s и native economy run402271.188 key тот же, повторной оплаты нет. Новый docs/fractional-station-budget-acceptance-20261013.md. Installed51 содержит правильную float-формулу и сохранение release reason. Последующее source-only уточнение ReadRestockQuote reason (корабль/поставщик/инвентарь вместо общего supply_asset_or_inventory_changed) ещё НЕ установлено. Живого pipe больше нет, текущая X4 после успешной оплаты остаётся запущена; PID повторно проверить перед закрытием. Перед следующей установкой сохранить оплаченный мир029, не откатывать подтверждённый платёж молча к028.

Адресный тест l: installed51 + diagnostic l11, PID175500, controller9076 terminal exit0. Exact028 load accepted; station_budget_retry8 и последующий autonomous9 отклонены ДО оплаты. Live wanted MD1484742 vs Lua1484743 при одинаковом balance638413: integer division `/1Cr` отбросила fractional part ДО +0.5. Source Wanted исправлен на явные float casts обеих величин `((productionmoney)f/(1Cr)f+0.5)i*1Cr`; повторная игровая проверка ещё обязательна. Не принимать предыдущий fix как работающий. Source/installed снова отличаются одной формулой. Supply request4 quote_ready/price5309, old payment1 consumed/paid6118: первоначальный отказ supply4 возник после quote, а не quote_failed; точный новый MD outcome ещё нужен.

Последующее source-only исправление tm_empire_supply.xml: Wanted=((productionmoney/1Cr)+0.5)i*1Cr согласует MD quote/certificate со штатным whole-credit Lua recommended budget; integer cast i используется штатными FinaliseStations и описан Egosoft Mission Director Guide. ConsumeRestockResult сохраняет исходный reason, ожидание stop хранит в отдельном releasereason и убирает после освобождения claim. XML parse PASS; production install/runtime ещё V2, новый source НЕ принимается по старому двухчасовому тесту. Нужен короткий actual paid fractional-budget сценарий и новый supply outcome с сохранённой первопричиной; допуски Lua и guards не ослаблены.

Collector73196 terminal exit0: collection_finished,121 samples/7206.043725s,62 frozen installed files. post-full-v2-20261013.json подтвердил новые решения текущего интервала: factory creation398180.669, expansion construction2_398210.678 queued, plot1_398249.798 observed и construction funding1 observed, builder_hire2 arrived/deployed399690.18; новый captain transfer issued401944.569/observed401971.257 exact seed1948930943911742143, source_member0/intransit0/scheduled0. Это реальные новые развитие/кадры, не прежний Control build. Стройка ещё не completed; эти события не выдают все критерии выпуска за закрытые.

save028 CRC/marker/SHA проверены: size91498137/mtime_ns1791863839059212800, sha256 cbf1735cf80d738710bcec16da6705eaf5bea11e3d35a56849f4969c03b5e33a, оба Control ready. Старый PID72876 закрыт штатно. Diagnostic k11 installed/SHA, productionV2 не менялся. Новый PID182744; controller97923 terminal exit0, загрузка exact028 accepted, domain diagnostic_version20261013k подтверждён. Единого активного pipe сейчас нет.

Новая фактическая граница: Lua station_funding_observation wanted1484743 при request wanted1484742.5; currentbalance638413 отличается от исторического560225, поэтому текущий balance НЕ доказывает значение в момент отказа. Рассогласование округления recommended budget подтверждено, требуется согласовать quote/certificate и выполнить короткую реальную оплату. supply4_400834.683 outcome rejected_before_effect, shipYDU-207 exists/orders0/claimnull — owned_orders_stopping устаревшая причина, не текущая блокировка. Исходный отказ supply всё ещё неизвестен; не подменять его причиной освобождения.29/32,6.1/6.4/6.6 остаются открыты до аудита и исправлений.

# Текущее13.10: full V2 live97min; исходная причина отказа supply может теряться

Session73196 повторно подтверждён live через write_stdin; progress98 samples/5824.788513s. Это ещё не двухчасовой результат. Последний проверенный purchase10_399530.677/DKV-605 delivered/accepted1, current manager1, native_orders1/TradeRoutine. Исходный goal уже retired; его invalid не означает потерю принятого задания. Installed production V2 и diagnostics j не менялись.

Чтение текущего ConsumeRestockResult показало: при completed/rejected_before_effect вызов StopAndReleaseOwnedShip может перезаписать Receipt.reason значением owned_orders_stopping, затем это значение попадает в result после освобождения claim. Поэтому текущая строка НЕ доказывает первопричину первоначального отказа поставки. Gameplay не исправлялся по предположению. После terminal: сохранить текущий мир в свободный slot028 с preflight, установить подготовленный диагностический k и проверить точные receipt/claim/orders и Lua station budget values. Текущие значения не считать историческими значениями в момент отказа. 29/32; 6.1/6.4/6.6 открыты.

# Текущее13.10: full V2 live53min; новая военная покупка/Recon подтверждены

Session73196 вновь подтверждён live. В текущем full V2: purchase7_397920.862/VAS-154 delivered/accepted1 living Start; затем purchase8_398015.282/HYS-596 delivered. Первое Wait/orders0/acceptednull НЕ принималось за приказ. Raw052/053-role после native receiver: accepted1/goal_exists1/manager_current1; completion exact key/ship, native_orders1/current_orderRecon/same_goal1. Квитанция final-v2-native-recon-evidence-20261013.json со SHA первичных файлов. Это новая настоящая военная работа текущего интервала, не old PCS и не source-only.

Satellite deployed0/rejected consumed сowned_orders_stopping и кадровые hire/transfernull по-прежнему не положительный результат. Старый audit-final-interim incomplete native_fleet_periodic_work теперь устарел в отношении реальногоRecon; не объявлять весь fleet/supply закрытым. Остаются development/personnel interval ифинальное120min/clean acceptance.29/32 сохраняется; sourcek diagnostic НЕ установлен, active j/productionV2 не менять.

# Текущее13.10: full V2 live42min; diagnostic k SOURCE ONLY

Session73196 вновь live,43samples/2525.773s. Current installed diagnostic j иproduction51 НЕ изменены. Source diagnostic k подготовлен: Lua station_funding_observation current money/productionmoney/owner/types; MD supply_claim_read exact receipt/ship/dock/claim/stoprequested/orders и максимум8 supply_owned_order handles/state/queue/override/priority. XML parse иLua syntax PASS, live read-back ещё НЕ выполнен. Не считать sourcek установленным по versionстроке; install только после terminal collector. Производственная логика остановки/денег/снабжения не менялась.

purchase6_397303.67 building при отдельном rejected/consumed supply3. Новая независимая экономика работает; это не положительная поставка спутника/кадры.29/32,6.1/6.4/6.6 остаются открыты.

# Текущее13.10: общий V2 live37min, новая military supply3 отказана до эффекта

Session73196 вновь live;38samples/2225.136s. Raw037-role: native_deployables goal20/claimed2/satellites0, supply_key=supply_3_397235.917, reason=satellite_supply_rejected_before_effect: owned_orders_stopping; receipts supply=rejected_before_effect. Это реальная новая периодическая попытка native Manager, не успешная поставка/развёртывание. Эффект/деньги/новый satellite не принимать по одному key. Предыдущий отказ финансирования требует будущего actualLua наблюдения; source funding observation не установлен. Остальное29/32,6.1/6.4/6.6 открыты. Collector не останавливать из-за обычного локального отказа, не вводить конкурирующий pipe.

# Текущее13.10: общий прогон20min; funding observation SOURCE ONLY

Session73196 вновь live, completed21 samples/1204.954s. Новый economy_last_run396147.862 показывает второй стратегический цикл. station_funding1 и2 rejected_before_payment/station_production_quote_changed; wanted1484742.5, второй balance161019; повторного списания нет. Это НЕ доказанный rounding bug: request board не содержит actual Lua current wanted/balance в момент отказа.

Source tests/diagnostics/extension/ui/role_probe.lua добавлен read-only station_funding_observation: GetComponentData money/productionmoney/owner/types под pcall. Native Lua syntax PASS. НЕ INSTALLED: active diagnostics j/production51 не менять, source теперь отличается от frozen diagnostic по этому чтению. После terminal провести короткое чтение actual numeric boundary, при необходимости исправить только доказанную причину. Не выдавать текущие observed значения (когда появятся) за историческое время отказа.

29/32; полный прогон не принят. Ждать реальный terminal/7200s, не restart по timeout.

# Текущее13.10: V2 package parity PASS; общий прогон live

Session73196 вновь подтверждён live; последний completed progress8 samples/425.314s, ожидается120realmin. Новый интервал уже дал настоящую продажу61 siliconwafers (MZK-812→BOF-341, observed395278.406), назначение VSA-005/Кремний, новую purchase5_395143.928/building и последнюю delivered purchase4. Эти события принадлежат именно autonomy-final-v2-20261013, не прежнему общему тесту. final-v2-interim-evidence-20261013.json содержит SHA первичных продаж; домены development/fleet/personnel в новом интервале ещё не приняты.

final-v2-package-parity-20261013.json: ZIP51/manifest51/installed51 все SHA и перечни равны; diagnostics отсутствует. Archive SHA b35eed4b4c92b5e7970a5b6940c789686a785de17b07f0bfddf04b3516103db2. README/release-notes актуализированы именно к V2, qualified_release=false. Clean reinstall/reopen только ПОСЛЕ terminal полного collector; сейчас installed не менять.29/32 сохраняется, остаются6.1/6.4/6.6. Задача активна, не blocked.
# Текущее13.10:29/32, военные границы приняты

3.6 закрыта military-boundaries-acceptance-20261013.md и military-boundaries-review-20261013.json (actual unknown guard/SHA +51 installed SHA). PCS/возврат и6118Cr supply/load сверены с соответствующими ранее принятыми докладами. НовыйTVZ бой НЕ присвоен PCS. Единственный collector session73196 подтверждён live; autonomy-final-v2-20261013, X4PID72876. Прямых собственных MD ошибок в последних2000 строк debug.log не найдено. Остаются6.1/6.4/6.6; новый autonomous satellite selector ещё ожидается в общем прогоне. Native economy cadence15–20min, поэтому краткое отсутствие новой оценки не приписывать сбою. Strict OpenSpec PASS.

# Текущее 13.10: финальный общий V2 прогон запущен; 28/32

X4 PID72876 подтверждён через CIM. Единственный активный pipe owner — collect_autonomy.py, unified session73196, каталог .cache/tmp/station-boundary-20261011/autonomy-final-v2-20261013, запрос120min/interval60s/domains. Не запускать второй pipe, не менять installed files, не перезапускать игру пока контроллер активен. Длительность и результаты ещё НЕ приняты; qualified_release=false.

Diagnostic j целиком установлен до текущего запуска; production51 V2 неизменен. Контроллер35641 terminal0: actual unknown sector EvaluateSector accepted0, goals_before1/after1, effectsfalse. Native Report после подготовки территории claimed2/goals2. Созданы192 пустых hulls без приказов/персонала. Исторический context_unavailable surplus выяснен: отсутствовала MiningFixture после rollback027. Последующие два коротких контроллера terminal0 создали DJS-478/VSA-005 и buyerBOF-341/traderHUR-925,5000wafers; открыли реальную продажу и observerV4, без own orders/claims. Mining resources/trace пока отклонены: miner ещё не назначен станции, это не доказательство добычи. Старые domain acceptance остаются отдельными ранее принятыми доказательствами.

Native TVZ-752 уничтожил NCZ-179 (enemy hull0/lastattacker exact TVZ); без PCS claim/response эту новую сцену не принимать как PCS, прежний GMI226 PCS case отдельный. Остаются3.6/6.1/6.4/6.6. Следующее: наблюдать подтверждённый session73196, проверить реальные независимые события и ошибки; после terminal выполнить полный аудит и clean install/reopen/package qualification. Не закрывать criteria по heartbeat/времени.
# Текущее 13.10: 28/32; control/module roles/UI reopen принят

Controller68964 terminal0,7commands, current X4 PID139004. Verified027 load accepted, diagnostic i read real Control entry3/4 operational1/same_macro1. Binding exact employee0x4b030 отличается от stationmanager0x4b02d, manager_unchanged1, seed-9126173547698565463 unchanged. Native pages status29/2tables/23rows, empire123/4/18, stats186/2/86. 6.3 закрыт module-roles-ui-acceptance-20261013.md вместе с ранее принятыми appointment/change cases; governor_roles_read passed0/uninitialized fixture НЕ принят как новая смена. Source diagnostic pseudo fix теперь реально работает. Активных pipe клиентов нет.

Исследован единственный оставшийся direct log error DomainProbe.Execute291: nested relationto.{State.$Threat.$target.zone.policefaction} при отсутствующей test Threat. Source исправлен на внутренний @ и version20261013j; это ещё НЕ INSTALLED. Дополнительно native_deployables read-only строка показывает actual native networkgoal/claimed/stock/pendingreason/supplykey. Source XSD/scheduling+strict OpenSpec PASS; gameplay production V2/51 unchanged. Недостаток этих диагностических данных не приписывать gameplay и не считать нейтральный read роли passed0 ошибкой назначения.

Остаётся3.6/6.1/6.4/6.6. Next: одним согласованным restart установить diagnostic j, load immutable027 (два готовых Control) и подготовить пакет оставшейся автономной supply/unknown military/большой собственности через проверенные mod functions; final120realmin после коротких границ. Предыдущая территория/сбыт/mining из025 принадлежит иной rollback timeline; перед final world fixtures проверять actual State, не принимать старую receipt как новое событие. Текущий027 safe checkpoint, next028 с физическим/native preflight отсутствия, прежние не перезаписывать. Candidate V2 ZIP51 qualifiedfalse; полного прогонa пока нет.

# Текущее 13.10: 27/32; Control достроен, diagnostic i установлен

3.4 закрыт: control-module-build-acceptance-20261013.md. Actual expansion construction1_393644.616/build0xa9e2 observed394513.765; snapshot027CRC/SHA fdd80f8ee67f068db6a87a1ca1bd23fe5f04c5ba5383b579c96fe4bdb5c83e96, два готовых Control, в026 новый был stateconstruction. Next slot028. Все controllers39034/observation/completion027 terminal0, активных старых pipes нет.

X4 PID139260 штатно закрыт после success027; установлены исправленные diagnostics11/version20261013i, receipt construction-entry-i-diagnostics-20261013.json. Production V2/51 unchanged. Steam без дополнительных аргументов. Единственный новый controller-control-module-load027-20261013.py: load verified027, read/runtime/entries/roles + UI три страницы; source diagnostic pseudo entry fix проверяется live, прежние null rows не принимать. Дождаться terminal этого клиента, не запускать конкурирующий pipe.

Остаётся3.6/6.1/6.3/6.4/6.6. 6.3 закрыть только после свежих read-back/module roles/UI/reopen; 3.6 свести известные group/task/reason и remaining unknown/supply. Полный2h НЕ начат, release qualifiedfalse.

# Текущее 13.10: 26/32; новая обычная стройка Control подтверждена

Предыдущий turn progress: экономическая адаптация3.2 принята по сверенным первичным live квитанциям дефицит160/добыча980/сбыт61 и текущим known-market/owned guards; source51 совпал с installed. Документ economy-domain-acceptance-20261013.md, evidence economy-domain-evidence-review-20261013.json. 3.8 также принято: bounded-blocked-acceptance-20261013.md сводит18 проверенных raw SHA/10 snapshots, exact loss, независимую purchase2 accepted при blocked construction и exact unknown transfer после load013. Полный6.4 остаётся открыт. OpenSpec strict valid.

X4 PID139260. Controller81680 terminal0 load005→expansion_native_fixture: отрицательная предпосылка waiting_blueprints/required_blueprints_missing, никаких builder/funding/build. Controller39034 terminal0: blueprint подготовлен диагностически без покупки/списания; та же заявка construction_1_393644.616 consumed→native build0xa9e2, actual constructingmodule0x1aa05c/macro tm_empire_control_arg_macro. Материалы подготовлены construction_resources, paid_supply=false; оплаченный NPC builder_hire_1_393927.881/50000Cr поставлен штатным управляющим, domain_builder_position только подготовил его положение. Фактическое deployment observed393942.883; normal elapsed0→271.644/540. SETA использован коротко и штатно закончен factor1/ended, не перезапускать once helper. Read-only observation позже elapsed378.602/540, active тот же manager. Завершение пока НЕ принято.

Native save026 создан свободным и проверен stable/gzipCRC/SHA16932d687b4e32844e3673f593e63d9a53fdf0860ea3cda17db97cb04b876f2c. Сохранение содержит старый готовый Control entry3 и НОВЫЙ Control entry4/компонент stateconstruction; поэтому ordinary module building доказан непосредственно, не по старому демо-модулю. Прежние025 и005 неизменны. Следующий свободный слот027. Слоты008–010 старые сторонние пользовательские; только read008 metadata уже сделан, не изменять/не загружать.

Диагностика installed construction-entry-diagnostics-20261013.json выявила собственный пробел: constructionplanentrydata — pseudo, её нельзя присвоить переменной Entry/BaseEntry. Source исправлен на прямой .sequence.{index}.id/.macro (scriptproperties.xml1728); XSD/scheduling PASS. Дополнительно вложенный неизвестный Threat target внутри distanceto защищён @; source Domain diagnostic version20261013i. Эта коррекция ещё НЕ INSTALLED; installed h readentry даёт null и не принимается. Новая реальная стройка доказана отдельными native processor и saved026, без доверия ошибочным entry rows.

Активных pipe controllers нет; полный2h НЕ запущен. Не рестартовать ради ожидания: текущая стройка выполняется native. Следующее — read её настоящего completion и сохранить027; затем установить согласованный diagnostic i одним restart и load завершённого checkpoint. Подготовить общий остаток3.6/3.8, после функционала/коротких границ финальный120min. Production V2 unchanged/ZIP51 qualifiedfalse. Новые диагностические source изменения не меняют исходный gameplay package.

# Текущее 13.10: purchase reservation v2 проверен; checkpoint025

Controller69949 terminal0: 20 команд, exact purchase15 передан/accepted1, Lua reconciled по первоначальным id38111/1070000Cr. Read-back native_orders1/current_orderRecon/same_goal1. После native SaveGame025 gzipCRC/markers PASS; SHA fd2f76be1d03aaee5a8ab8c43e52a016c7a4321ee697c6ac0c7a4c9ce0a0d2ae. Независимый audit saved025 подтвердил одну owned/native Recon очередь, без второго приказа из024. Квитанции purchase-reservation-v2-evidence-review-20261013.json, save025-scenario-checkpoint-20261013.json, save025-paid-ship-audit-20261013.json. Следующий свободный слот026; прежние не перезаписывать.

Полный прогон не запущен, ченж24/32. Пакет purchase-reservation-v2-candidate-20261013.zip без diagnostics, qualified_release=false. Старые записи ниже исторические; controller69949 больше не активен. Продолжить оставшиеся границы строительства/снабжения/общей приёмки; нового pipe клиента запускать последовательно.

# Текущее 13.10: purchase reservation v2 INSTALLED; controller69949 live

Предыдущий goal turn — progress: source общий purchase handoff исправлен, установлено/проверено; получены реальные delivered/accepted/reconciled purchase15 и выявлен второй Recon приказ в saved024. 24/32, ченж ещё не принят. Полный120min прогон не начат; старый22258 stopped_by_request на23min.

**Единственный активный клиент:** controller-purchase-reservation-v2-load016-20261013.py, unified exec session69949. Не запускать другой pipe и не перезапускать игру до terminal. Steam без добавочных параметров. Nativeclose предыдущего X4 PID101932 выполнен. Новая установка51production+11diagnostics, receipts purchase-reservation-v2-install-20261013.json / purchase-reservation-v2-diagnostics-20261013.json. Контроллер загружает immutable016; затем12×10s read +domain/idle/UI, безSETA. Completion projection добавляет native_orders/current_order/same_goal.

**Исправление v2:** CanUseOwnedShip и ClaimOwnedShip имеют PurchaseKey defaultnull. Резерв exact native-ready hull теперь защищает от раннего приобретения всеми селекторами, даже первоначальным покупателем. Только DeliverCompletedShip передаёт текущий ключ. Recon/Defend receiver не повторяет add/strength/signal, если ship уже в native группе. Generator и generated2files согласованы; XSD/closure/scheduling PASS. Installed ещё нуждается в реальном read-back: delivered/accepted, same goal, native Recon queue1, unchanged original payment. Старая v1 purchase-reservation-candidate ZIP устарела после v2.

**Последний проверенный checkpoint024:** size93986931,mtime_ns1791851936001921100,SHA daf71e0d336ca95b47ad8ddeebeba4ad933863eef777bad6d4331e9af93fb2ec, gzipCRC/markersPASS. В нём purchase15 reconciled, но сохранён известный двойной Recon; это свидетельство бага, не окончательный baseline. Следующий слот025. 019/020 — старые пользовательские, не трогать. 015–018/021–024 не перезаписывать.

**Что уже подтверждено:** controller47267 terminal0,23commands, exact purchase15/UTT100/1070000Cr/id38111 → delivered/accepted1/claim_goal matches, Lua reconciled. Native builder180→300/1140 продолжал работу. SETA запросfactor6 автоматически отменился; endfactor1/ended подтверждён. Audit saved024 exact owned ship0x6690e, claimgoal759216, native Recon orders0x9077 и0x950f выявил повтор. См. purchase-load-identity-20261013.md и raw purchase-reservation-evidence-review-20261013.json (принимает передачу/платёж, не отсутствие повтора orders).

**Исследование строительства:** raw batch776 подтверждает обычную очередь construction1_393644.644, paid builder/handoff и native completion; архивная role_probe-before-retired-evaluation.xml содержит exact Control module generation, но её полный SHA не найден среди install receipts. Save012 содержит current factory construction2 и operational Control component (HQ), не прежнюю Request1. Save006/007 взяты до поздней rollback-проверки construction1 и НЕ содержат её vars; не использовать их как подтверждение macro этой очереди. 6.3 пока открыта, нужно завершить точное сопоставление или короткую новую ordinary module пробу. Не создавать большой новый diagnostic обход глобальной Expansion receipt без необходимости.

**Остальные критерии:** 3.2 deficit/sale/mining visibility; 3.4 ordinary development/all prerequisites; 3.6 group/task/reason/unknown threat/autonomous supply; 3.8 bounded/backoff/stall/loss;6.1 composite;6.3module+roles/UI;6.4actual≥7200s;6.6package/cleanreopen/strict. Final2h только после функционала/коротких границ. OpenSpec CLI работает с require_escalated; plain sandbox status ложно сообщает schema missing. Последний strict valid,24/32.

# Текущее 13.10: telemetry terminal; verified023

Telemetry controller session98052 завершён: receipt purchase-completion-telemetry-short-20261013.json содержит 7 команд; повторный stdin сообщает Unknown process id, новых клиентов нет. X4 PID105168 работает. CompletePurchase реально вызван:408616.744 waiting/manual_or_priority_order на exact UTT-100;408631.752 waiting/claimed_by_other_goal. Exact ship0x19fea ранее WaitForSignal+claim sent, позже native Recon+claim sent; это не пропавший корабль и не невызванный poll. Purchase15 остаётся ready, paid1070000/id38111 неизменны. Нельзя считать native Recon завершением исходной receipt или безусловно отбирать корабль у другой цели. Следующее — установить точную цель claim и источник раннего назначения, исправить общую границу доставки/распределения, сохранив manual/helm/unknown ограничения.

Native checkpoint023 создан в свободном слоте и проверен: size94066837,mtime_ns1791851330316423200,SHA4d10cc9a968ab8275b981b26e3c01993d0a2c54a25dfddb4d70100f2830cf4c9,uncompressed765873703,gzipCRC/markers PASS. Receipt save023-scenario-checkpoint-20261013.json. Следующий слот024. Установлены telemetry51+diag11; полный прогон не начат,24/32.

# Текущее 13.10: диагностика передачи, session98052

Короткий controller125960 завершён; receipt completed-purchase-delivery-short-20261013.json содержит 7 команд. На X4 PID108112 purchase15 остался ready: повторной оплаты нет, delivered/accepted не подтверждены. Delivery guard был установлен (completed-purchase-delivery-install-20261013.json); прежняя запись SOURCE ниже устарела.

Для точного диагноза CompletePurchase сохраняет последнее время/key/result вызова, без изменения решений и эффектов. Read-only диагностический read выводит purchase_completion. XSD и scheduling PASS. X4 PID108112 штатно закрыт; установлены 51 production + 11 diagnostics, receipts purchase-completion-telemetry-install-20261013.json и purchase-completion-telemetry-diagnostics-20261013.json. Steam запущен без дополнительных параметров. Единственный controller-completion-telemetry-load022-20261013.py работает в exec session98052: native load verified022, затем 4 коротких read. Не запускать конкурирующий pipe-клиент. Результат ещё не принят.

Checkpoint022 сохранён и неизменен; следующий свободный слот023. Старые019/020 не трогать. 24/32, полный двухчасовой прогон не начат; прежний23-минутный остановлен. После точного completion reason исправить первопричину всей цепочки, затем обычное строительство модуля и оставшиеся короткие сценарии.

# Текущее13.10: short68951 TERMINAL, verified022, delivery guard SOURCE

68951terminal0, load021v3accepted, paidpurchase15readyноНЕdelivered.
ВDeliverCompletedShip ещёбылnotTracked.Build? — пропущенныйвнутреннийguard.
ИсправленSOURCEдопускnativecertifiedready приtypedemptybuild; ObserveTracked
валидируетстрогийcertificateпередClaimOwnedShip. ВсеBuild?условиявpurchase
просмотрены; остальныеотносятсякpending/неоплаченной/новойстройке/eventlive
илиужеимеютreadyдопуск. XSD/schedulingPASS. Installedпокапредыдущийhandofffix.
Новыйcheckpoint022nativeсозданwithoutoverwrite,stableCRCmarkersverified:
size93950076,mtime_ns1791850694928595100,
SHA274e8af0d5c58dcc8c71ee3df1087e17a19994b591a349b378cdea0aa5a62f8c.
Receipt save022-scenario-checkpoint-20261013.json. СохранёнреальныйRecongoal
subtree purchase022-goal-subtree.xml: goal759105, PurchaseKey759112,
PurchasedShipObserved759113active. Нетактивныхcontroller, X4PID138436live.
Следующееinstalldeliveryguardвсейгруппой→nativeloadverified022, shortexact
purchase15handoff/reconcile/accepted/no duplicate; потомобычнаяmoduleстройка.
Final2hНЕначат,24/32. Candidateустарел; ченжнеприниматьпокаэтаграницанепройдёт.

# Live13.10: controller68951/load021v3 ACCEPTED

X4 PID138436 Respondingtrue CPU70.66. Native load021v3 accepted; exactreceipt
load021-completed-purchase-v3-20261013.json. Samecontroller68951ещёlive,
ждётrolepipe/worldready затем4×10sec read. Невторойclient/неrestart.
Completed-purchase-handoff-shortreceiptпокаещётребуется. Послеterminal
реальныйhandoff/accepted проверить, затемSETAboundedconstructionhelper
возможен: existingdomain_seta_begin guards playercontrolledown/active/notonce,
6xnativefactor и12mingameautoend. Не выставляетbuildprogress; обязательное
прочтениеactualfactor иEndfinally. Не считать этотhelper уже выполненным.

# Текущее13.10: handoff FIX INSTALLED, controller68951 live

3721 terminal0, exactpurchase15 unknown→ready/nativecompletedrecovered,
но не delivered. Причина2: четыреадаптированныхreceiver poll требовали
Tracked.Build?, сохранившийсяreadyeventсbuild0несчитался. Generator3templates
исправленBuild? OR Pending.ready; orphanreadyguard исправлен. ПроверкиPASS.
Production51новыйinstalled receipt completed-purchase-handoff-install-20261013.json.
X4 PID141232 штатноclose послеshort. SteamHiddenобычныйзапуск.
Единственныйcontroller68951: completed-purchase-load021-v3, receiptsloadv3
иcompleted-purchase-handoff-short; читатьтотжеhandleдоterminal, неsecondclient.
Diagsh/save-menu30сохранён. Verified021неизменён. ПредыдущийZIP79a226...
устарелпослеhandofffix; qualifiedreleaseНЕготов.24/32, final2hНЕначат.
Далее actualdelivered/claim/nativeorder/accepted exactpurchase15, ordinarymodule.

# Live13.10: load021v2 ACCEPTED, samecontroller3721

Native save list теперь содержит021, load receiptv2 accepted save021.
X4 PID141232 Respondingtrue CPU43+, bootprogressреален. Controller3721
ещёlive, перешёл кrolepipe/игровому read; shortreceipt покаотсутствует.
Это принятиеload, неготовностьмира/неpurchaseacceptance. Re-poll3721,
не второйclient. Production51completedpurchasefix/diagshsavemenu30.

# Текущее13.10: controller3721 load021v2 live, save-menu filter fixed

Прежний controller31620 TERMINAL exit1 ДО загрузки: save021 отсутствовал в
GetSaveList(diagnosticSaveFilenames), потому save_menu.lua for15..20 приh
roleprobe сохранял015..030. Это ошибкадиагностики, неотсутствиефайла/CRC.
load021-completed-purchase-20261013.json хранит failure list, load неотправлен.
save_menu source for15..30, остальные native/once/physicalguards сохранены.
X4 PID43124 был вmainmenu, штатноclose передdiagnosticinstall;
scenario-h-save-list-install-20261013.json11files. Production51 completedfix
не менялся. SteamHidden обычныйзапуск. Новыйединственный controller3721
controller-completed-purchase-load021-v2-20261013.py, receiptload021...v2.
Re-poll3721 доterminal, не запускать второйclient/неrestart. Actualload и
completedpurchase short всёещёнедоказаны. CandidateSHA79a2268abfe8b99d919d9e683f16b1818f957adb0038545a9ffe40401f6efa38,
qualifiedfalse. Verified021unchanged. Final2hне начат;24/32.

# Текущее13.10: completed-purchase FIX INSTALLED, controller31620 live

Verified021 stable/SHA передrestart. X4 PID50520 штатно Close/ExitTrue/True.
Установлен51production с completed-event recovery+market pending+militarysupport;
receipt completed-purchase-install-20261013.json. Diagnosticsh11 сохранён.
SteamHidden applaunch392160 бездополнительныхпараметров отправлен.
Единственный controller31620: controller-completed-purchase-load021-20261013.py,
load021 native save-menu, затем versionh/read4×10s/idle/ui read-only.
Pipe owner только31620; re-pollтотжеhandle, не запускать competing client.
НовыйPID/boot/load/actualpurchase15 recovery ещёнеприняты; request не результат.
Final2h НЕ начат. Candidate прежнийустарел.24/32 ещёоткрыты8.

# Текущее13.10: purchase completed-event FIX SOURCE

Сравнение018/021: Observation ready/native_built_event +paid107000000 и
exact ownship0x6690d→remapped0x19d54 сохраняется; Build0x28e6→typed0.
Причинаunknown: recovery пытается TrackBuild заново после завершения.
SOURCE purchaseXML добавляет ValidateCompletedPurchaseCertificate и путь
ready до проверки отсутствующегоbuild; exact receipt/candidate/event/ship,
безпохожихкораблей/новойоплаты. XSD/cue/closure PASS; НЕ INSTALLED.
Installed51marketfix/diagsh11, PID50520 live. Нетактивныхcontrollers.
Verified021latest. Следующее штатный restart/installpurchasefix/load021
и короткий точный purchase15 reconcile/handoff/no replay read. Затем
ordinarymodulepath +прочиеграницы. Final2hещёнезапущен,24/32.

# Дополнение13.10: purchase15 saved audit

Нет активных controllers. Новый документpurchase-load-identity-20261013.md.
Decoded021 submission41668 built/keypurchase15/id38111/paid1070000,
match39424 candidateindex1; candidate list4247→table39064 buildtyped[0x0].
Match_reasonbuild_id_mismatch/candidateid0. Live unknown безновогоэффекта.
Следующее ReadTracked Observation/BuiltShip receipt и исходный018 exact
queue/build refs, а не подборкорабляпоmacroprice. PID50520 liveпоследняяпроверка.

# Текущее13.10: short h TERMINAL, новый verified021

X4 PID50520 Respondingtrue. Единственный short controller13527 terminal exit0;
market-h-short-20261013.json7commands: domainh/read/native_analysis/3reads/provision.
Current direct mod script errors0; экономические last_run408307.617→408486.163
→408502.786, native стройка361.812→407.125/1140. Прежний invalidreturn исчез.
Pending ветка принудительно не моделировалась; deferred13 может быть сохранённым
счётчиком. Полную live-приёмку pending только по этому счётчику не заявлять.
Evidence market-h-evidence-review-20261013.json, qualifiedfalse.
После load018 purchase15_408301.653 building→unknown, submissionbuilt;
recovery purchase_effect_requires_reconciliation, повтор не создаётся.
Нужен exact saved native queue/ship audit, не подменять неизвестность успехом.
Новый native checkpoint021 requested безoverwrite и VERIFIED:
size93903756, mtime_ns1791849713120191200,
SHAf20b8438d5c871457cd3c59d3cf68d596552de98e0d7cc56f6be28240bb45144,
CRC/stable/markers PASS, save021-scenario-checkpoint-20261013.json.
Нет активного pipe controller. Следующийprotectedslot022 приabsence;
следующийrestart толькоverified021/новее. Installed51marketfix/diagsh11.
Final2h НЕ начат;24/32остаются. Далее unknownpurchase saved audit +обычная
module стройка послеglobalexpansionobserved; активнаяподготовкаусловийразрешена.

# Текущее13.10: load018-h accepted, short h стартует

Save-menu controller38220 terminal exit0; load018-h-20261013.json содержит
native accepted save018. X4 PID50520 Respondingtrue CPU53.84 при принятии.
Следующий единственный owner controller-market-h-short-20261013.py:
versionh read → native_analysis один раз →3×15s reads +provision.
Скрипт prepared и теперь запускается; точный execsession в текущем output.
Не запускать второй client/не менять installed до terminal короткого пакета.
Save021 controller/verifier готовы, ещё не исполнялись; physical/native
absence иonce guards обязательны. Final2h НЕ начат на исправленной версии.

# LIVE handoff13.10: X4 PID50520, load018-h controller38220

PID50520 boot жив, CPU растёт. Единственный активный pipe owner
controller-load018-h-20261013.py/session38220, native save-menu connection.
Повторно проверен38220 live; пока не запускать второй client/не restart.
Load receipt load018-h-20261013.json появится terminal; сначала re-poll38220.
Ни отправленный boot, ни connection waiting не доказывают native load.

# Текущее состояние13.10: market pending FIX INSTALLED, Steam launch sent

Collector22258 terminal exit0/stopped_by_request23samples1375.12s, НЕ full2h.
Checkpoint018 повторно SHA/stable/CRC verified. Ответа quicksave не было;
выбран уже разрешённый018. X4 PID129544 штатно CloseMainWindow/WaitForExit
True/True. Production51 с economy pendingfix установлен; receipt
market-pending-install-20261013.json. Diagnosticsh11 установлен; receipt
scenario-h-install-20261013.json. h поддерживает защищённые slots015–030,
021 следующий если физически/native свободен;019/020 старые чужие не трогать.
Lua5.1 syntax h PASS; XML/scheduling/closure PASS. Steam applaunch392160
Hidden отправлен без дополнительных параметров. Новый PID/boot/load018
ещё требуется подтвердить; не считать отправленный запуск загрузкой.
Следующее: native save-menu load018, domain versionh read; короткий пакет
market pending и дальнейшая ordinarymodule стройка. Source economy теперь
совпадает с установкой, старый candidate supportfix устарел. Live acceptance
исправления и final2h ещё не пройдены.

# Текущее состояние13.10: collector22258 TERMINAL, sourcefix ждёт установки

stop.request штатно завершил collector22258 exit0: stopped_by_request,
23samples/1375.12098s. Это НЕ2h acceptance. Причина — подтверждённый
invalid cue return в economy1041; исправлено SOURCE, gamefiles прежние.
Дальше новый checkpoint и установка economyfix с группой необходимых границ,
короткая проверка market pending/ordinary module build перед новым finalfull.
Первый checkpoint019 controller остановился ДО pipe/effect: физический
save019 уже существует. НЕ перезаписывать019. Проверить свободный020;
если занят, добавить отдельный свободный native slot через diagnostic guard.
Ни save019, ни gamefiles этим controller не изменены. X4 PID129544 жив.

# Дополнение13.10: market pending исправлен SOURCE, не installed

Collector22258 подтверждён live; PID129544 жив. Установка остаётся frozen
supportfix51/diagnosticsg11, прежний кандидат не включает следующую правку.
Current debug.log выявил cue return в economy1041 (408303.55 startup).
Generator исправлен: pending ставит TM_SectorMarketPending и break ware loop;
TableRefIndex/завершение report guarded not pending, штатный reset в конце
сохранён. При retry уже обработанные товары пропускаются по прежнему cache.
Сгенерированы13scripts; единственный source/install delta — economy XML.
XSD/cue scheduling/closure guards PASS; live market-pending acceptance ЕЩЁ НЕТ.
Установить вместе с прочими итоговыми исправлениями после terminal collector,
не менять gamefiles/не запускать конкурирующий pipe сейчас. Текущий fullrun
собирает независимые свидетельства, не final release gate исправленного пакета.

# Текущее состояние — 13.10.2026: общий 120min прогон/session22258 live

X4 PID129544 Respondingtrue. g controller34772 terminal exit0; finalread terminal0.
Единственный pipeowner теперь collect_autonomy.py/session22258, каталог
.cache/tmp/station-boundary-20261011/autonomy-military-support-20261013,
--minutes120 --interval60 --domains. Первый набор role/provision/domain real,
progress1/6.238s, позже4/184.625s; handle22258 live перепроверен.
До terminal не запускать другие pipe clients/не перезапускать игру/не менять
установленный пакет. Collector фиксирует все51production+11diagnostic SHA,
PID/creationtime; выполняет только чтения и не квалифицирует релиз сам.
Production supportfix51 и diagnosticsg11 установлены, manifest актуален.
Новый candidate military-support-candidate-20261013.zip SHA
3e556b40fdf9de5ef85486e2e7ba42984722f6384de7ebe055fd251ccbad8383,
qualifiedfalse; старыйcandidatev3 устарел.
Verified018: size93973854, mtime_ns1791847548700417000,
SHAcade163c3cb36647feb27b4c320bfbd6893cc30e9c8ac0c33b63fe39fd8ae240,
receipt save018-scenario-checkpoint-20261013.json. НЕ перезаписывать018;
следующийcheckpoint019 послепрогона, restartтольковverified018/новее.
GMI-226 ship0x9ca6 realRecon→ProtectShip/ProtectPosition→Attack;
PCS group1/orders2–4 confirmed1/complete1 с support_origin. Actual hit
observed408791.248 manager_matches1/confirmed1/complete1; YVQhull0/shield0.
Retireg при cycle4 былdeclined response0; collector не убивал enemy.
ПозжеGMI тотже0x9ca6 Recon/queue1/support_originnull/claimsent, goals5→4:
настоящий возврат наблюдён. Подробноmilitary-support-boundary doc.
MZK freshpickup61 observed409026.57, cargo61 DockAt destinationANT387;
actualsale ещёnull. Не принимать доevent. Factorynativeстройкапродолжается.
Функциональные исправления собраны и короткие новые границы проверены;
последующие боевойконец/сбыт/стройка наблюдаются вместе, не ожиданиеоднойфункции.
24/32;2hещёнезавершены; module ordinarybuild потребуетсяпослеFactoryobserved.
Native expansionfixture issuednull, нельзяпосылатьприglobalexpansionqueued.
Следующее: ждатьтотже22258 и читатьновыефайлы, агрегироватьошибкибезвторогоowner;
после terminal read/checkpoint019/приёмка и ordinarymodule path по предпосылкам.

# Текущее состояние — 13.10.2026: g controller34772 live, production support fix installed

Штатный close185096/WaitForExit PASS. Новая production51 установлена SHA,
receipt military-support-install-20261013.json; источник/установка совпадают.
Изменены ровноRuntime+PCS (source delta receipt). LIVE после boot будет supportfix;
не считать runtime загрузившимся до versiong read. Diagnosticsg11 установлены,
scenario-g-install-20261013.json. Source/XSD/cues/closure/Lua PASS.
Единственный controller/session34772 controller-scenario-g-load016-20261013.py:
verified016 → sourcegversion → surplus_watchV4/buyer_support/threat_distress →
6×30s readings → retiretestenemy (guard response_count>0) → new018.
До terminal не запускать другой pipeowner/не рестартовать игру.
Rollback016 выбран потому, что nativePCS failedgoal уже complete в017;
сохранили verified017/CRC/SHA c96bf8af8155e09b16b7a0ad8a7a94e913994b8e557d762d6ac96a3a65efd5ff,
size93911799,mtime_ns1791846674703000400. Слоты015/016/017 не перезаписывать.
Реальная ошибкаf: PCS classified own military ship claimed_by_other_goal,
newgoal774759/Orders124705empty/string128135. Подробноmilitary-support-boundary doc.
ОтдельноfNPCsupport НЕ был исполнен: несуществующееBuyer.manager; posts017
по корректному полному component толькоmanager/accountsnone. Вg guard исправлен.
SaleV3 не могработать: engine требовал space/seller/buyer, а conditionwareonly.
Вg добавлен selector иfreshV4. Значит old sale_null не доказывает отказ торговли.
Candidate ZIP прежний v3 устарел послеproductionfix; rebuildпослепроверки.
24/32; full2h пока НЕ начат. Следующее: terminal34772/read/evidence,
verified018, PCS ownorders/return, actual native sale; затем combined2h только
после короткихграниц. Не повторять длительные ожидания радиоднойфункции.

# Текущее состояние — 13.10.2026: scenario f controller63917 live

PID20724 штатно закрыт, diagnostics f установлен11/SHA: scenario-f-install-20261013.json.
Steam без новыхflags → X4 PID185096 boot. Единственный pipeowner/session63917
controller-scenario-f-load016-20261013.py: проверенный016 → versionf → buyer_support
и threat_distress → four30sreads/UI → protected017. Не создавать competing client.
NPC fixture support повторяет scenario_advanced initializer managerexisting,
missingdefence и 10000000Cr отNPCArgon; owncredits/cargo/prices/orders не меняются.
Distress только exactscene hits>0/knownrealenemy/relation/native galaxy signal;
сам сигнал подготовка, responsecounts/ownedorders должны читаться отдельно.
MD XSD/cues/Lua PASS. Production51/v3 не изменён. 24/32, full2h не начат.
Finale-read до close: BJV уже nativeAttack после10HP (самозащита), hits1/responses0,
PCS master1/local2 со старымvictimZKI. Large191живой, snapshot287: необходимо
разделить новыйpaidship+1/утрату1, не трактовать count287 как провал удаления.
Factoryelapsed274/1140, paidpurchase15built; rollback016 сознательно тестовый.
Последний безопасныйcheckpoint016; не перезаписывать016/015.

# Текущее состояние — 13.10.2026: scenario e terminal0, verified016

Controller19851 terminal exit0; активного pipe client нет. X4 PID20724 live.
LIVE diagnostics e11/SHA scenario-e-install-20261013.json; production51/v3.
verified015 реально загружен, затем short120s: provoke10HP incoming один native
attackevent/hits1, собственных militaryresponses0. Не принимать3.6.
LargeAssets living192→191 после удаления пустого ZXU783. Session11 resetscan;
firstsnapshot287/to408222.387 (включает async переход), nextfrom408282.445 +1min,
partial128/cursor124. Нужно следующее завершённое чтение, не закрывать3.8 ещё.
Factoryelapsed57→178/1140, nativebuilder/budget/materials продолжаются.
Purchase15 building native; продажи пока нет. UIstatus отработал.
NativeSave016 requested nooverwrite; stableCRC/SHA PASS:
e6b27620e96515c2a933b08fb0b14c3516bc3ade446eab3ee7f804708ccde92a,
size93822353,mtime_ns1791846236887171600. Receipt save016-scenario-checkpoint-20261013.json.
Слот016 НЕ перезаписывать, следующий017; будущий restart толькоverified016.
NPCbuyerNKU508 save015 имеет manager, нет defence; SMdockingbay есть.
Native scenario_advanced с тем же планом создаёт manager+defence+NPCbudget.
Но причинность cannotdock пока не доказана: production provision не менять
по догадке. PCS слушает galaxy ship_in_distress/station_under_attack, а не
сырой event_object_attacked; native interrupt.attacked требует noncomputer/
policefaction/relation для помощи. Следующее: exacttarget pilot/signal/zone,
nativePCS master/local read; по необходимости подготовить штатный distress
без собственных combatorders. Не повторять произвольные ожидания.
24/32; полный2h ещё не запущен. История ниже.

# Текущее состояние — 13.10.2026: scenario e запущен

X4 PID102152 штатно закрыт, WaitForExit PASS. Diagnostics e установлен11/SHA,
receipt scenario-e-install-20261013.json. Steam без добавочных параметров.
Единственный live controller/session19851: controller-scenario-e-load015-20261013.py.
Проверяет SHA/CRC/stable015, загружает015, выполняет короткий threat_provoke10HP,
large_asset_loss192bare и market/read, затем защищённый новый016.
До завершения controller не запускать другой pipe owner, не перезапускать игру.
MDXSD/scheduling/Lua PASS. Production51/v3 без изменений. 24/32.
Пользователь сообщил «сохранил», но новый quicksave не найден: старый12.10.
Использован уже проверенный015 по действующему разрешению тестовых откатов.
Market d: buyer37871wafers@419, source5429@326.2: спрос/прибыль реальны.
MZK812 nativeDockAt cannotdock=1 destinationNKU508; причина ещё не доказана.
Не менять provision/vanilla AI на основании этой догадки.

# Текущее состояние — 13.10.2026: scenario d terminal0, verified015

Controller73448 terminal exit0; NativeSave15 requested → файл stable/CRC/SHA
подтверждён, save015-scenario-checkpoint-20261013.json. Size93809546,
SHA1f2a206834e98d968e378a0efa60c17346f57a970699f887815626dfb9d7ff13.
X4 PID102152 live после short; новых pipe clients нет. LIVE diagnosticsd11,
scenario-d-install-20261013.json. Source теперьe, ещё НЕ установлен.
Большая империя: created192barehulls, total287, session10; sourcecursor188/
partial192 → snapshot287/to408102.294; следующаяfrom408162.343 ровно+1min,
cursor124/partial128. Не полныйrefresh каждыйtick. UIbody121rows работает.
Legacy11 согласован после rollback, native12_408067.604 building→delivered;
13waitingpricechanged, без повторного12. Builder native arrival+elapsed56
наблюдён; остальноеfinishне принимаем. MiningTrace вновь armed, после014
прошлый980 не переносится в currentstate. Surplusopen/watchV3 заново.
MilitaryScene YVQ-400/targetBJV geometry исправлена, ноhits0/responses0 за120s.
Saved15проверил2рабочихxenonlaser, реальныйNPCattack/fighterAI, dmg result0 и
useforwardweaponsfalse в snapshot; НЕ объявлять навсегда сломанным vanillaAI.
Не принимать военную функцию по такой неподготовленной угрозе.
Sourcee добавляет exactscene threat_provoke: incoming10HP через native
apply_attackstrength от реальногоXenon, толькоtestprep; ownorders/damageout
неподставляются. Отдельная loss192emptyownedhull с guardsHelm/pilot/commander/
claim/idle. Responsewatch bounded16 уникальныхship/goal, самозащита отдельно.
Checkpoint helper теперь допускает только015–020, физическийclientpreflight+
nativeabsence+once permarker сохранены; слот015 сохранён/неперезаписывать.
MDXSD/cue/Lua проверкиe PASS передпоследнейexplicitparentguard; повторитьXSD.
Следующее: sourceXSDe → штатный close102152 → installdiagfreshreceipt →Steam
→ verified015load (НЕ014, неоткатыватьbulk) → shortprovoke/assetloss/read →save016.
24/32;3.8 всё ещё требуетbackoff/stall/loss evidence,3.6непринят, full2hненачат.
История ниже.

# Текущее состояние — 13.10.2026: scenario d controller73448 активен

PID77408 штатно закрыт WaitForExitPASS. diagnosticsd установлен11/SHA,
receipt scenario-d-install-20261013.json. Steam без новыхflags запустил
X4 PID102152 (boot/loading, Respondingfalse не считать падением).
Один live controller/session73448: controller-scenario-d-load014-20261013.py,
verified014 stat+SHA/CRC → native load → scenario-package-d короткий120s.
До terminal не создавать второй pipe owner и не перезапускать игру.
Использован ранее разрешённый откат testworld/любойsave014; отсутствие нового
quicksave не принято за ответ/согласие. Нативные чтения980silicon/стройка3модуля
до отката записаны; текущий мир должен читаться заново, futuredataне переносить.
Старый quicksave12.10 mtime не использован. Pending пользовательский вопрос
о сохранении уже не является blocker для разрешённого014 сценария.
Controller: read/versiond, mining_trace_arm, surplus_open/watch,
threat_range, large_assets192, четыре30sreads, UI, protectedslot015.
Контроль015 ещё НЕ записан/принят; sourceprepareне означаетeffects.
Source/MDXSD/cues/Lua/OpenSpec strict PASS. Production без новыхизменений,
24/32, full2h не начат. История ниже.

# Текущее состояние — 13.10.2026: реальная доставка кремния подтверждена

Host X4 PID77408 live; domain-prepackage-audit и independent-repeat exit0,
активных клиентов этих controllers нет. MiningTrace actual silicon980
DON-919→EKA-355 observed408614.587, повтор сохраняет результат и MiningCollect.
Factory build0x6d8 прошёл pier1140 и перешёл defence_bor_tube120, не fullfinish.
Текущий purchase24 built nativeID270185ULL/paid1101651Cr, player2984399Cr;
номера включают waiting pricechanged, повторную оплату ключа не объявлять.
Документ: docs/domain-short-evidence-20261013.md. 24/32 остаётся.
Source diagnosticd дополнен threat_range/events, large_assets192,
защищённым новым save015; XSD/scheduling/Lua PASS. НЕ установлено после
этих правок; LIVEc. Async вопрос о quicksave pending, до ответа не закрывать
игру/не откатывать014. Следующий единый короткий пакет после verifiedquicksave:
штатный close77408→installdiagnostics freshreceipt→Steam→verifiedload,
threat_range/read, large_assets/последовательные reads, checkpoint015.
mining_resources не вызывать: настоящая добыча уже подтверждена.
Полный2h не начат;3.2 сбыт,3.4 развитие,3.6military,3.8bounded и6.3module
остаются обязательными. История ниже.

# Текущее состояние — 13.10.2026: подготовка mining_resources

X4 PID77408 live Respondingtrue подтверждён HOST/escalation. Sandbox process
list ошибочно пуст; НЕ считать это остановкой. Новый pipe-клиент не создан.
Diagnostics20261013d: добавлена однократная domain_mining_resources только
для точных MiningFixture station/miner с действующим назначением и без штурвала.
Штатный create_resource_area + собственный resource probe; не меняет груз,
приказы, навыки, claims или receipt доставки. Маркер ставится до эффекта;
неуспех области/зонда не повторяет создание. Подготовка не означает добычу.
MD XSD/cue scheduling и Lua5.1 syntax PASS. Установка остановилась WinError32
на занятом файле: receipt mining-resources-d-install-20261013.json НЕ создан.
Повтор без штатного завершения игры запрещён. После ошибки отдельная
проверка всех11 source/destination SHA дала0diff: файлы d уже на диске,
но install receipt отсутствует и LIVE runtime остаётся c до перезапуска.
Не считать совпадение диска загрузкой нового MD/Lua в работающую игру.
Production не изменён. Сохранение014 остаётся последним найденным; живой несохранённый прогресс
PID77408 сохранять, НЕ откатывать для установки без необходимости.
OpenSpec apply ready24/32 подтверждён через рабочую команду с escalation;
обычный sandbox CLI выдавал ошибку schema из другого пользовательского профиля.
Следующее: единый короткий пакет load014/read/legacy reconciliation,
mining_resources/mining_trace_arm, затем actual event delivery и остальные домены.
Перед запуском сверить owner pipe; полный2h пока не начинать.

# Текущее состояние — 13.10.2026

### Актуально: legacy delivery v3 подтверждён; активного клиента нет

X4 PID77408 live, controllers22300/v3 и final-read terminal0, нет active pipes.
Current world verified014 + обычный цикл; production51/v3 установлен SHA,
legacy-delivery-v3-install-20261013.json. Diagnostics11/c-v2 установлены SHA.
Candidate SHAf85b4381b5deec9dca85d376193454969860fc18b3eab3c370270f7eccd0463c,
qualified_releasefalse. Source совпадает с установленным пакетом.
Принят narrow legacy repair: purchase11 acceptednull→1→1, key/ship/goal сохранены,
WDR-951 commanderVTV-679/TradeRoutine/queue1/claimsent остаётся. Никаких новых
orders/Transfer/cancel/reset paid receipts для него. Новый отдельный native
purchase12_408062.614/BuildID34584ULL/paid7906044Cr pendingbuilding; другой
запрос held previous_purchase_unreconciled. Повтора12 по двум чтениям нет.
НЕ выходить/откатывать нынешний прогресс без необходимости установки/сценария:
014 содержит состояние ДО repair/purchase12; новый сохранённый checkpoint не создан.
Native стройка того же hired builder реально начала движение времени0→29.1569/1140,
модуль pier_bor_harbor_03_macro. Не принимаем finish3.4/6.3. Source fixture
siliconwafers external flag0, observerV3 armed, mining tracearmed; sale/deliverynull.
SETA попытки закончены, factor1. Military combat ещё не принят.
24/32; full2h не начат. Следующий аудит: referenced native cues/staticbase,
поскольку static шаблон != working instantiating cue; не чинить по имени без
точного lineage. Затем оставшиеся экономика/стройка/оборона/6.3 модуль.
Свидетельства docs/legacy-delivery-boundary-20261013.md; история ниже.

# Текущее состояние — 13.10.2026

### Актуально: legacy delivery v3 установлен; controller22300 активен

Controller64821/v2 terminal0: acceptednull, LegacyRecoveryResult
legacy_delivery_not_applicable. Guard сравнивал Goal.static с исходным
Request_Freighter шаблоном. Native scriptproperties: static=instantiatingcue,
staticbase=base. Verified014 read-only показал Goal764257 под764256/base764146
ref764317. Это referenced native Economy, не исходный md static cue.
V3 проверяет Goal.nameRequest_Freighter и Goal.parent==текущий Manager.economy,
сохраняя exact manager/key/paid/ship/requester/claim/order и отсутствие pending.
Функционал дальше не упрощался. XSD/scheduling PASS, production51 установлены
с SHA; receipt legacy-delivery-v3-install-20261013.json. Diagnostics11/c-v2
не менялись. Candidate SHAf85b4381b5deec9dca85d376193454969860fc18b3eab3c370270f7eccd0463c, qualified_releasefalse.
После native close127672 X4 стартована черезSteam, PID уточнить read.
Единственный pipe owner controller22300: verified014/load, native_analysis,
два read через20/40сек. До terminal второй клиент/выход игры запрещён.
24/32 принято; legacy repair НЕ принят до positive read-back; full2h не начат.
Записи ниже — история.

# Текущее состояние — 13.10.2026

### Актуально: legacy delivery v2 установлен; controller64821 активен

Controller57709 terminal0, acceptednull после native_analysis/20/40сек;
первый recovery не принят. Verified014 offline read показал прежний
TM_HandoffReasonexisting_behavior. V2 подтверждает старый exact claim через
существующий AcknowledgeDelivery, без TransferOwnedClaim/cancel/новых orders.
Полные guards/paid/owned/native routine evidence сохранены; cause записывается.
Production51 и diagnostics11 SHA установлены: legacy-delivery-v2-install и
legacy-delivery-v2-diagnostics-20261013.json. Candidate SHAe7f0012b0040db194a5331aa588b8e85bc0d80e0b0c3334103035879f47391e0,
qualified_releasefalse. X4 запущена черезSteam после native close37560.
Controller64821 единственный клиент: verified014/load, short native cycle;
до terminal не создавать новый клиент/не завершать игру. PID уточнить read.
24/32; full2h не начат. Записи ниже — история.

# Текущее состояние — 13.10.2026

### Актуально: production legacy delivery repair установлен; controller57709 активен

Последние controllers37550/C и C-final-read terminal0; после них PID146520
штатно завершён. Production51 с ReconcileLegacyFreighterDelivery установлен,
receipt legacy-delivery-install-20261013.json; candidate SHA35810d7db76096367cccdd1fc71b0bd1e1127012c84fd9cdab96241cadffe933,
qualified_releasefalse. diagnostics11/c не менялись после принятой установки.
X4 PID37560 boot черезSteam без дополнительных launch flags. Controller57709
единственный live pipe owner: verified014/load, read→native_analysis→20/40secs
read. До terminal не создавать второй client/не завершать игру.
Причина поставки и границы fix: docs/legacy-delivery-boundary-20261013.md.
24/32 принято; live repair пока не принят; full2h не начат.
C SETA попытка закончена/очищена, factor1. C-command surplus_open реальный
fixture flag1→0. Продажа/доставка/оборона/стройка ещё не приняты.
Записи ниже — история.

# Текущее состояние — 13.10.2026

### Актуально: diagnostics20261013c установлен; controller37550 активен

X4 PID146520 стартована черезSteam без добавления параметров. Controller37550
ожидает загрузку verified014 и короткий пакет; новый pipe-клиент до terminal запрещён.
Предыдущий controller99564 и followup terminal0. diagnostics11/c установлены,
receipt domain-diagnostics-c-install-20261013.json; source/installed SHA проверены.
Production51 и candidate44ee3283... неизменны,24/32, fullrun не начат.
B-проба доказала: EKA-355 siliconwafers istraderestricted1; WDR-951 реально
TradeRoutine/commanderVTV-679/claimsent, но purchase11 delivered/acceptednull,
Request_Freighter exists/complete и ReadGoalLifetimeavailable (не cancelled).
Нельзя устранять эту блокировку как «умершую цель» или очищать paid receipt.
C-проба читает точные claim/previousgoal/poll/Requester, перед production repair.
C открывает продажу только wafers тестовой refinery для реального NPC покупателя;
не посылает торговые приказы. Исправлен диагностический SETA guard: native docs
player.timewarp.active, factor1 нормальный (B ошибочно ожидала factor0, эффекта не было).
B-threat repair разместил Xenon в1385м от BJV-644; прежний убийца NPC scaleplate,
не наш флот. Новый enemy затем сменил Attack target на ownfighter; PCS ещё не принят.
Mining tracearmed, доставка ещёnull; стройка pier_bor_harbor_03_macro elapsed0,
требует реального deploy. Записи ниже — история.

# Текущее состояние — 13.10.2026

### Актуально: diagnostics20261013b установлен; короткий пакет подготовлен

Предыдущие controllers41855/86494 завершены, активного pipe-клиента до запуска
controller-domain-short-b-20261013.py нет. X4 PID169816 штатно завершена,
diagnostics11 установлен в tm_empire_diagnostics с SHA всех файлов,
receipt domain-diagnostics-b-install-20261013.json. Steam запущен без новых параметров.
Production51 и candidate SHA44ee3283cd0ff3df8ee05f97bd18fd0ab9075c60f56481f8be1e7af999faff2e неизменны.
Save014 создан штатно без перезаписи, gzip CRC/SHA/stats проверены:
save014-domain-checkpoint-20261013.json. Проверяем 014; пользователь также сообщил о сохранении.
Новый пакет расширяет observer на фактического NPC покупателя, чинит тестовую
сцену нападения на транспорт в его действительной зоне, читает lifetime оплаченной
поставки и modulemacro стройки. Native SETA ограничена коротким тестом и finally/end,
никакие building elapsed/deployed и собственные боевые приказы не подделываются.
XSD/native MD/AI/scheduling PASS после последней диагностической правки.
24/32 принято; полный длительный прогон не начат. Записи ниже — история.

# Текущее состояние — 13.10.2026

### Актуально: исправлена установка diagnostics; controller41855 активен

X4 PID169816 стартовала черезSteam. Controller41855 ожидает native save-menu,
затем verified013/load и короткий повтор; до terminal нового клиента не создавать.
Предыдущий controller86494 terminal1: новая команда не была распознана старым Lua.
Причина доказана debug.log: addon/MD duplicate. Ошибочно созданная мной папка
extensions/tm_empire_role_probe имела content ID tm_empire_diagnostics; X4 выбрала
старую правильную папку. Созданный duplicate удалён ТОЛЬКО после проверки exact
resolved path/без reparse point/11 файлов/SHA по receipt, native exit68532.
Никакие чужие расширения/сохранения не удалены. Корректная diagnostics11 теперь
установлена в tm_empire_diagnostics, receipt patrol-transport-correct-install-20261013.json.
tools/install_diagnostics.py выводит путь из content ID и отказывает при duplicate;
выполненная установка подтверждает11SHA. Production51 с PCS filter уже корректна.
Архив SHA44ee3283cd0ff3df8ee05f97bd18fd0ab9075c60f56481f8be1e7af999faff2e.
Прошлая short попытка НЕ принимается как результат новых diagnostic commands.
Новый runner пишет response до assertions, включая отрицательный ответ.
Save014 ещё не вызывался;24/32, полный прогон не начат. Записи ниже — история.

### Актуально: установлен patrol/transport пакет; короткий controller активен

Production51 и diagnostics11 установлены, native closure13 regenerated;
check_adapted_manager/XSD/scheduling5/Lua diagnostic syntax/install51 PASS.
Receipt patrol-transport-boundary-install-20261012.json. Архив пересобран;
current candidate SHA 44ee3283cd0ff3df8ee05f97bd18fd0ab9075c60f56481f8be1e7af999faff2e, qualified_releasefalse.
X4 PID68532 стартовала черезSteam; controller86494 ожидает native save-menu
и затем выполнит verified013/load + short package. Пока controller не terminal,
другой pipe-клиент/перезапуск запрещён. Период boot Respondingfalse не признан зависанием.

Исправлен узкий visibility seam PCS: this.$OurSectorShips/this.$AttackedOwner
является own pool зарегистрированного player, не enemy live-view pool. Другие
чужие корабли по-прежнему known/isinliveview. NPC originals не менялись.
Diagnostic read теперь до32 экономических действий + requester/trade/search,
до8 native distress records и до8 pickup records с точным ship/cargo/order.
Новая guarded threat_transport подготавливает реальное нападение того же
Xenon на свободный транспорт BJV-644 возле собственной fixture группы; только
enemy получает Attack. Native fighter attackrespond сам по себе не вызывает
callforhelp (interrupt.attacked native102–114); прежняя сцена не доказывала PCS.
Добавлен отдельный protected014 SaveGame helper для будущего checkpoint после
physical preflight, native ReloadSaveList, active projection и once marker.
Он ещё НЕ вызывался и не перезаписывает011/012/013.

Перед выходом сохранены receipts before-patrol-boundary-install-20261012.json:
строительство elapsed577.696/1140, MZK-812 всё ещё commanderEKA-355,
HOL-217 commanderKMT-485, оба настоящие торговые приказы. Повторного назначения
постороннего ship этим read не выявлено. Продажа NPC ещёnull; приемка24/32.
Записи ниже — история.

### Актуально: station trading установлен; короткий повтор завершён

24/32; X4 PID158092 responding, controllers35782/24545 terminal0,
активного pipe-клиента нет. Production51 и diagnostics11 установлены/SHA
проверены: station-trade-provision-install-20261012.json.

Добавлена потребность торгового подчинённого по штатному Upkeep и её передача
обычному Econ_Manager/Request_Commandeerable_Freighter; отдельного исполнителя нет.
Станция EKA-355 теперь имеет2 действующих подчинённых, производит; потребность
в торговом корабле исчезла. Точный commander подтверждён штатной read-only командой idle_orders_read:
MZK-812 commanderEKA-355/defaultTradeRoutine/claimsent; HOL-217 commanderKMT-485.
Receipt station-trader-commander-read-20261012.json, controller terminal0.
Повтор отсутствия дубля ещё нужен; общий read показывает только первые8 ActionReports.
BJV-644 Wait не означает, что управляющий никого не назначил: MZK-812 уже
TradeRoutine/claim sent/Request_Commandeerable_Freighter, exact commanderEKA-355.

Последние receipts: saved-current-boundaries-20261012.json и
current-native-provision-repeat-20261012.json (короткий native_analysis +15сек).
Стройка РЕАЛЬНО началась: processor building1, elapsed34.4548→155.681/1140,
тот же нанятый builder0x196bf/станция0x197ed, command buildingto, оплата50000Cr.
Завершения ещё нет;3.4/6.3 не принимать по одному началу.
Surplus pickup_count1, source4985→5092 (производство работает), NPC buyer0,
sale ещёnull. NPC реальная заявка wafers37810 @419Cr против own338.73Cr
подтверждена GetTradeList; продажа и прибыль не доказаны.
Target Attack/lastattacker точныйenemy, но claimnull; FOC записывает distress
order_sent0. Не выдавать самооборону/чужой мод за решение нашего управляющего.

Текущий candidate ZIP51 SHA
b20dd14024f03bcd08d4b8634d4799c2cb8a66921ff1b638d36eab2eebcceef2,
qualified_releasefalse. Generated closure13/XSD/Lua fixtures/scheduling5/
installer dry-run/OpenSpec strict PASS. Полный долгий прогон не начат.
Пользователь сообщил «сохранил»; новая запись физически не найдена в текущей
save-папке при чтении. Ничего не перезаписано и текущая игра не перезагружалась.
Проверенный013 сохраняется неизменным. Записи ниже — история.

### Актуально: v3 завершён; установочный кандидат собран

24/32, X4 PID177420, controllers11024 и прежние terminal0; pipe-клиента нет.
Diagnostics11 v3 установлен/SHA проверен. Причина удержания builder_repath
подтверждена: hired ship paranid. Исправленная диагностика отправила штатный
signal407836.708. Deployed/elapsed ещё0; это не принятая стройка.
Threat once resume407856.77 выполнен; собственные orders не инжектировались.
Surplus observer_v2 armed, pickup/sale ещё0. Подробности и receipts:
domain-native-resume-boundary-20261012.md.

Source после v3 содержит следующий ещё НЕ INSTALLED пакет: builder_position
для подготовки положения/ориентации по native расчёту без forced deployment,
market_source/market_buyer (reuse existing read-only GetTradeList), combat
shield/lastattack/attacker. XSD/Lua syntax PASS. Следующий шаг — установить эти
три уточнения вместе, load verified013 и коротко проверить реальные результаты.
Не ждать естественное развитие мира ради одного сценария.

tools/package_mod.py + README готовы; ZIP51 проверен по source/installed SHA,
dist/tm_empire_management-candidate.zip, qualified_releasefalse.6.6 не закрыта:
игровые критерии и длительный прогон остаются обязательными. Записи ниже — история.

### Актуально: domain-native-resume-v2; активного клиента нет

24/32, production51 не менялся. Diagnostics11 v2 установлен и SHA проверен
domain-native-resume-v2-install-20261012.json. X4 PID164980 responding.
Controllers40120/6679 terminal0; domain-native-live-followup terminal0.
Verified013 загружен без overwrite. Native Manager active, age407980.872.
Наблюдатель surplus_v2 armed407836.665: отслеживает собственную покупку wafers
у EKA-355 и последующую продажу тому же NPC outlet; до32 transport records.
Это исправляет неполный диагностический фильтр commander-only, не меняет AI.
Реальной покупки/продажи ещё нет: pickups0, source5000, buyer0, traderWait.
Enemy MOM-017 pilot реальный, Attack targetIYF-712/flying, hulltarget100;
поздний повтор threat_resume удержан existingAttack, эффекта нет.
Builder paid5000000 native units =50000Cr, DeployToStation точной LFQ-500,
pilot/aipilot существуют. builder_repath удержан, marker null; причина guard
ещё не установлена. Не выдавать пустой marker за выполненный сигнал.
Processor elapsed0/total1140, дистанция до native build position3264.5.

Source ПОСЛЕ установки ещё уточнён и пока НЕ installed: diagnostic read включает
все основные boolean guards застройщика; repath использует штатный friend/NPC
критерий вместо лишнего ограничения faction.argon. Native picker может нанять
любого подходящего NPC. Threat resume допускает тот же действующий Attack,
чтобы один раз расположить фиксированного enemy возле текущего target и дать
Attack100km. Предыдущий v2 допускает только Wait/Patrol. Source XSD PASS.
Следующий шаг: одним пакетом установить диагностические уточнения и проверить
три домена, не ожидать естественную стройку ради одного сценария. Гейты открыты.

### Актуально: 24/32; доказана причина пустого отчёта

4.2 принята: personnel-transfer-acceptance-20261012.md объединяет реальное
прибытие, отказ по вместимости, потерю назначения и сохранение точной квитанции
после загрузки013. Controllers37180 и37614 terminal0; активного pipe-клиента нет.
Исходный управляющий восстановлен после короткой смены, seed не изменён.
ui-governor-switch-20261012.json: tasks14, строка10 имеет reason1238 UTF-8 bytes;
предел1024 отвергал весь отчёт. Source теперь допускает task.reason до4096,
остальные пределы сохранены. Native Lua fixture PASS: длинный русский текст
принимается,4097 bytes отвергаются. Установка и игровая проверка завершены:
status-reason-boundary-20261012.md. X4 PID56044; controllers74712/7289/9170
terminal0, pipe-клиента нет. Вкладка110строк, top27/selected29 сохраняются.
Диагностические пилоты созданы; собственные приказы остаются штатными.
Продажа избытка, ответ на угрозу и завершение стройки ещё не приняты.
Полный длительный прогон не начат. Записи ниже — история.

### Актуально: пакет domains / verified save013 / исправление fixture crews

Приёмка23/32. Production51 с startup fix не менялся; все installed SHA сверены.
Diagnostics11 добавляет domain_probe/blocked_crew_probe, bounded projection_raw,
и безопасный новый save_boundary_package только с preflight свободного013.
XML/scheduling, native Lua syntax и unittest5 PASS. Все11 SHA сверены.

Controller-domain-package-short/session39841 terminal0, followup terminal0:
реальный crew key crew_assignment_3_407611.92/person17869491377443404523/
seed-577252696266147093. Target NWU-455 уничтожен в407611.944 до native
podarrival407621.928. Последующий read: exact receipt unknown/transfer_destination_lost,
source member0/target gone, без повторного назначения.4.2 ещё открыта.
Docs: personnel-destination-loss-20261012.md.

Surplus: EKA-355 siliconwafers5000, NPC buyer NKU-508, native trade subscription,
trader BJV-644. Military: ownerless-known sector Близнец Хевы IV Бухта player,
4 fighters, known Xenon MOM-017 рядом с IYF-712; Attack только enemy.
ПРОБЫ ЕЩЁ НЕ ПРИНЯТЫ: у trader/4fighters/enemy нет pilot — ошибка подготовки.
Исправлены source military_fleet_prepare/domain создавая native control entities.
Добавлен guarded domain_complete_crews для существующих фиксированных fixtures,
без повторного спавна и без собственных injected orders.

Regression: после lifecycle restore UI1row/projectionfalse при active governor,
post-lifecycle-domains-20261012.json. Причина ещё не доказана. Свежий load012
и domain followup дали projectiontrue/все четыре секции valid; не выдавать
один restart за исправление. projection_raw now section count + invalid_item
позволяет получить точную причину после повторной смены governor.

Новый checkpoint013 реально записан без overwrite (client terminal0):
93318252 bytes, mtime_ns1791833893966588200, age407836.492, CRC PASS,
SHA c8b2275ac4823d663f8ca7fa6d766a9756d41956feb18010fce8c6b7f4150d38,
все4 markers true; save013-boundary-package-20261012.json.
Не перезаписывать013 и старые slots. Штатно закрыт PID118280, установлен
crew fix diagnostic11 (domain-crews-fix-install-20261012.json).
X4 PID65104, единственный controller-domain-crews-load013/session37180/
PID128992 ЖИВОЙ: load verified013 → projection_raw → complete_crews → reads.
Не запускать второй pipe и не перезапускать по timeout наблюдения.
Полный длительный прогон не начат. Остальные записи ниже — история.


### Актуально: lifecycle принят, исходное назначение восстановлено

Приёмка23/32:2.4 закрыта по governor-loss-acceptance-20261012.md.
Controller-startup-fixed/session85427 terminal0: новый Manager active,
old_manager_stopped1; исправление общего startup barrier принято в игре.
Controller-lifecycle-losses/session8645 terminal0: module_loss/station_loss/
actor_loss реально исполнены только на отдельной fixture, каждый →inactive,
governor/manager null, old_manager_stopped1. Между потерями реальные rebind active.
Последний restore: исходный actor0x4bb7a/seed-9126173547698565463,
station0x4bb73/module0x4bba2; manager0x4bb90/seed-7877045512791511809
сохранён. Runtime active, original physical binding/flags корректны.

Платежи/ключи plot/funding/expansion/builder/purchase не сброшены и не повторены;
plot transaction count1. Старый native builder продолжает существовать, receipt
sent/deployment_pending честная, готовность не подменялась. Fixture actor погиб,
исходный actor не уничтожался. Receipt lifecycle-losses-20261012.json.
X4 PID101644 живой, контроллеров pipe сейчас нет (сторонние Python не трогать).
Установка production51 с исправленным startup, diagnostics9, хеши подтверждены.
Новые сохранения клиентом не создавались. Полный длительный прогон не начат.
Оставшиеся3.2/3.4/3.6/3.8/4.2/6.1/6.3/6.4/6.6 (9 задач).


### Актуально: исправлен общий startup barrier, идёт повторный load012

Первый lifecycle-load/session93546 terminal0: prepare/bind успешны,
fixture station0x186eea/module0x186f49/actor0x186f5a, seed1914611559896981528.
Исходный actor seed-9126173547698565463 и station manager сохранены.
Manager не стартовал: runtime bound/manager null, причиной был общий запрет
TM_PlayerManagerWatch при любом остатке OwnedClaims/StationReassignments.
Потери НЕ выполнялись: клиент правильно остановился до их подготовки.
read-active terminal0 подтвердил ту же причину, не считается приёмкой2.4.

Исправлен generator adapt_native_manager.py и пересобран closure13:
старые claims не очищаются и не переприсваиваются; identity/unknown/receipt
проверки сохраняют конкретные активы защищёнными. После отмены прежнего cue
новый Manager стартует, независимые активы не ждут общего обнуления claims.
Проверки closure13, XML/scheduling, install dry-run51 и OpenSpec strict PASS.
Diagnostics restore теперь умеет штатно снять текущего fixture governor;
исходный seed/станция/module/manager и original temporary trait обязательны.

Штатно закрыт X4 PID78652. Установлен полный production51, SHA read-back
в docs/installed-manifest.json (qualified_release=false). Diagnostics9 SHA:
.cache/tmp/station-boundary-20261011/lifecycle-startup-fix-install-20261012.json.
Новый controller-lifecycle-startup-fixed/session85427 ЖИВОЙ, ждёт SaveMenu,
затем load verified save012, prepare/bind/read. Не запускать второй pipe.
Rollback к012 намеренный: отдельная несохранённая fixture не является checkpoint.
Повторный игровой запуск исправления пока не принят. Приёмка22/32.
Полный длительный прогон не начат. Остальные записи ниже — история.


### Текущий запуск: отдельная lifecycle fixture

Production51 не менялся. Diagnostics9 установлен с полным SHA read-back:
.cache/tmp/station-boundary-20261011/lifecycle-install-20261012.json.
Новый lifecycle_probe.xml использует только отдельную prefab станцию,
сотрудника и модуль. Штаб-квартира/исходный сотрудник не уничтожаются.
API уничтожения actor проверен по common.xsd remove_actor_from_room destroy=true.
Исходному actor после штатного Unbind временно сохраняется жизнь; Restore
возвращает исходный temporary trait перед штатным RequestAssignment.
Никаких изменений Registry OriginalTemporary напрямую нет.
XML/scheduling, native Lua syntax, unittest5 и closure13 PASS.

После штатного CloseMainWindow/WaitForExit PID171136 запущен X4 PID78652.
Единственный controller-lifecycle-load/session93546/PID60608 живой,
load save012 принят штатным SaveMenu. Не запускать второй pipe и не
перезапускать по timeout. Клиент prepare/bind/read НЕ выполняет потери;
они допускаются только после реального active Manager fixture.
Приёмка22/32;2.4 ещё не принята. Полный длительный прогон не начат.
Свидетельство добычи980 silicon записано в mining-delivery-boundary-20261012.md.


### Актуально: короткий read-back после подтверждения сохранения

Приёмка22/32:2.2 закрыта по governor-assignment-acceptance-20261012.md.
X4 PID171136 работает; loader40168 завершён с exit0. Короткий клиент
controller-saved-world-read-20261012.py также terminal0, активных pipe клиентов нет.
Production51/diagnostics8. Старые записи о живом loader и21/32 ниже — история.

mining_trace_read подтвердил точное native event_trade_completed:
DON-919 → EKA-355, silicon980, issued407611.922, observed407954.506.
Это реальная доставка назначенного штатным алгоритмом шахтёра, не просто
рост запаса и не диагностическая подмена. Текущий запас500, miner cargo0,
commander прежний, order MiningCollect, Claim sent/Request_Commandeerable_Freighter.
3.2 остаётся открыта до проверки оставшейся границы сбыта.
Receipt: .cache/tmp/station-boundary-20261011/saved-world-read-20261012.json.
UI: mode tm_empire_status, body_rows212. Управляющий active.

Новые сохранения этим read-only клиентом не создавались. Последний физический
именованный слот по текущей проверке save012 (21:25:39),93068284 bytes.
Подтверждение пользователя не выдаётся за наличие нового файла сохранения.
Исправления idle DockAndWait и сохранения прокрутки уже приняты ранее:
idle-scroll-funding-acceptance-20261012.md. Полный длительный прогон не начат.


### Текущий процесс: installed trace / load012

Diagnostics8 установлен после штатного CloseMainWindow/WaitForExit PID90272.
Все8 SHA сверены, receipt diagnostic-boundary-trace-install-20261012.json.
Новые mining_trace_arm/read и governor_binding уже В УСТАНОВКЕ; production51
не изменён. XML/scheduling, Lua syntax и unittest probe responses5 PASS.
Попытка pytest не исполняла тесты (pytest отсутствует); после этого выполнен
реальный стандартный unittest discovery,5/5 OK; зависимости не устанавливались.

Сейчас X4 PID171136 (boot), единственный controller boundary-trace-load /
session40168 / PID147772 ЖИВОЙ: ждёт mainmenu pipe, затем загрузит verified
save012 и вызовет personnel_read/mining_trace_arm/mining_read/provision/read.
Нет нового factory trigger/спавна/оплаты. Не запускать второй pipe и не
перезапускать из-за timeout наблюдения. Checkpoint тот же, физические слоты
не перезаписаны. После load: проверить binding exact actor/seed/module и
station manager; trace armed не равно delivery observed. Приёмка21/32,
полный длительный прогон не начат. Остальные записи ниже — история.

### Актуально: контроль игрока принят; diagnostics trace подготовлен

Приёмка21/32:3.7 закрыта по player-control-acceptance-20261012.md.
Controller-control-boundaries-prepared/session51820 terminal0; все фазы
passenger/helm/manual/priority/restore passed1, MD personnel guard и Lua queue
guard согласованы. Lua queue guard сам не проверяет helm — отдельные Lua
финансовые исполнители проверяют GetPlayerControlledShipID. Исходный игрок
возвращён на container/control0x19467. Native constructor продолжал elapsed
21.9774→29.9099; governor/seed сохранены. Первый неподготовленный клиент
control-boundaries terminal1/not_prepared не принимался за успех, эффектов нет.

Construction-control-followup terminal0: runtime active/goals3,
economy_last_run408079.319, age408570.503; native build processing1,
elapsed568.129/total1140. Mining EKA-355 silicon0→740→1000; DON-919 остаётся
MiningCollect с тем же native claim/commander. Источник конкретной поставки
этой суммой ещё не доказан,3.2 не закрыта. Crew remote exact person/seed и
target_member1/source0/flags0 сохранены, но текущая Transfer receipt другая,
поэтому read unmatched не выдаётся за новый transfer receipt.

SOURCE-only diagnostics пакет (ещё НЕ установлен): одноразовые mining_trace_arm /
mining_trace_read, native event_trade_completed конкретного miner→station,
только одна квитанция/одно событие, без асинхронных Lua-ответов, без production
истории или изменения мира. Поля State.MiningFixture проверены по реальному
setup. Также read выводит exact governor actor/seed/station/module/macro и
station manager/seed. Native event contract взят из rml_deliver_wares и
common.xsd. MD/XSD/scheduling, Lua syntax, OpenSpec strict PASS.
Production не менялся; обе дополнительные границы нужно установить вместе
при следующем согласованном обновлении, затем native load012 и read/arm.
Сейчас X4 PID90272 живой, клиентов python нет; save012 остаётся проверенной
базой, остальные слоты не изменены. Полный длительный прогон не начат.

### Load012 завершён; текущие клиент и приёмка

Session35035 terminal0; активного pipe клиента нет. X4 PID90272 живой,
Responding=true. Save012 native load принят. Runtime active, один Manager,
goals3, factory receiver существует. Exact paid hire559840Cr/seed сохранён;
mining commander remapped0x4b637, тот же DON-919/claim/MiningCollect.
Новый construction_2_407451.359 ремаппирован station0x19694/build0x6ff;
plot/funding observed, builder_hire2 остаётся единственным paid50000Cr.
Настоящий строитель0x19590 стал actualbuilder; processor building1,
elapsed0/total1140/step_total60. Это начало штатной стройки, не её завершение.
Начальный native_analysis busy — нормальная занятость restored analysis,
не признак отсутствующего управляющего. Собственных новых MD ошибок узкий
поиск текущего debug.log не нашёл; весь лог чужих модов этим не квалифицирован.

4.1 закрыта после сверки точных условий задачи с имеющимися свидетельствами:
autonomous hire/vacancy, no candidate, money/replay fixtures786, отдельные
governor/station roles621, latest paid/save012 read-back. Документ:
personnel-hire-acceptance-20261012.md. Приёмка20/32. 4.2 не закрыта: положительные
native remote/service arrivals и capacity negative уже есть (batch-current-
contracts.json), их повторять не нужно; остаётся сверить недоступный маршрут.
Текущая full production51/scalar catalogue установка проверена installer.
Полный длительный прогон не начат; не ждать1140s ради одной стройки, продолжать
другие короткие независимые границы. Следующая база — проверенный save012.

### Актуально: save012 и полный исправленный catalogue пакет

Приёмка19/32:5.4 закрыта по station-catalog-batch/repeat. Native Upkeep
назначил DON-919 станции EKA-355; повторный цикл не назначил второй корабль,
свежая проекция mining=null/subordinates1, текущий приказ MiningCollect.
Добыча/доставка3.2 не приняты. Новый native plan8 entries принят по чертежам,
construction_2_407451.359/build0x8ae6 queued; plot2 observed, funding2
observed6320362Cr, paid builder_hire_2_407571.206. Diagnostics подготовила
материалы и переместила оплаченного строителя ближе; completion не форсирован.

Сохранён отдельный ранее пустой slot012 native SaveGame, без overwrite.
save012-package-20261012.json:93068284bytes,
SHA66494d9846cdf8d7fe987f134cc150548e45ef8f18fc51444109ca6ba79eb9c3,
CRC/stable PASS, paid hire/service wharf/new construction markers true.
Игровое время407611.495. Это новая база; старые autosaves/save011 не изменены.

Точный повторный catalogue error был get_god_production_construction_plan,
не create_factory/select. Он также исправлен на одну культурную faction.
Generated13/check/XSD PASS, production51 установлен после штатного закрытия
PID81148. Текущий X4 PID90272 (boot), единственный pipe controller
station-save012-load/session35035 ЖИВОЙ, ждёт menu/load012. Контроллер не
создаёт новую фабрику/минера, только read-back + native_analysis после load.
Проверить session35035 перед любым следующим pipe. Полный прогон не начат.

### Обновление: исправление native factory catalogue

Session76020 завершена успешно. MAR-136 получила свободный VUB-709 через
обычный native Request_Commandeerable_Freighter: commander=0x188ae9,
order=MiningRoutine, claim=sent. Это подтверждает назначение, но ещё не добычу
или доставку. Повторный клиент PID160432 не подключился; штатно остановлен
перед обновлением, новых эффектов и квитанции повторной проверки нет.

Реальный Request_Factory создал shell0x188ead, но обнаружены ошибки:
create_factory/select требует одну faction, а не список; изолированная
EquipmentTable не была инициализирована. Генератор исправлен: native faction
по культуре владельца и штатный get_ware_definition flags=equipment. Исходные
скрипты игры не изменены. Adapter check и XML schema PASS, production51
установлен после штатного завершения PID59644. Steam запущен только с appid.

Текущий единственный pipe клиент — controller-station-catalog-load/session34015:
ожидает native main-menu, загрузит проверенный autosave_01 и повторит короткий
пакет подготовки mining/paid factory/read-back. Не запускать второй клиент.
Старые разделы ниже — история. Приёмка остаётся18/32; полный прогон не начат.

### Текущий общий station report / paid construction пакет

Session41440 и followup terminal0, больше не живые. Второй реальный mining
fixture IOP-356/IJN-713 всё ещё пропущен: Report.keys.count0 не включает станцию
в native GlobalStorageData. Source исправлен: один native Upkeep до report gate,
Report.$TM_MissingMiningTypes сохраняет непустую потребность, UI переиспользует
результат. Quantitative native shortage не выдумывается. Generated13+check/
MD+Lua syntax и diagnostics tests5 PASS. Общий production51/diagnostics8 с SHA
установлен после штатного закрытия PID154584. Детали — station-provision-package.

Сейчас X4 PID59644 Responding=true. Controller station-report-load/session76020
ЖИВОЙ: native accepted load autosave_01, ждёт окончанияload, затем prepare
mining world, native_analysis, factory_build_start и read-back. Не запускать
второй pipe клиент/не перезапускать по observation timeout. В source/установке
есть новые factory_build_start (normal paid Request_Factory, не free spawn),
mining_read report_present/time, keyed world resources/builder-near для нового
заказа и safe own save012. Слот012 физически пуст на последней проверке;
перед реальным save повторить physical preflight и не переписывать старые слоты.

Следующее: дождаться76020, разобрать native mining request/search/commander,
новый factory plan storage + prerequisites/payment/build. При реальном новом
build разрешена краткая diagnostics подготовка ресурсов/близкого paid builder,
но не форсировать завершение/приказ/прибытие как доказательство. Для сохранения
этого пакета использовать012 после physical preflight, CRC/SHA, потомnative load.
Широкие3.4/5.4 открыты, общий прогон не начат;18/32.

### Исправленный Upkeep-пакет установлен; загрузка в процессе

Актуальная квитанция и объяснение: docs/station-provision-package-20261012.md.
Новый native mining_setup/mining_read установлен с diagnostic8. Реальный платный
hire_1_407213.473 observed, exact actor/seed, paid559840Cr; autosave_01 20:44:24
CRC/stable/SHA проверен, содержит hire/service wharf/старую реальную стройку.
Load общего storage+mining пакета/session6355 terminal0 подтвердил persistence
hire/passed1. Бесплатная prefab refinery WQH-227 и idle miner FIR-145 выявили
лишний gate: native Upkeep missing miner, production waits resources, но native
InsufficientProductionWares пуст. Gate удалён; действующая vacancy Upkeep сама
является основанием, report amount0 не подменяется выдуманным дефицитом.

Generated13+check_adapted_manager+MD syntax/ref/scheduling PASS. PID113824
штатно закрыт; обновлён полный production51 с SHA. Diagnostic8 не менялся.
Steam перезапущен только appid392160. Controller mining-upkeep-load/session41440
сейчас ЖИВОЙ: ждёт mainmenu pipe, затем load того же проверенного autosave_01,
personnel persistence read, mining_setup заново, native_analysis и read-back.
Новый X4 PID154584 сейчас Responding=true; session41440 получил native
load accepted/autosave_01 и ждёт окончания загрузки. Последний CPU142.98sec,
собственных MD ошибок узкий поиск debug.log не обнаружил. Это не общий аудит
чужих модов. Не запускать второй pipe клиент, не перезапускать по timeout наблюдения.
Проверить session41440 и текущий X4 handle в следующем ходе. Bootstrap на старте
может опережать завершение initialization station; краткий follow-up после
готового native report допустим, не ждать естественного мира долго.
Полный прогон не начат; задачи18/32, широкая3.4/5.4 всё ещё открыта.

### Обнаружены недостающие хранилища новой фабрики

Короткие service-provision/mining-cycle-20261012 завершились exit0; квитанции
в `.cache/tmp/station-boundary-20261011/`. Реальная новая фабрика VTV-679,
0x4b736: creation adopted, expansion observed (7 entries), plot/funding/builder
observed; production_total1, но cargo capacities energycells/silicon/scanningarrays0.
Это не функционально готовая фабрика и не приёмка3.4/5.4. Native mining upkeep
видит отсутствие добывающего корабля, но отчёт production не содержит дефицита
при нулевой ёмкости. Отдельно diagnostic service_setup создал бесплатную wharf
SXB-995/0xa1f7054 (21 modules); это только условия тестирования, не строительство.

В adapt_native_manager.py/adapt_finalise_plan_generation добавлен штатный
get_suitable_storage_modules перед native layout: учитываются все production и
storage из NewPlannedModules/BaseSequence, добавляются только необходимые storage.
Все модули проходят прежнюю общую проверку чертежей и платную очередь.
Копия create_factory на самом деле сохранена; не утверждать, что её удаление
вызвало проблему. Точная причина неполного результата selection ещё не доказана.
Generated13 scripts пересобраны; check_adapted_manager и validate_md PASS.
Этот новый storage-пакет ещё НЕ установлен в PID154872. Старый runtime работает.

Read-only personnel-state-20261012 exit0: native personnel goal живой,
last_tick407062.079; scan VTV target/post manager, кандидат известной станции
known_hireable_actor_unavailable. Hire receipt нет; VTV manager отсутствует.
Это обычная нехватка доступного кандидата, пока не доказан баг executor.
Не создавать бесплатного менеджера вместо проверки реального найма.

Следующее: закончить coherent storage/станционные prerequisites, подготовить
короткие условия minable deficit/известного hireable actor, затем единая установка
и короткая проверка реального плана/строительства/обеспечения. Существующую VTV
нельзя считать исправленной новой логикой: нужен реальный платный expansion.
Полный долгий прогон не начат; приняты по-прежнему18/32. Активного pipe клиента нет.

### Новое quicksave, общий пакет установлен, короткий прогон завершён

Пользователь подтвердил сохранение. Quicksave17:09:36/93922980bytes,
CRC/stable/SHA подтверждены квитанцией quicksave-package-20261012.json.
PID66472 штатно закрыт, production51/diagnostics8 установлены и SHA проверены.
PID154872 загрузил именно quicksave. Package controller/session56495 terminal1
из-за слишком ранней проверки прокрутки при35rows/topclamped7. Retry/session12019
terminal0:129rows, frame5850→6674, top27/selected29 сохранены, empire18/stats85.
BKK-871/Dротик idle1/DockAndWait→реальный TradeRoutine/claimsent;37trade/29mining
задач сохранены. Station funding key1_396669.992 observed/paid67800Cr,
paymentreconciled; KMT actual135600Cr=productionmoney послеload. Подробности:
docs/idle-scroll-funding-acceptance-20261012.md. Новых широких принятых задач
нет,18/32;5.4 требует обеспечения кораблями. Полный прогон ещё не начат.
Активного pipe клиента нет. Ожидание сохранения и blocked-записи ниже устарели.

### Ожидание сохранения текущего тестового мира

Последняя проверка: X4 PID66472 Responding=true; новой физической записи
сохранения нет, последнее игровое save011 от12.10.2026 15:56:56, quicksave
от11.10.2026 20:51:16. Dry-run полного source пакета51 файлов PASS, установка
не изменена. В текущем мире после save011 появились новые корабли/назначения
и подготовлены условия station supply/budget. Запрос пользователю сделать
быстрое сохранение остаётся без ответа несколько последовательных goal turns.
Дальнейшая установка/игровое подтверждение ждут сохранения: не завершать игру
с потерей этого состояния. Цель blocked до ответа/нового сохранения, не complete;
приёмка18/32. После возобновления проверить файл/CRC, штатно закрыть X4,
установить общий source+diagnostics пакет с SHA, загрузить новый quicksave,
выполнить idle-scroll/provision и остальные короткие сценарии до полного прогона.

### Исправления по сообщению игрока: простой и прокрутка

В исходниках вкладка восстанавливает штатные settoprow/setselectedrow при
обновлении. Lua fixture проверяет восстановление 27/29 и сброс сохранённых
значений. Общий фильтр HasOnlyIdleOrders разрешает только бессрочный Wait
и завершённый DockAndWait без служебных параметров, очереди настоящих задач,
override/priority/loop. При новом назначении убираются только проверенные
приказы простоя; default DockAndWait заменяется штатным Wait. Проекция
использует тот же фильтр. Изменения пока не установлены в живой PID66472;
игровое подтверждение обоих исправлений остаётся открытым. Новых принятых
задач нет, 18/32. Также не установлен ранее изменённый отчёт снабжения флота.

Короткий read-only idle-before-20261012 завершился exit0: текущий мир
2stations/74ships, UI115rows, provision age396042.165; priority fixture
не подготовлен. В исходники diagnostics добавлены idle_orders_read (до128
кораблей, без эффектов), ui_scroll_prepare и ui_scroll_read. Последние
проверяют штатную прокрутку через refreshInfoFrame/GetTopRow, без внешнего
управления экраном. MD/schema/closure/Lua syntax/UI fixture/OpenSpec strict
PASS. Текущий мир отличается от save011 новыми кораблями; у пользователя
запрошено быстрое сохранение перед общей установкой/перезапуском. Пока
ответа о сохранении нет, игру не завершать. Клиент idle-before терминальный.

Следующая доработка исходников: причина нехватки боезапаса учитывает не
только rawloadoutlevel корабля, но и наследование настройки от командира
и player.loadoutlevel по interrupt.restock. Обход ограничен16 звеньями;
незавершённая цепочка не объявляется отключённым снабжением. Снабжение
выполняет исходный игровой обработчик, новых заказов и настроек этот
отчёт не создаёт. MD schemas/scheduling и closure PASS; живое подтверждение
по-прежнему требует общей установки. Быстрое сохранение по чтению каталога
не обновлено (quicksave.xml.gz от11.10.2026 20:51:16).

Проверены libraries/scriptproperties.xml:1410/1413 и order.move.wait.xml:
при завершении перемещения он вызывает order.wait, который выставляет
command.wait/commandaction.standingby. Фильтр теперь допускает текущий
бессрочный MoveWait только с этим фактическим состоянием пилота, без
withdraw/waitforatgate/gate/noattackresponse. WaitForSignal и WaitForVenture
служебные и не освобождаются. Любой order.trade/build/operation сохраняется.
Диагностический read показывает pilot_command/pilot_action. MD/closure PASS,
source пока не установлен; новое игровое подтверждение обязательно.

Подготовлен controller-idle-scroll-20261012.py (ещё не запущен): чтение
реальных приказов, открытие статуса, установка штатной прокрутки27/29,
короткое ожидание обновления и read-back. Приёмка требует смены native
frame ID и сохранения обеих позиций, иначе проверка считается недоказанной.
Затем проверяются неизменённые штатные страницы empire/stats. Скрипт не
перезаписывает существующую квитанцию и не повторяет эффект после ошибки.

provision-short-20261012 и provision-read-after-20261012 terminal exit0:
KMT открыта для торговли штатной командой, player→station50000Cr с
двухсторонним read-back. Подготовка бюджета station→player82200Cr реально
уменьшила150000→67800 и увеличила игрока53890588→53972788, но diagnostic
неверно ожидал положительный result: native result=-82200. Проверка source
исправлена на допустимый знак при обязательном точном read-back обеих
сторон. Повторной подготовки/перевода нет. native_analysis requested;
factory текущие energycells1485/water0, ресурсные trade rules owner_only0;
свежий отчёт396666.509 показывает water/production budget shortage. Чтение
396837.071: отчёт тот же, stationFunding ещё не доказан (UI выводит только
первые8 задач).5.4 открыта. В source ProvisionRead добавлены отдельные
текущие счета и stationFunding receipt/payment без эффектов, для следующей
общей установки. Старый quicksave ещё не обновлён; тестовый мир теперь
имеет75ships/2stations. Новое сохранение должно включать эти условия.

personnel-read-20261012 terminal exit0: активная кадровая цель имеет свежий
last_tick397056.811/required_control_posts_present; подготовленного HireScenario
в этом мире нет, receipt null/passed0 и это не принимается как найм. Список
кандидатов читает217 известных доступных для стыковки станций малыми группами;
служебные NPC/занятые посты отвергаются actor_not_hirable_or_remote. Нового
найма/перевода не выдано. README уточнён по принятому station status/load и
ожидающим игрового подтверждения idle/scroll изменениям. Из UI удалено
оставшееся упоминание «вины менеджера» в причине native_no_viable_economic_action.
UI fixture PASS. Пакет по-прежнему не установлен; новых принятых задач нет.

### Приняты текущий статус и загрузка нового менеджера

status-reload-bound/session71115 terminal exit0. Native list/load принял011;
current_new1/seed-7877045512791511809/transit0/source_member0 сохранены,
governor/EmpireManager независимы. До свежей проекции station_status не было,
затем74assets/2stations/117rows: factory needs_attention/energycells+water,
HQ Крисс Донел/ready, assessment/history false. Empire18/stats85 работают.
Supply consumed6118Cr лишь прочитан, новых переводов/найма не выдавалось.
5.1/6.5 приняты по docs/station-status-load-acceptance-20261012.md:18/32.
Длительный прогон не начат. X4 PID66472 живой, активного pipe клиента нет;
production51/diagnostics8 установлены. Старые pending записи ниже исторические.

### Согласованный пакет bound-save и привязка незавершённого наблюдения

status-save-bound/session34429 terminal exit0. HQ manager same new seed
-7877045512791511809/current_new1/transit0, governor unchanged; штатные
empire/stats открылись. crew_capacity preparation_unavailable и roles_read
без подготовленного singleton-сценария не принимаются как успешные проверки.
Сохранённая supply6118Cr/consumed квитанция прочитана без нового заказа.
SaveGame запросил save011; реальный файл91638431 bytes/uncompressed748587930,
gzip CRC/stable PASS, SHA9b05d50051d51e693296f04941643775050f08ccc9b0e107a326939e4b456644.
Все17 прежних xml/xml.gz файлов по size/mtime не изменены. Квитанции:
status-save-bound-20261012.json и verified-status-save-bound-20261012.json.
Это ещё не доказывает load; controller-status-reload-bound/session71115 живой,
новый X4 PID66472 загружает сохранение. Пока16/32, full run не начат.

Production51 и diagnostics8 установлены; установщик/диагностические SHA
проверены. X4 PID177512 запущен через Steam, controller-status-save-bound-
20261012/session34429 работает; результат ещё не принят. Он использует
request_status_save (физическая предварительная проверка save011), затем
потребуется gzip/CRC/SHA/stability и настоящий native load/read-back.
Старые save001–010 не трогать; прежние контроллеры терминальные.

В production Assets частичный сбор теперь хранит SourceManager/SourceSession
при начале обхода. При смене управляющего/сессии или откате времени он
сбрасывается, в готовую проекцию передаётся исходная привязка, а не текущая
на момент завершения. Это закрывает смешивание разных назначений при
обходе большой собственности; MD schemas/scheduling/изоляция PASS.
Широкая игровая приёмка3.8 остаётся открытой,16/32, full run не начат.
Сведения о pending установке предыдущей диагностики ниже исторические.

### Короткая проверка сохранения текущего статуса

Повтор status-save-win32-20261012/session67935 терминальный exit1:
file_check_unavailable/effects=false; сохранение не выдавалось. X4 PID150068
живой и отвечает; активного pipe-клиента после terminal нет. Не считать
Windows FFI доступным только по библиотечному синтаксису. Штатный helper
подтвердил диапазон save001–010, все10 физически заняты; GetSaveList скрывает
часть несовместимых старых файлов. Поэтому свободный обычный слот отсутствует.

В исходниках диагностический save_current_status теперь требует точный
preflight_save_011_absent. Python request_status_save проверяет физическое
отсутствие save011.xml/xml.gz непосредственно перед единственным запросом;
Lua дополнительно проверяет native list для этого отдельного имени, active
governor и сохранённый no-replay marker. Диагностический список load допускает
save011 локально, без изменения Helper.validSaveFilenames штатного UI.
Недоступные io/Win32 FFI удалены. Предыдущие auto-slot команды отказывают
preflight_required, save_fixture retired. Это исходная доработка: последние
role_probe/save_menu ещё НЕ установлены; native save/load011 НЕ доказан.
5 response/preflight tests PASS (занятый физический файл не отправляет запрос;
stale frame не повторяется), Lua syntax/Python compile/OpenSpec strict PASS.
Перед следующей общей короткой установкой обновить контроллер на
request_status_save; текущий старый контроллер не соответствует новому wire.
Резервные слоты/старые сохранения не изменять. Приёмка16/32, full run не начат.

status-save-20261012/session7656 завершён exit1: штатная смена менеджера HQ
сохранена в live read-back (тот же новый seed, transit0, governor unchanged),
но save_current_status отказал file_check_unavailable/effects=false. Запись
сохранения не выдавалась. Game Lua не предоставляет пригодный io.open для
этой проверки; standalone Lua fixture не доказывает доступность в игре.

Диагностика исправлена: проверка файлов через GetFileAttributesW/UTF-8→UTF-16,
отдельная проверка существующей папки и отказ при любой ошибке, кроме
ERROR_FILE_NOT_FOUND. Старый безусловный save_fixture/save004 отключён;
клиент save теперь вызывает safe save_current_status. Изменения только в
диагностике, production51 не менялся. Diagnostics8 установлены и SHA проверены;
Lua syntax/Python compile/OpenSpec strict PASS. Новый controller-status-save-win32-
20261012/session67935 запущен; терминальный итог и сохранение ещё не приняты.
Старый X4 PID96032 штатно завершён. Новый PID необходимо читать из процесса.
Приёмка остаётся16/32. Длительный прогон не запускался.

## Актуальная доработка: текущий статус вместо оценки менеджеров

### Повтор current-contracts: терминальный результат

Controller-current-contracts-retry/session23604 и readonly follow-up завершены
exit0. Исправленный hire_setup выдал один prepared; штатный RequestHire sent,
реальная оплата654070Cr, exact actor/seed2803707277279200888, observed arrival.
После смены authority diagnostic passed0 из-за retired goal: это не принимается
за успех новой автономной кадровой цели. Service fixture подготовил условия;
native repairs_initiate hull20→80 подтверждён без счётчика оценщика и оплаты.

HQ сменил реального manager: old seed-6861446903147557245 →
new seed-7877045512791511809, transit0/source_member0, governor unchanged.
Старые наблюдения отвергнуты; новая проекция показывает «Крисс Донел»/ready.
Фабрика needs_attention/resources; service station needs_attention/build/miners.
Все3 station_status assessment/history false. Ownership loss выключил active/
старый Manager; restore того же governor затем дал новую активную проекцию.
UI167 rows, empire18/stats85; mod MD ошибок в проверенном журнале нет.
Текущий X4 PID171068, активного pipe клиента нет.

Приняты 5.3 и5.6 по docs/current-station-status-acceptance-20261012.md:
16/32. 5.1/5.4/6.5 и остальные широкие задачи остаются открытыми. Длительный
прогон не начат; head соответствует установленному production51/diagnostics8.
Квитанции batch-current-contracts-retry.json и read-current-contracts-retry.json.
Сведения об остановленном первом пакете ниже исторические.

### Пакет current-contracts: результат и групповые исправления

Установлены production51 files и diagnostics8 files, SHA совпали. Load007
успешен; controller-current-contracts/session9908 завершён exit1, не активен.
До остановки: runtime active; capacity negative без изменения квитанции/
source-person/seed; remote personnel exact seed/observed arrival сохранён.
На hire_setup диагностический fallback выдал два самостоятельных ответа:
сначала fallback, затем prepared. Второй попал в ответ следующего repair_setup,
и строгий клиент остановился без повторения эффекта. Это подтверждается
debug.log393704.99 и batch-current-contracts.json. Ремонт и оставшиеся сценарии
этого пакета не приняты; запуск не был длительной приёмкой.

Причина исправлена в исходниках: fallback теперь сохраняет только локальную
пометку, итоговый ответ остаётся один. Удалены вызовы двух удалённых assessment
libraries из диагностических library/cue; retired-команды отвечают effects=false.
Ремонтный сценарий читает фактический hull, не удалённый счётчик оценщика.
Проба смены manager допускает отсутствие старого period и выдаёт workstate.
Short runner не вызывает retired trade-decision/quote сценарии. MD/scheduling,
Lua syntax, probe response tests(3), registration tests(3), status fixture и
OpenSpec strict PASS. Последние диагностические исправления ещё не установлены;
перед следующим пакетом проверить состав и перезапустить штатно.

Продолжение после короткого игрового read-back: в исходниках добавлена проверка
binding готового снимка непосредственно перед Publish. До32 station/employee/
seed проверяются против фактического назначения; при смене сотрудника,
собственности, Manager/session или rollback снимок и незавершённый scan
снимаются. Это устраняет показ старого имени до минутного обновления.
MD schemas/scheduling и isolation/refs PASS. Эта последняя правка ещё не
установлена; её игровой read-back включить в следующий согласованный пакет,
не принимать по проверке предыдущей сборки.

По подтверждению пользователя оценка сотрудников станций исключена из кода:
сбор событий производства/торговли/ремонта, история счетов и периодов,
сравнение решений о закупках, расчёт ответственности и оценки удалены.
Два пассивных AI diff оставлены пустыми для совместимости обновления;
Lua-сборщик котировок отключён. Архив исходников находится в
`.cache/tmp/station-boundary-20261011/evaluation-removal-source-before/`.

Строки станций сохранены: текущий сотрудник, работа производства, паузы,
потребности ресурсов/бюджета/шахтёров, текущие подчинённые и запасы.
Введён текущий статус working/needs_attention/paused/ready/unknown/missing_manager.
Сохраняется только последний штатный экономический отчёт; при смене сотрудника
или load старый отчёт не принимается как актуальный. История старого формата
не выводится и очищается при load. Штатное управление станцией не изменено.

Проверены MD/AI schemas и scheduling, isolation/refs, Lua syntax, обновлённый
UI fixture (новый статус без периодов, старые оценки игнорируются, неверные
состояния и время отвергаются), install dry-run 51 files, OpenSpec strict.
Изменение установлено (51 SHA). Короткий load007/read/UI завершён, controller
exit0: исходный штатный manager HQ Тэмманчассат восстановлен сохранением,
governor/Manager active. Фабрика KMT-485: производство ждёт ресурсов, дефицит
energycells/water; HQ XZS-342: без выявленного дефицита, production_total0.
Assessment/confidence/history/from/samples отсутствуют в актуальном evidence.
Вкладка после готовности снимка:115 rows, projection=true,74 assets/2 stations;
empire18 rows/stats85 rows работают. В текущем журнале нет ошибок MD нашего
Assets/Economy. Существующие ошибки сторонних модов не принимаются за наши.
Квитанции: `.cache/tmp/station-boundary-20261011/batch-current-status.json`
и `read-current-status.json`. Это короткая проверка, не полная приёмка:
5.1/5.3/5.4/5.6/6.5 остаются открытыми до нужного read-back.
Долгий полный прогон не запущен. Сведения об установках ниже исторические;
controller820 и controller_current_status завершены; read_current_status exit0,
активного pipe-клиента нет.

Активный change: `add-empire-management-module`, 16/32 принятых задач по обновлённым требованиям.

## Уточнение порядка работы пользователем — 12.10.2026

Сначала завершить весь функционал и доработки мода. До этого выполнять только
необходимые короткие частичные проверки, активно подготавливая игровой мир
командами: корабли, застройщик, ресурсы и условия сценария. Долгий полный прогон
запускать после завершения реализации. Естественное ожидание одной функции
не должно останавливать независимую разработку. Проверки не подменяют реальные
критерии приёмки; открытые задачи остаются открытыми до подтверждения.
## Текущая установка818; native vacate/replace пакет в работе

Production815 без изменений, diagnostics817 установлены:8 SHA совпали.
Controller818/session24779 запущен дляload007 и native station manager vacate/
replace/period/history/restore. Новый сценарий сначала требует production отказ
destination_post_not_free, затем использует native passage same-station для
освобождения поста. Действующий manager не вытесняется прямым dismiss/slot.
Return первоначального тоже только через свободный post и native assignment.
Документ: economic-retirement-and-manager-period-816-20261012.md. Результатов
818 ещё нет; один pipe client. MD/Lua/Python/strict проверены, приёмка15/32.

## Результат предыдущей установки816/read817

Controller816/session51539 и read817 TERMINAL exit0. Ordinary выбрал VHJ-116,
claimsent/1order, requester sector: commandernull — штатный самостоятельный
TradeRoutine. Priority выбрал RED-923,2orders/claimsent/commander совпал.
Bindings сохраняются вread817 без новой покупки. Missing Ship/duplicate mod MD
ошибок в текущем журнале не найдено. Station replacement отказалpostoccupied/
effectsfalse; никаких смен должности не выполнено. Исходныйmanager сохранён.
UI/provision/personnel проверены независимо. Diagnostics817 уточняет ordinary
commander_required=false/expected actual claim commander и общий order evidence.

## Историческая подготовка установки816

Production815 и diagnostics816 установлены:51 production/8 diagnostic SHA
совпали, X4 PID163428. Игра закрыта штатно; один controller816/session51539
запущен для load007 и общего пакета economic negative/priority/retirement,
station manager native replacement/period/history/restore, personnel/read/UI.
Проверка source816 schemas/scheduling/Lua/Python/install dry-run PASS.
Фактических результатов816 ещё нет; приёмка15/32 и полный прогон не начат.
Подготовленный диагностический swap не меняет governor, оценки или arrival;
оба назначения исполняет native Conversations. Если native check запрещает
замену, никаких dismiss/forced slot/повторных действий не будет.

## Предыдущий checkpoint814/read815; source815 был не installed

Runtime production810/diagnostics814; loaded007, X4 PID111220. Controllers813,
814/session80578 и read815 завершились exit0, активных pipe clients нет.
Native list007/title/time1791791925 и loadaccepted; exact remote transfer binding
сохранился source0/target1/same seed/service/flags0/podnull/observed. Повторные
prepare/transfer отклонены effectsfalse. После дальнейшей автономной работы
новая production Transfer receipt заменила terminal старую: read815 unmatched
не отменяет реальную membership и доказанный reload814; не считать это дублем.
Governor ownership loss814: registryinactive, projection0/0, actual старый cue
exists0/stop1, station manager unchanged. Restore того же employee/seed:bound→
new manageractive; read815 projection1/1, oldauthorityinstance_mismatch, status
136rows. Три стандартные UI страницы работают, stale active отсутствует.
Задачи5.5/5.6 приняты по status-ui-acceptance-813-815-20261012.md:15/32.
Source815 исправляет два optional lookup для async negative/cancelled search
в CheckRunningActions/factory subaction retirement. Ошибка first-bad814 exact
$ActionReportDef.$Ship была в журнале393721.87; это не приёмка всей экономики.
Генератор13-script/guards, MD+AI schemas/scheduling, actual caller boundary и
OpenSpec strict PASS. Source815 НЕ установлен; следующий пакет должен включить
оба согласованных исправления, а не маскировать negative как successful ship.
Полный длительный прогон ещё не запускался.

## Предыдущий checkpoint813 и подготовка814

Production810 без изменений, diagnostics814 установлены (8 SHA совпали).
Controller813/session40833 TERMINAL exit0. Реальный remote transfer:
RCU-821 → ZKI-807, key crew_assignment_2_393676.392,
person/seed6145579947266952518. Target недокован, подготовлен в20–25km.
Сначала native podarrival393686.409, затем null; source0/target1, тот же seed,
service, transit0/scheduled0/temporary0; production observer стал observed.
UI status29/body96, empire342/stats405; provision и финальный read выполнены.
Новый save_007:91646978 bytes compressed,748297818 uncompressed,
SHA e28f7d00b07df9f9d777cfa135befcd90738a93f4e90b912e4da812593428b2f;
gzip CRC и stable stat PASS. Прежние слоты не перезаписывались.
Controller814/session80578 запущен: загрузка007 и пакет persistence/no-replay,
утрата ownership одного actual governor, старый authority/cue/UI, возврат того
же employee и независимость station manager. Результатов814 ещё нет.
Эффекты этого сценария диагностические; production функция не менялась.
Source814 MD schemas/scheduling, Lua syntax, Python compile, strict OpenSpec PASS.
На этом историческом checkpoint приёмка была13/32; полный прогон не запускался.

## Исторический checkpoint811

Source812 diagnostics(НЕ installed): добавлен отдельный no-replay remote crew
сценарий — actual source crew на докеHQ, target недокован в20–25km, production
RequestTransfer и точное read-back key/source/target/person/seed/membership/
role/transit/scheduled/pod. Никаких injected arrival/receipts. Новый typed
save_remote_personnel использует прежний native free-slot механизм с отдельным
marker, не очищает старые checkpoints и не перезаписывает прежние слоты.
MD/Lua/Pythonsyntax/OpenSpec strict PASS. Core production не менялся;
runtime/install811, loaded006, controller отсутствует по terminal811/process
audit812. Новый remote путь и persistence ещё НЕ проверены в игре.
Причинный trade audit812 подтвердил существующие ограничения same-zone/native
search/небольшего расстояния/реальной оплаченной покупки; неподтверждённый новый
планировщик или правило обвинения менеджера не добавлялись.

Installed811=production810+diagnostic prepare/priority cases. Production51 и
diagnostics SHA совпали, install811.json; X4 нормально перезапущена черезSteam,
loaded006 без перезаписи save. **Controller811/session36637 TERMINAL exit0**.
Нет активного pipe клиента. Пакет создал2 actual транспорты ISJ-044/PFU-098 с
pilot/cargo capacity; claims/orders/results не подставлялись. Ordinary request
finished/exhausted без покупки; positive ordinary остаётся непроверенным.

Priority393690.564: prepare cluster26/cursor42 →candidate cluster46/cursor4 →
finished/candidate_found/committed1. Реальный выбор YDU-207/0xcc3c; nativeorders3,
claim_sent, commander0x4c197==expected0x4c197, purchase null. Следующее read
сохранило тот же результат/ship/orders3: нового эффекта нет. Весь scope native
списка готовится перед выбором; fixture корабли не принуждают выбор алгоритма.

Log811: duplicate cue0, legacy SearchDone errors0, ReadOwnedOrderEvidence errors0.
Provisions/status29/body96/empire342/stats405 и final read работают. Сохранённый
crew transfer observed/key/person/membership сохранён. Это узкие positive priority/
negative ordinary/legacy-load/UI границы, не полная3.8 или6.4. Приёмка13/32.
Следующий пакет должен охватить оставшиеся обычное назначение/asset loss/authority,
дальний персонал и живые причинные оценки, после необходимых source доработок.
Подробные факты — docs/economic-search-short-811-20261012.md.

## История checkpoint809–810

Source810(НЕ installed): по log809 исправлен legacy completion guard — старые
сохранённые Request без SearchDone не должны читать отсутствующее поле или
начинать новую continuation. Condition проверяет SearchDone? до значения.
Убраны неиспользуемые captures static child templates и их вводящие в заблуждение
state fields в diagnostic read. Build/check_adapted/MD+AI/scheduling/caller806 PASS.
Install/runtime остаётся809/006; нет активного controller. На log snapshot810:
duplicate cue0, ReadOwnedOrderEvidence errors0, legacy SearchDone errors399.
Эта локальная ошибка не повторяет effects; source guard ожидает следующего
пакетного install/reopen вместе с prepared positive/priority/legacy load проверкой.
Широкая clean migration и3.8 не приняты.

**Controller809/session51226 TERMINAL exit0**: native load006 accepted; поиск
issued393682.419 →cluster24/cursor15 →cluster31/done1 →finished/exhausted,
searchcue invalid после штатной отмены, purchase null/ship null. Ошибка completion
807–808 исправлена в реальной игре. Status frame29/body96, empire342/stats405
открылись; provision/read выполнены. Нет активных pipe controller по terminal809.
Отрицательный поиск принят как узкая граница; большая positive выборка/priority/
authority/load и полная3.8 остаются open. Ни одно широкое task checkbox не закрыто.

Записи ниже описывают запуск809 до этого terminal результата.

Source/install809: исправлены две реальные ошибки короткой пробы807–808 —
completion вынесен в отдельный sibling cue с1s checkinterval; перенесённые lifetime
cue получили собственные уникальные имена для загрузки старых сохранений.
Search result сохраняется в ActionDefinition отдельно от эфемерного cue.
Добавлена общая read-only библиотека ReadOwnedOrderEvidence из существовавшего
военного read-back; военная и экономическая проекции используют одни guards и
реальные order refs. Экономика больше не называет действующий приказ планом и
не считает наличие выбранного Ship подтверждением отправки.

Build13/check_adapted/MD+AI schemas/scheduling/Lua syntax/caller fixture806/
OpenSpec strict PASS. Production51 и diagnostics SHA проверены; install809.json.
X4 после штатного close121652 запущена черезSteam без дополнительных flags.
**Controller809/session51226 RUNNING**: единственный клиент, загрузка006 и
короткий поиск→provision/UI. Не запускать второй pipe client и не restart до
terminal. Результат809 ещё не подтверждён. Полный длительный прогон не начинался;
13/32, задачи3.8/5.5 и широкие критерии остаются открытыми.

Controller807/session69406 TERMINAL0: load006 accepted, governor active, штатные
UI страницы работают; search start context_unavailable/effectsfalse. После
инициализации экономики Controller808/session57512 TERMINAL0 отправил один
настоящий Request_Commandeerable_Freighter: курсор дошёл до31/exhausted, но
done1/committed0 сохранялся во всех16 чтениях. Покупки нет. Это FAIL completion,
не успешное завершение поиска. Debug log показал3 duplicate native lifetime cue
при загрузке. Оба наблюдения исправлены source809, ожидают короткого повторения.

## История checkpoint788–808

- Source806: замкнуты все4 синхронных caller порционного поиска. Pending запросы
  попадают в reports/sub-actions, Upkeep/factory не покупают параллельно поиску;
  их исходный fallback покупает только после полного отрицательного результата.
  Отмена factory помечает ещё не имеющий ship search sub-action Disregard.
  Actual XML caller flow fixture806 PASS(4 calls+nonproduction factory), build/
  check_adapted/MD+AI schemas/scheduling PASS. Source805 был неполным и НЕ
  устанавливался; source806 также пока не установлен. Широкая3.8 остаётсяopen.

- Source805: порционный экономический поиск реализован воспроизводимым
  batch_economic_ship_selection;≤32 шага/порцию,1s delay, сохранены stock priority
  order/candidate checks/effect tail. ActionReports удерживает incomplete до
  completion; UI показывает ожидание. Утрата authority/requester и asset loss
  пересверяются. Build13/check_adapted/MD+AI schemas/scheduling/Lua syntax PASS.
  Документ economic-search-boundary-803-20261012.md дополнен реализацией805.
  НЕ установлен: runtime остаётся install800/loaded006, активных pipe clients нет
  по последнему terminal802. Игровой bounded поиск и широкая3.8 ещё не приняты.

- Controller802/session37334 TERMINAL exit0: новый same-dock employee сохранён и
  восстановлен006, exactkey/person/seed/role, source0/target1/transit0/scheduled0/
  temp0; Manager active, assignment/payment не повторены. Документ crew-persistence-
  800-802-20261012.md. Дальний transfer и новая governor persistence остаютсяopen.
  Нет активного pipe controller; X4 loaded006/install800.

- Controller802/session37334 RUNNING по poll803: native list подтвердил новый006,
  load006 accepted. После завершения read сравнить exact person/seed/source/target
  membership/role/native transit flags; save acceptance не заменяет persistence.
- Source audit803 нашёл unbounded economic candidate search. Простое cap32 не
  внесено: оно могло бы объявить отсутствие ship и отправить лишнюю purchase.
  Нужен resumable native candidate scan/incomplete blocks purchase; контракт и
  затронутый Request_Commandeerable_Freighter записаны economic-search-boundary-
  803-20261012.md. Next implementation boundary3.8, без переписывания stock strategy.

- Controller800/session52699 TERMINAL exit0: native crew_assignment_1_393644.637
  observed; person4700167841469765590 sourceXMG-481→targetOBI-268, source0/target1/
  role service/transit0/scheduled0/temp0. save_checkpoint requested save006 free.
  Новый file91713616bytes/uncompressed748271151/gzipCRCpass, SHA561aee137d8a564f
  be2d7d5ce9169303b11288c9eea6f5cc1762be70085eeca4 (save800-file.json).
- Controller802/session37334 RUNNING: единственный native save-menu load006 после
  штатного console close/Steam restart, затем только read/provision/UI. Source/
  install800 неизменны. Не запускать другие clients до terminal802; employee
  persistence ещё не подтверждена reload. Старые004/005/autosave не перезаписаны.

- Source/client801: --save теперь валидирует штатное имя saveNNN/autosave01–03/
  quicksave вместо узкого списка004/005/009. Native save-menu valid filenames/list/
  IsSaveValid gates сохранены, произвольные paths запрещены. PythoncompilePASS;
  READMEdiagnostics описывает checkpoint request≠filecompletion и nooverwrite.
- Controller800/session52699 RUNNING подтверждён poll801; X4 PID23768 respondingTrue,
  пока нет load800/batch800 результатов. Единственный pipe controller, не restart.

- Install800: production795–798/diagnostics799 установлены51files+diagSHA verified,
  validate800 MD/scheduling/Luasyntax PASS. Старый X4 штатно завершён, Steamlaunch.
  Единственный controller800/session52699 RUNNING, ждёт native load005.
- Batch800 создаёт same-dock crew world → один native role transfer → bounded
  read exact receiptkey observed/native_crew_arrival_observed (до13reads/3s) →
  ui_status → save_checkpoint. Нет arrival → exception, save/replay не выполняются.
  PythoncompilePASS. Запрос сохранения не равен готовому файлу; после terminal
  проверить новый slot/file/gzipCRC/hash/native list перед reload. Old004/005/autosave
  не перезаписывать. Другой pipe client до terminal800 не запускать.

- Source diagnostics799 (не установлен): save_checkpoint использует штатный
  ReloadSaveList/GetSaveList(validSaveFilenames)/SaveGame и только первый свободный
  saveNNN; собственный persisted no-replay marker $tm_empire_checkpoint_save,
  прежний $tm_empire_validation_save не сбрасывается. Active projection preflight,
  recheck marker перед native request, requested не означает savecompleted.
  Отдельный путь нужен для persistence новых назначений после исходного005;
  existing saves не перезаписывает. CLI/prefix подключены, Lua/PythonsyntaxPASS.
  Pending production795–798/diag799; install794/runtime controllers terminal.

- Batch797 terminal exit0: один native_analysis подготовленного794мира, без денег/
  replay. Реальная KMT evidence money67800/need135600/restricted0, responsibility
  insufficient_provision/medium/scopeprovision, recommendation+67800Cr; явно не
  доказаны влияние на общий результат/ошибкаmanager. XZS unknown/low, samples2.
- Source798 (не установлен): убраны ведущие'; ' в single provision reason и
  recommendation; diagnostic budgetreceipt сохраняет transfer result и выводит
  playerbefore/after для следующей проверки unknown794. Common.xsd33392 contract
  result — фактически перенесённая сумма, не boolean. Unknown не сбрасывался,
  денежный эффект не повторялся. Итоговый MD/scheduling validate798 PASS.
  Pending production795–798/diagnostics798, install794. Controllers terminal.

- Controller794/session37474 TERMINAL exit0: source793 fresh-load boundary подтверждён
  без diagnostic native_analysis. На6ом bounded read обе станции получили fresh
  from/observed393656.77 вместо ожидания15–30min; low/unknown причинность корректна.
- Причинная world preparation794: supply observed+50000Cr/rules opened;
  budget withdrawal real station150000→67800Cr/need135600Cr, но diagnostic stateunknown
  (совокупный transfer/player read-back не совпал). Денежное действие не повторять.
  Native analysis не вызван из-за guardedunknown; следующий шаг — read/diagnose
  существующего budgetreceipt и штатное наблюдение подготовленного мира, без replay.
- Source796 (не установлен, вместе795): RecordCrewPodArrival принимает deadline
  только при exact seed исходной receipt, не по одному template. Validate796 PASS.
  Нет активных pipe controllers; install794, broad tasks13/32.

- Source795 (не установлен): ObserveTransfer сохраняет protected recovery reasons
  player_helm/manual_or_priority/order_queue_incomplete от двух recovery helpers,
  не перезаписывает их общим10min arrival timeout; после срока stateunknown,
  до срока pending stateсохранён. Нет assignment/recovery replay или successfake.
  MD schema/scheduling validate795 PASS. Controller794/session37474 RUNNING
  подтверждён poll795, всё ещё ожидание native load/пакета; другой клиент не запускался.

- Install794: production793/diagnostics78951files+diagSHA verified; X4 штатно
  перезапущён Steam. Единственный controller794/session37474 RUNNING, ждёт load005.
  Batch794 ограниченно читает fresh station evidence без native_analysis (до7reads
  через3s) для boundary793, затем отдельная причинная подготовка supply→budget→
  native_analysis→provision/UI при observed preconditions. PythoncompilePASS.
- Read792 уточнил: KMT account100000Cr/need135600Cr/traderestricted1, поэтому
  budgetsetup790 отказал корректно. Сначала native world supply setup открывает
  resource buy rules/переводит50000Cr, затем budget withdrawal моделирует50%need.
  Оценка не меняется диагностикой. Probe expected-prefix guards added for этих
  команд и provision_read; другие pipe clients не запускать до terminal794.

- Batch792 terminal: один native_analysis requested немедленно дал fresh observations
  обеих станций, from/observed393800.759, KMT production/observed/low confidence,
  XZS other/unknown/low. Причина blank791 — старый период до штатного15–30min ticker,
  не поломка записи. Неполный новый период не обвиняет менеджера.
- Source793 (не установлен): Assets.Scan однократно запрашивает штатный
  GenerateShortageData для новой пары active ManagerCue/ObservationSession,
  когда analyzerwaiting и соблюдены native15s после LastRunTime. Pair marker
  записан до сигнала, обычный stock ticker сохранён, нет fullrefresh каждый tick.
  MD schema/scheduling validate793 PASS. Diagnostics789 также новее install787.
  Следующая короткая load boundary должна доказать fresh без diagnostic analysis.

- Controller787/session44939 TERMINAL exit0: все6priority fixture phases passed1;
  status→empire→stats→status реальные frames/tables работают. Read790 native crew
  assignment_1_393644.692 observed393672.806: exactperson/seed, targetrole/source0/
  transit0/scheduled0/temp0. No duplicate transfer sent.
- Batch790 budget preparation unavailable (денежный эффект не наблюдён).
  Ошибка вызова provision вместо wire provision_read исправлена read-only791,
  без повторения budget effect. Read791 обе station observations отсутствуют:
  reason fresh_economic_observations insufficient, purpose/from/samplesnull.
  Следующий источник проверки: порядок ObservationSession/load и native economy
  first-run. Не принимать причинные оценки по отсутствующим данным.

- Controller787/session44939 RUNNING по poll789; native save-menu load005 accepted,
  X4 PID52716 respondingTrue. Теперь ожидает/выполняет batch787; не запускать другой
  pipe controller. Load accepted не означает, что проверки batch прошли.
- Source diagnostics789 (не установлен): provision reader дополнительно выводит
  реальную station_responsibility со station/employee/from/observed/kind/confidence/
  scope/reason/recommendation из ReadStationEvidence. Не создаёт synthetic evidence
  и не изменяет production assessment. MD schema/scheduling validate789 PASS.
  Использовать вместе с существующей world budget/supply preparation в следующем
  согласованном пакете; не перезапускать игру ради одного read-back поля.

- Change add-empire-management-module: ready,13/32 принято. Полная приёмка и
  длительный прогон не начаты. Последняя strict validation786 PASS.
- Installed787 включает production779–784/UI778/diagnostics781. Generator787
  воспроизводит bounded DefendArea/Recon; пересборка изменила только эти2файла.
  check_adapted_manager/validate787 IncludeNativeCopies PASS;51production files
  и все diagnostics SHA verified. Семь Lua fixtures786 PASS.
- Единственный controller787/session44939 RUNNING, подтверждён poll788;
  ждёт native save-menu load005. Не запускать параллельный pipe client и не
  считать timeout наблюдения завершением или основанием для restart.
- Batch787: saved supply, native crew same dock, passenger/helm/manual/priority
  с restorefinally, military world preparation, status→empire→stats→status.
  Все новые игровые результаты пока не подтверждены.
- Предыдущая timeline777: read785 подтвердил5own military orders в2HoldSpace
  целях и новую оплаченную экономическую покупку1190675Cr. Это не завершение
  боевой задачи/торговли. Doc military-orders-785-20261012.md.
- Стройка timeline761 завершена read776 после реального handoff772; материал
  подготовлен free773, paid-material/factory/plot gates этим не приняты.
- Следующий независимый блок: живые причинные оценки станций и persistence
  нового сотрудника; существующие math fixtures не заменяют эти сценарии.

## Журнал предыдущих пакетов (исторические состояния)

### Пакеты774–787: исторические записи

- Install787: первая попытка установщика отказала до копирования по SHA двух
  вручную изменённых военных подцелей. Ограничения782–783 перенесены в generator
  bound_military_ship_selection; пересборка изменила только DefendArea/Recon.
  check_adapted_manager+validate787 IncludeNativeCopies PASS. Production51files
  и diag all SHA verified; source779–784/UI778/diag781 теперь установлен787.
- Единственный controller787/session44939 RUNNING: ожидает native save-menu load005
  после Steam запуска; старый X4 штатно завершён. Batch787 включает saved supply,
  native crew same dock, priority/passenger/helm/manual/restore, military setup,
  status→empire→stats→status. Все эффекты guarded/no replay, priority restorefinally.
  Не запускать другой pipe client до terminal. Full прогон не начат.

- Source batch786: актуальный OpenSpec ready13/32/context ru; strict validatePASS.
  Семь существующих Lua fixtures status/orderguard/personnelcontract/seed/hire/
  supplypayment/purchasereceipt exit0, receipt fixtures786.json; doc source-batch-
  786-20261012.md. Накопленная source779–784 ещё не установлена, install777 остаётся
  runtime. Это source boundary evidence, игровые широкие задачи не закрывались.

- Batch785 terminal exit0/read+ui_status: projection показывает реальное военное
  исполнение sent у5own ships в2HoldSpace целях (2Близнец Хевы IV Бухта/3Большая
  биржа I), проверенные native orders/claims. Doc military-orders-785-20261012.md.
  Новая оплаченная экономическая покупка built/paid1190675Cr и Hermes transfer
  к экономической задаче observed; торговый результат этим не принимается.
  UI frame29/tables2/body_rows95/snapshot77assets/tasks12, broad gatesopen.
  README вводный статус обновлён по подтверждённым результатам; без release claim.

- Source784 (не установлен): ReadMilitaryExecution сообщает selectionpartial
  при native subgoal military_ship_sample_incomplete; ReadNativeMilitaryTasks
  добавляет русское объяснение частичного подбора к причине цели. Состояние задачи
  по-прежнему sent только при собственных live orders/точных claims; partial подбор
  не выдаётся за выполнение. validate784 IncludeNativeCopies и действующий
  empire_status_fixture.lua PASS. Pending production779–784/UI778/diag781,
  install777; controllers terminal, broad tasks пока13/32.

- Source783 (не установлен): Recon выбор PotentialShips32 со штатным shuffle и
  incomplete reason, DefendArea оба прохода StandbyKeys ограничены32 со shuffle
  перед выборкой. Validate783 IncludeNativeCopies итоговый PASS, включая guard782.
  Native original files не изменены. Ограничены asset checks/effects, полный stock
  find/shuffle и суммарные вложенные пространства ещё не объявлены bounded.
  Coherent pending source779–783/UI778/diag781; install777/live goalsread780.

- Source782 (не установлен): адаптированный DefendArea выбор найденных own fight
  ships ограничен32 за проход вместо PotentialShips.count. Штатный shuffle остаётся,
  sample incomplete имеет отдельную причину/UI text, очищается перед новой выборкой.
  Это ограничивает проверки/claims/orders, не обещает bounded native find/shuffle
  и не принимает широкую large-empire задачу3.8. validate782 с IncludeNativeCopies
  и Lua syntax PASS; повторить после последнего clear-reason guard при следующем
  пакетном source check. Последние live military цели read780, controllers terminal.

- Read780 terminal exit0: active governor/goals2/claimed2; штатные HoldSpace цели
  для Близнец Хевы IV Бухта и Большая биржа I, subgoals2 каждая. Четыре fighter
  operational. Их command=null не является доказательством отсутствия приказа:
  diagnostic ошибочно читал ship.command вместо pilot.commandaction.value.
- Source781 (не установлен): military fixture read теперь показывает actual pilot,
  pilot commandaction/value/target и orders.count. Projection завершённого supply
  consumed/resultcompleted показывает native_supply_delivery_observed независимо
  от старого progress reason сохранённой receipt; receipt/payment/effects неизменны.
  MD schema/scheduling validate781 PASS. Next coherent source production779+781/
  UI778/diag781 новее install777. Нет активных pipe controllers.

- Controller777/session17816 TERMINAL exit0: native load005 accepted, batch777
  active governor/read saved supply consumed/resultcompleted/inventory1/paid6118Cr,
  native military_setup ownerless→player sector Близнец Хевы IV Бухта,
  military_fleet_prepare создал4own operational fighters185a08/185a13/185a1e/185a29.
  Read сразу после создания goals0; выполнение флота не принято. Supply reason
  остался old native_supply_build_in_progress несмотря на terminal state: UI/read
  normalization source770 ещё не доказана. Нет активного controller.
- Source779 (не установлен): ResumeMissingCrewTransport/ResumeExistingCrewActor
  проверяют shared CheckPersonnelShipControl для source и target непосредственно
  перед recovery effect. Ручные/priority/неполная очередь удерживают восстановление,
  reason сохраняется, attempt не расходуется, повторное назначение не выполняется.
  Diagnostics orders исправлен orderqueue.count→orders.count (штатное свойство).
  MD schema/scheduling validate779 PASS. Source UI778 также новее install777.

- Source UI778 (не установлен поверх777): четыре русских причины crew authorization/
  employee unavailable/recycling manager pending/unconfirmed; syntax Lua PASS.
  Controller777/session17816 всё ещё RUNNING по poll, новых load/batch receipts нет.
  Batch777 до запуска подготовлен с bounded4x3s ожиданием bound→active; Python
  compile PASS. Не создавать второго клиента save-menu/role pipe.

- Install777: production770/UI774 + diagnostics777 (включая military world
  preparation775 и bounded per-fixture ship read-back) установлены; 51 production
  file verified installer, все diagnostic files SHA verified. MD schema/scheduling
  validate777 PASS; batch777 Python compile PASS. Предыдущий X4 штатно завершён.
- X4 через Steam PID33660 (последнее RespondingFalse во время старта, не считать
  падением). Единственный controller777/session17816 RUNNING подтверждён poll,
  пока ожидает native save-menu load005. Не запускать другие pipe controllers
  и не перезапускать игру только по timeout наблюдения. Далее load777/batch777:
  active read → saved supply read → military_setup → military_fleet_prepare →read.
  Подготовка создаёт условия мира, не native goals/orders. Полный прогон не начат.

- Read776 terminal exit0: X4 PID53148 respondingTrue; прежняя expansion
  construction_1_393644.644/build8aff observed/native_expansion_modules_observed
  observed395173.253. Native processor building0/buildnull. Реальная очередь после
  смены governor завершена; материалы free773, paid-material gate остаётся открыт.
  Military prepare775 подключён к CLI choices/dispatch; Python compile PASS.

- Source diagnostics775 (не установлен): military_fleet_prepare создаёт четыре
  собственных вооружённых аргoнских истребителя в normal zone ранее подготовленного
  собственного сектора. Требуется active governor; повторное создание запрещено
  сохранённым State.$MilitaryFleet. Цели/claims/orders/receipts не подменяются.
  MD schema/scheduling validate775 PASS; Lua syntax774 повторно PASS для текущего
  source. Короткая игровая проверка выполнения флотом ещё не проведена. Включить
  в ближайший общий install вместе с production770/UI774, без отдельного restart.

- Batch772 terminal: hired builder0x9a147 deployed1/native module0x4c244,
  observed394362.98/commandbuildingto0x4c324. Реальный handoff после смены
  governor accepted: oldmanager/goalinvalid→active TM_PlayerManager/Econ_Manager,
  keyconstruction_1_393644.644/build8aff unchanged, spent512702Cr unchanged,
  no payment/queue creation. Doc construction-handoff-761-772-20261012.md.
- Batch773 terminal: construction_resources prepared (paid_supply=false),
  native processor0x4c245/build8aff building1,total540s/step60s,module0x188be8.
  Штатная стройка идёт под новым manager, повторный handoff same key/spent.
  Не ждать ради одной функции: продолжать независимую сборку; позже read
  completion. Не считать free resource preparation платной поставкой.
- Source UI774 (не установлен): русские explanations для8handoff/loss/payment
  состояний, нет нового UI/исполнителя. Lua syntax774 PASS. Coherent source
  production770+UI774/diagnostic768 новее install759/diag760. Active game пока
  оставить для наблюдения стройки; source load race пакет далее при установке.
- Все controllers терминальны; единственный текущий X4 PID53148/save005 timeline
  с восстановленным governor и running native build. Goal13/32 accepted.
- Source production770 (не установлен): исправлена подтверждённая load race
 761 fresh plan age393644.644→delayed ValidationLoaded reset393649.401.
 ValidationLoaded сразу invalidates MD-only evidence. Шесть остальных Loaded
 handlers capture saved key при load через signal_cue_instantly и выполняют
 delayed5s reconciliation только при совпадении current key. Все прежние
 native guards/unknown/no-replay сохранены. XSD/scheduling770 PASS. Doc
 load-receipt-boundary-770-20261012.md. Нужен короткий live load boundary пакет.
- Latest install всё ещё production759/diag760, X4 PID53148/save005 timeline,
 active governor после766. Нет активных pipe controllers. Builder pending
 native deployment, queue/payments сохранены. Не переотправлять заказ.
- Batch767 terminal exit0: текущий governor active после766; native builder
  всё ещё sent/deployed0, корабль послеwarp вышел изstorage zone в0xda67,
  distance17.56Mm. Handoff удержан effect_unreconciled, key/build/spent512702Cr
  unchanged. Не считать handoff accepted и не повторять hire/payment.
- Source diagnostic768 (не установлен): после BuilderNear warp добавлен штатный
  reinitialise_control_entities (common.xsd21353: restart suitable AI scripts),
  чтобы native navigation начиналась из подготовленной позиции. Не изменяет
  order/employee/receipt/deployed/build progress. XSD/scheduling PASS; live
  ещё не проверено. Текущий BuilderNearAttempt уже выполнен, не сбрасывать его
  ради retry. Следующая свежая timeline/когерентный install использует новый prep.
- Production759/diagnostic760 установлены761, X4 PID53148/timeline005; активных
  pipe controllers нет. Предыдущие process/running/source строки исторические.
- Controller761/session46073 TERMINAL exit0; batch761 validating после12s.
  Последующее read763 подтвердило queued build0x8aff/keyconstruction_1_393644.644,
  native funding observed463702Cr + hire50000Cr, spent512702Cr. Сам mod нанял
  builder0x9a147; local_owned_builder правильно отказался создавать лишний.
- Batch764 terminal: paid hired builder диагностически перенесён из34.7Mm
  к storage3891.5m, native DeployToStation/order/receipt неизменны, deployed0
  на момент read. Не ждать естественный перелёт, не менять deployment флаг.
- Batch762 release реально inactive/manager unchanged1, Assign option unavailable:
  сообщение результата снятия ещё открыто. Batch765 back закрыл сообщение,
  пустые options; новых назначений не было. Batch766 штатный default→more→roles→
  assign exact choices SENT; затем active read и construction_handoff.
  Controllers763/764/762/765/766 terminal; активных pipe нет. Не повторять
  payment/queue/assignment. Сначала оценить JSON766 итог handoff и binding,
  затем продолжать. Не заменять snapshot queued реальной приёмкой всех3.4.
- Controller761/session46073 RUNNING подтверждён последним poll. X4 PID53148,
  respondingTrue/CPU95.52; пока save-menu ожидание, нет batch761 результата.
  Не запускать batch762 до terminal761 и проверки реальной queued expansion.
- Temp batch762.py подготовлен/Pythoncompile PASS (не запущен): baseline
  active+queued, handoff текущего owner→native dialog release exact choice→
  inactive readback→native dialog assign exact choice→bounded active wait→
  handoff+read/UI. Не создаёт платежи/очередь/лицензию/виртуального governor,
  при отказе выбора не угадывает пункт и не повторяет effect. После ошибки
  обязательно inspect current binding перед любой восстановительной операцией.
- Source diagnostic762 добавляет Goal.exists preflight expansion перед issued,
  чтобы отсутствующий настоящий экономический cue не исчерпывал world fixture.
  XSD/scheduling PASS; не установлен. Production759 всё ещё установлен761.
- Установка761: production75951файл и diagnostics760 SHA verified; прежний
  X4 штатно завершён; Steam launch без новых параметров. Controller761/
  session46073 RUNNING подтверждён. Единственный контроллер: native load005,
  blueprint preparation→expansion_native_fixture→до6reads*2s→own builder→
  construction_handoff→native_analysis/read/UI. Пока результатов нет.
  Проверяет живую очередь/идентичность, не моделирует завершение или платежи.
  Проверка после настоящего завершения старой authority ещё отдельный этап.
- Batch758: setup/passenger/helm/manual/priority/restore passed1; PersonnelReason
  совпал с common ship guard. Нет принятых новых broad tasks: полный effect
  coverage3.7 и hire/training вызовы с отказом ещё открыты. Luasyntax760 PASS.
- Source production759/diagnostics760 теперь установлены761; следующие
  source-newer/старые running758 строки исторические, их заменяет этот блок.
- Controller758/session62127 TERMINAL exit0; batch758.json готов. Приоритетные
  фазы выполнены, результаты нужно оценить по passed/personnel_reason.
- Diagnostic760 (не установлен): expansion_native_fixture использует реальный
  tm_empire_economy_cue вместо diagnostic State; construction_handoff вызывает
  production ReconcileQueuedExpansionOwner, сообщает old/new authority,
  сохранность key/build/spent и native queue. Не создаёт receipt/queue/payment,
  не меняет lifetime; отказ старой активной authority оставляет всё как есть.
  XSD/scheduling PASS после исправления cue return переносом в library.
- Source construction759 (не установлен): queued handoff теперь блокируют
  pending Funding/Plot/Builder только той же станции либо без station identity.
  Глобальный последний receipt другой станции ранее блокировал чужую очередь.
  Native queue/claim/provenance/paid bookkeeping checks сохранены; никаких
  платежей/повторной стройки. XSD/scheduling PASS; live handoff gate открыт.
- Controller758/session62127 всё ещё RUNNING подтверждён poll; X4 PID33616,
  CPU11.25 при startup, save-menu pipe ещё ждёт. Не создавать второй клиент,
  не перезапускать по таймауту наблюдения. Результаты batch758 отсутствуют.
- Установка758: прежний X4 штатно завершён; production75751файл и diagnostics758
  установлены/SHA verified, Steam launch без новых параметров. Controller758/
  session62127 RUNNING подтверждён: native load005 → короткий batch758.
  Не создавать второй controller; poll именно62127/receiptJSON. Новый report
  сравнивает PersonnelReason с CanUseOwnedShip для passenger/helm/manual/priority;
  их passed требует обоих guards. Source758 XSD/scheduling PASS. Результат
  ещё не получен. Следующие installed749/source-newer строки исторические.
- Installed production749/diagnostics752,51production SHA и diagnostic copies
  verified. X4 PID42132, native load save005 accepted752. Controllers752/
  session29015 и754/session33666 terminal exit0; активных pipe клиентов нет.
- Source production757/diagnostics755 новее установки. Personnel shared
  CheckPersonnelShipControl применяется в RequestHire до оплаты, AssignPaidHire
  после оплаты/до назначения, RequestTransfer source+target, RequestSeminar
  до изменения навыка/инвентаря, legacy CrewExchangeChecked до approval.
  Helm/current+queued override/priority/loop, bounded32 scan. XSD/scheduling757
  PASS; новые guards не получили live negative acceptance. Не менять replay
  sent/unknown, не возвращать оплату без real native evidence.
- 752→754 native assign_hired_actor role transfer: source0x1859c2,target0x1859cc,
  person10619398833150267955/seed-7827345240559283661. Same native dock0xcb3f,
  target member1/source0/transit0/scheduled0/temp0. Production observed393672.81,
  issued393644.672/reasonnative_crew_arrival_observed. Far arrival/persistence
  нового назначения этим не доказаны. Legacy bulk в одном доке748 тоже прибыл;
  прежний far unknown нельзя переотправлять или превращать в observed.
- 754 реальные passenger/helm/manual/priority/restore passed1. Governor/member
  unchanged; passenger pilot unchanged1. Manual/priority Wait timeout60s,
  реальные flags+queue сохранялись до read. Причина исчезновения старого
  бесконечного Wait750 не установлена. Doc crew-priority-short-752-754-20261012.md.
- Diagnostic755 report выбирает claim.goal того же manager во всех фазах:
  setup может получить native Start claim до report; это не сбой защиты.
  Пустой cockpit создаётся непосредственно перед helm, чтобы manager не
  успевал назначить пилота до игрока. Не установлен.
- Paid supply7426118Cr/satellite0→1/build88e4 completed/consumed; save005 CRC/SHA,
  native save/load745/no replay confirmed. Doc paid-supply-load-742-745-20261012.md.
  RestoreSupply уже instantiate=true, old terminal in_progress reason после
  load748 остаётся: actual cue trace нужен, не менять платёж/stock/result.
- Save004/autosave01 не перезаписывать. Новый save005 пригоден для коротких
  пакетов; save_validation marker предотвращает повторную запись в нём.
- Следующий coherent install: production757+diag755; короткий пакет guards
  personnel/hire/training + оставшиеся remote/lifecycle/construction границы.
  Не ждать естественной подготовки мира; использовать диагностические команды.
- Change13/32 accepted,19 open. Полный≥2h не запускался. Сначала закончить весь
  функционал и короткие gates, затем общий длительный прогон всех доменов.



Следующие записи описывают прежние версии/процессы; текущие authority/source/
installed/controller приведены в checkpoint выше.

Пакет731–733 terminal: native service registration и ремонт20→80/count1
подтверждены; expansion construction_1_393633.039 observed394363.001,
reason native_expansion_modules_observed, processor building0/buildnull.
Документ short-build-repair-731-733-20261012.md. Исправлена диагностическая
ошибка двойного ответа RepairRead (source732, не установлена); schema и
Python syntax PASS. Installed716/diag721; Lua723/MD732 ждут общего обновления.
Ни paid restock, ни все условия construction этим пакетом не принимаются.

Source production734: исправлен orphan неоплаченного supply quote после
утраты authority. Watcher наблюдает quote_requested/quoted; terminal до
оплаты освобождается после старого claim, payment intent остаётся unknown.
Документ supply-authority-reconciliation-734-20261012.md; XSD/scheduling PASS.
Не установлено, live lifecycle/payment probes остаются открытыми.

Установка737: штатно завершён прежний X4, production734 установлен51файл/
SHA verified, diagnostics736 все файлы SHA verified; Steam launch без новых
параметров. X4 PID54844. Единственный controller737 session42996/Python15984
запущен: load autosave_01→короткий supply adapter/UI batch. Результат ещё не
получен, не создавать второй pipe-клиент и не повторять эффекты.
Supply fixture736 готовит docked own scout у известной NPC-верфи, не меняет
отношения/кошелёк/запас; QuoteRestock→StepRestockDelivery использует production.
Read сохраняет исходную receipt reference, не подменяет квитанции. XSD/MD
scheduling validate736 и Lua syntax680 PASS; CLI включает новые supply modes.

Пакет737 завершён exit0: снабжение rejected_before_effect→consumed,
price empty, без оплаты. Доказанная runtime причина — invalid MD string
key satellite_mk1. Исправлено738: фиксированные ware/amount значения→Lua
price map. MD XSD/scheduling+supply_payment fixture (новая wire форма и
no-replay/manual)+empire_status fixture PASS. Русские supply reasons739.
Installed production738/UI739 51SHA verified, diagnostics736. X4 PID56116,
единственный controller739 session32930 жив; load autosave_01/supply/UI/
свободный save_validation. Не создавать второй pipe или повторять эффекты.
Документ supply-wire-boundary-737-739-20261012.md. Результат739 ещё не получен.

Пакеты739/740 terminal exit0. Paid supply_1_393634.116: ship187753,
NPC wharf c33c, price/paid6118Cr, satellite0→1, nativebuild8747;
payment build_recorded. Read740: build.exists0, receipt всё ещё build_observed.
Raw native/Lua build equality не позволяет завершить согласование; точные
типы нужно прочитать расширенным diagnostic741, причина преобразования ещё
не доказана. Source741 заменяет зависимость от исчезающей ссылки durable
buildtoken: MD сохраняет исходную строку native build, Lua подтверждает token
только после C.GetBuildTaskInfo/SetBuildTaskTransferredMoney. MD completion
сверяет key/ship/builder/price/token и фактический запас/конец очереди.
Legacy без token остаётся unknown, платёж не повторяется. XSD/scheduling,
supply_payment fixture (включая token), diagnostic Lua syntax PASS.
Save739 правильно отказал slot_occupied (старый save009 действительно есть).
Source diagnostic741 выбирает первый свободный native slot из raw SaveList,
не перезаписывая существующие/invalid saves; CLI load дополнен save005.
Installed production738/UI739/diagnostics736, source741 НЕ установлен.
X4 PID56116, активных контроллеров нет. Следующая установка одним пакетом:
production741+diagnostics741; короткий fresh supply+save/free-slot/load.


Пакет728–729: оба controller terminal0, активных pipe нет, PID2484.
Военная подготовка728: known ownerless Наполеос IV Фортуна → ownerplayer
наблюдён (world fixture, goal не сигналился). Read729 подтвердил вторую
штатную HoldSpace goal: Start complete/2subgoals для этого сектора, наряду
с Большая биржа I. Это пока наличие цели, не выполнение флота/снабжения.
Repair_setup728 отказал до эффектов: own_native_service_station_unavailable.
Service_setup729 подготовил own native arg_wharf1c509d/21modules/canequip1/
shiptrader1c5b51; free_world_preparationtrue, paid_constructionfalse,
repair_calledfalse. Дождаться её реального observation/service registration
по read/provision, затем один repair_scenario через existing handler;
не считать fixture paid supply. Read729 HQ processor elapsed259.278/540,
step19.2777/60: стройка идёт во время независимых сценариев, повторов нет.
Installed716/diag721, sourceLua723 не установлен; задачи не закрывались.

Результат725–727: все три probe/controller terminal0, активных pipe нет.
Own builder18774a получил настоящий DeployToStation и station/storage4b6f2/
4b612; funding463702Cr observed. Builder receipt sent393687.814→deployed1
→observed393807.848. Read727 processor elapsed56.8612/540, step56.8612/60,
building1: стройка действительно идёт. Test materials подготовлены command
construction_resources726 (paid_supplyfalse, construction_completedfalse),
не считать native оплаченной доставкой. UI status/empire/stats/status
открылись и имеют реальные frame/bodyrows133/18/85/133; никакой пустойвкладки.
Документ docs/owned-builder-ui-acceptance-725-727-20261012.md. Полная очередь/
полные UI-сценарии ещё не приняты. Installed716/diag721, sourceLua723 не
установлен. X4 PID2484 живую timeline сохранять пока независимые проверки;
не начинать длительный прогон только ради очереди540s.

Результат722/724: controller45802 terminal0, load722 accepted autosave_01.
Blueprint prerequisite world_fixture money_unchanged1/purchasefalse.
Одна expansion generation construction_1_393633.039/HQ4b6f2:4/4blueprints
observed→consumed. Owned builder18774a/pilot187754 подготовлен во время
validation (native purposebuild1/defaultWait/57actualbuildunits/~6895m).
Read724 terminal0: expansion queued/build8c7e, native processorbuilding1,
elapsed0/total2700/step300/requiresbuilder1; builderreceiptnull/deployed0.
Это ещё не назначение или строительство. World init PID2484; controllerов
нет. Следующий read после штатного funding/builder tick, затем анализ
CanUseOwnedShip если не выбран; повторный spawn/generation запрещён.
Production716/installeddiagnostic721; sourceLua723(save_validation) не
установлен. Нового restart/сохранения/долгого прогона не было.

Наблюдение/доработка723: controller722 session45802 жив; load722 получил
accepted|autosave_01. X4 PID2484 Responding true CPU96.41, мир загружается.
Batch722 ещё не подтверждён; второй клиент не запускать. Installed
production716/diagnostics721, sourceLua723 ещё не установлен.
Добавлена save_validation: только свободный native save_009 после свежего
GetSaveList, validSaveFilenames и active projection; no-replay intent перед
SaveGame, occupied/list-not-ready запрещают эффект. Requested не доказывает
save success. Probe load whitelist расширена save_009, Lua syntax/Python
compile PASS. Save_004/autosave_01 не затронуты; новая команда ещё не вызвана.
Использовать в последующем общем persistence/binding/queue пакете после
current builder результата, не перезапускать игру только ради этого сейчас.

Установка/запуск722: diagnostics720/721 MD+Lua установлены и hashes
сверены после штатного закрытия X4. Production716 без изменений. Один
controller722 session45802 жив на первом poll (save-menu pipe), затем
load722 autosave_01 и batch722. Короткий пакет ждёт только bound→active
(до4 read-only интервалов5s), grant одного тестового blueprint→одна
expansion generation→owned builder во время validating→read-back.
NPC режим prehire не менялся; owned validating требует текущий Manager/goal.
Schema721 PASS. Никаких сохранений/сброса квитанций/длинного прогона.
Следующий шаг poll45802; второго pipe controller не запускать.

Результат717/719 и доработка720: load717 autosave_01 accepted,
controller66022 terminal0; baseline без construction/hire/transfer receipts,
governor4bbe1 station4bbdb, station manager4bbde unchanged. Batch719
controller57416 terminal0: runtime active, expansion_fixture один раз
запустил generation HQ. План construction_1_393694.022 (4entries) удержан
waiting_blueprints/required_blueprints_missing: отсутствует только
ware tm_module_empire_control_arg. Expansion validating; никакой build,
funding/plot/builder receipt пока нет; local_owned_builder НЕ вызывался.
Добавлена диагностическая construction_blueprint_prepare: native
add_blueprints только macro управляющего модуля; денег/лицензий/квитанций
не меняет, world_fixture=true, не квалифицирует purchase. MD720 и Lua syntax
PASS. Source diagnostics720 ещё не установлен. Installed production716/
diagnostic712+709; X4 PID54496, controllerов нет. Не повторять expansion:
после выдачи prerequisite существующий план должен продолжиться сам.

Наблюдение718: controller717 session66022 повторно подтверждён живым.
X4 PID54496 Responding true CPU41.38; debug подтверждает startmenu9.00
и100s до intro. Результаты load717/batch717 ещё не получены; world effects
не отправлялись. Подготовка следующего этапа должна опираться на baseline:
module_fixture допускается для HQ, assign_fixture переводит существующую
service crew (один раз) и place_fixture ждёт actual arrival. Не применять
check_roles без State.Employee/Module. Если Registry active уже есть,
повторную подготовку должности не делать. Старые неизвестные receipts не
сбрасывать. Источники и установка остаются717; никакого нового restart.

Установка/запуск717: все51 production files установлены install_mod с
проверкой manifest/closure; qualified_release=false. Production716 и
полная diagnostics712+709 (local_owned_builder и context/template dialogue)
установлены, MD/Lua source/install hashes сверены. Прежняя X4 штатно
закрыта до копирования. Steam запущен с прежними launch options. Один
controller717 session66022 жив на последнем poll: load717 autosave_01 затем
read-only batch717 (read/provision/personnel). Результат ещё не получен.
Save_004/autosave_01 не перезаписываются, квитанции не сбрасываются.
Следующий шаг poll66022 и подготовка свежего мира по фактическому baseline.

Доработка716: bare factory guard удерживает new create_factory при
незавершённой Expansion, даже если handoff отказал. ReconcileQueuedExpansionOwner
перед authority сверяет observed funding/plot ключ/paid этой station/build,
затем учитывает debit в spent только при новом accounted key. Денег/квитанций
не меняет, ранее учтённое не добавляет снова. Closure13 и schema/scheduling
полных MD/AI716 PASS. Source716 + diagnostic712 пока не установлен;
installed699/MD709/Lua706, X4 PID8300 и ни одного контроллера.
Следующий общий короткий пакет handoff/accounting/unknown/builder проводить
из разрешённой ранней timeline (например autosave_01), а не стирать старую
queued/unknown текущего мира ради фикстуры. Документ713 обновлён.

Доработка715: handoff интегрирован в штатный Request_Factory генератора:
matching orphan queued nativecreation по сохранённому creation.product и
RequestSector/Ware→ReconcileQueuedExpansionOwner. Успех использует старую
Station/ActionDefinition/native observers, подавляет создание/finalise;
отказ сохраняет штатный путь с existing expansion guard. Product сохраняется
при новых фабриках, старые записи без него не принимаются по догадке.
Новая цель дополнительно проходит ReadGoalLifetime. Closure13 пересобрана;
Python/schema adaptedMD/AI/scheduling PASS715. После добавления lifetime
нужно validate715b. Installed699/diagnosticMD709/Lua706; source715/diag712.
Новых игровых действий/установки в715 не было, controllerов нет.
Следующий крупный шаг — свежий общий короткий пакет handoff/builder/guards;
старый read713 creation безproduct не использовать как подтверждённый intent.

Доработка714: ReconcileQueuedExpansionOwner и вызов из StepPrefabExpansion
для выбранной штатным AI той же станции. Точная native queue/sequence/claim,
новая authority/исчезновение старой, creation provenance, terminal-only
funding/plot/builder receipts обязательны. Ключ/spent/accounting/очередь
сохраняются, эффектов handoff не выполняет. Source ещё не установлен.
Требуется интеграционная сверка new-factory startup: штатный AI должен
выбрать существующую очередь; hook следующей prefab стадии не доказывает
этот путь. docs/construction-handoff-boundary-713-20261012.md обновлён.
Installed production699/MD709/Lua706, source production714/diagnostics712;
X4 PID8300, pipe controllers нет. Задачи остаются открытыми.

Уточнение713: read713 terminal0, pipe владельцев нет, X4 PID8300.
Expansion4ca8f/1dee теперь queued/construction_goal_missing_after_queue,
реальная задача сохранена. Plot rejection — старая квитанция18, установленный
construction_plot.lua уже исправлен430; повторная правка quote не нужна.
Доказана граница принятия старой стройки после смены governor710. Описание
и инварианты docs/construction-handoff-boundary-713-20261012.md. Следующий
крупный шаг — handoff existing native queue новым штатным goal с сохранением
квитанций/accounting/неповтором эффектов; затем owned-builder короткий probe.
Production699/installedMD709/Lua706; source diagnostics712 ещё не установлен.

Результат710/711: controller35780 terminal0, snapshot711 terminal0.
Remote назначение выполнено через настоящий context/template диалог:
seed6848502423851159041 source188e22→governor18cbc7 station4c234/module4c26d;
sent402519.078→bound402536.283→active402549.738. Intransit0/scheduled0,
station manager4c237 unchanged, один TM_PlayerManager/economy/factory receiver.
Подробности docs/governor-remote-arrival-710-20261012.md. Current X4 PID8300,
активных pipe controllers нет. Task2.2 ещё открыта: требуется полная сверка
binding/сохранение/защиты, отдельные подтверждения не расширять до приёмки.
Общий snapshot711: construction4ca8f/1dee queued; plot receipt rejected
plot_location_requires_reconciliation, builderactualnull, elapsed0.
Следующая сборочная граница — согласование plot до owned-builder probe.
Installed production699/MD709/Lua706; source diagnostics712 ещё не установлен.

Доработка712: добавлена диагностическая команда local_owned_builder,
адаптирует существующую LocalBuilderSetup через Owned param. Spawn штатного
Argon XL builder/пилот/30build drones в5–7км, faction.player/default Wait;
NPC режим FindBuildTasks сохранён. Guard не допускает spawn после уже
назначенного constructor или sent/unknown receipt этой queued expansion.
Назначение/claims/deploy остаются production AI; материалы/оплаты/результат
не форсируются. MD712 schema/scheduling и Lua syntax PASS. Source712 пока
не установлен; установлен MD709/Lua706, production699. Текущий controller710
session35780 остаётся единственным владельцем pipe до terminal; batch711
не запущен. Новое тестовое средство не принимает construction3.4.

Наблюдение711: текущий controller710 session35780 повторно подтверждён
живым; X4 PID8300 Responding true CPU26.06, ещё стадия инициализации
расширений, load710/batch710 результата пока нет. Перезапуска/повтора команд
не было. Подготовлен batch711.py (py_compile PASS) для последовательных
read/provision_read/personnel_autonomous_read, без игровых эффектов. Он
пока НЕ запущен: сначала должен завершиться владелец pipe35780. Этот общий
снимок объединит экономику/стройку/военные квитанции и причины станций;
не считается приёмкой результата или долгим прогоном.

Установка710: source709 MD установлен после штатного завершения X4,
source/install SHA8506CE58B89F2C9316945A7F851E3E38D1D755DC0105281A340C5B55735F02AC.
Production699 / diagnosticLua706 без изменений. Steam запущен с существующими
параметрами, controller710 session35780 жив на последнем poll, ждёт
save-menu pipe→load710 save_004→batch710. Batch требует не только prepared,
но и native_possible1 ДО release. Никакое сохранение не перезаписывается.
Следующий шаг poll35780; не создавать второго владельца pipe.

Результат709: controller707 session49910 terminal1; batch707.json получен.
Настоящая crew запись source188e45/template4226042147235854424 существует,
transit0/scheduled0/native_possible1. Локальный release подтверждён:
runtime inactive, governor null, station manager unchanged. Remote dialogue
не открылся: debug402518.12 «not a valid conversation actor», кнопка выбора
отклонена до эффекта. Pending idle; перевод НЕ отправлялся. X4 PID33624 live.
Причина доказана common.xsd conversationactor: tuple нельзя передавать в
actor; для NPC template требуются context и template отдельно. Source709
исправляет start_conversation обеих ветвей, component сохраняет actor.
Проверки/установка709 ещё не выполнены. Нужен штатный restore исходного
управляющего или загрузка тестового сохранения; никаких reset/replay receipt.

Наблюдение708: session49910 подтверждён живым повторными poll; load707
получил штатный accepted|save_004. X4 PID33624 Responding true CPU40.72;
лог подтверждает startmenu и101s до intro. Batch707.json ещё отсутствует,
поэтому его эффекты/результат не подтверждены. Транспорт не перезапускался,
назначение не переотправлялось. OpenSpec apply708 ready13/32 (19remaining),
проверен в настоящем профиле пользователя; sandbox-профиль давал ложный
schema-not-found, это не отсутствие схемы проекта. Следующий шаг — poll
того же49910, затем разобрать batch707 и фактические Pending/binding.

Установка/запуск707: PID47032 штатно завершён (CloseMainWindow/WaitForExit).
Diagnostics706 установлена: MD BC1477292AF51AE3492DD26F9A2C820F3F57F4A8BE3F5E4D3C2315235C1ECD40,
Lua D5D24DE7228775B2FEAEA0A56A6C4B591ACACF4B78E404C1892276C05181C3C8;
source/install hashes совпали. Production699 без изменений. Lua syntax680
повторно PASS. Steam запущен без дополнительных launch flags. Единственный
controller707 session49910 выполняет load707 save_004 и затем batch707;
на последнем подтверждённом poll жив, ожидает save-menu pipe. Результат
назначения пока не получен; не запускать второй controller/повтор эффектов.

Актуализация706: batch704 завершён (terminal0), read705 получен.
Штатный preflight реальной crew записи разрешил перевод (native_possible1),
но материализованный actor188dd9 первоначально был intransit1, а в read705
его container/roleobject отсутствуют. Remote state unknown; transfer не
отправлялся, исходный governor4b520 и station manager сохранены.
Diagnostics706 использует штатный generic actor [ship,template] вместо
предварительной материализации NPC. Production уже поддерживает такой
actor; production699 не менялся. Guard проверяет запись и transit/scheduled,
Lua проверяет ownership исходного корабля. Read-back дополнен crew membership
и её transit/scheduled. MD706/schema/scheduling PASS. Новая диагностика ещё
не установлена и не проверена в игре; 2.2 остаётся открытой. Production699 /
installed diagnostics702; последняя известная игра PID47032. Никаких новых
покупок, переводов, сохранений или перезапусков в706 не выполнялось.

Актуализация704: controller16539 terminal0,load701 accepted. Native700
показал точную причину: cueactor0x188e8f/template4908279078625414699,
source_member0/native_possible0/native_failure invalid. UI699 правильно
вернул assignment_rejected/invalid и показал отдельное сообщение;
Pending idle, отправленного transfer нет. Source crew отсутствовал.
Diagnostics702 исправляет подготовку через штатные create_ship/people
(service crew) и create_npc_from_template настоящей записи. Не меняет
production проверку, не создаёт disconnected cue actor и не выставляет
arrival/transfer. Native preflight остаётся check=true. MD702 PASS.
Установка704: production699 без изменений,diagnostics702 MD/Lua hashes match.
PID15512 штатно завершён. Единственный живой controller session51549:
Steam→load704 save_004→batch704, на первом poll ждёт save-menu pipe.
Итоги ещё не получены, сохранение не перезаписывается.
Установка701: production699, diagnostics700;51 production hashes и
diagnostic MD/Lua hashes сверены, qualified_release=false. PID55772 штатно
завершён. Один живой controller session16539: Steam→load701 save_004→batch701;
на последнем poll ожидает save-menu pipe. Нового loader/probe не запускать.
Batch701 не повторяет принятый default entry698; читает native preflight
и template/source membership, результатную строку настоящего remote assign
до CancelConversation и LastResult. Эти данные должны отделить отказ
тестового NPC от дефекта производственной роли. Итоги ещё ожидаются.
Актуализация700: session53437 terminal0, load698 accepted save_004,
X4 PID55772. Batch698 подтвердил реальные default options, «Ещё» button5,
пункт мода button2 и role dialog с release button1. Namestring fix697
работает; customhandler0. Remoteactor0x188e91/seed-9168992542312332941
на docked source0x188e87 подготовлен. После remote assign button1
Pending idle, Governor null, actor всё ещё source; перевод не подтверждён.
Сам ответ choice sent не принят как binding. Native точный отказ ещё неизвестен.
Restore700 terminal0: проверенный CheckRoles восстановил того же исходного
локального сотрудника без нового transfer, repeat_binding bound,
manager_attempt existing_post/manager_unchanged1. Runtime готовится к активации.
Source699 улучшает реальные сообщения UI (ownership/module/arrival/actor/native
rejection) и сохраняет один LastResult UI с actor/time + NativeFailure проверки
без replay/нового executor. Source700 diagnostic prep читает npctemplate/
source_member и native check=true failure. MD/closure/localized XML PASS.
Оба source пока не установлены. Старый remote intent не отправлять повторно
без установления результата; активных контроллеров698/700 нет.
Установка698: production696 (economy694 + bounded evidence retirement),
diagnostics697.51 production hashes проверены установщиком, diagnostic
MD/Lua hashes match, qualified_release=false. PID55348 штатно завершён.
Единственный живой контроллер session53437 выполняет Steam→load698→batch698;
первый poll ожидает save-menu pipe. Другие контроллеры этого пакета отсутствуют.
Source696 очищает observation/history только утраченных станций,32 записи
с вращением окна на существующей snapshot cadence, без нового таймера
и без отмены native orders/receipts. MD/closure PASS, игровой read-back pending.
Причина пустых695/692 диалогов найдена в diagnostics685: start_conversation
conversation="$Conversation" ошибочно использовал expression в namestring.
Source697 выбирает literal default/tm_empire_roles в двух ветках. До685
dialog683 literal путь работал; customhandler695=0, эта гипотеза опровергнута.
Controller43280 terminal1; ни release, ни transfer не выполнялись.
Batch698 даёт до10с bounded чтения initial options без повторного открытия;
отказ default entry не блокирует независимый remote UI test после CancelConversation.
Установка695 завершена: production694, diagnostics693;51 production файлов
сверены установщиком, diagnostic MD/Lua hashes match, qualified_release=false.
PID3824 штатно завершён. Единственный живой контроллер session43280
последовательно выполняет Steam→load695 save_004→batch695. На первом poll
ожидает save-menu pipe; игровые результаты ещё не получены. Не запускать
второй loader/probe до завершения этого handle; сохранение не перезаписывает.
Source694: production history period теперь учитывает cargo_capacity и
pilot_seed/pilot_skill существующих подчинённых при TM_SameProvision.
Неизвестный пилот unknown, старые snapshots без полей отделяются новым
периодом; cargo_used как результат работы не разрывает период. Генератор
и13-script manifest пересобраны; только economy.xml отличается от
production674. MD/closure/native-copy PASS; originals unchanged.
Source ещё не установлен. Batch695 подготовлен для одной установки
production694+diagnostics693: traits→native cancel→default entry и
независимый remote UI transfer. Обычная ошибка входа не блокирует перевод;
неизвестный эффект не повторяется. Пока не запущен.
Актуализация693: load689 accepted save_004, X4 PID3824. Controller76766
terminal1 из-за пустого default-разговора; dialog689 подтвердил подготовку
remoteactor0x188f5d/seed-7220070101721314094 на docked source0x188f53,
station0x4b51d. Ни assignment, ни arrival не вызывались при подготовке.
Read691 после ожидания всё ещё6 пустых кнопок. Independent remote692
terminal1: даже новый tm_empire_roles unqueued не показал кнопок после
этого default. Снятие отклонено до эффекта; governor остаётся active,
manager unchanged. Hypothesis: пустой разговор остаётся активным и блокирует
unqueued; customhandler тестового NPC ещё не измерен, не утверждать как причину.
Source693 добавляет штатный CancelConversation (Helper.closeMenuAndCancelConversation)
и чтение customhandler/temporary. Пока не установлен. Это отмена
тестового UI-разговора, не отмена assignment/journey или штатных приказов.
Все контроллеры689/691/692 terminal; нового полного/долгого прогона нет.
Установка689: diagnostic source688 MD/Lua hashes match, production674
не менялся. PID18356 штатно завершён. Один контроллер session76766
выполняет Steam→load689 save_004→dialog689 последовательно; на старте
ожидает save-menu pipe, итогов пока нет. Сохранения не перезаписывает.
Source685–688: штатный default→«Ещё»→tm_empire_roles проверяется настоящими
кнопками; свободный реальный passenger готовится на отдельном корабле,
созданном docked через штатный find_dockingbay/create_ship. Не вызывает
assign_hired_actor/RequestAssignment в подготовке, не подменяет прибытие.
Remote read сверяет seed/container/roleobject/pending/manager. Back допускает
возврат по нескольким уровням; эффект release/assign ограничен одним выбором
на открытие. MD/scheduling validate688, Lua syntax, Python syntax PASS.
Актуализация684: diagnostic source681–682 установлен, MD/Lua hashes match;
production674 не менялся. PID45960 штатно завершён, Steam без новых параметров
запустил PID18356. Load682 save_004 accepted; controller9676 terminal0.
Dialog683/session97853 terminal0: настоящий start_conversation и реальные
GetDialogOption/SelectDialogOption доступны в extension Lua. Снятие button1
→inactive/manager_exists0/governor0; повторное открытие, выбор исходного
модуля button1 →bound с тем же actor0x4c234/module0x4c267/station0x4c22e.
Check684 terminal0: manager_attempt existing_post, repeat_binding bound,
manager_unchanged1, projection active1; проверка содержит защищённые
повторные попытки BindGovernor и не является чистым чтением.
Это подтверждает локальный настоящий диалог, но ещё не вход через штатное
«Ещё» и перевод удалённого сотрудника через UI. Task2.2 остаётся открытой.
Активных контроллеров682–684 нет; сохранение не перезаписывалось.
Актуализация680: session8051 terminal (handle отсутствует), batch675.json
содержит все16 команд; read677 отдельный terminal0, age402780.408.
Production674/diagnostics673 остаются установленной версией. Новый
diagnostic source678–680 пока не установлен; игровых результатов для него нет.
FindBuildTasks местного fixture не доказал доступность: штатный цикл выбрал
другого builder_hire3_402686.904, оплатил50000Cr и назначил0x982f7;
read677: расстояние18.75млнм, elapsed0/total780. Прогон ожидания перелёта
не запускается. Новый read отделяет LocalBuilderAttempt от оплаченного
строителя и показывает pilot/default/current orders/constructionmodule.
Diagnostic680: governor_dialog_open/read/release/assign используют настоящий
start_conversation и GetDialogOption/SelectDialogOption текущей X4.
Только точный ожидаемый текст кнопки, собственный actor, не более одного
release/assign на открытие; production RequestAssignment напрямую не вызывается.
Это средство проверки UI2.2, не свидетельство её приёмки. MD XSD/scheduling
validate680 PASS, Lua syntax680 PASS через игровую Lua DLL, probe.py syntax PASS.
Следующая установка должна собрать обе диагностические границы в одну
короткую проверку; не повторять весь старый пакет только ради этих изменений.
Audit676: существующий personnel_hire_fixture PASS (hire-negative676.txt):
нет денег, изменённая цена, revoked, destination loss, частичная оплата
unknown/no replay и штатная нулевая цена. Это Lua/payment граница, не полная
приёмка всех vacancies4.1. Реальное no candidate current batch подтверждено
batch668, положительный paid hire/arrival671–672. Новых дефектов бюджета
аудит не установил, соответствующий production код не менялся.
Load675/batch675 session8051 ещё работает; X4 PID45960 отвечает, CPU41.23s.
Установка675: production674/diagnostics673,51 файл, diagnostic hashes match,
qualified_release=false. X4 PID32504 штатно завершён. Load675→batch675
запущен последовательно через Steam без новых параметров; результат ожидается.
Новый пакет повторяет независимые кадровые/UI/causal проверки и готовит
местного NPC с штатным FindBuildTasks до найма. Сохранение не перезаписывает.
Живой контроллер установки675/load675/batch675 — session8051; на последнем
poll ещё ожидал save-menu pipe. Других контроллеров этого пакета нет.
Source674: военная проекция учитывает собственный default/current order,
а не только Ship.orders: штатная DefendArea создаёт ProtectPosition как
default=true и регистрирует тот же receipt. Проверяется Order.object==Ship,
claim/goal/priority guards сохранены. MD/closure PASS, ещё не установлено.
Подтверждённый hire671→arrival672 добавлен в personnel-integration-acceptance.
Read671/672 terminal0: autonomous hire135480Cr observed, employee0x193853,
seed2414503123811654272, target0x188fef, transit0/scheduled0/podnull/pass1.
Builder local0x188db2 всё ещё builder_busy до оплаты несмотря на Wait;
гипотеза «обычный Wait делает NPC нанимаемым» опровергнута. Primary jobs.xml
argon_construction_vessel_xl задаёт default FindBuildTasks. Diagnostics673
теперь использует этот штатный order, maxjumps0/playeronlytrue; validate673
PASS, ещё не установлен, native hire availability пока не доказана.
Read672 session69660 terminal0, активных контроллеров671/672 нет.
Batch668/session57957 terminal0,load669 accepted. Local0x188db2 prepared
в5872м; vacancy target0x188fef/recruit actor0x188fea prepared, prerequisite
registered Econ_Manager. Первый кадровый tick no_available_employee_in_current_batch,
реального hire/arrival ещё нет. Assessment10/trade12 PASS,3 UI modes PASS.
Construction elapsed0, ожидается bounded licence/funding/hire. Candidate670
подготовлен на следующей реальной станции поиска; JSON сохраняет результат.
Контроллер установки669/load669→batch668: session57957 живой, ожидает
save-menu pipe, новый X4 PID32504. Предыдущие контроллеры terminal;
повторный запуск/параллельный pipe controller не требуется. Документ
assignment-contracts теперь явно маркирует ранние «AI не реализован»
как исторические этапы; полноценная приёмка пользовательского диалога открыта.
Установка669: production666, diagnostics664,51 файл, diagnostic MD/Lua
source/installed hashes match, qualified_release=false. PID16932 штатно
завершён; Steam запуск без новых параметров. Load669 save_004→batch668
выполняется последовательно одним контроллером; результаты ещё не получены.
Изменены военные имена/priority/lifetime projection и idle local builder.
Batch668.py подготовлен для следующей установки666+diagnostics664:
local builder/resources и hire vacancy/candidate готовятся в начале,
затем causal boundaries,3 UI pages,3 совместных personnel/build reads.
Никакого reset receipts/timers; syntax PASS; ещё не запущен. Read667
подтвердил безопасный fallback после busy местного: builder_hire3 sent
для другого реального NPC0x97e17, remote18.76млнм,elapsed0. Нет успеха стройки.
Source666: ReadMilitaryExecution исключает недействующие goal lifetime,
ручные/приоритетные приказы и циклы, очередь>32 даёт incomplete. Военная
проекция не считает такой корабль действующим участником и не вызывает
CanUseOwnedShip (тот может регистрировать кадровую потребность). Чтение
остаётся без dispatch/смены приказов. MD/closure PASS, ещё не установлен.
Source665: военная задача во вкладке теперь перечисляет до4 кораблей
с подтверждёнными действующими собственными приказами (имя/idcode),
ссылаясь на список собственности для остальных. Planned goal не считается
флотом; существующие governor/goal/ownership/helm/receipt guards и bounded
16 subgoals/32 ships/16 orders сохраняются. MD/closure PASS, не установлено.
Read663: выбран именно local0x188f0c, builder_hire2 rejected_before_effect
builder_busy, actualbuildernull, orders0/commandflying,elapsed0. Платёж по
этой попытке не выполнялся. Source diagnostics664 задаёт вновь создаваемому
fixture NPC штатный default Wait (как cpu_ship_manager/boarding), вместо
генерируемого полётного задания. Это проверяемая гипотеза busy, не доказанная
причина; guard IsBuilderBusy сохранён. Validate664 PASS, ещё не установлен.
Roles662 reads без fixture context дают passed0/null: не приёмка singleton
и не регрессия. Personnel required_control_posts_present, vacancies не созданы.
Local658 session71638 terminal0:3 чтения завершены, elapsed0, local NPC
строитель подготовлен до найма. UI660 terminal0: tm_empire_status111 строк,
empire18 строк, stats85 строк; точные mode/frame ответы, смена страниц
успешна. JSON ui660.json сохранён; визуальная приёмка/полная projection
сверка ещё открыты. Активных контроллеров658/660 нет, X4 PID16932.
Local658: save_004 accepted; world active402513.764. Команда local_builder
подтвердила нового NPC ship0x188f0c в5432м от текущей стройки0x4b8a0;
native loadout+units дают фактически67 build units (не ровно30: loadout
тоже добавляет дроны). Ресурсы подготовлены. Read402524/402534 всё ещё
plot pending, elapsed0/actualbuildernull; это прежний bounded backoff,
не доказательство провала найма. Контроллер71638 делает последние чтения.
Probe659: Python request проверяет ожидаемые префиксы local_builder,
builder_near/construction_resources и точный ui mode; несовпадение останавливает
следующие шаги без replay. Py_compile PASS. Source/installed gameplay не меняет.
Short651 UI read-back: mode tm_empire_status, frame72, tables2, body_rows31,
width1205/x61/y99/maxheight621; пустой body не воспроизведён, полная визуальная
приёмка не доказана. Local658 session71638 ещё работает; новый X4 PID16932.
Установка657: production656, diagnostics655/навигация652,51 файл,
source/installed diagnostic MD+Lua hashes совпадают; qualified_release=false.
X4 PID52684 штатно завершён. Steam launch без новых параметров;
последовательный load658 save_004→local658 controller session71638 работает.
До завершения контроллера повторные загрузчики/пробы не запускать. Local658
готовит NPC строителя до найма, ресурсы, затем3 чтения с10с интервалом;
Python syntax/13-script closure PASS. Save_004 не перезаписывается.
Source655–656: диагностика local_builder создаёт известного аргонского
строителя с30 строительными дронами в5–7км до найма, отказывает при уже
назначенном/current sent builder, одно создание на session/save state.
Production поиск кандидатов теперь использует штатный sortbydistanceto
станции: ближайшие рассматриваются первыми, bounded8/cursor/guards прежние.
Validate655/656 PASS. Эти изменения ещё не установлены; live успех не заявлен.
Read653: plot19/funding2 observed, штатный builder_hire2 sent. Builder653
warp after_storage2303м; read654 уже75.68млн м, другая zone, flying/order1,
native elapsed0. Подготовка warp не прерывает активный штатный маршрут;
повторять её не нужно. Следующая короткая проба: местный строитель до найма.
Все контроллеры653/654 terminal0; production649/diagnostics647 установлены.
Short651 session99406 завершился0, read652 завершился0. Assessment10 и
trade decision12 PASS. Current стройка после load ждёт plot licence,
budget0/actualbuildernull, native elapsed0/requires_builder1. Старый builder
receipt относится к иной станции; builder_near отказался до эффекта.
Source diagnostics652 исправляет station/build привязку навигации,
validate652 PASS, ещё не установлен. Подробности short-batch-651-20261012.md.
Текущий X4 PID52684; активных контроллеров651 нет.
Установка650: X4 PID52704 штатно завершён; production649 установлен,
51 файл, qualified_release=false. Диагностика647 установлена, MD SHA
E13152D50702A7D5710690FEB6911F4F7E683FC70FD5225038024CD145B4DC57.
Steam запущен без добавления параметров. Контроллер загрузки save_004:
session75306, load650.json; на момент записи ещё работает, world readiness
не подтверждено. Ниже записи об установке635 являются историческими.
Apply651 подтверждает ready,13/32. Короткий пакет short651.py подготовлен
(assessment/trade boundaries, существующий builder/resources, clocks/UI),
ещё не запущен: session75306 ожидает save-menu pipe. Последний live процесс
X4 PID52684 отвечает, CPU66.38s; это запуск, не доказательство готового мира.
Обновление: session75306 завершился0, save_004 accepted (load650.json).
Контроллер short651 запущен после завершения загрузчика, ожидает world pipe.
Source648: закрыты пропуски отзыва recovery_approved строителя и approved
пополнения счёта станции при утрате governor; MD и две Lua fixtures PASS.
Ещё не установлено. Подробности `async-approval-audit-648-20261012.md`.
Source649: recovery повторно читает актуальное разрешение перед эффектом;
RestoreSupply отзывает неподтверждённый saved payment approval, сохраняя
payment evidence. MD, closure и builder fixture PASS. Установка всё ещё635.
Короткая проверка строительства643–646: оплаченный штатный строитель
назначен, недостающие материалы подготовлены командой, deployed=0;
завершение не доказано. Диагностика647 расширена чтением native clocks
и навигации, validate647 PASS, ещё не установлена. Подробности:
`construction-boundary-647-20261012.md`. Контроллер read646 завершился0.
Чекбоксы `openspec/changes/add-empire-management-module/tasks.md` определяют
приёмку; исторические записи ниже не являются актуальной сводкой готовности.

Актуальная установка635:51 файл; qualified_release=false. В неё включены
производственные исправления633–634: отзыв разрешений bulk crew exchange
при утрате назначения/отмене цели и согласование после load. Диагностика
626–632 установлена вместе; все диагностические SHA сверены в
diagnostic-hashes635.json. Load635 autosave_01 принят штатным меню,
контроллер session63931 завершился с кодом0. Короткий пакет short635.py
завершился с кодом0:10 assessment и12 trade decision cases PASS;
подготовка crew остановилась до эффекта из-за отсутствия военной цели.
В текущем готовом мире crew636 отправил первый свежий bulk exchange;
контроллер session79779 завершился с кодом0 после трёх чтений; receipt sent,
source_member0/target_member1, реальное прибытие ещё не подтверждено.
Диагностика640 установлена: исправлен fixture goal, добавлена обычная
пассажирская телепортация для проверки внимания и read-back player.container.
MD source/installed SHA совпадают, validate640 PASS. Текущий X4 PID52704;
последовательный load640/save_004→attention640 контроллер session31575
завершился с кодом0: посадка и возврат подтверждены player_context;
сохранённый unknown crew transit остался. Активных контроллеров640 нет.
Load639 ранее был accepted и его
контроллер завершился, но телепортация639 не запускалась из-за выявленного
payload routing дефекта. Save_004 не перезаписан. Долгий прогон не начат.
Последние подтверждённые результаты: short625 пассажир/helm PASS;
read627 — самостоятельный оплаченный заказ delivered; read629 — автономное
назначение пилота observed с точным seed, без исходного членства/транзита;
supply630/provision631 — новый период после изменения обеспечения, low
confidence единственного снимка. Это не закрывает все условия открытых задач.

Историческая сводка621 и более ранних проверок (не актуальный runtime):
В установку621 включены
исправления lifecycle/payments/supply reconciliation, ротация станционных
оценок и ограниченный кадровый поиск4 станции/64 кандидата.
Последние завершённые проверки: short581/read584 подтвердили автономный
оплаченный наём478960Cr и observed arrival; интеграция персонала4.4 принята.
short586 подготовил материалы и приблизил оплаченного строителя текущего
строительного заказа; через15s deployed0, строительство ещё не принято.
Свежий перевод с arrival остаётся открытым; старый unknown native_bulk
сохраняется без повторной отправки. Диагностический двойной ответ исправлен
и проверен в игре. Оба контроллера завершены terminal0.
Пакет578 включает573–577: отзыв funding до оплаты, сверку бюджета станции,
единый кадровый diagnostic response и seed-проверку обучения/перевода.
Исходные/установленные SHA четырёх изменённых production файлов и diagnostic
XML совпали. Текущий тестовый X4 PID47004 подтверждён после запуска через
Steam и загрузки579 save_004. Активных pipe-контроллеров нет.
Установленная порция580/583/585/587/589: причины кадрового перевода, защита
назначения governor от незавершённых кадровых операций, подготовка строителя
с observed arrival и очистка событийных записей утраченных станций. XSD PASS.
Пакет597 также включает identity оценки589 и диагностику двух ролей592–596.
Старый X4 штатно завершён. После запуска PID55936 load598/session5155
завершился terminal0, save_004 загружен. short599/session62344 также
завершился terminal0: интерфейс заполнился; подготовка второго сотрудника
вернула placement_unavailable до изменений мира. Активных контроллеров нет.
Source600–601 исправляет назначение независимого локального governor при
старом unknown Pending; source602–603 добавляет штатное размещение сотрудника
в controlroom, когда NPC slot недоступен. validate603: XSD и scheduling PASS.
Эти изменения ещё не установлены и не подтверждены игровым read-back.
Ниже прежний PID и наблюдения относятся к завершённым проверкам установки578.
Подтверждённый порядок работы: сначала весь функционал и необходимые короткие
граничные проверки с командной подготовкой мира, затем полный длительный
прогон. Ожидание одной функции не является основанием для длительного прогона.
Source604 дополняет identity-границу: seed проверяется при продолжении периода
в адаптированной Economy и при выборке финансовых/производственных снимков.
Генератор и source fingerprint согласованы; XSD/scheduling/closure PASS.
Изменения не установлены; смена сотрудника/load ещё требует игровой приёмки.
Source605–606 завершает ту же границу для production/trade/service событий
и отложенных наблюдений штатных сделок/ремонта. Seed передаётся и проверяется
до добавления данных в текущую оценку. MD XSD/scheduling и оба AI overlay
selector/merged XSD PASS; игровые исходники неизменны.
Source607 подключает событийные таблицы к вращающемуся окну оценок вместо
постоянных первых32 станций. XSD и арифметика0–512 станций PASS.
600–607 установлены608; PID55936 штатно завершён перед установкой. Единственная
последовательность load608→short608/session32889 ожидает меню загрузки после
запуска Steam. Результаты двух ролей/UI пока не получены, полный gate не начат.
Уточнение текущего процесса: X4 PID51420, Python контроллера55504. Оба живы,
X4 Responding=true, CPU31.40625; log подтверждает startmenu и102s инициализации.
Session32889 всё ещё ждёт подключения save-menu pipe; второй контроллер не
запущен. Source609 защищает чтение/очистку завершённой trade_decision по seed,
XSD/scheduling PASS, ещё не установлен.
Load608 получил список сохранений и accepted/save_004. Единственная
session32889 перешла к short608 и ожидает world pipe; успех роли/вкладок
до ответов короткого пакета не подтверждён.
Short608/session32889 завершён terminal0: placement1, второй governor после
снятия первого bound, исходный восстановленbound, manager_unchanged1, passed1.
Статус/empire/stats созданы11/18/85 строк. Прямое состояние прежнего Manager cue
и игровой диалог не проверены;2.2/2.3 не закрываются. Контроллеров больше нет.
Source610 ограничивает ServiceStations группу подписки тем же окном до32
станций; XSD/scheduling PASS,609–610 пока не установлены.
Diagnostic611 проверяет реальное состояние прежнего Manager cue после снятия
и выводит current cue/state. XSD/scheduling PASS, не установлен.
Read612 terminal0: age402620.04, active/goals1, economy_last_run402526.91;
штатный стратегический цикл продолжился после смены роли608. Manager станции
сохранён. Контроллер чтения завершён; активных контроллеров нет.
Source613 исправляет ObserveHire: фактическое прибытие требует seed оплаченного
кандидата; совпадение component больше не достаточно. Другой сотрудник или
legacy seed missing сохраняетunknown/hire_employee_identity_changed без
повторной оплаты/назначения. MD XSD/scheduling и UI Lua fixture PASS.
609–613 ещё не установлены; текущая установка608.4.1/4.2 остаются открытыми.
Batch614:14 Lua fixtures PASS,4 effect_receipts и3 probe_responses PASS,
13-script shared guard/receipt closure PASS. Результат относится к исходникам
и контролируемым fixtures, не игровой приёмке. Полный6.1 остаётся открытым;
следующая установка включает накопленную порцию609–613 и diagnostic611.
615: накопленная порция установлена, SHA пяти изменённых production файлов
совпали. PID51420 штатно завершён; Steam запущен. Единственная последовательность
load615→short615/session42978 ждёт подключения меню, затем выполнит связанный
короткий пакет ролей/защит/assessment/trade decision/UI. Полный gate не начат.
Short615/session42978 terminal0: роль второго назначена/восстановлена,
manager_unchanged1; original_manager_stopped0, priority goal_instance_missing.
Не принимаются2.3/3.7. Игрок восстановленrestore passed1; UI98/18/85 строк.
Итог active/goals1/economy_last_run402526.902. Активных контроллеров нет.
Diagnostic616 добавляет раздельную подготовку пары перевода рядом со source
и проверку seed/зоны/≤5km перед обычным RequestTransfer; старыйunknown не
трогает. XSD/scheduling и3 response tests PASS, пока не установлен.
Source617: общий CanUseOwnedShip защищает queued override/priority orders,
до32; большая очередь даёт order_queue_inspection_incomplete. Diagnostic
priority проверяет сохранённый order handle и действующий Manager context,
не ждёт первого кадрового Tick. Original cue report дополнен state/lifetime/
registered; критерий stopped не ослаблен. XSD/scheduling/closure PASS.
616–617 пока не установлены; текущая установка615. Задачи2.3/3.7 открыты.
Source618 готовит общую Lua проверку реальной очереди GetOrders3 для границы
между MD approval и асинхронным эффектом. Пока не подключена к adapters,
не установлена/не принята. Следующее действие: интеграция supply/hire/crew
перед эффектом и общий пакет затронутых fixtures. Установка пока615.
Source619 подключает player_order_guard к supply/hire/crew до эффекта.
Новый приказ после crew check блокирует submission. UI registration/порядок
зависимостей исправлены; dry-run51 files PASS, общий Lua batch15 PASS.
616–619 ещё не установлены; живая проверка3.7 открыта. Подробности и ограничения
fixtures: docs/async-order-boundary-20261012.md.
Diagnostic620 исправляет timing singleton проверки: native cancel_cue
применяется после текущего actions block (libraries/md.xsd2520–2524).
Check теперьpending_cancellation, таймер2s записывает реальное stopped без
лишнего pipe ответа; governor_roles_read требует stopped и другой active cue.
XSD/scheduling PASS, не установлен.2.3 не закрыта до read-back нового пакета.
621:616–620 установлены, diagnostic дополняет priority ответы реальным
GetOrders3 read-back через production helper. PID54516 штатно завершён,
Steam запущен; единственная load621→short621/session44518 ждёт меню загрузки.
Short включает отложенный governor_roles_read, роли/приоритеты/assessment/UI.
Результаты не получены, задачи не закрываются. Полный gate не начат.
Текущий X4 PID52900 подтверждён; log startmenu/100s инициализации.
Session44518 жива и ждёт pipe, повторный запуск не выполнялся.
Source622: русские UI причины manual/priority/incomplete/unavailable queue,
crew guard reason без Lua file/line prefix. Crew contract и UI fixtures PASS.
622 не установлен; текущая игровая установка621. Полный gate не начат.
Short621/session44518 terminal0: deferred original_stopped1/current_exists1/
different_instance1/passed1;2.3 принята. Стратегический цикл после смены active,
goals1/economy_last_run402526.914. Helm/manual/priority прошли, Lua GetOrders3
реально распознаёт queued manual/priority. Passenger не принят: claimed_by_other
goal/player.shipnull;3.7 остаётся открытой. UI98/18/85 строк. Контроллеров нет.
Diagnostic623: passenger ship создаётся в космосе, проверяются player.container
и исходныйpilot/seed. Если AI занял ship, используется настоящий Claim.goal
только текущего Manager; claims и protection не меняются. Отчёт дополнен
container/docked/goal. XSD623-final PASS, включая поля;622–623 не установлены.
Приёмка12/32, установка621.3.7 открыта, полный gate не запущен.
Полный длительный gate не запускался. Далее — хронология, её номера версий
и состояния процессов относятся к моменту конкретной записи.

## Хронология пакетов

Пакет557: 50 основных файлов установлены. Diagnostic source556 использует
действующую экономическую цель вместо первого военного Goal; validate556
и dry-run установки прошли. Первое копирование diagnostic XML не удалось
из-за ошибочного имени каталога tm_empire_role_probe; правильный каталог —
tm_empire_diagnostics. Запрошено штатное завершение X4, чтобы исправить
копирование до чтения scripts. Процесс2872 ещё завершался после30s;
session54250 ждёт тот же процесс перед копированием/запуском. Единственный
контроллер load557→short558: session60500, Python48076. Не запускать второй
контроллер, не считать результаты короткого пакета полученными без JSON.

Уточнение: session54250 завершилась terminal0, diagnostic XML скопирован
в подтверждённый путь; исходный и установленный SHA равны. X4 запущен,
PID16456, CPU12.19/Respondingfalse на последней проверке ранней загрузки.
session60500/Python48076 остаётся единственным ожидающим контроллером.
Source559 дополнительно исправляет постоянный выбор первых32 станций
для проекции оценки: окно rotates32 без роста бюджета. XSD и арифметическое
покрытие0–512 станций прошли; source559 ещё не установлен. Подробнее:
`docs/station-observation-rotation-20261012.md`.

Source560: вкладка сообщает число оценённых в текущей порции станций и общее
число станций. Существующий empire_status_fixture PASS. Неполное окно не
выдаётся за полную оценку империи. Native evidence/history проверены чтением
исходника: наблюдения записываются штатным проходом; история ограничена16,
неполные производственные/корабельные выборки имеют собственные complete.
Это source-аудит, а не закрытие игровых задач5.1/5.5.
load557 получил accepted/save_004; session60500 ещё ждёт world pipe.

Short558 завершён terminal0, session60500 больше не активна; результаты:
`docs/short-batch-558-20261012.md`. Автономный найм не квалифицирован:
fixture создан до публикации реального кадрового поиска и вне текущей станции.
Source561/562/563 не установлены: safe retirement отозванного неоплаченного
найма; lifetime перед семинаром; ожидание готовности diagnostic подготовки;
исправленная точка lifetime в CheckPlotConstructionBoundary.
В555 lifetime ошибочно попал только в RequestStationPlot, поэтому описание
новой общей строительной границы уточнено; actual source563 включает обе.
validate563 PASS. X4 после короткого теста продолжает работать, второй
контроллер не запускался. Full gate не запускался, приёмка10/32.

Source564 не установлен: RestockResultWatch независимо от lifetime доменной
цели читает исходную payment_approved/build_observed supply receipt каждые15s.
Новых оплат/приказов/заказов/автоматического consume не выполняет.
validate564 PASS; игровая военная граница остаётся открытой.
`docs/supply-reconciliation-boundary-20261012.md`.

Source565/566 не установлен: terminal supply receipt отменённой цели
принимается только после ухода её исходного claim; результат сохраняется
в квитанции, в отсутствующий GoalCue не пишется. Unknown не принимается.
Diagnostic setup не ждёт поиск до создания вакансии (это могло создать
циклическую зависимость); fallback явно маркируется и не квалифицирует
следующую поисковую станцию. MD/XSD/scheduling validate565/566 PASS.
Групповые существующие fixtures supply_payment/personnel_hire/empire_status
и dry-run50 файлов PASS; они не доказывают новые MD-переходы в игре.
Последняя установленная версия557; последняя игровая проба558 terminal0.

Installed567: штатное завершение X4 terminal0,50 основных файлов установлены,
diagnostic XML скопирован в tm_empire_diagnostics. Manifest qualified_release=false.
Включены source559–566: ротация оценок станций/пояснение частичного окна,
кадровая отмена до оплаты/семинар lifetime, исправленная общая строительная
граница и независимое наблюдение/принятие terminal supply receipt.
Запущен один контроллер load568→short568, session40795/Python17904;
X4PID9088. Короткий пакет: read/native_analysis, существующие assessment/
trade decision/role contracts, штатные empire/stats и новая status, final read.
Длительного ожидания игрового события в нём нет. Загрузка save_004 отдельно
от готовности world pipe; результат пакета пока не получен. Новые payment/
arrival переходы этот пакет автоматически не квалифицирует.

Short568 завершён terminal0 (session40795 больше не активна): active Manager
до/после load, обновление native economy time,6 assessment и12 trade-decision
контрактов совпали с ожиданиями, role existing_post/repeat bound/manager unchanged,
empire/stats/status таблицы сформированы. `docs/short-batch-568-20261012.md`.
Source569 не установлен: ограниченный кадровый поиск4 станции/64 кандидата
за цикл вместо1/16, прежний порядок/страницы/штатные проверки сохранены;
validate569 PASS. `docs/personnel-search-budget-20261012.md`.

Diagnostic source570 не установлен: hire_candidate_next готовит кандидата
в фактической следующей ограниченной порции поиска после создания вакансии;
приближает только свободный тестовый target, не вызывает оплату/назначение,
не меняет курсоры/таймеры/arrival. validate570 PASS; игровая граница не проверена.
`docs/personnel-two-stage-preparation-20261012.md`.

Installed571:50 файлов основного мода установлены, diagnostic MD и Lua
скопированы в подтверждённые пути. Установлен source569 кадрового поиска
и diagnostic570 второй стадии. X4PID54532; единственный контроллер
load571→short572 session56726/Python13580. После готовности мира короткий
сценарий создаёт вакансию, регистрирует реальную экономическую предпосылку,
ждёт30s, проверяет результат; при отсутствии подтверждения готовит кандидата
в следующей порции и проверяет ещё два обычных цикла по30s. Прямого вызова
RequestHire/StepPersonnel и изменения cursor/tick нет. Завершает ui_status/read.
Результат ещё не получен, новый автономный найм не квалифицирован.

Source573/574 не установлен: отозванное строительное финансирование без
matching payment intent закрывается rejected; отправленный intent обрабатывается
первым и остаётся observed/unknown. Рабочий бюджет станции получил независимую
15s сверку sent/unknown без новых оплат, включая отсутствие callback после load.
validate573/574 PASS. Документы `construction-revoked-funding-20261012.md`,
`station-funding-reconciliation-20261012.md`.

Код всех согласованных доменов находится в одной адаптации штатного Manager:
экономика, развитие/строительство, флот/оборона, персонал, наблюдения/оценки
станций и вкладка. Наличие кода не подтверждает все сквозные критерии;
открыты задачи2.2–2.4,3.2,3.4,3.6–3.8,4.1–4.2,4.4,5.1–5.6,
6.1,6.3–6.6. В частности, не завершены приёмка свежего переноса с arrival,
актуальной строительной оплаты/строительства, всех военных границ и реальные
причинные оценки; финальный двухчасовой прогон ещё не квалифицирован.

Пакет526 установлен:50 файлов собственного мода с проверенными SHA;
диагностический мод установлен отдельно. Включены native Lua quote перед
оплатой строительства, повторная авторизация переноса экипажа и исправленный
event.param3 нового короткого сценария приоритетов. Source-проверки MD/XSD,
scheduling, затронутые Lua fixtures, изоляция адаптированного Manager и
OpenSpec strict прошли. Release остаётся unqualified.

Игра запущена через установленный Steam без добавления параметров. Контроллер
load526 завершился terminal0 и получил accepted/save_004. Это подтверждает
принятие штатной команды загрузки, но не игровую приёмку пакета. Short527
запущен одним контроллером и ожидает готовности игрового мира/ответов.
Дополнительные сохранения не записывались.

Short527 завершён terminal0, ответы в `.cache/tmp/station-boundary-20261011/short527.json`.
Пассажир: actual player.ship=fixture, controlled=null, CanUseOwnedShip=available,
passed=1. Restore: исходный корабль и исходный контроль возвращены, passed=1.
Helm: native teleport_player control=true не передал штурвал (controlled=null),
поэтому сценарий не подтверждён. Manual/priority: штатные флаги приказов
подтверждены, но проверки допустимости не квалифицированы: к этому моменту
runtime inactive/manager_exists=0, фактический StopReason «Управляющий утрачен».
Это требует разбора срока жизни employee actor при смене контекста игрока,
не нового долгого ожидания строительства. Задачи3.7/2.4 остаются открытыми.
Diagnostic source528 дополнен сохранёнными person/seed/station и read-back
actor/people/roleentity/StopReason; MD/XSD/scheduling PASS, пока не установлен.

Installed530/short531 terminal0 подтвердил исправление temporary lifecycle:
тот же employee seed-9126173547698565463, person9320570526010986153 и actor0x4b527
сохраняются во всех переходах; runtime active до и после, StopReason=null.
Пассажир, manual override, native priority flag и точный возврат игрока passed1.
Helm не подтверждён: native teleport в занятое кресло оставил controlled=null.
Diagnostic source532 создаёт отдельный fixture helm ship со свободным креслом;
MD/XSD/scheduling PASS, не установлен. Source533 пропускает повторную запись
temporary=false для уже постоянного actor. Эти адресные свидетельства не
закрывают целиком задачи2.4/3.7. Подробнее:
`docs/governor-actor-lifetime-20261012.md`.

Подробности последнего исправления:
`docs/personnel-funding-boundaries-20261012.md`.

## Исторические записи

# Текущая работа — 12.10.2026

## Source520 — точная причина финансового отказа и штатная котировка

Installed516/PID52132, load516 terminal0/accepted/save_004; short517 terminal0,
9 отдельных frames без сдвига материалов. assessment_fixture: все6 cases PASS
в реальном MD (чистые синтетические входы, не продуктовые наблюдения).
production/building snapshot→observed/low, warehouse/service/other без данных
→unknown/low, production period→observed/medium. Это граница собственного
классификатора, не причинная игровая приёмка5.3/6.5. Вкладка/снабжение/стройка
не считаются завершёнными по этому ограниченному свидетельству.

role518/519 — свежие отдельные чтения. Plot19 observed, resources0; funding2
rejected. Точный отказ: MD wanted1211197.8Cr, native GetComponentData wanted
1211198Cr, balance0 в обоих источниках. Source514 tolerance0.005Cr не исправляет
разницу0.2Cr, поэтому она не была обычной погрешностью double. Доказанная
несовместимая граница — центная оценка MD против штатной Lua-оценки.

Source520 подключает получение штатного Lua funding quote без оплаты; MD
затем повторно проверяет текущий governor/goal/build/storage, бюджет, возраст
котировки и соответствие native estimate текущему MD-состоянию (до1Cr для
различия представления). Перед эффектом Lua снова требует ту же одобренную
котировку с точностью0.005Cr. wanted/amount в квитанции одобряются по точной
native quote; старый raw_wanted хранится отдельно. Нового метода округления
или свободного допуска другой оплаты нет. Настоящее изменение native quote
после одобрения всё ещё отвергается. Quote requests удерживают новые запросы,
возобновляются после load как чтение и истекают через1min без финансового
эффекта. Timeout не изменяет заявку с чужим key. Rejected сохраняет причину и
1min backoff; отправленные/unknown платежи сохраняют запрет повтора.

Существующий Lua funding fixture дополнен реальным случаем1211197.8→1211198:
quote без эффекта, MD-approval simulation, однократная оплата1211198 и отказ
при изменении quote после approval. Этот Lua fixture и empire_status, MD/XSD
и проверка адаптированного замыкания PASS. MD/Lua соединение новой фазы ещё
нужно проверить в игре; Source520 staged, Installed516 текущий. Controller
short517 завершён; живых тестовых pipe-контроллеров нет. 10/32 принято,
финальный двухчасовой прогон не запускался.

Для следующего пакета границы игрока подтверждены штатные доступные команды:
common.xsd teleport_player(control=false/true, instant=true, force=true),
create_order(immediate/priority/override). Они позволяют подготовить пассажира,
штурвал и настоящий override/priority order в disposable мире без экрана.
Контроль после teleport необходимо читать фактически, а не выводить из запроса.

## Source510–515 — короткая граница, финансы и достаточность периода

Installed508:50 файлов скопированы/проверены установщиком, штатный restart,
PID34776. load508 terminal0/accepted/save_004, short509 terminal0. Сохранение
не перезаписывалось. Команда construction_resources добавила claytronics542,
energycells1083, hullparts1980; role511/513 подтвердили missing resource_types0.
Это бесплатная подготовка условий, не оплаченная доставка/постройка.

short509 выдавал отдельные ответы на каждый товар, поэтому часть дальнейших
чтений сдвинута. Не использовать метку команды как доказательство содержимого.
Source511 сводит весь ответ материалов в один frame. role511 и role513 получены
отдельно после terminal0/закрытия старого pipe и подтверждают paid hire observed:
actor0x188f33/seed8364106362045006570 стал капитаном target0x188f38;
issued402515.982→arrival402536.846, intransit0/scheduled0. Это проверка штатного
платного назначения на подготовленную вакансию, не вся автономная кадровая цель.

PFY706/station0x4bd7f/build0x1dee: plot19 observed; funding9 rejected с точной
причиной native_construction_quote_changed, money0/wanted1211197Cr. Builder512
отказал paid_native_order_unavailable без эффекта. Дальнейшее ожидание строителя
не требуется, пока эта финансовая граница не согласована. Причина различия
сумм в живой игре пока не доказана; не приписывать отказ нехватке денег.

Source514 сравнивает денежные снимки funding и station_funding через уже
используемый sameMoney (<0.005Cr), сохраняя проверки формы/суммы/одобрения и
read-back списания. Fixtures различного двоичного представления одного цента
PASS; missing debit0.01Cr по-прежнему unknown и без повторной оплаты.
При реальном изменении строительной котировки сохраняются observedwanted/
observedbalance для точного сравнения с MD-запросом. Отказ теперь передаёт
причину в Expansion и задерживает следующую попытку на1min вместо повторения
на каждом проходе. Diagnostic plot_context использует Lua IDs и больше не
вызывает заведомо неправильный GetComponentData(cdata).

Source510 добавляет русские причины найма во вкладку; Source515 понижает
уверенность результата станции до low при одном снимке/неполном периоде,
сохраняя наблюдаемый факт. Добавлен единый чистый assessment_fixture для
production/building/trading/ship_support/other и полноценного периода:
синтетические данные не попадают в продуктовые наблюдения.

Изменения510–515 пока staged. Lua fixtures изменённых мостов и MD/XSD PASS;
assessment_fixture ещё не исполнен в игре. Принятых задач10/32, задачи3.4,
4.1/4.2/4.4 и5.* сохраняют реальные оставшиеся условия. Полный длительный
прогон не запускался; текущий пакет игры508, PID34776, контроллеров не осталось.

## Source506–507 — строительный ID и границы перед оплатой

506: construction_plot.quote читает владельца сектора через исходный Lua ID,
а C-вызовы используют 64-bit ID. Существующий fixture теперь различает эти
типы; прежняя числовая заглушка скрывала неправильный GetComponentData.
В диагностике добавлена construction_resources: однократное бесплатное
пополнение buildstorage текущего отслеживаемого build, максимум16 товаров,
не более1000000 единиц каждого и не сверх вместимости. Записываются before,
needed/requested/after и результат add_wares. Это подготовка мира, а не
доказательство оплаченного снабжения или завершения строительства.
builder_near проверяет расстояние до buildstorage, куда фактически переносит.

507: перед оплатой снабжения и найма Lua повторно проверяет точный native
GetPlayerControlledShipID. При штурвале игрока эффекта/списания нет. Наём
дополнительно связывает неизменный target с MD-заявкой и повторно проверяет
собственность/операционность цели. MD сохраняет target в заявке; изменение
actor/source/target/fee/budget отменяет допуск. При NPC-пилоте присутствие
игрока пассажиром само по себе не исключает корабль.

Все14 существующих Lua fixtures прошли единым коротким пакетом; MD/XSD и
адаптированное замыкание507 PASS. Эти изменения пока staged, игровой read-back
не выполнялся. Installed502 последний подтверждённый пакет; задачи остаются
открытыми до соответствующей игровой приёмки. Длительный прогон не запускался.

## Source505 — точная связь native hired builder со стройкой

Installed502/PID14692 после штатного restart, load502 terminal0/accepted.
build503 terminal0: первый builder_near отказал paid_native_order_unavailable
до появления нового заказа; денег/приказов/положения не менял. Короткие чтения
показали ожидаемую pending plot licence и отсутствующий builder, без новых
собственных MD/AI ошибок. Это не приёмка строительства.

Однократный role504 terminal0 после естественного перехода: PFY-706,
station0x4bd6c/build0x1dee, buildstorage3108364Cr/wanted3108364Cr;
plot_19 observed, funding_2 observed. Builder key builder_hire_2_402626.879:
ship0xaa8c == actualbuilder0xaa8c, constructionmodule0x4bd69,
deployed0/sent. Реальный оплаченный корабль привязан; развёртывание ещё
не наблюдалось. Не объявлять sent успешным прибытием.

Подготовительная команда501 ошибочно исключала даже этот же привязанный
корабль. Source505 исключает только другого actualbuilder; переносит к
buildstorage (2–3км), сохраняя native order/payment/bindings и отсутствие
forced deployment/build completion. MD/XSD/scheduling505 PASS. Изменение
пока не установлено; Installed502 текущий, задача3.4 остаётся открытой.

## Source501 — команда подготовки перелёта оплаченного застройщика

Диагностическая `builder_near` принимает только действующую native_hired
квитанцию sent с реальной paid суммой, тем же submission key/paid/orderindex,
живыми ship/station/build, штатным DeployToStation на эту станцию и активным
governor. Корабль под штурвалом игрока, изменившийся приказ, уже развёрнутый
корабль или существующий строитель станции исключаются. Повторная попытка
не перемещает корабль вновь, даже при unknown результате.

Единственный эффект — штатный warp рядом со станцией (10–15км) для сокращения
перелёта в тестовом мире. Команда не назначает строителя, не меняет его приказ,
не запускает/завершает build, не платит и не заменяет продуктовые квитанции.
Последующее реальное native deployment и строительство проверяются отдельно.
Штатный контракт station параметра проверен в order.build.deploy.xml;
warp/safepos — в common.xsd. MD/XSD/scheduling, Python dispatcher и Lua syntax
501 PASS. Команда пока не установлена/не исполнена; Source498/500/501 staged,
Installed496/PID7280 остаётся текущим. Задача3.4 не закрыта.

## Source500 — строительная граница перед оплатой застройщика

role499 terminal0 из текущего PID7280/Installed496. Native construction
PFY-706: build0x1dee, processing1, реальный constructor0xb798,
три resource types; рабочий buildstorage budget3108364Cr совпадает с wanted.
Plot geometry/licence observed (plot_19_402551.857); construction funding
observed (construction_funding_2_402611.875). Новый hiring key
builder_hire_2_402626.876: paid50000Cr, sent/native deployment pending.
Общий read-back не содержал hired ship identity, поэтому нельзя считать
constructor0xb798 именно этим нанятым кораблём или объявить arrival observed.

RequestHiredBuilder уже проверял отсутствие существующего строителя при
поиске. Source500 повторяет эту проверку непосредственно при утверждении
quoted fee перед Lua-оплатой: если за время котировки строитель появился,
approval отклоняется без платежа и без замены работающего строителя.
Диагностический construction_receipt теперь читает hired ship/deployed/
constructionmodule/actualbuilder, чтобы проверять реальную привязку,
а не угадывать по одному наличию constructionvessel. MD/XSD/scheduling500
PASS. Source498 cleanup и500 пока не установлены; Installed496 текущий.
Игровую проверку новой защиты и полную задачу3.4 не закрываем.

## Source498 — общая MD/AI граница подтверждена реальным ремонтом

Installed496:50SHA, X4 PID7280; load496 terminal0/accepted/save_004;
service497 terminal0. На реальной границе build.shiptrader зафиксированы
employee0x1893ee, Manager16cea4, session5, period402513.926,
ship0x18be71, before20/target80. MD NativeRepairObserved получил тот же ship,
station0x18893f/session5. Read-back: state active/hasperiod1/captured1,
hull20→80 и ServiceEvents.repaired=1. Прежний null State в AI устранён.
Это подтверждает ремонтную запись через штатный эффект, не платный заказ
ремонта и не все сценарии сервисной оценки/военных guards.

Бюджет снова подтверждён: key station_funding_1_402517.367,
67800Cr, exact debit42286126→42218326 и credit67800→135600,
native payment reconciled, тот же key при следующих чтениях.
Свидетельства: service497/responses.json и свежий debug.log.

В check_adapted_manager добавлена проверка всей границы: ни один собственный
AI не читает symbolic MD Registry/Assets path, после каждой смены/удаления
State/ManagerCue в MD следует синхронная публикация. PASS.
Source498 удаляет временные AI/MD debug_text, shared repair trace и его
диагностический reader; repair observation и shared AIState сохранены.
Overlay/XSD и guard checks498 PASS. Cleanup498 пока не установлен;
текущая игра содержит496. Полная приёмка задач остаётся открытой.

## Source495 — исправление общей границы состояния MD → AI

Installed492:50SHA read-back, X4 PID50692. load492 terminal0/accepted;
service493 terminal0. Реальный ремонт снова hull20→80, count null.
Свежий AI log дал decisive read: hasperiod=1, state=null в build.shiptrader
при чтении `md.TM_Empire_Runtime.Registry.$State`. Одновременно запись trace
на component отвергнута движком (нельзя писать component.$custom); не принят
trace=0 как доказательство отсутствия выполнения. Нативные build.shiptrader
и trade.find.commander побайтно совпали с08.cat (`native494.json`).

Source495 публикует state/manager/session в shared global.$TM_EmpireAIState.
PublishAIState вызывается синхронно после каждой установки/удаления State и
ManagerCue в Runtime и генерируемом Manager, перед ValidateBinding и после
обновления ObservationSession на load. AI-наложения ремонта/торговли и все
13 генерируемых AI-скриптов читают эти shared значения вместо symbolic MD cue
paths. Защиты ownership/helm/manual/claim остаются на прежних местах; state
при отсутствии governor публикуется inactive. Это общая граница, не ослабление
guard ради теста. Source normalizer сохраняет её при повторной генерации.

Временный trace теперь в отдельном shared global (инициализация на load),
не на component и не в ServiceEvents. MD/XSD/scheduling, два AI overlays и
shared13 guards495 PASS. Игровой эффект исправленной границы ещё не доказан.
Source495 не установлен; Installed492 остаётся текущим, долгий прогон не начат.

## Source491 — реальное пополнение бюджета подтверждено, ремонт ещё открыт

load488 terminal0/accepted/save_004; сервисный клиент489 terminal0. X4 PID5556.
Installed488 содержит487, но не490/491. Создана верфь EVK-462 (0x18893c),
штатный shiptrader0x188ae0; ремонт корабля0x18b51c hull20→80 подтверждён
четырьмя чтениями. Read-back repair_context: parent complete, listener waiting,
station в ServiceStations (index3), observation exists, employee/manager/session
все совпали. Service count остаётся null. Две строки debug_text в логе не
появились даже с general; по отсутствию строк исполнение не определяется.

Бюджет KMT-485: подготовка реально снизила счёт150000→67800Cr;
диагностическая квитанция подготовки unknown, поэтому её успех не заявляется.
После native_analysis продукт сам запросил и оплатил67800Cr: платёж key
station_funding_1_402517.297, before42286126/after42218326Cr,
stationbefore67800/stationafter135600Cr, paid67800, state reconciled.
Несколько последующих чтений содержат тот же key/paid, повторного перевода нет.
Это реальное подтверждение исправленной station_funding границы, не принятие
всей экономики3.2/feedback5.4. Сырой read-back: service489/responses.json.

Source491 добавляет один последний AI boundary trace на собственную станцию
с реальным ship/time/governor-state/наличием period/captured; диагностический
repair_read читает его без изменения мира. Это временная трассировка причины,
не ServiceEvents/экономическое наблюдение и не результат ремонта. Перед
чистой поставкой трассировку удалить. XML overlay/XSD/MD/scheduling491 PASS.
Источник пока не установлен, причина отсутствия repair signal не доказана.

## Source490 — общая Lua-граница строительства/застройщика/снабжения

Проверка остальных вызовов выявила тот же GetComponentData(C-ID) в
construction_funding, construction_builder и purchase_dispatch (снабжение).
Вызовы используют исходные request/r userdata; C API и TransferPlayerMoneyTo
сохраняют64-bit ID по штатным примерам menu_map/menu_interactmenu.
Fixtures construction_funding/construction_builder/supply_payment теперь
проверяют настоящий Lua component ID вместо разрешения числового C ID.
Все три PASS, включая однократность платежа/заказа, изменение условий и
unknown effect. Реальное строительство/найм застройщика/снабжение после
этого исправления ещё требуют проверки. Source490 не установлен.

Installed488 содержит487 и диагностический repair_context (состояние parent
и listener, membership group, employee/manager/session binding). После
штатного закрытия PID20372 новая X4 PID5556 запущена через Steam.
Клиент load488 session51673 ещё ждёт; не запускать конкурирующий клиент
загрузки и не перезапускать игру только из-за ожидания. Сервисный сценарий489
подготовлен, но ещё не запущен: вместе с ремонтом включает реальное
снижение бюджета тестовой KMT-485 и штатный native_analysis.

## Source487 — исправлена Lua-граница бюджета и торговых котировок

Installed485 подтверждён50SHA. X4 PID20372; load485 accepted/save_004,
сервисный клиент486 terminal0. Готовая верфь UMG-880 (0x188942),21модуль,
shiptrader0x188ae6; native_analysis requested. Реальный ремонт0x18b2b0 снова
hull20→80, четыре read-back. Счётчик всё ещё null; причина не доказана,
приёмка ремонта/сервисной оценки остаётся открытой. Ошибки player.position,
TradeChoices list/null и раннего $Timeout в свежем журнале не повторились.

В UI station_funding и trade_choice_quote GetComponentData вызывался с
ConvertIDTo64Bit результатом, тогда как API требует Lua component ID; журнал
содержал invalid cdata argument. Теперь для GetComponentData используется
исходный userdata, для C API/нативных торговых вызовов сохранён64-bit ID.
Fixtures теперь различают два типа и отвергают C ID в GetComponentData;
оба fixtures PASS, включая отсутствие повторной оплаты и неизвестный эффект.
Живое пополнение бюджета/котировки после правки ещё не испытывались.

Два сообщения ремонта переведены из стандартного scripts-фильтра в general:
в486 они не появились; отсутствие строки не доказывает отсутствие выполнения.
Последний установленный пакет485 не содержит487, долгий прогон не запускался.

## Source484 — результаты короткого сервисного пакета483

Клиент483 завершился terminal0. Настоящая верфь QDH-824 (0x188941) создана:
21 модуль, operational/canequip=1, штатный shiptrader 0x188ae5. После команды
native_analysis настоящий период наблюдения появился за один повтор через10с.
Корабль0x18b00c создан docked; штатный repairs_initiate восстановил hull20→80,
подтверждено четырьмя read-back. Product service count осталось null во всех
четырёх чтениях: ремонт выполнен, наблюдение результата НЕ принято. Приёмка
сервисной оценки остаётся открытой; бесплатная подготовка не доказывает оплату.

Исправлены две подтверждённые ошибки нового пути: player.position заменён
на player.entity.position в safepos; TradeChoices на load инициализируется
пустой таблицей вместо удаления (ReadStationEvidence раньше перебирал null).
В генераторе собственная адаптация timeout watcher теперь проверяет наличие
$Timeout перед сравнением: штатная переменная устанавливается только после
доставки платного корабля, дочерний watcher уже активен в ожидании доставки.
Это не сбрасывает оплаченный заказ/receipt и не запускает приобретение вновь.

Добавлены сообщения на фактической AI-границе ремонта и входе MD event для
локализации потери наблюдения при следующем общем коротком пакете. Причина
потери события ещё не доказана. Сборка/MD/XSD/scheduling/AIScript overlays и
shared13-script guard484 PASS. Source484 пока не установлен; Installed482
остаётся текущим. PID30496 жив. Исправленные в480 prerequisite/group init
ошибки не встретились в свежем логе; hire optional поле отдельно не испытывалось.

## Installed482 — короткий сервисный сценарий

Source480/481 установлен единым пакетом после штатного завершения X4.
Все50 файлов подтверждены SHA read-back (`installed482-readback.json` в
текущем временном каталоге). X4 PID30496 запущена через Steam без добавления
параметров; load482 принял `save_004`, клиент загрузки завершился terminal0.
Это подтверждает запрос загрузки, а не готовность игрового мира.

Сервисный клиент483 использует один pipe: `service_setup`, существующий
`native_analysis` для реального штатного отчёта, затем ограниченное ожидание
периода наблюдения (не более60с после готовности мира), один запуск ремонта
и четыре read-back. Повторные запросы repair_setup допускаются только пока
отсутствует сервисная станция в наблюдениях и попытка ремонта ещё не создана.
Результаты сохраняются после каждой команды; итог проверяется отдельно.

## Source481 — подготовка сервисного сценария и привязка оценки к сотруднику

Диагностическая команда `service_setup` создаёт одну готовую собственную
станцию по штатному плану `arg_wharf`, отдельного менеджера станции и продавца
кораблей через назначение `controlpost.shiptrader` и `NPC_Shiptrader.Base`, как
в `inituniverse.CreateShipDealerEntity`. Повторная команда не создаёт вторую
станцию, в том числе при неподтверждённом результате. Это бесплатная подготовка
тестового мира, не проверка покупки, строительства или найма. Команда не
подставляет экономические наблюдения и не запускает ремонт: сценарий ремонта
по-прежнему требует настоящий период наблюдения и штатного продавца.

Пассивная торговая запись и её MD-приём/чтение теперь требуют существующего
сотрудника станции. Совпадение двух null-значений не позволяет обвинять
отсутствующего менеджера в выборе поставщика; quote response и завершение
покупки также отвергают запись утраченного сотрудника.

MD/XSD/scheduling, XML-наложения штатных AIScript, общий guard адаптированных
13 скриптов, Python-диспетчер и синтаксис диагностического Lua прошли.
Игровое создание сервисной станции и ремонт ещё не подтверждены. Source480/481
пока не установлены; Installed478 остаётся последним установленным пакетом.
Длительный прогон не запускался, задачи приёмки остаются открытыми.

## Source480 — исправление общей инициализации при старом save/load

Installed478:50 SHA совпали, X4 PID10156; load478/save_004 accepted и мир
подтверждён short479 terminal0 (10команд,4read-back). Все12 engine MD boundary
cases causal rule совпали с expected (positive1,11negative0). Это synthetic
расчёт, не живое доказательство неэффективного выбора. Платный hire снова
sent→observed; старый transfer unknown не сбрасывался. Ремонт не исполнен,
своей сервисной станции нет в bounded sample. Длительный прогон не запускался.

Свежий log выявил три корня загрузки: (1) новый global personnel_prerequisites
не создан в старом save, поскольку ComponentRecords cue уже complete;
(2) event-group обработчики активируются до создания ServiceStations в Loaded;
(3) optional assignmentissued читается без @ в раннем hire receipt.
Source480 добавляет idempotent EnsurePersonnelPrerequisites на load и перед
обработкой/записью очереди; существующие role needs/receipts не очищаются.
Group listeners перенесены под единственный ServiceEventsReady, который ждёт
создания группы; Loaded сбрасывает этот родитель после создания группы, чтобы
на reload не множить подписки. Optional assignmentissued читается через @.
MD/XSD/scheduling480 и shared13-script guards PASS; игровой повтор исправлений
ещё не выполнен. Installed478 пока старый; source480 не установлен.
Ошибки $homebase.type из стороннего mobile_space_station_ru отмечены отдельно,
чужой мод не изменён. Задачи кадров/оценки/приёмки остаются открытыми.

## Source477 — MD boundary cases и чтение реальной торговой цепочки

Добавлена диагностическая trade_decision_fixture:12 случаев вызывают именно
продуктовый AssessTradeDecision в MD. Synthetic context помечен явно, не
попадает в State.TradeChoices, экономические наблюдения или UI-оценку и не
меняет игровой мир. Проверяет positive, manual, buyfree, incomplete, quote
после покупки, недостаточный объём, другая зона, длиннее путь, changed price,
тот же seller, unknown quote и отсутствие покупки. Это будущая проверка
математики/ветвлений в движке, не доказательство реального плохого выбора.
Продукт теперь дополнительно требует другого seller для альтернативы.

Role read выводит до8 реальных TradeChoices: automatic/alternatives/quotes/
purchase/decision/key. Позволяет проверить native search→Lua quote→completed
trade→classification без принятия одного heartbeat. MD/XSD/scheduling477 и
Lua syntax/UI rendering/native quote fixtures PASS. Source474–477 не установлен;
MD fixture ещё не запускался в игре и положительный живой случай5.3 не принят.

## Source476 — причинное правило стоимости штатной закупки

AssessTradeDecision использует настоящую native trace, quote для того же
корабля до покупки и завершённый Trade с точным source offer. Требует automatic
assignment.trade/TradeRoutine, отсутствие manual/priority/loop, полный bounded
список, buyfree=false, фактический объём и сохранение выбранной quoted price
до завершения. Альтернатива — тот же товар/объём, подтверждённый native
CanTradeWith/price, тот же sector/zone, без увеличения наблюдаемых двух расстояний.
При меньшей цене сохраняет manager_decision для конкретного выбора закупки,
разницу стоимости относительно возможности на момент решения и medium confidence.
Не заявляет общий ущерб выпуску, гарантированную будущую экономию или отсутствие
изменения альтернативы в пути. Idle/низкий навык/сырой список продавцов не подходят.

ReadStationEvidence принимает decision только своего текущего employee/manager/
period/session. Responsibility сохраняет независимые provision/external как
mixed; conditions добавляет отдельную procurement/purchase_price_difference.
UI допускает manager_decision и до7 условий, явно пишет «Решение менеджера при
закупке», причину и рекомендацию проверить выбор, без автоматического увольнения.
MD/XSD/scheduling476, merged overlay selectors/XSD/native SHA и UI fixture с
реальным callback rendering новой строки/отрицательным impact PASS. Причинные
MD positive/negative и игровые случаи ещё не проверены;5.3/6.5 остаются открытыми.
Source474–476 ещё не установлен, installed472 остаётся49files.

## Source475 — штатные цены выбранного и альтернативных предложений

Добавлен пассивный ui/trade_choice_quote.lua: GetTradeData(offer, ship).price
берётся непосредственно из игры; MapMenu21955–21982 использует этот price для
общего изменения цены, включая pricemodifiers. Своя формула скидки не создаётся.
На каждый реальный выбор MD передаёт до17 уже найденных offers; Lua проверяет
selloffer/source identity, amount/minamount и штатный CanTradeWith для того же
корабля. Исчезнувшее предложение/недостаточная доступность/ошибка API/NaN дают
unknown. Никакие trade orders, резервирование или оплата не выполняются.

Response привязан к request key/ship/station, MD принимает в пределах2sec с
повторной проверкой employee/manager/period/session/helm/commander. На load
pending quote boards очищаются. Параллельный более новый choice не наследует
старый ответ. Quotes дополняют native trace; пока не объявляются causal
manager_decision без завершённого сопоставимого случая. MD/XSD/scheduling475,
Lua fixture positive80.8/permission/revoked binding/NaN/wrong seller PASS.
Fixture использует mock engine и не заменяет игру. Installer dry-run50files
PASS; source474–475 ещё не установлен, installed472 остаётся49files.

## Source474 — первопричина кадровой ошибки short473

Short473 terminal0; read-only trade_quote_probe вернул4 настоящих offers и
GetTradeData с кораблём/без него. Подтверждены engine fields price/marketprice,
amount/minamount, pricemodifiers table, source station/id. В первом selloffer
price1874.96Cr отличается от marketprice1966.76Cr; GetTradeList и оба GetTradeData
дали одинаковые значения. Это подтверждает доступность quote API; конкретный
состав pricemodifiers и связь с оплатой ещё нужно сверить до causal вывода.
Ремонт снова сообщает отсутствующую свою сервисную станцию, не PASS.

Game выявил StepPersonnel $Need.$manager lookup. Первопричина установлена в
tools/adapt_native_manager.py:1245–1264: старое personnel_needs уже используется
штатным адаптером Upkeep для role need ($shiptrade/$trade/другие роли) по Object.
Наш prerequisite queue ошибочно занял тот же namespace и ожидал manager/goal.
Source474 разделяет данные: personnel_needs сохранён адаптеру без изменения,
очередь капитанов теперь personnel_prerequisites с отдельной инициализацией и
registry field. Не очищает и не переинтерпретирует старые role needs. Перед
чтением metadata StepPersonnel проверяет table/manager/goal, повреждённые записи
новой очереди удаляет без эффекта. MD/XSD/scheduling474 и shared13-script guards
PASS. Исправление ещё не установлено; игровое отсутствие ошибки не доказано.

Installed472:49 SHA совпали, X4 PID50412, load472/save_004 accepted и игровой
мир подтверждён short473. Совместное с mobile_space_station_ru объединение diff
проверено в обоих порядках: exact selectors/XSD/unchanged native+foreign SHA PASS.
Новое tooling ForeignOverlays/ForeignLast проверяет реальные attribute replaces
и add в памяти. Полный длительный прогон не запускался;5.3 и другие gates открыты.

## Source471 — read-only проба штатных торговых цен

Найдены штатные GetTradeList(station, ship, false) (MapMenu22999) и
GetTradeData(trade, ship) (MapMenu1063). По исходникам второй интерфейс точно
используется для параметров приказа; effective price из этого ещё не следует.
Добавлена диагностическая trade_quote_probe: MD передаёт только station/ship
из существующего HireScenario; Lua читает до4 offers и печатает до24 scalar
fields каждого GetTradeList/GetTradeData с кораблём и без него. Ни сделок,
резерваций, скидок, денег или приказов эта команда не изменяет. Ошибка API или
отсутствующий контекст возвращаются отдельным результатом, не нулевой ценой.
Команда нужна для подтверждения engine fields в следующем коротком пакете,
не добавляет новый продуктовый price calculator. MD/XSD/scheduling471 и
Lua syntax runtime PASS; source471 не установлен, игровой результат отсутствует.

## Source470 — сопоставимость альтернатив и чужой trade overlay

Наблюдение ограничено именно station homebase (мобильный resupplier не
попадает в оценку менеджера станции). Для выбранного и альтернативных
предложений сохраняются source offer, sector/zone продавца и расстояния двух
плеч на момент решения, sector корабля/станции. Геометрическое расстояние
не объявляется безопасным маршрутом: это сведения для проверки сопоставимости,
не готовое обвинение менеджера. Native quote остаётся ценой без доказанного
учёта будущих скидок; GetTradeData(trade, ship) найден как штатная UI-граница,
но её конкретные fields/effective-price контракт ещё предстоит подтвердить.
Merged native XPath/XSD и неизменность originals SHA PASS; source468–470
пока не установлен.

Проверка установленных cat/loose путей нашла единственный сторонний overlay
trade.find.commander в mobile_space_station_ru. Его полный diff прочитан:
он меняет FindCommanderStation/homebase chain и warebasket, добавляет wares
resupplier после tradewares. Возврат buyoffer/selloffer и наш selector не
изменены; наши add перед return не меняют его selectors. Чужой файл не правился.
Предварительная совместимость структуры подтверждена чтением, проверка
совместно объединённого XML и игровая корреляция остаются обязательными.

## Source469 — связь выбора с фактической торговлей и срок хранения

Native choice сохраняет исходный selloffer. event_player_trade_completed
связывается с ним по trade.tradeoffer, точным buyer ship/seller/ware и текущему
employee/manager/station/period/session. Записывает transferredamount и native
unitprice только после завершённой передачи; отдельно сохраняет buyfree этого
покупателя. Похожие товары/названия и снимок запаса не заменяют идентичность.
Повтор события не перезаписывает уже наблюдённую покупку. Это ещё не проверка
потери результата или фактического списания счёта: причинная5.3 открыта.

Исправлена приёмка native defaultorder: он допускается как точная сохранённая
идентичность наряду с обычной очередью. Cleanup раз в1min удаляет из bounded32
trace потерянные активы, смену сотрудника/периода/командира и записи старше30min,
так что прежние корабли не занимают все слоты навсегда. На load traces очищаются.
MD/XSD/scheduling469 и merged overlay selectors/XSD/native SHA PASS; source468–469
не установлен, игровая корреляция ещё не доказана. Installed466 остаётся48файлов.

## Source468 — реальный выбор торговли и кандидаты из штатного поиска

Добавлен пассивный trade.find.commander overlay перед штатным return buyoffer/
selloffer. Поиск предложений, выбор, случайный порядок, blacklists и эффекты
остаются штатными. Снимаются выбранный seller/ware/amount/quote и до16 других
доступных предложений того же товара из уже найденного штатного списка, с
повторной проверкой доступности/запрета нелегального груза. Scope — только
покупка своим подчинённым для своей станции; другие торговые ветки не наблюдаются.
MD хранит до32 последних traces по кораблю, связывает exact order/station/
employee/manager/period/session и отбрасывает stale/helm/смену командира.

Это факты поиска, не завершённая торговля, не полная альтернативная стратегия
и не доказательство ошибки. Quote не выдаётся за фактически уплаченную цену.
Для причинной ветки ещё нужны связанный фактический расход/результат и проверка
сопоставимости маршрута/объёма/ограничений альтернативы. manager_decision не
подменён формальной веткой без таких фактов, задача5.3 остаётся открытой.
Merged overlay XPath/XSD/native SHA и MD/XSD/scheduling468 PASS. Source468
не установлен: сначала нужна проверка overlays других модов для этого скрипта.

## Installed466 / short467 — накопленный пакет и короткая проверка

Штатное завершение PID43312, установка source460–465 одним пакетом, запуск
через Steam: текущий X4 PID16088. Все48 файлов установочного манифеста совпали
по SHA (installed466-readback.json), qualified_release=false. Диагностические
MD/Lua465 скопированы отдельно. Load466 завершился с accepted save_004; текущий
мир подтверждён ответами short467, а не только ответом меню загрузки.

Проверены51 cat-индекс и loose пути расширений: build.shiptrader меняет только
официальный ego_dlc_pirate/ext_03.cat. Его262 байта/digest и reference совпали;
patch меняет allowextmacro (Асгард), не наш repair handler. Originals и чужие
файлы не записывались. Синтаксис diagnostic Lua штатным runtime PASS.

Short467 terminal0:8 команд,4 игровых read-back402514.099–402544.289 (~30sec).
Реальный платный hire sent→observed, actor0x18892e, native fee104047000 MDunits,
target0x188933; предыдущий unknown transfer не сброшен. Штатный Manager учёл
подготовленный ownerless→player сектор: claimed1→2, новая Hold goal с двумя
подцелями, purchase building. Cue.state complete означает инициализацию,
не завершение обороны. Ремонт не исполнен: подходящей своей сервисной станции
нет в bounded sample. Это отсутствующая предпосылка для подготовки следующего
тестового мира, не PASS ремонта. Остальные проверки продолжились независимо.
Длительный прогон не запускался. Общие задачи и причинная manager_decision
остаются открытыми; short467 не доказывает весь функционал персонала/обороны.

## Source465 — короткий диагностический сценарий штатного ремонта

Добавлены repair_setup/repair_scenario/repair_read. Setup ищет до32 собственных
оперативных сервисных станций с настоящим shiptrader и текущим наблюдением,
создаёт один диагностический scout в доке и повреждает его корпус до20%.
Run единожды сигнализирует существующему штатному обработчику repairs_initiate
целевой hull80; запись sent предшествует эффекту. Read отдельно возвращает
реальный hull и счётчик наблюдений до/после. Подготовка мира не записывает
продуктовый результат. Повторный запуск sent/unknown не выполняет ремонт заново.
Этот сценарий проверяет наблюдение фактического ремонта, не обычную оплату заказа.
Если подходящей своей станции нет, сообщает отсутствующую предпосылку без
подмены результата или захвата чужой станции. MD/XSD/scheduling465-final и
компиляция Python PASS. Диагностика и source460–465 ещё не установлены.

Проверка текущего процесса: X4 PID43312 существует. В установленном extensions
не найдены loose build.shiptrader.xml других расширений; архивные cat/dat overlays
этим поиском не проверены, общая совместимость пока не заявляется подтверждённой.

## Source464 — результат ремонта на штатной границе исполнения

Вместо асинхронной пары repairs_initiate/repairs_done добавлен пассивный diff
aiscripts/build.shiptrader.xml. Он снимает hull до штатного restore_object и
после него в одном существующем обработчике, затем передаёт факт в MD. Никакие
штатные платежи, ремонты, приказы или назначения не заменяются. Наблюдение
ограничено собственными станциями при active управляющем и текущем периоде.
MD требует фактического улучшения корпуса до целевого значения, свежего события,
совпадения сотрудника/управляющего/периода/сессии. Смена менеджера или load
отбрасывают старый факт. Component-only ремонт пока не заявляется измеренным.
Старая пара событий и её очередь удалены, чтобы один ремонт не считался дважды.

Установщик включает aiscripts overlays; dry-run показывает 48 файлов без
изменения установки. Новый validate_aiscript_overlays.ps1 проверяет единственность
XPath-границ, XSD объединённого скрипта в памяти и неизменность SHA оригинала.
Проверка overlay и MD/XSD/scheduling464 PASS. Переносы строк штатных expression
нормализуются только в памяти валидатора, исходный скрипт не записывается.
Перед игровой пробой остаётся сверить совместимость с установленными overlays
чужих расширений. Source460–464 пока не установлен; задачи5.2/5.3 не приняты.
Причинная ветка manager_decision требует отдельного завершения; захват списка
допустимых торговых предложений сам по себе не доказывает ошибку менеджера.

## Source463 — единые ограничения для кадровой предпосылки

Потребность в капитане теперь записывается в конце CanUseOwnedShip, после
проверок ручных приказов, текущего поведения, командира, принадлежности claim,
unknown/missing/stoprequested/issuing и незавершённого переподчинения. Отсутствие
капитана больше не позволяет обойти эти ограничения при постановке потребности.
StepPersonnel повторно вызывает ту же проверку для исходной доменной цели перед
выбором приоритетной вакансии: изменившееся назначение корабля не запускает
найм через очередь. Существующий капитан в пути не создаёт новую потребность.

MD/XSD/scheduling463 и проверка замыкания 13 адаптированных скриптов PASS.
Изменения source460–463 пока не установлены и не приняты в игре. Полный
длительный прогон не запускался; сначала остаётся завершить функционал и
короткие проверки подготовленных командой сценариев. Задачи 4.4/3.7 открыты.

## Source462 — вакансия капитана как предпосылка штатной доменной задачи

Ранее global personnel_needs инициализировался, но не использовался. Общий
CanUseOwnedShip при действующей цели и реально свободном post aipilot теперь
передаёт bounded need (manager/goal/post/ship) единому StepPersonnel. Транзит
существующего капитана не вызывает второй найм. Helm/manual/priority,
неразрешённая reassignment и конфликтующий claim не создают эту потребность.
Максимум32 ключа, повторное наблюдение того же корабля не добавляет дубликат.

StepPersonnel чередует обычный asset scan с приоритетными предпосылками,
проверяет до8 вращающихся needs за шаг, удаляет закрытые вакансии/потерянные
объекты/предыдущее назначение/отменённые цели. Использует существующие native
RequestTransfer/RequestHire, средства и unknown guards; новый исполнитель не
создан. Обычный просмотр собственности не вытеснен вечной одной вакансией.
MD/XSD/scheduling462 и adapted guard/13-script closure PASS. Source460–462
ещё не установлен, игровая автономная реакция4.4 пока не принята.

## Source461 — отдельные факты оплаты и прибытия во вкладке

AssignPaidHire после проверки точного paid payment receipt фиксирует paid в
hire receipt до назначения. Это подтверждённое списание, не обещанный nominal
amount и не факт прибытия. При stale governor/должности оплата остаётся видна,
но назначение не объявляется успешным. ObserveHire по-прежнему требует employee,
seed/post/container/no transit и actual paid receipt для observed.

UI projection для найма передаёт paid в Cr только при записанном подтверждении,
и отдельно observed timestamp существующего receipt. Lua валидирует finite,
nonnegative и0.01Cr precision; показывает «Подтверждённая оплата» отдельно от
state и информации о прибытии. Timestamp называется временем наблюдения, а не
автоматическим доказательством завершения. Unknown не выдаёт nominal как paid.
MD/XSD/scheduling461 и UI fixture (pending paid80.8Cr, invalid/NaN/subcent) PASS.
Source460–461 ещё не установлен; current product457/PID43312. Приёмка5.5/5.6
требует реального нового UI read-back и остальных ещё открытых условий.

## Role459 / source460 — военный Recon и правдивый статус исполнения

Role459 terminal0/PID43312: purchase11_402533.654 delivered/nativegoal Start;
purchase12_402624.368 building. QBF441 имеет own claim sent,1 native tracked/queued
order Recon, assigned/active captain0x19659a совпадают, roleobjectnull,
intransit0. Это реальная работа собственного военного корабля, не только
существование цели или оплаченного заказа. Полная оборона/угроза3.6 ещё открыта.

Source460 исправляет UI проекцию стратегических задач: planned заменяется sent
только при актуальном собственном приказе корабля соответствующей native subgoal.
ReadMilitaryExecution читает native registry table.$Cue, groupShips, own claim,
manager/goal binding и actual Ship.orders membership. Максимум16 subgoals,
32 различных sampledships и16 orders/ship; helm/stoprequested/чужое/неоперативное
не доказывает работу. Partial отмечается, sent не объявляет результат observed.
MD/XSD/scheduling и UI fixture PASS; source460 ещё не установлен.

## Short458 — реальный платный найм и новая военная покупка

Load457 controller40355 и short458 controller83550 terminal0. PID43312/current
product457. В7 запросах за30.3s: recruitable service actor0x188924,
seed-6190938264116987476 (=unsigned template12255805809592564140), target0x188929,
hire_1_402513.843 sent→observed402536.846. Employee тот же actor и seed, controlpost
aipilot; сначала intransit1/containerSource0x14090, затем intransit0/containerTarget,
roleobjectnull допустим при native assigned post. Итог native_paid_hire_arrival_observed:
реальный платный найм и прибытие подтверждены за23.003s, не по одному sent.

Fixture подготовил только отдельного NPC и корабль; продукт использовал native
fee56,004,000MD money units=560,040Cr, обычную оплату и assign_hired_actor.
PlayerMoney42,203,926→40,455,058: разница1,748,868Cr складывается из этого найма
560,040Cr и нового native ship purchase1,188,828Cr (submission id35523,statebuilt).
Полный ledger не опрошен; связанный native hire receipt доказывает оплату отдельно.
Старая purchase id1098234/reconciled не повторилась. Штатная военная цель нового
сектора имеет2 subgoals; наблюдается новая корабельная покупка, фактическая доставка
и fleet order ещё не подтверждены. Legacy transferunknown не сброшен.

Source455 устранение component-wrapper approval отказа подтверждено в игре.
Полная4.1/4.4 и3.6 ещё открыты: нужны автономное выявление вакансии/отрицательные
случаи и реальное назначение корабля, а не только адресный RequestHire/покупка.

## Source456 — crew exchange approval привязан к проверенной паре

Дополнение installed457: PID33268 штатно закрыт; общий product packet455–456
установлен (47 files, qualified_release=false). Запущен новый X4 через Steam.
Load457 controller40355 единственный текущий pipe owner, ждёт главное меню.
После terminal0 запустить short_scenarios.py с новым outputdir short458;
не повторять эффекты short454 в прежнем мире и не сбрасывать unknown.

Аудит связанной Lua границы выявил, что checked receipt crew exchange содержал
только key/state: новый approved request того же key мог заменить target/seed/role
и пройти новую native capacity check как другой перевод. Checked теперь сохраняет
source/target/seed/role, submit требует те же component IDs через IsSameComponent
и те же seed/role. Изменение отклоняется до PerformCrewExchange2 effect. Native
capacity/membership/scheduled/helm проверки остаются, неизвестный эффект не повторён.
Ownership принимается строго true/1, numeric0 больше не считается собственностью.
personnel_transfer_contract_fixture PASS: четыре изменённых поля, numeric0,
helm/capacity/replay/unknown. Источники455–456 пока не установлены; game446.

## Short454 / source455 — реальные независимые результаты и ошибка component equality

Load452 controller6409 и short454 controller6923 terminal0. PID33268 загружен.
Короткий пакет завершил7 запросов: setup, hire, territory и4 read snapshots,
наблюдаемый период402514.036–402544.256 (30.22s). Responses сохранены сразу.
Кандидат service actor0x188926/seed4945335915547381829 hirable1/remote1,
target0x18892b/pilotnull; RequestHire sent hire_1_402513.881. Затем rejected
hire_approval_revoked до оплаты, employee отсутствует:4.1 не принята.

В Source445 проверка current.actor/source через ~= сравнивала Lua userdata
обёртки повторно считанного blackboard. Source455 заменяет её штатным
IsSameComponent с предварительной проверкой datatype. Same-key fee/budget/state
сохраняются. Fixture моделирует новую wrapper identity того же actor/source и
реальную замену компонента: первый вариант допускает оплату, второй отклоняет;
PASS. Source455 ещё не установлен, устранение игрового отказа требует read-back.

military_setup observed: игрок получил ранее ownerless «Нопилеос Удача IV Луна».
ClaimedSectors1→2, native Manager goals1→2; последний read содержит новую цель
именно этого сектора с CurrentPhaseSubGoals2. Цель не сигнализировалась тестом.
Это подтверждает native HoldSpace trigger/territory propagation за30s.
Cue.state=complete означает завершённые начальные actions, не завершённую защиту:
реальные fleet orders/угроза/снабжение3.6 пока не приняты, standby0. Отношения
фракций/чужие территории не изменены. Legacy transferunknown сохранён.

## Installed452 / source453 — короткий пакет независимых сценариев

Диагностический450–451 установлен, PID39004 закрыт штатно. Load452 controller6409
ожидает меню нового X4; единственный pipe owner. Product446 остаётся тем же.
Source451 Read теперь ограниченно показывает реальные HoldSpace/Invade goals,
target/cue state/subgoals/standby/wait reason и actual owner тестовой территории.
Это read-back, не запуск цели. MD/XSD/scheduling451-final и Lua syntax PASS.

Source453 добавляет reusable short_scenarios.py: один hire setup, один найм только
при новом prepared, одна military setup и4 read snapshots/10s. Ответы сохраняет
немедленно, эффектов/retry/очисткиunknown нет, один role pipe. Python syntax PASS.
Запускать после terminal0 load452; уникальный outputdir. Игровой пакет пока
не выполнялся, принятие найма/военного домена остаётся открытым.

## Installed449 — штатный visitor контракт диагностического кандидата

Дополнение450: controller94980 terminal0. Setup449 prepared actor0x18892b,
seed2185127960165706919, target0x188930/pilot=null. Run449 отказал до оплаты,
точные flags: exists1/owned0/control0/remote1/missionnull/source0x1338a,
role passenger/hirable0. Причина — именно non-hirable роль, не виртуальность,
remote или отсутствие источника. roles.xml service hired=true, passenger без
hired; Conversations222 использует тот же role.hirable guard. Source450 меняет
только подготовку кандидата на service, сохраняет native fee/visitor/slot и
полный RequestHire путь. Продуктовая проверка верна и не ослаблена.
450 ещё не установлен. Pending controllers нет; следующий native hire test
нужен после установки общего следующего пакета и исходного test load.

Сверены NPC_Instantiation recruitable branch1969–2004 и NPC_State_Machines
ENTER_init: диагностике не хватало station_visitor=true и native title/icon
override. Признак выбирает STATE_idle; без него используется общий пассажирский
путь. Source449 воспроизводит этот контракт; причина отказа448 пока не установлена
точно, product eligibility guards не изменены. MD/XSD/scheduling449 PASS.

Установлены диагностические447–449 (MD/Lua hash receipt diagnostic-install449.json),
продукт446 не менялся. PID39004 штатно запущен, responding=true при age121s.
Load449 controller65868 завершён exit0; hire-setup449 controller94980 ждёт
готовность загружаемого мира. До завершения этого controller другие pipe-команды
не запускать. После prepared выполнить один hire_scenario с флагами candidate;
отдельно military_setup и native read-back. Оплату/прибытие пока не считать
подтверждёнными. Длительного collector нет, цель/задачи остаются открытыми.

## Installed446 / source447 — найм и подготовка военного сценария

Дополнение448: load controller37819 и hire setup controller52837 завершены exit0.
hire-setup446: prepared, station ZYH979, actor0x188933, seed6415226416128420979,
native fee35052000MD money units, target0x188938, pilot=null. Исправление443
подтверждено реальным размещением; бесплатная подготовка не является наймом.
RequestHire448: known_hireable_actor_unavailable, receipt=null, оплата не вызвана.
Source448 расширяет точный ответ готового теста флагами этого actor; guard не
ослаблен без доказательства. Survey448 ограничен16/220 stations,26 candidates,
eligible0, не включает выбранную ZYH979 и не объясняет отказ именно её кандидата.
Диагностические447–448 пока не установлены. Реальный платный найм4.1 не принят.

Пакет443–445 установлен вместе, X4 штатно перезапущен, load446/save_004 accepted.
Controller hire-setup446 запущен после завершения load controller37819;
единственный владелец role pipe — session52837, ожидает загрузку мира.
Продуктовая оплата пока не вызвана; считать успех найма без read-back нельзя.

Source447 добавляет диагностическую military_setup. Использует stock
setup.xml/SectorClaimedAchievement_DEBUG/set_owner на известном ownerless секторе,
выбор максимум16. До эффекта сохраняется sent; фактический owner даёт observed
либо unknown. Любая предыдущая попытка блокирует второй эффект. Чужие сектора,
relations и native goals не изменяются; цель защиты должен создать сам Manager.
MD/XSD/scheduling447 и Lua diagnostic syntax PASS. Source447 ещё не установлен,
живой военный сценарий не выполнялся;3.6 остаётся открытым.

## Source445 — повторная native проверка платного назначения

Между предварительным assign_hired_actor check и назначением проходит Lua оплата.
AssignPaidHire теперь повторно сверяет сохранённый seed, существование/доступность
источника и remote comm кандидата, затем вызывает native check=true перед эффектом.
Изменившаяся вместимость/должность/маршрут не обходятся из-за старого quote.
Assignmentissued выставляется только непосредственно перед единственным actual
assign_hired_actor. При изменении условий paid receipt сохранён, новый найм
блокирован; успешное назначение и прибытие не заявляются до read-back.

Lua перед списанием сверяет actor/source/fee/budget повторного approval, а не только
key/state. Fixture моделирует изменение каждого поля между quote и эффектом:
ни одного списания, hire_approval_revoked. personnel_hire_fixture и
MD/XSD/scheduling445 PASS. Источники443–445 ещё не установлены; runtime442/PID6852.
Короткий повторный найм требует загрузки исходного test save после установки
всего связанного пакета, а не очистки предыдущего неизвестного actor attempt.

## Source444 — штатная дробная цена найма и подтверждённая оплата

MapMenu.buttonHire применяет RoundTotalTradePrice(fee) * hiringdiscounts.totalfactor.
Адаптер ошибочно запрещал дробную Cr цену после скидки; теперь принимает деньги
с точностью0.01Cr, исключает NaN/Infinity/некорректную скидку и использует сравнение
реального списания с точностью меньше половины0.01Cr. Native fee/formula сохранены.
Durable receipt сначала хранит amount и paid=0; paid выставляется только после
полностью подтверждённого списания. Partial/unknown не отображают номинал как
оплату и сохраняют блокировку повторного эффекта. Фактические before/after записаны.
personnel_hire_fixture PASS: обычная/бесплатная/дробная цена80.8Cr, недостаток денег,
NaN budget, изменившаяся цена, partial и replay. Источник444 ещё не установлен;
игровая квалификация реального платного найма остаётся открытой.

## Installed442 / short probe443 — пакет и граница найма

Нормально закрыт PID49968, установлен source434–441:47 файлов; каждый установленный
SHA совпадает с manifest (install442.json), qualified_release=false. Все13 Lua
fixtures и диагностический Lua syntax PASS. Новый X4 PID6852, test save_004
загружен через pipe (load442.json); прежний collector не возобновлялся.

hire-setup442 вернул native_actor_creation_failed до создания целевого корабля
и до RequestHire/оплаты. Сравнение NPC_Instantiation1969–2004 выявило преждевременную
проверку Actor.exists до add_actor_to_room; native проверяет сам actor reference.
Source443 исправляет guard и сохраняет ссылку даже при отказе; после размещения
требует actual exists/container. MD/XSD/scheduling443 PASS. Диагностический443
ещё не установлен: повторная проба входит в следующий согласованный пакет.
Не сбрасывать State.HireScenario unknown; для следующего опыта загрузить исходный
разрешённый test save, где не было этой подготовки.

role443 подтверждает реальных капитанов EPO442/RTT402: assignedcontrolentity,
assignedaipilot и activeaipilot совпадают при null roleobject; корабли имеют native
TradeRoutine/Undock, claim sent. CRZ471 по-прежнему без назначенного капитана.
Это адресный read-back source434; полный набор helm/manual/emergency3.7 открыт.
Найм4.1 не принят: реальной оплаты/прибытия в этой пробе не было.

## Source440–441 — фактические результаты корабельного обслуживания

Добавлено пассивное наблюдение event_object_built_ship на группе своих станций:
учитываются завершённые штатные постройки, включая корабли клиентов. Для ремонта
используются штатные repairs_initiate/repairs_done из order.repair/build.shiptrader.
Учитывается только пара с привязкой к станции/сотруднику/управляющему/периоду/session
и фактическим ростом корпуса до запрошенного уровня. Pending ограничен32 кораблями,
устаревает через1min; дубликат completion без pending не считается. Ремонт только
компонентов, прибыль и доля выполненного спроса не заявлены измеренными.

UI сохраняет и показывает раздельные built/repaired counts и период. Lua fixture
проверяет отображение, границы периода, будущие данные и недопустимые счётчики;
PASS. MD/XSD/scheduling441 PASS. Исходники434–441 ещё не установлены; игровые
положительные пробы впереди, особенно порядок немедленных native repair signals.
Отсутствие наблюдаемой пары оставляет результат unknown, не создаёт фиктивный ремонт.
Задачи5.2/5.3 остаются открытыми; causal manager_decision ещё требует реализации.

Длительный collector412 остановлен. Следующий игровой пакет — короткие адресные
сценарии с командным созданием условий; полный длительный прогон после реализации.

## Source439 — результаты по назначению станции

AssessStationResults теперь использует уже накопленные текущие native events:
production добавляет фактически finished циклы с периодом; trading/storage при
complete trade_flow и положительном движении сообщает число входящих/исходящих
видов товаров и период. Объёмы остаются раздельными по ware, неоднородные товары
не складываются в фиктивную производительность. Без движения или при partial
flow результат trading остаётся unknown; отсутствие прибыли не означает провал.
Причинная ответственность отдельна: movement/cycle counts не доказывают manager
efficiency. Scope employee/manager/session/from уже проверен ReadStationEvidence.
MD/XSD/scheduling439 и UI fixture PASS;439 ещё не установлен. Ship support
completed orders и causal manager_decision остаются функциональными пробелами.

## Source438 — связанная группа native control-post исправлений

Проверены ObserveHire/ObserveTransfer: та же выявленная role433 несовместимость
null roleobject у реально назначенного/действующего капитана могла навсегда
оставлять оплаченный найм/перевод pending/unknown. Теперь назначение подтверждает
Target.assignedcontrolentity[post], actor/template/seed и employee.controlpost;
roleobject может отсутствовать, но non-null чужой объект не принимается.
Container/station/transit/pod/scheduled/source membership и paid receipt gates
сохранены. RelocateRecyclingManager также опирается на native assigned manager,
controlpost.manager и фактический Source container вместо passenger roleobject.
MD/XSD/scheduling и shared guards PASS (validate438). Source434/436/437/438
собраны вместе, пока не установлены; положительный live hire/transfer не заявлен.

## Diagnostic437 — готов короткий сценарий найма

Source-only команды hire_setup/hire_scenario подготовлены и MD/XSD/scheduling,
Python syntax PASS. Setup один раз создаёт diagnostic Argon recruitable/regular
pilot через native character definition/create_cue_actor/passenger/roleobject,
CalculateNPCHiringFee и свободный native NPC slot (bounded16 known Argon stations).
Создаёт один явно тестовый owned scout docked at source, без задания звёзд или
выдуманного HiringFee. State creating записан до эффектов, повтор setup блокирован.
Run один раз вызывает product RequestHire с реальными Manager/personnel Goal,
actor/target/controlpost.aipilot/player money; все product checks/payment receipts
сохраняются, free ship test setup НЕ считается product acquisition.
Событийные cue вызывают run_actions libraries: ранние return внутри cue были
пойманы scheduling checker и устранены. В игре437 пока не установлен/не выполнялся.
Собрать с434/436 и оставшимися функциональными изменениями перед общей короткой
проверкой; paid hire/arrival4.1/4.2/4.4 пока не закрыты.

## Diagnostic436 — подготовка короткой ситуации найма

Согласованный пользователем порядок включён в отредактированную активную цель:
реализация крупными порциями → короткие необходимые сценарии с командами мира →
групповые исправления → полный прогон только после функциональной готовности.
В HireCandidates исправлено actor.entityseed (такого свойства нет) на actor.seed
и добавлены отдельные owned/control_entity/hirable/remote/mission/source/arrival
признаки вместо одного объединённого отказа. MD/XSD/scheduling436 PASS.
Primary NPC_Instantiation1969–2004 показывает штатный recruitable character,
create_cue_actor/passenger/source role object/CalculateNPCHiringFee/add_actor_to_room;
CalculateNPCHiringFee2267–2283 рассчитывает цену от реальных native potentialskills.
Следующий diagnostic сценарий использовать этот путь для одного тестового кандидата
и существующую или явно диагностическую вакансию, без выдуманной цены/звёзд.
Product найм по-прежнему только штатно оплаченный; fixture создание отдельно.

## Короткий пакет433–435 / source434

Пользователь уточнил порядок: сначала весь функционал, короткие адресные игровые
пробы только по необходимости, активное моделирование мира командами разрешено;
полный длительный прогон после завершения реализации. Новые collector не запускать.
Load432 accepted save004, controller81877 terminal0; X4 PID49968.
Role433 terminal0: manager active, native factory queue сохранена послеload.
Обнаружена реальная несовместимость423: у assigned/active aipilot RTT402/IHR001
и других управляемых кораблей roleobject=null, transit0/scheduled0/podnull.
Source434 меняет ship staff guard на native assignedaipilot/aipilot==assigned
controlentity плюс существующие arrival guards; отсутствующий капитан CRZ471
по-прежнему запрещён. MD/XSD/scheduling/shared checks PASS;434 ещё не установлен.
HireCandidates435 terminal0 выполнен как короткое read-only обследование.
Следующие исправления собирать вместе; не перезапускать ради одной этой правки.

## Install432 — единый пакет source413–430

Save431 записан в разрешённый004 и проверен до gzip EOF/CRC со стабильным stat:
compressed91448240/uncompressed745346441/mtime1791744980.6640234.
Прежний save407 с unknown plot7 сохранён отдельно как cache artifact
parked-plot7-save407.xml.gz; quicksave/autosaves не изменялись.
PID5264 штатно CloseMainWindow/WaitForExit завершён. Install_mod --include-adapted
установил47 product files, diagnostic MD/Lua обновлены source427/428.
Steam запущен только с -applaunch392160; load432 --save save_004 session81877
остаётся текущим единственным controller owner до терминального результата.
Пакет ещё не квалифицирован: ближайший общий read-back plot/funding/mining,
assigned/active pilot, hire_candidates, staff/history/UI;6.4 не закрыт.

## Runtime412 остановлен — переход к общему пакету430

После замечания пользователя о прогоне ради одной функции collector80242 штатно
остановлен stop.request, session exit0. Summary stopped_by_request,18 samples,
elapsed5243.488s; это НЕ двухчасовая приёмка6.4. Последний017 age402325.481,
первый000397232.602: наблюдаемое игровое окно5092.879s.
Модуль завершён401393.008; новая factory0x81ba279/build0xcf15e adopted, plan8/8;
plot15_402311.193 rejected_before_effect из-за исправленной в source430 quote ошибки.
Дальнейшее ожидание frozen408 не испытывает430/428/423/414/415 и не даёт военного
или оплаченного hire положительного сценария. Следующее действие: сохранить
текущую test timeline в разрешённый004 (parked unknown plot7 сохранить отдельным
артефактом для расследования), normal close, единая установка source413–430,
reopen и пакетная проверка plot/funding/mining/personnel/UI. Других pipe owners нет.

## Source430 / frozen runtime408

Autonomy412/015: factory0x81ba279 adopted/native_factory_queue_observed/build0xcf15e,
plan construction2_401436.833 consumed8/8, очередь ждёт лицензию участка.
Plot5_401709.003 rejected_before_effect/plot_location_requires_reconciliation.
Причина: наш quote ошибочно запрещал GetBuildPlotPayment changed=true.
Stock menu_map.plotModeUpdatePrice4242–4257 и station_configuration3311–3326
считают текущую цену минус native credit независимо от этого флага.
Source construction_plot430 убирает только лишний pre-effect запрет; свежая
цена/credit, expected geometry/price, lifecycle и post-payment read-back остаются.
Fixture moved_new_station: quote100Cr→debit100Cr→PayBuildPlotSize→reconciled,
повтор без оплаты; construction_plot_fixture PASS. В игру430 не установлен,
collector80242 live;16 samples/4504s.3.4/6.3 и paid plot positive остаются открыты.

## Live429 / frozen runtime408

Autonomy412/014 подтвердил expansion1_393687.476:
observed/native_expansion_modules_observed в401393.008, station HQ0x4a6e4,
native build0x1cf6. План4/4 consumed; limit5000000Cr/spent512702Cr.
Перед этим012 storage resource_types0/budget0/wanted0/processing1: ресурсы
доставлены штатно после observed builder arrival398307.292 (fee50000Cr один раз).
Затем создание новой factory shell0x81ba279 в401406.798: bare_station_observed,
factory_shell_pending, build/plot покаnull. Это НЕ завершённая новая фабрика.
Collector80242 live;15 samples/4203s (~70min), age401425.19. Общая двухчасовая
и остальные доменные проверки остаются открыты; source428 ещё не установлен.

## Source428 / frozen runtime408

Исправлен starvation поиска NPC: общий HirePersonCursor ранее увеличивался
на16 при каждой станции. При двух станциях с32 NPC station1 всегда получала
offset0(mod32), station2 offset16(mod32); половина кандидатов каждой выпадала.
Теперь HirePersonPage продвигается на16 только при новом круге station index1.
Лимит16 NPC/одна станция за product вызов сохранён, таблица per-station не нужна.
Diagnostic427 также листает страницы NPC по полному кругу станций.
MD/XSD/scheduling и shared guard checks PASS (validate428), live ещё frozen408.
Найм/прибытие4.1/4.4 остаются открыты до фактической оплаченной транзакции.

## Diagnostic427 / Source425 / frozen runtime408

Добавлен source-only `probe.py hire_candidates`: существующие известные
неигровые станции с разрешённой стыковкой;16 станций/16 NPC на станцию за вызов,
вращающийся station cursor. Показывает реальный entityseed/HiringFee и ограничения
native hire actor/source/arrival, до32 строк с приоритетом пригодных кандидатов.
Отдельно публикует eligible/rejected в выборке и пределы; destination check ещё
не выполнен и отсутствие кандидата в выборке не означает отсутствие во вселенной.
Не вызывает assign_hired_actor, не платит, не создаёт NPC. Диагностические MD XSD,
Lua loadfile и Python syntax PASS; live команда ждёт следующей установки после412.
Collector80242 подтверждён live;010 age400225.989,11 samples/3003.6s.

## Preflight426 / Source425 / frozen runtime408

Единый повторный прогон после интеграции413–425:13/13 Lua fixtures PASS.
Результаты и хеши MD/UI/adapted sources сохранены в
`.cache/tmp/station-boundary-20261011/preflight426.json`; игровых эффектов нет.
Autonomy412/009: active age399926.385, expansion1 queued; builder1 observed,
storage budget/wanted321402Cr, processing1, claytronics137/stock0.
Collector80242 продолжает быть единственным pipe owner;10 samples/2704s.
Installed408 не изменён. Новые игровые критерии не закрыты по offline fixtures.

## Source425 / frozen runtime408

Подготовлены вместе413–425: financial facts/cents/reasons, native station mining
и operating budget, captain arrival guard423+diagnostic active/assigned pilot424,
previous periods425 с immutable employee name/seed и bounded4 rows в UI.
Последний MD/XSD/scheduling/генерация PASS, UI history fixture PASS; live ещё
не установлен. Collector80242 единственный pipe owner, installed408 сохраняется.
Текущие gates5.1/5.3/5.4/5.6/4.4/3.7 и общая приёмка открыты.

## Source420 / frozen runtime408

Source413–417: финансовые факты, mining needs, station budget, cents, revocation
и UI task.47-file dry-run PASS, installation не выполнялась.13 Lua fixtures
успешны:12 batch418 и supply419 после исправления обоих dofile путей.
Autonomy412/006 active age399026.449; purchase8 delivered/capacity25500 water,
builder1 observed, expansion1 queued. Collector80242 live;7 samples/1804s.
Новый packet live, military/personnel/causal gates ещё не приняты.

## Staged415: рабочий бюджет станции

Добавлен RequestStationFunding в единый EvaluateShortages, штатный productionmoney
порог90%, реальный player-to-station transfer с durable amount/paid/balances,
unknown без повтора, revocation и UI task. Lua fixture/UI registration/MD/XSD/AI
PASS, validate415.txt. Source-only: installed408 и collector80242 не менялись.
Следующий игровой пакет должен проверить вместе413/414/415;5.4 не закрыта.

## Staged414: mining потребность существующих станций

Source-only адаптация EvaluateShortages после native CheckRunningActions:
Upkeep mining gap -> commandeer/purchase штатные requests -> ActionReports.
До8 станций за цикл, pending/unknown coverage по requester/transport и старой
assignment claim, guards/receipt остаются штатными адаптерами. Генерация13,
check_adapted_manager, MD/XSD/AI/scheduling PASS (validate414.txt).
Frozen installed408 не менялся.413 financial receipt correction также staged.
Положительный mining read-back и бюджет operational станции ещё нужны;5.4 открыта.
Autonomy412/003 age398132.326: purchase7 delivered, builder1 sent, expansion1
queued; collector80242 live, samples4/903.0196345s.
## Autonomy412/001 и native кадровый тариф

Collector80242 live. Новый001-role age397533.236, economy_last_run397511.821
после396372.577; управляющий active. Расширение1 теперь queued/native_construction
in_progress; builder1 ещё sent/deployment pending. Progress подтвердил обе пары:
samples2/303.9008905s. MarketDeferred4/report null/index null, новый purchase7
397514.81 building: цикл завершился после порций и продолжил обычное приобретение.
Первичный тариф найма NPC_Instantiation2279–2282/Conversations222–226 совпадает
с RequestHire; docs/personnel-independent-vacancy-boundary дополнен контрактом.
Изменены только docs; frozen runtime сохранён. Кадровый live hire ещё не принят.

## Payment evidence audit / autonomy412 продолжается

Добавлен docs/plot-payment-boundary-20261011.md: точный native recipient путь,
разделение pre-effect6 и actual unknown7, недостаточность count0 журнала,
amount/paid/before-after контракт. Fixture усилен проверкой финансовых фактов
полной100 и частичной50 оплаты и оплаченной, но неподтверждённой лицензии; PASS.
Только test/doc edits: frozen installed packet не менялся. Collector80242
подтверждён live; latest000 role active/age397232.602, builder1 sent/deployment
pending, samples1. Положительная новая лицензия ещё не проверена;3.4 открыта.

## Quicksave role411 / autonomy412

Load410/session32812 terminal0: quicksave accepted. X4 PID5264. Role411 terminal0,
age397185.76: governor active, old expansion1_393687.476 queued, funding observed,
storage463702Cr/wanted463702Cr. Creation/plot/reservation null: независимая timeline
без unknown plot7. Crew unknown1 сохранён (no replay). Уже самостоятельно нанят
builder1_397163.919, fee/paid50000Cr, native deployment pending; это новая операция
в earlier timeline до прежнего найма2, не повтор заказа текущего save_004.
Installed пакет не менялся. Autonomy412 запущен120min/300s, PID5264, frozen
manifest+diagnostic SHA, session80242. Это единственный pipe owner; до stop.request+terminal
не выполнять другие probes/эффекты/install. Save_004/save407 остаётся parked
unknown7 timeline, пользовательский quicksave не изменяется. Приёмка открыта.

## Role409 / отдельная quicksave timeline

Load408/session74232 terminal0; role409/session35893 terminal0. PID6464.
plot_transactions key7 count0/read0/completetrue в issued-1..issued+10: отсутствие
записи не признано основанием повторить unknown платеж. Текущий save_004/save407
паркует эту timeline с unknown7, не очищается и не перезаписывается quicksave.
Load410 quicksave/session32812 остаётся единственным pipe owner. Выяснено
точное ограничение save_menu.lua:195–207 — arm/tick/startmenu-only. Для загрузки
через этот verified controller PID6464 штатно закрыт, Steam запущен повторно;
тот же клиент32812 ожидает новый startmenu. Не создавать второй клиент и не
считать ожидание ошибкой процесса. Source/installed пакет не изменялся.

## Packet408 / финансовый read-back

Save407 CRC/stability PASS compressed91826670/uncompressed748619427,
mtime1791739085.507598. PID17352 штатно закрыт,46-file packet установлен SHA-check:
native recipient conversion, actual payment/before-after, periodic recovery gate
без same-key payment intent, прежний unknown7 сохранён. Diagnostic Lua установлен
SHA70529627833EB78D74781ADBEACA0C705E309478242A1DCEFDD8F62843DC4FA6.
Единственный текущий pipe owner load408/session74232 ждёт меню; до terminal
не запускать другой probe. Далее role409 должен прочитать native transaction
log вокруг plot7 времени. Нулевого count недостаточно для очистки unknown.

Read-only quicksave inspection: присутствует operational control module0x4b78b
и construction module0x2197748, plan entries3/4. Quicksave не изменён; save_004
хранит текущую timeline с unknown7. Если платёж не удаётся однозначно сверить,
для независимой положительной пробы допустима загрузка whole earlier quicksave
по прежнему разрешению пользователя, без удаления receipt в текущей timeline.

## Role406: market завершился; diagnostic transaction log подготовлен

Role406 terminal0: active, native economy_last_run404753.373 (прежний403584.42),
age404807.07. MarketDeferred3/report null/sector_index null: штатный цикл
продолжился после трёх pending порций и закончил обработку. Новый обычный
purchase9_404755.175 building; дальнейшая работа не остановлена. Это один
подтверждённый цикл, не полная3.2/3.8/двухчасовая6.4 приёмка.

Primary Helper transaction log: struct107–125, API361/384, conversion money/100
10615–10637. SOURCE-ONLY diagnostic role добавлен bounded read player transaction
log key issued-1..issued+10, query cap256/rows64, completeness и pcall errors.
Не dispatch/не новый финансовый планировщик; отрицательный журнал сам по себе
не сбрасывает неизвестный платёж. Lua syntax PASS. Новая diagnostic Lua ещё
не установлена. Next coherent packet: ConvertStringTo64Bit recipient,
amount/actual paid/before-after, recovery scheduling и этот read-back. Старый
plot7 payment unknown сохранять без повторной оплаты. PID17352, pipe owner нет.

## Save405: настоящий payment unknown, НЕ повторять

Role404 age404648.304 показал новый key plot7/404591.173. Save405/plot-read405
session23463 terminal0: payment board40565 существует и state unknown;
request40568 reason plot_payment_unknown. Старое paid1800000 поле было
номинальной ценой, не доказанным расходом. Самостоятельно восстановление7
НЕ выполнять и receipt НЕ очищать. Native MapMenu4274–4275 преобразует
GetSectorControlStation через ConvertStringTo64Bit(tostring(controlstation));
наш вызов передавал сырой C-return, как прежняя ошибка owner-чтения.
SOURCE-ONLY вызов приведён к точному штатному; receipt amount=price/paid0,
moneybefore/after теперь записываются, paidprice устанавливается только после
exact balance delta. Plot fixture PASS; старый unknown7 не переотправляется.
Recovery scheduling из403 ещё SOURCE-ONLY. PID17352, pipe owner отсутствует.
Нужен независимый новый игровой сценарий либо доказательная сверка старого
платежа по штатному финансовому журналу; простого текущего баланса недостаточно.

## Role402 и recovery scheduling

Load401/session28811 terminal0, role402/session21067 terminal0; X4 PID17352.
Role402 age404586.124: same plot6 unknown/licence_failed, оплаты ещё не принято.
Найдена оставшаяся scheduling граница: periodic PlotRetry cue проверял unknown
только extend, хотя библиотека уже допускает точный неоплаченный quote rejection
новой станции. SOURCE-ONLY cue condition приведена к тому же узкому случаю:
same request key, licence_failed/quoted_plot_geometry_or_price_changed,
отсутствующий same-key payment receipt. Остальные library guards сохранены.
MD/XSD/scheduling PASS validate403.txt; новая cue condition не установлена.
Pipe owner нет. Market новый cycle ещё не наблюдён, last403584.42.

## Packet401: typed free и безопасное продолжение неоплаченной лицензии

ResumeUnpaidPlotLicence теперь допускает unknown новой станции только при
request licence_failed/quoted_plot_geometry_or_price_changed; этот конкретный
Lua return предшествует durable payment intent/native effects. Прежний same-key
payment receipt guard, governor/goal/build claim, ownership, сектор/позиция,
sequence/геометрия, бюджет и backoff сохраняются. Receipt/key не очищаются.
Numeric free0/1 нормализован с отказом любых иных значений; plot fixture PASS,
MD/XSD/scheduling PASS validate400.txt. Общий46-file пакет установлен SHA-check.
Save400 CRC/stability PASS compressed91607997/uncompressed747541852,
mtime1791738525.005772. PID8992 штатно завершён. Steam запуск -applaunch392160.
Текущий единственный pipe owner load401/session28811 ждёт меню; до terminal
не отправлять другой probe. Игровой результат новой recovery ещё не подтверждён.

## Save399: отказ лицензии до оплаты установлен

save399 requested save_004; plot-read399/session83794 terminal exit0, полный
gzip прочитан дважды. Request table188: key plot_6_404260.956, state licence_failed,
reason quoted_plot_geometry_or_price_changed (string refs14011/14009/14012).
Plot payment receipt board отсутствует. M.license возвращает этот reason до
создания payment intent и native effects. SOURCE-ONLY expected.free сравнение
теперь нормализует ровно bool/0/1; fixture MD round-trip free0 PASS. В игру
исправление ещё не установлено. Для старой unknown новой станции существующий
ResumeUnpaidPlotLicence разрешает unknown только extend; нужен узкий безопасный
путь для доказанного pre-effect quote rejection с сохранением same-key/no-payment,
governor/goal/ownership/geometry/build claim проверок. Не очищать receipt вручную.
X4 PID8992, pipe owner нет;3.4 остаётся открыта.

## Role398 / участок удерживается unknown

Load397/session72509 terminal exit0; role398/session83590 terminal exit0.
X4 PID8992 живой, governor active, age404381.212. Pipe owner отсутствует.
Owner boundary пройдена: Plot6/404260.956 достиг licence_failed вместо прежнего
owner-unavailable; product receipt unknown/native_plot_licence_not_confirmed.
НЕ повторять оплату/не очищать receipt. Нужен read-back request.reason и
tm_empire_plot_receipt/payment/key/state, чтобы отличить pre-effect rejection
от неизвестного платежа. Возможная следующая граница: expected.free приходит
MD numeric0/1, а M.license сравнивает с Lua bool quote.free без нормализации.
Это гипотеза до проверки raw reason; сохранять existing recovery guards.
Market_progress deferred/report/index пока null: новый native cycle ещё не
начался (last_run403584.42). Порционный алгоритм пока не квалифицирован.

## Packet397: owner + порционный native market установлены

Повторный source audit native EvaluateSectorShortage подтвердил, что pending
reset/return стоит до эффектов текущего ware и до increment TableRefIndex;
TM_EvaluatedPublicWares проверяется перед повторным анализом уже законченных
reportIndex/sector/ware. Generator регенерирован; full MD/XSD/AI/scheduling PASS
validate396.txt. Добавлен diagnostic market_progress (deferred/report/sector_index)
для живого подтверждения продолжения, не новый исполнитель решений.
Save396 CRC/stability PASS:compressed91525801/uncompressed747249746,
mtime1791738100.5134642. PID17840 штатно закрыт. Installed46 SHA-checked файлов
включают single-property stock owner и market continuation. Diagnostic MD
обновлён с SHA-check; diagnostic Lua остаётся636F89F9B1C5B60A97F673A9800A9FF2CFE00ADFAD36328649BF98792716D022.
Steam запуск только -applaunch392160. Текущий единственный pipe owner:
load397/session72509, ожидает меню; до terminal не запускать другой pipe probe.
3.2/3.4/3.8 остаются открыты до фактического игрового read-back.

## Packet394 / role395 и SOURCE-ONLY market continuation

Save393 CRC/stability PASS compressed91495963/uncompressed747453853,
mtime1791737756.2234325; PID49172 штатно закрыт. Полный46-file пакет установлен,
новый X4 PID17840. Load394/session57861 terminal exit0; role395 terminal exit0,
gameage404246.478. Pipe owner сейчас нет. Plot5/404200.928 всё ещё rejected
before effect/plot_sector_owner_unavailable. Diagnostic stock single-property
owner=teladi/string, context owner=nil, один sector ID304131. SOURCE-ONLY quote
теперь использует одиночный GetComponentData(sector,'owner'), точно как успешная
диагностика и MapMenu, вместо составного owner/isplayerowned. Free определяется
owner player/ownerless/xenon; fixture всех трёх free и paid/replay PASS.
Новый вариант ещё не установлен, неизвестный эффект/оплата не обходятся.

Generator SOURCE-ONLY: FillKnownSellOffers больше не прекращает всякий рынок
при числе соседних секторов>32. До512известных секторов в snapshot, не более8
новых sector/ware searches и128offers/search на один вызов; cache текущего
штатного анализа сохраняется между вызовами. pending возвращает управление
в существующий EvaluateSectorShortage через reset/return (его штатный delay
100–250ms). TM_EvaluatedPublicWares keyed reportIndex/sector/ware предотвращает
повтор уже обработанных решений при возврате к тому же сектору; обе таблицы
сбрасываются новым EvaluateShortages. Только public known docking offers,
штатный выбор решений не заменён. Неполные>128offer snapshots и>512секторов
сохраняют unknown-вход. Regeneration13scripts/check_adapted + full MD/XSD,
AI schema/scheduling PASS в validate-market395.txt; игровая приёмка отсутствует.
Следующий общий install должен включать одиночный owner и market continuation.

## Role392: причина nil-владельца доказана

Save390 gzip CRC/стабильность PASS:compressed91466397/uncompressed747079445,
mtime1791737414.2893362. PID17852 штатно закрыт; diagnostic Lua установлен
SHA636F89F9B1C5B60A97F673A9800A9FF2CFE00ADFAD36328649BF98792716D022.
Steam запуск нового PID49172; load391/session53690 terminal exit0.
Role392/session91191 terminal exit0, gameage404139.811. Сейчас pipe owner нет.
plot_context:context_sector304790ULL, stock_sectorID304790,
context_owner=nil/type nil, stock_owner=teladi/type string. Один ID сектора,
но native C-return representation не прочитана Lua GetComponentData напрямую;
штатный MapMenu путь sectorid→ConvertIDTo64Bit работает. Продукт quote/license
SOURCE-ONLY переведён на этот точный путь вместо C.GetContextByClass.
Plot fixture обновлён: sectorid отдельное свойство, C-context путь запрещён;
license/payment/geometry/newstation/replay PASS. Исправление ещё не установлено.
Product packet386 остаётся прежним; следующая проверка требует общего install
и штатного reload с текущим test save. Повтор прежнего unknown crew запрещён.

Отдельный аудит3.2/3.8: FillKnownSellOffers при NearbySectors.count>32 возвращает
false без порционного продолжения; cache TM_KnownMarketWares сбрасывается каждым
EvaluateShortages. Это возможный постоянный пропуск крупного известного рынка,
а не доказанное отсутствие предложений. Нужна bounded continuation в существующем
штатном EvaluateSectorShortage, без внешнего выбора стратегии/скрытых входов.

## После load386: участок, role388–389

Load386/session57863 terminal exit0, accepted save_004. Новый X4 PID17852,
start11.10.2026 19:44:27. Role388 и389 terminal exit0, сейчас pipe owner нет.
Role388: governor active, штатная экономика/receiver существуют, прежний
unknown crew transfer с тем же person/source/target сохранён без повтора.
Diagnostic construction_lua непосредственно подтвердил newconstruction1:number,
extend0:number. Role389/gameage404028.866: RequestPlotChange прошёл старую
ошибку лимита и готовности; request budget55508431Cr равен свежему балансу,
исходный лимит55514041Cr. Plot2/404020.795 rejected_before_effect:
plot_sector_owner_unavailable. Лицензия/ресурсы ещё не оплачены;3.4 открыта.

Подготовлена SOURCE-ONLY диагностическая строка plot_context: сравнение
C.GetContextByClass(station64,'sector',false) с штатным MapMenu путём
GetComponentData(station,'sectorid'), оба owner/value/type. Без эффектов,
pcall изоляция ошибок, Lua loadfile PASS. Ещё не установлена; не выводить причину
nil-owner из догадки и не обходить получение реального владельца/оплату.
Следующая адресная проверка этой неизвестной границы требует штатного save/close,
обновления diagnostic Lua и load; производственный пакет386 пока сохраняется.
OpenSpec apply387 ready,10/32; strict validate PASS, closure13/source copy PASS.

## Packet386: установлен общий пакет; загрузка тестового состояния

Autonomy380 остановлен запросом:8samples/2334.46s, session42670 terminal exit0.
Двухчасовая приёмка6.4 не закрыта. Save385 save_004: gzip полностью прочитан
до EOF/CRC, compressed91993913/uncompressed749511949, mtime1791737002.2551677,
размер/mtime неизменны до и после проверки. PID48480 штатно завершён.
Установлены46файлов общего source пакета с SHA-проверкой: cargo.all,
независимая кадровая вакансия, точность валютного delta, фактическое прерывание
поставки/external-mixed, лимит участка, numeric MD flags plot/funding,
русские причины ожидания. Эти изменения теперь installed, game qualification
ещё не выполнена. Обновлены diagnostic MD SHA710E2520D9CCDBB3DFD7F6DE72B3F846B5F035D9F3716764930BC12DC84E12B1
и Lua SHAC3A816294494A1895134D1C22E0155EEBAC7861E3084E3388AC3A60BF63FDAB7.
Lua read дополнен сырыми типами newconstruction/extend. Steam запуск только
-applaunch392160. Единственный текущий pipe owner: load386/session57863,
ожидает save-menu; до terminal не запускать другие pipe probes.

## SOURCE-ONLY: логические MD-флаги новой станции

Autonomy380/007: новый native economy cycle403584.42; station MPB-208,
build0x4b056, wanted3412243Cr. Plot receipt plot_1_403660.485 отклонена
до эффекта: plot_station_unavailable. Fixtures с MD newconstruction=1
воспроизвели ошибку и лицензии, и финансирования; прежние fixtures использовали
только Lua true. Обработчики принимают ровно true/1, остальные значения не
разрешают неоперативную станцию. Extend также понимает true/1; новая станция
с extend1 отклоняется. Fixtures PASS: numeric0/2 не разрешают оплату, replay
не списывает повторно, ограничения цены/денег/владения сохранены. Тестовый
IsSameComponent восстановлен в plot fixture (штатный API уже используется
production dispatch). В diagnostic role source добавлен construction_limit
с limit/spent/player Cr и nativecreation; новых эффектов в read нет.
Всё ещё SOURCE-ONLY, установленный packet373 и collector42670 не менялись.

## Autonomy380/005–006: строительство и новый участок

Расширение construction_1_393687.476 подтверждено в состоянии observed:
native_expansion_modules_observed, station0x4ac12, build0x1d60,
observed402970.047. StepQueuedExpansion проверяет каждую запись плана по
planmodule.id, точному macro и isoperational. Исходный запрос ExpansionFixture
передаёт macro.tm_empire_control_arg_macro; это обычное строительство модуля
с ресурсами и нанятым строителем. Результат не закрывает6.3 целиком:
назначение/смена сотрудника и остальные условия остаются обязательны.

Затем штатный экономический алгоритм сам создал пустую оболочку новой станции
0x21f227e; план construction_2_403137.993 проверен11/11 и поставлен в очередь
build0x4b056, creation=adopted/native_factory_queue_observed. Следующая граница
остановлена plot_licence_budget_missing. RequestPlotChange сравнивает прежний
общий остаток лимита с текущим балансом целиком, хотя это верхняя граница,
а не цена лицензии. SOURCE-ONLY: передаваемый лимит ограничен минимумом остатка
разрешённого бюджета и текущего player.money. Проверки цены quote против лимита
и свежего баланса перед оплатой сохранены. MD/XSD и scheduling PASS.
Изменение ещё не установлено; packet373 неизменен. Collector42670 продолжает,
samples7/1804.3727919s;3.4 и6.3 остаются открыты.

## Приёмка3.3 / managed delivery380/004

Пункт3.3 принят по docs/economic-assignment-acceptance-20261011.md; общий
прогресс10/32. Autonomy380/004:completed incoming water160, managed_incoming160,
last_managed_ship Тефида Агрессор/observed402738.453; supplier attribution
подтверждена native trade event + own claim. Шесть delivered actions двух wares
привязаны к шести различным кораблям/штатным приказам. Защиты Pending/financial
unknown/replay и уже принятые typed paid/save-load handoff сохраняются; покрытая
потребность не запускает безусловный повтор. Полный анализ3.2 и домены6.x открыты.
Collector42670 live, samples6/1502.5840542s, packet373 immutable, qualifiedfalse.

## SOURCE-ONLY: прерванная доставка / причины5.3

В generator native Upkeep добавлен bounded пример собственно прерванной доставки:
assigned trade subordinate/Flee/recent known enemy attack, station zero stock
native insufficient production ware, matching positive ship cargo, not playerhelm.
Без поиска новой сделки/dispatch: существующие32ship/8ware пределы, один пример.
Assets классифицирует external либо mixed при одновременной provision gap,
scope provision; общий ущерб выпуску явно не измерен, manager не обвиняется.
UI принимает external/mixed и отдельное delivery_interrupted условие (6conditions),
сохраняет неизвестное влияние обычного attack. Closure regeneration/check,
MD/XSD/scheduling и status fixture PASS; ещё не установлено/не принято в игре.
Новый source economy SHA отличается от предыдущего SOURCE-ONLY cargo.all SHA:
последний hash брать из regenerated docs/native-manager-adapted.json.
Полная5.3, manager_decision и blockade tests остаются открытыми.9/32.
Autonomy380/session42670 — единственный live pipeowner, samples5/1202.715041s;
installed packet373 immutable. Продолжать прогон/подготовку общего следующего пакета.

## Autonomy380/003 и финансовая граница UI

Сборщик42670 live, samples4/elapsed903.0672487s. Latest age402519.622,
economy_last_run402426.917 — новый штатный экономический цикл после load.
Builder observed/native_hired_builder_arrival_observed в402414.609, deployment
подтверждён reciprocal native state. Expansion ещё queued/in progress; новые
модули не приняты готовыми. Factory purpose production/producing1/resources0,
HQ purpose building; tradeprofit не используется как критерий стройки.
Finance375 сначала null (нет свежего периода);380/003 теперь реальные счета:
factory150000Cr/required135600Cr, HQ100000Cr/required0. Money bridge установлен
и runtime единицы подтвердились; не приписывать движения счёта прибыли.

SOURCE-ONLY UI: fixture выявил отклонение правильных cent-valued сумм
opening50000.01/closing49999.99/delta-0.02 из-за bit-exact Lua subtraction.
Validate допускает погрешность меньше половины native cent (0.005Cr), сохраняя
отказ для расхождения0.01Cr. Новый положительный сценарий сначала FAIL на прежнем
коде, после исправления PASS вместе с существующими отрицательными проверками.
Installed packet373 не менялся; добавить в следующий общий пакет с cargo.all и
independent vacancy guards.9/32, qualified_releasefalse.

## Приёмка6.2 / аудит381

Пункт6.2 принят; общий прогресс9/32, qualified_release=false. Документ:
docs/install-isolation-acceptance-20261011.md. install-boundary381:46 installed
files совпали, старого contentid topmanager нет, новый mod ровно один,74 affected
foreign overlays без изменений. Source-audit381:140 native sources/0mismatches/
0unresolved/4resolvedDLC; дополнительные3overlays принадлежат нашему модулю.
check_native_manager_copy PASS для13 исходных копий. Runtime380 active,
manager_exists1/goals1. Всё read-only, collector42670 не прерывался.
Принят только контракт изоляции установки, домены/2h/релиз остаются открытыми.

## Кадровая граница при активном autonomy380

SOURCE-ONLY: StepPersonnel больше не завершает весь поиск найма при unknown
переводе на другую target/post. На совпадающую должность ожидание сохранено;
RequestHire/RequestTransfer теперь взаимно удерживают pending назначения на
одинаковую target/post. Исходная transfer receipt не сбрасывается/не повторяется.
MD/XSD/scheduling и empire_status fixture PASS; игровые4.1/4.2/4.4 открыты.
Подробности/следующие проверки: personnel-independent-vacancy-boundary-20261011.md.
Seminar tiers сверены с primary Conversations934–991, совпадают, не изменены.
Прогон380/session42670 остаётся единственным pipeowner, latest samples2,
game401920.29; Expansion queued/native_construction_in_progress, builder sent.
Это назначенный строитель и очередь, фактическое deployed/готовность ещё не приняты.

## Source-проверка во время autonomy380

Сборщик42670 подтверждён live, samples1; installed packet373 не изменялся.
Найден несовместимый cargo lookup подчинённых в генераторе наблюдений станции:
containercargolist требует capacity.all/free.all. Исправлен adapt_native_manager.py,
staged closure пересобран (13 scripts), check_adapted_manager PASS. Dry-run полного
пакета46files PASS после запуска с доступом к Steam path. Исправление SOURCE-ONLY:
source economy SHA04C0B808983ECDD33D737C41614A85E3B1AED8A831DBC252197FB1EFF7511909,
installed economy SHA02D7698092CA1C65B8DA7141B38C3BE93F607DC65D59AD819409AAAD98939E75.
Новая проверенная граница/дальнейшие обязательства5.3:
docs/station-assessment-boundary-20261011.md. Чужой mobile_space_station_ru вызывает
homebase.type lookup на NPC станциях; его файлы не изменялись. Не считать эти
ошибки виной менеджеров TopManager без точного совпадения объекта/периода.

## Прогон374–380 — текущий

load373/session50735 терминально exit0, save_004 accepted. Игра PID48480.
role374/session67513 терминально exit0; Registry active, governor1, отдельные
station managers сохранены. После load assessments пока null из-за нового
ObservationSession; это ожидаемое отсутствие свежего периода, не нулевой результат.
provision375: request recovery_approved, штатные cargo/offer читаются.
Save376 — текущий save_004, запрос подтверждён. builder-read377 два прохода
gzip доEOF: исходные before61616987/after61566987/fee50000/paid50000 сохранены;
строковые ref157711=$destination_version со значением2 и ref157713=
$recovery_attempted со значением1. Отдельная проверка stablemtime пока не выполнена.
builder-order379 использует исправленный parser self-closing components:
YKC-004 теперь runtimeid0x11f59, DeployToStation0x872c started, station0x4ac12
(тот же HQ после ремапа IDs при загрузке). No second payment.
role378 age401550.237: construction_supply.builder0x11f59,resource_types0;
Expansion queued/native_construction_in_progress. Builder arrival ещё sent:
назначение не равно фактическому deployed и готовому модулю.3.4 остаётся открыта.

Текущий единственный pipeowner autonomy380/session42670: minutes120/interval300,
PID48480, immutable packet373 (46 files + diagnostic hashes выше), первый
sample age401620.607, samples1. Перед новыми pipe-командами stop.request и
терминальное завершение42670. Не менять installed files во время прогона.
Strict OpenSpec validate PASS в этом прогоне;8/32/qualified_releasefalse.
После очередного штатного economic cycle проверять реальные UI суммы и managed
station trade quantities, завершение строительства, кадровые события и военные
решения. До принятия обязательных доменов длительность не закрывает6.4.

## Пакет372–373 — текущий

Autonomy369 терминально stopped_by_request:3 samples/612.9032241s, session68345
завершена. Нельзя считать его текущим pipeowner. Save372 проверен CRC доEOF и
стабильностью: compressed95436765/uncompressed766841243,
mtime1791734243.7751062; текущий save_004. X4 PID24388 штатно завершён.
Установлен общий пакет373:46files с проверкой SHA. Включает исправленный адресат
NPC builder, guarded однократную миграцию оплаченного legacy deployment без
новой оплаты, UI receipts/статусы, managed station trade attribution и Money→Lua
без повторного деления. MD/XSD/scheduling, builder fixture и status fixture PASS.
Diagnostic MD также установлен, SHA
9986E51BDB416C3554BBF7A6A3AE0D1D73E82EA9AC3FD628EDE9C2A6DA340462.
Diagnostic Lua прежний B81A62244447B505ED5079D1BBFEAAB83FDBE97C7DFC429B13F2AE0B6A3F8B29.
Steam запущен только -applaunch392160. Текущий единственный pipeowner load373,
session50735; до терминального выхода не запускать второй запрос. Далее role/
provision и debuglog: отсутствие MD errors, восстановленный DeployToStation,
однократная исходная оплата50000Cr, прибытие/строительство, корректные UI суммы
и новый station managed flow. qualified_release=false,8/32.

## Прогон369–371 — текущий

Игра PID24388, установлен неизменный packet357 (46 files), qualified_release=false.
Единственный владелец pipes: autonomy369, session68345, interval300/minutes85;
перед новыми командами stop.request и дождаться терминального выхода сборщика.
Autonomy363 завершён stopped_by_request (3 samples/707.59s), autonomy366 также
завершён (6 samples/1779.99s). Время само по себе не закрывает приёмку6.4.
Save368 — текущий save_004: compressed95153143/uncompressed765855038,
mtime1791733576.668935, CRC доEOF и стабильность проверены; quicksave не тронут.
Autonomy369/001: delivery367 trade0x8a72c,126water, delivery_observed400859.611.
Purchase361 отдельно purchase_observed; баланс меняется параллельно другими
действиями. Фабрика производит воду, но общий station flow не доказывает
принадлежность поставщика управляющему. Managed attribution подготовлен только
в source. В construction_supply теперь resource_types0/budget0/wanted0,
processing1, buildernull: нехватка материалов больше не объясняет ожидание.

Builder-read370 из Save368 доказывает единственную оплату50000Cr:
before61616987/after61566987, key builder_hire_2_398142.008, ship0x130f2 YKC-004.
Builder-order371: у корабля только default FindBuildTasks, DeployToStation отсутствует.
Parents этого одноразового парсера ненадёжны (self-closing components), не использовать
их для утверждения сектора. Первопричина в source подтверждена штатными
menu_map.lua:3511 и order.build.deploy.xml: параметр station должен содержать
станцию0x4c09e, адаптер передавал storage0x4bff7. Source исправлен, fixture теперь
проверяет точный destination==station; run_lua_fixture PASS. Не установлено.
Повторно оплачивать нельзя. Следующая работа: guarded восстановление именно
этого оплаченного ошибочного deployment без повторного списания подготовлено
в source (RecoverLegacyHiredBuilder/M.recover). Оно одноразовое, требует полной
оплаты/совпадения квитанции и действующей задачи; не отменяет приказы. Новые
приказы destination_version2 исключены из миграции. Fixture негативных условий/
повтора/неудачи и MD/XSD/scheduling PASS. Далее единый пакет source UI/managed
trade attribution/money bridge и восстановление/приёмка после текущего прогона.

Также source-only: builder error normalization, receipt/status UI, raw Money→Lua
без повторного /1Cr, diagnostic quantities, README, summarize_autonomy.py.
Принято8/32; строительное прибытие/crew intransit и прочие критерии открыты.

## Прогон358–363 — текущий

load357 accepted,PID24388. Packet46files все SHA verified, qualified_releasefalse. diagnosticMD DF0C271A70EAEC48B5CFD01D894921B81F095D6DD8285E3297ECD42AD59BC724; diagnosticLua B81A62244447B505ED5079D1BBFEAAB83FDBE97C7DFC429B13F2AE0B6A3F8B29. role362: builder_hire_2_398142.008, штатный fee50000Cr, paid50000Cr, Lua sent/native_hired_builder_deployment_pending; MDsent, фактическое прибытие ещё не принято. Старый key1 не имел подтверждённой оплаты, замена не доказывает повторное списание. Tradecandidate360 найден APU544/RPW225/water/KMT485@32Cr; trade361 issued398162.7,126units (4032Cr), trade0x8cd0, unknown. Повтор НЕ запускать до native completion. Autonomy363 read-only120min/interval300 запущен, session59557, PID24388; samples1, единственный pipeowner. Для новых команд сначала stop.request и терминальное завершение сборщика. Прогресс8/32, приёмка3.4/4.2/6.x открыта. Source crewexchange aisle deprecated3.30, не использовать для восстановления; штатный modern pod max travel5min + launch15s, текущее долгое intransit не объясняется штатным ETA.

## Исправление352–357

role352 показал сохранённую builder request check_requested, userdata компонентов, number budget и отсутствие Lua результата. Save/table353–356 доказали ошибку типов: budget после /1Cr сохранился type=money value4537298, то есть Lua получил45372.98Cr и silently reject integer. Source передаёт исходную Money сумму как в Funding, BuilderWatch восстанавливает только same-key check_requested с отсутствующим результатом; бюджет может содержать доли кредита, fee остаётся целым. Все дешёвые проверки прошли; пакет357 установлен46files, load357 выполняется. Оплата пока не подтверждена, task3.4 не закрыта.

## Прогон345–351

load344 accepted,role345/349 terminal,PID16152. Builder quote pending key builder_hire_1_397946.788; обнаружена MD ошибка relation.friend (неподдерживаемая константа), оплата/приказ не подтверждены. Исправлено на штатное hasrelation.friend, добавлен read-back сохранённого Lua результата в BuilderWatch и диагностический builder_lua. MD/XSD/scheduling и builderfixture повторно passed. Пакет350–351 установлен46files, diagnosticLua обновлён; load351 ожидается. Save350 CRC/stability: compressed93765302/uncompressed758872853,mtime1791730325.0355883. В role349 реальный строительный wanted/budget327430Cr, resource_types2 (ранее3): штатные поставки идут. Trading346/347 обе ограниченные группы проверены. В347 purchase_candidate APU544/RPW225/water/KMT485@32Cr найден; первая строка none относится к доставке текущего груза. Приказ не выдан, кандидат истёк. provision348: water0, buy2027@74Cr и RPW225 sell39550@32Cr — нельзя объяснять отсутствие сделки отсутствием поставщика. Crew тот же unknown/intransit, не принят.

## Пакет341–344

Найм штатного NPC строителя установлен полным пакетом46files. Использует native fee/payment/DeployToStation, не удаляет чужие приказы. Durable unknown перед оплатой, paid receipt перед созданием приказа; повторы запрещены. Luafixture и MD/XSD/scheduling passed. Save343: gzip CRC и стабильность проверены, compressed93732767/uncompressed758175843. Исправление IssueTradeFixture purpose установлено в tm_empire_diagnostics, MD SHA DF0C271A70EAEC48B5CFD01D894921B81F095D6DD8285E3297ECD42AD59BC724. load344 запущен, итог ещё не прочитан. Прогресс8/32, игровые критерии не закрыты.

## Прогон337–340

load336 завершён,session31383 terminal; игра PID44436 Respondingtrue.
batch337 terminal. Новые diagnostic MD поля работали без TM lookup errors:
crew_actor null/exists0, тот же person9873631311134785487 на цели,intransit1,
source0/target1,transferunknown. Это не физическое прибытие.
Строительный бюджет463702Cr равен wanted463702Cr; fundingobserved,
Expansionqueued/owned_builder_unavailable; нужны claytronics137/energycells274/
hullparts501,stock0. Обычная NPC hiring граница исследована в отдельном
native-builder-hire-boundary-20261011.md; пока не реализована.
provision338: фабрикаenergycells1485,water0; RPW225 известная water sell39566@32Cr.
trade_candidate339: AP U544 (id APU-544),water,KMT485,order_calledfalse.
trade340: библиотека НЕ исполнялась из-за отсутствия purpose=run_actions;
результатnil, ошибка в debuglog397230.67. Команда не повторялась.
Source исправлен; checker теперь ловит вызванные библиотеки без purpose и
библиотеки с return без run_actions. Регрессионные5 tests и MD/XSD/scheduling
passed. Исправление purpose НЕ установлено; installed MD SHA ниже прежний.
collect_autonomy.py создан как конечный read-only сборщик, импорт probe
исправлен после прерывания, но сборщик ещё НЕ запускался/не квалифицирован.

## Последний пакет335–336: диагностика установлена

После пользовательской церемонии blueprint332:observed/ownedtrue,
1007844Cr paid,before64437819/after63429975Cr. role334/game397077.961:
construction_1_393687.476 consumed,total4/checked4; Expansion queued,
build0xc9d2,reasonnative_expansion_resources_pending. Это обычная очередь,
не готовый модуль. План и сотрудник не создавались повторно.

Save335 подтверждён gzip CRC доEOF и стабильным размером:mtime1791728890.9212608,
bytes93480728,uncompressed756369471,game397141.065,money62965473Cr.
Это актуальный save004; прежние Save202/323 ниже исторические.
Новый диагностический MD установлен, SHA:
522B6F51E35785C0697BFBB261C8B3D200E4E36AB768902CB0D59A38BCB39FC7.
Включает cargo.capacity.all, crew_actor/assignment-event, generalized resource
trade fixture≤5000Cr и construction_supply/resources. Product45files прежний,
qualified_release=false. MD/XSD/scheduling passed перед копированием;
runtime этих новых полей ещё не принят. Игра перезапущена через Steam,
load336/session31383 ожидает соединения; не запускать второй pipe-клиент,
пока этот запрос не завершился. Принято8/32, goalactive.

## Актуализация: пакет323–325

Установлен общий пакет:45 файлов проверены по installed-manifest, несовпадений0,
qualified_release=false. UI видимость вкладки теперь читает schema/has_governor
независимо от валидности остальных строк отчёта. Неверная строка не скрывает
кнопку: страница сообщает о недоступности снимка. Fixture passed; это исправление
подтверждённой уязвимости кода, не доказательство причины пользовательского случая.
module320 подтвердил существующий HQ XZS342/module0x4b6ae без создания дубля;
role321 — действующий управляющий; ui322 — открытая страница129 строк.

В пакет вошли подготовленные assets/UI309: наблюдаемые ограничения закупок
дефицитных товаров отдельным условием trade_rules, без обвинения менеджера.
Диагностика314–318 читает текущие ресурсы/известные офферы, штатную цель и
скорректированный score покупки, флаги точного переводимого сотрудника;
фильтры trade fixtures учитывают tradesknownto и actual ship tradepartner.
Установленный diagnostic MD SHA:
F17B48E73C6928BAC819B153EB3755149955C48FB12FF72039F0E8E5C8D90E88.
MD/XSD/scheduling и Lua syntax прошли. Новые игровые поля пока не приняты.

Штатный Save323 подтвердился файлом save_004.xml.gz:mtime1791727985.7517788,
bytes93254187,game396504.236,money64456119Cr,GUID прежний.
Это актуальный тестовый checkpoint с финансированием фабрики и новыми кораблями;
описание Save202 ниже является историей. Запрос load324/session98502 ещё ожидается;
его таймаут наблюдения не означает завершение процесса.

load324 завершился:save_004 принят. Игра PID33216, batch326/session21444
завершился; UI328 открыта21 строка сразу после load, пока новый bounded
снимок ещё собирался. Диагностический crew_transfer326:точный person9873631311134785487,
source_member0,target_member1,intransit1,scheduled0,podarrivalnull,temporary1,
stateunknown/native_crew_arrival_not_observed. Это НЕ прибытие; перевод не повторён.
current_supply327:KMT485 cargo0 обоих ресурсов,owner_only0,buy energycells656@22Cr,
water1743@74Cr,known_sector_sell_found0 для обоих. Это только известные офферы
в текущем секторе, не доказательство отсутствия поставщиков во всей галактике.
Нативные economic_action score106963→90473→74595→58698 учитывают ранее
заказанные корабли; одинаковый товар сам по себе не доказывает дублирование.
Диагностическое поле Ship.cargo.capacity вызвало lookup errors в326;
источник исправлен на штатное cargo.capacity.all (scriptproperties2028,
story_buccaneers205), XSD/scheduling passed. Исправление ещё НЕ установлено,
новая игровая проба read326 поэтому остаётся частичной. Продуктовых MD ошибок
в проверенном контексте не обнаружено. Не перезапускать игру ради этого поля:
пользователь согласился пройти обычную церемонию Аргонской Федерации.

batch329 завершился без новых эффектов. ui330:93 строки, frame1456, страница
tm_empire_status после load собирает данные. current_supply329/game396602.438:
water buy1831@74Cr и известный sell39307@32Cr на RPW225 появились;
energycells buy_found0/known_sell0,cargo0. Офферы изменяются: отрицательная
проба327 не используется как постоянная причина отсутствия снабжения.
Периодические station observations после load пока ждут новый economy cycle;
null не заменён нулями. Все pipe-запросы завершены, игра PID33216 оставлена
пользователю для обычной церемонии, контрольный save004 остаётся Save323.

personnel316: один обычный bulk-перевод GYU115→MZK812, тот же template;
role317 подтвердил изменение membership, но не прибытие. Не повторять назначение.
blueprint319: station_gen_advanced отсутствует, ceremonyally отсутствует,
relation21/min20,payment_called=false. Нужна обычная церемония повышения.
Автономный economy cycle395269.666 и реальные перемещения Recon подтверждены,
но все обязательные домены и2h ещё не приняты. Прогресс остаётся8/32.

crew-save331 — read-only потоковый разбор Save323:одна people-запись точного
seed9873631311134785487,service,intransit|temporary; без изменения файла.
Stock bulk/order.trade.crewexchange и Conversations.LaunchCrewTransferPod
не считаются взаимозаменяемыми recovery путями без наблюдения фактического этапа.
HandleVanillaPilotAssignment стороннего galaxy_trader присутствует в save с этим
seed, но это не доказательство причины зависания. Packed/extracted gt_core_system
SHA совпал:7b7f15d5f46e1ecfb5dfaaa4dbf73064d9b900f38dc17a62140299cfd4bc799c.
Чужой мод не менялся. Source диагностического MD дополнен read-only crew_actor
и одной последней CrewAssignmentEvent точного человека/квитанции.
Listener ничего не назначает, не сигналит native cue, не меняет флаги NPC;
отсутствие события до установки не трактуется как отсутствие штатного dispatch.
Вместе с cargo.capacity.all это PENDING_SOURCE, не установлено и не принято
в игре. XML/XSD/scheduling passed. Перевод316 повторно не отправлялся.

Дополнение source332: TradeCandidate ищет реальные ресурсы станции, а не
только energycells. Ограничения64ship/16station/16resource сохранены;
известные офферы, реальная цена, cargo capacity и цель проверяются перед
эффектом. TradeFixture выбирает до1024 единиц, общий purchase cost≤5000Cr
и≤player.money, delivery≤фактически купленного/имеющегося количества.
MD integer cast следует stock diplomacy2193/CPUShipManager943; бюджет
дополнительно проверяется после вычисления количества. Source/target pending
crew transfer исключены из этой тестовой пробы. Unknown replay удерживается.
Это НЕ продуктовый дополнительный планировщик и НЕ исполненная торговля:
изменения только в тестовом MD, ещё не установлены. XSD/scheduling passed.

blueprint332 завершился: штатная покупка чертежа observed/ownedtrue,
price1007844Cr,before64437819Cr,after63429975Cr. Лицензионная предпосылка
снята реальной пользовательской церемонией; не заменялась прямым AddLicence.
Игра PID33216 Respondingtrue. Строительная цепочка пока не принята.

## Предыдущая контрольная точка294–306

Актуальное состояние после пакета294 и прогонов295–306:
продукт установлен,45 файлов совпадают с installed-manifest; qualified_release=false.
Исследовательский модуль HQ больше не входит в товарное производство:
provision281 подтвердил XZS342 purposeother/total0 и KMT485 production/total1.
Условия периода включают наблюдаемый owner-only флаг отдельных товаров;
это не полный отпечаток всех фракционных правил и чёрных списков.

Диагностика снабжения установлена: MD SHA
2628BBEAFE56BEF2003CD4AD4DC641246136B1CEFB0B1EC37C979AD8BC8B2D62,
Lua SHA F5C954E2DD68DC22535D40A15728647F88F8D1FE5E157DDBAAF0C92AA41DA5BB.
KMT485 выращивает солнечные цветы; вода и энергоэлементы — ресурсы,
не продукты этой фабрики. Неудачная проба290 остановилась до эффектов
из-за неверной диагностической проверки товара; проверка исправлена.
Проба299 подтвердила обычное разрешение закупок ресурсов и перевод
50000Cr от faction.player на фабрику:100000→150000Cr; деньги игрока
уменьшились ровно на50000Cr. Сырые MD monetary значения в receipt299
выражены в сотых долях Cr. Повтор303 вернул previous_attempt/observed.

provision298→301: период фабрики393732.144→393738.236,samples1,
бюджет150000Cr; неизменная HQ сохранила from393732.144,samples2.
Общий trade_restricted фабрики также изменился1→0, поэтому этот прогон
не доказывает отдельно изменение только товарного правила при неизменном
общем флаге. Обе штатные диагностические analysis-команды не считаются
доказательством автономного запуска. До provision305 реальная поставка
и finished→started пары не подтверждены; финансы нового периодаdelta0
корректно не выдают перевод через границу условий за прибыль.

ui306 — действующая страница,125 строк. role304 — Registryactive,
Manager/economy/factoryreceiver существуют, age393832.262,
economylastrun393738.236. Игра PID2196 остаётся запущенной для обычной
доставки и производственных событий; pipe-команды завершены.
Сохранения не перезаписаны. Принято8/32; строительство, полноценная
причинность, кадровые/военные игровые эффекты,2h и выпуск остаются открыты.

## История прежних контрольных точек

Ниже сохранены прежние состояния; версии, PID и ограничения runtime
в них не относятся к текущему пакету.

Checkpoint231 sourceprogress: диагностический поиск теперь готовит также
реальную закупку energycells, если найден idle/unclaimed/uncommanded ownship
с подходящим cargo.free и ownoperationalstation с resources.energycells и
реальным find_buy_offer. find_sell_offer штатный, tradepartner=Ship,
space=DestinationStation.sector; foreignseller должен быть известен игроку,
offer.amount>0/unitprice>=0/player.money>=1unitprice. Никакие цены/офферы/
товары не создаются. Сохраняется один exactPurchaseCandidate и очищается
при новом запросе. Это READONLY подготовка, не выполненная закупка.
Nativecommon.xsd28283/find_sell_offer и stocktrade.find.free289 подтверждают
маршрут. Cargo.list/nativeLIB_Generic467, unitprice/nativeNotifications
подтверждены. Пагинация+закупочныйпоиск sourceНЕустановлены; validation231
до финальной очистки/onecandidateguard прошла. Передустановкой повторить
cheapvalidation. Для tradeeffect недостаёт полного исполнителя/receipt/
actualevent и готового read-back. НЕ считать этот source полностью готовой
торговойпробой. Live PID4252,pipeownerнет,пакет229;8/32goalactive.

Checkpoint229: диагностический поиск установлен (product45files224unchanged),
MD SHA4F7E88F341FB1B32300B198ECF6080948977B418C2BDC6EFDA3A55464071AA02.
Передустановкой добавлены hasorderloop/commander/override/priority/claim
исключения и removeстарогокандидата. MD/XSD/scheduling passed.
Load228/session36912 terminal/save004; Trade229/session64693 terminal:
none_in_bounded_scan,ships67/stations2, ownMD/parsererrorsнет. Это только
первые64ship,не доказательство отсутствиякандидата во всейимперии.
Source дополнен пагинацией64ship/cursor/from/to; по следующему запросу
дочитывает остаток, затем начинаетновыйцикл. Пагинация покаНЕустановлена.
ТекущийPID4252,pipeownerнет,заказынесоздавались. Следующийобщийпакет:
установитьпагинацию, дочитатьвсювладельческуюопись; приотсутствиисвободного
гружёногосудна подготовить обычную оплачиваемую закупку нужноготовара на
доступном idle судне или ждать управляемое завершение его штатнойзадачи,
не отменять ручные/чужие/unknown приказы и не выдаватьcargo бесплатно.
Факт tradecompleted и fullchangeещёнепринят;8/32goalactive.

Checkpoint225: подготовлена READ-ONLY диагностическая TradeCandidate команда.
Она ищет реальный find_buy_offer ownstation для существующего груза idle
ownship, operational/pilot/неplayerhelm/нетorders, bounded64ships×16wares×
16stations. Сохраняет exactship/station/ware/offer/age, возвращает цену/объём;
не создаёт товары/офферы/заказы. NativeLIB_Generic467 подтверждает cargo.list;
common.xsd24057 create_trade_order обычный путь: deal+queuedAIorder, неinstant
transfer. Следующий шаг: подключитьmode вprobe.py, установить диагностику
в следующемпакете и получить livecandidate; прямо перед реальнымtradeorder
повторить всеownership/helm/manual/cargo/offer/budgetguards, записатьunknown
доэффекта и ждать nativecompleted event. Не вызывать RecordStationTrade
искусственно и не засчитывать только create_trade_order как завершение.
MD/XSD/scheduling+diagnosticLua syntax прошли до cargo.list исправления;
source ещёНЕустановлен. Live PID13432/45productfiles224,pipeownerнет,8/32.

Checkpoint224: установлен единый пакет218–219 (45productfiles), diagnostic
MD содержит station_trade_value/station_external. XML/XSD/scheduling и
расширенный UI fixture перед установкой прошли. Штатный close/restart.
Load221/session31985 terminalaccepted save004. PID13432. Analysis222/
session48297 terminalrequested. Provision223 terminal: freshfinance обеих
станций from/to393730.1/samples1/opening=closing100000,required135600/0.
Свежих ownMD/parser errors нет. Trade/external событий в этом периоде
нет в read-back; это НЕ положительная квалификация coverage/сумм/атак.
Ui224 статус открыт, OpenSpec strict passed. Pipeownerнет, новых saveнет.
Следующий шаг: реальная штатная доставка товаров на ownstation (без создания
фиктивного tradeoffer/вызова RecordStationTrade как будто событие), затем
сверить buyer/seller и unitprice*transferredamount. Наблюдение реальной атаки
также необходимо для positive external gate, не заменять временем вручную.
Полные5.1/causal5.3/feedback5.4 и релиз остаются open8/32.

Checkpoint219: согласованный source-пакет расширен внешними наблюдениями.
Скопированный штатный Economy сохраняет last_attack=Object.lastattacktime
и имя lastattacker только если exists+isknown. Штатный factionlogic.xml874/
1251 сравнивает lastattacktime с player.age; единицы подтверждены источником.
ReadStationEvidence выдаёт external только при from<=attack<=observed,
строго в уже проверенном employee/session/manager периоде. UI показывает
факт атаки/неизвестного нападавшего без вывода о блокаде, ущербе или виновности.
Finance218 sums contract расширенного UI fixture теперь покрывает positive,
partial financial_complete=false, missing/negative values. External contract
покрывает неизвестного нападавшего, старый период, будущее и известное имя.
Fixture прошёл;13 adaptedscripts regenerated; XML/XSD/scheduling прошли.
Это часть5.1, не закрытие причинных5.3/5.4. Пакет218+219 НЕустановлен:
PID41608 пока financial217,pipeownerнет. Следующий пакетныйinstall/restart
нужен для реального completedtrade/attack read-back. Не повторять штатные
внутренние AI tests; проверить изменённую границу, обе стороны сделки,
самопокупку/частичный перевод, employee/session/period isolation.
Цель активна;8/32accepted,не общийblocked и не releasequalified.

Checkpoint218 (source progress, без перезапуска ради одной границы): штатный
notifications.xml2741 PlayerFactionTradeCompleted использует тот же
event_player_trade_completed для seller.owner=player и buyer.owner!=player,
рассчитывает сумму unitprice*transferredamount. Это подтверждает маршрут
фракционных сделок, но не является полной игровой проверкой coverage.
В RecordStationTrade добавлены фактические incoming_value/outgoing_value;
они инициализируются только у нового пустого журнала. Старый журнал с уже
накопленными количествами не получает выдуманные нулевые суммы. При отсутствии
цены financial_complete=false; UI маркирует суммы как частичные. Количества
и суммы проверяются независимо, внутренние сделки явно не названы прибылью.
Проекция и UI поддерживают новые поля. XSD/scheduling и существующий UI
fixture прошли; новый контракт сумм ещё требует отдельного negative fixture
и реальной completedtrade read-back (не оффер/оплата корабля).
Изменения tm_empire_assets.xml/ui/empire_status.lua пока НЕ установлены;
PID41608 использует квалифицированный финансовый пакет217. Pipeownerнет.
Установить вместе со следующим согласованным пакетом, затем общий прогон.
Задачи5.1/5.2/5.3 и полный ченж всё ещё открыты8/32, release не принят.

Актуальный checkpoint217 — добавлена и проверена финансовая история.
Предыдущий и текущий goal turns: progress. Ченж остаётся 8/32; задача5.1
целиком не принята (внешние условия/использование подчинённых ещё неполны).
ReadFinanceSamples в tm_empire_assets использует текущий штатный отчёт +
до15 предыдущих, строго station/employee/manager/session/period и не позже
текущего observed. Счёт отсутствует => finance=null, не нулевой баланс.
Проекция содержит from/to/samples/period_samples/opening/closing/required/delta.
UI различает движение средств и прибыль. Нового опросчика/планировщика нет.
Расширенный существующий UI fixture прошёл: отрицательная delta, чужой период,
rollback/future, missing balance, противоречивые поля, односнимочный период.
XSD/scheduling прошли. Установлены45productfiles + diagnostic MD с
station_finance в provision_read. Load211/session17064 terminal save004;
Role212/session85335 terminal active/sameconstructionkey.
Analysis213 штатный путь для проверки новых наблюдений после загрузки,
Provision214: KMT485 и XZS342 по100000Cr, новый from393754.071/samples1,
required135600/0 соответственно. Analysis215+Provision216: тотжеfrom,
to393806.181/samples2/period_samples2/opening=closing100000/delta0.
Никакого выдуманного финансового потока; положительный/отрицательный реальный
delta ещё не проверен, отрицательный контракт покрыт Lua fixture.
Ui217 настоящий статус открыт,122строки/2таблицы/projectiontrue,
актуальный snapshot393802.827–393812.833. Свежих собственных MD/parsererrors нет.
В процессе nativeanalysis продолжились обычные покупки кораблей: assetcount70,
paid38056ULL1111768Cr/bank68852220; это не новый критерий полной экономики.
Текущий PID41608, pipeowner отсутствует. Новых сохранений после202 не писали.
Следующие независимые области: полная trade-event coverage, внешние условия,
causal rules и обратная связь штатномуAI; personnel arrival/hire/military.
Строительный план всё ещё ждёт advanced licence/чертёж; не повторять генерацию.

Checkpoint208 актуальный: Load20677899 terminal/save004,PID12880.
Blueprint207 terminal: stockmenu работает, цена1007844Cr, условиянепройдены,
paymentневызывался. Role208 samekeyconstruction_1_393687.476,waitingblueprints,
missing толькоtm_module_empire_control_arg; никакойновойгенерации/заказа.
Parser @property? errors и ownMDerrors в свежемжурнале отсутствуют.
Точнаяпредпосылка подтверждена из save004(player faction ONLY): лицензии
generaluseequipment/generaluseship/station_gen_basic/station_illegal/envoy_access;
station_gen_advanced отсутствует. Productware требует station_gen_advanced,
каквштатномadminмодуле. Проверены playerfaction licenses вautosave01/02/03,
quicksave,save008: ниодиннеимеетadvanced. Первоначальный firstlicencesprefix
попадалвNPCfreesplit; исправленнаяпроверка ограниченаidplayer, не смешивать.
Положительнаяпроба покупки/строительства наэтихсейвах пока недоказана;
невыдавать скрытолицензии/репутацию/чертежи и неослаблять productrestriction
радипрохождения. Это локальная тестоваяпредпосылка,не общийblocked: можно
продолжатьfinance/history/cause/personnel/military и общийпакет.
Диагностикеполезно далее ответить licence/haslicence/money/totalprice явно.
Штатныйменю-магазиннайден examples/x4_lua/.../menu_trader_blueprintsorlicences.lua:
buttonSelectBlueprint655/Confirm595,LearnBlueprint+TransferPlayerMoneyTo,
GetNumBlueprints/GetBlueprints readback. Все submissionunknown защищены отповтора.
Новых saveпосле207неписали,004 по-прежнему202 waitingplan, оригиналы untouched.
Pipeownerнет. Установлены45 coherentfiles+исправленнаядиагностика;8/32accepted.

Актуальный checkpoint206: progress,8/32,не blocker. Load19896367 terminal,
Role199 terminal. Expansion200 один запуск; Role201 доказал null-loadout
исправление: собственных MDerrors нет, успешный nativeevent/count4,
keyconstruction_1_393687.476, waiting_blueprints, missing только
tm_module_empire_control_arg. Сохранение202 ONLYsave004 реально записано:
1791718762.88455/91682814bytes/header393729.956/build611726/bank71168097,
тотжеGUID C45BAA91-B465-4CF8-B9F7-3B8AF5303AC3. Это текущий пригодный
checkpoint ожидания; старое описание004как167/173 больше не актуально.
Load20310966terminal/save004; Role20449563terminal тотжеkey/event/manageractive.
План восстановлен без повторной генерации. Blueprint2053463terminal timeout;
точнаяLuaerror Helper onUpdate compare nilnumber: новая диагностическая
callback не передала третье время. Она не исполнилась/штатная покупка не
вызвана; sourcefix false,getElapsedTime()+.2. Не утверждать покупку принятой.
Новая probe.py modeblueprint/MD BlueprintFixture использует существующего
argon.representative только известной станции, Lua открывает штатный
BlueprintOrLicenceTraderMenu, сверяет warehouse price/licence/money,
записывает unknown до stockbuttonSelectBlueprint/buttonConfirm один раз,
проверяет GetBlueprints+moneydelta; хранит submission и не повторяетunknown.
Толькоdiagnostics,неproduct/freegrant. MD/XSD/scheduling+Lua51syntax прошли.
Startup203 также выявил две productparser ошибки @property?: Runtime
Action.StartTime и генератор PreviousObservation.miningtypes. Убраны @
перед existence? в исходниках; regenerated13copies. Cheapexistingvalidator
теперь проверяет этот запрещённый синтаксис, включаяadaptedMD.
Установлены45files и исправленныйdiagnosticLua, штатныйrestart выполнен.
Единственный живой pipeowner Load206 execsession77899, save004 pending.
Сначала terminal+role, затем blueprint один раз; не запускатьexpansion
повторно: надо продолжитьconstruction_1_393687.476. Нужны actualpayment,
planvalidation/identity/queue/funding/builder/resources и дальнейшийreadback.

Актуальный checkpoint197: предыдущий goal turn — progress; текущий также
исправил реальные границы плана и получил игровой read-back. OpenSpec apply192
ready8/32 (sandbox read191 не видел схему, elevated192 прошёл без изменения
конфига). Штатный restart/Load193 session43682 terminal acceptedautosave01.
PID20912. Role194 session98633 terminal; сначала bound, через10s активен.
Expansion195 один генератор; Role196 keyconstruction_1_393659.925,
eventsuccess1/count4/11connectors. Чтение pseudo entry через конкретные поля
подтверждено: construction_entry_invalid исчез. Plan теперь показывает
required_blueprints_missing, но ReadPlanPage также получил null loadout на
всех4элементах. Это штатное отсутствие оснащения, не отсутствующий элемент.
Новый пакет: сохраняет реальный Loadout/null, пустой список только при null,
отдельный has_loadout snapshot; identity требует совпадение наличия оснащения
и списков. Старые snapshots без has_loadout отвергаются до эффекта.
UI MD task reason перечисляет максимум32 фактически недостающих чертежа;
диагностика read добавляет construction_missing_blueprint ware/name.
XSD/scheduling и существующий UI fixture прошли,45файлов+diagnostic установлены.
PID20912 пока использует пакет ДО null-loadout/названий, для их read-back
нужен следующий restart. Ui197 открыт через мод, pipeownerнет. Не повторять
expansion195 в этом сохранении и не сбрасывать маркер. Следующая адресная
проба чистый autosave01: read реального missing list без MDerrors, затем
обычная оплаченная покупка чертежа по штатному маршруту, никаких freegrants.
Строительство, причинные оценки, personnel arrival и полная приёмка открыты.

Последний checkpoint190: Load186/session9728 terminal acceptedautosave01;
Module187/session76729 terminal, HQXZS342 0x4b6f0, module0x4b760 observed.
Ui188 настоящий статус открыт, 84 строки/2таблицы. PID29644, pipeownerнет.
Expansion189 один запуск; Role190 event success1/count4, реальный key
construction_1_393650.425, statevalidating, checked0. Передача event params
исправлена и подтверждена игрой. Следующая доказанная ошибка ReadPlanPage:
попытка сохранить $Sequence.{1} в $Entry. Штатные scriptproperties.xml1711
описывают constructionplanentrydata как pseudo, не реальный datatype.
Исправлены все 3 места в строительной библиотеке: ReadPlanPage,
CheckPlanIdentityPage и StepQueuedExpansion читают конкретные поля через
sequence.{index}.field непосредственно. XML/XSD/scheduling прошли.
Файл установлен и SHA совпадает, но PID29644 всё ещё использует старую
библиотеку до перезапуска. Вкладка открыта, управляющий активен. Не повторять
expansion189: маркер и generationclaim уже существуют. Следующий пакетный
перезапуск загрузить чистый autosave01, проверить новую planvalidation.
waiting_blueprints/construction_entry_invalid в190 — ошибка псевдотипа,
не доказательство отсутствия чертежа. Полный ченж остаётся8/32.

Актуально после проверки 185: Load180 завершён, autosave_01 загружен.
Role181 подтвердил активного управляющего. Module182 идемпотентно подтвердил
модуль 0x4c954 на штаб-квартире XZS-342 (0x4c8e4); команда не доказывает,
что модуль отсутствовал до неё. Ui183 открыл настоящий tm_empire_status:
две таблицы, 117 строк, данные 68 объектов. Причина ранее исчезнувшей вкладки
пока не установлена; отсутствие модуля в этой сессии не подтвердилось.
Expansion184/Role185: штатный генератор прислал успешное событие, 4 элемента,
393802.253, 11 соединителей. Доказанная ошибка: run_actions библиотека не
получает event.object; AcceptGeneratedExpansion отверг результат с ошибкой
lookup. Исправлены явные EventStation/EventSequence/EventSuccess параметры
в библиотеке, обоих штатных обработчиках генератора и диагностике.
Регенерация 13 скриптов и XML/XSD/scheduling прошли. Установлены 45 файлов
и исправленная диагностика; штатный перезапуск Steam выполнен.
Текущий единственный pipe-владелец Load186, exec session 9728, загрузка
autosave_01. Сначала дождаться terminal, затем role/module/ui и одна expansion
на чистом маркере. Не сбрасывать старые попытки. Полное строительство и
релиз не приняты; остаётся 8/32. Все ниже записи являются историческими.

Load17535624terminal acceptedautosave01; Role176terminal/newManageractive.
Expansion177 nativegeneration once; Role178 age393683.97: goalexists1/budget5MCr/
connectors11 but eventnone/receiptsnull. Proven startup MDerror393627.80:
ExpansionFixtureGenerated event_object_construction_sequence_created without
object/group evaluatesnull notcomponent. XSD allowed optionalattrs but runtime
needs source. Source179 observer childof ExpansionEventTargets rootinitgroup;
adds exacttarget beforegeneration, registersgroup event. Callbackstillfilters
StateTarget andrecords native event. This fix NOTinstalled; XML/XSD/scheduling validation179passed.
Nativegenerator completion remainsunqualified;don’tcallmodeexpansionagaincurrentmarker.
PID33584/45productfiles diag174. Noactivepipeowner.8/32 accepted.


Save173 verifiedgzip game.time393716.007: FixtureGoal validcue760631(State),
budget500000000money=5MCr, targetvalid; previousinputfix confirmed. No record
FixtureEvent/Result and no recordedinstance of nested ExpansionFixtureGenerated
in save (searched actualcueIDs). This is notproofwhy callbackmissing.
Primarycommon.xsd24147 states async generator returnsinstantly/eventlater;
stockEconomy nests observer inchild. SourceExpansion174 diagnostic now independent
toplevel observer event_object_construction_sequence_created + exactStateTarget
check; records observed/success/count then calls sameproductAcceptGeneratedExpansion.
Read now includes expansion_fixture_state budget/goal/connectors/event/result.
No unsolicitedpipe response; no immediate blockinggenerator/directconstruction.
XML/XSD/scheduling passed. Source174 NOTinstalled; nextsamepre165autosave01
withoutmarkerreset needed. CurrentPID43744/installeddiag168,45productfiles;
noactivepipeowner.3.4 and fullchange remainunqualified8/32.


Role170terminal: autosave01 validboundgovernor existingemployee0x4c8de/HQ.
Expansion171 once acceptedgenerating; nativeManagerbootstrap last_run393637.814
proven onnewsave. Role172 age393689.967 constructionreceiptsstillnull, noTMerrors.
Correctedfixture StateGoal/budget5000000Cr installed; nativeeventresult notyetknown.
Save173 requestedONLY004 to inspect actualState/childcue/generation; verify gzip
write beforeuse. Originalautosave01 untouched, nextdiagnosegenerator notrerun.
PID43744/45files coherent;noactivepipeowner;8/32accepted.


DiagnosticExpansion168 fix installed: stableGoalState/budget5000000Cr;
product45filesledger161/bootstrap153 unchanged. Normalrestart succeeded.
Load169 client85266 terminalexit0 accepted autosave01 (preExpansion165); source
slotsnotrewritten. PID43744 respondingtrue/CPU39.39, no debug5MCr/TM MDerrors.
Role170 readclientstarted (inspecttoolsession), onlypipeowner untilterminal.
Next inspect existinggov/module; use module/checkonlyifneeded, then expansion
onceoncleanmarker; don’treset priorattempt manually. 3.4/6.3 notaccepted8/32.


Load163 terminal21980accepted; Role16478250terminal confirmedactive/receiptsexact.
Expansion165 productBeginExpansionGeneration returnedgenerating HQXZS342
at389845.279; Role166 after28s constructionreceiptsnull. Save167 overwritten
ONLY004 captures actualfixture State: issued/targetvalid, Goalcueempty/Budgetnull.
Found explicit scriptparse Input:[player.money,5MCr].min in debug, notMDcueerror.
Sourcefix: budget5000000Cr; fixturegoal stableState insteadshortlivedthis.
No claimsnormalbuildaccepted from165. Validationneeded; fix notinstalled.
Save004 nowcontains generationclaim/attempt167, use pre165 baselinequicksave/
autosave or preserve167+explicitreconciliation (don’tresetmarkers blind).
PID47656/live45files; noactivepipeowner.8/32accepted. Ledger161 installed;
afterrebindvisibility check notyetdoneinthisrun.


Installedledger16145productfiles plus diagnosticExpansion162 after XSD/scheduling.
New probe.py expansion→expansion_fixture, no direct module/stationcreate. Calls
BeginExpansionGeneration for ownHQ/newtm_empire_control macro, nativeconnectors
Station.modulesets1; parentcue is exactgoal; childnativeconstructionevent calls
AcceptGeneratedExpansion. Product owns blueprint/queue/funding/builder/readback.
Budget max5MCr/currentplayerbalance. Singleattempt marker, no unsolicitedpipe
reply onasyncgeneration. Probe notruntimequalified,3.4 stillopen.
Normalclose/install/Steam restart success. Load163 save004 client starts:
inspect exacttoolsession before moreclients. UI ledger oldunknown/building
visibility gate also pending. Originalslots untouched.8/32 accepted.


Provision159 fresh native analysisperiod389824.533: KMT485 production resources1,
restriction1/provisionnull, trueperiod/manager. UI160 status opened81rows/2tables.
Found newruntime UIgap after rebind: global unknowncrew/buildingpurchase exist
but receipt.manager != currentManager hides both tasks. Sourceledger161 repaired:
unfinished receipts visible across cue replacement (terminal observed/delivered/
completed/consumed/rejected/revoked excluded unlesscurrent), with explicit
previousappointment reason. Noeffect/replay/reassignment added. XML/XSD/scheduling
+existingUIfixture passed. NOTinstalled yet; liveunknown/buildingvisibility gate
stillrequired. PID21068/installed45files, noactivepipeowner.8/32 accepted.


Bootstrap153 LIVE passed narrowfirstanalysis: Role155 completed; release156
unbound, rebind157 sameactor0x4afab bound/stationmanagerunchanged1. Role158
oneactiveManager/goals1, nativeeconomy_last_run389824.533 (old389774.468),
age389839.304, no manualanalysis command and debugTM MDerrors0. Exactpaid
build285357ULL/5267498Cr/bank64726187 preserved; crewreceiptunknown no repeat.
Noactivepipeowner. Installed45 coherentfiles/PID21068. Firstnativeanalysis
bootstrap corrected and verified; full3.2/3.3/personnel/assessment open8/32.
Previous Role155pending note below historical.


Load154 client31496 terminalexit0 accepted save004; livePID21068 respondingtrue.
Role155 readclient запущен (toolsession), onlypipeowner пока readpending.
Следующий шаг release/place того жеemployee и role после5s безmanualanalysis;
проверить fullyqualifiedbootstrap153 last_run увеличился, debugTMerrors0.
assignment-contracts обновлён по actual140/141/149 и failed152, не claims4.2done.
8/32 accepted.


Bootstrap153 fullyqualified fix установлен45files; normal close/install/Steam succeeded.
Load154 save004 client session31496 alivewaiting, единственныйpipeowner.
Нельзя новыеpipecommands пока154notterminal. Next role/release/rebind check
native firstanalysis exactlast_run/newstationperiod plus no duplicate paidbuild.
Предыдущая запись NOTinstalled bootstrap153 ниже теперь historical.


Role149 terminal97451 exit0 loadconfirmed: active1/goals1, exact paid build
285357ULL/5267498Cr samekeypurchase3_389778.271, bank64726187 unchanged;
crewunknown sameperson/sourceremoved/targetmember/transit1. Release150 unbound,
hasgov0/active0 managerstationunchanged; Rebind151 sameactor0x4aacc bound.
Role152 oneactiveManager/goals1 no duplicate crew/payment. BootstrapFAILED live:
Econ_Manager inst188c08 at389824.76 lookup GenerateShortageData_Delay null.
Rootcause library instance needs fullyqualified md.TM_Empire_FactionLogic_Economy.
Sourcebootstrap153 correctedfullyqualifiedcue, regen13scripts/XML/XSD/scheduling
passed; fix NOTinstalled yet. Do not claim firstanalysis works from earlierchecks.
Currentinstalled45files/PID44824 responding; noactivepipeowner.8/32 accepted.


Load148 client77175 terminalexit0: accepted save004. X4PID44824 respondingtrue/
CPU80.27; debuggame.time389801.16 загрузка началась с точного Save147. Installed
coherent45 productfiles sourcebootstrap/period/provision/terminalcallback.
Role149 readclient запущен (смотреть toolsession), ждётготовности runtime;
не запускать второйpipeowner. Unknowncrew/payment pending сохранены в004,
живойread-back их состояния/невоспроизведения ещё не получен.8/32 accepted.


Save147 реально записан save004: size95044027/game.time389801.158,
bank64726187/GUIDC45BAA91-B465-4CF8-B9F7-3B8AF5303AC3. Содержит nativebulkunknown
и paid pendingbuild285357ULL/5267498Cr. Originalslots untouched. Installed
45files coherent bootstrap/period/provisionresponsibility/terminalcallback
package; normalclose/install/Steam restart success. Load148 save004 pipeclient
pending: inspect exact toolsession returned before morepipe clients.
No replay of unknowncrew/paidbuild.8/32 accepted; allnewruntimechecks open.


Arrival141 observer73771 terminalexit0, resultunverified/timeout600s.
Nativebulk receipt nowunknown: age389737.34 vsissued389131.617, sourceabsent,
targetmember1/exactrole/intransit1/temporary1/podnull/scheduled0. Noeffectrepeat,
no oldNPCfallback. specificdebugerrors(TM MD/personnelLua/NPCAssigned)=0;
no primaryrootcause yet. 4.2 notqualified. Pipe ownerreleased; subsequent
Analysis145/Provision146 independentnativeeconomy probes dispatched.
Next investigate exact bulk event/cue transit chain, record source/target
native transport context; don’t inferarrival frommember1 or clearflags manually.
Source bootstrap/period/provision/terminalcallback not installed.8/32 accepted.


НЕ установленная source crew144: ApplyCrewExchangeSubmission принимает
callback только для sent/unknown. Терминальные observed/rejected не возвращаются
в sent от delayed/duplicateLuaevent. XML/XSD/scheduling + transfercontract passed.
Arrival141 observer73771 confirmedlive;078 age389619.819, Targetmember1/Source0,
roleexact/intransit1/scheduled0/podnull/temporary1, ещё sent. result.json absent.
Не повторятьeffect, не создавать второйpipeowner. Sourceнакопленныеgroups
bootstrap/period/provisionresponsibility/terminalcallback ещё НЕ installed.
Installed45files/livePID27436. Full goal retained;8/32 accepted.


НЕ установленная source группа period143: economy_observation сохраняет
actualmanager skilltype.management. SameProvision сравнивает skill, чтобы
семинар начинал новый период. NativeUpkeep miningtypes сравниваются по полной
принадлежности/количеству; missing boundedcoverage не равно emptytypes и
сбрасывает продолжение. Generator13scripts + XML/XSD/scheduling all passed
(period143-validation). Source bootstrap/provisionresponsibility/period группы
не установлены. Нужна livequalification сменыskills/miningtypes/rollback.
Arrival141 observer73771 live latest049 age389440.557, nativebulktransfer
sent/intransit1/temporary1/podnull. No repeat/legacyNPC fallback. 8/32 accepted.


НЕ установленная source группа nativeeconomy bootstrap: выяснено штатное
первое GenerateShortageData_Ticker 25–30min, далее15–20min. adapt_economy_observations
при создании своего Econ_Manager (exact registrycue/active guard) единожды
signal GenerateShortageData_Delay, reuse existing5s→GenerateShortageData pipeline.
Нет собственного планировщика/анализакаждыйтик; periods remain stock.
Generator regeneration13scripts passed; validate_md-IncludeNativeCopies passed
(bootstrap142-validation). Вместе с causeprovision/UI эта группа не installed.
Arrival141 observer73771 жив; latest040 age389384.799, unchangedintransit1.
Не повторятьnativebulk, не делатьload/save/restartпока observerowns pipe.
Full4.2/5.3/5.4/runtimebootstrap qualification open;8/32 accepted.


НЕ установленная source группа: AssessStationResponsibility выдаёт отдельный
scopeprovision: insufficient_provision/medium только nativeUpkeep mining/budget
facts, иначе unknown/low. Явно не доказывает overallperformance/managerfault.
UI validates scope/kind/confidence/reason/recommendation и выводит отдельные
строки ответственности/рекомендации. XML/XSD/scheduling/UIfixture passed;
fixture проверяет render и rejects unknownmedium/overallscope. Полные правила
manager_decision/external/mixed и causalfeedback ещё не сделаны,5.3/5.4 open.
Arrival141 observer73771 re-polledlive; latest021 age389267.417 targetmember1/
sourceabsent/intransit1/scheduled0/podnull/temporary1; ordinarybulk arrival
ещё не observed. Не restart/replay/recoveryoldNPC. Installed45files unchanged.


Check139 after native governor deadline: bound; existing stationmanager
rejected existing_post, unchanged1. Transfer140 single new ordinary crew native
bulk accepted: GYU115→MZK812, exactperson9873631311134785487, issued389131.617.
Arrival141 observer session73771 live, timeout600s, onlypipeowner. First readback
age389156.375: Sourceabsent/Targetmember1/roleexact/intransit1/scheduled0/
podnull/temporary1. Receipt native_bulk_crew_exchange_pending. No old recovery,
no actor creation, no repeat. Current stock menu_map.performCrewExchange has
no additional effect after PerformCrewExchange2; native arrival awaited.
PID27436 active, one Manager/goals1. Source slots untouched. 4.2 not accepted
until actualarrival plus negatives/save-load;8/32 accepted.


Role130 confirmed quicksave loaded age388755.686: inactive/no receipts,
2stations/66ships. Module131 added HQ XZS342 module0x4a7cb. Assign132 transferred
existing employee seed-9126173547698565463 from DAS334; Place133 instantiated
same template actor0x18abf9. Check134 stationmanager rejected existing_post,
governor not_arrived, stationmanager unchanged. Role135/136 actual physical
station/roleobject0x4a75e and native poddeadline389095.039, age388952.788;
not activate before deadline. No direct timer clearing. Next check after native
arrival, then one personnel_transfer_fixture on clean receipt. No pipe owner
currently running. Contract fixture covers helm/ownership/capacity rejection,
MD approval, pre-effect recheck, duplicate/unknown no replay and passed;
real LuaJIT uint64 seed fixture remains separate. Native live success pending.


Установлен новый согласованный пакет45productfiles (install exit0); diagnostic
MD/Lua обновлены. RequestTransfer ordinary crew больше не вызывает старый
AssignHiredActor дажеcheckonly; Post остаётся nativeassign. Legacy bulk recovery
исключён. XML/XSD/scheduling/UI/realuint64 fixtures passed. Игра штатно закрыта,
запущена через SteamExe изHKCU без дополнительныхаргументов: PID27436.
Load129 client43594 завершён exit0: штатное меню accepted quicksave.
Последняя проверка PID27436 Respondingtrue/CPU62.58/4.57GB, загрузка сохранения
в процессе; accepted меню не доказывает готовность MD или crew/lifecycle. Исходные slots
не перезаписаны. 8/32 accepted, полный change остаётся незавершённым.


Проверка по просьбе пользователя: Role127 live age390113.437, governor active,
station/roleobject0x4a9e1, employee0x4a9e7, podnull/intransit0. Модуль и
назначение существуют, повторно модуль не добавляли. UI128 командой открыт
mode tm_empire_status,111 body rows/2tables; has_governor1/active1.
Arrival126 observer92811 завершён: result unverified/timeout900s,
role-slot unavailable, старый crew receipt unknown; не повторять dispatch.
Новая source группа native bulk bridge реализована, ещё НЕ установлена:
ui/personnel_transfer.lua + ui.xml, exact uint64 NPCSeed, native checkonly,
MD approval recheck, unknown marker before one PerformCrewExchange2.
Оба legacy recovery исключают native_bulk receipts. XML/XSD/scheduling и
real LuaJIT uint64 seed fixture passed. Package dry-run45files ранее passed.
Live native bulk/save-load/lifecycle and release acceptance remain open8/32.


Arrival126/090 age389490.105: native role-slot unavailable, actorresumeattemptnull;
worker NPC не создавался, transfer unknown/intransit1. Observer92811 живой.
Найдена текущая stock bulk crew граница menu_map:24211 PerformCrewExchange2;
AssignHiredActor там используется для manager/shiptrader, обычные crew идутbulk.
DEPRECATED order.trade.crewexchange (с3.30) не применять. Контракт точных NPCSeed/
checkonly/ownership/helm/membership/read-back записан assignment-contracts.
Следующая продуктовая порция: подключить native bulk для обычных Role transfers,
сохранив AssignHiredActor для Post и unknown безповтора. Нового bridge пока нет;
не заявлять4.2 completed. Старую квитанцию не переводить повторно новымAPI,
испытать native bulk из раннего сохранения, разрешённого пользователем.
НЕ установленная source группа waiting_arrival/trade flows/ReadTransferGovernor
дополнена сохранением owner actor/station/module прямо в новых transfer receipts;
legacy fallback только через exact original cue variables. XML/XSD passed.

НЕ установленная lifecycle группа: ValidateBinding сохраняет appointment также
при transit/scheduled/временном отсутствии физического контекста, если рольobject
по-прежнему та же станция и module/ownership действуют. Waiting_arrival отзывает
effects/старый Manager; UI сохраняет has_governor с inactive/причиной ожидания.
После native arrival StartWatch запускает один новый Manager. ReadTransferGovernor
позволяет согласование существующей квитанции новым экземпляром только при точном
совпадении исходного Governor/Station/Module; остальные safeguards/attempt markers
не меняются, при другом сотруднике recovery запрещён. Это устраняет зависимость
старой квитанции только от cue instance после штатного ожидания, не повторяет
assignment. XML/XSD/scheduling/UI fixture passed; живой переход ещё не принят.
Observer92811 продолжает работать, source изменения на него не влияют.

Важная коррекция прежнего вывода: common.xsd21483 документирует, что Actor
может физически быть в destination, но остаётся unavailable до pod arrival.
Поэтому снятие pod guard было ошибочным. В НЕ установленном source возвращены
guards BindGovernor/role availability/ArrivalWatch/post personnel read-back.
ValidateBinding теперь при pod timer сохраняет назначение, отзывает новые эффекты
и переводит registry waiting_arrival; после native timer clear переводит bound
для обычного запуска единственного Manager. Не удаляет appointment по одному
timer и не выдаёт физический container за arrival. XML/XSD/scheduling passed.
Нужен игровой pending→active/save-load read-back. Старые записи про «остаточный
timer не снимает» относятся к ошибочной установленной версии, не к принятому
контракту. Observer92811 продолжается; в текущей игре его governor deadline уже
прошёл, но предыдущая ранняя активация не считается корректной приёмкой2.4.

Новая НЕ установленная группа: readonly торговые потоки через native
event_player_trade_completed/event.param.transferredamount (common.xsd16094,
scriptproperties1522). До32 stations×32wares, только свои station buyer/seller,
точные manager/employee/session/period, reset onload; crewexchange исключён.
UI показывает фактические входящие/исходящие товары, не объявляет это прибылью.
XML/XSD/scheduling и existing UI fixture с positive render/чужим периодом/negative
quantity passed. Событийное покрытие player-station trades ещё не доказано живым
прогоном;5.1/финансы/причинные правила не приняты. Observer92811 живой, единственный
pipe owner. Последний осмотр age389003.625, active, transfer sent безattempt.

Load121 accepted, role122 active/goals1/economy/factory receiver/patrol entry1.
PID29748 отвечает. NativeAnalysis123 requested, Provision124 age388925.354:
KMT485 production complete1/total1/resources1, assessment observed/medium с явным
ограничением снимка и неизвестной виной; период388909.45 samples1, restricted1,
budget provisionnull, stocks вода/энергия0, subordinates total/read0 complete1.
UI125:112 строк/1205px/621maxheight, valid projection. Штатный анализ породил
оплаченный заказ1066743Cr, build34468ULL, built, bank70151778; не duplicate старого.
Role122/session58824 завершён; analysis/provision/ui тоже завершены. Запущен
Arrival126/session92811 — единственный observer текущего crew person9873631311134785487/MZK812
на установленном role-slot пакете, timeout900s. 8/32 accepted;5.2 подтверждена
только производственная станция, специализированные и причинная оценка открыты.

Текущий пакет установлен:44 product files, обновлён diagnostic MD/Lua.
Arrival120/session65049 завершился unverified (900s), без нового назначения;
actorresume native_existing_employee_instanced не снял template.intransit.
Накопленная группа: stock role-slot instancing; physical post read-back без
остаточного timer veto; production product events32; purpose-specific assessment;
readonly resumed_actor/behavior/station_assessment/product diagnostics.
X4 штатно перезапущен. Load121/session20737 ожидает save_004 доattempts.
Следующие действия: дождаться именно20737, role read-back управляющего,
native_analysis для свежего периода, provision/ui в том же прогоне, затем observer
существующего person9873631311134785487/targetMZK812. Новый transfer fixture НЕ
нужен. Save_004 не перезаписан; 8/32 приняты, пакет пока не принят в игре.

НЕ установленный пакет дополнен stock role-slot instantiation в personnel recovery:
find_npc_slot roleReceipt.role перед попыткойcreate, отдельная причина отсутствия
места, exact slot вместо общего placementobject controlroom. Native worker при
отсутствии slot выбирает despawn, поэтому одно создание в комнате недостаточно.
Это source-контракт, не доказанная причина конкретного Arrival120. Readonly
crew_resumed_behavior для state-machine/roomslot/type добавлен в diagnostic source.
XML/XSD/scheduling passed. Observer65049 ещё живой, новых dispatch/save/load нет.

Arrival120/095 age389484.528: native transportattempt389400.648,
observedpodarrival389410.649, actorresumeattempt389475.673 теперь
native_existing_employee_instanced (seed/template/roleobject/role подтверждены
синхронным результатом). Но roleentity ужеnull и people.intransit1, квитанцияunknown;
это НЕ completed transfer. Наблюдатель65049 ещё живой, повторов нет. Предыдущая
ошибка role association исправлена, дальнейший native NPC lifecycle ещё исследуется.
В НЕ установленной диагностике добавлены station_assessment/production_product,
XML/XSD/scheduling passed. Следующий pipe owner только после завершения65049.

НЕ установленная группа дополнена AssessStationResults: трактует existing native
purpose/complete production flags относительно назначения. Производство — числа
текущих состояний, строительство — native isbuilding; торговля/склад и ship_support
показывают недостающие результаты вместо оценки по прибыли. Evidence assessment
содержит observed/unknown, medium/low и объяснение границ снимка; не обвиняет
менеджера и не подменяет причинные правила5.3. UI передаёт/рисует assessment;
existing fixture проверяет unknown low, observed medium и запрещает неподтверждённый
manager_decision в поле результата. XML/XSD/scheduling и UI fixture passed.
5.2/5.3 ещё не приняты; до установки/игровых результатов группа только source.
Arrival120/session65049 живой,049-read age389207.934, active/sent безattempt.

Дополнение НЕ установленной группы: root-cause timer fix в физическом read-back
ObserveHire/ObserveTransfer controlpost (см.assignment-contracts), агрегат UI
называет завершения продукции, не количество физических циклов всех модулей.
Проверки XML/XSD/scheduling/UI fixture passed. Arrival120/session65049 живой,
последний осмотр033: age389111.745, runtime active, crew sent безrecoveryattempt;
до10min recovery boundary ещё не дошло. Наём/перевод/оценка остаются открытыми.

Новая source-группа пока НЕ установлена: производственные события по32 товарам
в пределах существующего employee/manager/session/period; started/finished
используют native event.param2 (common.xsd15215/15226), cancelled остаётся общим
из-за другого payload. UI отображает циклы, не выдумывает количество продукции.
XML/XSD/scheduling и дополненный существующий UI fixture passed (положительная
отрисовка, превышение aggregate и дубли). Добавлено readonly crew_resumed_actor
для следующего диагностического пакета, также ещё не установлено. Arrival120
session65049 остаётся живым единственным pipe owner; его не прерывать ради
этой группы. Last read: age389003.517, governor active, transfer sent безattempt.
5.1/4.2 остаются открытыми; source-проверки не заменяют игровую приёмку.

Load118 accepted save_004, Role119 подтвердил исправление регрессии: runtime active,
manager/goals/economy/factory receiver существуют, patrol entry_count1. Governor
0x4a503 на HQ0x4a4fd (container/station/roleobject совпадают), intransit0/scheduled0,
остаточный pod389055.697 не снимает назначение. Seed-9126173547698565463 и
station manager0x4a500 unchanged. PID21128 отвечает. Crew исходная квитанция sent,
person9873631311134785487/targetMZK812, никаких recoveryattempt пока нет.
Arrival120/session65049 — единственный живой readonly pipe owner, timeout900s;
наблюдает штатное однократное восстановление без dispatch/save/load. Перед другой
командой проверить завершение65049, не создавать конкурирующий pipe client.
Регрессия управляющего подтверждённо исправлена; весь пункт2.4 ещё не принят.

Текущий шаг: Role117 доказал физическое положение сохранённого управляющего
на HQ при intransit0/scheduled0 и остаточном pod timer. Устранена ошибочная
проверка этого таймера для физически прибывшего Actor; физические/роль/transit
границы сохранены. Проверки XML/XSD/scheduling passed,44 product files installed.
Load118/session43505 ожидает загрузки save_004 для повторного read-back.
Никакой тестовый слот не перезаписан. Предыдущие Load114/116 завершены.

Load114 accepted save_004. Role115 обнаружил регрессию новой физической проверки:
registry inactive/governor null при сохранённом fixture employee0x4a9db,
seed-9126173547698565463, station manager0x4a9d8 unchanged. Crew receipt остаётся
sent без recoveryattempt. Новые эффекты остановлены; сохранение не перезаписано.
Для установления точного отсутствующего свойства governor_location теперь читает
сохранённого fixture employee, если Registry уже удалил привязку. Это только
read-only диагностика; XML/XSD/scheduling passed, диагностический MD установлен,
X4 штатно перезапущен, Load116 ожидает ту же save_004. Пока не менять guards
на предположении и не считать load/перевод принятыми.

Последняя группа: module112 подтвердил существующий модуль HQ0x4b9a8;
ui113 открыл статус,109 строк, governor/active1. Arrival111 завершён unverified
после900s, без повторного назначения. Исправлен пропущенный штатный
set_entity_role_object после создания физического NPC существующего сотрудника;
подробности в assignment-contracts.md. Дополнены физические/pod/scheduled
проверки управляющего и readonly governor_location/construction/subordinates.
XML/XSD/scheduling проходят. Группа44 файлов установлена, X4 штатно перезапущен
(PID14240). Load114/session75123 ожидает соединения для загрузки save_004 до
однократной попытки восстановления; результат загрузки ещё не подтверждён.
8/32 приняты, новых игровых критериев этот пакет пока не закрывает.

Обновление текущего прогона: пользователь разрешил загрузить любое нужное
сохранение для испытаний. Исходные слоты не перезаписываются; результаты — save_004.
Save82 завершено до перезапуска (game.time396126.199). Установлена новая группа44
файлов: участники поручений, история до16 снимков текущего периода производства,
проверки pod arrival при найме и точное наблюдение native deadline перевода экипажа.
Восстановление физического NPC использует существующий person/template и штатный
NPC_State_Machines, без нового сотрудника и прямого снятия isintransit; успех требует
последующего read-back. Старой квитанции без наблюдаемого deadline это не применяется.
XML/XSD/scheduling и существующий UI fixture прошли. Load83 accepted quicksave. Module87/Place88 подтвердили модуль HQ и
существующего управляющего при неизменном менеджере станции; read94 active.
UI97 видима,82 строки. Новый purchase_1_389791.137 paid5301758Cr, настоящий
build/index1 typeoflargefloat. Read104 подтверждает delivered первого заказа,
YNL892/TradeRoutine/Econ_Manager и самостоятельный второй заказ1076355Cr.
Transfer95 отправлен один раз, Arrival98 завершён timeout180s без подтверждения
прибытия и без повторной команды. Save102 не записал файл; API request не принят
за completed save.
Source CaptureCrewPod дополнен ограниченным наблюдением30×1s задержанного
штатного pod timer; CheckRoles защищён от незавершённой fixture. Добавлена
сводка подчинённых из native report. Новая группа44 файлов установлена;
XML/XSD/scheduling, UI fixture и diagnostic Lua syntax прошли. Load106 accepted
quicksave, PID48892 живой. Fresh107: module HQ0x4b9a8, отдельный сотрудник
0x1885d3/seed-9126173547698565463, manager0x4b93e unchanged, runtime active,
goals1/economy/factory receiver. Штатный scout purchase_1_388784.415 delivered,
paid1213332Cr, bank71218521; независимые native Recon приказы продолжаются.
После120s перевод crew-person9873631311134785487 остаётся sent/intransit1,
podnull/actornull/temporary1, новый dispatch не выдаётся. Arrival111 продолжает
наблюдение до900s через session84669; единственный pipe owner.
Save fresh107/035 фактически завершено12:15:20,94534284bytes, time388907.261;
исправление диагностического SaveGame+closeMenu подтверждено. Analysis108/109:
свежие station periods samples1, restricted1, stocks воды/энергоэлементов0,
history_samples1. OpenSpec strict valid, ready8/32.
Новые игровые критерии пока не приняты: по-прежнему8/32.


После перезагрузки работа возобновлена, диагностика скорости запуска закрыта
пользователем. Пакетная приёмка записана в `batch-acceptance-20261011.md`.
Установлены полная ширина UI, интерактивные строки со штатной прокруткой,
классификация назначения станций и исправления чтения сводки экипажа.
Тестовое save_004 сохранено 11.10 в 11:14:30: HBL-445 выполняет TradeRoutine,
положительное обучение менеджера KMT-485 сохранено (skill8→11, семинар1→0).
Один отправленный crew transfer сохраняется без повтора: прибытие не подтверждено,
квитанция unknown. Экономический пакет учитывает асинхронные оплаченные заказы
и публичные предложения рынка. В первой пробе обнаружена ошибка области
видимости run_actions; исправлена явной передачей двух таблиц и установлена.
Повторная проверка явных параметров прошла без своих ошибок MD. Анализ30/role31
подтвердил штатный выбор request_priority_freighter и корректный failed/waiting
вместо вечного unknown. Исправлены денежные единицы Lua→MD и сравнение
обёрток компонентов через штатный IsSameComponent.
Role41/build42: ключ purchase_23_392649.211, создан обычный оплаченный заказ
за8370545Cr; native identity/container=true, missing_resources=false/queue0.
Production tracking остановился из-за потери типа build при Lua→MD: возвращённый
userdata стал component cargo_gen_buildstorage. Установлено сопоставление через
индекс исходного типизированного MD-кандидата и точный BuildTaskID, повторная
загрузка47 подтвердила восстановление без повторной оплаты. Build52 подтвердил
готовый playerowned/operational корабль, role54 — HBL-445 с TradeRoutine,
переданной Econ_Manager собственностью и штатным TTL. Задача3.5 принята.
Задача4.3 принята: отрицательный случай без семинара, потребление одного реального
предмета и рост навыка, запрет повторной диагностической отправки подтверждены.
Следующий заказ24 за1135669Cr завершился до исправления типа Lua-индекса
largefloat; исходный build уже удалён, точная связь с готовым кораблём потеряна.
Он остаётся unknown без повторной оплаты и поиска похожей собственности.
Установлены штатные production flags и bounded production event counters.
Read68: KMT-485 waiting_resources1 при нулевых запасах воды/энергоэлементов;
HQ не получает ложную оценку за отсутствие прибыли. Циклы ещё не наблюдались.
Вкладка видима и прокручивается; стандартные empire/stats открываются.
Полные причинные оценки остаются открытыми. Установлено однократное продолжение
отсутствующего native transport после уже наблюдаемого назначения того же
crew-person: source0/target1/role match/no actor/no pod arrival/no schedule.
Повтор assign_hired_actor не вызывается. Arrival71 подтвердил штатный pod arrival
и завершение его таймера, но isintransit остаётся1; прибытие не принято.
Load73/role75 подтверждают active и сохранённые квитанции без повторной оплаты
или запуска транспортировки. Исправлены типизированный адрес factory receiver
и NPC job-ветка RedeployJobShips; собственных MD ошибок в свежем журнале не найдено.
Положительная приёмка строительства и флотов этим не закрывается.
В исходниках дополнена проекция глобального ограничения торговли станции;
пакет44 файлов установлен, load77 принят. Role79 подтвердил factory_receiver_exists1,
69 активов: 2 станции, 26 S/30 M/10 L/1 XL, состояния waiting4/sent2/excluded63.
Оценка менеджеров остаётся unknown до свежих наблюдений текущей сессии.
OpenSpec ready, принято 8/32; релиз не квалифицирован.

## Порядок работы — согласовано 10.10.2026

Цель — ускорить разработку TopManager. После общего аудита зависимостей и несовместимых границ собирать целостный адаптированный штатный управляющий крупными согласованными порциями. Во время разработки выполнять дешёвые проверки синтаксиса и ссылок изменённых файлов; не повторять принятые проверки штатного AI, не создавать тест на каждую мелкую правку и не перезапускать игру ради каждого пункта.

Затем одним пакетом испытывать все доступные сценарии, собирать независимые ошибки в общий отчёт, исправлять группами по первопричине и повторять затронутые сценарии вместе с общим прогоном. Адресная игровая проба нужна только когда неизвестная граница блокирует сборку или делает остальной прогон недостоверным. Падение или неконтролируемые повторные эффекты требуют остановки и исправления; обычная локальная ошибка не мешает проверить независимые сценарии. Один подтверждённый игровой прогон может закрывать несколько задач. Критерии выпуска и реальный read-back сохраняются; до приёмки задачи остаются открытыми.

Текущее сохранение пользователь подтвердил как тестовое: дополнительная резервная копия не требуется. Разрешены запуск, штатное завершение и перезапуск X4 через консоль по необходимости испытаний. Это разрешение относится к тестовому сохранению и X4, а не к другим сохранениям и посторонним процессам.

Change: add-empire-management-module. Выполнено 8/32 задач; установленная разработка не является принятым релизом. Приёмка изоляции Manager: `docs/manager-isolation-acceptance-20261011.md`; текущая проверка обеспечения и обучения: `docs/station-provision-observations.md`. Нижеследующие записи сохраняют историю проб и могут описывать предшествующий пакет.

## Текущий целостный пакет

11.10.2026, остаточные NPC jobs: общий аудит выявил один reachable get_suitable_job в Invade_Space для выбора expedition-tags и два запроса/set_job_active в невызываемой Fleet_Evolution библиотеке Job_Helper. Экспедиционная ветка теперь проверяет известный operational собственный боевой корабль и использует player military-category; реальные планы/фазы военной цели не удалены. Неиспользуемые библиотеки глобального переключения NPC job фаз исключены из private closure (их checker уже отсутствовал). Аудит всех staged MD теперь запрещает get_suitable_job/request_job_ship/create_job_ship/set_job_active. Пересборка/границы/XML/XSD прошли, поиск подтвердил отсутствие этих действий. Полноценный состав/пополнение/назначение реальных флотов остаётся задачей3.6 и не закрыт отсутствием NPC jobs; UI/оценки/общая приёмка также открыты. Пакет не установлен, 5/32.

11.10.2026, завершение recycling: common.xsd подтверждает event_build_finished.param3=buildtask, event_build_cancelled.param=buildtask. До очереди сохраняется receipt на buildstorage и регистрируется группа observer. События сверяют точный BuildTask; только finished + исчезновение станции либо отсутствие её модулей даёт observed, отмена/просто пропажа остаются unknown. Экономический tick завершает ActionDefinition.RecycleEndTime после observed. Независимый FinishedRecyclingWatch (до8 stores/15s) финализирует receipt и снимает exact station claim даже после отмены исходной цели; действующий штатный build не отменяется. Пересборка, границы и XML/XSD прошли до добавления независимого observer. Ресурсный возврат и реальный full-station build event всё ещё не проверены в игре; прочие роли/ручные корабли сохраняют причины ожидания, пакет не установлен, 5/32.

11.10.2026, подключение переназначения: Runtime.RequestStationReassignment сохраняет отдельный lease перед выдачей TM_AssignCommander, требует exact recycling goal/source, actual current commander, совместимость исходного assignment с новым own operational station, отсутствие shared claim/helm/manual/priority. Реальный order handle/ID/object сверяются. StationReassignmentWatch наблюдает до8 leases/15s, подтверждает target+assignment после окончания конкретного приказа, при отмене отзывает только private order; чужая собственность освобождает только нашу metadata. Общий CanUseOwnedShip блокирует незавершённый lease; новый Manager ждёт обе группы старых claims. Recycling переносит максимум4 subordinates×8targets за проход, затем ждёт их реального ухода; приоритет шага стоит перед расстыковкой. Пересборка/границы/XML/XSD прошли до уточнения order ID и удаления foreign metadata. Реальные default behavior, очередь/назначение/helm/save и полный recycling не квалифицированы; пакет не установлен, 5/32 задач.

11.10.2026, подготовка переназначения подчинённых: изучен stock order.assign.commander.xml (cancelorders по умолчанию true, отдельный native assignment/default-order путь). Generator добавляет третью private AI-копию TM_AssignCommander, не меняя original: cancel_all_orders удалён, default cancelorders=false, перед сменой commander/reservations/default behavior вызываются guards ownership/helm/manual/priority, отсутствия обычного claim, точного private order/goal/manager lease и живой собственной цели. Пересборка 13 MD +3 AI, аудит и XML/XSD прошли до последнего условия source/target identity. Выдающий MD-helper/учёт отдельного lease/отзыв и реальное переназначение ещё не подключены; копия staged и не вызывает эффектов сама. Пакет не установлен, 5/32 задач.

11.10.2026, пристыкованные корабли: добавлен StepDockedShipEvacuation, максимум8 candidates/проход с устойчивым курсором и один pending MoveGeneric. Перед приказом используются общий ClaimOwnedShip (ownership/helm/manual/priority/commander), durable order_sent и RecordOwnedOrder; выход подтверждается отсутствием docking/context станции и фактическим расстоянием за её габаритами. Claim освобождается через общий StopAndReleaseOwnedShip после наблюдения, исчезновение приказа без выхода остаётся unknown без повтора. Recycling ждёт вывода корабля до очереди демонтажа. XML/XSD прошли до ограниченного курсора; подчинённые станции с действующими задачами пока защищены общим assigned_asset и требуют отдельного переназначения, чужие/manual ships требуют ожидания; реальная навигация/helm и completion recycling не приняты. Пакет не установлен, 5/32.

11.10.2026, экипаж эвакуации: RequestTransfer расширен взаимоисключающими Post/Role, без изменения прежних вызовов с Post. Role принимает только штатные service/marine, проверяет собственный operational корабль, player.controlled, people.free и native assignment check; используется прежняя durable Personnel.Transfer. ObserveTransfer для Role проверяет фактический seed в people, совпадение роли, отсутствие transit/scheduled и исходного членства. Recycling рассматривает максимум4 человека ×8 кораблей за проход, курсоры сохраняются; первый sent/unknown прекращает выдачу новых переводов. Штатные controlpost/mission/temporary/governor guards сохранены. XML/XSD прошли. Другие роли/станционные NPC, освобождение кораблей, игровой crew transfer и завершение демонтажа ещё открыты; пакет не установлен, 5/32 задач.

11.10.2026, эвакуация station manager: проверен genericactor контракт assign_hired_actor (conversations.xml/common.xsd). Добавлен RelocateRecyclingManager через фактического назначенного NPC, только при точном recycling-goal/source/manager и свободной должности manager на собственной operational станции. HQ/станция управляющего/управляющие модули защищены; реальная попытка сохраняется в общем Personnel.Transfer до native assignment, повтор sent/unknown не допускается. Recycling перебирает максимум8 destinations за проход с устойчивым курсором и ждёт ObserveTransfer/реального назначения до демонтажа. XML/XSD прошли до заключительного защитного условия. Полная эвакуация остальных сотрудников, подчинённых/пристыкованных кораблей и завершение recycling ещё не реализованы/не приняты; реальный genericactor transfer требует игровой проверки. Пакет не установлен, 5/32 задач.

11.10.2026, демонтаж: изучены нативные Remove_Factory и add_build_to_recycle_station. Добавлен TM_Empire_Recycling.StepFactoryRecycling; generator сохраняет исходный выбор/критерии factory и заменяет NPC-эвакуацию, убийство сотрудников и отмену очереди на TM_RecyclingTick. Helper повторно проверяет lifecycle, собственность, защищённые функции HQ/governor/module, отсутствие активного производства, последнего известного производителя, персонала, подчинённых/пристыкованных кораблей и существующей очереди. queue_sent и station claim сохраняются до штатного заказа, фактический Build сверяется; исчезновение станции/Build пока означает unknown, не успешный демонтаж. Пересборка, границы и XML/XSD прошли. Автоматическая эвакуация персонала/кораблей, resources/refund и подтверждённое завершение остаются обязательными незавершёнными частями; новый пакет не установлен, ченж 5/32.

11.10.2026, Economy prefab: generator заменяет оставшийся прямой add_build_to_expand_station в Request_Production_Module на устойчивый TM_ProductionPrefabTick (15s), который вызывает общий StepPrefabExpansion. Ожидающая проверки/BP заявка сохраняет ActionDefinition/RequestGoal/Station и причину, не проходит нативную ветку немедленной отмены из-за отсутствующего Build. После подтверждённого queued/реального handle выполняется прежняя штатная фиксация ProductionEntries; обычные Started/Evaluate_Build обработчики сохранены. Unknown/queue_sent возвращаются как сохранённый результат и не создают второй заказ. Аудит теперь запрещает прямые расширения во всех staged MD; проверка подтвердила их отсутствие. Пересборка, границы и XML/XSD прошли. Контракт first/last, конкуренция запросов и реальная стадийная стройка ещё требуют игровой приёмки; пакет не установлен, 5/32 задач.

11.10.2026, prefab-расширение: добавлен StepPrefabExpansion с устойчивой заявкой GoalCue, проверкой неизменной станции/плана/очередной стадии, общей проверкой BP, лицензии участка и свободной очереди. До add_build_to_expand_station записываются queue_sent и station claim, фактический Build проверяется по станции/buildstorage/isexpansion; неизвестный результат не повторяется. StepQueuedExpansion теперь для стадии наблюдает только [first,last), сохраняя bounded32 и общий путь ресурсов/финансирования/строителя. Manager ExpandPrefabs переведён на адаптер, удерживает выбранную станцию до решения и повторяет только проверку prerequisites через1min. Пересборка, аудит границ и XML/XSD прошли. Economy Request_Production_Module ещё содержит вторую прямую prefab-ветку; контракт Stage/границ и реальная стройка требуют игровой приёмки. Полный пакет не установлен, ченж 5/32.

11.10.2026, установка общего пакета: install_mod.py получил --include-adapted и --dry-run. Полный режим перед записью проверяет точное соответствие staged MD/AI манифесту, SHA и отсутствие конфликтов путей, затем размещает копии в md/aiscripts расширения; диагностические files исключены. Dry-run текущего пакета проверил 42 файла без изменения установленной игры. Частичная установка поверх уже установленного полного Manager отклоняется. Аудит подтвердил две оставшиеся прямые prefab-expansion ветки (Manager ExpandPrefabs и Economy Request_Production_Module): требуется стадийный адаптер с BP/очередью/ресурсами и read-back, они не признаны готовыми. Полный режим пока не выполнялся, игровой запуск не заявлен, ченж остаётся 5/32.

11.10.2026, запуск копии: generator добавляет TM_PlayerManagerWatch/Start внутрь staged TM_Empire_FactionLogic. Реальное bound назначение проходит повторную проверку actor/station/module, starting резервирует запуск, Registry указывает единственный экземпляр ref Manager с faction.player и реальным сотрудником. Непустой общий реестр старых claims задерживает новый запуск. RevokePurchaseApproval теперь отзывает разрешения дерева и отменяет старый Manager после остановки собственных AI. Повторное назначение той же тройки при active идемпотентно; смена модуля отзывает прежний экземпляр. Проекция различает starting/active только по Registry и существующей cue. XML/XSD и пересборка прошли для первого варианта; последующая правка идемпотентности нуждается в повторной проверке. Staged closure по-прежнему не устанавливается обычным install_mod.py; игровой lifecycle/save и все доменные критерии открыты, 5/32 задач приняты.

11.10.2026: Supply добавлен к общему RevokeGoalApprovals, включая payment_approved. Отозванная заявка без финансовой попытки отклоняется до эффекта; наличие payment_sent/paid/unknown сохраняет unknown вместо ложного безопасного завершения. Для сети спутников generator читает SatelliteNetworkGoal из штатного ArgonFactionLogic_Manager (20), устраняя нулевой default общей библиотеки. При инициализации учитываются уже существующие известные собственные operational satellites; они не создаются заново из-за пустого внутреннего списка. Пересборка 13 MD, аудит границ и XML/XSD прошли. Реальная активация копии Manager, весь bootstrap/lifecycle и игровое подтверждение сети остаются открыты; 5/32 задач приняты.

11.10.2026, интеграция Supply с сетью спутников: генератор копии Manager при отсутствии спутника ищет свободный собственный корабль с вместимостью и известного поставщика, запрашивает обычную котировку одного спутника. StepRestockDelivery выдаёт один штатный DockAndWait, сохраняет фактический order в общем claim, после прибытия допускает оплату и наблюдает результат. Завершение освобождает заявку через ConsumeRestockResult; неизвестная отправка не повторяется. Новые сетевые решения сохраняют штатный интервал 1800s, уже выданное пополнение получает отдельное наблюдение 15s. Пересборка closure, проверка границ и XML/XSD прошли до выделения отдельного observer; после выделения требуется повторная проверка. Сеть по умолчанию ещё наследует нативный SatelliteNetworkGoal=0; настройка bootstrap, ресурсная доступность поставщика и игровой путь остаются обязательной незавершённой частью.

11.10.2026, граница штатного оснащения: по interrupt.restock.xml установлено, что ammo содержит желаемый итоговый запас, ключи — ware. Supply теперь передаёт before + amount и сохраняет текущие missile/deployable позиции вместо единственной macro-позиции; котировка оплачивает только докупаемое количество. Перед переводом Lua повторно проверяет собственность, operational и GetTopLevelContainer(ship) == supplier, ABI подтверждён штатным helper.lua/menu_ship_configuration.lua. XML/XSD и supply_payment_fixture прошли. Семантика сохранения всех типов ammo, лимиты вместимости и реальные ресурсные ограничения остаются непроверенными в игре; подключение Manager и доставка к поставщику ещё требуются.

11.10.2026, продолжение Supply: ReadRestockQuote теперь не меняет состояния после допуска оплаты, а новая котировка требует consumed у предыдущей заявки. ConsumeRestockResult сохраняет отдельный итог на GoalCue и освобождает только точный собственный claim после completed/rejected_before_effect; неизвестный финансовый результат не очищается. RestoreSupply повторяет только неоплаченную котировку, продолжает по сохранённому paid либо регистрирует существующий build; неподтверждённая отправка становится unknown и не оплачивается повторно. Fixture дополнен повторным загрузочным созданием Lua-модуля с сохранённым unknown/payment_sent. XML/XSD и ссылки прошли; реальная загрузка сохранения и инвентарный read-back остаются игровой приёмкой, интеграция потребностей Manager ещё не завершена.

11.10.2026: добавлены Lua-обработчики оплаты пополнения и регистрации оплаченной суммы в штатном заказе оснащения. Состояние payment_sent записывается до перевода; одинаковый ключ и незавершённая предыдущая попытка блокируют новое списание, включая неизвестный результат. Регистрация проверяет реальный BuildTaskID, корабль, поставщика, фракцию и цену; повторное событие после build_recorded не повторяет регистрацию. MD ReadRestockResult отличает отклонённую оплату, неизвестный эффект, выполняемую постройку и подтверждённое увеличение запаса после завершения заказа. Fixture supply_payment_fixture.lua подтвердил повтор события, блокировку следующей оплаты до завершения и неизвестный результат; проверка MD/XSD и ссылок прошла. Изменения остаются исходным пакетом: игровая финансовая граница, восстановление после загрузки, освобождение заявки и подключение к потребностям Manager ещё не приняты; задачи не закрыты.

11.10: TM_Empire_Supply.QuoteRestock/ReadRestockQuote соединяют MD-goal с
общим Lua quote_supply через purchase_dispatch. Перед запросом проверяются
CanUseOwnedShip, известный operational supplier с реальным shiptrader и
native canequipclass/canbuildfor; сохраняются actual ammo count, macro,
quantity, builder, manager и goal. Read повторно проверяет корабль/инвентарь
и exact quote key/assets. Цена возвращается как quoted, не разрешение эффекта.
Ни payment, ни modify build эта граница ещё не отправляет. XML/ref и общий
финансовый fixture проходят. Native paid modify/TransferredMoney/refund и
inventory delivery остаются незавершёнными; игровой приёмки и установки нет.

11.10: общий purchase_quote получил quote_supply/reprice_supply для конкретного
набора расходников, с тем же GetBuildWarePrice/RoundTotalTradePrice игрового
меню, без генерации/замены loadout. Котировка ограничена32 видами и целыми
положительными количествами; внутренний snapshot не доверяет изменённому
объекту quote, повторная цена берётся заново. Нулевая цена собственного
строителя явно requires_resources=true, не означает бесплатное оборудование.
Расширенный общий purchase_quote fixture прошёл: изменение цены, пустое/
дробное количество, чужой builder, свой builder и отсутствие generate_loadout.
Это readonly финансовая граница для restock; оплата/modify build/инвентарь
ещё не соединены и не приняты в игре.

11.10: satellite target теперь использует штатный выбор own station или
LIB_Generic.FindSectorEntryPoints. Возвращённые переходы фильтруются по isknown
и actual sector, до16 за проход; скрытый gate не задаёт приказ. Выбор кораблей
обходит до32 с сохранённым циклическим cursor, а не всегда первый префикс.
XML/ref/closure и OpenSpec проходят. Для приобретения оборудования исследован
interrupt.restock: прямой add_build_to_modify_ship может идти с price=0Cr,
поэтому resupply signal ещё не подключён без доказанного player-cost/ресурсов
и read-back. Это открытая реализация, а не принятая ветка или новая граница scope.

11.10: satellite network размещает спутник штатным DeployObjectAtPosition из
реального ammo storage своего корабля. Отдельная копия AI TM_DeployObjectAtPosition
сохраняет движение/launch, добавляет guards владения/helm/active claim и stop
interrupts, фиксирует deployment_sent до launch_satellite и observed только
по реально созданному объекту и inventory decrement. Manager выбирает до32
своих кораблей, один pending order; unknown без повтора. Штатная периодичность
сети сохраняется. Target — известная собственная станция в известном claimed
sector; поиск gate-target и приобретение отсутствующего оборудования остаются
открыты. Source closure теперь13MD+2AI, XML/ref проходят; игра не испытывалась,
новый пакет не установлен. Полная спутниковая ветка ещё не принята.

Дополнение к cleanup-аудиту: checker обнаружил ещё root Debug_* cues в
StaticDefense с бесплатным create_object, set_owner и warp чужого корабля.
Отладочные cues удалены из private closure; штатные GetStrategy/позиции/
deploy order сохраняются. Повторные checker и XML/ref проходят.

11.10: аудит прямых эффектов выявил сохранённые NPC cleanup: destroyObject
разведчиков/заказанных кораблей/неудачной станции, ownerless и убийство персонала
при Remove_Factory, искусственное разрушение и бесплатный spawn спутников.
В копии разведчик вместо удаления передаётся StopAndReleaseOwnedShip с exact
claim manager/goal и существующими guards ручных/критических приказов; прочая
фактическая собственность при cleanup сохраняется. Remove_Factory и satellite
network теперь явно ждут обычного recycling/inventory-deployment adapter,
а не выполняют NPC-обход. Это незавершённая часть полной реализации, не
исключение из критериев выпуска. Аудит manifest расширен create_object и
disposal effects; checker запрещает destroy_object/create_object/set_owner/
set_object_hull в private MD. XML/ref прошли. X4 PID61984 по текущему чтению
ещё работает со старым пакетом; новый source не установлен и не активирован.

11.10: station type request хранит весь штатный список альтернативных планов.
Перед generate_loadout и общей валидацией проверяет чертежи модулей страницами
по 32 через ReadPlanPage(ModulesOnly=true); при недоступном плане переходит к
следующему, после полного обхода ждёт 1min. Позиция/тип потребности сохраняются.
ModulesOnly применяется лишь к выбору кандидата: окончательный ReadValidatedPlan
по-прежнему проверяет все модули и сгенерированное оборудование, затем повторно
сверяет идентичность полного плана. Пересборка/XML/ref прошли. Реальный выбор
между отсутствующим и доступным планом, большие планы и изменение чертежей
при save/load ещё не проверены в игре; задачи не отмечены завершёнными.

11.10: lookup каталога модулей/планов/производственных товаров отделён от
фракции владельца. Фильтр player заменён списком фракций из category текущих
libraries/modules.xml и stations.xml, включая извлечённые DLC; Xenon/Khaak
не добавляются. Native create_factory получает этот список только в select,
owner и проверки реальной собственности остаются player. Все планы проходят
существующую проверку чертежей игрока, каталог не выдаёт доступ к ним.
Manifest хранит список и SHA 11 входных библиотек. Сборка читает каталог один
раз, без рекурсивного повторного обхода всех исходников. XML/ref прошли;
выбор доступной альтернативы при неподходящем случайном плане и реальные
lookups/loadouts ещё требуют реализации/игровой проверки.

11.10: FactionLogic_Stations сохраняет native анализ типов станций и оценку
сектора/позиции, но передаёт выбранный construction plan в собственный
TM_StationBuildRequest. Чертежи, нулевая стадия, реальная очередь и финансирование
проходят через общий Construction adapter. Прямые create_god_station,
create_station и add_build_to_expand_station из Stations удалены; макро без
construction plan отмечается причиной вместо бесплатного создания.
Pending по типу станции не увеличивает счётчик собственности; после adopted
освобождается для следующего запроса, число станций берётся из штатного обзора.
Unknown не повторяется. Пересборка/XML/ref прошли; реальные планы для player,
асинхронные cue/координаты/save-load и многократное пополнение ещё не приняты.

11.10: HoldSpace больше не создаёт high/low-tech factories отдельными прямыми
create_factory и не отправляет генератору запрос без потребителя результата.
Штатный выбор товара и production limit передаётся Econ_Manager в собственный
TM_RequestSectorFactory, который запускает существующий Request_Factory.
Один запрос sector/ware удерживается до появления станции либо завершения
неудачной задачи с выдержкой 5min. Хранится общий ActionDefinition/RequestGoal;
старый $Station очищается до отправки, чтобы предыдущий результат не выглядел
успехом текущего запроса. Нового планировщика не добавлено. XML/ref проверки
прошли; динамическая ссылка cue, engine counters и поведение при смене цели
ещё требуют общей игровой приёмки. FactionLogic_Stations остаётся открытой
отдельной строительной границей; весь Manager пока не активирован.

11.10: generated factory сохраняет native create_factory/select/compatibilities,
но фиксирует creation_sent до вызова и принимает результат только как пустую
собственную оболочку с plot/storage, без модулей и очереди. Неподтверждённая
оболочка остаётся unknown и повторно не создаётся. Prepared-план проверяется
целиком; QueueValidatedFactoryPlan ставит обычный add_build_to_expand_station
с durable queue intent и claim, затем передаёт реальный Build существующему
лицензированию/финансированию/строителю. Factory_Finalised после prepared
перевооружается для последующего finished; bookkeeping запускается после
наблюдения очереди. Проверки XML/ref прошли. В игре ещё нужно подтвердить,
что create_factory действительно возвращает пустую оболочку на этой версии,
идентичность native sequence, оплату и завершение — source не установлен.

11.10: обработчики factory destroyed/disregarded/build started/finished теперь
активируются под TM_FactoryStationObservers после появления реальной станции,
поскольку prefab-валидация предшествует её созданию. Finished требует собственную
станцию, пустую очередь строительства и действующий производственный модуль;
одного события завершения промежуточного build недостаточно. В prefab-позиции
возвращены штатные случайные yaw/Y/радиус сектора вместо фиксированного центра;
для выбранной зоны используется позиция относительно сектора. Пересборка,
XML Schema и проверка refs прошли, фактические события/save-load ещё не приняты.

11.10: prefab-фабрики сохраняют штатный выбор GOD construction plan, но теперь
проверяют весь готовый план до создания станции через RequestPlanValidation.
Станция создаётся общей CreateValidatedNativeStation с нулевой стадией и
исходным product, затем StepCreatedNativeStation сверяет реальную очередь
и передаёт её существующему финансированию/лицензии участка. Native factory
bookkeeping получает finished только после adopted с фактическим Build.
Ожидание чертежей не отменяет Request_Factory; Finalise generator вызывается
только для другой, генерируемой ветки. XML/ref проверки прошли после правки
обёртки вызова библиотеки. Реальные координаты, очередь и оплата этой ветки
ещё не проверены; generated factory и HoldSpace требуют дальнейшей адаптации.

11.10: получение купленного грузового корабля разделено на передачу claim
основной экономической задаче и подтверждение доставки. После успешной
передачи сохраняется TM_DeliveryHandedOff; повторный опрос вызывает только
AcknowledgeDelivery, без повторной выдачи приказов от завершённой задачи
покупки. ActionDefinition.Ship заполняется после accepted, при ожидании
сохраняется причина receipt. Пересборка 13 MD + private AI, проверка замыкания
и XML Schema прошли. Save/load и фактический отказ/повтор подтверждения в игре
ещё не проверены; задачи приёмки не закрыты.

11.10: owner/trueowner loss снимает только private claim и goal indexes
по событиям для OwnedClaims ships. Чужие orders/commander/commandeer не меняются;
outcome ownership_lost_execution_unconfirmed явно не означает успешную задачу.
Private deployment AI abort handler также слушает trueowner change, помимо owner.
Native ordinary orders на потерянном корабле требуют engine ownership read-back,
поэтому остановка всех действий после capture не объявлена принятой.
MD checks проходят; реальная смена владельца в игре ещё не проверена.

11.10: ReleaseStoppedMetadata снимает только private claim/index, когда
native iscommandeered=false и все tracked orders реально исчезли, без pending
submission/missing receipt. Ручная очередь/override/priority/helm/commander
не меняются; это read-back cleanup, не native release/cancel. Stop watcher
проверяет этот путь до исключения helm/manual control. Если commandeer ещё
удерживается или tracked handle существует — прежние ожидания сохраняются.
MD XSD/ссылки и adapter checks проходят; real mixed queue ещё не принят.

11.10: claim индексируется по goal и его ancestors; TransferOwnedClaim
переиндексирует, ReleaseOwnedClaim удаляет записи. RevokeGoalApprovals проходит
clone списка только отменяемой ветки, проверяет exact текущий lineage и сразу
ставит stoprequested, посылает private stop и отменяет tracked orders.
Периодический обход остаётся recovery для legacy/missing references, а не
основной остановкой. Переданный cargo отсутствует в старом request index.
MD XSD/ссылки и адаптационные guards проходят; reentrancy/cue references после
cancel, ownership change и save/load ещё требуют игровых подтверждений.

11.10: RevokeGoalApprovals отмечает exact cue отменённым до cancel.
ReadGoalLifetime проверяет goal и ancestors; CanUseOwnedShip больше не выдаёт
новые приказы из отменённой ветки. StoppedOrdersWatch (8 ships/15s) обнаруживает
missing/cancelled goal, ставит stoprequested и посылает private stop сигнал,
затем использует прежнюю exact ledger cancellation. Cargo handoff на Economy
parent предотвращает остановку delivered ship от отмены purchase child.
Синтаксис/ссылки и guards проходят; cue lifetime/save semantics и задержка
mid-child stop остаются не принятыми в игре.

11.10: cargo delivery перед завершением временного Request_Freighter передаёт
exact claim постоянному Economy parent namespace через TransferOwnedClaim.
AcknowledgeDelivery поддерживает TransferredClaimGoal и проверяет previousgoal,
current goal и manager из actual delivery receipt; cancel только при accepted.
Повтор того же handoff idempotent с CanUseOwnedShip текущего goal.
После покупки корабль не остаётся за исчезнувшим request goal. Pending ack после
неожиданной смены receipt требует дальнейшей recovery, не разрешает новое создание.
13 MD + 1 AI generation/guards/XSD проходят; actual delivery handoff не проверен.

11.10: revoke ставит exact claim.stoprequested и отменяет только tracked order
handles той же own ship, кроме helm/manual loop/override/priority и unknown claim.
Critical order получает один cancel request; после выхода из critical возможен
повтор. StoppedOrdersWatch обрабатывает до 8 ships/15s и ждёт actual order end;
CanUseOwnedShip и private AI не возобновляют stopped claim. Existing manual
orders не отменяются. ReleaseOwnedClaim пока сохраняет claim при manual queues,
смене commander/unknown/default behaviours: эти recovery cases ещё открыты.
MD XSD/ссылки проходят; critical cancellation в игре не принята.

11.10: Registry revoke/unbind перед удалением ManagerCue посылает private
TM_Empire_StopOwnedOrder только own ships с exact claim этого Manager.
Private deployment AI сверяет manager param и abort_called_scripts → finish.
Оригинальные NPC/native обычные orders этот сигнал не обслуживают; остановка
остальных ledger orders ещё требует общей lifecycle интеграции. Claims и
платежные receipts не очищаются от одного сигнала; требуется actual order end.
13 MD + 1 AI generation/guards/XSD проходят; live signal/child abort не проверен.

11.10: private deployment AI имеет event_player_started_control (param=ship)
и ownership-change handlers: abort_called_scripts → finish. Перед attention
run_script/signal_objects проверяются owned ship, отсутствие player.controlled,
живые claim manager/goal, active Registry exact manager и отсутствие unknown.
Это включает native resupply signal. Пассажирское присутствие не исключается.
Native move/resupply/deployment libs не переписаны; текущий child script может
продолжаться до interrupt, поэтому engine helm-event execution и manager-loss
mid-child behaviour остаются открытыми для проверки/дальнейшей интеграции.
AI+MD XSD проходят; изменение staged, в игре не устанавливалось.

11.10: StaticDefense shared claim/order calls используют постоянный
TM_ClaimGoal=StaticDefenseManager вместо временных handler namespace.
Request/deploy/complete events требуют exact ship claim manager/goal и strategy
mapping; request исключает player.controlled. Deploy дополнительно требует
живой own object нужного macro/sector и исключает duplicate SuccessCount.
AI nearby-object search ограничен owner=player, чужие мины не дают успех.
Native attempt/75-percent completion semantics сохранены; completed status
не означает полный ряд всех позиций. Guard execution, inventory/payment,
save/load и helm takeover ещё требуют игрового прогона. MD+AI XSD проходят.

11.10: отдельная копия native DeployStaticDefenseStrategy AI order
(TM_DeployStaticDefenseStrategy) и private TM_Empire_StaticDefense_* signals
всех adapted MD/AI. Штатные NPC handlers больше не совпадают с протоколом копии.
Native order layout/interrupts/resupply/deployment остаются; исходный AI неизменён.
Manifest фиксирует SHA исходного и нового AI; checker проверяет order ID и отсутствие
original signal literals. validate_md -IncludeNativeCopies проверяет и AI XSD.
13 MD + 1 AI остаются staged, не установлены. Реальные inventory/payment,
helm interruption и deployment receipts ещё требуют общего игрового прогона.

11.10: mission-only rigged asteroids в private Manager заменены штатной веткой
deployable mine strategy. Выбор сектора/позиции и GetStrategy/AddStrategy
сохранён; MineType=0 больше не вызывает LIB_Generic.create_object, вместо него
используется MineType=1 generic native mine strategy. NPC оригинал не изменён.
Фактическое развёртывание с inventory и native AI ещё не квалифицировано:
это удаление миссионного spawn, не доказательство полного minefield исполнения.
13-script generation/guards/XSD/ссылки проходят, установка не выполнялась.

11.10: отчёт closure теперь учитывает create_cue_actor/create_platform_actor/
assign_control_entity и внешние MD calls/signals. Прямых actor creation в копии
не найдено; InitUniverse trade manager означает controlpost.manager, уже
обрабатываемый StepPersonnel. Удалены native debug beacon creation и global
DestroyAllBeacons из адаптированной копии; result заменён null, оригиналы неизменны.
Обнаружен внешний PlaceRiggedAsteroids: LIB_Generic создаёт explosive asteroid
для миссий, не mining resource. Это ещё не адаптированная граница minefield
Manager, отдельно от native deployable inventory/orders; активация не разрешена.
Генерация, guard checks и XSD/ссылки всех 13 scripts проходят.

11.10: unknown extended plot с сохранённым after snapshot и без финансового
receipt своего key теперь может возобновить licence-only этап. Watch 15s,
эффектная попытка не чаще 1min; прежние manager/goal/queue/base/geometry checks
обязательны. Request переводится в licence_approved только после этих проверок.
Существующий payment/unknown receipt запрещает retry, extension не повторяется.
Если after snapshot не сохранён или условия изменились — остаётся unknown.
MD XSD/ссылки и прежний Lua fixture проходят; recovery watcher в игре не принят.

11.10: ResumeUnpaidPlotLicence после load проверяет exact unpaid key,
governor lifecycle, actual build/claim/queue, station/sector/position/base,
последнюю подтверждённую геометрию и budget до повторного Lua event.
Если лицензия без extension ещё не оплачивалась, изменение условий отклоняет
approval и освобождает exact plot claim. Уже выполненный extension остаётся
unknown и требует recovery; существующий платёжный receipt не перезапускается.
MD XSD/ссылки проходят. Это исходники; real save/load ещё не принят.

11.10: FundingLoaded перед возобновлением неоплаченного approved key проверяет
actual build/station/storage, exact claim manager/goal и единственную очередь
через CheckPlotConstructionBoundary. При изменении — rejected_before_payment
с причиной и ObserveConstructionFunding; платёжные receipts не сбрасываются.
Общий boundary сначала проверяет существование goal/manager/owned station/storage.
MD XSD/ссылки и Lua funding fixture проходят; реальный save/load остаётся открытым.

11.10: StepCreatedNativeStation обновляет blueprint validation параллельно
постраничной корреляции native sequence. Раньше свежесть проверялась только
после полного прохода, что для больших планов могло повторно запускать проверку.
ReadValidatedPlan теперь возвращает exact abandoned_before_effect с причиной,
а не generic waiting; factory validation polling может прекратиться на отказе.
Новая станция после отказа остаётся station_observed с причиной и не создаётся
повторно; recovery такой уже созданной станции ещё требует реализации.
XSD/ссылки и strict OpenSpec проходят; больших планов в игре ещё не проверяли.

11.10: plot quote/licence допускают non-operational native-created станцию
только с exact adopted manager/goal/build claim и единственным actual build.
MD повторно проверяет boundary перед licence approval; новый typed-флаг
newconstruction проходит dispatch и повторную проверку перед оплатой.
Расширение участка такой станции запрещено; лицензируется текущая геометрия.
Lua fixture подтверждает оплату и отсутствие replay для новой станции,
прежние проверки лицензии проходят. XSD/ссылки проходят; engine ещё не проверен.

11.10: финансирование native-created станции больше не требует operational
самой станции при exact adopted creation manager/goal/build и существующем
own expansion claim. Lua принимает newconstruction=true только из MD approval,
повторно сравнивает это поле перед оплатой; storage остаётся operational/own.
Fixture подтверждает отказ без adoption-флага, оплату новой станции, отсутствие
повторной оплаты и прежние unknown/revocation/quote проверки. XSD/ссылки проходят.
Plot request/quote/licence всё ещё требуют operational станции: следующий
необходимый шаг — аналогичная поддержка exact adopted native build в лицензии.
Это исходники, не игровая квалификация и не полное подключение factory.

11.10: prepared factory sequence подключён к RequestPlanValidation и
ReadValidatedPlan через TM_FactoryPlanValidation (15s). Key принимается только
для exact Request_Factory goal; Manager берётся из родителя этого namespace.
Проверяются все модули, без existing-station исключений. Достигнутый
blueprints_observed или abandoned_before_effect прекращает polling;
validation key сохраняется для следующего этапа queue/лицензии. Создание самой
factory всё ещё до этой проверки и не квалифицировано, поэтому это не допуск
к установке/активации. Проверки сборки и XSD/ссылок проходят.

11.10: Request_Factory_Finalised различает prepared и finished. Prepared
сохраняет constructionsequence только при совпадении station/type и сообщает
validation_pending; SpawnTime/Habitation bookkeeping не запускаются. Старый
finished требует actual expansion build той же станции/storage в queued/inprogress.
Это приём промежуточного плана, не подключённая строительная ветка: validation,
лицензия, adoption, генерация HoldSpace и actual create_factory остаются в работе.
common.xsd create_factory подтверждает default state=construction и результат
BaseSequence (может быть null); это не доказательство отсутствия engine effects.
Перегенерация 13 файлов, проверки guards и XSD/ссылок проходят.

11.10: конечный Expansion observed/abandoned_before_effect сохраняется клоном
на его живом GoalCue до освобождения общего слота. ReadExpansionResult проверяет
exact key/manager/goal и читает сначала конечный результат задания, затем активный
общий receipt. HabitationObserved переведён на этот контракт: следующий Expansion
другого задания больше не скрывает уже завершённый результат. На задании хранится
последний конечный результат; новая операция того же задания должна потребить его
до замены. Синтаксис и ссылки проверены; save/load поведение требует игрового прогона.

11.10: private FinaliseStations теперь выдаёт только native layout/loadout:
обе ветки AddBuild (очередь и немедленный apply_construction_sequence)
удалены из адаптированной копии. Сигнал результата — prepared с sequence,
null build и исходной станцией, а не finished. Это промежуточный контракт:
HoldSpace без ReportCue и экономика ещё требуют подключения к проверке
чертежей/оплаты и подтверждению реального строительства; копия не активирована.
Генератор адаптации, проверка 13 файлов и XSD/семантические ссылки проходят.
Отчёт границ теперь включает create_factory и отдельные строительные эффекты,
которые прежде не попадали в полный список оставшейся адаптации.

11.10: перед create сохранён immutable список entry ID/macro/stage/equipment из
проверенного плана. StepCreatedNativeStation сверяет фактический sequence с этим
снимком по 32 записи за проход; accepted Expansion использует фактический sequence,
а не исходную ссылку. Изменение sequence сбрасывает курсор; mismatch переводит
creation в unknown без повторного создания. После load корреляция начинается
сначала. В BuildStation до эффекта разрешено повторить abandoned validation,
но сохранённое creation_sent/unknown никогда не вызывает повторного create.
Для staged-prefab subset/замены entry ID engine semantics ещё не квалифицированы;
военная flat-plan ветка требует общей игровой проверки, экономика не подключена.

11.10: copied FactionSubgoal_BuildStation подключён к RequestPlanValidation →
CreateValidatedNativeStation → StepCreatedNativeStation. Штатные цель/место/
макро/план/генерация loadout сохранены, прямые create_station/add_build удалены
только из адаптированной копии. 15-секундная дочерняя проверка ждёт полные
blueprints, станцию/задачу/план, после adopted возобновляет штатный Station_Management
и Evaluate. До adopted оценка preparing вместо ложного failed из-за null станции.
Сборка/XSD/source checks проходят; game qualification и корреляция copied sequence
пока отсутствуют. Factory/prefab callers и FinaliseStations эффекты ещё открыты.

11.10: CreateValidatedNativeStation использует штатный create_station с state=
construction и проверенным полным планом. До эффекта сохраняет creation_sent на
точной цели и в Creation.$Receipt; повтор или новая цель при непринятом результате
не создают вторую станцию. После подтверждения владельца/сектора/plot/storage
записывает provenance на станции и реальный Build из queued/inprogress.
AdoptNativeStationBuild помечает provenance adopted после принятия очереди.
Связь копий таблиц/идентичность engine sequence после create ещё требуют пробы;
поэтому helpers пока не подключены к native callers и не установлены в игру.
Остаются ожидание плана/задачи, восстановление orphan и адаптация штатных callers.

11.10: RequestPlotChange принимает необязательный Build для лицензии уже
созданной станции. CheckPlotConstructionBoundary проверяет ту же цель/Manager/
claim/единственную queued или inprogress задачу и повторяет проверку после quote;
при Build расширение plot запрещено. StepQueuedExpansion для nativecreation
запрашивает обычную лицензию и ждёт подтверждения, затем однократно учитывает её
платёж по ключу в spent общего бюджета перед финансированием материалов.
Обычные expansion-вызовы без Build по-прежнему требуют пустую очередь. XML и
существующий Lua plot-fixture проходят; actual nativecreation caller и игровая
приёмка этой связи остаются открытыми. Поведение пустой станции/isoperational
требует read-back, не разрешено обходить guard без доказательства.

11.10: AdoptNativeStationBuild принимает уже созданную штатную очередь без
повторного add_build. Требует точную creation provenance (Manager/Goal/PlanKey/
Build), единственную задачу queued или inprogress, владельца игрока, валидированный
полный план и корреляцию native plannedconstruction.sequence. Создаёт обычную
Expansion/claim квитанцию для общего сопровождения; повтор возвращает тот же ключ.
Перед финансированием/назначением строителя StepQueuedExpansion теперь проверяет
оплаченную лицензию участка. Принятие ещё не вызывается production-ветками:
creation wrapper, корреляция копии плана и лицензирование queued-станции остаются
открытыми. XSD/OpenSpec проходят, новых игровых эффектов этот helper не выполнял.

11.10: station-v3.json — реальная DOU-267 игрока, сразу после create_station:
modules.all=0, queued=1, inprogress=0, expansion=1, buildobject=созданная станция,
plot.max=(5000,5000,5000)m, paidplot отсутствует, buildstorage существует;
player.money до/после7243185300 (MD-единицы). Немедленный plannedconstruction.sequence
ещё null и вызвал property warning: нельзя считать этот план синхронно доступным.
station-v3-repeat.json возвращает ту же DOU-267 без второго создания; позднее
modules.all=1, plan=15, queued=0/inprogress=1, wantedmoney598562600, деньги игрока
не изменились. modules.all не доказывает operational: природа первого компонента
и требование CV/ресурсов требуют следующего read-back. Создание базовой станции/
неоплаченного участка/реальной очереди подтверждено; завершение не подтверждено.
Подключение новых станций должно искать queued И inprogress, ждать фактического
плана и связывать его с той же станцией, не резервировать второй участок.

11.10: замыкание копии расширено до 13 файлов: добавлены только необходимые
FinaliseStations библиотеки и адресный cue-signal endpoint. Автоматические
GOD/NPC-события и обновление соседних станций исключены. Все ссылки экономических
и военных целей переведены в частный namespace; include-actions расчётов
жилых модулей/доков/обороны сохраняют штатный алгоритм. Проверки ссылок, hashes,
исходников и XSD проходят. Эффекты этой библиотеки ещё требуют адаптации,
пакет не установлен и Manager не активирован.
Диагностическая station-проба теперь использует фиксированный штатный plan ID
arg_advancedcomposites_prefab_04 из constructionplans.xml, исключая GOD selection
из теста construction semantics. MD hash24DD2AE2C5FF2FB9DE88BF481E3DC621C44BCC2A269F85741F9697E05C735093;
свежая X4 PID61984, клиент load-save004-v3/session86674 пока ожидает соединение.

11.10: второй игровой station-v2.json подтвердил native_plan_unavailable/type=null,
создания снова не было. Проверен libraries/god.xml: arg_energycells — product с
динамическим factory/select, а не prefab station; у arg_advancedcomposites есть
реальный constructionplan arg_advancedcomposites_prefab_04. Диагностическая
проба переведена на advancedcomposites. Предыдущее предположение, что виноват
только фильтр space, оказалось недостаточным. PID148444 жив, сохранение загружено;
новая версия MD ещё не прочитана процессом, следующая проба требует свежего запуска.

11.10, 02:29: предыдущая тестовая X4 PID138900 остановлена, свежий Steam-запуск
подтверждён PID148444. Исправленная диагностическая MD SHA256
4F6C0350950FA350F4DB6EE00815FC3F49888CB4CCBF7B4C3DC26A0B895B7A4A.
Клиент load-save004-v2 ожидает tm_empire_save_menu, exec session63174 live;
не запускать второй клиент/игру до проверки этой сессии. Первое создание не
выполнялось: нет записанного issued, native_plan_unavailable был pre-effect.

11.10: PID138900 загрузил save_004, read-back role-before.json подтверждает
2 станции/67 кораблей, прежнего сотрудника и неизменного менеджера станции.
station-first.json: native_plan_unavailable, до issued/create_station не дошло.
Schema get_god_production_construction_plan подтверждает: space фильтрует GOD
entry по месту; HQ не обязана подходить аргонскому prefab. В диагностической
пробе фильтр места убран (решения production Manager не изменены), к отказу
добавлен typeof результата. Исправленная проба требует загрузки свежего MD.

11.10, 02:24: диагностическая MD/Lua-копия установлена; MD SHA256
3BF21E0E5486F41E8A16EA257BEFB8D35C8EB2717E300106D1F854FE3FB847C1,
Lua SHA256 16C1EE590FF6BB428AA079F338B46B28047D8A0F950825CBA2DBA39359765CF9.
X4 через Steam реально запущена под COMP/Avalakh, PID138900. Песочница работает
как COMP/CodexSandboxOffline: обычный вызов Steam не запускал игру, клиент не
имел pywin32. Через разрешённый elevated execution запуск подтверждён Steam-log;
pywin32 установлен только в .cache/tmp/station-boundary-20261011/python-deps.
Клиент saves ожидает соединение, exec session5068 ещё live. Под владельцем игры
X4 пока Responding=false, CPU~13s, startup-log остановлен на 02:24:35; нет
ответа pipes и нет принятого station_fixture. Не перезапускать только из-за
таймаута наблюдения: сначала повторно проверить PID/session и журнал.

11.10: в общий диагностический pipe-клиент добавлен station_fixture, для
адресной проверки неизвестной create_station(state=construction)/stage=1 границы.
Одна фактическая станция по штатному energycells-плану; никаких process_build,
материалов, денег, готовых модулей или сотрудников. Перед эффектом сохранён
issued; повторы только read-back той же станции/очереди/plot/storage/баланса.
MD schema и scheduling проходят. Проба ещё не установлена/исполнена, X4 остановлена;
это подготовка испытания, не свидетельство игрового поведения или завершённая задача.

11.10: проверена точная семантика create_station/stage в common.xsd. Для
state=construction движок создаёт станцию без модулей и добавляет build task;
предположение о готовом бесплатном prefab-модуле не подтверждается. process_build
означает начало обработки очереди, не доказанный обход материалов. Для дальнейшей
адаптации предпочтительна проверка уже штатного construction пути и его plot/
buildstorage, затем минимальное подключение лицензии/финансирования/строителя.
reserve_build_plot в MD также найден, но его API не определяет размер по плану.
Не требуется переписывать штатный prefab только из-за наличия create_station.

11.10: reserve-подтверждение дополнительно сравнивает GetObjectPositionInSector
с фактически переданной C-структурой UIPosRot. Несовпадение позиции сохраняет
unknown без повторного создания; fixture покрывает этот случай. MD observer
отзывает approved без записи эффекта при потере цели/активной привязки, даже
если цель исчезла через onfail без явного cancel_cue. Выбор размера участка для
готовых планов пока открыт: MD constructionsequence не раскрывает координаты
модулей и bounding box. Нужен штатный планировочный API/генератор, а не выдуманный
размер по количеству модулей; callers ещё не подключены.

11.10: результат резервирования удерживается в observed до явного ACK той же
целью/Manager/ключом/станцией; следующая заявка не затирает ожидающий результат.
ReadReservedStationPlot проверяет принадлежность квитанции и сохранность станции.
StationPlotLoaded восстанавливает только approved без квитанции эффекта и с
живой активной целью; reservation_sent/unknown не повторяются. Fixture теперь
исполняет зарегистрированный MD↔Lua dispatcher и проверяет изменение геометрии
между чтением заявки и последней проверкой разрешения. MD load/ACK в игре ещё
не квалифицированы, штатные callers пока не подключены.

11.10: RequestStationPlot связывает MD-цель/Manager с reserve-модулем через
типизированную BB-заявку. Штатный get_safe_pos учитывает существующие plotbox и
радиус суммы полуразмеров, покрывающий весь участок; Lua повторно сравнивает точную геометрию/сектор/ключ.
ObserveStationPlot подтверждает реальную станцию игрока с buildplot/buildstorage,
отмечает квитанцию reconciled; unknown не создаёт участок повторно. Отзыв binding
и явная отмена цели отзывают разрешение. Координаты MD↔C, гонка размещения между
get_safe_pos и ReserveBuildPlot, а также штатные callers остаются неподтверждёнными;
адаптированный Manager пока не активирован.

11.10: construction_reserve.lua реализует обычный ReserveBuildPlot для пустого
участка игрока: валидирует числовую геометрию, проверяет разрешение вызывающей
стороны, сохраняет reservation_sent до эффекта, возвращает фактический station,
проверяет владельца/сектор/размер и не повторяет unknown или тот же ключ.
Lua-fixture покрывает отмену, успех, повтор, блокировку предыдущей квитанцией,
несовпадение размера и потерянный ответ. Это вспомогательный модуль: штатные
ветки создания станций пока не переведены на него; игровая квалификация отсутствует.

11.10: TM_PersonnelGoal теперь постоянный namespace внутри копии Manager;
30-секундный TM_PersonnelTick сбрасывает только себя и передаёт в операции
родительскую цель. Квитанции найма/перемещения и курсоры обхода больше не
ссылаются на сбрасываемый таймер. Проверка сборки контролирует эту структуру.
Нулевой бюджет разрешён для штатного бесплатного найма; Lua-fixture проверяет
нулевую цену, отсутствие списания и защиту от повторного исполнения. Реальное
исполнение/загрузка остаются частью общей игровой приёмки.

11.10: адаптер перед каждым cancel_cue вызывает RevokeGoalApprovals.
По точному ключу заявки и цепочке родительских cue отзываются только ожидающие
разрешения покупки, найма, финансирования строительства и лицензии участка.
Финансовые квитанции и реальные заказы/строительство сохраняются. Проверки
покрывают наличие и порядок hook во всех 12 копиях; исполнение MD и гонка
с Lua требуют общей игровой приёмки. Исходные штатные скрипты не изменены.
Общий перехват reset_cue удалён: периодический тик персонала может одновременно
выдать заявку и сбросить свой cue. Это требует отдельного сохранения жизненного
цикла цели персонала, а не отзыва всех разрешений при каждом тике.

11.10: Habitation_Helper использует общий BeginExpansionGeneration и
AcceptGeneratedExpansion вместо прямого добавления плана. Штатный расчёт
необходимых жилых модулей сохранён. Цель живёт до подтверждения построенных
модулей или отказа до постановки плана; load освобождает только незавершённую
генерацию, сохраняя уже принятый план. При отказе станция возвращается в штатную
группу ожидания. Ветки prefab/new station ещё требуют адаптации; пакет не установлен.

11.10: plot extension/licence подключены к dynamic Request_Production_Module.
Сохранён штатный threshold заполненности/размера и symmetric1km X/Z,0.5km Y.
RequestPlotChange удерживает station/manager/goal/key claim и MD snapshot
plot/sector/position/base/queue ДО readonly Lua quote. Quote использует native
GetBuildPlotPrice/Payment и C GetBuildPlotSize, не пересчитывает налог. После
quote_ready CommitQuotedPlot сверяет lifecycle, неизменную геометрию/очередь,
owner/budget; свежий can_safely_extend_build_plot непосредственно перед native
extend_build_plot и persisted extension_sent. Затем normal TransferPlayerMoneyTo
sector controlstation + PayBuildPlotSize через существующий plot helper;
actual size/center/price/credit должны совпасть с quote до финансового эффекта.
MD и Lua bookends используют каждый свои native координаты, без предположения
о коэффициенте между MD buildplot.max и C GetBuildPlotSize.

Free licence rule взят из Helper.getPlotData13806–13833: player-owned,
ownerless и xenon sectors не требуют перевода владельцу; geometry licence
записывается обычным PayBuildPlotSize. ReadPlotLicence учитывает это правило,
но по-прежнему проверяет actual paid bounds/center. Dynamic goal ждёт
TM_PlotReady5s и только после observed/rejected-before-effect запускает native
sequence generation; в rejected случае возможна попытка в старом участке,
как у штатного алгоритма при невозможном расширении. Недостающая обычная
лицензия существующего участка также проходит этот путь с Extend=false.
Unknown после geometry/payment не повторяет эффект. On-load plot ожидание
сохраняет тот же goal/key, а не перезапускает всю генерацию; PlotLoaded может
повторить readonly quote или потерянную delivery licence_approved без same-key
financial receipt. Binding loss и observer lifecycle guard отзывают approved
запросы, sent/unknown финансовая история не удаляется.

Проверки: расширен existing construction_plot_fixture — normal credit/pay,
partial/no retry, changed/missing geometry, read-only extension quote, actual
expected size requirement, free ownerless/xenon/player licence без денег,
registered quote→MD-boundary-mock→licence/replay/revoked bridge; Lua5.1 PASS.
XSD/scheduling всех MD и refs/hash12-copy audit PASS; originals unchanged.
При проверке исправлена промежуточная ошибка генератора: conditional reset
теперь только у TM_PlotReady; poll static defense восстановлен и не ссылается
на TM_WaitPlot. Source не установлен и native ABI/MD event flow/geometry
effect/paid licence ещё НЕ приняты в игре; это не закрывает3.4 или release.
Остаются habitat/prefab/новые станции/чужой builder, parallel station requests,
доказанный немедленный отзыв UI approval при отмене goal, unknown/cancel/orphan
reconciliation и общий gameplay пакет. Progress5/32, goal остаётся active.

11.10: динамическая ветка Request_Production_Module в адаптированном Economy
подключена к TM_Empire_Construction. BeginExpansionGeneration проверяет active
manager/goal, свою operational станцию, свободную очередь/claim и точную paid
plot geometry; штатный asynchronous create_construction_sequence ограничен её
участком. AcceptGeneratedExpansion принимает именно native event/object/sequence
с тем же generation claim. Порционная blueprint/identity validation предшествует
QueueValidatedExpansion; изменения base plan/plot/manual queue/lifecycle отменяют
только ещё не выданный запрос. Persisted queue_sent и station manager/goal/build
claim сохраняются ДО native add_build_to_expand_station; его реальный Build
проверяется по Station/buildstorage. Не добавляются ресурсы, модули или build speed.
Старая NPC extend_build_plot в этой ветке заменена отметкой потребности до
подключения настоящего платного extension/licence adapter; требование расширения
участка остаётся открытым. Native aborted-on-load/failure освобождает только
неприменённый generation claim той же цели.

ApproveConstructionFunding использует реальный Storage.wantedmoney — штатный
остаточный ресурсный бюджет, включая оборудование, вместо собственного расчёта.
ui/construction_funding.lua повторяет StationConfiguration.buttonSetMoneyToEstimate:
обычный TransferPlayerMoneyTo на собственный склад, положительный дефицит без
изъятия существующих средств; проверка текущей native quote/account/approval,
receipt payment_sent ДО оплаты, exact debit+credit read-back. Unknown/payment_sent
не повторяются; governor loss отзывает только approved запрос. FundingLoaded
может повторить лишь потерянную доставку того же approved запроса без его
финансового receipt. Повторный расход учитывается cumulative spent в лимите
исходного Budget; native missing resources/processing публикуются в receipt.
StepQueuedExpansion проверяет по32 реальных planmodule IDs, выдаёт guarded
DeployToStation своему строителю порциями по8; отсутствие бюджета/строителя
имеет backoff1min. Завершение означает наблюдавшиеся настоящие operational
модули, а не оплату/готовый план. Регистрация funding UI добавлена.

Проверки: Lua5.1 construction_funding_fixture — debit/credit, zero top-up,
same-key/unreconciled/after-load replay, money/cap, quote change, lost operational
asset, revoked approval, partial credit→unknown/no retry; PASS. XSD/scheduling
всех production/diagnostic/raw/adapted MD, 12-script refs/hash guards и strict
OpenSpec — PASS. Source не установлен, X4 остановлена; native properties/event
context/sequence identity/account timing и фактическое строительство НЕ приняты
в игре. Это частичная подключённая ветка, не завершённая3.4 и не релиз;5/32.
Остались habitat/prefab/новые станции/plot extension+licence/чужой builder,
параллельные station requests (Expansion пока single receipt до delivery),
unknown/cancel/orphan reconciliation и пакетная игровая приёмка. Не включать
остальные ещё сырые create_station/build ветки ради этой частичной проверки.

11.10: RequestOwnedBuilder добавлен в construction adapter: только реальный
expansion Build на своей Station/buildstorage, exact goal/manager/build claim,
own idle purpose.build ship через общие CanUse/Claim guards. Persisted deployment
receipt и issuing flag до native DeployToStation; actual Order записан общим
RecordOwnedOrder. ObserveOwnedBuilder требует tracked running Order/station,
own claim и взаимное фактическое constructionmodule/constructionvessel с
isdeployedconstructionvessel; helm исключён. Watch15s не отправляет приказ
повторно, ended/timeout10min→unknown. Native source order.build.deploy.xml,
MapMenu.selectCV/orderDeployToStation3490–3524; чужой наём оплачивается отдельным
native GetBuilderHiringFee, ещё не адаптирован. Resources source найден:
StationConfiguration.refreshPlan3428→PrepareBuildSequenceResources2(map,
container,true)/GetBuildSequenceResources, включает native loadout quantities.
XSD/scheduling проходят. Нового queue caller/owned build claim writer пока нет;
это staged helper без игровой приёмки,3.4 не закрыта.

11.10: plan validation сохраняет entry id/macro/stage и clone equipment ware
list каждой успешно проверенной страницы. После blueprints scan отдельный
checking_identity проход32 entries сверяет весь набор; same-count module/
stage/equipment change даёт abandoned_before_effect. blueprints_observed
выставляется после второго полного прохода. Load/freshness reset очищает
snapshot и cursor согласованно. XSD/scheduling проходят. Это проверка публичных
MD identity полей, не полной geometry/loadout quantities: native construction
quote/placement boundary ещё должна подтвердить позиции, соединения и точные
количества перед эффектом. Caller/runtime gameplay отсутствует;3.4 открыта,
source не установлен. Следующая часть — native geometry/resource/builder path.

11.10: construction validation объединена в сохраняемый Request/key с
Manager/Goal/Sequence. Watch5s проверяет ровно32 entries, на missing blueprint
backoff1min; полный blueprint receipt только при непрерывном checked==total.
До любого эффекта утрата lifecycle даёт abandoned_before_effect. ReadValidatedPlan
проверяет exact key/manager/goal, active binding, whole count и freshness1min.
Game load начинает проверку снова только в доэффектных validation states,
не выдаёт сохранённый результат за актуальный и не повторяет финансовых effects.
Состояние blueprints_observed означает только доступ чертежей, не готовность
строительства. Mutable same-count sequence/loadout identity, geometric fit,
resources/builder и native goal caller ещё требуют завершения. XSD/scheduling
проходят. Source не установлен;3.4 и release по-прежнему открыты.

11.10: construction_plot.lua реализует обычную licence существующего plot
по MapMenu.buttonBuyPlot: GetBuildPlotPrice минус GetBuildPlotPayment,
TransferPlayerMoneyTo sector controlstation и PayBuildPlotSize. Own/operational,
native size/center/position-changed и lifecycle проверяются до эффекта.
Durable receipt сохраняется перед payment/licence; exact-key/unreconciled
исключает повтор. Read-back требует current paid size/center/payment; несовпадение
или partial payment даёт unknown, не повторную оплату. Plain module пока без
MD caller/event: не выбирает участок, не резервирует новый и не строит модули.
Lua5.1 construction_plot_fixture проходит success/credit, key replay, money,
revoked, foreign, partial payment/no retry, unconfirmed licence/no retry.
Native boundary mocked; фактическая цена/licence в игре ещё не принята.
Placement validity найден как IsCurrentBuildMapPlotValid(holomap); независимая
геометрия нового ReserveBuildPlot и full construction queue требуют продолжения.
Source не установлен,3.4 и общий release остаются открытыми.

11.10: начата native station construction boundary. Найден обычный путь
MapMenu selectbuildlocation27418–27429: ReserveBuildPlot + PayBuildPlotSize;
buttonBuyPlot4260–4277 отдельно переводит licence price sector controlstation.
Создание через NPC create_station не признано допустимым player adapter.
Добавлен tm_empire_construction.xml: ReadPlanPage проверяет по32 entries
constructionsequence, owned module/equipment blueprints, возвращает точный
диапазон/missing/next и никогда не объявляет проверенной всю непрочитанную
sequence. ReadExpansionPrerequisites читает собственный buildstorage, текущую
оплаченную licence, существующую очередь, account и requiresconstructionvessel.
Оба helper read-only; геометрия/ресурсная quote, plot/payment adapter, builder
и присоединение к native station goals ещё не реализованы. XSD/scheduling
проходят.3.4 остаётся открыта; source в игру не переустановлен.

11.10: station training demand подключён к кадровой цели. Native range
источник order.trade.routine.xml17–35/154/242: max(manager management,
pilot piloting)/3. ReadStationSkillNeed читает собственный production deficit,
реальные trade subordinates/cargo и known dock-access sell offers, доступные
по station account. Выбирает ближайшего доступного поставщика после всего
наблюдаемого набора; обучение не выдаётся за решение, если рядом уже есть
альтернатива или пилот обеспечивает дальность. More32 offers/carriers не
дают доказанного training need; partial observation не считается отсутствием.
Demand содержит ware/supplier/distance/skill/time, затем расход native seminar.
Это не причинная оценка менеджера: trade rules/блокировки и исполнение после
обучения ещё требуют общего игрового прогона. Исправлен inventory refresh:
cursor сохраняется при10min refresh, иначе империя>20 assets никогда не
доходила до хвоста; person cursor map очищается от потерянных assets.
XSD/scheduling проходят; staged source, все игровые критерии остаются открыты.

11.10: кадровый caller TM_PersonnelGoal добавлен внутри copied Manager,
StepPersonnel вызывается каждые30s; отдельного верхнего управляющего нет.
Native own inventory refresh ограничен10min, один asset на проход. Выявляет
free manager/shiptrader/aipilot posts, сначала native transfer своих people,
затем native paid hire из known dock-access stations/remotecommable NPC.
Source round и person cursors вращают порции32/16 без вечного первых32;
ограниченная порция без кандидата явно не означает отсутствие во всей игре.
Обучение пилота инициируется требованием real tracked native order.requiredskill,
через seminar adapter; cap piloting при недостатке combinedskill даёт native
experience waiting, не произвольное изменение морали/звёзд. Station management
training demand, UI projection и финансовые orphan cases ещё не завершены.
Сборка/ref/hash/XSD/scheduling проходят; caller staged, Manager не активирован
и игровой кадровый цикл ещё не принят.4.1–4.4 остаются открытыми.

11.10: добавлен платный native hire путь RequestHire→personnel_hire.lua→
AssignPaidHire→ObserveHire. Только доступный remotecommable hirable NPC без
занятого поста/mission, known station и native assignment check. Lua повторяет
MapMenu fee+discount calculation и TransferPlayerMoneyTo; durable payment
receipt сохраняется до эффекта. Exact-key и unreconciled запрещают повторную
оплату; native нулевая цена/скидка допустима, NPC spawn отсутствует. Governor
binding loss отзывает approval. Assignment intent записывается до native
assign_hired_actor; observed требует native paid receipt и exact employee/seed
на нужном посту без transit. HireWatch15s сверяет, payment не повторяет.
Lua5.1 personnel_hire_fixture проверяет скидку/успех, duplicate/unreconciled,
fee change, no money, revoked, partial payment→unknown без retry; проходит.
MD XSD/scheduling проходят. Кадровый caller ещё не подключён, paid orphan/
refund recovery и игровые сценарии не приняты:4.1–4.4 остаются открытыми.
Изменения source не переустановлены в игру.

11.10: RequestSeminar в personnel adapter повторяет native Conversations
g_seminar tier selection и операции: inventory seminar соответствующего
piloting/management, +3 points с cap15, entity/template вариант по наличию
roleentity. Требует действующего governor/goal, own arrived person и реальной
недостающей квалификации. До эффекта сохраняет exact skill/inventory receipt;
observed требует одновременно фактический skill и расход ровно одного item.
Unknown запрещает повторный расход; TrainingWatch15s только читает результат.
Перевод и обучение одного человека взаимно блокируют sent/unknown.
XSD/scheduling проходят. Source boundary: native conversations.xml853–1003;
платный наём: menu_map.buttonHire4125 использует HiringFee, native payment и
AssignHiredActor (не бесплатное создание). Caller кадровых целей и платный
hire ещё впереди;4.3 не закрыта без gameplay/read-back. Source не установлен.

11.10: добавлен production tm_empire_personnel.xml: RequestTransfer вызывает
штатный assign_hired_actor для существующего player people template и свободного
controlpost. Проверяет действующий governor/goal, ownership/operational,
player helm, native capacity/assignment check, transit/busy/mission/temporary,
защищает governor и уже занятые человеком посты, в том числе без roleentity.
Intent сохраняется до native effect; rejected/sent/unknown/observed различены.
ObserveTransfer подтверждает exact template/post/employee, фактическое
прибытие и прекращение source membership. Watch15s наблюдает unknown без
повторной отправки; timeout10min не считается успехом. XSD/scheduling проходят.
Пока нет caller из Manager personnel goal, платного hire/training adapter и
игрового read-back:4.1–4.4 остаются открытыми. Мод в игру не переустановлен.

11.10: native shortage processor теперь читает подробные production/cargo
reports только у собственных assets/build storage, а buy/sell search требует
native tradesknownto=faction.player. Убраны два скрытых InitUniverse create
personnel эффекта из экономического наблюдения: отсутствие tradenpc/shiptrader
фиксируется как vacancy_requires_native_hire на объекте. При фактическом
появлении соответствующего actor запись вакансии очищается. Это вход для
ещё не завершённого personnel adapter, не реализация найма и не основание
закрывать4.1. Воспроизводимая сборка12 скриптов/ref/hash/XSD проходит;
изменения остаются staged и не квалифицированы игровым read-back.

11.10: добавлено восстановление acquisition после event_game_loaded с delay5s.
Без финансового receipt и native build сохранённые quote_requested/quote_ready/
approved пересчитывают оснащение и повторно проходят ApprovePurchase. Receipt
того же key запрещает повторную оплату/build: built запускает correlation и
delivery reconcile, reconciled завершает MD delivery общей библиотекой даже
при потерянном UI event. Unknown/payment_sent остаются ожидающими сверки.
Lua dedup хранит один последний key вместо растущей таблицы; сохранённый
reconciled receipt также запрещает повторное использование того же key.
purchase_submit_fixture и полный MD XSD/scheduling проходят. Save/load в игре
ещё не проверен; source не установлен, критерии change остаются открытыми.

11.10: поиски adapted native ships/stations ограничены known; чужие ships
дополнительно isinliveview. Собственные $Faction/player ships остаются
доступны вдали от игрока. Все12 копий проходят ref/guard/hash и XSD checks.
Это ограничение поисков, не полная приёмка видимости: чтение скрытых
инвентарей/фракционных агрегатов и длительное использование наблюдений
по-прежнему требуют адаптации.

11.10: из adapted Manager убраны Ship_Construction_Manager и
Fleet_Evolution_Checker — обращения к NPC Job_Helper. Первый собирал
disconnected jobs и добавлял0Cr build на чужой верфи; второе меняло
global job active для NPC fleetphase. Для player это не развитие реального
флота и не может запускаться параллельно normal purchases. Native economic/
military demand и class/strength selection сохранены; scope флота не снят.
Raw Job_Helper остаётся provenance reference/staged unqualified, ни одной
active ссылки из Manager к нему нет. Пересборка/ref/hash/XSD проходят.

11.10: общий purchase_submit_fixture выполнен Lua5.1 текущей игры без
запуска X4. Сценарии: успешная native payment/build/record последовательность,
отказ другого заказа при unreconciled, exact build ID match и чужой faction,
нет денег без effects, lifecycle loss перед оплатой без effects, build0
после оплаты→unknown без повторной оплаты, частичный баланс→unknown без
build/retry. Blackboard копируется по значению; счётчики effects проверены.
Ранее принятые quote/receipt fixtures также прошли общий acquisition пакет.
Это mocked native boundary, не gameplay/read-back или подтверждение full
Manager; все обязательные игровые критерии остаются открытыми.

11.10: исправлен catalogue filter для player-owned верфи: ship definitions
не фильтруются faction.player (у игрока нет NPC library category), а native
player build wares определяют точный доступ/blueprint. Ограничение64
применяется к доступным уникальным models, а не первым64 definitions, чтобы
порядок рас/модов не создавал ложное отсутствие. Перебор конечного static
catalog сохраняет classes/tags, все динамические yards по-прежнему known и
до32. XSD проходит; длительность в игре и доступная quote не подтверждены.

11.10: AssignCommander сохраняет exact native handle/параметр commander в
claim.assignment, проверяет owned destination перед эффектом; Runtime
ObserveOwnedCommander/event_object_commander_set/order-ended принимает
фактическое назначение только при tracked intent, своём ship и отсутствии
чужих orders/helm. Обновляется только собственный ledger, commander не
перезаписывается. Economy priority completion требует observed commander,
не только sent order; немедленное native изменение проверяется после
RecordOwnedOrder. Пересборка/ref/hash проходят; native runtime ещё не принят.

11.10: экономический post-purchase порядок разбит на одноразовые native
steps: каждый routine/AssignCommander сохраняет свой sent/unknown receipt
и handle;15s poll повторяет только шаг, до эффекта которого guard отказал.
Уже выданная routine не создаётся снова, если назначение станции ждёт.
Success требует подходящую routine и, при priority container, отдельный
AssignCommander receipt; устаревший общий $TM_OrderReceipt не засчитывается.
Пересборка/XSD/ref/hash проходят; commander actual read-back/unknown и
длительное выполнение остаются в пакете интеграции и игровой приёмки.

11.10: Economy.Request_Freighter использует native cargo categories
miner/transporttag, tug или trader/transporttag на доступных верфях и общий
Prepare/Complete/15s poll. После ready перенесены оригинальные MiningRoutine/
SalvageRoutine/TradeRoutine params; приоритетный AssignCommander сохранён
через общий effect guard. ActionDefinition.Ship фиксируется после receipt,
delivery ack затем cancel request; предоплатный отказ закрывает watcher с
причиной. NPC requested ship events/timeout/spawn удалены из этой ветки.
Пересборка/XSD/ref/hash проходят; комплект mining/tug, повтор частично
выданных orders и actual runtime необходимо проверить/согласовать.

11.10: OrphanPurchaseWatch15s согласует готовый оплаченный exact build,
если requesting Goal закончилась, не назначая приказ/commander/claim;
корабль остаётся player property, результат orphaned_ready сохраняет причину.
После уже выполненной доставки исчезнувшая Goal освобождает только свой
claim через общий безопасный Release; live orders/manual/helm/unknown
сохраняют ожидание, утрата собственности фиксируется без изменения чужого
корабля. XSD проходит; cancelled/refund/unknown и save/load ещё не приняты.

11.10: устранено окно потери delivery между Lua reconcile и15s native goal
poll. PreparePurchase и анализ acquisition блокируются до AcknowledgeDelivery
последнего delivered result. Ack требует exact key/живой goal/owned ship и
тот же claim; Recon/Defend подтверждают после включения в native task,
StaticDefense после native order receipt sent. Другой заказ не перезапишет
непрочитанный результат. Generator/XSD/ref/hash проходят. Утрата получателя/
order unknown и игровой прогон остаются частью lifecycle приёмки, не закрыты.

11.10: StaticDefense.CreateJobShips теперь сохраняет native quota3M/2S,
ищет military M (fallbackS)/S, PreparePurchase c Goal=StaticDefenseManager,
без NPC request/activate_job_ship_orders.15s PurchasedEngineerObserved
получает reconciled ship, выпускает guarded DeployStaticDefenseStrategy
(isminesonly дляS), добавляет в engineers group только при native receipt
sent; last key фиксируется после успеха, manual/unknown не дают ложный
успех. Пересборка/ref/hash/XSD проходят. Native resupply и долгие order
helm/manual guards ещё требуют аудита; runtime не активирован.

11.10: полный поиск consumers Get_Scout/Military/Suitable_Jobs в raw closure
подтвердил только Recon/DefendArea для изменённого selector payload. Оба
адаптированы, проверка требует отсутствие request_job_ship и наличие
Prepare/Complete/15s poll. Acquisition analysis пропускается при общем
pending/backoff, перебор вариантов прекращается после первого принятого
заказа. Прежняя заметка об «остальных consumers Suitable_Jobs» ниже уточнена:
других нет; отдельные staticdefense/economy jobs и Job_Helper ещё требуют
собственной адаптации. Пересборка/XSD/ref/hash проходят; игра не запускалась.

11.10: Recon/DefendArea Request_Job_Ship заменены PreparePurchase по
option[macro,shipyard], без request_job_ship/disconnected job component.
Проверка15s наблюдает exact key и CompletePurchase, после reconciled delivery
добавляет реальный ship в native group/strength и вызывает Set_Ship_Order.
Ожидаемая сила до готовности не начисляется; pending защищён общим purchase
слотом. XSD/ref/hash замыкания проходят. Остальные consumers Suitable_Jobs
и бюджет/активация/игровая приёмка ещё открыты; staged не установлен.

11.10: native Get_Suitable_Jobs_Lib сохраняет алгоритм points/class/tier/
random selection, заменены только get_suitable_job на ReadPurchaseOptions:
до32 известных верфей и64 доступных macro/yard options, native category tags
без NPC factionlogic. **Изменён внутренний payload Suitable_Jobs: теперь
table[macro,shipyard], не job ID.** Downstream Request_Job_Ship/прочие callers
ещё требуют адаптации и не могут быть активированы в этом промежуточном
состоянии. Generator/ref/hash/XSD проходят; этот статический результат не
подтверждает исполнение приобретения. Исходные NPC файлы не изменены.

11.10: выявлен native acquisition seam: Request_Job_Ship возвращает
непостроенный NPC job component; этот объект нельзя считать покупкой игрока.
ReadPurchaseCandidates использует штатный get_ship_definition по category
tags/size/фракции выбранной известной верфи и пересечение native player
get_ship_build_wares. Возвращает до64 реальных доступных macro с reason/
truncated, без spawn/payment и собственной таблицы кораблей. XSD проходит.
Нужно подключить native class/strength demand и delivery в goals; не закрыто.

11.10: CancelUnsubmittedPurchase освобождает только тот же pending key при
отсутствии TrackBuild и любой квитанции его эффектов, до approved/sent/
built/unknown. Quote/предоплатный submit failure записывает waiting reason,
очищает локальную quote и даёт backoff1min; подготовка учитывает NextAttempt.
Финансовая неопределённость не превращается в бесплатный retry. XSD проходит;
load recovery/Manager polling/пакетные игровые сценарии ещё открыты.

11.10: устранён source конфликт economy/shared claim: старый экономический
set_value создавал claim без manager/commander до общей ClaimOwnedShip,
что приводило к claim_manager_mismatch. Локальное создание/group удалено,
единственный автор полного claim — Runtime. ActionDefinition.Ship/
CommandeerTime теперь записываются только после успешного claim, без
фиктивного назначения при отказе. Generator/checker исправлены,12 файлов
пересобраны; ref/hash и XSD полного замыкания проходят. Runtime не запускался.

11.10: CompletePurchase связывает exact match/Tracked build с доставкой
целевой задаче, затем Lua ReconcilePurchase сверяет key/native ID/macro/paid
и реальную собственность/operational корабля. Только reconciled очищает
Pending и bounded candidate/match буферы; Request.LastResult сохраняет
task/ship/paid/key для вызывающего Manager. Unknown/cancelled не снимают
финансовую блокировку. XSD/Lua syntax проходят; native goals ещё не вызывают
этот цикл, save/load и полный игровой путь требуют пакетной проверки.

11.10: product BuildAdded сохраняет ограниченный16 список native handles
той же верфи/macro. MatchPurchase вызывается и после native event, и после
PurchaseSubmitted: оба порядка delivery поддержаны, выбор не останавливается
на первом похожем ручном заказе. Lua exact ID/yard/price/faction/macro match
публикует один typed handle, MD TrackMatchedPurchase сверяет Pending key/
yard/macro и вызывает прежний ReadBuild/TrackBuild с фактической ценой.
При overflow/несовпадении нет подбора по одной модели и повторной покупки.
XSD/Lua syntax проходят; Manager caller/доставка/reconcile и игра ещё открыты.

11.10: QuoteReady→ApprovePurchase повторяет CanAct/живую Goal/yard/доступ
постройки/бюджет и точный request key, затем единожды разрешает Lua submit
той же зарегистрированной quote. Dispatcher снимает локальную quote после
ответа, publish built/unknown/submission_failed. ValidateBinding/Unbind
отзывают ещё неисполненные approvals; sent/unknown receipt не уничтожается.
XSD и Lua syntax проходят. Нет Manager caller и native event correlation
product dispatcher; пока source-only, не подтверждён полный игровой цикл.

11.10: PreparePurchase добавляет product MD request: живые Manager/Goal,
CanAct binding, известная действующая верфь, ship macro, бюджет/level и
native get_ship_build_wares(requireblueprints/canbuild) перед quote. Один
pending запрос, собственный sequence/key; Lua purchase_dispatch генерирует
штатную quote и публикует QuoteReady без оплаты. Dispatcher зарегистрирован
в ui.xml; пока нет Manager caller/ветки разрешения оплаты. XML/Lua syntax
проходят; установка и игровой вызов не выполнялись.

11.10: DeliverCompletedShip передаёт exact Tracked.Build только после ready
read-back и успешного ClaimOwnedShip целевой задачи. При отказе управление/
деньги/track не сбрасываются; success сохраняет LastBuild/LastDelivery и
очищает один purchase slot, повтор последнего build отвергается. Общий
CanUse требует живую GoalCue и совпадение Manager в claim, включая новый
корабль. XML/ref checks проходят. Production caller и согласование Lua
submission после доставки ещё не подключены; игровая приёмка не выполнена.

11.10: exact native BuildTaskID correlation перенесён в purchase_submit.match;
диагностика вызывает тот же product helper вместо отдельного алгоритма.
ID candidate явно cast BuildTaskID перед десятичным string сравнением,
без tonumber/потери64bit; отдельно сверяются оба yard/цена/faction/macro.
Отказ теперь различает invalid correlation, ID mismatch и native identity
mismatch и сохраняет candidate ID. Lua5.1 syntax обоих файлов проходит.
Причина прежнего native_match=0 ещё не доказана; следующий общий игровой
прогон должен дать точный отказ, не обход TrackBuild и не фиктивное закрытие.

11.10: purchase_submit.lua выделяет из принятой headless пробы normal
TransferPlayerMoneyTo/AddBuildTask6/SetBuildTaskTransferredMoney. Принимает
готовую зарегистрированную quote и бюджет Manager, повторно проверяет
lifecycle через обязательный canAct перед оплатой, сохраняет sent/unknown
до эффектов и точный native ID до проверки ABI/read-back. Непримирённая
покупка блокирует повтор. Lua5.1 syntax проходит; модуль пока не зарегистрирован
как событие и не вызывается Manager. MD lifecycle dispatch, exact handle
correlation и пакетная игровая приёмка ещё необходимы; 3.5 открыта.

Дополнительно11.10: резервирование перенесено перед изменением native
groups/counts/force totals в местах commandeer. При отказе ClaimOwnedShip
исходная ветка не добавляет корабль, не увеличивает число подкреплений и
не отправляет Set_Ship_Order/Send_Patrol. Это устраняет ложную доступную
силу после отказа общего guard. Пересборка12 scripts и XSD/ref проходят;
игровое подтверждение остаётся в общем пакете, задачи не закрыты.

11.10: staged замыкание12 scripts переведено на общие CanUse/Claim/Record/
Release guards в tm_empire_runtime. Перед каждым create_order/назначением
повторная проверка binding/собственности/helm/ручных приказов, штатный handle
сохраняется; issuing защищает синхронную замену defaultorder. Освобождение
не меняет commander и уступает новым ручным приказам. Через native standby
таблицу claim передаётся только тому же Manager после проверки выбранного
корабля; просмотр кандидата не меняет владельца задачи. Scout/envoy job tags
заменены native shiptype.scout, military — purpose.fight; второй штатный
проход разведки по S/M fighters сохранён. XSD/ref/hash checks проходят.
Эти изменения source/staged, не установлены/не активированы; игровая
приёмка передачи и остальных доменов остаётся открытой. 5/32 без изменений.

Серия отдельных игровых перезапусков прекращена. load-31 проверила native
quote → plan → UILoadout2 без UI (6 software, 3 engines) и обычную покупку
без окна: ID35347ULL, price/paid1234013Cr, баланс72431853 →71197840.
build-contract-07/08 наблюдали building →ready, playerowned/operational courier,
но native_match=0. Выявлен обход: return в обычном MD cue не завершает его
действия; выполнялась общая ветка TrackBuild. Source исправлен явным do_else
и библиотекой run_actions для раннего отказа. Добавлена семантическая проверка
обычных cue returns; 8 unit checks проходят. Точный ID match остаётся в общем
отчёте, новая игровая микропроба ради этой правки не запускается.

Следующий пакет — целостная адаптация единого Manager по карте несовместимых
границ: owned assets/economy/acquisition/stations/military/personnel и общие
lifecycle/control guards, затем UI причин и пакетная приёмка. Generator теперь
собирает все12 private scripts в native/adapted/md; manifest содержит SHA и
cue paths всех найденных job/acquisition/assignment/finance/faction/personnel
границ. Копии пока частично адаптированы, не устанавливаются и не активируются.
XSD всего замыкания и прежний HQ/economy ref check проходят; это состояние
сборки, не готовый управляющий. Остальные исторические заметки ниже не отменяют
этот checkpoint и новый порядок работы.

После build-contract-08 тестовый процесс X4 PID177172 завершён. Исправленные
диагностические файлы скопированы в extension для следующего пакетного запуска;
новых покупок/перезапусков ради этой правки не было. Тестовое состояние покупки
не записывалось в save_004; JSON receipts хранят результаты проведённой пробы.

load-20/build-contract-02 подтвердили загрузку purchase_receipt после
исправления его регистрации в ui.xml. Native build в текущем сохранении
не найден, поэтому ABI/передача самого handle пока не проверены.
load-21/quote-contract-01: штатный GenerateShipLoadout2 выполнился на известной
верфи игрока; цена 1210593, crewprice=0, crewcount=0, purchase_called=false.
Получение комплектации/цены реально работает без второго подбора оборудования.
Receipt/ReadBuild исправлены: native build.price исключает экипаж,
transferredamount включает его. Fixtures и XSD проходят; установка 16 файлов
проверена по SHA. Сравнение того же payload со штатным окном покупки подготовлено.
Настоящая оплата/заказ/готовность корабля ещё не выполнены; 3.5 открыта.
Размер собственной пиктограммы подтверждён пользователем; AI остаётся inactive.

load-25/ui-assets-03: опубликован полный снимок 69 объектов (2 станции,
67 кораблей), 5 waiting, 64 excluded; UI ограничил строки 64. Период
388832.8002318–388842.8121937; независимый native подсчёт совпал.
Это проверка наблюдения, не выполнение доменов управления.

load-27/quote-ui-06: одинаковая комплектация дала 1233995 при первичном
расчёте и 1233996 в native UI. Постатейная сверка установила изменение
цены оружия 108760 → 108761 между вызовами. Добавлен reprice той же
корзины; Lua fixture и проверка native ABI проходят. load-28/quote-ui-07
подтвердили текущую цену в игре: price=native_price=1233996, matches=true,
initial_price=1233995, обе crewprice=0, purchase_called=false. Пересчёт
той же комплектации прошёл; 3.5 остаётся открытой до оплаты/build/ready.

Следующий слой 3.5: в source добавлены TrackBuild/ObserveTracked и точные
native события ready/cancelled. Связь с готовым ship сохраняется после
удаления заказа из очереди; unknown не разрешает новый заказ. Диагностика
получает native build из event_player_build_added, включая чужие верфи.
XSD/scheduling и strict OpenSpec validate проходят. Эти новые MD изменения
ещё не загружены текущим процессом X4 и не прошли игровую приёмку.

load-29/purchase-fixture-01 выполнена штатная покупка одного курьера за
1233996Cr: баланс 72431853 → 71197857. build-contract-03 подтвердил настоящий
userdata handle, ID, верфь и цену GetBuildTaskInfo. Исходный save не записывался.
TrackBuild из added event поймал payment_unconfirmed до штатной отметки
оплаты. В source диагностическое read-back отложено на 1s для того же
handle; XSD проходит, исправленный порядок ещё не загружен в текущую игру.
3.5 открыта: готовность и production путь покупки из AI ещё не проверены.

load-30/purchase-fixture-02 → build-contract-05/06: штатная оплата1233996Cr,
building с paid=1233996 и без нехватки ресурсов, затем exact native
ready ship (userdata, playerowned/operational, courier macro). Повтор
purchase-fixture-repeat-01 отклонён без новой покупки; counts69 →70.
Поздняя диагностическая TrackingResult перезаписалась отказом другой
добавки до первого delayed чтения. Original tracked handle/ready не заменены.
Source фиксирует added немедленно в первом событии и допускает delayed
read-back только из added; XSD/strict validate проходят. Исправленный latch
ещё не загружен в текущую игру. AI purchase адаптер и 3.5 остаются открытыми.

Подготовка покупки без меню: purchase_quote.to_plan строит native upgradeplan
через Helper.convertLoadout с software slots того же macro. Quote удерживает
исходные arrays, повторной генерации нет. Fixture и native ABI check проходят.
quote_contract теперь проверяет native Helper.callLoadoutFunction roundtrip
без окна/покупки; после следующего запуска требуется её игровая проверка.

Подготовлен TM_Empire_Assets и вывод счётчиков/периода/ограниченных строк
реальной собственности. Полный native поиск раз в минуту; обработка по
32 объекта каждые 5s; UI до 64 строк, счётчики охватывают весь снимок.
Нет исполнения приказов, торговли или отдельной стратегии. XSD/scheduling
и UI fixture проходят. Новый source установлен (17 файлов с SHA-проверкой);
игровая приёмка — load-23. 5.5/3.8 остаются открытыми до всех критериев.
quote-ui-01: диагностический вызов пропустил выбор класса, stock menu не
подготовил modwaresByWare. Порядок исправлен штатным dropdownShipClass
перед dropdownShip; quote-ui-02 подготовлена, финансовые эффекты отсутствуют.

Продолжение lifecycle: ValidateBinding проверяет действительность сохранённого
назначения перед публикацией и повторным BindGovernor. Утрата сотрудника,
станции/собственности, модуля/operational состояния, уход/иная штатная
должность очищают только собственные Registry/actor blackboards; штатная
должность сотрудника не отменяется. Причина сохраняется в StopReason и
показывается на уже открытой странице после исчезновения управляющего.
XSD/scheduling и Lua fixture причины остановки проходят. Новые исходники
установлены с проверкой SHA; текущий процесс игры ещё использует предыдущие
загруженные scripts. 2.4 остаётся открытой: нужны адресная игровая приёмка,
согласование pending/unknown переводов и будущих доменных эффектов/load.

Продолжение pending: ArrivalWatch наблюдает sent и unknown, поэтому позднее
прибытие после таймаута может завершить привязку. Unknown не разрешает
повторную команду npc_move_to; assign_hired_actor остаётся только в исходном
RequestAssignment, не повторяется наблюдателем. Перед перемещением живого
NPC проверяются ownership/controlpost. Полученный реальный Employee
сохраняется в Pending.$Actor до BindGovernor, чтобы следующая проверка не
создавала его снова из уже прибывшего шаблона. Claim остаётся удержанным
при недоказанном исходе; утрата destination не выдаётся за отменённый
штатный перевод. XSD/scheduling проходят; адресная late-arrival/load проба
ещё не выполнена, поэтому 2.2/2.4 не закрываются.

load-18: штатный save_004 загружен, role-contract-02 подтверждает
manager=existing_post, repeat=bound, pending=idle, manager_unchanged=1.
UI status-08/09 реально создали собственный frame с двумя tables;
ui-stats-02 и ui-empire-03 создали обычные соседние страницы. Новый ресурс
tm_empire_status.gz запрошен игрой при построении панели (debug.log);
сообщений icon overlap/1079 в этой пробе не найдено. Это подтверждает
загрузку ресурса и создание страницы, но не визуальные размеры пиктограммы.
Страница статуса оставлена открытой. Экономический Manager по-прежнему
не активирован: projection.active=0; 3.1 и доменная приёмка открыты.

- 1.1: аудит 138 исходников и 74 наложений расширений записан в game-source-audit.json. Полное runtime-замыкание пока не квалифицировано.
- 2.1: копия аргонского модуля имеет собственные идентификаторы; штатные захват, рецепт, цены и лицензии сохранены. Изолированная modulegroup не меняет выбор модулей NPC.
- Старый установленный topmanager v157 полностью сохранён с проверкой 70 SHA256 в archives/installed-topmanager-v157-2026-10-10 и удалён из extensions. Новая разработка установлена как tm_empire_management; манифест installed-manifest.json.
- UI: собственная вкладка вставляется после empire, перед stats. Lua-fixture проверяет порядок, отсутствие дубликатов, остановку без сотрудника и неизвестный исход. Живой диагностический ответ подтверждает наличие штатного callback API; полный UI ещё не принят.
- Отдельный диагностический мод tm_empire_diagnostics и общий pipe-клиент находятся в tests/diagnostics и не входят в продуктовую поставку.
- 1.2: штатная проверка разрешает назначение существующего работника пассажиром на станцию; реальное назначение уменьшило экипаж источника, создало пассажирскую запись на станции и сохранило обычного менеджера. Прибытие и создание физического сотрудника пока не подтверждены: запись остаётся intransit. Причина исследуется, независимый управляющий пока не реализован.
- Тестовый save_099 создан штатным SaveGame; исходный autosave_03 скопирован в .cache/tmp/role-probe. User разрешил мгновенное добавление модуля на HQ для испытаний: команда module использует штатный create_module и повторное find_module, только в диагностическом моде.
- Полный скопированный FactionLogic.Manager, управление империей, оценки станций и двухчасовая приёмка ещё предстоят. Галочки задач остаются открытыми до выполнения критериев.

Живая проба module-01/module-02: модуль 0x1871e8 добавлен на HQ XZS-342 (0x4c304), оба ответа повторного поиска совпадают; повторная команда не создала дубликат. Сохранение с этим модулем пока не проверено. save_099 существует на диске, но не появился в штатном списке — восстановление из него не квалифицировано; проба модуля выполнена после загрузки autosave_03.

Продолжение после quicksave пользователя: SHA256 резервной копии 3100ECEDE59D51C436AE22596062217C1AB123B0279D8B496A04DECCD18E81E7. module-03 подтверждает восстановление модуля. assign-04/role-read-08/place-08 подтверждают перевод существующего crew NPC, фактическое прибытие, отдельный actor 0x18da4b, module binding 0x4a7cb и неизменного менеджера HQ. save_004 содержит собственный Registry и blackboard actor. Первая загрузка save_004 вызвала 1079: новый ProjectionWatch сбрасывался без явного delay; checkinterval не ограничивает повтор при истинном условии. Исправление: явный delay=5s, регрессионная проверка tools/check_md_scheduling.py. Повторная загрузка для приёмки исправления выполняется; 1.2/1.3 пока не закрыты.

1.2 завершена: assign-04/role-read-08/place-08, штатный save_004, успешная загрузка load-13 и check-02 (manager_attempt=existing_post, repeat_binding=bound, manager_unchanged=1). release-01/role-read-09 подтверждают снятие независимой должности при сохранении человека на HQ и штатного менеджера. После исправления delay повторная загрузка того же save_004 прошла; игровой clock продвинулся, AutoIDMap/FATAL отсутствуют. Общий прогресс 3/32. Пользовательский UI назначения и AI остаются открытыми задачами.

1.3 завершена: Lua fixture проверяет порядок sidebar empire/status/stats, bounded валидацию, native MD boolean 0/1 и область обновления только своей страницы. Живые ui-status-04/05, ui-empire-02 и ui-stats-01 подтверждают создание штатных frames и переходы между тремя страницами на текущей X4. release-02 сохраняет менеджера станции; ui-status-06 подтверждает governor=0 и новый frame открытой страницы после события MD. Внешнее окно и Extension Options не используются. Общий прогресс 4/32; полный контент вкладки, пользовательское назначение и управляющий AI ещё не реализованы.

Причина fatal 1079: наш ProjectionWatch сбрасывал себя при постоянно истинном условии без delay и заполнял AutoIDMap. checkinterval не обеспечивал задержку повторного экземпляра. Добавлен явный delay=5s, XSD и отдельная семантическая проверка self-reset MD. Тот же неизменённый save_004 успешно загружен в load-13/14/15; последующие обращения к UI и снятие должности выполнены без повторения fatal. Это адресная проверка исправления, а не двухчасовая приёмка автономного управления.

1.4: effect-contract.md сверяет native assignment/payment/skill/build границы и формализует read-back/unknown. Четыре отрицательных fixture-теста отклоняют недостаточные подтверждения, чужие активы, helm/manual/emergency и потерю unknown claim. Валидатор относится к тестам, не является новым игровым исполнительным framework. load-16/check-03 подтверждают восстановление сохранённого назначения после теста снятия. Общий прогресс 5/32; доменная интеграция этих правил ещё предстоит.

Продолжение 2.2/3.1: собственные разделы штатного диалога сотрудника добавлены в TM_Empire_Roles; RequestAssignment/ArrivalWatch используют native assign/arrival/actor placement. Пользовательский выбор и перевод ещё в приёмке, задача не закрыта. Manager v18 и 12 scripts динамического/текстового замыкания скопированы в native/md с собственными namespaces/globals, SHA и XSD-проверкой; копии не устанавливаются, пока несовместимые эффекты не адаптированы. Оригинальные NPC scripts неизменны. Общий прогресс остаётся 5/32.

load-17/role-contract-01: после загрузки той же save_004 новая production RequestAssignment отклонила реального station manager как existing_post, повтор текущего governor дала bound, Pending=idle и manager_unchanged=1. Это живая проверка библиотеки новой роли, а не завершённая UI/transfer приёмка. Инициализация X4 до intro заняла 102 секунды, до start menu ещё около 18; длительная загрузка не была повторно запущена по тайм-ауту наблюдения. Игра ответила после загрузки; AutoIDMap/IDBase fatal не повторились.

11.10.2026, исправление пустой вкладки по скриншоту пользователя: render теперь
создаёт таблицу по штатному шаблону PlayerInfoMenu (tabOrder/border/width/x/y,
maxVisibleHeight вместо передачи height; явная ширина колонок). Lua fixture
проходит. Пакет 44 файлов установлен, диагностический Lua расширен геометрией
таблицы и количеством rows. PID168592, load-18 accepted/save_004:
ui-status-68 body_rows=4 при запуске управляющего; ui-status-69 body_rows=76,
active=1, assets=69, rows=64, tasks=1. Область таблицы width=347,x=61,y=99,
maxVisibleHeight=621 внутри экрана. Это доказательство populated table/геометрии,
не визуальная приёмка текста: screenshot после исправления пока не получен.
Текущий запуск также содержит предыдущие source-исправления static purchase
acknowledgement и счётчики анализа; их конкретные сценарии ещё не доказаны.
По запросу другого потока диагностики запуска предоставлено безопасное окно:
после ui-status-69 в этой сессии нет незавершённых диагностических команд или
покупок. До завершения согласованных запусков текущий поток не изменяет runtime.

Следующий source UI-пакет: render использует native empire full width
(menu.playerInfoFullWidth - sideBarWidth - Helper.borderSize) вместо narrow
ширины callback. Установленный UIX выбирает full width только для известных
ему режимов, наш mode туда не входит: live ui-status-69 подтвердил 347 px.
Ячейки используют штатные wordwrap и mouseOverText. Fixture проверяет область
1115 px при экране 1280, её границы и maxVisibleHeight без height; проходит,
dry-run 44 файлов и strict OpenSpec проходят. Пакет пока не установлен:
игровой runtime предоставлен другому потоку для диагностики startup.
Видимость текста, прокрутка и live full-width ещё требуют игрового read-back
и визуального подтверждения; задачи 5.5/5.6 не закрываются по одному fixture.











Исходник575: исправлен двойной ответ PersonnelAutonomousRead в диагностике;
кадровый клиент останавливается при несовпадении ответа. XSD PASS,3 transport
contract tests PASS. Пока не установлен; см. diagnostic-response-boundary-20261012.md.

Исходник576: seed сотрудника сохраняется перед семинаром; замена личности
при сверке даёт unknown без повторного расхода. Русская причина добавлена.
validate576 PASS; игровой сценарий ещё не принят, установка571 сохраняется.

Актуальный контроллер: load579 terminal0 accepted save_004; short581
session76715 запущен для установки578 (исправленный протокол). X4 PID47004.
Неустановленный source580: точная причина несогласованного состава перевода
сохраняется в receipt и отображается по-русски; XSD/UI fixture PASS.

Исходник583: диалог назначения governor защищает сотрудника с sent/unknown
переводом или обучением до local binding и native dispatch. validate583 PASS.
Установка578; неустановленные580/583. short581/session76715 ещё активен на
последней проверке; единая кадровая response рамка подтверждена.

short581 завершён terminal0. Штатный кадровый тик самостоятельно выбрал
подготовленного NPC, оплатил478960Cr и назначил на созданный тестовый корабль.
Employee seed совпал; container=target, transit=0/scheduled=0. Receipt остаётся
sent/native_hire_arrival_pending: полный observed результат ещё не принят.
Это новый реальный paid-hire эффект, не бесплатное назначение fixture.

read584 terminal0: hire observed, paid478960Cr, тот же actor/seed, container
target, transit0/scheduled0, passed1. Принята4.4 (11/32);4.1/4.2 открыты.
Контроллеров нет; установка578, source580/583 ещё не установлен.

Исходник585 (diagnostic only): builder_near принимает оплаченный observed
arrival при незавершённом DeployToStation; исходный key/order/build проверяются.
validate585 PASS. Ещё не установлен;3.4 остаётся открыта, ожидания нет.

short586 terminal0: текущие plot/funding observed и оплаченный builder_hire2
связаны с PFY-706/build0x1dee. Команды подтвердили приближение строителя и
материалы; через15s resource_types3→0, но deployed0/expansion queued.3.4
не принята. Контроллеров нет; установка578, source580/583/585 не установлен.

Исходник587: минутная очистка событийных slots утраченными/проданными
станциями (3 таблицы × максимум32), без сброса действующих периодов.
validate587 PASS; ещё не установлен. Установка578; source580/583/585/587
накоплены общей порцией. Активных контроллеров нет,11/32 приняты.

Исходник589: текущая станционная оценка и исключение текущего периода из
истории требуют совпадение фактического employee seed. validate590 PASS.
Не установлен; общий пакет source580/583/585/587/589, текущая установка578.

Diagnostic592–594: однократная подготовка второго module/реального NPC и
проверка запрета второго governor, смены/возврата с независимым station manager.
validate594 PASS после исправления slot атрибутов. Не установлен/не исполнен.
read591 terminal0 подтвердил прежний observed hire; construction still queued.

Уточнение594: XSD PASS, scheduling FAIL (return в cue). Исправлено595
переносом действий в run_actions libraries; validate595 XSD/scheduling PASS.
Предыдущая запись validate594 PASS не является верной общей приёмкой.

load598 terminal0 accepted save_004. short599 запущен после закрытия loader.
Source600–601: независимый физически прибывший сотрудник может bind локально
при Pending другого человека; старый Pending и собственные personnel guards
сохранены. validate601 PASS; не установлен (игровой пакет597).

short599/session62344: role setup placement_unavailable, кадровые mutations
не запускались. Source602 diagnostic: проверка штатных passenger/service slots
после generic slot; validate602 PASS, не установлен. Два модуля не приняты.



















`nКонтроллер short h: unifiedexec13527 подтверждён live, повторно опрашивать его.








