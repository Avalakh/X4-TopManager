# Штатный вход в диалог и незавершённая проверка перевода

Production696/diagnostics697, load698 save_004 accepted. Controller53437
terminal0, X4 PID55772. Сохранение не перезаписывалось.

Batch698 после исправления literal conversation подтвердил реальные кнопки
default: семинар, работа в другом месте, «Ещё», прощание. Выбор «Ещё»
(button5) показал штатное увольнение и новый пункт «Управление империей…»
(button2). Выбор пункта открыл производственный Dialog с кнопкой снятия.
Это подтверждает AddChoice в реальном штатном разговоре. customhandler0.

Снятие через настоящий диалог: Registry inactive, ManagerCue отсутствует,
station manager0x4b526 сохранён. Prepared remote passenger0x188e91,
seed-9168992542312332941, находится на docked source0x188e87;
станция0x4b523/module0x4b55c. Выбор точной кнопки модуля выполнен,
но три последующих чтения показывают Pending idle/Governor null,
actor container/roleobject остаются source, transit0/scheduled0.
Перевод или назначение не подтверждены. Приготовление физического NPC
не доказывает, что native personnel engine считает его доступным crew member.

Точная причина ещё не измерена: controller слишком рано отменял разговор,
не читая результатную строку, а production возвращал общий текст для ряда
отказов. Source699 добавляет отдельные пользовательские сообщения по
существующим return codes и один последний UI result; native preflight
failure сохраняется отдельно для диагностики, без повторной попытки.
Source700 читает template/source_member и native check=true ещё при
подготовке, без отправки transfer. Оба source ещё не установлены.

После проверки Restore700 через существующий CheckRoles заново привязал
исходного сотрудника, который всё это время оставался на штабе.
repeat_binding bound, manager_attempt existing_post, manager_unchanged1.
Это диагностическое восстановление исходной ситуации, не доказательство
remote transfer. Task2.2 остаётся открытой до фактического результата.
