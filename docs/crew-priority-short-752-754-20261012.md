# Короткий пакет кадров и приоритетов752–754

Production749/diagnostics752 установлены с проверкой51production SHA и
диагностических копий. X4 PID42132, native load save005 accepted. Controllers
752/session29015 и754/session33666 завершились exit0; активных pipe нет.

## Реальный штатный перевод

RequestTransfer использовал assign_hired_actor actor=[Source,Person], role,
после native check=true. Source0x1859c2, target0x1859cc, один док0xcb3f,
person10619398833150267955/seed-7827345240559283661. Подготовка создала только
условия (корабли/нативный экипаж), не изменяла arrival/transit/receipts.
752 actual target member1/service, source0/transit0/scheduled0/temp0.
754 production observer: observed393672.81, issued393644.672,
native_crew_arrival_observed. Эффект вызван один раз, в754 только чтение.
Far transfer и persistence нового назначения этим результатом не доказаны.

## Общий ship guard

Тестовый корабль0x186152 получил native claim goalStart до отчёта setup;
setup claimed_by_other_goal не означал сбой защиты. Source diagnostic755
выбирает существующую цель того же менеджера во всех фазах, без изменения claim.

754 на реально подготовленных условиях:
- passenger: player.container0x186152/controllednull, pilot unchanged1,
  reasonavailable, passed1;
- helm: новый cockpit0x18de7a создан непосредственно перед teleport,
  controlled0x18de7a/reasonplayer_helm, passed1;
- manual: real Wait override1/priority0, orders2, createdexists1,
  reasonmanual_or_priority_order, passed1;
- priority: real Wait override0/priority1, orders2, createdexists1,
  reasonmanual_or_priority_order, passed1;
- restore: исходный player.container/control0x19cbe, passed1.

Новый Wait имеет timeout60s. Причина исчезновения старого бессрочного Wait750
не доказана; не приписывать её production. Здесь защищённые приказы существуют
и сохраняются до реального наблюдения. Governor seed/member/roleentity не
менялись, обычный pilot пассажирского корабля остался тем же.

Source production754 (не установлен) объединяет bounded32 manual/priority/helm
guard найма и перевода: до hire payment, после payment/до assignment, перед
transfer source/target. XSD/scheduling755 PASS. Эти новые hire checks ещё
не прошли игровой отрицательный сценарий. Общие задачи3.7/4.2 остаются открыты
до полного объёма их критериев; полный длительный прогон не запускался.

Результаты: .cache/tmp/station-boundary-20261011/batch752.json, batch754.json,
load752.json, install752.txt, validate755.txt.
