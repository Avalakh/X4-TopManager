"""Игровая проверка остановки и повторного назначения; только диагностика."""
import argparse
import json
import time
from pathlib import Path

from named_pipe import NamedPipeServer
from probe import request


def fields(line):
    return dict(part.split('=', 1) for part in line.split('|') if '=' in part)


def record(lines, prefix):
    return fields(next(line for line in lines if line.startswith(prefix + '|')))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=False)
    serial = 0

    def call(mode):
        nonlocal serial
        pipe = NamedPipeServer('tm_empire_role_probe')
        try:
            pipe.connect()
            response = request(pipe, mode)
        finally:
            pipe.close()
        serial += 1
        (args.output_dir / f'{serial:02d}-{mode}.json').write_text(
            json.dumps({'mode': mode, 'responses': [response]}, ensure_ascii=False, indent=2),
            encoding='utf-8')
        return response.splitlines()

    def active():
        for _ in range(10):
            lines = call('read')
            if record(lines, 'runtime')['state'] == 'active':
                return lines
            time.sleep(2)
        raise AssertionError('Управляющий не перешёл в active')

    before = active()
    coverage = record(before, 'ship_coverage')
    assert coverage['complete'] == '1' and coverage['read'] == coverage['total']
    patrol = record(before, 'patrol_registration')
    assert patrol['index'] != 'null' and patrol['service'] != 'null'
    employee = record(before, 'binding')['employee']
    starting_claims = sum(fields(line).get('claim') != 'null'
                          for line in before if line.startswith('ship|'))
    print('Исходный управляющий активен; охват кораблей полный', flush=True)
    released = call('release_fixture')
    assert any(line.startswith('release|unbound|manager_unchanged=1') for line in released)
    stopped = call('read')
    assert record(stopped, 'runtime')['state'] == 'inactive'
    stopped_coverage = record(stopped, 'ship_coverage')
    assert stopped_coverage['complete'] == '1'
    ships = [fields(line) for line in stopped if line.startswith('ship|')]
    assert len(ships) == int(stopped_coverage['total'])
    assert all(ship['claim'] == 'null' and ship['tracked_orders'] == 'null' for ship in ships)
    print('Остановка подтверждена; собственные claims очищены', flush=True)
    assigned = record(call('place_fixture'), 'reassign')
    assert assigned['result'] == 'bound' and assigned['employee'] == employee
    assert assigned['manager_unchanged'] == '1'
    after = active()
    assert record(after, 'binding')['employee'] == employee
    after_patrol = record(after, 'patrol_registration')
    assert after_patrol['index'] == patrol['index']
    assert after_patrol['service'] == patrol['service']
    assert after_patrol['factions'] == patrol['factions']
    print('Повторное назначение подтверждено; регистрация патрулей сохранена', flush=True)
    (args.output_dir / 'result.json').write_text(json.dumps({
        'status': 'passed', 'employee': employee, 'patrol': after_patrol,
        'starting_claims': starting_claims,
        'scope': 'stop/reassign of same governor; no payment, loss or two-hour acceptance'
    }, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
