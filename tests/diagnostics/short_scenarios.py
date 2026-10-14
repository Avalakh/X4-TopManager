"""Короткий игровой пакет; подготовка мира один раз, затем только read-back."""
import argparse
import json
import time
from pathlib import Path

from named_pipe import NamedPipeServer
from probe import request


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=False)
    pipe = NamedPipeServer('tm_empire_role_probe')
    records = []

    def invoke(command):
        response = request(pipe, command)
        records.append({'command': command, 'response': response})
        (args.output_dir / 'responses.json').write_text(
            json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
        for line in response.splitlines():
            if line.startswith(('trade_decision_fixture|', 'trade_decision_case|', 'trade_choice|',
                                'repair_setup|', 'repair_scenario|', 'repair_read|',
                                'hire_setup|', 'hire_scenario|', 'military_setup|',
                                'military_territory|', 'military_goal|', 'receipts|')):
                print(line, flush=True)
        return response

    try:
        print('Ожидаю готовый игровой мир; один владелец pipe.', flush=True)
        pipe.connect()
        prepared = invoke('hire_setup')
        # A failed or previously submitted preparation never dispatches again.
        if any(line.startswith('hire_setup|state=prepared|')
               for line in prepared.splitlines()):
            invoke('hire_scenario')
        invoke('military_setup')
        repair = invoke('repair_setup')
        repair_prepared = any(line.startswith('repair_setup|state=prepared|')
                              for line in repair.splitlines())
        if repair_prepared:
            invoke('repair_scenario')
        for index in range(4):
            if index:
                time.sleep(10)
            invoke('read')
            if repair_prepared:
                invoke('repair_read')
    finally:
        pipe.close()


if __name__ == '__main__':
    main()
