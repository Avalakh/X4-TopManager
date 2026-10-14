"""Проверить изоляцию staged копии и оригиналы; не доказывает готовность AI."""
from pathlib import Path
import hashlib
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
MOD = ROOT / 'X4_TopManager'
manifest = json.loads((MOD / 'docs/native-manager-copy.json').read_text(encoding='utf-8'))
mapping = manifest['namespace_map']
assert manifest['installed'] is False and manifest['player_runtime_enabled'] is False
definitions = {}
for record in manifest['records']:
    tree = ET.parse(MOD / record['target'])
    definitions[record['target_md']] = {
        node.get('name') for node in tree.iter() if node.tag in ('cue', 'library')
    }
for record in manifest['records']:
    source, target = ROOT / record['source'], MOD / record['target']
    assert hashlib.sha256(source.read_bytes()).hexdigest() == record['source_sha256']
    assert hashlib.sha256(target.read_bytes()).hexdigest() == record['target_sha256']
    text = target.read_text(encoding='utf-8')
    root = ET.fromstring(text)
    assert root.get('name') == record['target_md']
    for original in mapping:
        assert not re.search(r'\bmd\.' + re.escape(original) + r'\.', text), (target, original)
    assert 'global.$FactionManagers' not in text and 'global.$FactionGoals' not in text
    assert 'md.$FactionData' not in text
    assert not re.search(r'global\.\$(?!TM_Empire)[A-Za-z0-9_]+', text)
    assert not re.search(r'md\.\$(?!TM_Empire|SystemTimeAtGamestart\b)[A-Za-z0-9_]+', text)
    assert target.parts[-3:-1] == ('native', 'md')
    # Pruning roots may leave children pointing at a missing private endpoint.
    for node in root.iter():
        for attribute in ('cue', 'ref'):
            match = re.fullmatch(r'md\.([A-Za-z0-9_]+)\.([A-Za-z0-9_]+)', node.get(attribute, ''))
            if match and match[1] in definitions:
                assert match[2] in definitions[match[1]], (target, attribute, match[0])
    if record['source_md'] == 'FactionLogic':
        assert root.find("cues/cue[@name='FactionLogicManagers']") is None
        endpoint = root.find("cues/cue[@name='FactionSignalled']")
        assert endpoint is not None
        assert endpoint.find('conditions/event_cue_signalled') is not None
        assert endpoint.find('actions') is None
        assert root.find("cues/cue[@name='Generate_Global_Report']") is None
        assert root.find("cues/library[@name='Manager']").get('version') == '18'
    if record['source_md'] == 'FinaliseStations':
        assert root.find("cues/cue[@name='God_DefaultFinaliseFactory']") is None
        assert root.find("cues/cue[@name='NewStation_GenerateFactory_God_Runtime']") is None
        assert root.find("cues/cue[@name='Update_Neighbor_Defense_Station_Loadout']") is None
        endpoint = root.find("cues/cue[@name='NewStation_GenerateFactory_Signal']")
        assert endpoint.find('conditions/event_cue_signalled') is not None
        assert root.find("cues/library[@name='NewStation_GenerateFactory']") is not None
print(f"PASS: {len(manifest['records'])} isolated source copies; originals unchanged; AI unqualified")
