# Текущий статус станции после смены сотрудника и загрузки

Принимаются5.1 и6.5. Производственная сборка51 files и диагностика8 files
установлены с проверкой SHA. Контроллеры status-save-bound/session34429 и
status-reload-bound/session71115 завершились exit0. Квитанции в
`.cache/tmp/station-boundary-20261011/`: status-save-bound-20261012.json,
verified-status-save-bound-20261012.json, load-status-reload-bound-20261012.json,
status-reload-bound-20261012.json.

## Сотрудник и штатная работа

Штатный assign_hired_actor освободил station manager HQ в passenger и
назначил Крисса Донела, seed-7877045512791511809. Read-back подтвердил
current_new1/transit0/source_member0, независимые governor/EmpireManager
не изменились. При отсутствии свежего отчёта прежнего назначения статус
был неизвестным, старые assessment/confidence/period/history отсутствовали.

Результат сохранён в отдельном save011:91638431 compressed и748587930
uncompressed bytes, gzip CRC/stability PASS, SHA
9b05d50051d51e693296f04941643775050f08ccc9b0e107a326939e4b456644.
Все17 прежних файлов сохранений сохранили size/mtime. Штатный список
подтвердил save011/title/rawtime1791809808, native LoadGame принял этот слот.
После загрузки exact new seed/current_new1/transit0 сохранились, governor
и имперский управляющий не заменили сотрудника станции.

## Актуальность и потребности

До нового завершённого обхода страницы имели20–22 строки и не содержали
station_status. Затем появилась проекция74 объектов/2 станции/117 строк:
snapshot_from393716.833 и snapshot_to393726.840, без будущих меток времени.
Загрузка снимает сохранённый Snapshot/Sources и меняет ObservationSession;
незавершённые обходы привязаны к исходному Manager/session и сбрасываются
при их смене или откате времени. UI fixture отвергает future observation,
невалидные workstate и отрицательные значения, не превращая неизвестность
в нулевой факт. Сам обход и вывод ограничены, окно явно частичное.

ФабрикаKMT-485: needs_attention, производственный модуль waiting_resources1,
реальный cargo energycells0/water0 и buy_amount425/1136; проблемы показывают
оба ресурса. Неизвестные предложения продавца остаются null, не нулевой ценой.
HQ: Крисс Донел/ready, production_total0, отчёт не выявил дефицита. ready
не считается доказательством эффективности. Ранее current-contracts-retry
подтвердил также текущую нехватку шахтёров у тестовой верфиRNU-509.
В обеих свежих station_status assessment_present/history_present=false.
Старый сотрудник не возвращён принудительно; работа штатных менеджеров
продолжается. Стандартные empire18/stats85 строки открылись после загрузки.

## Границы свидетельства

Не принимаются общий lifecycle2.4, обеспечение потребности5.4, все кадровые/
военные/строительные сценарии, большая империя3.8 и полный двухчасовой прогон.
Сохранённая supply6118Cr/consumed квитанция лишь прочитана, новая оплата
не выдавалась. Crew capacity preparation_unavailable и неподготовленный
roles_read/passed0 не считаются успешной проверкой этих отдельных сценариев.
