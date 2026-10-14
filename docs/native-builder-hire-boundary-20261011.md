# Штатный платный найм строительного корабля

Проба role337: расширение HQ поставлено в очередь, строительный счёт
463702Cr равен штатной требуемой оценке. Недостающие ресурсы:
клейтроника137, энергоэлементы274, детали корпуса501; склад0 для всех.
Назначенного строительного корабля нет; reason owned_builder_unavailable.
Текущее исполнение рассматривает только собственных строителей.
Это ограничение адаптера, а не доказательство отсутствия доступных NPC строителей.

Первичный источник X4 9.00: `menu_station_configuration.lua:1380` открывает
MapMenu/selectCV. `menu_map.lua:3490` проверяет IsBuilderBusy, isreallyenemy,
GetPlayerMoney и GetBuilderHiringFee. Для чужого строителя выполняет
TransferPlayerMoneyTo(fee, builder), затем orderDeployToStation.
`menu_map.lua:3511`: IsOrderSelectableFor, CreateDeployToStationOrder,
SetOrderParam(builder,index,1,nil,station), EnableOrder.
Это именно станция, как подтверждает параметр station в order.build.deploy.xml;
штатный AI затем получает station.buildstorage сам.
Stock clear=true вызывает RemoveAllOrders; переносить без отдельной проверки
занятости/контекста нельзя. Плата и создание приказа — разные эффекты.

Продуктовая адаптация должна выбирать реально известного доступного строителя,
читать штатный тариф, резервировать единственную попытку для точного
station/build/builder/manager/goal, повторно проверять условия перед оплатой.
Unknown после оплаты не разрешает платить снова. Read-back должен разделять
оплату, выданный приказ, фактическое назначение строительного корабля и
готовность модулей. Не следует требовать player ownership для нанятого
строителя и не следует обходить действующие отношения.

Этот документ фиксирует обнаруженный штатный путь и незакрытую границу.
Платный найм NPC строителя реализован и установлен в пакете341–344 (46 файлов). Lua fixture проверяет успешную оплату, повтор, изменение тарифа, занятость, отзыв разрешения, частичную оплату и отказ создания приказа; MD/XSD/scheduling прошли. Игровое назначение и прибытие пока не приняты; задача3.4 открыта.

Прогон371 выявил ошибочный адресат в прежнем адаптере: storage вместо station.
Оплата50000Cr доказана before61616987/after61566987, однако в Save368 у YKC-004
остался только default FindBuildTasks. Исправлено только в source.
Добавлена однократная миграция старой sent квитанции с полной подтверждённой
оплатой и без destination_version: MD повторно проверяет governor/goal/build/
construction claim/ship/station/storage; Lua требует idle/not busy и сохраняет
recovery_attempted+unknown до выдачи нового DeployToStation. Оплаты в миграции нет.
Новые приказы помечены destination_version2 и миграции не подлежат. Частичная
оплата, неверный ключ, занятость, повтор и неудача покрыты fixture; PASS.
Синтаксис MD/XSD/scheduling PASS; игровая миграция ещё не установлена/проверена.

## Подтверждение после packet373

Миграция установлена в общем46-file packet373. Save376/builder-read377:
destination_version2/recovery_attempted1, те же before61616987/after61566987/
paid50000Cr; второго списания нет. builder-order379: DeployToStation0x872c
started, station0x4ac12 (HQ после ремапа handles), ship YKC-004/0x11f59.
Autonomy380/003-role: builder receipt observed/native_hired_builder_arrival_observed,
observed402414.609. Это проверка deployed с reciprocal buildmodule/constructionvessel,
а не только отправка приказа. Expansion ещё queued/native_construction_in_progress:
готовность новых модулей отдельно не принята. Прогон380 остаётся read-only.

## Завершение расширения: autonomy380/005

Последующий снимок подтвердил observed/native_expansion_modules_observed,
observed402970.047, тот же key construction_1_393687.476, station0x4ac12,
build0x1d60. Исходный ExpansionFixture запрашивал
macro.tm_empire_control_arg_macro. Product StepQueuedExpansion сверяет каждую
запись sequence по planmodule.id, точному macro и isoperational; наблюдение
подтверждает готовность всей очереди, а не только окончание работы строителя.
Этот результат заменяет прежнее ожидание готовности выше. Развитие новой
станции и полная приёмка3.4/6.3 всё ещё требуют собственных подтверждений.


## Autonomy412/004: прибытие строителя

Новая ранняя timeline: builder1_397163.919 observed/native_hired_builder_arrival
observed398307.292 после sent в003, station HQ XZS342/storage builder0x117a7.
Списанный fee50000Cr остаётся единственным: paid50000 в исходной Lua квитанции.
Expansion1 queued, storage budget/wanted327430Cr/resources2/processing1.
Доставка строителя подтверждена, завершение расширения ещё не подтверждено.

## Live429: штатное завершение в текущей timeline

Autonomy412/014 теперь подтверждает expansion1_393687.476 observed с причиной
native_expansion_modules_observed, observed401393.008, HQ station0x4a6e4/build0x1cf6.
Plan4/4 consumed; общий tracked spent512702Cr при limit5000000Cr.
В012 resource_types0 и storage budget/wanted0 при processing1 предшествовали
завершению. Путь hire fee50000→arrival398307.292→native supplies→module completion
подтверждён в одной текущей timeline frozen408. После завершения создана новая
factory shell0x81ba279 в401406.798; bare_station_observed/factory_shell_pending
не означает построенную фабрику, plot/build пока отсутствуют. Collector80242
остаётся единственным pipe owner, прогон15 samples/4203s ещё не двухчасовой.
