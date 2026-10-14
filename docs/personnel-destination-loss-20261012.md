# Потеря пункта назначения во время перевода

Diagnostics11, production51 с исправленным startup barrier. Короткие клиенты
`controller-domain-package-short-20261012.py` / session39841 и
`controller-domain-package-followup-20261012.py` завершены с exit0.
Квитанции находятся в одноимённых JSON под `.cache/tmp/station-boundary-20261011/`.

Подготовлены два отдельные бесплатные scout fixture и настоящий service crew
member. Production `RequestTransfer` вызван с действующим Manager/Goal и точными
Source/Target/Person/seed. Диагностика не задавала результат перевода.

В407611.92 создана квитанция `crew_assignment_3_407611.92`:
source MNV-963, target NWU-455, person17869491377443404523,
seed-577252696266147093. После штатного назначения source member0,
target member1 с тем же seed, podarrival407621.928. Начальный pending/target
membership не выдаётся за физическое завершение перемещения.

В407611.944 уничтожен только отдельный target fixture корабль до podarrival.
Через6s target уже отсутствовал, receipt ещё sent; это промежуточный результат.
Последующее чтение407661.714: та же квитанция и seed, state unknown,
reason transfer_destination_lost, source member0, target отсутствует.
Новый человек либо новый ключ не создавались, повтор перевода не выполнялся.

Состояние сохранено штатным SaveGame в новый заранее проверенный свободный
save013, title TM Empire boundary package, game age407836.492.
Физический файл93318252 bytes; gzip CRC и неизменность size/mtime во время
чтения проверены. SHA c8b2275ac4823d663f8ca7fa6d766a9756d41956feb18010fce8c6b7f4150d38.
Все markers присутствуют: точный crew key, подготовленная NPC outlet station,
старый construction key и новый marker записи слота. Старые слоты не перезаписаны.

Это подтверждает честный неизвестный исход при исчезновении цели в пути.
Положительный реальный remote arrival и capacity rejection описаны отдельно
в personnel-remote-boundary-812-20261012.md и текущих contract receipts.
Новый read-back unknown после load013 ещё не принят на момент этой записи;
задача4.2 пока открыта. Никакого длительного прогона ради этого случая нет.

Проба сбыта/угрозы этой же порции пока не принята: созданные test trader,
четыре fighters и Xenon fighter оказались без native AI pilots. Это ошибка
подготовки мира, а не доказательство отказа рабочих алгоритмов. Исправление
diagnostics создаёт пилотов штатным create_control_entity только в фиксированных
fixture объектах; штатный наём4.1 этим не заменяется. Подготовленные корпуса
и условия сохранены в013, повторно создавать их не требуется.
