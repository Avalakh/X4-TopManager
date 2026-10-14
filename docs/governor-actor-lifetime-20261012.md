# Время жизни назначенного управляющего

## Наблюдение527

Installed526, load526 accepted/save_004, short527 terminal0.
До смены контекста actor0x4c264 находится на station0x4c25e, roleobject
той же станции, controlpost=null, intransit0/scheduled0/podnull;
Registry active, manager exists. После перехода игрока на fixture ship
actor перестаёт существовать, runtime inactive, StopReason «Управляющий утрачен».
Пассажир до этого подтверждён available, точный возврат игрока подтверждён.
Утрата actor не позволяет принять последующие manual/priority проверки.

## Штатная граница и минимальная адаптация529

NPC_Instantiation.xml:2168+ ищет temporaryentity при удалении instantiated NPC
с покидаемого объекта. OnRemoveInstantiatedNPC:2198 и OnNPCLeft:2213
уничтожают только временные экземпляры. Это штатное удаление представления
NPC, которое несовместимо с отдельной должностью, привязанной к живому actor.
common.xsd:7885+ и35929+ определяет штатный set_entity_traits temporary.

BindGovernor после всех проверок назначения сохраняет исходный temporary
одного назначенного actor и устанавливает temporary=false. ValidateBinding
выполняет это же для существующего сохранённого назначения, включая загрузку.
UnbindGovernor и ветка недействительного назначения восстанавливают исходное
значение живого actor и удаляют сохранённое значение. При уничтожении actor
никакого создания нового NPC, восстановления звёзд или повторного назначения
нет. Остальные признаки и штатный controlpost не изменяются.

Задача2.4 не закрыта: связь наблюдения527 с temporary cleanup должна получить
игровое подтверждение повтором с тем же сотрудником. Это проверяемое исправление
выявленной несовместимой границы, а не доказательство всех случаев утраты.

## Проверки

validate529.txt: MD/XSD/scheduling PASS. check_adapted_manager.py PASS:
изолированные ссылки,13 AI scripts, публикация общего состояния.
Installed530:50 файлов с SHA проверены; отдельный diagnostic source528 содержит
person/seed/station и actor/people/roleentity/StopReason read-back.
Load530 terminal0/accepted/save_004, short531 terminal0. Долгий прогон не запущен.

## Игровое подтверждение531

Начальный и конечный read: actor0x4b527, station/container/roleobject0x4b521,
intransit0/scheduled0/podnull, controlpost=null. На всех фазах governor_exists1,
person9320570526010986153, seed-9126173547698565463, member1, roleentity0x4b527,
StopReason=null. Начальный и конечный runtime active/manager_exists1.
Изменились только transient IDs относительно запуска527; seed сохраняет
личность сотрудника из исходного save_004. Подмены employee не было.

Пассажир: реальный player.ship0x188eb2, controlled=null, reasonavailable,
passed1; NPC-пилот неизменён. Manual: override1, reasonmanual_or_priority_order,
passed1. Priority: priority1, та же причина, passed1. Restore: исходный
player.ship/control0x778ff, passed1. Оплаченный персонал этой world fixture
не проверялся. Helm в этом пакете passed0: кресло NPC-пилота занято, штатный
teleport_player не передал управление; сценарий не засчитан.

В source532 добавлен отдельный disposable helm ship без занятого кресла,
не затрагивающий NPC-пилота пассажирской fixture. Эта новая граница пока
не установлена и не проверена в игре. Она проверяет реальный player_helm
на отдельном корабле, а не обещает посадку в занятое кресло первого корабля.
MD/XSD/scheduling532 PASS. Source533 не вызывает set_entity_traits повторно,
если actor уже permanent; точная логика сохранения/возврата флага сохранена.
Задачи2.4 и3.7 остаются открытыми по оставшимся широким критериям.
