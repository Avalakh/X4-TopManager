# Длинное описание задачи не должно обнулять отчёт

До исправления: ui-governor-switch-20261012.json, tasks14, item10 reason1238
UTF-8 bytes. Единственный нарушенный предел — task.reason1024 в UI validator.
Военный producer добавляет объяснение угрозы, подбора, исполнения и снабжения,
а также до четырёх названий кораблей. Теперь только task.reason ограничен4096
bytes; остальные пределы сохранены. Текст не обрезается.

Native Lua fixture принимает и выводит полный длинный русский текст;
4097 bytes отвергаются. Installed production51 SHA сверены install_mod.
X4 PID65104 штатно завершён, PID56044 запущен Steam без новых параметров.
Verified013 загружен, controller74712 terminal0; старые slots не перезаписаны.

ui-governor-switch-fixed-20261012.json, controller7289 terminal0: все секции
valid до/после смены. Старый Manager остановлен, исходный actor восстановлен
с seed-9126173547698565463, home_manager_unchanged1, runtimeactive.
Смена не доказывает повторение прежней строки ровно1238 bytes; длинный текст
покрыт fixture, игровой read-back проверяет полный новый отчёт.

ui-report-followup-fixed-20261012.json, controller9170 terminal0: body_rows110,
frame4108. Реальная прокрутка frame4463/top27/selected29 →
frame4818/top27/selected29 после8секунд. Первый отчёт17строк ограничил top до1;
это не регрессия. Освобождение Дротика BKK-871 от DockAndWait ранее подтверждено
в idle-scroll-funding-acceptance-20261012.md и не повторялось ради этой правки.

Остальные домены и общий длительный прогон остаются открытыми.
