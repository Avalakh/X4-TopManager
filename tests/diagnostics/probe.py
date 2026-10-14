"""Общий тестовый pipe-клиент. Не входит в поставку игрового мода."""
import argparse
import json
import re
import time
import uuid
from pathlib import Path
from named_pipe import NamedPipeServer


def save_name(value):
    if not re.fullmatch(r'(?:save_[0-9]{3}|autosave_0[123]|quicksave)', value):
        raise argparse.ArgumentTypeError('Ожидается штатное имя слота сохранения')
    return value


def request(pipe, frame, timeout=15):
    pipe.send(frame, timeout_seconds=5)
    result = pipe.recv(timeout)
    if result is None:
        raise TimeoutError('Нет ответа игры; запрос не повторяется')
    # These multi-stage world preparations must never consume a stale response
    # as permission to start the next step. Fail without replaying an effect.
    expected = {
        'station_budget_retry': 'station_budget_retry|',
        'supply_boundary_retry': 'supply_boundary|',
        'supply_boundary_step': 'supply_boundary|',
        'idle_orders_read': 'idle_orders|',
        'military_visibility_probe': 'military_visibility|',
        'military_refresh_report': 'military_refresh_report|',
        'ui_scroll_prepare': 'ui_scroll|',
        'ui_scroll_read': 'ui_scroll|',
        'governor_remote_prepare': 'governor_remote|',
        'governor_dialog_remote': 'governor_dialog|',
        'governor_dialog_open': 'governor_dialog|',
        'governor_dialog_default': 'governor_dialog|',
        'governor_dialog_more': 'governor_dialog|',
        'governor_dialog_roles': 'governor_dialog|',
        'governor_dialog_cancel': 'governor_dialog|',
        'governor_dialog_goodbye': 'governor_dialog|',
        'governor_dialog_read': 'governor_dialog|',
        'governor_dialog_release': 'governor_dialog|',
        'governor_dialog_assign': 'governor_dialog|',
        'governor_dialog_back': 'governor_dialog|',
        'personnel_autonomous_read': 'personnel_autonomous|',
        'personnel_prerequisite': 'personnel_prerequisite|',
        'hire_candidate_next': 'hire_candidate_next|',
        'hire_setup': 'hire_setup|',
        'governor_roles_setup': 'governor_roles_setup|',
        'governor_roles_check': 'governor_roles_check|',
        'governor_roles_read': 'governor_roles_read|',
        'personnel_transfer_prepare': 'personnel_transfer|',
        'personnel_transfer_fixture': 'personnel_transfer|',
        'save_validation': 'save_validation|',
        'save_checkpoint': 'save_checkpoint|',
        'save_remote_personnel': 'save_remote_personnel|',
        'save_current_status': 'save_current_status|',
        'save_scenario_checkpoint': 'save_scenario_checkpoint|',
        'save_station_package': 'save_station_package|',
        'local_builder': 'local_builder|',
        'local_owned_builder': 'local_builder|',
        'construction_blueprint_prepare': 'construction_blueprint_prepare|',
        'expansion_native_fixture': 'expansion_fixture|',
        'construction_handoff': 'construction_handoff|',
        'crew_docked_prepare': 'crew_docked_prepare|',
        'military_fleet_prepare': 'military_fleet_prepare|',
        'supply_setup': 'supply_setup|',
        'supply_quote': 'supply_quote|',
        'supply_step': 'supply_step|',
        'supply_read': 'supply_read|',
        'repair_setup': 'repair_setup|',
        'repair_scenario': 'repair_scenario|',
        'repair_read': 'repair_read|',
        'native_analysis': 'native_analysis|',
        'economic_search_start': 'economic_search|',
        'economic_transport_prepare': 'economic_prepare|',
        'crew_remote_prepare': 'crew_remote|',
        'crew_remote_transfer': 'crew_remote|',
        'crew_remote_read': 'crew_remote|',
        'governor_ownership_loss': 'governor_ownership|',
        'governor_ownership_restore': 'governor_ownership|',
        'governor_ownership_read': 'governor_ownership|',
        'station_manager_replace': 'station_manager_period|',
        'station_manager_vacate': 'station_manager_period|',
        'crew_capacity_check': 'crew_capacity|',
        'station_manager_restore_prepare': 'station_manager_period|',
        'station_manager_restore': 'station_manager_period|',
        'station_manager_read': 'station_manager_period|',
        'economic_search_priority': 'economic_search|',
        'economic_search_priority_read': 'economic_search|',
        'economic_search_read': 'economic_search|',
        'service_setup': 'service_setup|',
        'station_supply_setup': 'station_supply_setup|',
        'station_budget_setup': 'station_budget_setup|',
        'provision_read': 'provision|',
        'mining_setup': 'mining_setup|',
        'mining_trace_arm': 'mining_trace|',
        'mining_trace_read': 'mining_trace|',
        'projection_raw': 'projection_raw|',
        'save_boundary_package': 'save_boundary_package|',
        'save_domain_checkpoint': 'save_domain_checkpoint|',
        'domain_surplus_prepare': 'domain|',
        'domain_threat_prepare': 'domain|',
        'domain_read': 'domain|',
        'domain_threat_range': 'domain|',
        'domain_threat_retire': 'domain|',
        'domain_buyer_support': 'domain|',
        'domain_threat_distress': 'domain|',
        'domain_threat_provoke': 'domain|',
        'domain_large_asset_loss': 'domain|',
        'domain_large_assets': 'domain|',
        'domain_mining_resources': 'domain|',
        'domain_complete_crews': 'domain|',
        'domain_builder_repath': 'domain|',
        'domain_threat_resume': 'domain|',
        'domain_threat_transport': 'domain|',
        'domain_seta_begin': 'domain|',
        'domain_seta_end': 'domain|',
        'domain_surplus_watch': 'domain|',
        'domain_surplus_open': 'domain|',
        'domain_market_source': 'domain|',
        'domain_market_buyer': 'domain|',
        'domain_builder_position': 'domain|',
        'crew_blocked_prepare': 'crew_blocked|',
        'crew_blocked_transfer': 'crew_blocked|',
        'crew_blocked_destination_loss': 'crew_blocked|',
        'crew_blocked_read': 'crew_blocked|',
        'lifecycle_prepare': 'lifecycle|',
        'lifecycle_bind': 'lifecycle|',
        'lifecycle_module_loss': 'lifecycle|',
        'lifecycle_station_loss': 'lifecycle|',
        'lifecycle_actor_loss': 'lifecycle|',
        'lifecycle_rebind': 'lifecycle|',
        'lifecycle_restore': 'lifecycle|',
        'lifecycle_read': 'lifecycle|',
        'mining_read': 'mining_read|',
        'factory_build_start': 'factory_build_start|',
        'builder_near': 'builder_near|',
        'construction_resources': 'construction_resources|',
        'ui_status': 'ui|mode=tm_empire_status|',
        'ui_empire': 'ui|mode=empire|',
        'ui_stats': 'ui|mode=stats|',
    }.get(frame.split('|', 1)[0])
    if expected and not any(line.startswith(expected) for line in result.splitlines()):
        raise ValueError('Ответ не соответствует команде ' + frame
                         + '; эффект не повторяется, следующие шаги остановлены')
    return result


def request_status_save(pipe, folder):
    """Проверка физического файла перед единственной записью диагностического слота."""
    folder = Path(folder).resolve(strict=True)
    if not folder.is_dir():
        raise ValueError('Папка сохранений отсутствует')
    for suffix in ('.xml', '.xml.gz'):
        try:
            (folder / ('save_011' + suffix)).lstat()
        except FileNotFoundError:
            pass
        else:
            raise FileExistsError('Диагностический слот save_011 занят; запись не отправлена')
    return request(pipe, 'save_current_status|preflight_save_011_absent', timeout=30)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['domain', 'supply_setup', 'supply_quote', 'supply_step', 'supply_read', 'save_validation', 'save_checkpoint', 'priority_setup', 'priority_passenger', 'priority_helm', 'priority_manual', 'priority_priority', 'priority_restore', 'priority_read', 'assessment_fixture', 'trade_decision_fixture', 'trade_quote_probe', 'service_setup', 'builder_near', 'construction_resources', 'repair_setup', 'repair_scenario', 'repair_read', 'military_setup', 'military_fleet_prepare', 'hire_setup', 'hire_scenario', 'hire_candidates', 'station_budget_setup', 'station_supply_setup', 'trade_fixture', 'trade_candidate', 'blueprint', 'expansion', 'personnel_transfer', 'provision', 'training', 'analysis', 'saves', 'load', 'role', 'assign', 'place', 'save', 'module', 'check', 'release', 'role_contract', 'build_contract', 'station_fixture', 'quote_contract', 'quote_ui', 'purchase_fixture', 'purchase_native', 'ui_status', 'ui_empire', 'ui_stats'])
    parser.add_argument('--save', type=save_name)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Свидетельство уже существует')
    if args.mode == 'load' and not args.save:
        parser.error('Укажите точное сохранение')
    name = ('tm_empire_save_menu' if args.mode in ('saves', 'load')
            else 'tm_empire_role_probe')
    pipe = NamedPipeServer(name)
    records = []
    try:
        print('Ожидаю соединения X4: ' + name, flush=True)
        pipe.connect()
        key = 'probe_' + uuid.uuid4().hex[:16]
        if args.mode in ('saves', 'load'):
            deadline = time.monotonic() + 30
            while True:
                response = request(pipe, f'tm_save_menu_v1|{key}|list')
                records.append(response)
                if '|loading|' not in response:
                    break
                if time.monotonic() >= deadline:
                    raise TimeoutError('Список сохранений не готов')
                time.sleep(.2)
            if args.mode == 'load':
                entries = response.split('|', 3)
                if len(entries) != 4 or entries[2] != 'list' or not any(
                        row.split(',')[0] == args.save for row in entries[3].split(';')):
                    raise ValueError('Сохранение недоступно в штатном списке')
                records.append(request(pipe, f'tm_save_menu_v1|{key}_load|load|{args.save}'))
        else:
            records.append(request_status_save(pipe, Path('C:/Users/Avalakh/Documents/Egosoft/X4/138753290/save')) if args.mode == 'save' else request(pipe, {'domain':'domain_read', 'supply_setup':'supply_setup', 'supply_quote':'supply_quote', 'supply_step':'supply_step', 'supply_read':'supply_read', 'save_validation':'save_validation', 'save_checkpoint':'save_checkpoint', 'priority_setup':'priority_setup', 'priority_passenger':'priority_passenger', 'priority_helm':'priority_helm', 'priority_manual':'priority_manual', 'priority_priority':'priority_priority', 'priority_restore':'priority_restore', 'priority_read':'priority_read', 'assessment_fixture':'assessment_fixture', 'trade_decision_fixture':'trade_decision_fixture', 'trade_quote_probe':'trade_quote_probe', 'service_setup':'service_setup', 'builder_near':'builder_near', 'construction_resources':'construction_resources', 'repair_setup':'repair_setup', 'repair_scenario':'repair_scenario', 'repair_read':'repair_read', 'military_setup':'military_setup', 'military_fleet_prepare':'military_fleet_prepare', 'hire_setup':'hire_setup', 'hire_scenario':'hire_scenario', 'hire_candidates':'hire_candidates', 'station_budget_setup':'station_budget_setup', 'trade_fixture':'trade_fixture', 'trade_candidate':'trade_candidate', 'blueprint':'blueprint', 'expansion':'expansion_fixture', 'personnel_transfer':'personnel_transfer_fixture', 'role':'read', 'assign':'assign_fixture',
                                          'place':'place_fixture', 'save':'save_current_status', 'station_fixture':'station_fixture',
                                          'module':'module_fixture', 'check':'check_roles',
                                          'release':'release_fixture', 'role_contract':'role_contract', 'build_contract':'build_contract', 'quote_contract':'quote_contract', 'quote_ui':'quote_ui', 'purchase_fixture':'purchase_fixture', 'purchase_native':'purchase_native', 'ui_status':'ui_status',
                                          'station_supply_setup':'station_supply_setup', 'provision':'provision_read', 'training':'training_fixture', 'analysis':'native_analysis', 'ui_empire':'ui_empire', 'ui_stats':'ui_stats'}[args.mode]))
        print('\n'.join(records), flush=True)
    finally:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps({'mode': args.mode, 'responses': records},
                                          ensure_ascii=False, indent=2), encoding='utf-8')
        pipe.close()


if __name__ == '__main__':
    main()

