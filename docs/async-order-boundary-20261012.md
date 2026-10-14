# Очередь непосредственно перед асинхронным эффектом — source618

После617 shared MD guard проверяет очередь, но между MD approval и Lua
оплатой/crew exchange игрок может добавить приказ. Текущие Lua adapters
повторно проверяют helm/ownership, но не всю очередь. Это подтверждённый
неполный контракт3.7, не повод принимать защиту по одному MD fixture.

Штатный API подтверждён menu_map.lua: Order3 поля235–248, GetOrders3:749,
использование11085; GetNumOrders/GetOrderQueueFirstLoopIdx применяются меню.
Новый player_order_guard.lua читает этот API без изменения приказов и мира.
Для корабля проверяет loop, до32 orders и override/priority. Несовпадение
числа записей/лимит/ошибка API дают конкретную блокировку, не available.
Для станции корабельная очередь не читается; собственность/helm по-прежнему
должны проверять вызывающие adapters. Это минимальная общая адаптация
существующей очереди, не собственная система приказов.

618 пока не подключён к adapters и не установлен. Следующая порция должна
подключить проверку непосредственно до payment intent в supply/hire и до
crew exchange, затем выполнить fixtures этих изменённых границ. До этого
наличие helper не является выполненной защитой.3.7 остаётся открытой.

## Интеграция619

Подключён в supply payment до payment intent, hire payment до списания,
crew validation до check/submission native exchange. Последний повторяет
validation перед эффектом, поэтому новый приказ после check тоже блокирует
отправку. Supply/hire сохраняют rejected-before-payment с причиной, crew
сохраняет rejected-before-effect; уже оплаченные/отправленные квитанции не
переотправляются и не объявляются отменёнными этой проверкой.

Регистрация ui.xml и Register_Require_With_Init добавлены; helper загружается
перед использующими adapters. Первый dry-run выявил отсутствующую декларацию,
после исправления51 source file и все Lua зависимости прошли проверку.

Общий Lua batch619:15 fixtures PASS. Новые случаи supply/hire/crew доказывают
отсутствие списания/отправки при guard rejection; независимый guard fixture
использует реальный LuaJIT Order3 buffer с контролируемыми native read функциями
для queued override/priority, loop, превышения32, неполного чтения и ошибкиAPI.
Подмена guard в adapter fixtures проверяет их остановку перед эффектом,
не игровую достоверность GetOrders3. Живая граница остаётся открытой.
Результат сохранён lua-batch619.json. Повторный запуск старого lua614 runner
до переименования обновил lua-batch614.json; он больше не историческая квитанция
первоначального614. Исходный вывод614 сохранён в истории tool calls.
616–619 не установлены; текущая установка615, квалифицированного релиза нет.

## Статус отказа622

После установки621 UI source дополнен русскими объяснениями manual/priority,
incomplete/unavailable queue. Crew validate возвращает guard reason через
error(reason,0), поэтому pcall не добавляет имя файла/номер строки в code.
Report сохраняет тот же точный manual_or_priority_order для последующего UI.
Existing crew contract fixture подтверждает отказ после прежнего check,
нулевой новый effect и точный reason; empire_status_fixture PASS.
622 ещё не установлен; игра проверяет621. Это source/fixture результаты,
живое native GetOrders3 и показ строки должны подтвердиться игровым пакетом.
