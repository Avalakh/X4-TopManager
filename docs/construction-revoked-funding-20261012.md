# Отозванное строительное финансирование

Source573: ObserveConstructionFunding после проверки matching payment intent принимает revoked того же request key как rejected, аналогично rejected_before_payment. Ранее sent receipt с revoked approval и без платёжного намерения доходила до timeout/unknown и бессрочно блокировала финансирование.

Порядок проверок существенен: если $tm_empire_construction_payment содержит тот же key, ветка оплаты обрабатывается первой и возвращает observed либо unknown. Отзыв не скрывает paid/payment_sent/unknown и не создаёт возврат средств. Обновление reason/nextattempt текущей Expansion остаётся прежним и требует того же goal/build. Новой оплаты или строительного эффекта нет.

UI использует существующие rejected/reason. validate573: MD/XSD/scheduling PASS. Исходник573 не установлен; installed571 и короткий контроллер572 продолжаются отдельно. Новая граница не квалифицирована в игре.
