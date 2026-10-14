# Покупка15 после load018: текущие свидетельства

Live X4 PID50520, installed marketfix51/diagsh11. Checkpoint021 verified.
Сырые сохранённые данные прочитаны без изменения профиля:
save021-purchase-snippets-20261013.json и save021-purchase-decoded-20261013.json.

Submission table41668: key purchase_15_408301.653, statebuilt, id38111ULL,
price/paid1070000Cr, crewprice0, macroship_par_s_scout_01_a_macro,
shipyardcomponent0x6744e, match_reasonbuild_id_mismatch, candidateid0.
Match table39424: тот же key/id/yard/macro/price, candidateindex1.
Request table38822: тот же key/yard/macro, statebuilt.
Candidates list4247: единственный table39064; build typed build[0x0],
shipyardcomponent0x6744e. Числовой ID в Lua строке сам по себе не сохраняет
нативный объект очереди. Цена/модель/верфь не уникальная связь с кораблём.

Live short h: purchase15 building→unknown; recovery
purchase_effect_requires_reconciliation. Новая покупка не отправлена;
независимые экономический расчёт и стройка продолжаются.

Следующая проверка: Tracked.$Observation/BuiltShip native event и точные
сохранённые ссылки исходного build до/послеload. Пока не установлено,
исчезла ли очередь при реальном завершении, отмене или потере связи.
Нельзя объявлять оплату повторной либо построенный корабль потерянным
без этих данных; нельзя повторять оплату, искать похожий корабль и
принудительно менять receipt на delivered. Общее восстановление покупки
при load не принимается по этому случаю до объяснения точной связи.

## Установленная первопричина и source исправление

purchase-tracked018-021-20261013.json:018 Observation ready/native_built_event,
ship0x6690d, paid107000000 native units. Послеload021 та же сохранённая
Observation ready/native_built_event, ship remapped0x19d54, paid107000000.
Tracked.Build0180x28e6→021typedbuild0; Receipt numeric ID38111 не нужен
для повторного поиска завершённой очереди. Получение корабля не потеряно:
потерялась только возможность повторно проверить уже завершённый build.

SOURCE tm_empire_purchase.xml теперь ValidateCompletedPurchaseCertificate:
exact Pending/Receipt/Match key+id, schema/state, paid/price/crewprice,
tracked/pending/receipt/match yard+macro, persisted matched candidateindex
и typed candidate==Tracked.Build, original native_built_event, exact saved
ship собственный/операционный. Нет поиска по миру/макро/цене, новой оплаты
или искусственного события. Recover использует эту квитанцию до TrackBuild;
ObserveTracked проверяет завершённую квитанцию до отсутствия build handle.
Старая доказанная native event квитанция допускается без выдуманного нового ID.
Ручной/helm/authority контроль остаётся в существующей передаче ClaimOwnedShip.

XSD/scheduling/closure PASS. Это SOURCE, не installed/live acceptance.
Следующее: сохранить новыйcheckpoint при необходимости либо authorized021,
штатный restart с purchasefix и короткая actual handoff/reconcile/no replay
проверка exact purchase15; не считать source проверку получением корабля.

## Короткая проверка исправления и связанная граница

Controller3721 terminal exit0, completed-purchase-short-20261013.json:
408544.609 unknown →408554.698 ready; recovery
saved_native_completed_ship_recovered408549.426. Receipt ID38111/paid1070000
не изменились; новых запросов/оплат этой покупки controller не отправлял.
Нативный builder продолжил420.468→450.74/1140 независимо от recovery.
Передача получателю за30s НЕ состоялась: все PurchasedShipObserved/
PurchasedFreighterObserved/StaticDefense polling дополнительно требовали
Tracked.Build? и не вызывали CompletePurchase при пустом finished handle.

Generator исправляет три шаблона (четыре generated files): допуск polling
по Build? ИЛИ Pending.state ready; CompletePurchase сам повторно проверяет
завершённый сертификат, ownership/authority через прежний ClaimOwnedShip.
Orphan-ready guard также допускает сохранённый native-ready event, чтобы
не блокировать обязательство при завершении requesting goal. Других оплат,
искусственных ordered/delivered или поиска похожего корабля нет.
XSD/scheduling/closure PASS. Новый пакет51 установлен receipt
completed-purchase-handoff-install-20261013.json после штатногоclose141232.
Повтор exact021 handoff ещё в работе controller68951; не принимать заранее.

## Передача: текущая проверка 13.10

Controller68951 и controller125960 завершены. Их короткие read подтверждают recovery purchase15 в ready и неизменную исходную оплату1070000Cr, но не delivered/accepted. Допуск ready установлен в native receiver и DeliverCompletedShip; результата передачи это пока не доказывает.

Чтобы различить невызванный poll и конкретный отказ CompletePurchase, добавлена постоянная запись последнего вызова Request.CompletionObserved/CompletionKey/CompletionResult. Она не вызывает действий и не меняет квитанции; read выводит purchase_completion. Текущий единый controller-completion-telemetry-load022-20261013.py, session98052, загружает verified022 и читает четыре коротких состояния. Следующее решение — по реальному stage/reason, без искусственной доставки или повторной покупки.

## Первопричина раннего назначения

Save023: Pending.goal757634, manager757333, exact paid ship0x19fea; claim34480 принадлежит другой Recon goal757648 того же manager, issued408367.728. Разные target0x19f26/0x19fa4 и группы285/297 подтверждают две разные цели. Telemetry408616.744 waiting/manual_or_priority_order,408631.752 waiting/claimed_by_other_goal. Старый claim не переписывается и существующие orders не отменяются при доставке.

CanUseOwnedShip теперь запрещает приобретать ещё не claimed exact ship из native ready purchase другой цели до её передачи. Используется уже существующая Observation.ship и Pending.goal, без поиска или нового реестра. Проверка затрагивает только новый claim; выполнение/остановка существующего собственного поручения остаётся штатным. Состояние оплаты и сертификат по-прежнему проверяет CompletePurchase.

Для короткой проверки выбран existing016 (age408303.552), до ошибочного claim408367.728. 017/018 и023 содержат старый конфликт, поэтому не доказывают исправленный первичный путь. Все сохраняются без перезаписи.

## Полная передача и найденный повтор приказа

Controller47267 terminal0, purchase-reservation-short-20261013.json: 23 команды. На purchase15 доставлен exact UTT-100, accepted1/claim_manager1/goal_matches1, Lua reconciled, исходные1070000Cr/id38111 сохранены. Попытка16 отклонена до оплаты. SETA ended/factor1; устойчивое ускорение не подтверждено (автоматически вернулсяfactor1), поэтому эту проверку не считать ускоренным автономным прогоном. Новый native024 CRC/SHA проверен.

Однако отдельное чтение save024-paid-ship-audit-20261013.json обнаружило два native Recon приказа0x9077/0x950f в owned claim. Исходная цель тоже успевала подобрать ship до CompletePurchase, а receiver повторно назначал его. Передача и платёж подтверждены, отсутствие дублированного назначения — нет.

В SOURCE/installed v2 общий CanUseOwnedShip/ClaimOwnedShip имеет опциональный PurchaseKey (defaultnull); новый unclaimed exact ready purchase ship допускается только через DeliverCompletedShip с текущим ключом и исходной целью. Общие селекторы не получают этот допуск. Recon/Defend receiver добавляет корабль, силу и приказ только если его ещё нет в native группе; подтверждение доставки выполняется отдельно. Никакие старые чужие claims/приказы не переписываются. XSD/closure/scheduling PASS.

Установлено51+diag11; receipts purchase-reservation-v2-install-20261013.json / purchase-reservation-v2-diagnostics-20261013.json. Единственный новый controller69949 загружает verified016 и выполняет короткие read с native_orders/current_order/same_goal. Игровая приёмка v2 ещё в работе. Слот024 сохраняет предыдущий результат с известным повтором; следующий свободный025.

## Проверенная передача v2 без повтора приказа

Короткий controller69949 завершён, 20 команд без SETA. purchase15_408301.653 восстановлен из016, native built → delivered408376.673 → accepted1; первоначальная Lua оплата1070000Cr/id38111 reconciled. Четыре последовательных наблюдения показывают native_orders1/current_orderRecon/same_goal1. Native checkpoint025 отдельно разобран: UTT-100 имеет единственный started Recon в owned orders. CRC/SHA сохранения проверены; это принимает устранение конкретного двойного приказа и раннего назначения. Общая квалификация выпуска и двухчасовой прогон остаются открытыми. Квитанции: purchase-reservation-v2-evidence-review-20261013.json и save025-paid-ship-audit-20261013.json.
