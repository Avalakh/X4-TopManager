# Внутренний контракт действий и подтверждений

Контракт задачи 1.4. Не вводит новый транспорт или второй исполнитель. Игровые orders, queued builds, accounts, crew seeds и MD cue state являются первичными; собственный cue хранит только отсутствующую связь цели с отправленным действием и причиной. Тестовый Python ниже проверяет свидетельства, но не принимает игровые решения.

## Идентичность и жизненный цикл

Действие имеет собственный `goal`, `session`, `kind`, `asset`, время `issued`, состояния `planned/sent/observed/unknown/waiting/excluded`. Разрешённые kinds: `order`, `hire`, `transfer`, `training`, `ship_purchase`, `station_build`. Идентификаторы не являются командами: ни UI, ни диагностический pipe не принимают произвольный kind/asset для исполнения. Вызов остаётся конкретной внутренней веткой MD/штатного API.

Перед эффектом повторно проверяются действующий governor/module/station binding, принадлежность актива и назначения, деньги/материалы/чертежи/кандидаты, существующие обязательства и текущий контроль. `ship.pilot == player.entity` исключает штурвал; `player.ship` само по себе корабль не исключает. Явный приказ (`ship.order != ship.defaultorder`), critical order и native emergency оставляют актив игроку. Командные операции следует привязывать к native order handle, покупки — к native build handle, людей — к source/destination/seed; имя объекта недостаточно.

`sent` означает вызов принят, `observed` требует доменных доказательств ниже. `unknown` сохраняет занятый актив/деньги/людей и запрещает повтор до согласования с native handles. Тайм-аут не является отказом. Неизвестная операция не освобождается просто при load или смене управляющего. Если native источник доказывает окончательное отклонение/отсутствие эффекта, цель переходит в waiting и может повториться только после изменения предпосылки. Rollback читает только состояние загруженного сохранения, не внешние будущие свидетельства. Отдельной внешней БД нет.

## Авторитетные источники и границы

| Действие | Штатный источник | Достаточное наблюдение | Недостаточное наблюдение |
|---|---|---|---|
| Приказ | native order handle, aiscripts/order.trade.middleman.xml:795 | актуальный handle на том же принадлежащем игроку корабле, фактическое состояние/назначение и причина | отправленный сигнал или один idle |
| Найм | menu_map.lua:4125 buttonHire, `$HiringFee`, discounts, TransferPlayerMoneyTo; Conversations event_player_assigned_hired_actor | реальный candidate/seed, принадлежность игроку, назначение и фактически оплаченная полная рассчитанная сумма | assign_hired_actor success: это только принятие, API не оплачивает найм |
| Перевод | libraries/common.xsd:21426 assign_hired_actor, Conversations.LaunchCrewTransferPod | тот же seed покинул источник, существует только на назначении, intransit=false; размещение actor отдельно | intransit/template на станции или success=true |
| Обучение | conversations.xml:853–915 семинар, skill_gain.xml опыт | тот же сотрудник, native навык до/после; consumed seminar count либо фактический источник опыта | add_skill без исходного расхода/опыта, звёзды в UI |
| Корабль | native queued/inprogress builds и ship handle; Job_Helper ветка add_build_to_construct_ship | реальная цена/платёж, обычные материалы/очередь, готовый собственный ship, корректный loadout | NPC price=0Cr, оплачено, заказ принят или объект появился без связи с заказом |
| Станция | native build plan/progress, plot/licence/blueprints, builder, construction account/offers | собственный участок/чертежи, обычные ресурсы/средства/строитель и фактически operational modules плана | create_god_station/create_station или список плана без строительства |

`transfer_money` (libraries/common.xsd:33392) возвращает **фактически переведённую сумму** через result; amount в запросе не является платёжным подтверждением. Для собственного shipyard нельзя использовать NPC 0Cr: обычные материалы/загруженность и расходы всё равно учитываются. Чужие account/asset не становятся допустимыми из-за существования handle.

## Минимальные свидетельства

Тестовая форма словаря соответствует будущим MD tables: `goal/session/kind/asset/issued/state`, `owned`, `player_helm`, `manual_order`, `emergency`, `claim_held`, `evidence`. Evidence отдельно содержит native handle, actual ownership/arrival, платёж и ресурс/skill deltas по kind. Missing не преобразуется в ноль. Для неизвестного результата `claim_held=true`; операции в observed проверяются по evidence, а не по state label. Тестовый валидатор не подтверждает существование объектов в игре: его применение к живой записи требует источника read-back.

Проверки `tests/test_effect_receipts.py` отклоняют чужую собственность, helm/manual/emergency, accepted-only, недоплату, неприбывшего/дублированного человека, рост навыка без расхода/опыта, бесплатный spawn и потерянный unknown claim. Пассажир без перехвата управления допустим. Эти отрицательные fixtures проверяют контракт, а не заменяют доменную игровую приёмку задач 3–6.
