# Подготовка трёх доменов и фактический read-back

Controllers40120/6679/11024 завершились terminal0. Каждый использовал verified013
без перезаписи. Последний установленный diagnostics11 — v3, receipt
domain-native-resume-v3-install-20261012.json. Production51 не изменялся.

domain-native-resume-v3-20261012.json установил причину отказа старого тестового
repath: фактически оплаченный builder — paranid, не argon. paid5000000 native
units =50000Cr; fee_matches1, actual_matches1, station_matches1, helm0,
station_owned1. Это ошибка ограничения диагностики, а не оплаты/выбора мода.
После исправления на штатный friendly NPC критерий repath реально отправлен
407836.708 для прежнего builder_hire_2_407571.206. Деньги не списывались повторно,
другой строитель не назначался. По read407876.814 он ещё не deployed,
processor elapsed0/total1140, distance_build_position2873.5. Не принимать
отправленный сигнал за развёртывание или завершённое строительство.

Enemy MOM-017 имеет реального pilot и Attack. Once resume407856.77 переместил
только enemy возле текущего IYF-712 и отправил Attack100km. Собственные приказы
не инжектировались; native Recon сохранялся. После20сек enemy primary изменился
на другой own fighter. Target hull100 сам по себе не доказывает отсутствие боя:
для доказательства нужны shield/lastattack/attacker и состояние других fighters.

Surplus observer_v2 armed407836.656. Сопоставляет фактическую покупку own ship
на EKA-355 с продажей NPC NKU-508, независимо от назначения commander. До32
ship records; ни orders, ни cargo, ни прибыль этим наблюдателем не меняются.
Пока pickup_count0, stock5000, buyer0, traderWait. Продажа не принята.

Следующая подготовленная source-порция (ЕЩЁ НЕ INSTALLED): builder_position
один раз располагает ТОГО ЖЕ paid builder у точки и ориентации, рассчитанных
штатными get_building_position/get_safe_pos, затем будит штатный movement handler.
Не выставляет deployed/progress/finished. market_source/market_buyer используют
имеющийся GetTradeList/GetTradeData read-only путь на известных фиксированных
станциях; боевой read дополнен shields/attacker/lastattack. XSD и Lua syntax PASS.
Это сокращает подготовку коротких проб, не заменяет фактический результат мода.

6.6 подготовлена частично: tools/package_mod.py переиспользует installation_files
и собирает ZIP51 без diagnostics. ZIP content SHA сверены с source и установленным
manifest. dist/tm_empire_management-candidate.zip SHA
cbd8cc22d0703ba378b6e34248b30064e8e6ccecfb3fe075ebd7b726ff71afa8.
README включает установку архива; qualified_releasefalse, gate6.6 открыт.
