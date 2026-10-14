# Независимая сверка рабочего бюджета

Source574 добавляет StationFundingWatch: каждые15s при sent/unknown существующей StationFunding receipt вызывает ObserveStationFunding. Прежние проверки exact key/station/amount/wanted, фактического списания игрока и зачисления станции сохраняются. Никакой RequestStationFunding/оплаты/смены назначения watcher не вызывает.

Это покрывает отсутствие UI callback после load или остановки исходной цели: сверка больше не зависит от нового запроса производственного бюджета. При matching payment intent неподтверждённый результат остаётся unknown; revoked без такого intent уже обрабатывается существующей веткой rejected. Пустые или terminal квитанции watcher не запускают.

validate574: MD/XSD/scheduling PASS. Source574 не установлен и не квалифицирован в игре; installed571 и короткий тест572 продолжаются отдельно.
