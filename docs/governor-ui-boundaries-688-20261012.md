# Недостающие короткие границы назначения

Локальный производственный диалог уже подтверждён dialog683. Следующий
пакет проверяет две оставшиеся границы2.2 совместно:

- Настоящий default-разговор сотрудника, штатная кнопка «Ещё», затем
  добавленная AddChoice кнопка управления империей. Primary источники:
  Conversations.DefaultComm и section g_mainmore в текущей conversations.xml.
- Перевод отдельного свободного пассажира с другого roleobject на штаб.
  Для быстрого теста создаётся disposable scout в штатном dockingbay штаба
  и реальный cue actor, помещённый в его controlroom. Создание мира не
  считается обычным наймом/покупкой; эти домены здесь не принимаются.

Нативный контракт подготовки docked ship взят из diplomacy.xml:
find_dockingbay/match_dock storage=true size=dock_s и create_ship dock.
Actor preparation использует ранее проверенный create_cue_actor,
set_entity_role/passenger, set_entity_role_object и add_actor_to_room.
Назначение и путь на станцию остаются производственными механизмами.
Подготовка не вызывает assign_hired_actor и не выставляет transfer/arrival
или binding. Partial creation сохраняется unknown без повторного спавна.

Один controller dialog689 сначала готовит мир, затем выбирает реальные
диалоговые кнопки по точному тексту и активности. После снятия первого
управляющего вызывает настоящий диалог подготовленного пассажира и
выбирает исходный модуль. Три чтения через5с проверяют фактические
seed/container/roleobject/Registry и независимость station manager.
Отсутствие кнопки или неопределённый ответ прекращает зависимые шаги
без повторной отправки эффекта. Это короткая проверка границы, не долгий прогон.

Source685–688: MD XSD/scheduling validate688 PASS; Lua syntax680 PASS;
Python dialog689 syntax PASS. Установка689 сверила MD/Lua SHA. Игровые
результаты ещё ожидаются; задача2.2 остаётся открытой.
