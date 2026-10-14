# Короткий строительный пакет586

Контроллер73875 terminal0, установка578, исходник585 не установлен и не
потребовался: новый текущий builder receipt уже sent. Новую команду ресурсов
не добавляли — существующая совпала с текущей Expansion.$Receipt.

До подготовки: station PFY-706/0x4bd67, build0x1dee, plot19 observed,
funding2 observed, бюджет3108364Cr, builder_hire2 sent/native_hired,
ship0xaa87, тот же actualbuilder. Все эти эффекты выполнял мод до тестовой
подготовки. Не смешивать с прежним заказом другой станции.

builder_near confirmed prepared: исходное расстояние79429632m, до storage
2812.5m. deployment_forced=false. construction_resources prepared для той же
station/build: claytronics542, energycells1083, hullparts1980, before0,
after=запрошенное количество. Это бесплатная подготовка тестового мира,
paid_supply=false; не принимается как платная доставка ресурсов.

Через15s: needed resource_types3→0, wantedmoney3108364→1083538Cr;
build processing1. Builder всё ещё deployed0, receipt sent; Expansion queued
builder_arrival_pending. Не выдавать исчезновение потребности в материалах
за завершение строительства или развёртывания. UI status сформировала150
строк; визуальная читаемость и все UI критерии ещё не приняты.

Дальнейшее длительное ожидание одной функции не запускалось.3.4 остаётся
открытой. Накопленные source580/583/585 будут устанавливаться общей порцией.
