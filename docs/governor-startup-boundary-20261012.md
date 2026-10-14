# Смена управляющего при старых назначениях

Первый короткий сценарий `lifecycle-load-20261012.json` назначил реального
сотрудника на отдельную station/module fixture, но новый Manager не запускался.
Повторное чтение `lifecycle-read-active-20261012.json` подтвердило runtime bound,
manager null и причину «Ожидание завершения прежних приказов управляющего».

Причина в генераторе копии `TM_PlayerManagerWatch`: запуск требовал пустых
общих групп `OwnedClaims` и `StationReassignments`. Старое защищённое либо
неразрешённое назначение тем самым блокировало и независимые активы.

Условие удалено в `tools/adapt_native_manager.py`; closure пересобран штатным
инструментом. Запуск всё ещё требует проверенного binding/state bound и
отсутствия зарегистрированного Manager. Прежний Manager отменяется при Unbind.
Его заявки и квитанции не очищаются, неизвестные эффекты не повторяются.
Проверки Manager identity в `CanActForGovernor` и shared AI state запрещают
прежнему экземпляру новые эффекты; guards конкретных claims/reassignments
удерживают соответствующие активы до согласования. Поэтому смена сотрудника
не делает старые защищённые активы доступными новому экземпляру.

XML/scheduling, closure13 и полный install preflight51 прошли. Рабочий пакет
установлен после штатного завершения X4, SHA совпали с installed-manifest.
Новый `lifecycle-startup-fixed-20261012.json` / session85427 terminal0 подтвердил:
fixture governor0x186f60, runtime active, новый TM_PlayerManager,
old_manager_stopped1, home_manager_unchanged1. Exact исходный governor seed
-9126173547698565463 сохранён. Игровая проверка не выдаёт весь релиз за принятый.
