# Приёмка вкладки — задачи5.5 и5.6

Production810/UI без последующих изменений, diagnostics813–814. Короткие
controllers813/814 и read815 завершились exit0. Это приёмка представления
данных и жизненного цикла вкладки; исполнение всех экономических/военных
задач и полнота причинных правил остаются отдельными открытыми критериями.

## Собственность и поручения

В813 реальный read:2 станции/72 корабля, MD/Lua snapshot:74 объекта,
2 station/30 S/31 M/9 L/1 XL/1 other. Сумма типов74; состояния
waiting8/sent2/unknown0/excluded64 также дают74. Показаны64 строки;
UI явно подписывает частичное окно и интервал снимка, не выдаёт его за
полный список или мгновенное состояние постоянно меняющегося мира.

Projection проходит проверку schema/types/counts в production Lua. Источник
counts — полный порционный scan собственной собственности; ряд исключённых
объектов не означает отсутствия собственности. В813 status frame29 имел96
body rows; штатные empire342/stats405 также открылись. В815 status frame774
имеет136 rows после возобновления работы нового управляющего.

Поручения различают planned/sent/observed/unknown/waiting; sent для existing
transport требует actual owned order refs, не одного выбранного плана.
В815 три existing transports имеют sent и конкретные имена исполнителей,
следующие выбранные действия — planned. Перевод персонала813/814 имеет
точный source/person/target и observed после native arrival; его факт
отдельно проверен по actual people membership/seed/role. UI выводит участников,
причину и подтверждённую оплату отдельно от результата. Pending purchase
старого назначения после смены authority показывается unknown, не повторяется
и не становится автоматически успехом нового управляющего.

## Оценки и утрата управляющего

Provision815 содержит actual менеджеров Халило Мо/KMT-485 и
Тэмманчассат/XZS-342, период393716.821–393717.867, samples2. KMT — production,
наблюдение0/1 производств и ожидание ресурсов; ответственностьunknown/low.
XZS — other/unknown/low, без штрафа за отсутствие производственной прибыли.
Недостающие сведения явно перечислены. UI выводит назначение станции,
результат/confidence, период, обеспечение, причины и ответственность из
этой же валидированной проекции. Live budget797 ранее подтвердил отображаемую
причину insufficient_provision; один простой или низкая прибыль не считаются
ошибкой менеджера. Тексты объясняют нехватку и неизвестность по-русски.

814 changed owner только одного actual governor, не станции. Production
ValidateBinding снял binding и отозвал authority. Сразу projection_governor0/
active0; отложенный read:old_manager_exists0/stop1. UI status frame165 — одна
строка отсутствующего управляющего, без stale active. Штатные empire193 и
stats256 работают. Station manager unchanged1 и employee same_seed1.

Возврат того же employee:restore_resultbound, затем другой actual manager
active. Read815:old_manager_exists0, old_authoritymanager_instance_mismatch,
projection_governor1/active1, station_manager_unchanged1. Status снова показывает
актуальные поручения и оценки. Смена сотрудника станции, продажа/разрушение
модуля и широкие rollback сценарии этим не принимаются.

## Обнаруженная отдельная ошибка

После814 журнал показал CheckRunningActions.$ActionReportDef.$Ship: отрицательный
async search уже завершён, Ship ещё отсутствует. Source815 делает этот lookup
optional и исправляет аналогичный pending factory subaction lookup; генератор,
closure, MD schemas/scheduling и четыре actual caller offline branches PASS.
Source815 ещё не установлен. Эта ошибка учёта не подменяет критерии3.2/3.8 и
остаётся в общем отчёте для следующего пакета. UI код здесь не менялся.

Свидетельства: batch813.json/load813.json/save813-file.json,
batch814.json/load814.json/read815.json в .cache/tmp/station-boundary-20261011.
