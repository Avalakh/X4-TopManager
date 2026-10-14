# Приёмка2.2 — игровое назначение отдельного управляющего

Критерии проверены совместно, без повторного тестирования штатного диалога:

- governor-dialog-683-20261012.md / dialog683.json: реальный разговор,
  активная кнопка снятия, SelectDialogOption, inactive/старый Manager удалён;
  повторный разговор и точная кнопка модуля вернули того же actor/module в bound.
  Прямой диагностический RequestAssignment не заменял эти UI действия.
- governor-entry-698-20261012.md: настоящий DefaultComm → «Ещё» →
  «Управление империей…», customhandler0; открывается production диалог.
- governor-remote-arrival-710-20261012.md / batch710–711: настоящая кнопка
  модуля перевела штатного service crew member с docked scout; exact seed,
  source membership исчезло, actor прибыл на станцию, transit/scheduled/pod0,
  roleobject/container/station совпали. Прибытие не форсировалось.
- check684 и governor-singleton-acceptance-20261012.md: station manager
  отклонён existing_post, второй активный сотрудник отклонён, при смене
  отдельного governor station manager не изменился. Один employee не занимает
  обе должности, после освобождения допустимо другое назначение.
- boundary-trace-load-20261012.json / session40168 terminal0: native load
  проверенного save012. Governor0x4ae67/seed-9126173547698565463;
  station0x4ae60/module0x4ae8f, macro tm_empire_control_arg_macro,
  module_operational1. Station manager0x4ae7d/seed-7877045512791511809 —
  отдельный сотрудник. Governor controlpost=null, container/station/roleobject
  0x4ae60, transit0/scheduled0/podnull. Runtime active/один Manager.

Последнее чтение подтверждает сохранение module/station/actor binding и двух
должностей в текущей сборке. Оно не объявляет текущего governor тем сотрудником,
который участвовал в remote UI scenario710: это разные сценарии того же
production контракта. Save012 CRC/SHA проверены в save012-package-20261012.json.

2.2 принимается. Все виды утраты и rollback2.4, обычное строительство6.3 и
полный автономный прогон6.4 остаются отдельными открытыми критериями.
