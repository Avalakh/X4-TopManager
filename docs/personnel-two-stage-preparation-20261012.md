# Двухэтапная кадровая подготовка

Diagnostic source570 добавляет allowlisted hire_candidate_next. Сначала прежний hire_setup создаёт свободный тестовый корабль, personnel_prerequisite вызывает настоящую CanUseOwnedShip для Econ_Manager. После обычного кадрового tick новая команда использует опубликованный HireStations/HireIndex и ищет свободный npc_generic slot в следующих4 станциях. Она не меняет эти поля.

Создаётся отдельный тестовый кандидат штатными create_cue_actor/CalculateNPCHiringFee/add_actor_to_room; прежний диагностический кандидат сохраняется как previousactor. Имя/seed ожидания теперь относятся к новому кандидату. Бесплатное создание моделирует предложение рынка, а не квалифицирует найм. Производственный RequestHire должен сам отправить настоящую оплату и назначение.

Только свободный собственный тестовый target без assigned pilot и asset claim может быть перемещён warp возле источника. Повторная подготовка, target под штурвалом, активный sent/unknown hire этой цели и отсутствие реального списка отклоняются. Warp не считается подтверждённым до read-back. Создание pod/forced arrival, смена product cursors/ticks и прямой RequestHire отсутствуют. Если в ближайшей порции нет native slot, возвращается waiting, не фиктивный успех.

MD/XSD/scheduling validate570 PASS. Команда не установлена и не использована в игре. Границы native actor placement/warp/arrival пока не квалифицированы. Diagnostic extension не входит в поставку.
