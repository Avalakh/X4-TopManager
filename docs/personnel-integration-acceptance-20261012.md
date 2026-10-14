# Приёмка интеграции персонала4.4

Повторная проверка на установке669 (production666): batch668 создал вакансию
0x188fef и зарегистрировал её у Econ_Manager. После первого блока поиска
no_available_employee_in_current_batch candidate670 подготовил recruit на
следующей реальной станции0xc691 без изменения cursor/tick. Read671:
автономный hire_1_402586.31, actor0x193853/seed2414503123811654272,
реальное списание135480Cr, штатный transit/pod. Read672: receipt observed,
тот же actor/seed, transit0/scheduled0/podnull, passed1. Контроллер69660
завершился0. Эти квитанции подтверждают повторный положительный результат;
не закрывают недоказанные отрицательные ветки4.1 и bulk exchange4.2.

Установка578; load579 terminal0 accepted save_004; short581 terminal0;
readonly read584 terminal0. Кадровая цель — TM_PersonnelGoal дочерняя цель
единственного адаптированного Manager. Tick30s вызывает StepPersonnel,
сохраняет LastResult/LastReason/LastObserved. Отдельного кадрового планировщика
или внешнего управляющего нет. Диагностический pipe не входит в поставку.

Для свободного тестового корабля0x188e03 реальный CanUseOwnedShip с Econ_Manager
зарегистрировал ship_pilot_arrival_required. Фикстура создала только вакансию и
нанимаемого кандидата на одной из следующих известных станций; не вызывала
StepPersonnel/RequestHire, не меняла tick/cursor и не форсировала прибытие.
Штатный кадровый tick402586.32 самостоятельно выбрал actor0x18defa с
seed1949989519750888191, отправил hire_1_402586.32 и оплатил478960Cr.

Read584: receipt observed402611.876, тот же employee/seed, container=target,
intransit0/scheduled0/pod null; personnel_autonomous passed1. Last tick402646.335
возвращает required_control_posts_present. Нужный сотрудник действительно
стал предпосылкой существующей экономической задачи, а не виртуальной ролью.

Publish включает кадровую цель и квитанции hire/transfer/training в общую
проекцию задач. Старый transfer crew_exchange_1_395295.21 остаётся unknown
native_bulk с прежним source/target/person и без повторного dispatch или
вспомогательного создания человека. Независимый hire завершился несмотря на
этот unknown. personnel_hire_fixture PASS: replay, предыдущий неизвестный
платёж, недостаток денег, отзыв разрешения, потеря цели и helm не отправляют
повторную оплату. Семинары приняты ранее4.3.

Этот документ принимает интеграционную задачу4.4. Не принимает целиком4.1:
полная приёмка всех вакансий/независимости должностей ещё открыта.4.2 свежий
перевод с прибытием и остальные открытые пункты остаются обязательными.
