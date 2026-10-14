# Границы адаптации штатной игры

## Проверка источников

Игра: X4.exe9.0.0.0 и version.dat900. `game-source-audit.json` воспроизводится tools/audit_game_sources.py; CAT/DAT считываются read-only, каждый прочитанный payload проверен по MD5 каталога, сравнение SHA/байтов с извлечением.138 base records совпали;4 ссылки storyline разрешены в соответствующие установленным DLC исходники.74 overlay учтено отдельно (packed и loose); присутствие расширения не доказывает активность. Это не разрешение включать runtime capability.

## Классификация границ

- FactionLogic.Manager/Goals/Economy/Stations: копирование собственного экземпляра и stateful замыкания; оригинальная регистрация FactionManagers и NPC namespaces остаются нетронутыми.
- `get_suitable_job`, `request_job_ship`, `commandeer_object`: заменить только NPC-контракты подбора на реальные допустимые активы игрока, сохранить штатный анализ/назначения.
- `create_station`, `create_god_station`, `create_ship`, `destroy_object`: не использовать как обход реального приобретения/строительства/утилизации игрока; сохранить normal gameplay соответствующего механизма.
- Job_Helper `add_build_to_construct_ship` и ветка0Cr: требует обычной player оплаты/готовности, не считать native вызов автоматически безопасным.
- Faction HQ/representative/миссии/сюжетные cue refs: внешние границы, не копировать весь рекурсивный138-file граф как управляющего. Проверять фактически вызываемую ветку и guards; динамические refs требуют отдельной проверки при копировании.
- Global/static tables, signals/events, shared helpers: stateful вызовы изолировать; read-only helpers переиспользовать без собственной аналогичной реализации.
- Источники скрытых сведений: фильтровать входы решения игрока; типизированный dispatch не устраняет утечку при ранжировании.
- Macro административного модуля: новая идентичность и текст, все штатные свойства сохраняются, новый алгоритм захвата не создаётся.

## Отдельная должность — проверенный контракт

### Строительство — подключённая граница 11.10

Уточнение plot extension: штатный dynamic threshold/размеры теперь ведут в
RequestPlotChange→readonly C quote→MD bookend+can_safely_extend_build_plot→
native extend_build_plot→обычная licence. `Helper.getPlotData13806–13833`
определяет free ownerless/xenon/player-owned licence; не следует требовать
sector controlstation/payment в этих случаях. C quote использует собственные
native size/center, MD сравнивает собственные снимки без выдуманного перевода
координат. После resize helper проверяет именно quoted C size/center/price
перед оплатой. Пока это исходники: native flow и immediate goal-cancel
approval revocation ещё должны быть доказаны в полном пакете.

Stock `common.xsd:create_construction_sequence` документирует asynchronous
генерацию и plot bounding box конкретной станции. В dynamic production expansion
используется этот механизм, с сохранёнными manager/goal/base/plot перед вызовом;
результат принимается по штатному событию. Blueprint scan касается новых
компонентов; уже существующий planmodule того же macro не требует нового
чертежа для сохранения в base plan. Новый sequence остаётся private до queue.
Native geometry/sequence identity через load ещё требуют игрового доказательства.

`StationConfiguration.buttonSetMoneyToEstimate:939` использует обычный перевод
денег на buildstorage, а `:3849` получает `wantedmoney` самого склада. MD property
`wantedmoney` определена как стоимость всех оставшихся строительных ресурсов
без вычитания текущего счёта. Используется этот native quote после реального
Build, exact single-build claim и текущий баланс; fixture подтверждает только
адаптированную финансовую границу, не engine resource procurement/consumption.
Перед переводом durable receipt; ambiguous debit/credit удерживает unknown.
Нативная закупка/потребление ресурсов и готовность модулей проверяются отдельно.

NPC `extend_build_plot` не оплачивает лицензию игрока, поэтому в подключённой
dynamic ветке он исполняется только в новом quote/safety/licence adapter.
Прочие habitat/prefab/
new station branches ещё не адаптированы и не могут включаться как runtime.
Single Expansion receipt временно сериализует delivery; это ограничение staged
сборки, которое нужно устранить перед полной приёмкой управления империей.

### Статическая оборона — уточнение 11.10

`FactionLogic_StaticDefense.CreateJobShips` пополняет CombatEngineersAndSaboteurs:
3 M инженера и2 S минных постановщика, не обычных защитников станции.
`libraries/jobs.xml` argon_staticdefense_engineer_m/minelayer_s выбирают
обычные `get_ship_definition` categories military соответствующего класса;
job tag staticdefense не существует в `libraries/ships.xml` и не может
использоваться для product ReadPurchaseCandidates. Их default order —
DeployStaticDefenseStrategy; S получает isminesonly=true.

Штатный `aiscripts/order.deploy.staticdefensestrategy.xml:246` уже имеет
player-owned поиск известного operational снабжения, нейтральных отношений,
доступных deployables и достижимого пути. Затем signal resupply, после чего
order.deployobjectatposition расходует реальные запасы; это основание
переиспользовать native order вместо собственного постановщика. Оно ещё не
доказывает финансовый контракт resupply и guards прерывания при helm/manual:
callee и события должны быть проверены/при необходимости перепривязаны.
Acquisition adapter должен заменить job spawn обычной покупкой military
M/S и выдать native order с теми же параметрами, сохранив исходный анализ
стратегий. Не подменять эту ветку обычным Patrol и не включать сырой Job_Helper.

Vanilla `conversations.xml:615–618` использует `assign_hired_actor` на target с controlpost либо entityrole; UI personnel имеет station manager role. Эти факты не подтверждают второй manager slot или назначение actor на defencemodule. Нужна адресная проверка реального NPC/module binding, независимого от менеджера станции, с save/load. Нельзя подменять её копированием station manager role, виртуальным именем или неподтверждённым controlpost.

## Уточнение контракта пассажира
NPC_State_Machines:848–849 направляет пассажира в STATE_stay (3175), без перемещения к назначению. Штатный публичный сигнал npc_move_to (676–705) и gm_transport_passengers:1353–1358 дают маршрут физического пассажира; использовать их для новой должности вместо подмены intransit/телепорта. Неинстанцированный экипаж переводится через Conversations.LaunchCrewTransferPod (1472), с настоящим временем прибытия. Диагностическая проба этого пути выполняется отдельно.

Проба 1.2 завершена по assign-04/role-read-08/place-08/load-13/check-02/release-01: существующий сотрудник переведён, прибыл, создан как реальный actor из своего шаблона, связан с модулем через собственный реестр и blackboard, восстановлен из save_004. Снятие привязки сохранило человека и station manager. Используется association actor/module, а не второй engine manager slot. Пользовательский UI назначения пока не завершён.
# Подтверждённая граница нового участка — 11.10.2026

Внешняя зависимость Request_Factory_Finalise → FinaliseStations.NewStation_GenerateFactory
также содержит эффекты: NewStation_ConstructionSequenceCompleted генерирует
loadout, при AddBuild=true ставит план в очередь, а при false вызывает
apply_construction_sequence. Поэтому AddBuild=false нельзя считать режимом
«только получить план». Отчёт ReportCue передаёт ['finished', sequence, BuildTask,
Station], но поступает после соответствующего эффекта. При адаптации нужно
отделить завершённую генерацию от эффекта, сохранив штатный расчёт и не меняя
оригинальную библиотеку NPC. Источник: md/finalisestations.xml, блок 323–367.

Уточнение по schema common.xsd: create_station/stage прямо документирует, что
при state=construction станция начинается без модулей, а очередь строительства
добавляется движком. Следовательно, существующая prefab-ветка со stage=1 не
доказывает бесплатной выдачи первого модуля. process_build документирован как
начало обработки build task; сам вызов тоже не доказывает обход ресурсов.
Перед заменой нужно проверить реальный buildstorage/build/plot и оплату в игре.
Штатный путь пустого участка также доступен непосредственно в MD через
reserve_build_plot: он создаёт base station/buildstorage, но требует zone и
явных размеров, не принимает constructionsequence. Поэтому наличие этого
действия не решает автоматически задачу определения размера готового плана.
Эти выводы основаны на исходном schema, а не на игровом испытании.

Штатный menu_map.lua использует `ReserveBuildPlot(sector, "player", set,
offset, x, y, z)` и затем `PayBuildPlotSize`; это путь пустого участка игрока.
ABI объявлен в том же файле, фактический вызов — около строки 27423.
NPC create_station с constructionplan/stage и create_factory не являются
эквивалентом этого действия: prefab-ветка дополнительно запускает process_build.
Для адаптации новых станций нужно сохранить выбор места/плана штатным Manager,
резервировать пустой участок обычным API, оплатить лицензию и передать весь план
обычному строительству с ресурсами. Эти ветки пока не подключены.

Наблюдение завершения расширения теперь начинает новый список модулей на каждом
полном проходе (по 32 записи за тик). Исторически виденные, затем уничтоженные
модули больше не накапливаются между проходами. Для больших планов свидетельство
имеет интервал наблюдения; одновременный снимок всех модулей ещё не подтверждён.

