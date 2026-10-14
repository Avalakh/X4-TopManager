# Приёмка изоляции установки — пункт6.2

Пункт6.2 принят по свидетельствам381 и игровым снимкам374/378/autonomy380.
Это не clean-release приёмка6.6 и не приёмка обязательных доменов.

Используется подтверждённое пользователем тестовое save_004, без обязательной
дополнительной резервной копии. Запросы save372/save376 направлены только в этот
слот; пользовательские quicksave/autosave не перезаписывались.

Предыдущий установленный topmanager v157 ранее сохранён с проверкой70SHA в
archives/installed-topmanager-v157-2026-10-10 и удалён из extensions, как записано
в task-state.md. Текущий install-boundary381 повторно перечислил content IDs:
topmanager отсутствует, ровно один tm_empire_management и отдельный диагностический
tm_empire_diagnostics. Последний не входит в поставку управляющего.

Установленный packet373:46files, несовпадений с installed-manifest0. Действует
один собственный Manager: runtime active/manager_exists1/goals1, registry governor1.
Это собственный namespace/state, не второй штатный игроковый FactionManager.
Отдельные station managers сохранены. Доменная работа имеет свои незакрытые задачи.

source-audit381:140 штатных исходников совпали с текущими installed CAT/DAT,
base mismatches0/unresolved0,4DLC boundaries разрешены. check_native_manager_copy
повторно подтвердил SHA13 неизменённых первичных и изолированных исходных копий.
install-boundary381 сравнил все74 ранее учтённые affected overlays чужих
расширений: изменений0. Новые3 наложения в текущем audit принадлежат только
нашему модулю (wares/modulegroups/index macros). Это проверка затронутых границ,
а не новый полный манифест всех посторонних файлов игры.

Production source/UI/native closure не ссылаются на archive или прежний bridge.
install_mod.installation_files собирает ограниченный набор собственных файлов
и проверенные native/adapted источники, без чтения старой реализации из архива.
Процесс установки пишет только extensions/tm_empire_management; диагностическая
установка отдельно пишет tm_empire_diagnostics. Чужие моды не редактировались.

Сырые свидетельства: .cache/tmp/station-boundary-20261011/install-boundary381.json,
source-audit381.json, role374.json, role378.json, autonomy380/000-role.json.
installed-manifest.json и source-audit отражают qualified_releasefalse/статическую
границу и не заменяют финальную игровую приёмку.
