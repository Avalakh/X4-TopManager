"""Изолированная копия фракционного замыкания; ещё не установленный runtime."""
from pathlib import Path
import hashlib
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
MOD = ROOT / 'X4_TopManager'
BASE = ROOT / 'examples/x4_unpacked/md'
STAGE = MOD / 'native/md'
PREFIXES = ('FactionLogic', 'FactionGoal_', 'FactionSubgoal_', 'Job_Helper')


def main():
    # Start from Manager, then only scripts referenced by retained XML nodes.
    sources = {ET.parse(p).getroot().get('name'): p for p in BASE.glob('*.xml')}
    # Goal registry is a dynamic edge, not a textual md-ref in Manager.
    pending, copied = ['FactionLogic', 'FactionGoal_Hold_Space', 'FactionGoal_Invade_Space', 'FinaliseStations'], {}
    while pending:
        name = pending.pop()
        if name in copied:
            continue
        path = sources[name]
        root = ET.parse(path).getroot()
        if name == 'FinaliseStations':
            retained = {'NewStation_GenerateFactory', 'NewStation_GenerateFactory_Signal', 'DefaultCalculateHabitation',
                        'DefaultCalculateDocks', 'DefaultCalculatePiers',
                        'DefaultCalculateDefence', 'DefaultCalculateConnections'}
            for child in list(root.find('cues')):
                if child.get('name') not in retained:
                    root.find('cues').remove(child)
        if name == 'FactionLogic':
            # Keep the private signal endpoint required by Manager children.
            # It has no actions and cannot automatically start NPC managers.
            cues = root.find('cues')
            for child in list(cues):
                if child.get('name') in ('FactionLogicManagers', 'Generate_Global_Report'):
                    cues.remove(child)
        text = ET.tostring(root, encoding='unicode')
        copied[name] = (path, text)
        for ref in re.findall(r'md\.([A-Za-z0-9_]+)\.', text):
            if ref.startswith(PREFIXES) and ref in sources and ref not in copied:
                pending.append(ref)
    mapping = {name: 'TM_Empire_' + name for name in copied}
    manifest = {'qualification': 'staged_isolation_only', 'installed': False,
                'player_runtime_enabled': False, 'namespace_map': mapping, 'records': []}
    manifest['dynamic_edges'] = {'global.$FactionGoals': [
        'FactionGoal_Hold_Space', 'FactionGoal_Invade_Space',
        'FactionGoal_PatrolCoordinationService', 'FactionGoal_Plunder']}
    STAGE.mkdir(parents=True, exist_ok=True)
    for name, (path, text) in sorted(copied.items()):
        # md-name references occur in both XML expressions and ref attributes.
        for original, target in sorted(mapping.items(), key=lambda item: -len(item[0])):
            text = re.sub(r'\bmd\.' + re.escape(original) + r'(?=\.)', 'md.' + target, text)
        text = text.replace('global.$FactionManagers', 'global.$TM_EmpireFactionManagers')
        text = text.replace('global.$FactionGoals', 'global.$TM_EmpireFactionGoals')
        # Own copy must not mutate the game's faction metadata table.
        text = text.replace('md.$FactionData', 'md.$TM_EmpireFactionData')
        # Economy reports and deployable patches also have save-bound globals.
        # No staged copy may write into the original managers' tables.
        text = re.sub(r'global\.\$(?!TM_Empire)([A-Za-z0-9_]+)',
                      r'global.$TM_Empire_\1', text)
        text = re.sub(r'md\.\$(?!TM_Empire|SystemTimeAtGamestart\b)([A-Za-z0-9_]+)',
                      r'md.$TM_Empire_\1', text)
        root = ET.fromstring(text)
        root.set('name', mapping[name])
        external = sorted(set(re.findall(r'md\.([A-Za-z0-9_]+)\.', text)) - set(mapping.values()))
        effects = {}
        for node in root.iter():
            if node.tag.startswith(('create_', 'destroy_', 'request_job', 'commandeer_', 'add_build_', 'set_faction_', 'remove_representative')):
                effects[node.tag] = effects.get(node.tag, 0) + 1
        globals_used = sorted(set(re.findall(r'(?:global|md)\.\$[A-Za-z0-9_]+', text)))
        # These root cues would otherwise register and run in the NPC background.
        # A staged source is intentionally outside md/ and outside install allowlist.
        startup = [node.get('name') for node in root.find('cues') if node.tag == 'cue']
        ET.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        ET.indent(root, space='  ')
        output = STAGE / ('tm_' + path.name)
        data = ET.tostring(root, encoding='utf-8', xml_declaration=True)
        output.write_bytes(data)
        manifest['records'].append(dict(source=str(path.relative_to(ROOT)).replace('\\', '/'),
            source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(), source_md=name,
            target=str(output.relative_to(MOD)).replace('\\', '/'), target_md=mapping[name],
            target_sha256=hashlib.sha256(data).hexdigest(), external_boundaries=external,
            startup_cues=startup, effect_tags=effects, global_tables=globals_used))
    (MOD / 'docs/native-manager-copy.json').write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Copied {len(copied)} isolated scripts; staged only, no player activation')


if __name__ == '__main__':
    main()
