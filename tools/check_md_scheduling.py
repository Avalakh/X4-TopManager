"""Проверка собственных MD-циклов на сброс без ожидания; XSD это не проверяет."""
from pathlib import Path
import re
import xml.etree.ElementTree as ET


def polling_without_interval(root):
    problems = []
    for cue in root.iter('cue'):
        conditions = cue.find('conditions')
        if conditions is not None and not any(node.tag.startswith('event_') for node in conditions.iter()):
            if not cue.get('checkinterval'):
                problems.append(cue.get('name', '<unnamed>'))
    return problems


def unsafe_resets(root):
    problems = []
    for cue in root.iter('cue'):
        actions = cue.find('actions')
        if actions is None or not any(
                node.get('cue') == 'this' for node in actions.iter('reset_cue')):
            continue
        conditions = cue.find('conditions')
        if conditions is not None and any(
                node.tag.startswith('event_') for node in conditions.iter()):
            continue
        delay = cue.find('delay')
        value = delay.get('exact', delay.get('min', '')) if delay is not None else ''
        match = re.fullmatch(r'([0-9]+(?:\.[0-9]+)?)(ms|s|min|h)', value)
        if not match or float(match[1]) <= 0:
            problems.append(cue.get('name', '<unnamed>'))
    return problems


def unsupported_cue_returns(root):
    # common.xsd: return is supported only in MD run_actions libraries.
    problems = []
    for cue in root.iter('cue'):
        actions = cue.find('actions')
        if actions is not None and next(actions.iter('return'), None) is not None:
            problems.append(cue.get('name', '<unnamed>'))
    return problems


def invalid_optional_exists(root):
    # The engine rejects @property? even though XSD treats it as a string.
    # Optional lookup (@) and the existence test (?) are distinct operators.
    return [f'{node.tag}:{key}' for node in root.iter()
            for key, value in node.attrib.items()
            if re.search(r'@[A-Za-z_$][A-Za-z0-9_.$]*\?', value)]


def invalid_run_actions_libraries(root):
    libraries = {node.get('name'): node for node in root.iter('library')}
    problems = set()
    prefix = 'md.' + root.get('name', '') + '.'
    for call in root.iter('run_actions'):
        reference = call.get('ref', '')
        name = reference[len(prefix):] if reference.startswith(prefix) else reference
        library = libraries.get(name)
        if library is not None and library.get('purpose') != 'run_actions':
            problems.add(name)
    for name, library in libraries.items():
        if next(library.iter('return'), None) is not None and library.get('purpose') != 'run_actions':
            problems.add(name)
    return sorted(problems)


if __name__ == '__main__':
    mod = Path(__file__).resolve().parents[1]
    sources = [mod / 'md', mod / 'tests/diagnostics/extension/md']
    failures = []
    for source in sources:
        for path in source.glob('*.xml'):
            root = ET.parse(path).getroot()
            failures.extend(f'{path.name}:{name}' for name in unsafe_resets(root))
            failures.extend(f'{path.name}:{name}:missing_checkinterval' for name in polling_without_interval(root))
            failures.extend(f'{path.name}:{name}:unsupported_cue_return' for name in unsupported_cue_returns(root))
            failures.extend(f'{path.name}:{name}:invalid_optional_exists' for name in invalid_optional_exists(root))
            failures.extend(f'{path.name}:{name}:invalid_run_actions_library' for name in invalid_run_actions_libraries(root))
    for path in (mod / 'native/adapted/md').glob('*.xml'):
        root = ET.parse(path).getroot()
        failures.extend(f'{path.name}:{name}:invalid_optional_exists'
                        for name in invalid_optional_exists(root))
        failures.extend(f'{path.name}:{name}:unsupported_cue_return'
                        for name in unsupported_cue_returns(root))
    if failures:
        raise SystemExit('Непроверенный повтор без явной задержки: ' + ', '.join(failures))
    print('PASS: собственные повторяющиеся MD cue имеют явное ожидание')
