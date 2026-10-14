# Приёмка экономических назначений — пункт3.3

Принят контракт назначения собственных кораблей с сохранёнными claims и
финансовыми квитанциями. Полнота экономического анализа/сбыта/добычи3.2,
военных целей, двухчасового прогона и релиза этим документом не принимается.

## Два дефицита и собственность

Autonomy380/004-role содержит6 delivered действий штатного Econ_Manager:
purchase1/4/5/6 для energycells и purchase7/8 для water. Ключи сохраняют исходные
issued времена; все6ship handles различны в одной текущей сессии:
0x1790f/0x659ad/0x65945/0x664f0/0x17954/0x194d3. Read-back каждого показывает
native_economic_order_observed; реальные корабли имеют claim sent, goal Econ_Manager
и штатные TradeRoutine с дочерними DockAt/Undock/TradePerform. Это не только
выбранные планы и не поиск похожих кораблей по macro.

Runtime.CanUseOwnedShip перед эффектом отклоняет claim другого manager/goal,
unknown/issuing/stopping, смену commander, чужие orders/default behavior и
корабль под штурвалом игрока. RecordOwnedOrder сохраняет конкретный order
и собственный claim. Действующий корабль не выделяется второму дефициту.
Резервирование товара и исполнение торгового маршрута остаются штатными.

## Деньги и неизвестный эффект

Request.PreparePurchase сериализует незавершённый Pending/Tracked build.
Lua submit удерживает предыдущую unreconciled/same-key квитанцию, перепроверяет
manager/budget/реальную цену и текущий счёт перед оплатой; payment_sent сохраняется
до TransferPlayerMoneyTo, неизвестный исход сохраняется без повторной оплаты.
Typed native build/shipyard/macro/player/price/paid привязка подтверждена принятой
приёмкой3.5, включая save/load и продолжение после handoff. Её сырые финансовые
свидетельства/точные списания доступны в ship-purchase-contract.md, а не заменены
общим изменением баланса за период. purchase_submit/purchase_receipt fixtures
покрывают повтор/unknown/изменение условий; мод не создаёт собственный торговый
исполнитель и не выставляет оплату задним числом.

## Реальная работа и продолжение

Autonomy380/004-provision: station KMT-485, ware water, incoming160,
managed_incoming160, last_managed_ship «Тефида Агрессор»,
last_managed_observed402738.453. RecordStationTrade записывает это только на
штатном completed trade, с реальным transferredamount и player-owned кораблём
под claim действующего Manager. Таким образом подтверждена реальная поставка
кораблём управляющего; общие NPC поступления отдельно не приписываются ему.

Фабрика в новом native economic cycle402426.917 производит (producing1,
resources0), а цикл/журнал продолжается. Ранее role366 показывал штатное
native_existing_actions_cover_need для уже покрытой потребности воды, не новый
безусловный повтор. Другие неизвестные/неполные потребности остаются waiting
с конкретной причиной known_market_input_incomplete, независимо от работающих
поставщиков. Необоснованного повторного использования корабля/платежа не найдено
в подтверждённых сценариях этого контракта; это не универсальное доказательство
всех возможных игровых ситуаций.

Installed packet373/46files подтверждён install-boundary381; source-only изменения
оценки/кадров не участвовали в этом результате. Collector380 остаётся read-only,
qualified_releasefalse. Остальные22 задачи остаются открытыми.
