# Добыча и продолжение стройки — 13.10.2026

Свежие pipe controllers domain-prepackage-audit и domain-independent-repeat
завершились exit0. Полные ответы сохранены в .cache/tmp/station-boundary-20261011/
domain-prepackage-audit-20261013.json и domain-independent-repeat-20261013.json.

## Принятая узкая граница добычи

MiningDeliveryTrace наблюдает реальный event_trade_completed: продавец точный
назначенный шахтёр DON-919, покупатель точная EKA-355, ware.silicon, amount>0.
Оба чтения: stateobserved, amount980, issued408059.845, observed408614.587.
До и после он остаётся подчинённым EKA-355 с sent claim; реальный приказ
MiningCollect → DockAt → MiningCollect. Диагностика не выдавала приказ добычи,
не добавляла кремний в корабль и не подставляла событие доставки. Новая
mining_resources не вызвана и в live c недоступна. Native производство
wafers выросло5092→5337→5383; это не подмена подтверждения доставки.
Добывающая граница3.2 подтверждена; полный3.2 не закрыт: сбыт ещё не наблюдён.

## Строительство

Тот же build0x6d8/processor0x1a197/платный hired builder0x1a228:
часовщик pier_bor_harbor_03_macro elapsed187.482→1007.414/1140,
затем текущим стал defence_bor_tube_01_macro elapsed0/120. Это реальный
переход native стройки между модулями, не принудительное завершение.
Полный завод и обычное строительство tm_empire_control_arg ещё не приняты.

## Покупки

Номера purchase12→24 сами по себе не означают12 оплат. Есть заявки waiting
purchase_price_or_money_changed; текущий24 building/built с nativeID270185ULL,
price/paid1101651Cr, money2984399Cr. Ранее наблюдён reconciled nativeID264772ULL
paid1174516Cr. Отдельный12 weaponcomponents delivered ship0x1890f4/29000cargo,
те же старые water/energy actions сохраняют свои start/ship/expiry.
Повторная оплата одной exact заявки этими чтениями не подтверждена;
не объявлять весь будущий цикл защищённым лишь по двум ответам.

## Подготовленный пакет диагностики d

Источник: отдельное tests/diagnostics/extension, в production не включается.
- domain_threat_range: однократная сцена с точным свободным транспортом,
  неизменным escort reference для двух warp, только Xenon получает Attack.
  Native attacked events отдельно фиксируют настоящий удар по транспорту
  и собственные атакующие корабли с exact claim/goal/order evidence.
  Обычная самооборона без подтверждённой военной цели не принимается за AI.
- domain_large_assets: однократно192 пустых небольших hulls без orders,
  claims/бесплатного персонала; счётчик реальных созданий и scan cursor.
  Подготовка не доказывает bounded обработку: нужны последовательные reads.
- save_scenario_checkpoint|preflight_save_015_absent: штатный SaveGame,
  физическая проверка клиентом + native slot absence + once blackboard.
  Существующие slots не перезаписываются; проверка CRC/SHA/load обязательна.

MD XSD/cue scheduling и native Lua5.1 syntax PASS. Это только source;
живой PID77408 используетc. Установка d предыдущего turn остановлена
WinError32; последующие правки не устанавливались. Пользователю предложено
сделать quicksave, ответ ожидается; игру пока не закрывать. Full2h не начат.


Короткий пакет e: source XML/cue/Lua PASS; installed11/SHA receipt scenario-e-install-20261013.json. Verified015 загружен штатно. Контроллер scenario-package-e-short-20261013.json завершился exit0; входящая диагностическая атака10HP дала один engine event, но ответ собственного флота не наблюдён. Удалён ровно один пустой тестовый ZXU783, living192→191, boundedscan session11 продолжился; нужна следующая законченная выборка после асинхронного удаления. Factory elapsed57→178/1140, purchase15 building; сбыт не принят. Новый checkpoint016 создан без перезаписи и проверен stable/CRC/SHA, receipt save016-scenario-checkpoint-20261013.json. Эти частичные свидетельства не закрывают 3.2/3.4/3.6/3.8 или полный прогон.
