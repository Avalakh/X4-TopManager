# Согласование неоплаченного снабжения при утрате управляющего734

## Конкретная отсутствующая граница

RestockResultWatch наблюдал payment_approved/build_observed/terminal, но
не quote_requested/quoted. После прекращения доменной цели некому было
вызывать StepRestockDelivery. Неоплаченный запрос оставался в общем Request
и QuoteRestock возвращал previous_supply_request_unconsumed для нового
управляющего. Нельзя обходить это новым диспетчером или очисткой оплаченного
запроса: требуется согласование существующей квитанции.

## Изменение

ReadRestockResult для quote_requested/quoted проверяет CanActForGovernor
и ReadGoalLifetime. Утрата полномочий до оплаты переводит квитанцию в
rejected_before_effect и отзывает только совпадающий по key Lua request.
Если совпадающая платёжная квитанция уже payment_sent/paid/unknown/
build_recorded, результат unknown удерживается для фактического read-back.
Watcher включает две ранние стадии и допускает ConsumeRestockResult при
утрате manager authority, только когда старый ship claim уже освобождён
или принадлежит другой цели. Никаких новых orders, оплат или повторной
отправки нет; текущая активная цель продолжает обслуживаться прежним путём.

## Проверка и граница свидетельств

validate734: MD XSD и scheduling PASS. Source production734 пока не
установлен: installed production716, diagnostics721. Нужна короткая игровая
проба quote→release→new governor, отдельно payment intent→loss без replay.
Это исправление не принимает paid supply3.6 или lifecycle2.4 полностью.
