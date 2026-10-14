# Короткий пакет731–733: строительство и регистрация ремонта

Production716/installed diagnostics721, X4 PID2484, timeline autosave_01/load722.
Контроллер731 завершён: процесса python нет; receipt batch731.json содержит все ответы.
Контроллер733 завершён exit0. Полный длительный прогон не запускался.

## Строительство

Read733: expansion construction_1_393633.039, HQ0x4b6f2/build0x8c7e:
state=observed, reason=native_expansion_modules_observed, observed394363.001.
Processor0x4b613 building0/build=null, elapsed0/total0: очередь закончена.
Funding construction_funding_1_393672.808 observed, builder0x18774a
observed/deployed1 на storage0x4b612. Лимит5000000Cr/spent462702Cr.
Материалы и чертежи предоставлены диагностической подготовкой; это не
доказательство платной доставки ресурсов или обычной покупки чертежа.
Задача3.4 остаётся открытой: native factory creation, plot, handoff/load
и оплаченная доставка имеют самостоятельные условия приёмки.

## Ремонт

NativeAnalysis731 вызвал штатный GenerateShortageData раньше обычного
интервала. RepairSetup после этого prepared на own wharf DNK-255;
ship0x1e2068/hull20. RepairScenario один раз вызвал repairs_initiate[80,[]].
Фактический hull80 и ServiceEvents.repaired1 наблюдены. Service listener
waiting, registration group index3, economy observation существует,
employee/manager/session совпадают. Нет подтверждения платного restock:
сам ответ paid_order_test=false; world fixture не заменяет задачу3.6.

## Найденная ошибка диагностического протокола

RepairRead отправлял два Lua события: repair_context, затем repair_read.
Поэтому следующий read в731 получил repair_read; последующий provision_read
получил read. Ответы731 после repair_read нельзя принимать как ответы
подписанных команд. Показания корпуса достоверны как содержимое отдельного
repair_read, но идентификация запроса была сдвинута. Read733 использует
новое соединение и независимо подтверждает строительство.

Source732 объединяет оба блока в одно событие с начальным repair_read.
probe.py добавляет проверки префиксов repair/service/native_analysis:
несовпадение останавливает последовательность без повтора эффекта.
XML schema+MD scheduling validate732 PASS, Python compile PASS.
Изменение diagnostics732 и Lua723 ещё не установлены; игровая повторная
проверка протокола нужна после следующего общего обновления установки.
Ни одна задача не закрыта исключительно по этим узким свидетельствам.
