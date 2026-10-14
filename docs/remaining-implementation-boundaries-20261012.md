# Оставшиеся границы — текущий статус вместо оценки

Актуальная приёмка18/32:5.1/6.5 закрыты после native save011/CRC/SHA/load
и exact manager seed/read-back; новый текущий статус без оценки/истории,
factory shortage/HQ ready, стандартные страницы подтверждены. Controllers
bound save/reload терминальные exit0. Большая империя3.8, потребность→эффект5.4
и остальные широкие сценарии остаются открытыми. Full run не начат.

Актуальный повтор current-contracts-retry завершён exit0 и проверен read-back.
Реальная смена manager/HQ: fresh employee «Крисс Донел», rating/history absent;
governor loss/restore снял старый AI и восстановил active/новую проекцию.
Приняты5.3/5.6, текущая приёмка16/32. Native repair hull20→80 подтверждён;
paid hire654070Cr/exact seed observed, но его старый goal retired после смены
authority — не принимается за актуальную кадровую цель. Подробная граница
приёмки: docs/current-station-status-acceptance-20261012.md. Долгий прогон не начат.
Ниже сохранён предыдущий срез; незакрытые широкие сценарии остаются обязательными.

12.10.2026: подтверждено удаление оценки менеджеров. Из исходников убраны
история, периоды, сбор производственных/торговых/ремонтных событий и оценщик.
Сохранены текущие статусы станций, потребности и штатный экономический анализ.
Сборка с изменениями установлена, 51 SHA проверен; MD/Lua/refs/UI fixture/
OpenSpec strict проходят. Короткая проверка load007 и трёх страниц завершена:
factory energycells/water shortage, HQ без дефицита, rating/history null,
projection true/74 assets/115 UI rows; обе стандартные страницы работают.
Подробности и квитанции — docs/task-state.md. Смена менеджера на новой версии
и остальные обязательные сценарии остаются открытыми;
долгий полный прогон не начат. Актуальная приёмка 14/32, широкие задачи открыты.
Сведения об установке818 ниже относятся к предыдущему состоянию.

Production815 без изменений, diagnostics817 установлены(8 SHA).
816/read817 terminal0: ordinary/priority нашли собственные подготовленные ships,
claims/orders сохраняются, mod MD missing Ship ошибок не найдено; native
replacement отклонёнpostoccupied/effectsfalse. Controller818/session24779
проверяет обычный поиск без дополнительных transport fixtures и native
освобождение должности черезpassenger/замену/period/history/restore. Итогов818 нет.

Приёмка15/32: UI5.5/5.6 приняты по status-ui-acceptance-813-815-20261012.md.
Core815 включает optional absent Ship после async exhaustion и pending factory
retirement. Оба исправления проходят текущий общий короткий пакет816.

Короткий813: remote service transfer через native assign_hired_actor реально
завершён с exact seed/source0/target1 и очищенным podarrival. Новый007 gzip/CRC/
SHA/stable проверены; reload/no-replay814 PASS. Governor ownership loss actual
old cue cancelled/projectioninactive; restore same seed/new manageractive,
stationmanager unchanged. Широкие задачи2.4/4.2 всё ещё открыты.

Историческая проверка811 при13/32 включает порционный native economic search и
согласованный pending caller/report/UI contract, sibling completion, новые имена
lifetime cue и общий фактический read-back военных/экономических приказов.
Controller811 terminal0: priority поиск после cursor42 выбрал YDU-207,3 реальные
приказы, commander совпал; ordinary negative finished/exhausted без покупки.
Status/empire/stats открылись, saved crew exact binding сохраняется. Активных pipe
клиентов по последнему terminal read нет. Legacy SearchDone guard установлен;
конкретные duplicate/legacy lookup ошибки отсутствуют. Широкая save миграция
остаётся открытой.
Штатная стройка8aff в отдельной тестовой линии после handoff772 и подготовки
материалов773 завершилась776; это не строительное состояние текущего006.
Full длительный прогон не запускался. Native crew arrival и общие/кадровые
passenger/helm/manual/priority guards подтверждены752–758; saved paid supply и
no-replay742–745. Load-handler race770 требует проверки свежего post-load запроса;
saved terminal supply прочитан777 без повторной оплаты. Military orders5ships/2goals
подтверждены785; боевой результат и autonomous fleet supply пока не приняты.

| Область | Реализованный путь | Что ещё нужно доказать/доработать |
| --- | --- | --- |
| Модуль/должность2.2/2.4 | Реальный локальный диалог683, штатный default→«Ещё»→пункт мода698; singleton2.3 принят; ValidateBinding/отзыв разрешений | Native remote710–711: тот же seed реально прибыл через штатный UI/context+template; остаются persistence нового назначения и sale/loss/rollback |
| Экономика3.2 | Штатный анализ/собственные корабли, известные предложения, добывающие capabilities | Связанные результаты добычи и сбыта; доставка дефицита не заменяет эти сценарии |
| Строительство3.4 | Чертежи/plot/funding/builder нативными действиями;586 подготовил материалы/перелёт | Live handoff772 подтвердил смену authority с неизменными key/build/spent512702Cr; paid NPC builder observed/deployed1. Own builder722–733: deployed1→строительство→native_expansion_modules_observed. Остаются native factory/plot/handoff/load и paid supply; free preparation их не принимает |
| Флот3.6 | Изолированные военные цели и AI closure, реальная собственность/снабжение | Территориальные цели728–730 наблюдены. Native ремонт731 hull20→80/service count1 подтверждён; Paid supply742 completed/consumed6118Cr/inventory0→1 и load745 no-replay
подтверждены. Fleet execution/autonomous supply ещё не приняты |
| Защиты3.7/масштаб3.8 | Общий shared guard, проверки перед эффектами, bounded batches/backoff; сбор событий для оценки удалён | Пакет всех эффектов и большой империи; текущая проекция станций ограничена32 записями, это не доказательство наблюдения всей большой империи |
| Персонал4.1/4.2 | Повторный оплаченный автономный hire/arrival671–672; штатный bulk/post перевод с защищённым unknown | Остальные типы вакансий/недостаток предпосылок, native assign_hired_actor role transfer и exact arrival752–754 подтверждены; остаются дальний transfer и persistence нового сотрудника |
| Текущий статус5.1/5.3/5.4 | Только последний штатный отчёт, работа производства, паузы, ресурсы/бюджет/шахтёры;5.3 принят, сбор оценки и истории удалён | Смена менеджера и отказ старого отчёта подтверждены; persistence/load нового назначения и потребности в обычном стратегическом цикле остаются открытыми |
| UI5.5/5.6 | Typed counts/states и поручения/персонал сохранены; строки станций переведены на текущий статус;5.5/5.6 приняты | Общая сквозная приёмка6.1/6.3 остаётся открытой |
| Общая приёмка6.1/6.3–6.6 | Установка/изоляция и диагностические инструменты | Пакет обязательных сценариев, затем≥2h всех доменов и квалифицированная clean поставка |

Кадровый путь новых операций — штатный assign_hired_actor role/post из
conversations.xml; same-dock native arrival752–754 подтверждено. Старый bulk
observer сохранён для pending receipts. Успешный возврат API не заменяет
наблюдение сотрудника, exact seed, transit/scheduled/temp и исходной записи.

