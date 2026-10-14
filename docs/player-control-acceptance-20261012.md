# Приёмка3.7 — игрок и ручные приказы

Короткий controller-control-boundaries-prepared/session51820 завершился0.
Единственная подготовка создала свободный корабль с настоящим NPC-пилотом;
дополнительный cockpit служил только тесту штурвала. Исходный player container
и состояние управления восстановлены в finally, priority_restore passed1.
Ранее первый клиент обнаружил not_prepared и остановился без смены игрока;
эти ответы не принимались как успех.

Авторитетная квитанция — control-boundaries-prepared-20261012.json:

- Passenger: container0x1b20e1, controlled=null, native guard available,
  тот же pilot/seed, passed1. Находящийся пассажиром игрок не исключает корабль.
- Helm: controlled0x1b3a62, native asset guard и кадровый guard player_helm,
  passed1. Отдельный Lua order guard намеренно проверяет очередь, а штурвал
  финансовые исполнители проверяют отдельно GetPlayerControlledShipID.
- Manual: реальный Wait override1, очередь1, order.exists1;
  MD и Lua queue guards manual_or_priority_order, passed1.
- Priority: реальный Wait priority1, очередь1, order.exists1;
  MD и Lua guards manual_or_priority_order, passed1. Отмена предыдущего
  тестового manual order сделана только диагностикой при подготовке этой фазы.
- Независимый runtime сохраняет active/один Manager/goals3; native строитель
  processing1: elapsed21.9774→24.6708 при переходе к helm, затем27.2958→29.9099
  в manual/priority. Тот же mining claim/commander продолжает MiningCollect.

Check_adapted_manager и XML scheduling прошли для текущего установленного
пакета: общий runtime guard непосредственно перед эффектами копированной
13-script closure, отдельные pre-effect guards recovery/персонала и Lua
платежей. fixtures786.json проверяет смену разрешения/manual между check и
submit, unknown/replay для hire/transfer/supply/purchase; эти исполнители не
менялись в последнем station catalogue пакете. Originals/NPC AI не изменены.

3.7 принимается по всем указанным условиям. Это не принимает общий двухчасовой
автономный прогон6.4. Тестовые Wait ограничены60s; прочие реальные приказы
игрока не отменялись.
