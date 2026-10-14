# Согласованная установка621

PID54516 штатно завершён; посторонние Python/GE4X процессы не затронуты.
Установлены51 production файл, qualified_release=false; include-adapted.
Порция616–620: queued orders в MD и непосредственно перед асинхронными
supply/hire/crew effects, правильный priority context/order handles,
подготовка пары crew transfer и отложенное чтение отмены старого Manager.
Диагностические MD/Lua скопированы отдельно в tm_empire_diagnostics.

621 добавляет живое чтение player_order_guard к ответу каждой priority фазы.
MD передаёт в собственном диагностическом blackboard фактический ship и phase;
Lua проверяет контекст и читает очередь через тот же production helper.
Ответ lua_order_guard различает available/manual/неполную/недоступную очередь.
Не выполняет effects, не принимает сырой ID из внешней команды, не подменяет
MD passed. Всё приходит одним pipe сообщением, без второго Result от таймера.

validate621 XSD/scheduling PASS. Short621 подготовлен из615 с явным
governor_roles_read после5s паузы; первая shell замена CRLF не сработала,
исправлено нормализацией чтения Python до установки/запуска.

Steam запущен без дублирования параметров. Единственная последовательность
load621→short621/session44518 ждёт подключения save-menu pipe. save_004
разрешён пользователем, не перезаписывается. Пакет: два модуля/роль/старый cue,
role contract, synthetic assessment/trade decision, четыре приоритетные фазы
с restore, три страницы UI. Fresh transfer остаётся отдельным случаем из
сохранения до старогоunknown; текущая квитанция не сбрасывается.
Результат пока не получен; полный длительный gate не запущен.
