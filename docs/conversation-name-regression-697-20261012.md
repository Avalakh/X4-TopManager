# Пустой диагностический разговор: причина и исправление

Batch695: customhandler0 у действующего governor, но6 пустых кнопок
после default и после tm_empire_roles; release отклонён до эффекта.
Значит гипотеза customhandler подавления общего разговора не подтвердилась.
Пустые разговоры также наблюдались689/691/692. Подготовленный passenger
не переводился, исходный governor оставался active.

Сравнение с рабочим dialog683 выявило регрессию diagnostics685:
conversation="$Conversation" в start_conversation. common.xsd объявляет
conversation как namestring, а не expression. Имя переменной не выбирает
значение default/tm_empire_roles; соответствующие handlers не срабатывают.
Рабочий683 использовал literal tm_empire_roles. Production roles script
не содержит этого диагностического start_conversation и не менялся.

Source697 сохраняет параметр выбора только в условии do_if, а в обеих
start_conversation использует буквальные имена default/tm_empire_roles.
MD schema/scheduling PASS. Установлен698 вместе с production696.
Batch698 добавляет bounded чтение initial options до10с, без повторения
start/assignment, и продолжает независимый transfer после локального
отказа входа. Игровой результат исправленной версии ещё ожидается.
