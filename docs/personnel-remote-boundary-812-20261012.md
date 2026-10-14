# Подготовленная граница внешнего перевода персонала

Production RequestTransfer уже использует штатный assign_hired_actor и
Conversations.NPCAssigned. Check=true и эффект получают тот же реальный
Source/Person/Target/Role. Production guard проверяет governor/goal lifetime,
собственность, protected employee, native capacity, manual/priority control.
Receipt предшествует эффекту; read-back проверяет точный seed и native transit.
Самостоятельный транспорт или новый кадровый планировщик не вводятся.

Принятые короткие пробы752–758/800–802 доказывают same-dock arrival и сохранение
этого перевода. Они не доказывают путь к недокованному удалённому кораблю.

Diagnostic812 добавляет отдельный сценарий, который не сбрасывает старые markers:

- crew_remote_prepare создаёт source с реальными native service people на доке
  HQ и target в20–25km в том же zone; target имеет свободные места. Фактический
  Person/seed выбирается из source.people, а не создаётся как disconnected actor.
- crew_remote_transfer один раз вызывает production RequestTransfer с active
  native economy GoalCue. Attempt сохраняется перед вызовом. Key сохраняется
  только при ответеsent; никакая старая receipt не принимается как новая.
- crew_remote_read только читает exact binding и обе membership записи,
  target seed/role/transit/scheduled/podarrival/temporary. Receipt считается
  относящейся к сценарию только при совпадении key и всех исходных bindings.
- save_remote_personnel использует прежний native free-slot checkpoint путь
  с новым фиксированным marker. Requested не означает готовый file/save.

Сценарий установлен и выполнен813. RCU-821 → ZKI-807, key
crew_assignment_2_393676.392, person/seed6145579947266952518. Native podarrival
был393686.409 и затем очистился; source_member0/target_member1, exact seed,
service, transit0/scheduled0/temporary0, target_docked0. Production observer
подтвердил observed. Это actual remote arrival, не подставленный результат.

Controller813 terminal0; provision и три UI страницы также прочитаны.
Новый save_007 requested и проверен как стабильный gzip с корректным CRC:
91646978 compressed/748297818 uncompressed bytes,
SHA e28f7d00b07df9f9d777cfa135befcd90738a93f4e90b912e4da812593428b2f.
Native list814 подтвердил slot007/title/time1791791925; loadaccepted.
Exact key/person/seed/source0/target1/service/flags0/podnull/observed сохранились.
Повторные prepare/transfer отказали effectsfalse; следующий read имеет прежнюю
квитанцию и membership. Controller814 terminal0. Remote persistence подтверждён.
Позднее после смены управляющего автономный personnel создал другую receipt;
read815 поэтому receipt_matches0/unmatched, но прежний человек остаётся на
target с тем же seed и flags0. Не выдавать unmatched новой receipt за replay
или потерю уже подтверждённого прибытия.

Критерий короткой пробы: наблюдать реальное native перемещение, а не толькоsent;
точный человек должен отсутствовать в source и присутствовать вtarget с той же
ролью/seed без transit/scheduled/pod/temporary. При unavailable/pending/unknown
не повторять эффект и не выставлять прибытие командой; продолжить независимые
сценарии. После реального arrival допускается новый free-slot checkpoint,
file/gzip/native-list проверка и reload с exact person read-back.

Task4.2 остаётся открытой до покрытия её реальных условий. Этот документ
фиксирует готовый диагностический путь, а не приёмку или новую product функцию.
