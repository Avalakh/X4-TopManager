# Станционный пакет: хранилища, добыча, найм

## Изменения

Копия FinaliseStations вызывает штатный get_suitable_storage_modules до
генерации расположения модулей. Входы — все production/storage из выбранного
плана и BaseSequence; результат добавляется в общий план, который затем
проверяется на чертежи и строится прежним оплачиваемым путём. Предварительное
условие выявлено в реальной новой фабрике VTV-679: завершены семь элементов
плана, но energycells/silicon/scanningarrays имеют нулевую ёмкость. Приёмка
строительства3.4 до работоспособной фабрики остаётся открытой.

Обеспечение станции добытчиком в обычном EvaluateShortages использует native
Upkeep Needs_Subordinate_Mining_Ship_Lib как решение о вакансии. Native
InsufficientProductionWares и InsufficientBuildWares сохраняются для учёта,
но не блокируют назначение при пустой таблице. Это позволяет обслуживать
верфи с minable-ресурсами из установленного игрового каталога. Cargo capacity
должна быть положительной. Используются те же Request_Commandeerable_Freighter,
поиск собственных свободных кораблей, асинхронный fallback и оплачиваемое
Request_Freighter; нового исполнителя или отдельного стратегического цикла нет.

Диагностический mining_setup создаёт только условия: стандартный шестимодульный
scenario2_silicon_refinery, штатный менеджер, энергоэлементы и свободный минерал-
добытчик с пилотом. Кремний/назначение/claim не добавляются. Mining read показывает
реальные cargo, приказ, commander и claim. Бесплатное создание тестовых объектов
не является доказательством строительства или покупки модом.

## Найм до установки пакета

Квитанции: .cache/tmp/station-boundary-20261011/hire-batch-20261012.json,
personnel-hire-arrival-20261012.json. PID154872, установленный предыдущий пакет.
Setup создал реального нанимаемого аргонского NPC на известной ZYH-979 и
собственный корабль0xe187590 с пустой должностью пилота. Production RequestHire
вызван диагностикой напрямую: это адресная проверка адаптера, не доказательство
самостоятельного выбора кандидата кадровым tick.

Hire key hire_1_407213.473, actor0xc1b7cfd, seed -7711824739669823977.
Результат сначала sent, затем observed; оплачено559840Cr, exact actor/seed
занимает должность target, intransit0/scheduled0/podnull, passed1. Native кадровый
tick продолжает работу. Все вакансии и независимость ролей4.1 этим не принимаются.

## Установка и контрольная точка

Autosave_01 от12.10.2026 20:44:24 содержит этот hire, service test wharf и
construction_1_397332.222. Gzip CRC/stable/полный SHA проверены:
e3a9c2b6befff968d05abb871179b073d66524be329ee55e32e723c83118134b.
Квитанция autosave-package-20261012.json, game age407420.242. Чужие физические
сохранения не перезаписаны. PID154872 штатно завершён; общий production51 и
diagnostics8 скопированы с SHA read-back. Steam запущен только с appid392160,
без добавления пользовательских launch flags.

Generated13, MD syntax/scheduling/ref check, check_adapted_manager и Lua syntax
PASS. Игровой результат нового пакета пока требует read-back после загрузки;
клиент controller-mining-package-load-20261012.py/session6355 terminal0.
После load paid hire сохранился: target0x13185, employee0x1318a, тот же exact
seed/key, paid559840Cr, stateobserved/passed1. Изменившиеся object IDs послеload
не используются для корреляции без receipt/seed.

Mining fixture WQH-227/FIR-145 prepared: native storage silicon50000, zero cargo,
свободный miner/Wait без injected claim/order. Первый анализ не назначил корабль:
production waiting_resources1 и native Upkeep missing miner, но native
InsufficientProductionWares пуст. Это выявило лишний gate нашего адаптера.
Он удалён: vacancy определяется штатным Upkeep, количество из экономического
отчёта (включая0) остаётся только учётом; фиктивный дефицит не создаётся.

Исправленный полный production51 установлен после штатного закрытия PID113824;
diagnostics8 остаётся прежним, SHA уже проверены. Первый бесплатный mining
fixture откатился загрузкой прежнего тестового autosave и будет подготовлен
заново; сохранённый paid hire не повторяется. Новый клиент
controller-mining-upkeep-load-20261012.py/session41440 живой, ожидает mainmenu.
Session41440 terminal0, последующий mining-upkeep-followup terminal0: IOP-356
с production waiting_resources1 и свободный IJN-713 всё ещё без назначения.
Сверка ProcessStations выявила вторую часть причины: Report.keys.count0 вообще
не включает станцию в GlobalStorageData. Upkeep вычислялся только в UI observation.
Теперь native Upkeep вычисляется один раз до report gate, его непустой результат
сохраняется как Report.$TM_MissingMiningTypes; UI переиспользует тот же результат.
Количественные native shortage/overflow не подменяются и не дополняются выдуманными
числами. Source checks PASS, полный production51/diagnostics8 установлен после
штатного закрытия PID154584.

Диагностика пакета: mining_read показывает реальное наличие native report/time,
factory_build_start запускает нормальный receiver Request_Factory с siliconwafers
в текущем известном секторе и production limit1. Бесплатное создание фабрики,
выдача её чертежей или принудительное окончание стройки отсутствуют. Это проверка
платного пути с диагностическим триггером, не самостоятельного решения о развитии.
construction_resources/builder_near удерживают повтор той же build/payment key,
но разрешают подготовить новый подтверждённый заказ. Всё остаётся diagnostics-only.

Добавлен отдельный fixed save012 с обязательным physical client preflight и
native slot check; source/installed save_menu позволяют load012, прежние слоты
не изменены. Пять diagnostics response tests и Lua syntax PASS.
Controller station-report-load/session76020 сейчас живой; X4 PID59644,
Responding=true, native load accepted/autosave_01. После окончанияload клиент
готовит miner fixture, запускает native analysis и отдельный factory request,
собирает read/provision. Второй pipe клиент не запускать.
Полный длительный прогон не начат. Приёмка18/32.

Обновление после session76020 (terminal0): штатный анализ сам назначил
VUB-709 тестовой refinery MAR-136. MiningRead подтверждает commander0x188ae9,
MiningRoutine, claim sent / Request_Commandeerable_Freighter. Диагностика
создала только свободный корабль и станцию с native silicon capacity50000;
приказ и claim создал production manager. Добыча/доставка ещё не приняты.

Новый реальный factory request создал shell0x188ead, но выявил два собственных
MD сбоя: select.faction списка вместо одного faction и отсутствующую
md.$TM_Empire_EquipmentTable. Генератор использует одну штатную культурную
фракцию для каталога и get_ware_definition flags=equipment из stock setup.
Владелец остаётся player; ресурсы, деньги и чертежи не выдаются.
Check адаптера и XSD PASS. Production51 установлен после CloseMainWindow /
WaitForExit PID59644. Единственный следующий controller station-catalog-load /
session34015 ждёт повторной загрузки проверенного autosave_01. Старые строки
о живых session76020/41440 выше теперь относятся к истории.

Session34015 terminal0. station-catalog-batch/repeat подтверждают тот же путь
на новом fixture EKA-355 / DON-919: native request назначил commander0x188bad,
claim Request_Commandeerable_Freighter, MiningRoutine. Повторный ordinary
analysis407505.265 оставил тот же claim/корабль/командир; приказ MiningCollect,
свежая station observation407500.089: subordinates1, mining=null. Новая
потребность/второй корабль не появились. Принимается5.4: передача актуальной
потребности в существующий стратегический цикл, без отдельного оценщика.
Сам факт добычи/доставки ещё не доказан;3.2 открыта. Приёмка19/32.

Factory creation adopted, native plan8 entries прошёл blueprint validation,
build0x8ae6 queued, plot_2_407495.936 observed. Полная3.4 пока открыта.
Точная ошибка предыдущего списка faction оказалась также в
get_god_production_construction_plan (line3224), а не только create_factory
select. Исправлена в генераторе отдельно: одна культурная faction; остальные
get_module_definition/get_construction_plan поддерживают список по XSD.
Перегенерация/check/XSD PASS; эта последняя правка пока SOURCE-only.

Дальнейший короткий пакет station-catalog-construction terminal0:
construction_funding_2_407556.123 observed6320362Cr, plot2 observed.
Материалы добавлены только diagnostics world preparation; это не платная
поставка и не завершение строительства. save-station-package terminal0
подтвердил builder_hire_2_407571.206: оплаченный builder0x18486 перемещён
с54984m до2987.5m от storage, deploy/build completion не форсировались.

Slot012 сохранён штатным SaveGame в ранее физически пустой слот.
save012-package-20261012.json:93068284bytes, CRC/stable PASS,
SHA66494d9846cdf8d7fe987f134cc150548e45ef8f18fc51444109ca6ba79eb9c3;
hire/service wharf/new construction markers true. Старые слоты сохранены.
После штатного закрытия PID81148 последняя scalar get_god правка также
установлена в полном production51. Session35035 — единственный живой клиент;
native accepted load012. Он только read/native_analysis, без новой оплаты,
factory trigger или world spawn. Приёмка3.4 всё ещё открыта, общий прогон не начат.
