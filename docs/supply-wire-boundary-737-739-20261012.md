# Снабжение: реальная ошибка MD/Lua737 и исправление738–739

## Игровой результат737

Controller737 session42996 terminal exit0; load737 autosave_01 accepted.
Установлены production734/diagnostics736, X4 PID54844 (штатно завершён739).
Setup создал один docked own S scout0x187592 у известной NPC wharf0xd040,
ownerparanid. Это free world preparation, не оплаченная покупка корабля.
Запас satellite_mk1 before0. Quote supply_1_393634.078 запросил production
QuoteRestock. Step завершил rejected_before_effect→consumed с причиной
empty_supply_quote; inventory0, paymentkeynull, paymentstatenull, buildnull.

Debug.log содержит первопричину:
`md.TM_Empire_Supply.QuoteRestock: Invalid table key at position 1: satellite_mk1`.
MD пытался создать таблицу с произвольным string key `$Macro.ware.id`.
Следовательно пустая цена вызвана wire contract, не отсутствием NPC-верфи.
Деньги не списывались, очередь снабжения не создавалась, ошибка собрана.
Обычные UI status→empire→stats→status отрисовались (8/18/85/8bodyrows),
при этом первый полный snapshot ещё собирался; это не полнота UI приёмки.

## Минимальная адаптация738–739

MD передаёт фиксированные `$ware` и `$amount` вместо динамического ключа.
prepare_supply конструирует обычную Lua карту `[request.ware]=request.amount`
перед существующей quote_supply. Остальные stock price/discount/payment/build
пути не изменены. Legacy Lua request.wares оставлен читаемым.
Фикстура supply_payment теперь проверяет именно MD wire форму, наряду с
долговечными paid/unknown/no-replay и manual/helm guards. Не имитирует
native товарную цену; реальное ценообразование повторяется в739.

validate738 MD XSD/scheduling PASS. supply_payment_fixture PASS,
включая MD ware value converted to native supply price map.
Добавлены русские причины потери authority и отказа price во вкладку;
empire_status_fixture PASS. Ни одно свидетельство не закрывает paid fleet
supply или полный change до настоящего результата игры.

## Повторный короткий пакет739 (в работе)

Production738 + UI739 установлены51файл/hash verified; diagnostics736
сохраняется. Новый X4 PID56116, Steam без дополнительных параметров.
Controller739 session32930: autosave_01→одно setup/quote→production step/
read bounded3x3s→UI→save_validation только свободный save_009.
Save requested не считается сохранением: нужны native list/file/load.
Старые save_004/autosave_01 не перезаписываются.
