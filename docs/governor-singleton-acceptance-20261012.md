# Приёмка2.3 — единственное назначение и экземпляр управляющего

Установка621,51 production file, квалификация полного релизаfalse.
Load621 accepted/save_004, short621/session44518 terminal0; свидетельство
.cache/tmp/station-boundary-20261011/short621.json. Исходные/установленные
файлы сверяются installer; diagnostic MD/Lua поставляется отдельно.

На действующей станции0x4b519 с governor0x4b51f/stationmanager0x4b51c
создан второй физический модуль0x188f02 и реальный NPC0x188f13,
seed-8119076732352633310, placement1. Это подготовка мира, не обычная
покупка/строительство модуля или платный найм.

Production RequestAssignment второго сотрудника вернул governor_already_assigned.
Снятие исходногоunbound; второе назначениеbound, second_observed1;
второе снятиеunbound; исходное восстановленоbound; manager_unchanged1.
Нельзя занять вторую активную должность параллельно; после освобождения
должность доступна другому реальному сотруднику независимо от station manager.

Немедленное stopped0 не принималось за успех: native cancel_cue выполняется
после actions block. Отложенный governor_roles_read подтверждает stateobserved,
original_stopped1, original_statenull, current_exists1, different_instance1,
passed1. Сравниваются actual cue references, не одинаковое имяTM_PlayerManager.
До конца блока разрешения старого cue уже отозваны: original_lifetimegoal_cancelled,
original_registered0. После отмены старого cue нет, действует другой экземпляр.

Финальный read age402534.38: active/goals1, economy_last_run402526.914;
после смены роли стратегическая работа возобновлена. Оба первоначальных
сотрудника сохранены.2.3 принимается по указанному singleton сценарию.
Это не принимает UI назначения2.2, утрату/rollback2.4, обычное строительство6.3,
полный приоритет игрока3.7 или долгий автономный gate6.4.

В том же пакете helm/manual/priority прошли MD checks и manual/priority
распознаны production Lua GetOrders3. Passenger не принят: иной domain goal
занял fixture ship, player.ship оказалсяnull; нужна отдельная корректная
фиксация player.container и настоящего владеющего claim GoalCue.
Три UI страницы созданы98/18/85 строк; это не вся UI приёмка.
