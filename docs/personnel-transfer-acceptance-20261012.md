# Приёмка4.2 — штатное перемещение персонала

Условия проверены совместно на неизменённом production RequestTransfer/observer.
Startup fix изменил запуск Manager, а не механизм назначения сотрудника.

- Реальное назначение и прибытие: `personnel-remote-boundary-812-20261012.md`,
  scenarios813/814. Source RCU-821 → target ZKI-807, person/seed6145579947266952518,
  crew_assignment_2_393676.392. Native podarrival очистился; exact target person,
  service role, source0/target1, transit0/scheduled0/temporary0, target_docked0.
  Production receipt observed. Native save007 CRC/SHA/load подтвердил ту же
  личность и отсутствие повторного эффекта. Прибытие командой не задавалось.
- Вместимость: `.cache/tmp/station-boundary-20261011/batch-current-contracts.json`.
  Реальный target_free0 → destination_crew_role_or_capacity_unavailable;
  same_receipt1, source_member1, target_member0, same_seed1. Подготовка заполнения
  корабля не выдаётся за выполнение перевода. Назначение не отправлено.
- Цель в пути недоступна: `personnel-destination-loss-20261012.md`, точная
  crew_assignment_3_407611.92/person17869491377443404523/seed-577252696266147093.
  Native pending с podarrival407621.928; target уничтожен407611.944.
  Production observer установил unknown/transfer_destination_lost, не observed.
  Нет копии человека, нового key или повторной отправки.
- Persistence неизвестного исхода: `domain-crews-load013-20261012.json`,
  controller session37180 terminal0. После загрузки verified save013 — тот же
  key/source/person/seed, target gone, source_member0, receipt_matches1,
  receipt_state unknown, reason transfer_destination_lost. Квитанция не сброшена.
  Дополнительный read `domains-after-crews-20261012.json` подтвердил то же.

Недоступное место назначения показывается как требующее сверки, а не как
успешное прибытие: `ui/empire_status.lua` переводит transfer_destination_lost
«Место назначения утрачено или недоступно; результат перевода требует сверки».
RequestTransfer возвращает previous_personnel_transfer_unreconciled перед новым
эффектом при sent/unknown. Native preflight, свободный post/crew capacity,
source membership/seed и непосредственно предшествующие effect guards сохранены.
Подтверждённый контроль игрока/manual/priority — player-control-acceptance.

Зафиксированное ожидание при невозможности закончить маршрут честно сохраняет
unknown: погибший target не может подтвердить прибытие. Не требуется заменять
это фиктивным успехом либо создавать нового сотрудника. Положительная ветка,
отказ по вместимости и отрицательная ветка с persistence закрывают4.2.
Бесплатные корпуса/экипажи fixture — подготовка условий, не замена обычного
найма4.1 или сохранения личности. Общая приёмка6.1/6.4 остаётся открытой.
