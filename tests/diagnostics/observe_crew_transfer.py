"""Наблюдение конкретного ранее отправленного перевода; не отправляет команд."""
import argparse
import json
import time
from pathlib import Path

from named_pipe import NamedPipeServer
from probe import request
from lifecycle import fields


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--person', required=True)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument('--target', help='MD component в текущей загруженной сессии')
    target.add_argument('--target-idcode', help='Постоянный игровой код корабля после save/load')
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--timeout', type=int, default=600)
    args = parser.parse_args()
    if not 1 <= args.timeout <= 900:
        parser.error('Наблюдение ограничено 1–900 секундами')
    args.output_dir.mkdir(parents=True, exist_ok=False)
    deadline = time.monotonic() + args.timeout
    outcome = {'status': 'unverified', 'person': args.person, 'target': args.target,
               'target_idcode': args.target_idcode,
               'scope': 'arrival of one existing crew transfer; no dispatch or save/load proof'}
    try:
        serial = 0
        while True:
            pipe = NamedPipeServer('tm_empire_role_probe')
            try:
                pipe.connect()
                response = request(pipe, 'read')
            finally:
                pipe.close()
            serial += 1
            (args.output_dir / f'{serial:03d}-read.json').write_text(
                json.dumps({'mode': 'role', 'responses': [response]},
                           ensure_ascii=False, indent=2), encoding='utf-8')
            rows = response.splitlines()
            current_target = args.target
            if args.target_idcode:
                # Component handles могут измениться при load. Штатный idcode
                # связывается с текущим handle из того же полного read-back.
                ships = [row.split('|') for row in rows if row.startswith('ship|')]
                targets = [row[1] for row in ships if len(row) > 2
                           and row[2] == args.target_idcode]
                if len(targets) != 1:
                    raise RuntimeError('Корабль с указанным игровым кодом не найден однозначно')
                current_target = targets[0]
                outcome['target'] = current_target
            crews = [fields(row) for row in rows if row.startswith('crew_arrival|')]
            receipts = [fields(row) for row in rows if row.startswith('personnel_arrival|')]
            matches = [row for row in crews if row.get('person') == args.person
                       and row.get('target') == current_target]
            matching_receipts = [row for row in receipts if row.get('kind') == 'transfer'
                                 and row.get('person') == args.person
                                 and row.get('target') == current_target]
            if len(matches) != 1 or len(matching_receipts) != 1:
                raise RuntimeError('Конкретная квитанция перевода отсутствует или изменилась')
            crew, receipt = matches[0], matching_receipts[0]
            outcome['crew'] = crew
            outcome['receipt'] = receipt
            if receipt.get('state') == 'observed':
                if not (crew.get('target_member') == '1'
                        and crew.get('actual_role') == crew.get('expected_role')
                        and crew.get('intransit') == '0'
                        and crew.get('scheduled') == '0'
                        and crew.get('pod_arrival') == 'null'
                        and crew.get('source_member') == '0'):
                    raise RuntimeError('Observed не подтверждается фактическим экипажем')
                outcome['status'] = 'passed'
                print('Прибытие того же сотрудника подтверждено', flush=True)
                return
            if receipt.get('state') not in ('sent', 'unknown'):
                raise RuntimeError('Перевод завершился без подтверждённого прибытия')
            if time.monotonic() >= deadline:
                outcome['reason'] = 'observation_timeout_without_dispatch_retry'
                print('Прибытие не подтверждено; перевод не повторяется', flush=True)
                return
            time.sleep(5)
    except Exception as exc:
        outcome['reason'] = str(exc)
        raise
    finally:
        (args.output_dir / 'result.json').write_text(
            json.dumps(outcome, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
