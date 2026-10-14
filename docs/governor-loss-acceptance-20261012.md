# Приёмка2.4 — утрата управляющего и восстановление

Короткий клиент `controller-lifecycle-losses-20261012.py`, session8645,
завершился с exit0. Все17+1 чтения записаны в
`.cache/tmp/station-boundary-20261011/lifecycle-losses-20261012.json`.
Production51 соответствует installed-manifest; diagnostics9 отдельно от релиза.

Тестовая prefab станция, модуль и реальный сотрудник были бесплатной подготовкой
мира. Назначение/Unbind выполнял production Roles/Runtime. Перед каждой потерей
подтверждались active Manager, прежний Manager stopped1 и неизменный менеджер
штаб-квартиры. Диагностика не подменяла runtime state либо результат отмены.

- module_loss: только отдельный модуль fixture уничтожен `destroy_object`.
  Первоначально operational1 сохранялся до асинхронного завершения разрушения;
  через3s operational0, runtime inactive, governor/manager null,
  old_manager_stopped1, причина «Модуль утрачен или не действует».
- station_loss: владелец только fixture станции изменён player→argon.
  station_owned0, inactive, governor/manager null, old_manager_stopped1,
  причина «Станция утрачена или больше не принадлежит игроку».
  Проверяется именно утрата принадлежности, общий production путь продажи
  или захвата станции; это не утверждение об исполнении торгового диалога продажи.
- actor_loss: только fixture сотрудник удалён штатным
  `remove_actor_from_room destroy=true`; actor_exists0, inactive,
  governor/manager null, old_manager_stopped1, причина «Управляющий утрачен».

Между сценариями восстановление fixture модуля/принадлежности было подготовкой
следующего условия. Повторное штатное назначение реально запускало новый Manager.
После actor_loss восстановлен исходный живой сотрудник0x4bb7a,
seed-9126173547698565463, station0x4bb73/module0x4bba2. Station manager0x4bb90,
seed-7877045512791511809 — другой сотрудник и не изменён. Runtime active,
container/station/roleobject совпадают, transit0/scheduled0/podnull, postnull.
Исходный temporary trait возвращён перед production RequestAssignment.

До и после каждой потери сохранены те же реальные квитанции:
plot_2_407495.936 observed, construction_funding_2_407556.123 observed,
construction_2_407451.359 queued, builder_hire_2_407571.206 sent,
purchase_11_402186.122 delivered. Уже назначенный оплаченный builder не удалён
и не заменён. Заявка строителя остаётся sent с честным deployment_pending;
она не объявлена завершённой и не отправлена повторно. Plot transaction count1
и точная запись -1000000Cr/time407496.027 не изменились. Платежи не обнулялись.

При inactive binding производственный CanActForGovernor запрещает новые эффекты;
shared AI state и Manager identity запрещают эффекты старого экземпляра даже
после нового active binding. Старые claims/неизвестные квитанции не очищаются.
Статус потери имеет governor0/active0 и не выдаёт старые данные за управление.
Восстановление проекции может ожидать свежего отчёта: это не подстановка старого.

Save/load/rollback проверены совместно с существующими игровыми свидетельствами:
`governor-assignment-acceptance-20261012.md` — exact binding двух должностей после
CRC/SHA verified save012; `ship-purchase-contract.md` и принятая3.5 — реально
оплаченный native handoff/save-load без повторной оплаты; `player-control-acceptance-20261012.md`
и fixtures786 — sent/unknown/replay и отзыв разрешения до финансового эффекта.
Оба lifecycle запуска загружали тот же verified save012: исходный сотрудник,
оплаченные ключи и принадлежность восстановились из этого мира; данные погибшей
fixture первого несохранённого запуска не переносились в следующий.

Продажа/демонтаж модуля использует тот же production predicate наличия,
operational и членства module в station, а продажа станции — утрату ownership.
Оригинальные модули и чужая собственность не менялись. Эти условия вместе
с принятыми replay/save-load границами закрывают2.4; общий прогон6.1/6.4 ещё открыт.
