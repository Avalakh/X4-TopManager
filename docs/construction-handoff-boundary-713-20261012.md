# Продолжение стройки после смены управляющего713

Read713 terminal0: runtime active/единственный TM_PlayerManager, но expansion
construction_2_401436.833 на station4ca8f/build1dee queued с причиной
construction_goal_missing_after_queue. Native build существует/processing1,
elapsed0, требует builder, ресурсы не выданы. Старый plot18 rejected_before_effect
plot_location_requires_reconciliation не является текущим новым отказом.

Primary construction_plot.lua уже содержит исправление430: moved geometry
не запрещает свежий native quote. Нельзя повторно устранять снятый запрет или
сбрасывать старую квитанцию по одному тексту read-back.

StepQueuedExpansion md/tm_empire_construction.xml проверяет старые manager/goal
перед новыми эффектами и удерживает очередь при исчезновении цели.
AdoptNativeStationBuild отклоняет другую незавершённую expansion как
previous_expansion_unreconciled и требует provenance новой manager/goal.
Поэтому смена роли710 показала отдельную границу продолжения, а не plot bug.

Доработка должна сохранять station/build/sequence/plankey/spent/accounted
payment/plot и все старые receipts; не повторять create_station, plan queue,
платежи или unknown. Новая штатная цель может принять существующую очередь
только после сверки ownership/точной native build задачи и предыдущих
неразрешённых эффектов. Проверить release/новый governor и loss/rollback вместе.
Source изменения handoff ещё не выполнены, task3.4/2.4 остаются открытыми.
Диагностика712 local_owned_builder установлена ещё не была; её spawn следует
использовать после восстановления полномочий продолжения очереди.

## Первая согласованная доработка714

ReconcileQueuedExpansionOwner вызывается из штатного StepPrefabExpansion,
когда новая цель выбрала ту же станцию/штатный finalsequence, а старая очередь
queued. Проверяет исчезновение прежней authority, новый CanActForGovernor,
собственность станции/storage, точную единственную native build задачу,
неизменность sequence и claim key/build/old manager/goal. Неразрешённые
funding/plot/builder receipts запрещают передачу; разрешены только observed,
rejected_before_effect, consumed, abandoned_before_effect. Native creation
дополнительно требует adopted provenance той же старой authority/build.

Изменяются только authority expansion/claim/creation и ссылка новой цели;
старые authority сохранены в previousmanager/previousgoal. План, ключ,
расходы, accounted keys, квитанции и native очередь сохраняются. Ни одного
create_station/add_build/payment/create_order в handoff нет. Production
продолжает эффектные действия только через существующий StepQueuedExpansion.

Это ещё не полное решение нового factory startup: требуется проверить, что
штатный AI действительно создаёт цель для существующей строящейся станции,
а не только для следующей prefab стадии. Не создавать отдельный планировщик
ради этого. Source714 schema/scheduling проверены; установка и live handoff
ещё не выполнены. Приёмку3.4/2.4 не закрывает.

## Интеграция715 в Request_Factory

Генератор adapt_native_manager.py теперь добавляет проверку осиротевшей
queued nativecreation перед созданием новой фабрики в штатном Request_Factory.
Цель принимает её только для той же пары RequestSector/Ware и сохранённого
creation.product. Последний сохраняется при новых prefab/bare factory
созданиях, без восстановления по догадке для старого save.

После успешного общего ReconcileQueuedExpansionOwner ссылка Station и
ActionDefinition остаётся на существующей фабрике, TM_PrefabAccepted=true
удерживает повторное создание и finalise. Дальнейшие native construction/
destroyed/finished observers работают с той же станцией. Если принять
очередь нельзя, штатный путь сохраняется, его прежний expansion guard
удерживает новый эффект. Никакой отдельной управляющей цели или scheduler
не создаётся. Новая authority также проходит ReadGoalLifetime.

13-script closure пересобрана; MD и adapted AI схемы/scheduling715 PASS,
Python generator syntax PASS. Production715/diagnostics712 пока не
установлены. Старый тестовый creation не имеет нового product; не выдавать
ему выдуманную связь для прохода теста. Требуется свежая подготовка и общий
короткий пакет смены роли, handoff, builder, незавершённых платежей и loss.

## Общие границы716

Bare factory create guard генератора теперь дополнительно удерживает новую
станцию при незавершённой expansion квитанции. Поэтому отклонённый handoff
не обходит сериализацию через штатный fallback create_factory.

Handoff сначала валидирует всю финансовую часть observed funding/plot
этой station/build (есть ключ и неотрицательный paid). Затем добавляет
подтверждённый debit к spent только если соответствующий accounted key
ещё не записан. Квитанции и деньги не изменяются. Это закрывает потерю
учёта, если прежняя цель исчезла после наблюдения платежа, но до accounting.
Ранее учтённые платежи не добавляются повторно.

Closure и полные MD/adapted AI schemas/scheduling716 PASS. Изменения пока
не установлены. Требуется общий адресный пакет: paid-before-handoff,
accounted replay, unknown hold, одинаковая/другая product/sector, actual
queue и native builder. Свежая timeline до старой expansion нужна, старые
unknown/global receipts не стирать ради подготовки.

## Короткая подготовка717–720

Production716 установлен с51-file manifest verification. Autosave_01
не содержит старых operation receipts, governor прежний валиден.
Batch719 сделал одну generation HQ; plan construction_1_393694.022
остановился на отсутствии ровно управляющего blueprint. Реальный отказ
waiting_blueprints подтверждён; очереди/денег/застройщика ещё нет.

Source720 добавляет диагностический grant только этого prerequisite
через штатный add_blueprints. Schema/scheduling/Lua syntax PASS, ещё
не установлен. После подготовки не повторять generation: production
ожидание существующего плана должно само перейти к blueprint validation
и queue. Fixture blueprint не является purchase acceptance.

## Настоящая очередь и owned builder722–724

План HQ construction_1_393633.039 валидирован4/4 после test-only blueprint
prerequisite (денег не меняет) и consumed. Read724 подтверждает queued
build8c7e на station4b6f2, processorbuilding1/elapsed0/total2700/step300.
Во время validating подготовлен player-owned Argon builder18774a/pilot187754
в6895м; purposebuild1/defaultWait/native actualbuildunits57. Его создание
не покупка, не hire и не результат назначения. Builder receipt пока null,
deployed0; следующая короткая проверка должна подтвердить production
funding/claim/DeployToStation и реальный deploy. Повтор spawn/generation
не нужен. Controller722 terminal0, read724 terminal0; файл save не изменён.


## Уточнение743: ссылка старой цели не означает действующие полномочия

ReconcileQueuedExpansionOwner раньше отвергал handoff по одному сочетанию
manager.exists/goal.exists. Runtime отменяет Manager через cancel_cue,
а ReadGoalLifetime явно различает отсутствующую и отменённую цель; сохранённая
ссылка не должна удерживать очередь после утраты authority.
Теперь сначала валидируется новый управляющий/цель, затем проверяется
lifetime старой цели и её активная Registry authority. Старый живой владелец
по-прежнему препятствует передаче. Native queue/sequence/claim и неопределённые
эффекты проверяются прежним путём; новых платежей/queue/orders это изменение
не создаёт. validate743 MD XSD/scheduling PASS. Не установлен и не принят
в игре; нужен short live queued handoff в общем пакете lifecycle.
