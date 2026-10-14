# Доступность настоящего сотрудника для перевода

Batch701 (production699/diagnostics700) установил точную отрицательную
границу: actor0x188e8f имеет template/seed4908279078625414699, но
source0x188e85.people.{template}.exists=false. Native assign_hired_actor
check=true возвращает possible0/failure invalid. После настоящего выбора
кнопки производственный Dialog вернул assignment_rejected/native invalid,
показал текст32; Pending idle, актёр остался в source, transfer не отправлен.
Это корректный отказ, а не зависшее перемещение или недостаточный срок ожидания.

Старый fixture создавал cue actor, затем задавал roleobject/role. Физическое
нахождение в cockpit не сделало его записью штатного crew registry.
Ослаблять RequestAssignment или подменять прибытие нельзя.

Diagnostics702 использует штатный create_ship/people (fillpercent100,
service weight100) из setup_gamestarts.xml. Выбирает максимум из32 crew
records доступного service member и материализует именно этот template
через create_npc_from_template; существующий roleentity переиспользуется.
Owner/roleobject вручную не перепривязываются, новый cue actor не создаётся.
Prepared требует реального source membership/container/roleobject.
Перед дальнейшим испытанием сохраняется native check=true и failure.

Это разрешённая подготовка тестового мира, не доказательство оплаты найма
или покупки scout. Transfer/binding/arrival выполняются только через
производственный диалог/штатное перемещение. Partial preparation удерживается
unknown без повторного спавна. MD validate702 PASS.

Установлено704: production699 неизменён, diagnostics702 SHA совпадают.
Controller51549 последовательно load704→batch704; результат ещё ожидается.
Task2.2 остаётся открытой.

## Результат704–706

Batch704 завершён без отправки перевода. Native preflight разрешил реальную
запись service crew (template17765662605599420675, source188dcf), однако
материализованный actor188dd9 находился intransit1, а read705 уже не показывал
container/roleobject. Подготовка не была готова; это не успех назначения.
Исходный управляющий4b520 продолжал работу, менеджер станции не изменился.

В706 подготовка заменена на native generic actor [ship,template]: сохраняется
реальная crew запись, не создаётся предварительное физическое воплощение.
Production RequestAssignment уже имеет этот штатный путь. Диагностический
UI ownership guard проверяет исходный корабль; read-back показывает
source_member/source_intransit/source_scheduled. MD schema и scheduling
прошли; установка и игровой тест706 ещё не выполнены. Задача2.2 открыта.

## Граница диалога707–709

Batch707 terminal1: source188e45/template4226042147235854424 существует,
source_intransit0/source_scheduled0/native_possible1. Локальный release
успешен, менеджер станции сохранён. Remote assignment не отправлен: игра
отказала открыть диалог с tuple в actor (debug402518.12).

Это разные контракты: common.xsd genericactor допускает список, но
start_conversation использует attributeGroup conversationactor (строка7634),
где прямо требуется context/template для неинстанцированного NPC. Source709
исправляет обе ветви start_conversation соответственно типу актёра.
MD schema/scheduling validate709 PASS. Source709 ещё не установлен;
production699 не менялся. Исходный управляющий после тестового release
не активен; восстановить через разрешённую загрузку/штатный restore.
Задача2.2 не принята; runtime результатов назначения нет.
