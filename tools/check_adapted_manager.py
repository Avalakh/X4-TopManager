"""Проверка staged HQ-границы; не является игровой приёмкой Manager."""
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from component_records import PATTERN

MOD = Path(__file__).resolve().parents[1]
for path in list((MOD / 'md').glob('*.xml')) + list((MOD / 'native/adapted').rglob('*.xml')):
    assert not PATTERN.search(path.read_text(encoding='utf-8')), ('unsupported component record', path)
runtime = ET.parse(MOD / 'md/tm_empire_runtime.xml').getroot()
assert not list(runtime.iter('commandeer_object'))
assert not list(runtime.iter('release_commandeered_object'))
assert runtime.find("cues/cue[@name='ComponentRecords']/actions") is not None
for filename in ('tm_factionsubgoal_recon.xml', 'tm_factionsubgoal_defendarea.xml'):
    tree = ET.parse(MOD / 'native/adapted/md' / filename).getroot()
    guarded = 0
    for loop in tree.iter('do_all'):
        if not any(node.get('groupname') == '$Ships' and node.get('object') == '$Ship'
                   for node in loop.iter('add_to_group')):
            continue
        selection = list(loop)
        call = next((node for node in selection
                     if node.tag == 'run_actions' and node.get('ref') == 'md.TM_Empire_Runtime.CanUseOwnedShip'), None)
        if call is None:
            continue
        guard = loop.find("do_if[@value='$Ships.indexof.{$Ship}']")
        assert guard is not None and guard.find('continue') is not None, ('duplicate acquisition', filename)
        assert selection.index(guard) < selection.index(call)
        guarded += 1
    assert guarded, ('missing acquisition seam', filename)
manifest = json.loads((MOD / 'docs/native-manager-adapted.json').read_text(encoding='utf-8'))
source = MOD / 'native/md/tm_factionlogic.xml'
target = MOD / 'native/adapted/md/tm_factionlogic.xml'
assert hashlib.sha256(source.read_bytes()).hexdigest() == manifest['source_sha256']
assert hashlib.sha256(target.read_bytes()).hexdigest() == manifest['target_sha256']
assert manifest['installed'] is False
root = ET.parse(target).getroot()
for staged in (MOD / 'native/adapted/md').glob('*.xml'):
    assert not list(ET.parse(staged).getroot().iter('add_build_to_expand_station')), ('unguarded native expansion', staged.name)
manager = root.find("cues/library[@name='Manager']")
assert manager.get('version') == '1' and not manager.findall('patch')
assert manager.find("params/param[@name='HasMissions']").get('default') == 'false'
assert manager.find("actions/do_if[@value='not md.$TM_EmpireFactionData?']/set_value").get('exact') == 'table[]'
assert manager.find("actions/do_if[@value='not md.$TM_EmpireFactionData.{$Faction}?']/set_value").get('exact') == 'table[]'
for name in ('Governor', 'GovernorStation', 'GovernorModule'):
    assert manager.find(f"params/param[@name='{name}']") is not None
names = {node.get('name') for node in root.iter() if node.tag in ('cue', 'library')}
assert not set(manifest['removed_npc_cues']) & names
for node in root.iter():
    assert node.tag not in manifest['forbidden_effects']
    cue = node.get('cue', '')
    if re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', cue) and cue not in ('this', 'parent', 'namespace'):
        assert cue in names, ('missing local cue', cue)
assert manager.find("cues/cue[@name='Find_Faction_Headquarters']/actions/set_value[@name='$HQ']").get('exact') == '$GovernorStation'
assert not (MOD / 'md/tm_factionlogic.xml').exists()
print('PASS: HQ uses governor station; NPC representative/mood effects absent; local cue links intact')
personnel_goal = manager.find("cues/cue[@name='TM_PersonnelGoal']")
assert personnel_goal is not None and personnel_goal.find('actions/reset_cue') is None
tick = personnel_goal.find("cues/cue[@name='TM_PersonnelTick']")
assert tick.find('actions/reset_cue').get('cue') == 'this'
assert tick.find("actions/run_actions/param[@name='GoalCue']").get('value') == 'parent'
assert tick.find("actions/run_actions/param[@name='ManagerCue']").get('value') == 'parent.parent'
economy_source = MOD / 'native/md/tm_factionlogic_economy.xml'
economy_target = MOD / 'native/adapted/md/tm_factionlogic_economy.xml'
selection = manifest['economy_selection']
assert hashlib.sha256(economy_source.read_bytes()).hexdigest() == selection['source_sha256']
assert hashlib.sha256(economy_target.read_bytes()).hexdigest() == selection['target_sha256']
request = ET.parse(economy_target).getroot().find(".//cue[@name='Request_Commandeerable_Freighter']")
assert not list(request.iter('get_suitable_job'))
assert not list(request.iter('request_job_ship'))
for search in request.iter('find_ship_by_true_owner'):
    assert search.get('faction') == '$Faction'
    assert not {'jobtags', 'requestedjobship', 'commandeerable'} & search.attrib.keys()
assert request.find("actions/do_if[@value='$Faction == faction.player']") is not None
assert request.find(".//do_if[@value='not $PotentialShip.cargo.{$Ware}.max']/continue") is not None
assert request.find(".//find_object_component[@weaponmode='weaponmode.mining']") is not None
assert len(request.findall(".//run_actions[@ref='CanUseOwnedShip']")) == 2
assert request.find(".//do_if[@value=\"$Ship.exists and $UseShipReason == 'available'\"]//run_actions[@ref='md.TM_Empire_Runtime.ClaimOwnedShip']") is not None
assert not list(request.iter('commandeer_object'))
guard = ET.parse(economy_target).getroot().find("cues/library[@name='CanUseOwnedShip']")
assert guard.find("actions/run_actions[@ref='md.TM_Empire_Runtime.CanUseOwnedShip']") is not None
runtime = ET.parse(MOD / 'md/tm_empire_runtime.xml').getroot()
shared = runtime.find("cues/library[@name='CanUseOwnedShip']")
assert shared.find("actions/do_if[@value='$Ship == player.controlled']/return").get('value') == "'player_helm'"
assert 'player.occupiedship' not in ET.tostring(shared, encoding='unicode')
assert shared.find(".//do_if[@value='$Claim.$goal != $GoalCue']/return").get('value') == "'claimed_by_other_goal'"
assert all(order.get('name') for order in request.iter('create_order'))
assert not list(request.iter('remove_object_commander'))
assert request.find(".//set_value[@name='$Ship.$tm_empire_claim']") is None
assert request.find(".//run_actions[@ref='md.TM_Empire_Runtime.ClaimOwnedShip']") is not None
print('PASS: owned cargo candidates replace NPC jobs; native mining capability check retained; effects unqualified')
coverage = manifest['owned_ship_guards']
assert len(manifest['aiscripts']) == 3
for row in manifest['aiscripts']:
    path = MOD / row['path']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256']
    ai = ET.parse(path).getroot()
    assert (ai.get('name'), ai.find('order').get('id')) in {
        ('tm.order.deploystaticdefensestrategy', 'TM_DeployStaticDefenseStrategy'),
        ('tm.order.deployobjectatposition', 'TM_DeployObjectAtPosition'),
        ('tm.order.assigncommander', 'TM_AssignCommander')}
    if ai.find('order').get('id') == 'TM_AssignCommander':
        assert not list(ai.iter('cancel_all_orders'))
    assert not any("'StaticDefense_" in value for node in ai.iter() for value in node.attrib.values())
assert len(manifest['closure']) == 13 and set(coverage) == {Path(row['path']).name for row in manifest['closure']}
for row in manifest['closure']:
    path = MOD / row['path']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256']
    graph = ET.parse(path).getroot()
    assert not any("'StaticDefense_" in value for node in graph.iter() for value in node.attrib.values())
    assert not any(node.get('id') == "'DeployStaticDefenseStrategy'" for node in graph.iter('create_order'))
    assert not list(graph.iter('commandeer_object'))
    assert not list(graph.iter('release_commandeered_object'))
    assert not list(graph.iter('remove_object_commander'))
    assert not list(graph.iter('destroy_object'))
    assert not list(graph.iter('create_object'))
    assert not list(graph.iter('set_object_hull'))
    assert not list(graph.iter('set_owner'))
    for npc_job_action in ('get_suitable_job', 'request_job_ship', 'create_job_ship', 'set_job_active'):
        assert not list(graph.iter(npc_job_action)), ('NPC job effect remains', path.name, npc_job_action)
    parents = {child: parent for parent in graph.iter() for child in parent}
    if graph.get('name') == 'TM_Empire_FinaliseStations':
        assert not list(graph.iter('apply_construction_sequence'))
        assert not list(graph.iter('add_build_to_expand_station'))
        report = graph.find(".//cue[@name='NewStation_ConstructionSequenceCompleted']//signal_cue_instantly")
        assert report.get('param') == "['prepared', $ConstructionSequence, null, $Station]"
    if graph.get('name') == 'TM_Empire_FactionSubgoal_BuildStation':
        assert not list(graph.iter('create_station'))
        assert not list(graph.iter('add_build_to_expand_station'))
        timer = graph.find(".//cue[@name='TM_BuildStationProgress']")
        assert timer.find('delay').get('exact') == '15s'
        assert timer.find(".//run_actions[@ref='md.TM_Empire_Construction.RequestPlanValidation']") is not None
        assert timer.find(".//run_actions[@ref='md.TM_Empire_Construction.CreateValidatedNativeStation']") is not None
        assert timer.find(".//run_actions[@ref='md.TM_Empire_Construction.StepCreatedNativeStation']") is not None
    for cancellation in graph.iter():
        if cancellation.tag != 'cancel_cue':
            continue
        siblings = list(parents[cancellation])
        hook = siblings[siblings.index(cancellation) - 1]
        assert hook.tag == 'run_actions' and hook.get('ref') == 'md.TM_Empire_Runtime.RevokeGoalApprovals'
        assert hook.find("param[@name='CancelledCue']").get('value') == cancellation.get('cue')
    if graph.get('name') in ('TM_Empire_FactionSubgoal_Recon', 'TM_Empire_FactionSubgoal_DefendArea'):
        assert not list(graph.iter('request_job_ship'))
        assert graph.find(".//run_actions[@ref='md.TM_Empire_Purchase.PreparePurchase']") is not None
        assert graph.find(".//run_actions[@ref='md.TM_Empire_Purchase.CompletePurchase']") is not None
        assert graph.find(".//cue[@name='PurchasedShipObserved']/delay").get('exact') == '15s'
    for order in graph.iter('create_order'):
        gate = parents[order]
        if order.get('name') == '$TM_IdleOrder':
            assert gate.tag in ('do_if', 'do_elseif', 'do_else')
            assert order.get('name') == '$TM_IdleOrder'
            assert graph.find(".//cue[@name='TM_IdleWorkGoal']//run_actions[@ref='md.TM_Empire_Runtime.RecordOwnedOrder']") is not None
            continue
        assert gate.tag == 'do_if' and gate.get('value') == "$TM_ShipReason == 'available'"
        assert order.get('name') and gate.find("run_actions[@ref='md.TM_Empire_Runtime.RecordOwnedOrder']") is not None
print('PASS: 13-script closure uses shared guards and native order receipts; no direct commandeer/release/commander removal')

# AI cannot resolve symbolic MD cue paths. Check the whole installed source
# boundary and synchronous publication, including loss/cancellation branches.
for directory in (MOD / 'aiscripts', MOD / 'native/adapted/aiscripts'):
    for path in directory.glob('*.xml'):
        source = path.read_text(encoding='utf-8')
        assert 'md.TM_Empire_Runtime.Registry.' not in source, path
        assert 'md.TM_Empire_Assets.State.' not in source, path
for directory in (MOD / 'md', MOD / 'native/adapted/md'):
    for path in directory.glob('*.xml'):
        graph = ET.parse(path).getroot()
        for parent in graph.iter():
            children = list(parent)
            for index, node in enumerate(children):
                if node.tag not in ('set_value', 'remove_value') or node.get('name') not in (
                    'Registry.$State', 'Registry.$ManagerCue',
                    'md.TM_Empire_Runtime.Registry.$State', 'md.TM_Empire_Runtime.Registry.$ManagerCue'):
                    continue
                assert index + 1 < len(children), (path, node.attrib)
                assert children[index + 1].tag == 'run_actions' and children[index + 1].get('ref') == 'md.TM_Empire_Runtime.PublishAIState', (path, node.attrib)
print('PASS: all AI state reads use shared global; every registry mutation publishes synchronously')
