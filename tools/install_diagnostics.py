"""Установка отдельного тестового расширения по его собственному content ID."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game', type=Path, required=True)
    parser.add_argument('--receipt', type=Path, required=True)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    source = ROOT / 'tests/diagnostics/extension'
    identity = ET.parse(source / 'content.xml').getroot().get('id')
    if identity != 'tm_empire_diagnostics':
        raise ValueError('Неизвестное диагностическое расширение')
    game = args.game.absolute()
    if not game.is_dir():
        raise FileNotFoundError('Папка X4 не найдена: ' + str(game))
    extensions = game / 'extensions'
    destination = extensions / identity
    for folder in extensions.iterdir():
        content = folder / 'content.xml'
        if folder.is_dir() and content.is_file() and folder != destination:
            try:
                other_id = ET.parse(content).getroot().get('id')
            except ET.ParseError:
                continue
            if other_id == identity:
                raise ValueError('Дубликат диагностического content ID: ' + str(folder))
    if args.receipt.exists():
        raise FileExistsError('Квитанция уже существует')
    records = []
    for path in sorted(source.rglob('*')):
        if not path.is_file():
            continue
        relative = path.relative_to(source)
        target = destination / relative
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if not args.dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
                raise ValueError('SHA не совпал: ' + str(relative))
        records.append({'path': relative.as_posix(), 'sha256': digest})
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps({'id': identity, 'destination': str(destination),
                                      'dry_run': args.dry_run, 'files': records},
                                     ensure_ascii=False, indent=2), encoding='utf-8')
    print('PASS: diagnostics ' + str(len(records)) + ' files; ' + str(destination))


if __name__ == '__main__':
    main()
