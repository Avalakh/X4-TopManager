"""Сводка записанных игровых наблюдений; не заменяет приёмку доменов."""
import argparse
import json
from pathlib import Path


def records(path):
    data = json.loads(path.read_text(encoding='utf-8'))
    for response in data['responses']:
        for line in response.splitlines():
            parts = line.split('|')
            yield parts[0], dict(part.split('=', 1) for part in parts[1:] if '=' in part)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Свидетельство уже существует')
    ages, cycles, builders, trades = [], set(), {}, {}
    files = sorted(args.input.glob('*-role.json'))
    for path in files:
        for kind, row in records(path):
            if kind == 'runtime' and row.get('state') == 'active':
                ages.append(float(row['age']))
                if row.get('economy_last_run') not in (None, 'null', 'nil'):
                    cycles.add(float(row['economy_last_run']))
            elif kind == 'builder_lua' and row.get('board') == '$tm_empire_builder_result':
                if row.get('paid') not in (None, 'null', 'nil'):
                    builders[row['key']] = row
            elif kind == 'trade_fixture_receipt' and row.get('trade') not in (None, 'null', 'nil'):
                trades[(row.get('phase'), row['trade'], row.get('state'))] = row
    chronological = all(a <= b for a, b in zip(ages, ages[1:]))
    result = {'qualified_release': False, 'role_files': len(files),
              'active_runtime_samples': len(ages), 'chronological_game_ages': chronological,
              'first_game_age': ages[0] if ages else None,
              'last_game_age': ages[-1] if ages else None,
              'observed_game_seconds': ages[-1] - ages[0] if ages and chronological else None,
              'distinct_observed_economy_cycle_times': sorted(cycles),
              'observed_paid_builder_receipts': list(builders.values()),
              'observed_trade_states': list(trades.values()),
              'limitation': 'Снимки могут пропускать промежуточные события. Длительность и квитанции не закрывают обязательные домены.'}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({key: result[key] for key in ('role_files', 'active_runtime_samples', 'observed_game_seconds', 'qualified_release')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
