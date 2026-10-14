# Отложенное подтверждение отмены Manager — diagnostic620

Первопричина ложного stopped0 в615 подтверждена текущей штатной схемой:
examples/x4_unpacked/libraries/md.xsd:2520–2524 указывает, что cancel_cue
вступает в силу после завершения текущих cue actions. CheckGovernorRoles
проверял old.state внутри той же последовательности run_actions, до выхода
из actions. Statecomplete в этом месте не доказывает неработающую отмену.

Критерий не ослаблен. Check сохраняет реальный old cue и факт успешной
смены/восстановления роли; состояние pending_cancellation, немедленныйpassed0.
Отдельный GovernorRolesCancellationObserved через2s проверяет отсутствие
старого cue либо фактические cancelled/disabled. Никакой Result из таймера
не отправляется: диагностический pipe не получает лишнего ответа.

Новая read-only governor_roles_read требует подтверждённую остановку старого
cue, active Registry, существующий новый cue, отличие actual cue references,
исходного governor и неизменённого station manager. До выполнения условий
passed остаётсяfalse. Имя TM_PlayerManager само по себе не сравнивает экземпляры.
Следующий короткий пакет вызывает read после существующей5s паузы смены роли.

validate620: MD XSD/scheduling PASS.620 не установлен; игровая установка615.
Нужен настоящий read-back после выхода actions, задача2.3 ещё открыта.
