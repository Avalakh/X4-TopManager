# Асинхронные разрешения: исправления пакета 648

Проверены producer/consumer и reconciliation уже имеющихся запросов.
Обнаружены две пропущенные ветки в TM_Empire_Runtime.RevokePurchaseApproval:
`$tm_empire_builder_request` в состоянии `recovery_approved` и
`$tm_empire_station_funding` в состоянии `approved`.

Оба состояния разрешают отложенному Lua consumer создать новый штатный
заказ либо перечислить деньги. При смене/утрате governor теперь разрешение
отзывается с governor_binding_changed. В RevokeGoalApprovals добавлено
recovery_approved; существующий обход ancestry/key сохранён.

Это не отменяет уже оплаченный строительный заказ. Result sent/unknown
не переписывается и оплата не повторяется. ObserveStationFunding сначала
проверяет сохранённый payment result, затем отказ до эффекта: факт уже
прошедшего платежа имеет приоритет перед revoked approval.

Дешёвые проверки: validate648.txt MD schema/scheduling PASS;
construction_builder_fixture.lua PASS, включая revoked recovery без нового
заказа/платежа; station_funding_fixture.lua PASS. Это проверки границ кода,
не игровая приёмка всех требований 2.4/3.7. Чекбоксы остаются открытыми.
Production source изменён, установленная версия остаётся 635.

Дополнение649: восстановление оплаченного legacy builder заказа теперь
повторно читает текущий request непосредственно перед созданием заказа и
проверяет recovery_approved/key/ship/station/storage/budget. Обычный submit
уже имел такую проверку; recovery теперь сохраняет ту же границу.

RestoreSupply после load раньше переводил payment_approved receipt в
unknown при неподтверждённом платеже, оставляя board request в
payment_approved. Теперь этот request с совпадающим ключом отзывается;
payment evidence остаётся нетронутым. Подтверждённый paid продолжает
штатную ветку согласования. Не добавлены повторный платёж или заказ.

validate649 MD/scheduling PASS; check_adapted_manager PASS (13-script
closure, shared guards/state); construction_builder_fixture PASS.
Игровая проверка отмены/load входит в следующий пакет, ещё не выполнена.
