# Восстановление только сохранённой квитанции — source770

Короткий пакет761 показал гонку: новый construction_1_393644.644 создан после
load; затем ValidationLoaded сбросил его в checking_blueprints с причиной
plan_blueprints_require_load_revalidation в393649.401. Это была не сохранённая
проверка. Validator позднее завершился и реальная очередь8aff возникла;
не считать наблюдённый сброс окончательной потерей строительства.

ValidationLoaded теперь сбрасывает только MD validation evidence немедленно
при event_game_loaded. Нативных действий и Lua callbacks здесь нет; обычный
постраничный PlanValidationWatch остаётся bounded и проверяет реальные чертежи.

Шесть обработчиков с действительно отложенной работой (purchase, supply,
station reservation, plot, funding, native creation) теперь при событии load
передают key текущей квитанции через штатный signal_cue_instantly в отдельный
Reconcile cue. Он сохраняет delay5s, но выполняет прежние действия лишь при
nonempty event.param == current receipt key. При отсутствии saved receipt или
её замене новым запросом после load эти действия не выполняются. Тела native
reconciliation, ownership/goal/payment checks, unknown и no-replay сохранены.

common MD XSD: signal_cue не передаёт param; signal_cue_instantly передаёт.
Первый schema run обнаружил ошибку применения signal_cue; она исправлена.
Итог validate770: все MD/schema и scheduling checks PASS. Source не установлен;
требуется короткий saved receipt/no-replay и fresh-after-load пакет перед
приёмкой. Приёмка broad lifecycle/save-load задач этим документом не закрыта.
