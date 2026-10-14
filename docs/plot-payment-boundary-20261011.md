# Граница оплаты строительного участка

Состояние: исправление установлено в packet408; положительная игровая приёмка
новой лицензии ещё открыта. Прогон autonomy412 работает в отдельной timeline
quicksave. Save_004/save407 сохраняет прежний unknown plot7 без повтора.

## Штатный источник

MapMenu.buttonBuyPlot (examples/x4_unpacked/ui/addons/ego_detailmonitor/menu_map.lua,
4274–4276) передаёт получателя через ConvertStringTo64Bit(tostring(controlstation)),
затем вызывает PayBuildPlotSize. Тот же путь используется нашим адаптером.
Владелец сектора читается через sectorid и одиночный GetComponentData(owner),
как в штатном меню; результат proven role392/395: teladi/string вместо nil.
Логические поля после MD round-trip допускают только bool/0/1.

## Сохранённые случаи

Save399: plot6/404260.956 licence_failed/quoted_plot_geometry_or_price_changed,
payment receipt отсутствует. Этот конкретный return в Lua находится до payment
intent и эффекта. Ограниченное возобновление сохраняет ключ, проверяет отсутствие
same-key payment receipt, управляющего/цель/собственность/стройку/геометрию/бюджет.

Save405: plot7/404591.173 имеет payment receipt unknown/plot_payment_unknown.
Старое поле paid1800000 было записано номинальной суммой заранее и не доказывает
фактический расход. Очистка или повтор этого заказа не разрешены.
Role409: native transaction log issued-1..issued+10 дал count0/read0; это не
достаточное свидетельство отсутствия платежа и не основание снять unknown.

## Текущий контракт и проверки

До эффекта сохраняются amount и paid0; перед переводом — moneybefore и
payment_sent. После перевода сохраняется moneyafter. Paid становится amount
только при точном совпадении delta. Ошибка лицензии после полной оплаты оставляет
paidamount и unknown; ошибка/частичная оплата сохраняет before/after и удержание.
Лицензия принимается только по native payment/paid size/center и последующему
MD read-back соответствующего участка. При сохранённом same-key intent повтор
не разрешается даже после load.

Construction_plot fixture PASS подтверждает amount100/before1000/after900 для
полной оплаты, amount100/paid0/before1000/after950 для частичной и paid100 при
неподтверждённой лицензии. Во всех unknown случаях replay удерживается. Тест не
заменяет положительную игровую приёмку;3.4/6.3/6.6 остаются открыты.
# Source430: отказ изменённого положения участка

Autonomy412/015 (frozen408) обнаружил factory queue0xcf15e для новой station0x81ba279:
plan8/8 consumed, но plot5_401709.003 rejected_before_effect с причиной
plot_location_requires_reconciliation. Оплата по этой попытке не выполнялась.
В construction_plot.quote был лишний запрет GetBuildPlotPayment changed=true.
Primary menu_map.lua4242–4257 и menu_station_configuration.lua3311–3326 используют
native credit для расчёта текущей цены без такого запрета. Флаг отражает отличие
позиции от прежней оплаты; покупка текущей геометрии штатно разрешена.
Source430 удаляет этот pre-effect запрет, оставляя свежий full price/credit,
approval geometry/price matching, lifecycle guard и подтверждение PayBuildPlotSize.
Реальный новый failure воспроизведён fixture moved_new_station: moved flagtrue,
quote100Cr, единственный debit100Cr, native position reconciliation, no replay.
Lua fixture PASS.430 ещё не установлен, live paid plot success не заявлен.

