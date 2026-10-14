# Короткая проверка строительства 643–647

Тестовый мир save_004; сохранение не перезаписано. Источники: JSON в
`.cache/tmp/station-boundary-20261011/`: read643, builder644, resources644,
read645, read646. Контроллеры завершились; долгий прогон не запускался.

В read646 (player.age 403107.668) штатный строитель 0xa5be назначен на
PFY-706 / 0x4b89e, build 0x1dee. Сохранился оплаченный ключ
builder_hire_2_402626.891, native_hired, fee/paid 50000 Cr; назначенный
строитель совпадает с receipt. Deployed=0, expansion queued,
builder_arrival_pending. Бюджет стройсклада 3108364 Cr, wanted 996797 Cr,
processing=1, missing resource types=0. Эти поля не доказывают прогресс.

Команды 644 подготовили мир: приблизили того же строителя к стройскладу
(2438.5 м после перемещения) и добавили недостающие 542 claytronics,
1083 energycells, 1980 hullparts. Никакого повторного найма, платежа,
принудительного развёртывания или завершения строительства не было.
Добавленные ресурсы не являются доказательством платного снабжения мода.

Сверка ui/construction_builder.lua с штатным menu_map.lua подтверждает
CreateDeployToStationOrder и station в параметре 1. Штатный
order.build.deploy.xml сам рассчитывает get_building_position, безопасную
позицию, выполняет move_to и лишь затем deploy_construction_vessel.
Причина задержки пока не установлена; предположение о старом маршруте
после диагностического warp не подтверждено.

Изменение диагностики 647 добавляет только чтение native processor clocks,
isbuilding, requiresconstructionvessel, constructingmodule, расстояния до
storage и get_building_position, текущего commandaction и числа orders.
validate647.txt: MD schema и scheduling PASS. В игру изменение ещё не
установлено: оно предназначено для следующего согласованного пакета.
Установленная диагностика остаётся 640, production 635. Задача 3.4 открыта.
