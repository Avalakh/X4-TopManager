# Независимая вакансия при неподтверждённом переводе

Штатные пути остаются assign_hired_actor для должности и оплачиваемый найм
реального Actor с HiringFee; новые люди или второй кадровый планировщик не нужны.

В StepPersonnel вызов RequestTransfer возвращал global
previous_personnel_transfer_unreconciled, после чего Step немедленно завершался.
Найм для другой target/post таким образом не рассматривался. Это особенно
существенно при старой unknown квитанции обычного service crew: она не является
заказом пилота или менеджера другой станции.

Source исправлен: при несовпадении target/post поиск перевода прекращается через
break, затем рассматривается существующий штатный RequestHire. При точном
совпадении должности сохраняется ожидание. RequestHire дополнительно удерживает
новый найм на pending target/post перевода, RequestTransfer удерживает назначение
на pending target/post оплачиваемого найма. Исходная Transfer receipt не
перезаписывается и unknown эффект не отправляется снова. Переводы по-прежнему
сериализованы; это изменение разрешает независимый найм, а не параллельную
перезапись квитанций переводов.

MD/XSD/scheduling PASS; UI-тексты двух новых причин и recovery pending добавлены,
empire_status fixture PASS. Всё SOURCE-ONLY во время immutable autonomy380.
Далее пакетная игровая проверка: независимая реальная вакансия рассматривает
найм, совпадающая должность ждёт, нет оплаты/назначения двух людей на одно место,
оригинальная unknown receipt сохраняет person/source/target/state.4.4 открыта.

Проверка семинарного выбора отдельно подтвердила соответствие существующей
RequestSeminar первичному Conversations.xml:934–991 (skill /3 и tiers0–4).
Штатная формула не менялась; принятая4.3 не переоткрывалась без регрессии.

## Сверка источника тарифа во время autonomy412

NPC_Instantiation.xml:2279–2282 вызывает штатную HiringFeeFromCombinedSkill
и записывает npc.$HiringFee. Conversations.xml:222–226 использует тот же
признак/тариф для доступного найма. Наш RequestHire:279–295 принимает только
существующего чужого hirable/noncontrol Actor, remote comm, known operational
station roleobject, сохранённый штатный HiringFee и свободный target post;
assign_hired_actor check выполняется до оплаты. Нет необходимости создавать
тариф, менять навыки или ждать особого пользовательского диалога расчёта цены.
Эта сверка первичного контракта не подтверждает фактический найм/прибытие:
4.1/4.2/4.4 остаются открыты. Frozen installed пакет412 не изменялся.

## Капитан как предпосылка доменной задачи, staged423

Общий CanUseOwnedShip ранее проверял ownership/operational/helm/manual/lifetime,
но не arrival капитана. Теперь для ship.canhavecontrolentity.aipilot требует
существующий assigned pilot с roleobject==Ship, без intransit/transfer scheduled/
podarrivaltime. Иначе ship_pilot_arrival_required; helm исключается первым.
Существующий StepPersonnel видит свободный aipilot post и рассматривает перенос
или обычный платный найм; новые actor/звёзды/отдельный кадровый планировщик не
создаются. Старый unknown crew transfer остаётся сохранён, независимая vacancy
может идти через Hire согласно уже подготовленной границе.

UI перевод причины объясняет ожидание прибывшего капитана. Diagnostic read source
для managed/controlled ships дополнен ship_pilot с canhave/actor/roleobject/
transit/scheduled/pod, чтобы следующая игровая пачка сравнила реальный actor
со staff guard; остальные корабли не раскрывают дополнительное диагностическое
состояние. MD/XSD/scheduling и existing shared-guard coverage PASS, validate423.
Это source-only, не подтверждённый игровой arrival всех pilots;4.4 и3.7 открыты.
Collector80242 live/frozen408 без изменений, latest samples8/2103.7701866s.

## Контракт назначенного и действующего пилота, diagnostic424

Primary scriptproperties302–305 различает pilot/assignedpilot/aipilot/assignedaipilot;
назначенный сотрудник может ещё не пилотировать. Entity roleobject1364,
isintransit1377, transferscheduled1379/podarrivaltime1382 подтверждают типы
новой staff границы. npc_state_machines2080–2093 и2342 используют реальный
assignedcontrolentity.aipilot и переходы к pilot-at-post; наличие crew count
не заменяет наличие соответствующей entity. Diagnostic ship_pilot source теперь
показывает active_aipilot и assigned_aipilot рядом с assignedcontrolentity,
roleobject/transit/pod. Это read-only и не требует новой модели NPC state machine.
MD/XSD/scheduling PASS (validate424). Live проверка этого diagnostic ещё не
проводилась: frozen408 сохраняется. Поэтому совпадение назначенного/действующего
пилота и отсутствие лишнего ожидания423 не заявлены как принятые4.4/3.7.

## Source428: обход всех страниц кандидатов

В StepPersonnel найден детерминированный пропуск: общий HirePersonCursor
продвигался после каждой станции. Для двух станций с32 NPC и page16 последовательность
station1 offset0,32,64 и station2 offset16,48,80 никогда не читает вторую половину
первой станции и первую половину второй. Это источник ложного отсутствия кандидата.
HirePersonPage теперь меняется на16 один раз за полный круг HireStations;
обе станции получают страницы0 и16 в соседних кругах. По-прежнему проверяются
не более16 существующих NPC на одной станции за product вызов; бюджет, реальные
HiringFee, native assignment checks и блокировки unknown hire/transfer не изменены.
Read-only HireCandidates имеет такой же обход страниц, явные limits и счётчики
eligible/rejected в выборке, без вывода об отсутствии кандидатов во всей галактике.
Validate428 MD/XSD/scheduling и shared native guards PASS. Установка и paid-hire
read-back не выполнялись во время collector412; критерии4.1/4.4 не приняты.
