# Торговое обеспечение станций: штатная потребность и короткий read-back

Добавлен пропущенный стык между штатной проверкой Upkeep торгового подчинённого
и адаптированным Econ_Manager. ReadStationTradeNeed повторяет порядок штатного
Upkeep_Management (торговые товары, затем чистые ресурсы, без minable/recycling)
и вызывает оригинальную Needs_Subordinate_Trade_Ship_Lib. Эта библиотека проверяет
пригодность кораблей; она не заменяет определение потребности станции.

Обычный Econ_Manager сначала ищет собственный свободный транспорт тем же
Request_Commandeerable_Freighter. Покупка возможна только через прежний платный
Request_Freighter после окончания асинхронного поиска. Запись ActionReports с
TM_Requester защищает от повторной заявки; незавершённое/unknown не равно отказу.
Новая запись имеет AggregatedValue0: потребность не выдаётся за финансовый дефицит.
Работу назначенного транспорта выполняет обычный менеджер станции.

Вкладка показывает текущую нехватку торгового корабля и рекомендацию. Оценки,
история менеджера и новый торговый исполнитель не добавлены. Проверки ограничены
32 торговыми подчинёнными/товарами/ресурсами; неполный результат не запускает покупку.

Пакет установлен, source/install hashes сверены. Генератор13 native scripts,
XSD и scheduling, adapted refs/guards, Lua status fixtures, unittest5,
installer dry-run51 и OpenSpec strict прошли. Кандидат архива пересобран,
qualified_releasefalse. Эти проверки не заменяют игровую приёмку экономики.

Точные игровые receipts в .cache/tmp/station-boundary-20261011/:
station-trade-provision-20261012.json; saved-current-boundaries-20261012.json;
current-native-provision-repeat-20261012.json. Последний controller terminal0:
запустил обычный GenerateShortageData и через15сек прочитал фактический мир.
EKA-355 перешла к production producing1, subordinates_total2/operational2;
нехватка торгового корабля больше не показана. MZK-812 имеет TradeRoutine,
claim sent, goal Request_Commandeerable_Freighter. Нужен точный commander/read-back
всех новых ActionReports и повтор: фиксированный BJV-644 остался Wait, и по нему
одному нельзя отрицать назначение другого подходящего транспорта.

Торговая граница: observer зафиксировал1 реальную покупку собственного корабля
на EKA-355, продажа NKU-508 ещё не зарегистрирована. GetTradeList даёт действующую
заявку NPC на37810 siliconwafers по419Cr; собственная продажа ранее338.73Cr.
Доставка/доход ещё не приняты. Стройка другим native путём реально началась:
processor elapsed34.4548→155.681 из1140, тот же оплаченный50000Cr NPC builder,
command buildingto. Диагностика не меняла deployed/progress/finished.

24/32 остаётся:3.2/3.4/3.6/3.8/6.1/6.3/6.4/6.6 открыты.

Дополнительный read-only receipt station-trader-commander-read-20261012.json:
idle_orders_read вернул90 собственных кораблей. MZK-812 commanderEKA-355,
defaultTradeRoutine, DockAt/queue5, claimsent, helm0. DON-919 остаётся
MiningCollect/commanderEKA-355; роли обоих кораблей различаются. HOL-217
commanderKMT-485, TradeRoutine/defaultTradeRoutine, claimsent, searchingtrades.
BJV-644 действительно свободен (idle1/Wait/nullcommander/nullclaim).
Тем самым реальное назначение торговых подчинённых подтверждено без инжекции
собственных приказов. Доставка/продажа и повторная устойчивость остаются открыты.
