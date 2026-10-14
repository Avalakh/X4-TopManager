# Общий пакет экономического учёта и периода менеджера

First-bad814: после смены governor journal393721.87 показал missing
`$ActionReportDef.$Ship` в CheckRunningActions. После async negative search
и отмены pending search поле Ship законно отсутствует. Прежний synchronous
контракт обрабатывал только уже выбранный корабль.

Генератор815 оставляет штатную логику retirement, читая absent Ship optional;
отрицательный результат не превращается в покупку или найденный корабль.
Аналогичный factory subaction retirement теперь допускает отсутствие Ship
и Station, распространяя Disregard на ещё действующий search receipt.
Регенерированы13 adapted MD/3 AI и hash manifest. Closure guards, MD/AI schemas,
scheduling, четыре actual async caller branches и strict OpenSpec PASS.

Diagnostics816 добавляет station_manager_replace/read/restore. Replace выбирает
реального available service person с RemoteCrew.source и вызывает native
assign_hired_actor check=true, затем тот же actual source/person/station/post.
Conversations выполняет штатную замену сотрудника; diagnostic не подставляет
slot/seed/arrival/period/rating. Попытка фиксируется перед эффектом. Restore
требует того же старого actor/seed и фактически прибывшего нового сотрудника,
затем тоже использует native assignment. Governor и его manager cue должны
остаться прежними. Read сравнивает actual control slot/seed, native flags,
observations, новый период и old employee history через production библиотеку.

Installed816: production815, diagnostics816,51 production/8 diagnostic SHA
проверены. Controller816/session51539 TERMINAL exit0. Native load007 accepted.
Ordinary request393704.411 выбрал VHJ-116, claim sent/1 actual order; priority
393706.478 выбрал RED-923, claim sent/2 actual orders/commander0x4c0b9 совпал.
Read817 сохранил те же bindings, без новой покупки/эффекта. У ordinary requester
sector: штатный путь выдаёт самостоятельный TradeRoutine без назначения
commander. Diagnostics817 исправляет misleading expected field и добавляет
общий actual ReadOwnedOrderEvidence. Production native order path не менялся.

Station replacement native check вернулpostoccupied/effectsfalse: слот не
обходился. UI/provision/personnel persistence независимо проверены. В текущем
журнале mod MD missing Ship/duplicate ошибок не найдено. Полный прогон не шёл.

Source817 добавляет штатную подготовку свободной должности: сначала production
RequestTransfer подтверждает destination_post_not_free без эффекта, затем native
assign_hired_actor переводит прежнего manager в passenger той же станции.
После actual свободного controlpost/точной identity/завершённого native transit
допускается одно назначение нового. Для возврата аналогично сначала native
перевод нового manager в passenger, затем исходного на свободный post. Отдельные
attempt markers стоят перед каждым эффектом; нет прямого dismiss/slot/seed/
arrival/period вмешательства. Native запреты не обходятся.

Installed818: production815 без изменений, diagnostics817/8 SHA совпали.
Controller818/session24779 запущен для load007, одного ordinary поиска,
vacate/replace/native observations/history/restore, personnel/provision/UI.
Результатов818 пока нет. Source schemas/scheduling/Lua/Python/OpenSpec PASS.
