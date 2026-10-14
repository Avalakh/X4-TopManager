"""Установить только source игрового мода; тестовые расширения исключены."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ENTRIES = ('content.xml', 'assets', 'libraries', 'index', 't', 'md', 'aiscripts', 'ui', 'ui.xml')


def validate_ui_modules(root=ROOT):
    """Reject missing engine registration before copying any package file."""
    declared = [node.attrib['name'] for node in ET.parse(root / 'ui.xml').iter('file')]
    if len(declared) != len(set(declared)):
        raise ValueError('Повторный Lua-файл в ui.xml')
    modules = {}
    for relative in declared:
        path = root / relative
        if not path.is_file() or path.suffix != '.lua' or path.parent != root / 'ui':
            raise ValueError('Недопустимый Lua-файл в ui.xml: ' + relative)
        name = 'extensions.tm_empire_management.ui.' + path.stem
        source = path.read_text(encoding='utf-8')
        if not re.search(r"Register_Require_With_Init\(\s*['\"]" + re.escape(name) + r"['\"]", source):
            raise ValueError('Lua-модуль не зарегистрирован: ' + name)
        modules[name] = source
    for source in modules.values():
        for dependency in re.findall(r"require\(\s*['\"](extensions\.tm_empire_management\.ui\.[^'\"]+)['\"]", source):
            if dependency not in modules:
                raise ValueError('Lua-зависимость отсутствует в ui.xml: ' + dependency)


def installation_files(include_adapted=False):
    """Проверить полный набор до первого изменения установленного расширения."""
    validate_ui_modules()
    files = {}
    for entry in ENTRIES:
        source = ROOT / entry
        if not source.exists():
            continue
        for path in source.rglob('*') if source.is_dir() else [source]:
            if path.is_file():
                files[path.relative_to(ROOT)] = path
    if include_adapted:
        manifest = json.loads((ROOT / 'docs/native-manager-adapted.json').read_text(encoding='utf-8'))
        expected = manifest['closure'] + manifest['aiscripts']
        actual = set((ROOT / 'native/adapted/md').glob('*.xml')) | set((ROOT / 'native/adapted/aiscripts').glob('*.xml'))
        if actual != {(ROOT / item['path']) for item in expected}:
            raise ValueError('Staged пакет не совпадает с полным манифестом')
        for item in expected:
            path = ROOT / item['path']
            relative = path.relative_to(ROOT / 'native/adapted')
            if relative in files or hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
                raise ValueError('Конфликт пути или изменившийся SHA: ' + str(relative))
            files[relative] = path
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game', type=Path, required=True)
    parser.add_argument('--include-adapted', action='store_true', help='Включить полный staged Manager для игровой приёмки')
    parser.add_argument('--dry-run', action='store_true', help='Проверить состав и SHA без изменения установки')
    args = parser.parse_args()
    # On this Windows host Python's realpath() can raise WinError 5 for the
    # Steam library although ordinary file access is permitted.
    game = args.game.absolute()
    if not (game / 'X4.exe').is_file():
        raise ValueError('Не найдена X4.exe')
    target = game / 'extensions' / 'tm_empire_management'
    if not args.include_adapted and (target / 'md/tm_factionlogic.xml').exists():
        raise ValueError('Установлен полный Manager: частичная перезапись запрещена; используйте --include-adapted')
    files = installation_files(args.include_adapted)
    if args.dry_run:
        print(f'Проверено {len(files)} файлов; staged Manager: {args.include_adapted}; установка не изменена')
        return
    manifest = []
    for relative, path in files.items():
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if hashlib.sha256(destination.read_bytes()).hexdigest() != digest:
            raise ValueError('Копия отличается: ' + str(relative))
        manifest.append({'path': relative.as_posix(), 'sha256': digest})
    output = ROOT / 'docs' / 'installed-manifest.json'
    output.write_text(json.dumps({'target': str(target), 'qualified_release': False, 'includes_adapted_manager': args.include_adapted,
                                  'files': manifest}, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Установлено {len(manifest)} файлов в {target}; игровая приёмка не выполнена')


if __name__ == '__main__':
    main()
