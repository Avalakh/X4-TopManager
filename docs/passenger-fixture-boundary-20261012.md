# Пассажир в корабле с действующей задачей — diagnostic623

Short621: пассажирская проба получила claimed_by_other_goal, player.shipnull.
Штатный scriptproperties.xml2413–2416 различает player.container (контейнер)
и ship context (может бытьnull, например при посадке на станцию). Fixture
создавал корабль docked на станции; teleport controlfalse и ship context
не доказывали физическое присутствие внутри летящего NPC корабля.

Подготовка теперь создаёт отдельный disposable scout в зоне станции с
штатным safepos2–3km, не docked. NPC pilot остаётся штатным control entity,
сохранены component и seed. Passenger passed требует player.container==Ship,
player.controlled!=Ship, тот же pilot/seed и production Reasonavailable.
Платный найм/покупка не принимается по бесплатной подготовке мира.

Работающий AI вправе занять подготовленный ship до отчёта. Для passenger
используется реальный Claim.goal только когда Claim.manager совпадает с
текущим Manager и goal существует. Claim не создаётся/не очищается; все
прочие ownership/lifetime/manual/unknown guards остаются действующими.
Если задача недоступна, Reasonavailable не предполагается. Helm/manual/
priority сохраняют прежний контекст и требуют своих защит.

Отчёт дополнен player_container/ship_docked/goal/claim_goal для read-back.
validate623-final XSD/scheduling PASS, включая диагностические поля отчёта.
623 не установлен; текущий runtime621.3.7 остаётся открытой до корректной
игровой пробы и полного охвата эффектов.
