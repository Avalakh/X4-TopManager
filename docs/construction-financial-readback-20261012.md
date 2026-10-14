# Строительство: котировка, оплата и застройщик

Installed530, save_004, управляющий активен. Свидетельства находятся в
`.cache/tmp/station-boundary-20261011/role534.json`,role535.json,role536.json,
builder537.json иrole539.json. Это короткие чтения текущего игрового мира,
а не финальный длительный прогон.

## Подтверждено

Plot19_402551.861: native_plot_geometry_and_licence_observed для текущей
PFY-706/station0x4bd7c/build0x1dee. Затем construction_funding_2_402611.879
прошёл новую read-only Lua quote → MD approval → штатную оплату → read-back:
native wanted1211198Cr, balance0, состояние Luapaid, MDobserved402611.9,
на build storage1211198Cr. Причина предыдущего отказа1211197.8 MD против
1211198 native Lua устранена без ослабления проверки фактической оплаты.

Builder_hire_2_402626.882: native fee50000Cr фактически paid, ship0xaa9c,
receipt sent/native_hired_builder_deployment_pending. Стройка указывает
тот же actualbuilder0xaa9c, ship.constructionmodule0x4bd79. Это подтверждает
оплату и назначение; deployed0 означает, что развёртывание ещё не доказано.

Материалы подготовлены командой construction_resources бесплатно для теста;
resource_types0 не подтверждает оплаченный закупочный путь. Завершение
физического строительства ещё не подтверждено. Задача3.4 остаётся открытой.

## Ошибки и сгруппированные правки

BuilderNear537 отправил одну warp команду для этого оплаченного застройщика,
но сразу прочитал прежнюю дистанцию79462400 и записал unknown. По этому
результату нельзя утверждать успешное перемещение или повторять эффект.
Source538 теперь читает фактическое положение отдельным cue через2s после
warp, без назначения, оплаты или принудительного развёртывания.
MD/XSD/scheduling PASS; изменение ещё не установлено.

Source536 корректно трактует native bool или0/1 в проверках собственности и
враждебности Lua найма/восстановления застройщика. Существующий fixture
расширен numeric ownership/negative case и PASS. Изменение ещё не установлено.

Role539: assigned builder есть, deployed0, но expansion показывал
native_construction_in_progress из одного build.isprocessing. Source540
показывает builder_arrival_pending до фактического isdeployedconstructionvessel;
штатные orders и строительный алгоритм не меняются. MD/XSD/scheduling PASS;
изменение ещё не установлено. UI уже имеет текст этой причины.

Следующая установка объединяет source532 helm fixture,533 actor flag guard,
536 builder bool boundary,538 deferred warp read-back и540 статус стройки.
Нового застройщика пока создавать не нужно: реальный штатный уже назначен.
