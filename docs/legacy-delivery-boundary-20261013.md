# Согласование старой поставки — 13.10.2026

## Причина

Короткие domain-short-b/c и domain-c-final-read: purchase_11_402186.122
состояние delivered, acceptednull, WDR-951/Сонра Агрессор принадлежит игроку,
TradeRoutine/commanderVTV-679/claimsent. goal Request_Freighter complete/exists,
ReadGoalLifetimeavailable. Exact requesterVTV-679 равен commander, claimgoal
равен старой заявке, previousgoalnull; PurchasedFreighterObserved отсутствует.
Значит это сохранённая заявка до введения подтверждения передачи, а не
исчезнувшая цель. previous_delivery_not_consumed блокировал новые покупки.

## Исправление

PreparePurchase перед новым запросом использует ReconcileLegacyFreighterDelivery.
Разрешён только старый native Request_Freighter без нового child observer,
с тем же key/manager/реальным paid receipt, без Pending/Tracked, при active.
Нужны точно собственные station requester/ship/commander, прежний claim и
полное ReadOwnedOrderEvidence. Подтверждается существующий штатный
TradeRoutine/MiningRoutine/SalvageRoutine в действительной очереди/behavior.
Используются уже существующие TransferOwnedClaim и AcknowledgeDelivery;
после accepted старая заявка прекращается, рабочий приказ сохраняется.
Новых orders/builds/payment/create_ship и очистки неизвестных receipts нет.
Несоответствие оставляет прежнее ожидание. Новые requests с живым observer
этим путём не обрабатываются.

## Проверка

XSD/native scheduling/check_adapted_manager/install51 SHA PASS. Installed
receipt legacy-delivery-install-20261013.json; candidate ZIP пересобран,
qualified_releasefalse. Live проверка ещё не принята: controller57709
ожидает загрузку verified014, затем обычный native_analysis и два чтения
через20сек. Нельзя считать исправление принятым до read-back accepted и
сохранения исходного назначения/отсутствия повторной оплаты.

Независимые диагностические результаты: siliconwafers fixture EKA-355
внешний запрет1 снят test-only command до0; native observerV3 активен,
продажа/доставка ещёnull. SETA guard исправлен по native timewarp.active;
короткая попытка factor6 сразу→1, штатная активация устойчиво не подтверждена,
finally/end выполнен. Никакого длинного ожидания не запущено.

## Короткий повтор и уточнение v2

Controller57709 terminal0: после native_analysis через20/40сек accepted
остаётсяnull. Это не принято. Offline read-only verified014 дополнительно
обнаружил старое TM_HandoffReason=existing_behavior. Старый default мог быть
заменён штатным менеджером станции. Recovery больше не использует Transfer
и не отменяет старый goal: AcknowledgeDelivery может подтвердить точную
старую claim напрямую. Уже существующий parent handoff также принимается
только по previousgoal. Сохраняются paid/key/ship/manager/Requester/commander,
полное ReadOwnedOrderEvidence и действующий собственный routine; без новых
приказов/смены поведения. Причина recovery теперь доступна отдельным read.
Установка v2: legacy-delivery-v2-install-20261013.json +
legacy-delivery-v2-diagnostics-20261013.json; controller64821 активен.

## V3: проверка referenced native cue

V2 terminal0: LegacyRecoveryResultlegacy_delivery_not_applicable, acceptednull.
Native scriptproperties отличает static (instantiating cue) от staticbase.
Сохранение имеет Request instance764257 под764256, base764146 ref764317.
Нельзя сравнивать его static непосредственно с исходным md шаблоном.
V3 проверяет имя и точного parent текущего Economy; key/manager/paid и остальные
guards не убраны. Источники неподвижных значений: verified014 (read-only) и
examples/x4_unpacked/libraries/scriptproperties.xml cue2194–2204.
Production51 установлен/SHA, receipt legacy-delivery-v3-install-20261013.json.
Controller22300 активен, результат пока НЕ принят.

## Игровое подтверждение v3

Controller22300 terminal0, legacy-delivery-v3-short-20261013.json:
до цикла purchase11 acceptednull; после обычного native_analysis и20сек
тот же key/ship/goal/manager, accepted1, LegacyRecoveryResultaccepted.
Через40сек результат сохраняется. Нет повторной оплаты11: Lua переключился
на отдельный новый native purchase12_408062.614, BuildID34584ULL,
реальная цена/paid7906044Cr, pendingbuilding. Пока он building, остальные
requests ждут previous_purchase_unreconciled; повторной покупки12 нет.
Это новая отдельная потребность алгоритма, не повтор11. Завершение12
этой проверкой не принимается.

Дополнительный read-only legacy-delivery-v3-final-read terminal0 подтверждает
WDR-951 по-прежнему TradeRoutine/defaultTradeRoutine/queue1, commanderVTV-679,
claimsent, не helm. Следовательно, собственный порядок станции не заменён.
Блокировка старой поставки устранена по реальному native read-back.
Соседняя стройка независимо действительно начала выполнение: elapsed0→29.1569
из1140; native paid builder тот же. Завершения нет; широкие3.4/6.3 открыты.
Продажа и mining trace покаnull.24/32, минимум2h fullrun не запускался.
