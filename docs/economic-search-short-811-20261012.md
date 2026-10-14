# Короткий пакет811: priority поиск и миграция

## Установка и мир

51 production файлов и диагностическое расширение установлены с проверкой SHA;
снимок manifest install811.json. Core810 содержит optional legacy guard; diagnostic
содержит отдельные no-replay markers для ordinary иpriority запросов. X4 штатно
завершена и запущена черезSteam. Native save list/load006 accepted;006 не изменён.

Команда economic_transport_prepare создала реальные own M транспорты ISJ-044
иPFU-098 по зарегистрированному native macro ship_arg_m_trans_container_01_b_macro,
с native loadout/pilot и вместимостьюenergycells. Это только подготовка мира,
не доказательство покупки, назначения или того, что AI выбрал эти корабли.
Claims/orders/search results не подставлялись.

## Результаты

Ordinary native request393682.462 прошёл несколько порций и завершился exhausted:
cluster24/cursor13 →cluster31/done1 →finished/searchcueinvalid, purchase null.
Наличие двух подготовленных транспортов не позволяет объявить этот сценарий
положительным; пригодность/диапазон этих кораблей отдельно не установлена.

Priority request393690.564 использовал штатный диапазон5 и приоритетную подготовку:
cluster19 →prepare cluster26/cursor42 →cluster31 →candidate cluster46/cursor4.
Таким образом, действительный cursor пережил несколько порций и прошёл32 элементов
подготовки; выбор не обрезан первыми32 кандидатами.

Completion далcandidate_found, committed1. Алгоритм сам выбрал существующий
YDU-207/0xcc3c, а не один из подготовленных транспортеров. Реальный owned claim
state sent; native orders3. Commander0x4c197 совпадает с expectedHQ0x4c197.
Покупка отсутствует. Следующее read через2s сохраняет тот же корабль, issued,
результат и3 приказа; эффект не повторялся. Это подтверждает adapted priority
selection/stock effect tail и реальное назначение, не торговый результат.

После загрузки811 log содержит0 duplicate cue,0 legacy SearchDone lookup errors
и0 ReadOwnedOrderEvidence errors. Это исправление обеих конкретных source ошибок
807–809 на старой сохранённой структуре006, не всех save/rollback сценариев.

Provisions иfinal read получены; status frame29/body96, empire342/stats405 открылись.
Сохранённыйcrew_assignment_1_393644.637 остаётсяobserved с тем же сотрудником и
реальным членством. Controller811/session36637 terminal exit0.

## Границы доказательства

Не принимаются этим пакетом positive ordinary assignment, priority warebasket
tie-breaking относительно всех доступных альтернатив, исчезновение кандидата
во время поиска, смена authority, сохранениеpending search, результат торговли,
вся задача3.8 и длительная6.4. Широкие task checkboxes остаются открытыми.
Повторная проверка штатного внутреннего AI без изменения его границы не нужна.
