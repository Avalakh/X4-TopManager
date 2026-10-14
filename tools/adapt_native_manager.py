"""Воспроизводимая адаптация границы HQ; staged, не активирует AI."""
from pathlib import Path
import hashlib
import json
import shutil
import copy
import re
from functools import lru_cache
import xml.etree.ElementTree as ET
from component_records import normalize_tree

MOD = Path(__file__).resolve().parents[1]
SOURCE = MOD / 'native/md/tm_factionlogic.xml'
TARGET = MOD / 'native/adapted/md/tm_factionlogic.xml'


def batch_economic_ship_selection(graph):
    """Порционный обход штатного списка без ложного отрицательного результата."""
    if graph.get('name') != 'TM_Empire_FactionLogic_Economy':
        return
    request = graph.find(".//cue[@name='Request_Commandeerable_Freighter']")
    if request is None:
        raise ValueError('Missing native commandeer request')
    # Export the contextual cue handle like native faction subgoal callbacks;
    # consumers must not construct a child-cue name from a namespace value.
    economy = graph.find(".//library[@name='Econ_Manager']")
    ET.SubElement(economy.find('actions'), 'set_value', name='$tm_empire_search_cue', exact='Request_Commandeerable_Freighter')
    evaluate = economy.find("cues/cue[@name='EvaluateShortages']/actions")
    evaluate.insert(0, ET.Element('set_value', name='$tm_empire_search_cue', exact='Request_Commandeerable_Freighter'))
    actions = request.find('actions')
    branch = next(n for n in actions if n.tag == 'do_if' and n.get('value') == '$Faction == faction.player')
    clusters = branch.find("do_all[@exact='$LocalClusters.count']")
    candidates = clusters.find("do_all[@exact='$PotentialShips.count']")
    priority = clusters.find("do_if[@value='$Priority']")
    prepare = priority.find("do_all[@exact='$Temp_PotentialShips.count']")
    # Сохранить проверенный native effect tail; выполняется только один раз,
    # после полного поиска или нахождения кандидата. Его namespace остаётся Request.
    tail = list(branch)[list(branch).index(clusters) + 1:]
    for node in list(branch)[list(branch).index(clusters):]:
        branch.remove(node)
    ET.SubElement(branch, 'set_value', name='$TM_SearchEconomyCue', exact='parent')
    ET.SubElement(branch, 'set_value', name='$TM_ManagerCue', exact='parent.$FactionManagerCue')
    ET.SubElement(branch, 'set_value', name='$TM_SearchPhase', exact="'cluster'")
    ET.SubElement(branch, 'set_value', name='$i', exact='1')
    ET.SubElement(branch, 'set_value', name='$TM_SearchCursor', exact='1')
    ET.SubElement(branch, 'set_value', name='$TM_SearchDone', exact='false')
    ET.SubElement(branch, 'set_value', name='$TM_SearchCommitted', exact='false')
    ET.SubElement(branch, 'set_value', name='$ActionDefinition.$TM_SearchCue', exact='namespace')
    ET.SubElement(branch, 'set_value', name='$ActionDefinition.$TM_SearchState', exact="'searching'")
    ET.SubElement(branch, 'set_value', name='$TM_WaitReason', exact="'economic_ship_search_incomplete'")
    children = request.find('cues')
    native_children = list(children)
    for node in native_children:
        children.remove(node)
    tick = ET.SubElement(children, 'cue', name='TM_Commandeer_SearchBatch', checkinterval='1s')
    conditions = ET.SubElement(tick, 'conditions')
    ET.SubElement(conditions, 'check_value', value='$TM_SearchPhase? and not $TM_SearchDone')
    ET.SubElement(tick, 'delay', exact='1s')
    work = ET.SubElement(tick, 'actions')
    valid = ET.SubElement(work, 'do_if', value="$TM_SearchEconomyCue.exists and $TM_ManagerCue.exists and md.TM_Empire_Runtime.Registry.$State == 'active' and md.TM_Empire_Runtime.Registry.$ManagerCue == $TM_ManagerCue and $Requester.exists and $ActionDefinition.$TM_Requester == $Requester and not @$ActionDefinition.$Disregard")
    loop = ET.SubElement(valid, 'do_all', exact='32', counter='$TM_SearchWork')
    cluster = ET.SubElement(loop, 'do_if', value="$TM_SearchPhase == 'cluster'")
    exhausted = ET.SubElement(cluster, 'do_if', value='$i gt $LocalClusters.count')
    ET.SubElement(exhausted, 'set_value', name='$TM_SearchDone', exact='true')
    ET.SubElement(exhausted, 'break')
    start = ET.SubElement(cluster, 'do_else')
    ET.SubElement(start, 'set_value', name='$TM_SearchCursor', exact='1')
    prioritized = ET.SubElement(start, 'do_if', value='$Priority')
    for node in list(priority)[:list(priority).index(prepare)]:
        prioritized.append(copy.deepcopy(node))
    ET.SubElement(prioritized, 'set_value', name='$TM_SearchPhase', exact="'prepare'")
    ordinary = ET.SubElement(start, 'do_else')
    native_else = clusters.find('do_else')
    for node in native_else:
        ordinary.append(copy.deepcopy(node))
    ET.SubElement(ordinary, 'set_value', name='$TM_SearchPhase', exact="'candidate'")
    preparing = ET.SubElement(loop, 'do_elseif', value="$TM_SearchPhase == 'prepare'")
    ready = ET.SubElement(preparing, 'do_if', value='$TM_SearchCursor gt $Temp_PotentialShips.count')
    ET.SubElement(ready, 'remove_value', name='$Temp_PotentialShips')
    ET.SubElement(ready, 'set_value', name='$TM_SearchCursor', exact='1')
    ET.SubElement(ready, 'set_value', name='$TM_SearchPhase', exact="'candidate'")
    item = ET.SubElement(preparing, 'do_else')
    ET.SubElement(item, 'set_value', name='$k', exact='$TM_SearchCursor')
    ET.SubElement(item, 'set_value', name='$TM_SearchCursor', operation='add', exact='1')
    live = ET.SubElement(item, 'do_if', value='$Temp_PotentialShips.{$k}.exists and $Temp_PotentialShips.{$k}.isplayerowned')
    for node in prepare:
        live.append(copy.deepcopy(node))
    selecting = ET.SubElement(loop, 'do_elseif', value="$TM_SearchPhase == 'candidate'")
    next_cluster = ET.SubElement(selecting, 'do_if', value='$TM_SearchCursor gt $PotentialShips.count')
    ET.SubElement(next_cluster, 'set_value', name='$i', operation='add', exact='1')
    ET.SubElement(next_cluster, 'set_value', name='$TM_SearchPhase', exact="'cluster'")
    item = ET.SubElement(selecting, 'do_else')
    ET.SubElement(item, 'set_value', name='$k', exact='$TM_SearchCursor')
    ET.SubElement(item, 'set_value', name='$TM_SearchCursor', operation='add', exact='1')
    missing = ET.SubElement(item, 'do_if', value='not $PotentialShips.{$k}.exists or not $PotentialShips.{$k}.isplayerowned')
    ET.SubElement(missing, 'continue')
    for node in candidates:
        item.append(copy.deepcopy(node))
    found = ET.SubElement(valid, 'do_if', value='$Ship.exists')
    ET.SubElement(found, 'set_value', name='$TM_SearchDone', exact='true')
    again = ET.SubElement(valid, 'do_if', value='not $TM_SearchDone')
    ET.SubElement(again, 'reset_cue', cue='this')
    invalid = ET.SubElement(work, 'do_else')
    ET.SubElement(invalid, 'set_value', name='$ActionDefinition.$Disregard', exact='true')
    ET.SubElement(invalid, 'run_actions', ref='md.TM_Empire_Runtime.RevokeGoalApprovals').append(
        ET.Element('param', name='CancelledCue', value='Request_Commandeerable_Freighter'))
    ET.SubElement(invalid, 'cancel_cue', cue='Request_Commandeerable_Freighter')
    # Completion is a sibling: resetting a batching cue must never disable
    # the continuation which consumes its final result.
    done = ET.SubElement(children, 'cue', name='TM_Commandeer_SearchComplete', checkinterval='1s')
    conditions = ET.SubElement(done, 'conditions')
    # Loaded pre-batching requests have no search fields. They must retain
    # their old receipts without starting this newly added continuation.
    ET.SubElement(conditions, 'check_value', value='$TM_SearchDone? and $TM_SearchDone and not @$TM_SearchCommitted')
    completion = ET.SubElement(done, 'actions')
    ET.SubElement(completion, 'set_value', name='$TM_SearchCommitted', exact='true')
    ET.SubElement(completion, 'set_value', name='$ActionDefinition.$TM_SearchState', exact="'finished'")
    ET.SubElement(completion, 'set_value', name='$ActionDefinition.$TM_SearchResult', exact="if $Ship.exists then 'candidate_found' else 'exhausted'")
    ET.SubElement(completion, 'remove_value', name='$TM_WaitReason')
    for node in tail:
        completion.append(node)
    # parent is now a batching cue; preserve the original economy context.
    for node in list(tick.iter()) + list(done.iter()):
        for key, value in list(node.attrib.items()):
            node.set(key, value.replace('parent.$FactionManagerCue', '$TM_SearchEconomyCue.$FactionManagerCue'))
    lifetime = ET.SubElement(done, 'cues')
    lifetime_names = {
        'Request_Commandeerable_Freighter_Disregard_Patch': 'TM_Commandeer_DisregardTimer',
        'Request_Commandeerable_Freighter_Disregarded': 'TM_Commandeer_Disregarded',
        'Request_Commandeerable_Freighter_Destroyed': 'TM_Commandeer_Destroyed',
    }
    for node in native_children:
        # The old position can be serialized in saves. New unique names avoid
        # merging saved old-parent nodes with relocated lifetime definitions.
        for descendant in node.iter():
            for key, value in list(descendant.attrib.items()):
                for old, new in lifetime_names.items():
                    value = value.replace(old, new)
                descendant.set(key, value)
        lifetime.append(node)
    # Штатный report monitor не должен считать ещё ищущий запрос потерянным
    # кораблём и снять его потребность до окончания всех порций.
    monitor = next(n for n in graph.iter('do_if')
                   if n.get('value') == "$ActionReportDef.$Type == '$request_commandeerable_freighter' or $ActionReportDef.$Type == '$request_prio_commandeerable_freighter'")
    native_monitor = list(monitor)
    for node in native_monitor:
        monitor.remove(node)
    pending = ET.SubElement(monitor, 'do_if', value="@$ActionReportDef.$TM_SearchCue.exists and not @$ActionReportDef.$TM_SearchCue.$TM_SearchCommitted and not @$ActionReportDef.$Disregard")
    ET.SubElement(pending, 'set_value', name='$DisregardReason', exact="'economic_ship_search_incomplete'")
    normal = ET.SubElement(monitor, 'do_else')
    for node in native_monitor:
        # Exhaustion/cancellation now legitimately precede any Ship field.
        # Let the original monitor retire that report without a missing-field
        # error; do not synthesize a ship or trigger the paid fallback here.
        if node.tag == 'set_value' and node.get('name') == '$CommandeeredShip':
            assert node.get('exact') == '$ActionReportDef.$Ship'
            node.set('exact', '@$ActionReportDef.$Ship')
        normal.append(node)
    # Native callers consume a synchronous result. Accept the search receipt
    # without mistaking its initially absent Ship for failure or buying twice.
    calls = 0
    for parent in list(graph.iter()):
        for signal in list(parent):
            if signal.tag != 'signal_cue_instantly' or signal.get('cue') != 'Request_Commandeerable_Freighter':
                continue
            calls += 1
            param = signal.get('param')
            siblings = list(parent)
            next_node = siblings[siblings.index(signal) + 1]
            if param.startswith('[$TM_ProvisionDef,'):
                parent.insert(list(parent).index(signal), ET.Element('set_value', name='$TM_ProvisionDef.$TM_SearchFallback', exact='true'))
                next_node.set('value', 'not $TM_ProvisionDef.$Ship? and not @$TM_ProvisionDef.$TM_SearchCue.exists')
            elif param.startswith('[$NewActionDef, $Station,'):
                parent.insert(list(parent).index(signal), ET.Element('set_value', name='$NewActionDef.$TM_SearchFallback', exact='true'))
            elif param.startswith('[$NewActionDef, $Sector,'):
                assert next_node.tag == 'do_if' and next_node.get('value') == '$NewActionDef.$Ship?'
                next_node.set('value', '$NewActionDef.$Ship? or @$NewActionDef.$TM_SearchCue.exists')
                for debug in list(next_node):
                    if debug.tag == 'debug_text':
                        position = list(next_node).index(debug)
                        next_node.remove(debug)
                        guarded = ET.Element('do_if', value='$NewActionDef.$Ship?')
                        guarded.append(debug)
                        next_node.insert(position, guarded)
            else:
                raise ValueError('Unadapted synchronous commandeer caller: ' + param)
    # Two native sector callers, the native station caller, and our bounded
    # Upkeep mining/trading provision callers all share the same async boundary.
    assert calls == 5, ('Native commandeer caller closure changed', calls)
    for node in graph.iter('do_if'):
        if node.get('value') == '$TM_ProvisionDef.$Ship? or $TM_ProvisionDef.$TM_PurchaseKey?':
            node.set('value', node.get('value') + ' or @$TM_ProvisionDef.$TM_SearchCue.exists')
        elif node.get('value') == 'not $IsProduction or not $NewActionDef.$Ship?':
            node.set('value', 'not $IsProduction or (not $NewActionDef.$Ship? and not @$NewActionDef.$TM_SearchCue.exists)')
        elif node.get('value') == '$NewActionDef.$Ship? or $NewActionDef.$TM_PurchaseKey?' and node.find("do_if[@value='not $ActionDefinition.$SubActionDefs?']") is not None:
            node.set('value', node.get('value') + ' or @$NewActionDef.$TM_SearchCue.exists')
    # Restore only the two native search->purchase fallbacks after exhaustion.
    decision = next(n for n in completion if n.tag == 'do_if' and n.get('value') == "$Ship.exists and $UseShipReason == 'available'")
    negative = list(completion)[list(completion).index(decision) + 1]
    assert negative.tag == 'do_else'
    fallback = ET.Element('do_if', value="@$ActionDefinition.$TM_SearchFallback and not $Ship.exists and not @$ActionDefinition.$Disregard and $Requester.exists and $Requester.isplayerowned and md.TM_Empire_Runtime.Registry.$State == 'active' and md.TM_Empire_Runtime.Registry.$ManagerCue == $TM_ManagerCue")
    ET.SubElement(fallback, 'set_value', name='$ActionDefinition.$Type', exact="'$request_priority_freighter'")
    ET.SubElement(fallback, 'signal_cue_instantly', cue='Request_Freighter', param='[$ActionDefinition, $Requester, $Ware, true, null]')
    negative.insert(0, fallback)
    # A cancelled factory can lose its pending sub-action before any ship exists.
    # Propagate cancellation by receipt, rather than relying only on ship events.
    for parent in list(graph.iter()):
        for node in list(parent):
            if node.tag == 'set_value' and node.get('name') == '$DisregardObject' and node.get('exact') == 'if $SubActionDef.$Ship then $SubActionDef.$Ship else $SubActionDef.$Station':
                cancelled = ET.Element('do_if', value='@$SubActionDef.$TM_SearchCue.exists')
                ET.SubElement(cancelled, 'set_value', name='$SubActionDef.$Disregard', exact='true')
                parent.insert(list(parent).index(node), cancelled)
                node.set('exact', 'if @$SubActionDef.$Ship then $SubActionDef.$Ship else @$SubActionDef.$Station')


def bound_military_ship_selection(graph):
    if graph.get('name') not in ('TM_Empire_FactionSubgoal_DefendArea', 'TM_Empire_FactionSubgoal_Recon'):
        return
    for parent in list(graph.iter()):
        for node in list(parent):
            if node.tag != 'do_all':
                continue
            exact = node.get('exact')
            if exact == '$PotentialShips.count':
                index = list(parent).index(node)
                clear = ET.Element('do_if', value="@$TM_WaitReason == 'military_ship_sample_incomplete'")
                ET.SubElement(clear, 'remove_value', name='$TM_WaitReason')
                partial = ET.Element('do_if', value='$PotentialShips.count gt 32')
                ET.SubElement(partial, 'set_value', name='$TM_WaitReason', exact="'military_ship_sample_incomplete'")
                parent.insert(index, clear)
                parent.insert(index + 1, partial)
                node.set('exact', '[32, $PotentialShips.count].min')
            elif exact == 'this.$StandbyKeys.count':
                node.set('exact', '[32, this.$StandbyKeys.count].min')
        for node in list(parent):
            if node.tag == 'set_value' and node.get('name') == 'this.$StandbyKeys' and node.get('exact') == '$OwnerStandbyShipsTable.keys.sorted':
                parent.insert(list(parent).index(node) + 1, ET.Element('shuffle_list', list='this.$StandbyKeys'))


@lru_cache(maxsize=1)
def native_catalog_factions():
    # Категории доступны из текущей извлечённой игры, включая её DLC.
    # Это только каталог конструкций; владельцы/отношения/наблюдения не меняются.
    reference = MOD.parent / 'examples/x4_unpacked'
    names = {'player'}
    inputs = []
    paths = sorted({reference / 'libraries/modules.xml', reference / 'libraries/stations.xml'}
                   | set(reference.glob('*/libraries/modules.xml'))
                   | set(reference.glob('*/libraries/stations.xml')))
    for path in paths:
        graph = ET.parse(path).getroot()
        if graph.tag not in ('modules', 'stations', 'diff'):
            continue
        for category in graph.iter('category'):
            value = category.get('faction', '').replace('faction.', '')
            names.update(re.findall(r'\b[a-z][a-z0-9_]*\b', value))
        inputs.append({'path': str(path.relative_to(MOD.parent)), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    names.difference_update({'xenon', 'khaak', 'true', 'false', 'null'})
    return '[' + ', '.join('faction.' + name for name in sorted(names)) + ']', inputs


def native_factory_catalog_faction(owner):
    # create_factory/select and equipment definitions require one faction,
    # unlike get_module_definition's multi-faction catalogue input. Retain
    # the native culture choice without changing the actual player owner.
    return (f'if {owner} != faction.player then {owner} else '
            f'if {owner}.primaryrace == race.boron then faction.boron else '
            f'if {owner}.primaryrace == race.paranid then faction.paranid else '
            f'if {owner}.primaryrace == race.split then faction.split else '
            f'if {owner}.primaryrace == race.teladi then faction.teladi else faction.argon')


def adapt_native_catalog_selection(root):
    catalogue, _ = native_catalog_factions()
    for node in root.iter():
        if node.tag in ('get_module_definition', 'get_construction_plan',
                        'get_ware_definition'):
            if node.get('faction') in ('$Faction', '$Station.owner'):
                node.set('faction', catalogue)
        elif node.tag == 'get_god_production_construction_plan':
            if node.get('faction') in ('$Faction', '$Station.owner'):
                node.set('faction', native_factory_catalog_faction(node.get('faction')))
        elif node.tag == 'create_factory':
            select = node.find('select')
            if select is not None and select.get('faction') == '$Faction':
                select.set('faction', native_factory_catalog_faction('$Faction'))


def isolate_static_defense_protocol(root):
    for node in root.iter():
        for name, value in list(node.attrib.items()):
            if "'StaticDefense_" in value:
                node.set(name, value.replace("'StaticDefense_", "'TM_Empire_StaticDefense_"))
        if node.tag == 'create_order' and node.get('id') == "'DeployStaticDefenseStrategy'":
            node.set('id', "'TM_DeployStaticDefenseStrategy'")


def adapt_static_defense_receipts(root):
    if root.get('name') != 'TM_Empire_FactionLogic_StaticDefense':
        return
    manager = root.find("cues/library[@name='StaticDefenseManager']")
    manager.find('actions').insert(0, ET.Element('set_value', name='$TM_ClaimGoal', exact='namespace'))
    for library in root.iter('library'):
        if library.find("params/param[@name='StaticDefenseManager']") is not None:
            library.find('actions').insert(0, ET.Element('set_value', name='$TM_ClaimGoal', exact='$StaticDefenseManager'))
    for call in root.iter('run_actions'):
        if call.get('ref', '').startswith('md.TM_Empire_Runtime.'):
            param = call.find("param[@name='GoalCue']")
            if param is not None and param.get('value') == 'namespace':
                param.set('value', '$TM_ClaimGoal')
    requested = manager.find("cues/cue[@name='Ship_StrategyRequested']/conditions")
    ET.SubElement(requested, 'check_value', value="event.param2.{1}.exists and event.param2.{1}.isplayerowned and event.param2.{1} != player.controlled and @event.param2.{1}.$tm_empire_claim.$manager == parent.$TM_ManagerCue and @event.param2.{1}.$tm_empire_claim.$goal == parent")
    deployed = manager.find("cues/cue[@name='Ship_StaticDefenseDeployed']")
    conditions = deployed.find('conditions')
    ET.SubElement(conditions, 'check_value', value="event.param2.{1}.exists and event.param2.{1}.isplayerowned and @event.param2.{1}.$tm_empire_claim.$manager == parent.$TM_ManagerCue and @event.param2.{1}.$tm_empire_claim.$goal == parent")
    ET.SubElement(conditions, 'check_value', value="@parent.$StrategyByShipId.{'$' + event.param2.{1}.idcode} == event.param2.{2}")
    ET.SubElement(conditions, 'check_value', value="event.param2.{3}.exists and event.param2.{3}.isplayerowned and event.param2.{3}.sector == event.param2.{2}.$Sector and event.param2.{2}.$MacrosToDeploy.indexof.{event.param2.{3}.macro} and not @event.param2.{2}.$DeployedObjects.indexof.{event.param2.{3}}")
    completed = manager.find("cues/cue[@name='Strategy_Completed']/conditions/check_any")
    signal = completed.find('event_cue_signalled')
    completed.remove(signal)
    internal = ET.SubElement(completed, 'check_all')
    internal.append(signal)
    for gate, payload in [(internal, 'event.param'), (completed.find('check_all'), 'event.param2')]:
        ship, strategy = payload + '.{1}', payload + '.{2}'
        ET.SubElement(gate, 'check_value', value=f"{ship}.exists and {ship}.isplayerowned and @{ship}.$tm_empire_claim.$manager == parent.$TM_ManagerCue and @{ship}.$tm_empire_claim.$goal == parent and @parent.$StrategyByShipId.{{'$' + {ship}.idcode}} == {strategy}")


def copy_static_defense_order():
    source = MOD.parent / 'examples/x4_unpacked/aiscripts/order.deploy.staticdefensestrategy.xml'
    target = MOD / 'native/adapted/aiscripts/tm.order.deploy.staticdefensestrategy.xml'
    graph = ET.parse(source).getroot()
    graph.set('name', 'tm.order.deploystaticdefensestrategy')
    graph.find('order').set('id', 'TM_DeployStaticDefenseStrategy')
    private_actions = {node.get('name'): 'TM_Empire_' + node.get('name')
                       for node in graph.findall('interrupts/library/actions')}
    for node in graph.iter():
        if node.tag == 'actions' and node.get('name') in private_actions:
            node.set('name', private_actions[node.get('name')])
        if node.tag == 'include_interrupt_actions' and node.get('ref') in private_actions:
            node.set('ref', private_actions[node.get('ref')])
    nearby = graph.find(".//find_object[@name='$macro_nearby']")
    assert nearby is not None
    nearby.set('owner', 'faction.player')
    interrupts = graph.find('interrupts')
    revoked = ET.SubElement(interrupts, 'handler', comment='Stop copied child scripts after governor unbind')
    conditions = ET.SubElement(revoked, 'conditions')
    ET.SubElement(conditions, 'event_object_signalled', object='this.assignedcontrolled', param="'TM_Empire_StopOwnedOrder'")
    ET.SubElement(conditions, 'check_value', value='event.param2 == @this.assignedcontrolled.$tm_empire_claim.$manager')
    ET.SubElement(ET.SubElement(revoked, 'actions'), 'abort_called_scripts', resume='finish')
    helm = ET.SubElement(interrupts, 'handler', comment='Release the private order when the player takes the helm')
    conditions = ET.SubElement(helm, 'conditions')
    ET.SubElement(conditions, 'event_player_started_control')
    ET.SubElement(conditions, 'check_value', value='event.param == this.assignedcontrolled')
    ET.SubElement(ET.SubElement(helm, 'actions'), 'abort_called_scripts', resume='finish')
    owner = ET.SubElement(interrupts, 'handler', comment='Release private deployment after ownership changes')
    conditions = ET.SubElement(owner, 'conditions')
    changes = ET.SubElement(conditions, 'check_any')
    ET.SubElement(changes, 'event_object_changed_owner', object='this.assignedcontrolled')
    ET.SubElement(changes, 'event_object_changed_true_owner', object='this.assignedcontrolled')
    ET.SubElement(ET.SubElement(owner, 'actions'), 'abort_called_scripts', resume='finish')
    allowed = ("this.assignedcontrolled.isplayerowned and this.assignedcontrolled != player.controlled "
               "and @this.assignedcontrolled.$tm_empire_claim.$manager.exists "
               "and @this.assignedcontrolled.$tm_empire_claim.$goal.exists "
               "and @md.TM_Empire_Runtime.Registry.$State == 'active' "
               "and @this.assignedcontrolled.$tm_empire_claim.$manager == @md.TM_Empire_Runtime.Registry.$ManagerCue "
               "and @this.assignedcontrolled.$tm_empire_claim.$state != 'unknown'")
    allowed += ' and not @this.assignedcontrolled.$tm_empire_claim.$stoprequested'
    for parent in list(graph.find('attention').iter()):
        for node in list(parent):
            if node.tag not in ('run_script', 'signal_objects'):
                continue
            index = list(parent).index(node)
            gate = ET.Element('do_if', value='not (' + allowed + ')')
            ET.SubElement(gate, 'resume', label='finish')
            parent.insert(index, gate)
    isolate_static_defense_protocol(graph)
    normalize_tree(graph)
    ET.indent(graph, space='  ')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(ET.tostring(graph, encoding='utf-8', xml_declaration=True))
    return {'source': source.relative_to(MOD.parent).as_posix(),
            'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'path': target.relative_to(MOD).as_posix(),
            'sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
            'qualification': 'private_protocol_only_not_runtime', 'installed': False}


def copy_station_reassignment_order():
    source = MOD.parent / 'examples/x4_unpacked/aiscripts/order.assign.commander.xml'
    target = MOD / 'native/adapted/aiscripts/tm.order.assign.commander.xml'
    graph = ET.parse(source).getroot()
    graph.set('name', 'tm.order.assigncommander')
    graph.find('order').set('id', 'TM_AssignCommander')
    graph.find("order/params/param[@name='cancelorders']").set('default', 'false')
    for parent in list(graph.iter()):
        for node in list(parent):
            if node.tag in ('patch', 'cancel_all_orders'):
                parent.remove(node)
    allowed = ("this.assignedcontrolled.isplayerowned and this.assignedcontrolled != player.controlled "
               "and not this.assignedcontrolled.hasorderloop and not @this.assignedcontrolled.order.isoverride "
               "and not @this.assignedcontrolled.order.haspriority "
               "and not @this.assignedcontrolled.$tm_empire_claim "
               "and @this.assignedcontrolled.$tm_empire_station_reassignment.$state == 'sent' "
               "and @this.assignedcontrolled.$tm_empire_station_reassignment.$order == this.assignedcontrolled.order "
               "and @this.assignedcontrolled.$tm_empire_station_reassignment.$goal.exists "
               "and not @this.assignedcontrolled.$tm_empire_station_reassignment.$goal.$tm_empire_cancelled "
               "and @md.TM_Empire_Runtime.Registry.$State == 'active' "
               "and @md.TM_Empire_Runtime.Registry.$ManagerCue == @this.assignedcontrolled.$tm_empire_station_reassignment.$manager "
               "and (this.assignedcontrolled.commander == @this.assignedcontrolled.$tm_empire_station_reassignment.$source "
               "or this.assignedcontrolled.commander == $commander) "
               "and $commander.exists and $commander.isplayerowned and $commander.isoperational "
               "and $commander == @this.assignedcontrolled.$tm_empire_station_reassignment.$target")
    actions = graph.find('attention/actions')
    for parent in list(actions.iter()):
        for node in list(parent):
            if node.tag not in ('run_script', 'set_object_commander', 'remove_object_commander', 'create_order', 'set_subordinate_group_assignment', 'remove_ware_reservation'):
                continue
            gate = ET.Element('do_if', value='not (' + allowed + ')')
            ET.SubElement(gate, 'return', value='false')
            parent.insert(list(parent).index(node), gate)
    normalize_tree(graph)
    ET.indent(graph, space='  ')
    target.write_bytes(ET.tostring(graph, encoding='utf-8', xml_declaration=True))
    return {'source': source.relative_to(MOD.parent).as_posix(), 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'path': target.relative_to(MOD).as_posix(), 'sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
            'qualification': 'guarded_station_reassignment_unqualified', 'installed': False}


def owned_call(ref, ship, result='$TM_ShipReason'):
    call = ET.Element('run_actions', ref='md.TM_Empire_Runtime.' + ref, result=result)
    ET.SubElement(call, 'param', name='Ship', value=ship)
    ET.SubElement(call, 'param', name='GoalCue', value='namespace')
    if ref in ('CanUseOwnedShip', 'ClaimOwnedShip', 'TransferOwnedClaim'):
        ET.SubElement(call, 'param', name='ManagerCue', value='@$TM_ManagerCue')
    return call


def copy_satellite_deployment_order():
    source = MOD.parent / 'examples/x4_unpacked/aiscripts/order.deployobjectatposition.xml'
    target = MOD / 'native/adapted/aiscripts/tm.order.deployobjectatposition.xml'
    graph = ET.parse(source).getroot()
    graph.set('name', 'tm.order.deployobjectatposition')
    graph.find('order').set('id', 'TM_DeployObjectAtPosition')
    guarded = ET.parse(MOD / 'native/adapted/aiscripts/tm.order.deploy.staticdefensestrategy.xml').getroot()
    for handler in list(guarded.find('interrupts'))[-3:]:
        graph.find('interrupts').append(copy.deepcopy(handler))
    template = next(node for node in guarded.find('attention').iter('do_if') if node.get('value', '').startswith('not (this.assignedcontrolled.isplayerowned'))
    for parent in list(graph.find('attention').iter()):
        for node in list(parent):
            if node.tag == 'run_script' or node.tag.startswith('launch_'):
                index = list(parent).index(node)
                parent.insert(index, copy.deepcopy(template))
            if node.tag == 'launch_satellite':
                index = list(parent).index(node)
                node.set('name', '$TM_DeployedSatellite')
                parent.insert(index, ET.Element('set_value', name='this.assignedcontrolled.$tm_empire_satellite_receipt', exact="table[$state='deployment_sent', $manager=this.assignedcontrolled.$tm_empire_claim.$manager, $goal=this.assignedcontrolled.$tm_empire_claim.$goal, $order=$thisorder, $macro=$macro, $before=this.assignedcontrolled.ammostorage.{$macro}.count, $issued=player.age]"))
                observed = ET.Element('do_if', value='$TM_DeployedSatellite.exists and $TM_DeployedSatellite.isplayerowned and $TM_DeployedSatellite.macro == $macro and this.assignedcontrolled.ammostorage.{$macro}.count == this.assignedcontrolled.$tm_empire_satellite_receipt.$before - 1')
                ET.SubElement(observed, 'set_value', name='this.assignedcontrolled.$tm_empire_satellite_receipt.$state', exact="'observed'")
                ET.SubElement(observed, 'set_value', name='this.assignedcontrolled.$tm_empire_satellite_receipt.$satellite', exact='$TM_DeployedSatellite')
                parent.insert(list(parent).index(node) + 1, observed)
    normalize_tree(graph)
    ET.indent(graph, space='  ')
    target.write_bytes(ET.tostring(graph, encoding='utf-8', xml_declaration=True))
    return {'source': source.relative_to(MOD.parent).as_posix(), 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'path': target.relative_to(MOD).as_posix(), 'sha256': hashlib.sha256(target.read_bytes()).hexdigest(), 'qualification': 'native_inventory_deployment_unqualified', 'installed': False}


def adapt_economy_prefab_expansion(root):
    if root.get('name') != 'TM_Empire_FactionLogic_Economy':
        return
    request = root.find(".//cue[@name='Request_Production_Module']")
    direct = request.find('.//add_build_to_expand_station')
    if direct is None:
        return
    parents = {child: parent for parent in request.iter() for child in parent}
    branch = parents[direct]
    index = list(branch).index(direct)
    success = list(branch)[index + 1]
    failure = list(branch)[index + 2]
    assert success.tag == 'do_if' and success.get('value') == '$ResultBuild' and failure.tag == 'do_else'
    for node in (direct, success, failure):
        branch.remove(node)
    ET.SubElement(branch, 'set_value', name='$TM_PrefabWaiting', exact='true')
    ET.SubElement(branch, 'set_value', name='$ActionDefinition.$RequestGoal', exact='namespace')
    ET.SubElement(branch, 'set_value', name='$ActionDefinition.$Station', exact='$Station')
    ET.SubElement(branch, 'set_value', name='$ActionDefinition.$TM_ConstructionState', exact="'validating'")
    tick = ET.SubElement(request.find('cues'), 'cue', name='TM_ProductionPrefabTick', checkinterval='15s')
    ET.SubElement(ET.SubElement(tick, 'conditions'), 'check_value', value='@$TM_PrefabWaiting')
    ET.SubElement(tick, 'delay', exact='15s')
    actions = ET.SubElement(tick, 'actions')
    call = ET.SubElement(actions, 'run_actions', ref='md.TM_Empire_Construction.StepPrefabExpansion', result='this.$Result')
    for name, value in [('ManagerCue', '$TM_ManagerCue'), ('GoalCue', 'namespace'), ('Station', '$Station'), ('Sequence', '$ConstructionPlan.finalsequence'), ('Stage', '$ExpandingPrefabStage'), ('Budget', 'player.money')]:
        ET.SubElement(call, 'param', name=name, value=value)
    ET.SubElement(actions, 'set_value', name='$ActionDefinition.$TM_ConstructionState', exact='this.$Result.$state')
    ET.SubElement(actions, 'set_value', name='$ActionDefinition.$TM_ConstructionReason', exact='@this.$Result.$reason')
    queued = ET.SubElement(actions, 'do_if', value="this.$Result.$state == 'queued' and @this.$Result.$build.exists")
    ET.SubElement(queued, 'set_value', name='$ResultBuild', exact='this.$Result.$build')
    queued.extend(list(success))
    ET.SubElement(queued, 'set_value', name='$TM_PrefabWaiting', exact='false')
    repeat = ET.SubElement(actions, 'do_else')
    ET.SubElement(repeat, 'reset_cue', cue='this')


def adapt_goal_cancellation(root):
    """Отозвать ещё не исполненные разрешения до удаления дерева цели."""
    for parent_node in list(root.iter()):
        for node in list(parent_node):
            if node.tag != 'cancel_cue':
                continue
            call = ET.Element('run_actions', ref='md.TM_Empire_Runtime.RevokeGoalApprovals')
            ET.SubElement(call, 'param', name='CancelledCue', value=node.get('cue'))
            parent_node.insert(list(parent_node).index(node), call)


def adapt_owned_ship_boundaries(root):
    counts = {'candidate_filters': 0, 'effect_guards': 0, 'manager_contexts': 0, 'visible_searches': 0}
    for node in root.iter():
        if node.tag not in ('find_ship', 'find_ship_by_true_owner', 'find_station', 'find_station_by_true_owner'):
            continue
        node.set('known', 'true')
        owner = node.get('faction') or node.get('owner')
        own_distress_pool = (root.get('name') == 'TM_Empire_FactionGoal_PatrolCoordinationService'
                             and node.get('name') == 'this.$OurSectorShips'
                             and owner == 'this.$AttackedOwner')
        if node.tag in ('find_ship', 'find_ship_by_true_owner') and owner not in ('$Faction', 'faction.player') and not own_distress_pool:
            # Use actual current positions only for ships in player live view.
            # Our own asset pool remains empire-wide, including remote ships.
            node.set('isinliveview', 'true')
        counts['visible_searches'] += 1
    # No NPC save version is inherited by the isolated player closure.
    for parent in list(root.iter()):
        for node in list(parent):
            if node.tag == 'patch':
                parent.remove(node)
            elif node.tag == 'set_value' and node.get('name') in ('$FactionCue', '$OwnerGoal'):
                source = '$FactionCue' if node.get('name') == '$FactionCue' else '@$OwnerGoal.$TM_ManagerCue'
                parent.insert(list(parent).index(node) + 1, ET.Element('set_value', name='$TM_ManagerCue', exact=source))
                counts['manager_contexts'] += 1
    for library in root.iter('library'):
        params, actions = library.find('params'), library.find('actions')
        if params is not None and params.find("param[@name='FactionManagerCue']") is not None:
            if actions is None:
                actions = ET.Element('actions')
                children = list(library)
                index = next((i for i, child in enumerate(children) if child.tag == 'cues'), len(children))
                library.insert(index, actions)
            actions.insert(0, ET.Element('set_value', name='$TM_ManagerCue', exact='$FactionManagerCue'))
            counts['manager_contexts'] += 1
    manager = root.find("cues/library[@name='Manager']")
    if manager is not None and root.get('name') == 'TM_Empire_FactionLogic':
        manager.find('actions').insert(0, ET.Element('set_value', name='$TM_ManagerCue', exact='namespace'))
        counts['manager_contexts'] += 1
    # Candidate pools lose NPC job membership, retaining native role/range/class
    # and capability filters. Hostile observations are not turned into own ships.
    pools = set()
    for search in root.iter('find_ship_by_true_owner'):
        if search.get('faction') not in ('$Faction', 'faction.player'):
            continue
        if not ({'commandeerable', 'requestedjobship', 'jobtags'} & search.attrib.keys()
                or any('jobtags' in node.attrib for node in search.iter())):
            continue
        pools.add(search.get('name'))
        tags = ' '.join(node.get('jobtags', '') for node in search.iter())
        if 'tag.scout' in tags or 'tag.envoy' in tags:
            # Native scout ship type replaces NPC scout/envoy job membership.
            # The existing second pass still considers small/medium fighters.
            search.set('shiptype', 'shiptype.scout')
        elif 'tag.military' in tags:
            search.set('primarypurpose', 'purpose.fight')
        for key in ('commandeerable', 'requestedjobship', 'jobtags'):
            search.attrib.pop(key, None)
        search.attrib.pop('subordinatejobship', None)
        for parent in list(search.iter()):
            for node in list(parent):
                if node.tag == 'match' and 'jobtags' in node.attrib:
                    node.attrib.pop('jobtags')
                    if not node.attrib and not list(node): parent.remove(node)
        for parent in list(search.iter()):
            for node in list(parent):
                if node.tag in ('match_any', 'match_all') and not list(node): parent.remove(node)
        counts['candidate_filters'] += 1
    for loop in list(root.iter()):
        if loop.tag not in ('do_all', 'do_for_each'):
            continue
        for node in list(loop):
            if node.tag == 'set_value' and any((node.get('exact') or '').startswith(pool + '.{') for pool in pools if pool):
                ship = node.get('name')
                index = list(loop).index(node) + 1
                # Native commandeerable filtering also excluded ships already
                # counted by this goal. Our lease permits updating their orders,
                # so exclude membership here at the acquisition seam instead.
                if any(item.get('groupname') == '$Ships' and item.get('object') == ship
                       for item in loop.iter('add_to_group')):
                    assigned = ET.Element('do_if', value='$Ships.indexof.{' + ship + '}')
                    ET.SubElement(assigned, 'continue')
                    loop.insert(index, assigned)
                    index += 1
                loop.insert(index, owned_call('CanUseOwnedShip', ship))
                skip = ET.Element('do_if', value="$TM_ShipReason != 'available'")
                ET.SubElement(skip, 'continue')
                loop.insert(index + 1, skip)
    # Native standby tables define the explicit handoff seam. Transfer only
    # claims belonging to this same manager; keep the native order handles.
    for cue in root.iter('cue'):
        if cue.get('name') == 'Add_Standby_Ship':
            actions = cue.find('actions')
            for gate in list(actions):
                if gate.tag == 'do_if' and 'this.$Ship.isclass.ship' in gate.get('value', ''):
                    call = owned_call('TransferOwnedClaim', 'this.$Ship')
                    ET.SubElement(call, 'param', name='FromGoalCue', value='@this.$Ship.$tm_empire_claim.$goal')
                    original = list(gate)
                    gate.clear()
                    gate.set('value', 'typeof this.$Ship == datatype.component and this.$Ship.isclass.ship')
                    gate.append(call)
                    accepted = ET.SubElement(gate, 'do_if', value="$TM_ShipReason == 'available'")
                    accepted.extend(original)
                    refused = ET.SubElement(gate, 'do_else')
                    ET.SubElement(refused, 'set_value', name='event.param.{3}.{1}', exact='false')
                    ET.SubElement(refused, 'set_value', name='$TM_WaitReason', exact='$TM_ShipReason')
    for loop in list(root.iter('do_all')):
        for node in list(loop):
            if node.tag == 'set_value' and node.get('name') == 'this.$StandbyShip':
                call = owned_call('CanUseOwnedShip', 'this.$StandbyShip')
                call.find("param[@name='GoalCue']").set('value', '$OwnerGoal')
                index = list(loop).index(node) + 1
                loop.insert(index, call)
                blocked = ET.Element('do_if', value="$TM_ShipReason != 'available'")
                ET.SubElement(blocked, 'set_value', name='$TM_WaitReason', exact='$TM_ShipReason')
                ET.SubElement(blocked, 'continue')
                loop.insert(index + 1, blocked)
    for parent in list(root.iter()):
        for signal in list(parent):
            if signal.tag == 'signal_cue_instantly' and signal.get('param') == "['remove_standby_ship', this.$StandbyShip, false]":
                index = list(parent).index(signal)
                remainder = list(parent)[index:]
                for item in remainder: parent.remove(item)
                call = owned_call('TransferOwnedClaim', 'this.$StandbyShip')
                ET.SubElement(call, 'param', name='FromGoalCue', value='$OwnerGoal')
                parent.append(call)
                accepted = ET.SubElement(parent, 'do_if', value="$TM_ShipReason == 'available'")
                accepted.extend(remainder)
                refused = ET.SubElement(parent, 'do_else')
                ET.SubElement(refused, 'set_value', name='$TM_WaitReason', exact='$TM_ShipReason')
    # Reserve before changing native groups/counts/force totals. A failed
    # claim must not let the original tail report an assigned reinforcement.
    for parent in list(root.iter()):
        for claim in list(parent):
            if claim.tag != 'commandeer_object': continue
            ship = claim.get('object')
            children = list(parent)
            index = children.index(claim)
            start = index
            while start:
                previous = children[start - 1]
                if previous.tag == 'add_to_group' and previous.get('object') == ship:
                    start -= 1
                elif previous.tag == 'set_value' and previous.get('operation') == 'add':
                    start -= 1
                elif previous.tag == 'set_value' and previous.get('name') in ('$ActionDefinition.$Ship', '$ActionDefinition.$CommandeerTime'):
                    start -= 1
                else: break
            tail = children[start:]
            for item in tail: parent.remove(item)
            parent.append(owned_call('ClaimOwnedShip', ship))
            granted = ET.SubElement(parent, 'do_if', value="$TM_ShipReason == 'available'")
            granted.extend(item for item in tail if item is not claim)
            blocked = ET.SubElement(parent, 'do_else')
            ET.SubElement(blocked, 'set_value', name='$TM_WaitReason', exact='$TM_ShipReason')
            counts['effect_guards'] += 1
    # Guard the actual native effect, not just the earlier selection.
    for parent in list(root.iter()):
        for node in list(parent):
            tag, ship = node.tag, node.get('object')
            if tag not in ('commandeer_object', 'create_order', 'set_object_commander', 'remove_object_commander', 'release_commandeered_object'):
                continue
            if not ship: continue
            index = list(parent).index(node)
            parent.remove(node)
            counts['effect_guards'] += 1
            if tag == 'remove_object_commander':
                parent.insert(index, ET.Element('set_value', name='$TM_WaitReason', exact="'commander_cleanup_preserved'"))
                continue
            if tag == 'release_commandeered_object':
                parent.insert(index, owned_call('ReleaseOwnedClaim', ship))
                continue
            if tag == 'commandeer_object':
                parent.insert(index, owned_call('ClaimOwnedShip', ship))
                continue
            parent.insert(index, owned_call('CanUseOwnedShip', ship))
            gate = ET.Element('do_if', value="$TM_ShipReason == 'available'")
            parent.insert(index + 1, gate)
            if tag == 'set_object_commander' and node.get('commander'):
                commander = node.get('commander')
                gate.set('value', f"$TM_ShipReason == 'available' and (not {commander}.exists or {commander}.isplayerowned)")
            if tag == 'create_order' and node.get('id') == "'AssignCommander'":
                destination = node.find("param[@name='commander']")
                if destination is not None:
                    commander = destination.get('value')
                    gate.set('value', f"$TM_ShipReason == 'available' and {commander}.exists and {commander}.isplayerowned")
            gate.append(owned_call('ClaimOwnedShip', ship))
            granted = ET.SubElement(gate, 'do_if', value="$TM_ShipReason == 'available'")
            if tag == 'create_order':
                handle = node.get('name') or f'$TM_GuardedOrder_{counts["effect_guards"]}'
                node.set('name', handle)
                ET.SubElement(granted, 'set_value', name=ship + '.$tm_empire_claim.$issuing', exact='true')
                granted.append(node)
                record = owned_call('RecordOwnedOrder', ship, '$TM_OrderReceipt')
                ET.SubElement(record, 'param', name='Order', value=handle)
                if node.get('id') == "'AssignCommander'":
                    commander_param = node.find("param[@name='commander']")
                    if commander_param is not None:
                        ET.SubElement(record, 'param', name='ExpectedCommander', value=commander_param.get('value'))
                granted.append(record)
                # Replace the previous economy-specific capture with the shared
                # receipt; otherwise the same order would be appended twice.
                siblings = list(parent)
                following = siblings[siblings.index(gate) + 1:]
                if handle.startswith('$TM_Order_') and len(following) >= 2 and following[0].tag == 'do_if' and following[1].tag == 'do_else':
                    if following[0].get('value') == f'{handle}.exists and {handle}.object == $Ship':
                        parent.remove(following[0]); parent.remove(following[1])
            else:
                commander = node.get('commander')
                granted.append(node)
                confirmed = ET.SubElement(granted, 'do_if', value=f'{ship}.commander == {commander}')
                ET.SubElement(confirmed, 'set_value', name=ship + '.$tm_empire_claim.$commander', exact='@' + ship + '.commander')
                unknown = ET.SubElement(granted, 'do_else')
                ET.SubElement(unknown, 'set_value', name=ship + '.$tm_empire_claim.$state', exact="'unknown'")
                ET.SubElement(unknown, 'set_value', name='$TM_WaitReason', exact="'assignment_unconfirmed'")
            claim_failed = ET.SubElement(gate, 'do_else')
            ET.SubElement(claim_failed, 'set_value', name='$TM_WaitReason', exact='$TM_ShipReason')
            if tag == 'create_order': ET.SubElement(claim_failed, 'set_value', name=node.get('name'), exact='null')
            blocked = ET.Element('do_else')
            reason = "if $TM_ShipReason == 'available' then 'commander_not_owned' else $TM_ShipReason" if tag == 'set_object_commander' else '$TM_ShipReason'
            ET.SubElement(blocked, 'set_value', name='$TM_WaitReason', exact=reason)
            if tag == 'create_order': ET.SubElement(blocked, 'set_value', name=node.get('name'), exact='null')
            parent.insert(list(parent).index(gate) + 1, blocked)
    return counts


def adapt_goal_purchase(root):
    if root.get('name') not in ('TM_Empire_FactionSubgoal_Recon', 'TM_Empire_FactionSubgoal_DefendArea'):
        return
    request = root.find(".//cue[@name='Request_Job_Ship']")
    assert request is not None
    for parent in list(root.iter()):
        for node in list(parent):
            if node.tag == 'signal_cue_instantly' and node.get('cue') in ('md.TM_Empire_FactionLogic.Get_Scout_Jobs', 'md.TM_Empire_FactionLogic.Get_Military_Jobs'):
                # Do not repeat expensive native availability analysis while
                # the single purchase is pending or its backoff is active.
                assert parent.tag == 'do_if'
                parent.set('value', '(' + parent.get('value') + ") and not @md.TM_Empire_Purchase.Request.$Pending and player.age ge @md.TM_Empire_Purchase.Request.$NextAttempt and (@md.TM_Empire_Purchase.Request.$LastResult.$state != 'delivered' or @md.TM_Empire_Purchase.Request.$LastResult.$accepted)")
            if node.tag == 'signal_cue_instantly' and node.get('cue') == 'Request_Job_Ship' and parent.tag == 'do_all':
                stop = ET.Element('do_if', value='@md.TM_Empire_Purchase.Request.$Pending')
                ET.SubElement(stop, 'break')
                parent.insert(list(parent).index(node) + 1, stop)
    request.set('version', '1')
    for child in list(request):
        if child.tag != 'conditions': request.remove(child)
    actions = ET.SubElement(request, 'actions')
    ET.SubElement(actions, 'set_value', name='this.$Option', exact='event.param.{1}')
    gate = ET.SubElement(actions, 'do_if', value='typeof this.$Option == datatype.table')
    call = ET.SubElement(gate, 'run_actions', ref='md.TM_Empire_Purchase.PreparePurchase', result='this.$PurchaseState')
    for name, value in (('ManagerCue', '$TM_ManagerCue'), ('GoalCue', 'namespace'),
                        ('Shipyard', 'this.$Option.$shipyard'), ('Macro', 'this.$Option.$macro'), ('Budget', 'player.money')):
        ET.SubElement(call, 'param', name=name, value=value)
    accepted = ET.SubElement(gate, 'do_if', value="this.$PurchaseState == 'quote_requested'")
    ET.SubElement(accepted, 'set_value', name='this.$PurchaseKey', exact='md.TM_Empire_Purchase.Request.$Pending.$key')
    rejected = ET.SubElement(gate, 'do_else')
    ET.SubElement(rejected, 'set_value', name='$TM_WaitReason', exact='this.$PurchaseState')
    ET.SubElement(rejected, 'cancel_cue', cue='this')
    invalid = ET.SubElement(actions, 'do_else')
    ET.SubElement(invalid, 'set_value', name='$TM_WaitReason', exact="'invalid_purchase_option'")
    ET.SubElement(invalid, 'cancel_cue', cue='this')
    children = ET.SubElement(request, 'cues')
    poll = ET.SubElement(children, 'cue', name='PurchasedShipObserved', checkinterval='15s')
    conditions = ET.SubElement(poll, 'conditions')
    ET.SubElement(conditions, 'check_value', value='parent.$PurchaseKey?')
    ET.SubElement(poll, 'delay', exact='15s')
    actions = ET.SubElement(poll, 'actions')
    active = ET.SubElement(actions, 'do_if', value='@md.TM_Empire_Purchase.Request.$Pending.$key == parent.$PurchaseKey and (md.TM_Empire_Purchase.Tracked.$Build? or @md.TM_Empire_Purchase.Request.$Pending.$state == \'ready\')')
    ET.SubElement(active, 'run_actions', ref='md.TM_Empire_Purchase.CompletePurchase', result='this.$Progress')
    result = ET.SubElement(actions, 'do_if', value='@md.TM_Empire_Purchase.Request.$LastResult.$key == parent.$PurchaseKey')
    ready = ET.SubElement(result, 'do_if', value="md.TM_Empire_Purchase.Request.$LastResult.$state == 'delivered'")
    ET.SubElement(ready, 'set_value', name='this.$Ship', exact='md.TM_Empire_Purchase.Request.$LastResult.$ship')
    new_ship = ET.SubElement(ready, 'do_if', value='not $Ships.indexof.{this.$Ship}')
    ET.SubElement(new_ship, 'add_to_group', groupname='$Ships', object='this.$Ship')
    strength = ET.SubElement(new_ship, 'run_actions', ref='md.TM_Empire_FactionLogic.EvaluateForceStrengthLib', result='$EFS_Result')
    ET.SubElement(strength, 'param', name='Ships', value='this.$Ship')
    ET.SubElement(strength, 'param', name='ResultTable', value='$StrengthTable')
    for name in ('$ForceStrength', '$RegistryTable.$ShipStrength'):
        ET.SubElement(new_ship, 'set_value', name=name, operation='add', exact='$EFS_Result')
    ET.SubElement(new_ship, 'signal_cue_instantly', cue='Set_Ship_Order', param='this.$Ship')
    acknowledgement = ET.SubElement(ready, 'run_actions', ref='md.TM_Empire_Purchase.AcknowledgeDelivery', result='$TM_DeliveryReceipt')
    for name, value in (('Key', 'parent.$PurchaseKey'), ('GoalCue', 'namespace'), ('Ship', 'this.$Ship')):
        ET.SubElement(acknowledgement, 'param', name=name, value=value)
    waiting = ET.SubElement(result, 'do_else')
    ET.SubElement(waiting, 'set_value', name='$TM_WaitReason', exact='md.TM_Empire_Purchase.Request.$LastResult.$reason')
    ET.SubElement(result, 'cancel_cue', cue='parent')
    again = ET.SubElement(actions, 'do_else')
    ET.SubElement(again, 'set_value', name='$TM_WaitReason', exact="'purchase_pending_native_receipt'")
    ET.SubElement(again, 'reset_cue', cue='this')


def adapt_static_purchase(root):
    if root.get('name') != 'TM_Empire_FactionLogic_StaticDefense': return
    library = root.find("cues/library[@name='CreateJobShips']")
    actions = library.find('actions')
    # Preserve the original M/S count observation, replace only replenishment.
    for child in list(actions)[3:]: actions.remove(child)
    ET.SubElement(actions, 'do_if', value='@md.TM_Empire_Purchase.Request.$Pending').append(ET.Element('return', value="'purchase_pending'"))
    ET.SubElement(actions, 'do_if', value="@md.TM_Empire_Purchase.Request.$LastResult.$state == 'delivered' and not @md.TM_Empire_Purchase.Request.$LastResult.$accepted").append(ET.Element('return', value="'previous_delivery_not_consumed'"))
    ET.SubElement(actions, 'set_value', name='$Classes', exact='null')
    m = ET.SubElement(actions, 'do_if', value='$ShipMs.count lt 3')
    ET.SubElement(m, 'set_value', name='$Classes', exact='class.ship_m')
    s = ET.SubElement(actions, 'do_elseif', value='$ShipSs.count lt 2')
    ET.SubElement(s, 'set_value', name='$Classes', exact='class.ship_s')
    done = ET.SubElement(actions, 'do_else')
    ET.SubElement(done, 'return', value="'native_engineer_quota_satisfied'")
    def options(parent, classes):
        call = ET.SubElement(parent, 'run_actions', ref='md.TM_Empire_Purchase.ReadPurchaseOptions', result='$Options')
        ET.SubElement(call, 'param', name='Tags', value='[tag.military]')
        ET.SubElement(call, 'param', name='Classes', value=classes)
    options(actions, '$Classes')
    fallback = ET.SubElement(actions, 'do_if', value='$Classes == class.ship_m and not $Options.count')
    options(fallback, 'class.ship_s')
    unavailable = ET.SubElement(actions, 'do_if', value='not $Options.count')
    ET.SubElement(unavailable, 'return', value="'no_accessible_engineer_ship'")
    ET.SubElement(actions, 'set_value', name='$Option', exact='$Options.random')
    call = ET.SubElement(actions, 'run_actions', ref='md.TM_Empire_Purchase.PreparePurchase', result='$State')
    for name, value in (('ManagerCue', '$StaticDefenseManager.$TM_ManagerCue'), ('GoalCue', '$StaticDefenseManager'), ('Shipyard', '$Option.$shipyard'), ('Macro', '$Option.$macro'), ('Budget', 'player.money')):
        ET.SubElement(call, 'param', name=name, value=value)
    ET.SubElement(actions, 'return', value='$State')
    manager = root.find("cues/library[@name='StaticDefenseManager']")
    watch = ET.SubElement(manager.find('cues'), 'cue', name='PurchasedEngineerObserved', checkinterval='15s')
    conditions = ET.SubElement(watch, 'conditions')
    ET.SubElement(conditions, 'check_value', value='@md.TM_Empire_Purchase.Request.$Pending.$goal == namespace or @md.TM_Empire_Purchase.Request.$LastResult.$goal == namespace')
    ET.SubElement(watch, 'delay', exact='15s')
    actions = ET.SubElement(watch, 'actions')
    pending = ET.SubElement(actions, 'do_if', value='@md.TM_Empire_Purchase.Request.$Pending.$goal == namespace and (md.TM_Empire_Purchase.Tracked.$Build? or @md.TM_Empire_Purchase.Request.$Pending.$state == \'ready\')')
    ET.SubElement(pending, 'run_actions', ref='md.TM_Empire_Purchase.CompletePurchase', result='$TM_PurchaseProgress')
    received = ET.SubElement(actions, 'do_if', value="@md.TM_Empire_Purchase.Request.$LastResult.$goal == namespace and md.TM_Empire_Purchase.Request.$LastResult.$state == 'delivered' and @$TM_LastEngineerKey != md.TM_Empire_Purchase.Request.$LastResult.$key")
    ET.SubElement(received, 'set_value', name='$TM_Engineer', exact='md.TM_Empire_Purchase.Request.$LastResult.$ship')
    dispatch = ET.SubElement(received, 'do_if', value='@$TM_EngineerOrderKey != md.TM_Empire_Purchase.Request.$LastResult.$key')
    ET.SubElement(dispatch, 'set_value', name='$TM_OrderReceipt', exact="'not_sent'")
    order = ET.SubElement(dispatch, 'create_order', name='$TM_EngineerOrder', object='$TM_Engineer', id="'DeployStaticDefenseStrategy'", immediate='true')
    ET.SubElement(order, 'param', name='isminesonly', value='$TM_Engineer.isclass.ship_s')
    confirmed = ET.SubElement(dispatch, 'do_if', value="$TM_OrderReceipt == 'sent'")
    ET.SubElement(confirmed, 'set_value', name='$TM_EngineerOrderKey', exact='md.TM_Empire_Purchase.Request.$LastResult.$key')
    ET.SubElement(confirmed, 'add_to_group', groupname='$CombatEngineersAndSaboteurs', object='$TM_Engineer')
    handed = ET.SubElement(received, 'do_if', value='@$TM_EngineerOrderKey == md.TM_Empire_Purchase.Request.$LastResult.$key')
    acknowledgement = ET.SubElement(handed, 'run_actions', ref='md.TM_Empire_Purchase.AcknowledgeDelivery', result='$TM_DeliveryReceipt')
    for name, value in (('Key', '$TM_EngineerOrderKey'), ('GoalCue', 'namespace'), ('Ship', '$TM_Engineer')):
        ET.SubElement(acknowledgement, 'param', name=name, value=value)
    accepted = ET.SubElement(handed, 'do_if', value="$TM_DeliveryReceipt == 'accepted'")
    ET.SubElement(accepted, 'set_value', name='$TM_LastEngineerKey', exact='$TM_EngineerOrderKey')
    unacknowledged = ET.SubElement(handed, 'do_else')
    ET.SubElement(unacknowledged, 'set_value', name='$TM_WaitReason', exact='$TM_DeliveryReceipt')
    ET.SubElement(actions, 'reset_cue', cue='this')


def adapt_economy_purchase(root):
    if root.get('name') != 'TM_Empire_FactionLogic_Economy': return
    request = root.find(".//cue[@name='Request_Freighter']")
    native_built = copy.deepcopy(request.find("cues/cue[@name='Request_Freighter_Built']/actions"))
    step_receipts = {}
    for parent in list(native_built.iter()):
        for order in list(parent):
            if order.tag != 'create_order': continue
            if order.get('id') == "'AssignCommander'" and order.find("param[@name='commander']") is None: continue
            step = '$TM_PurchaseStep_' + str(len(step_receipts) + 1)
            step_receipts[order.get('id')] = step
            handle = '$TM_PurchaseHandle_' + str(len(step_receipts))
            order.set('name', handle)
            index = list(parent).index(order)
            parent.remove(order)
            once = ET.Element('do_if', value='not ' + step + '?')
            parent.insert(index, once)
            ET.SubElement(once, 'set_value', name='$TM_OrderReceipt', exact="'not_sent'")
            once.append(order)
            observed = ET.SubElement(once, 'do_if', value="$TM_OrderReceipt != 'not_sent'")
            ET.SubElement(observed, 'set_value', name=step, exact='$TM_OrderReceipt')
    original = list(request.find('actions'))[:6]
    for child in list(request):
        if child.tag != 'conditions': request.remove(child)
    request.set('version', '1')
    actions = ET.SubElement(request, 'actions')
    actions.extend(original)
    ET.SubElement(actions, 'set_value', name='$TM_ManagerCue', exact='parent.$FactionManagerCue')
    ET.SubElement(actions, 'set_value', name='$Faction', exact='parent.$Faction')
    ET.SubElement(actions, 'set_value', name='$RequestSector', exact='if $Requester.isclass.sector then $Requester else $Requester.sector')
    ET.SubElement(actions, 'set_value', name='$DebugText', exact="'TM economic purchase '")
    ET.SubElement(actions, 'set_value', name='$Miner', exact='$Ware.hastag.minable')
    ET.SubElement(actions, 'set_value', name='$Salvager', exact='not $Miner and $Ware.isprocessed and $Ware.hastag.recycling')
    ET.SubElement(actions, 'set_value', name='$Tags', exact='if $Miner then [tag.miner, $Ware.transporttag] else (if $Salvager then [tag.tug] else [tag.trader, $Ware.transporttag])')
    call = ET.SubElement(actions, 'run_actions', ref='md.TM_Empire_Purchase.ReadPurchaseOptions', result='$Options')
    ET.SubElement(call, 'param', name='Tags', value='$Tags')
    ET.SubElement(call, 'param', name='Classes', value='[class.ship_s, class.ship_m, class.ship_l]')
    available = ET.SubElement(actions, 'do_if', value='$Options.count')
    ET.SubElement(available, 'set_value', name='$Option', exact='$Options.random')
    call = ET.SubElement(available, 'run_actions', ref='md.TM_Empire_Purchase.PreparePurchase', result='$PurchaseState')
    for name, value in (('ManagerCue', '$TM_ManagerCue'), ('GoalCue', 'namespace'), ('Shipyard', '$Option.$shipyard'), ('Macro', '$Option.$macro'), ('Budget', 'player.money')):
        ET.SubElement(call, 'param', name=name, value=value)
    ET.SubElement(call, 'param', name='ActionRecord', value='$ActionDefinition')
    accepted = ET.SubElement(available, 'do_if', value="$PurchaseState == 'quote_requested'")
    ET.SubElement(accepted, 'set_value', name='$PurchaseKey', exact='$ActionDefinition.$TM_PurchaseKey')
    rejected = ET.SubElement(available, 'do_else')
    ET.SubElement(rejected, 'set_value', name='$ActionDefinition.$WaitReason', exact='$PurchaseState')
    ET.SubElement(rejected, 'cancel_cue', cue='this')
    empty = ET.SubElement(actions, 'do_else')
    ET.SubElement(empty, 'set_value', name='$ActionDefinition.$WaitReason', exact="'no_accessible_cargo_ship'")
    ET.SubElement(empty, 'cancel_cue', cue='this')
    children = ET.SubElement(request, 'cues')
    poll = ET.SubElement(children, 'cue', name='PurchasedFreighterObserved', checkinterval='15s')
    conditions = ET.SubElement(poll, 'conditions')
    ET.SubElement(conditions, 'check_value', value='$PurchaseKey?')
    ET.SubElement(poll, 'delay', exact='15s')
    actions = ET.SubElement(poll, 'actions')
    pending = ET.SubElement(actions, 'do_if', value='@md.TM_Empire_Purchase.Request.$Pending.$key == $PurchaseKey and (md.TM_Empire_Purchase.Tracked.$Build? or @md.TM_Empire_Purchase.Request.$Pending.$state == \'ready\')')
    ET.SubElement(pending, 'run_actions', ref='md.TM_Empire_Purchase.CompletePurchase', result='$PurchaseProgress')
    delivered = ET.SubElement(actions, 'do_if', value="@md.TM_Empire_Purchase.Request.$LastResult.$key == $PurchaseKey and md.TM_Empire_Purchase.Request.$LastResult.$state == 'delivered'")
    ET.SubElement(delivered, 'set_value', name='$Ship', exact='md.TM_Empire_Purchase.Request.$LastResult.$ship')
    # После передачи claim старый purchase goal больше не вправе выдавать
    # приказы. Повторяем только подтверждение доставки, сохраняя этот этап.
    delivery = delivered
    delivered = ET.SubElement(delivery, 'do_if', value='not @$TM_DeliveryHandedOff')
    observe = ET.SubElement(delivered, 'run_actions', ref='md.TM_Empire_Runtime.ObserveOwnedCommander', result='$TM_AssignmentObservation')
    ET.SubElement(observe, 'param', name='Ship', value='$Ship')
    ET.SubElement(delivered, 'set_value', name='$TM_OrderReceipt', exact="'not_sent'")
    timing_names = {'$ActionDefinition.$LaunchTime', '$Duration', '$Timeout'}
    timing = ET.SubElement(delivered, 'do_if', value='not $TM_RoutineTiming?')
    for node in list(native_built):
        if node.tag == 'set_value' and node.get('name') in timing_names:
            timing.append(node)
    ET.SubElement(timing, 'set_value', name='$TM_RoutineTiming', exact='true')
    for node in list(native_built):
        if node.tag in ('set_requested_job_ship_timeout', 'cancel_cue'): continue
        if node.tag == 'set_value' and node.get('name') in timing_names: continue
        if node.tag == 'do_if' and any(order.get('id') == "'AssignCommander'" and order.find("param[@name='commander']") is None for order in node.iter('create_order')): continue
        delivered.append(node)
    routine = ' or '.join('@' + step_receipts[key] + " == 'sent'" for key in ("'MiningRoutine'", "'SalvageRoutine'", "'TradeRoutine'"))
    commander = step_receipts["'AssignCommander'"]
    confirmed = ET.SubElement(delivered, 'do_if', value=f"({routine}) and (not ($Priority and $Requester.isclass.container) or (@{commander} == 'sent' and $Ship.commander == $Requester and @$Ship.$tm_empire_claim.$assignment.$state == 'observed'))")
    transfer = ET.SubElement(confirmed, 'run_actions', ref='md.TM_Empire_Runtime.TransferOwnedClaim', result='$TM_HandoffReason')
    for name, value in [('Ship', '$Ship'), ('ManagerCue', '$TM_ManagerCue'), ('GoalCue', 'namespace.parent'), ('FromGoalCue', 'namespace')]:
        ET.SubElement(transfer, 'param', name=name, value=value)
    accepted = ET.SubElement(confirmed, 'do_if', value="$TM_HandoffReason == 'available'")
    failed_handoff = ET.SubElement(confirmed, 'do_else')
    ET.SubElement(failed_handoff, 'set_value', name='$ActionDefinition.$WaitReason', exact='$TM_HandoffReason')
    ET.SubElement(accepted, 'set_value', name='$TM_DeliveryHandedOff', exact='true')
    confirmed = ET.SubElement(delivery, 'do_if', value='@$TM_DeliveryHandedOff')
    call = ET.SubElement(confirmed, 'run_actions', ref='md.TM_Empire_Purchase.AcknowledgeDelivery', result='$TM_DeliveryReceipt')
    for name, value in (('Key', '$PurchaseKey'), ('GoalCue', 'namespace'), ('Ship', '$Ship'), ('TransferredClaimGoal', 'namespace.parent')):
        ET.SubElement(call, 'param', name=name, value=value)
    acknowledged = ET.SubElement(confirmed, 'do_if', value="$TM_DeliveryReceipt == 'accepted'")
    ET.SubElement(acknowledged, 'set_value', name='$ActionDefinition.$Ship', exact='$Ship')
    ET.SubElement(acknowledged, 'set_value', name='$ActionDefinition.$TM_PurchaseState', exact="'delivered'")
    ET.SubElement(acknowledged, 'set_value', name='$ActionDefinition.$WaitReason', exact="'native_economic_order_observed'")
    ET.SubElement(acknowledged, 'set_value', name='$ActionDefinition.$TM_Expires', exact='$Timeout')
    ET.SubElement(acknowledged, 'cancel_cue', cue='parent')
    unacknowledged = ET.SubElement(confirmed, 'do_else')
    ET.SubElement(unacknowledged, 'set_value', name='$ActionDefinition.$WaitReason', exact='$TM_DeliveryReceipt')
    retry = ET.SubElement(actions, 'do_else')
    ET.SubElement(retry, 'set_value', name='$ActionDefinition.$WaitReason', exact="'purchase_pending_native_receipt'")
    failed = ET.SubElement(retry, 'do_if', value="@md.TM_Empire_Purchase.Request.$LastResult.$key == $PurchaseKey and md.TM_Empire_Purchase.Request.$LastResult.$state == 'waiting'")
    ET.SubElement(failed, 'set_value', name='$ActionDefinition.$WaitReason', exact='md.TM_Empire_Purchase.Request.$LastResult.$reason')
    ET.SubElement(failed, 'set_value', name='$ActionDefinition.$TM_PurchaseState', exact="'failed'")
    ET.SubElement(failed, 'cancel_cue', cue='parent')
    ET.SubElement(actions, 'reset_cue', cue='this')
    adapt_economy_action_receipts(root)


def adapt_economy_action_receipts(root):
    # Paid acquisition can wait for delivery before native timing is set.
    # The child timeout watcher is already active during this wait.
    for watcher in root.findall(".//cue[@name='Request_Commandeerable_Freighter_Disregard_Patch']"):
        for check in watcher.findall("conditions/check_value[@value='player.age ge $Timeout']"):
            check.set('value', '$Timeout? and player.age ge $Timeout')
    """Keep the native action accounting while a paid player order is pending."""
    evaluation = root.find(".//cue[@name='EvaluateSectorShortage']/actions")
    if evaluation is None:
        raise ValueError('native sector action accounting missing')
    for branch in evaluation.iter('do_elseif'):
        if branch.get('value') not in ("$ChosenAction == '$request_freighter'",
                                      "$ChosenAction == '$request_priority_freighter'"):
            continue
        ready = branch.find("do_if[@value='$NewActionDef.$Ship?']")
        if ready is None:
            raise ValueError('native freighter action acceptance missing')
        ready.set('value', '$NewActionDef.$Ship? or $NewActionDef.$TM_PurchaseKey?')
        for node in list(ready):
            if node.tag == 'debug_text':
                ready.remove(node)
                present = ET.Element('do_if', value='$NewActionDef.$Ship?')
                present.append(node)
                ready.insert(0, present)
    station_request = root.find(".//cue[@name='RequestProductionFreighter']/actions")
    if station_request is None:
        raise ValueError('native station transport accounting missing')
    station_receipts = [node for node in station_request.iter('do_if')
                        if node.get('value') == '$NewActionDef.$Ship?']
    for node in station_receipts:
        node.set('value', '$NewActionDef.$Ship? or $NewActionDef.$TM_PurchaseKey?')
        debug_branches = [child for child in node if child.tag in ('do_if', 'do_else')
                          and any('$NewActionDef.$Ship.' in entry.get('text', '')
                                  for entry in child.iter('debug_text'))]
        if debug_branches:
            present = ET.SubElement(node, 'do_if', value='$NewActionDef.$Ship?')
            for child in debug_branches:
                node.remove(child)
                present.append(child)
    check = root.find(".//library[@name='CheckRunningActions']/actions")
    if check is None:
        raise ValueError('native running economic action accounting missing')
    for node in check.iter('do_if'):
        if node.get('value') == '$CommandeeredShip.isoperational and $CommandeeredShip.isjobship and not @$ActionReportDef.$Disregard':
            node.set('value', '$CommandeeredShip.exists and $CommandeeredShip.isplayerowned and $CommandeeredShip.isoperational and not @$ActionReportDef.$Disregard')
    for branch in check.iter('do_elseif'):
        if branch.get('value') not in ("$ActionReportDef.$Type == '$request_freighter'",
                                      "$ActionReportDef.$Type == '$request_priority_freighter'"):
            continue
        for child in list(branch):
            branch.remove(child)
        ET.SubElement(branch, 'set_value', name='$RequestedShip', exact='@$ActionReportDef.$Ship')
        delivered = ET.SubElement(branch, 'do_if', value="@$ActionReportDef.$TM_PurchaseState == 'delivered'")
        lost = ET.SubElement(delivered, 'do_if', value='not $RequestedShip.exists or not $RequestedShip.isplayerowned or $RequestedShip.iswreck or (@$ActionReportDef.$TM_Expires and player.age ge $ActionReportDef.$TM_Expires)')
        ET.SubElement(lost, 'set_value', name='$DisregardAction', exact='true')
        ET.SubElement(lost, 'set_value', name='$DisregardReason', exact="'Owned ship lost or native request period elapsed; property retained'")
        ET.SubElement(lost, 'set_value', name='$DisregardObject', exact='$RequestedShip')
        pending = ET.SubElement(branch, 'do_elseif', value='$ActionReportDef.$TM_PurchaseKey?')
        failed = ET.SubElement(pending, 'do_if', value="@$ActionReportDef.$TM_PurchaseState == 'failed'")
        ET.SubElement(failed, 'set_value', name='$DisregardAction', exact='true')
        ET.SubElement(failed, 'set_value', name='$DisregardReason', exact='@$ActionReportDef.$WaitReason')
        # Pending and unknown keep the native action cost. A missing receipt
        # cannot authorize another paid effect; the purchase adapter reconciles it.
        missing = ET.SubElement(branch, 'do_else')
        ET.SubElement(missing, 'set_value', name='$DisregardAction', exact='true')
        ET.SubElement(missing, 'set_value', name='$DisregardReason', exact="'No owned ship or paid purchase receipt'")
        ET.SubElement(branch, 'remove_value', name='$RequestedShip')
    adapt_known_market_inputs(root)


def adapt_station_mining_provision(root):
    """Feed native Upkeep gaps to the existing economic request/accounting path."""
    if root.get('name') != 'TM_Empire_FactionLogic_Economy':
        return
    actions = root.find(".//cue[@name='EvaluateShortages']/actions")
    for name in ('Request_Commandeerable_Freighter', 'Request_Freighter'):
        request = root.find(f".//cue[@name='{name}']/actions")
        ware = request.find("set_value[@name='$Ware']")
        index = list(request).index(ware) + 1
        request.insert(index, ET.Element('set_value', name='$ActionDefinition.$TM_Requester', exact='$Requester'))
        request.insert(index + 1, ET.Element('set_value', name='$ActionDefinition.$TM_ResourceTransport', exact='$Ware.waretransport'))
    for parent in actions.iter():
        call = parent.find("run_actions[@ref='CheckRunningActions']")
        if call is None:
            continue
        fragment = ET.fromstring('''<actions>
          <do_if value="$TM_OwnerManager.exists and $TM_OwnerManager == @md.TM_Empire_Runtime.Registry.$ManagerCue and md.TM_Empire_Runtime.Registry.$State == 'active'">
            <set_value name="$TM_ProvisionReports" exact="@md.TM_Empire_FactionLogic_Economy.GlobalStorageData.$Reports.{$Faction}" />
            <set_value name="$TM_ProvisionStations" exact="if $TM_ProvisionReports then $TM_ProvisionReports.keys.list else []" />
            <do_if value="not $TM_ProvisionCursor?"><set_value name="$TM_ProvisionCursor" exact="1" /></do_if>
            <do_all exact="[8, $TM_ProvisionStations.count].min">
              <do_if value="$TM_ProvisionCursor gt $TM_ProvisionStations.count"><set_value name="$TM_ProvisionCursor" exact="1" /></do_if>
              <set_value name="$TM_ProvisionStation" exact="$TM_ProvisionStations.{$TM_ProvisionCursor}" />
              <set_value name="$TM_ProvisionCursor" operation="add" />
              <do_if value="not $TM_ProvisionStation.exists or not $TM_ProvisionStation.isclass.station or not $TM_ProvisionStation.isplayerowned or not $TM_ProvisionStation.isoperational"><continue /></do_if>
              <run_actions ref="md.TM_Empire_Supply.RequestStationFunding" result="$TM_ProvisionFunding">
                <param name="ManagerCue" value="$TM_OwnerManager" /><param name="GoalCue" value="namespace" /><param name="Station" value="$TM_ProvisionStation" /><param name="Budget" value="player.money" />
              </run_actions>
              <run_actions ref="md.TM_Empire_Runtime.ReadStationTradeNeed" result="$TM_TradeNeed"><param name="Station" value="$TM_ProvisionStation" /></run_actions>
              <do_if value="$TM_TradeNeed.$needed and $TM_TradeNeed.$complete">
                <set_value name="$TM_TradeCovered" exact="false" />
                <set_value name="$TM_TradeActions" exact="if $ActionReports.{$TM_ProvisionStation.sector}? then $ActionReports.{$TM_ProvisionStation.sector} else []" />
                <do_if value="$TM_TradeActions.count gt 128"><set_value name="$TM_TradeCovered" exact="true" /></do_if>
                <do_else>
                  <do_for_each name="$TM_TradeAction" in="$TM_TradeActions">
                    <do_if value="@$TM_TradeAction.$ActionDef.$TM_Requester == $TM_ProvisionStation and not @$TM_TradeAction.$Ware.hastag.minable"><set_value name="$TM_TradeCovered" exact="true" /><break /></do_if>
                  </do_for_each>
                </do_else>
                <do_if value="not $TM_TradeCovered">
                  <set_value name="$TM_ProvisionWare" exact="$TM_TradeNeed.$ware" />
                  <set_value name="$TM_ProvisionDef" exact="table[$Type='$request_prio_commandeerable_freighter', $TM_TradeProvision=true, $TM_ProvisionStation=$TM_ProvisionStation]" />
                  <signal_cue_instantly cue="Request_Commandeerable_Freighter" param="[$TM_ProvisionDef, $TM_ProvisionStation, $TM_ProvisionWare, true]" />
                  <do_if value="not $TM_ProvisionDef.$Ship?">
                    <set_value name="$TM_ProvisionDef.$Type" exact="'$request_priority_freighter'" />
                    <signal_cue_instantly cue="Request_Freighter" param="[$TM_ProvisionDef, $TM_ProvisionStation, $TM_ProvisionWare, true, null]" />
                  </do_if>
                  <do_if value="$TM_ProvisionDef.$Ship? or $TM_ProvisionDef.$TM_PurchaseKey?">
                    <do_if value="not $ActionReports.{$TM_ProvisionStation.sector}?"><set_value name="$ActionReports.{$TM_ProvisionStation.sector}" exact="[]" /></do_if>
                    <append_to_list name="$ActionReports.{$TM_ProvisionStation.sector}" exact="table[$ActionDef=$TM_ProvisionDef, $StartTime=player.age, $Sector=$TM_ProvisionStation.sector, $Ware=$TM_ProvisionWare, $AggregatedValue=0]" />
                  </do_if>
                </do_if>
              </do_if>
              <do_if value="$TM_ProvisionStation.subordinates.count gt 128 or $TM_ProvisionStation.resources.list.count gt 128"><continue /></do_if>
              <run_actions ref="md.Upkeep.Needs_Subordinate_Mining_Ship_Lib" result="$TM_ProvisionTypes"><param name="Commander" value="$TM_ProvisionStation" /></run_actions>
              <do_if value="not $TM_ProvisionTypes.count or $TM_ProvisionStation.resources.list.count gt 128"><continue /></do_if>
              <do_for_each name="$TM_ProvisionType" in="$TM_ProvisionTypes">
                <set_value name="$TM_ProvisionCovered" exact="false" />
                <set_value name="$TM_ProvisionActions" exact="if $ActionReports.{$TM_ProvisionStation.sector}? then $ActionReports.{$TM_ProvisionStation.sector} else []" />
                <do_if value="$TM_ProvisionActions.count gt 128"><continue /></do_if>
                <do_for_each name="$TM_ProvisionAction" in="$TM_ProvisionActions">
                  <do_if value="(@$TM_ProvisionAction.$ActionDef.$TM_Requester == $TM_ProvisionStation and @$TM_ProvisionAction.$ActionDef.$TM_ResourceTransport == $TM_ProvisionType) or (@$TM_ProvisionAction.$ActionDef.$Ship.exists and @$TM_ProvisionAction.$Ware.hastag.minable and @$TM_ProvisionAction.$Ware.waretransport == $TM_ProvisionType and @global.$TM_EmpireComponentRecords.$claim.{$TM_ProvisionAction.$ActionDef.$Ship}.$assignment.$commander == $TM_ProvisionStation)">
                    <set_value name="$TM_ProvisionCovered" exact="true" /><break />
                  </do_if>
                </do_for_each>
                <do_if value="$TM_ProvisionCovered"><continue /></do_if>
                <do_for_each name="$TM_ProvisionWare" in="$TM_ProvisionStation.resources.list">
                  <do_if value="not $TM_ProvisionWare.hastag.minable or $TM_ProvisionWare.waretransport != $TM_ProvisionType or $TM_ProvisionStation.cargo.{$TM_ProvisionWare}.max le 0"><continue /></do_if>
                  <set_value name="$TM_ProvisionAmount" exact="(if @$TM_ProvisionReports.{$TM_ProvisionStation}.$InsufficientProductionWares.{$TM_ProvisionWare} then $TM_ProvisionReports.{$TM_ProvisionStation}.$InsufficientProductionWares.{$TM_ProvisionWare} else 0) + (if @$TM_ProvisionReports.{$TM_ProvisionStation}.$InsufficientBuildWares.{$TM_ProvisionWare} then $TM_ProvisionReports.{$TM_ProvisionStation}.$InsufficientBuildWares.{$TM_ProvisionWare} else 0)" />
                  <!-- Upkeep is the native vacancy decision. Insufficient
                       reports may be empty for a newly started/owner-only
                       factory even while it is waiting for mined resources.
                       Keep the real report value (including zero) for action
                       accounting; do not fabricate a financial shortage. -->
                  <set_value name="$TM_ProvisionDef" exact="table[$Type='$request_prio_commandeerable_freighter', $TM_ProvisionStation=$TM_ProvisionStation, $TM_ProvisionTransport=$TM_ProvisionType]" />
                  <signal_cue_instantly cue="Request_Commandeerable_Freighter" param="[$TM_ProvisionDef, $TM_ProvisionStation, $TM_ProvisionWare, true]" />
                  <do_if value="not $TM_ProvisionDef.$Ship?">
                    <set_value name="$TM_ProvisionDef.$Type" exact="'$request_priority_freighter'" />
                    <signal_cue_instantly cue="Request_Freighter" param="[$TM_ProvisionDef, $TM_ProvisionStation, $TM_ProvisionWare, true, null]" />
                  </do_if>
                  <do_if value="$TM_ProvisionDef.$Ship? or $TM_ProvisionDef.$TM_PurchaseKey?">
                    <do_if value="not $ActionReports.{$TM_ProvisionStation.sector}?"><set_value name="$ActionReports.{$TM_ProvisionStation.sector}" exact="[]" /></do_if>
                    <append_to_list name="$ActionReports.{$TM_ProvisionStation.sector}" exact="table[$ActionDef=$TM_ProvisionDef, $StartTime=player.age, $Sector=$TM_ProvisionStation.sector, $Ware=$TM_ProvisionWare, $AggregatedValue=$TM_ProvisionAmount]" />
                  </do_if>
                  <break />
                </do_for_each>
              </do_for_each>
            </do_all>
            <remove_value name="$TM_ProvisionStations" />
            <remove_value name="$TM_ProvisionReports" />
            <remove_value name="$TM_ProvisionActions" />
            <remove_value name="$TM_ProvisionDef" />
            <remove_value name="$TM_ProvisionTypes" />
          </do_if>
        </actions>''')
        index = list(parent).index(call) + 1
        for node in fragment:
            parent.insert(index, node)
            index += 1
        return
    raise ValueError('native station provision accounting boundary missing')


def adapt_known_market_inputs(root):
    """Supply the stock analysis with public offers, without NPC private reports."""
    manager = root.find(".//library[@name='Econ_Manager']")
    evaluation = manager.find(".//cue[@name='EvaluateShortages']/actions")
    evaluation.insert(0, ET.Element('set_value', name='$TM_KnownMarketWares', exact='table[]'))
    evaluation.insert(1, ET.Element('set_value', name='$TM_EvaluatedPublicWares', exact='table[]'))
    evaluation.insert(2, ET.Element('set_value', name='$TM_MarketDeferred', exact='0'))
    sector = manager.find(".//cue[@name='EvaluateSectorShortage']/actions")
    parents = {child: parent for parent in sector.iter() for child in parent}
    anchor = next((node for node in sector.iter('set_value')
                   if node.get('name') == '$SectorBuyOfferValue'), None)
    if anchor is None:
        raise ValueError('native public supply input boundary missing')
    parent = parents[anchor]
    position = list(parent).index(anchor)
    call = ET.Element('run_actions', ref='FillKnownSellOffers', result='$TM_MarketComplete')
    ET.SubElement(call, 'param', name='Ware', value='$Ware')
    ET.SubElement(call, 'param', name='Sector', value='$Sector')
    ET.SubElement(call, 'param', name='SectorNeighbourTable', value='$SectorNeighbourTable')
    ET.SubElement(call, 'param', name='TM_KnownMarketWares', value='$TM_KnownMarketWares')
    ET.SubElement(call, 'param', name='SectorSellOfferAmountsTable', value='$SectorSellOfferAmountsTable')
    done = ET.Element('do_if', value='@$TM_EvaluatedPublicWares.{$ReportTablesIndex}.{$Sector}.{$Ware}')
    ET.SubElement(done, 'continue')
    parent.insert(position, done)
    parent.insert(position + 1, call)
    pending = ET.Element('do_if', value="$TM_MarketComplete == 'pending'")
    ET.SubElement(pending, 'set_value', name='$TM_MarketDeferred', exact='1', operation='add')
    # break leaves the ware loop; hold the sector cursor until public quotes
    # arrive. Cue actions cannot use a run_actions-library return.
    ET.SubElement(pending, 'set_value', name='$TM_SectorMarketPending', exact='true')
    ET.SubElement(pending, 'break')
    sector.insert(0, ET.Element('set_value', name='$TM_SectorMarketPending', exact='false'))
    advance = next(node for node in sector if node.tag == 'set_value'
                   and node.get('name') == '$TableRefIndex' and node.get('operation') == 'add')
    advance_index = list(sector).index(advance)
    bookkeeping = list(sector)[advance_index:advance_index + 2]
    if len(bookkeeping) != 2 or bookkeeping[1].tag != 'do_if':
        raise ValueError('native sector cursor completion boundary missing')
    ready = ET.Element('do_if', value='not $TM_SectorMarketPending')
    for node in bookkeeping:
        sector.remove(node)
        ready.append(node)
    sector.insert(advance_index, ready)
    parent.insert(position + 2, pending)
    missing = ET.Element('do_if', value='not $TM_MarketComplete')
    parent.insert(position + 3, missing)
    bounded = ET.SubElement(missing, 'do_if', value='$TM_NoActionRecords.count lt 32')
    ET.SubElement(bounded, 'append_to_list', name='$TM_NoActionRecords',
        exact="table[$sector=$Sector, $ware=$Ware, $reason='known_market_input_incomplete', $observed=player.age]")
    full = ET.SubElement(missing, 'do_else')
    ET.SubElement(full, 'set_value', name='$TM_NoActionRecordsComplete', exact='false')
    ET.SubElement(missing, 'continue')
    completed = ET.Element('do_if', value='not $TM_EvaluatedPublicWares.{$ReportTablesIndex}?')
    ET.SubElement(completed, 'set_value', name='$TM_EvaluatedPublicWares.{$ReportTablesIndex}', exact='table[]')
    parent.insert(position + 4, completed)
    completed_sector = ET.Element('do_if', value='not $TM_EvaluatedPublicWares.{$ReportTablesIndex}.{$Sector}?')
    ET.SubElement(completed_sector, 'set_value', name='$TM_EvaluatedPublicWares.{$ReportTablesIndex}.{$Sector}', exact='table[]')
    parent.insert(position + 5, completed_sector)
    parent.insert(position + 6, ET.Element('set_value', name='$TM_EvaluatedPublicWares.{$ReportTablesIndex}.{$Sector}.{$Ware}', exact='true'))
    library = ET.SubElement(manager.find('cues'), 'library',
                            name='FillKnownSellOffers', purpose='run_actions')
    params = ET.SubElement(library, 'params')
    ET.SubElement(params, 'param', name='Ware')
    ET.SubElement(params, 'param', name='Sector')
    ET.SubElement(params, 'param', name='SectorNeighbourTable')
    ET.SubElement(params, 'param', name='TM_KnownMarketWares')
    ET.SubElement(params, 'param', name='SectorSellOfferAmountsTable')
    actions = ET.SubElement(library, 'actions')
    ET.SubElement(actions, 'find_sector_in_range', name='$TM_NearbySectors',
                  distances='$TM_Distances', object='$Sector', maxdistance='5',
                  known='true', multiple='true')
    own = ET.SubElement(actions, 'do_if', value='not $TM_NearbySectors.indexof.{$Sector}')
    ET.SubElement(own, 'append_to_list', name='$TM_NearbySectors', exact='$Sector')
    ET.SubElement(actions, 'set_value', name='$TM_Distances.{$Sector}', exact='0')
    too_many = ET.SubElement(actions, 'do_if', value='$TM_NearbySectors.count gt 512')
    ET.SubElement(too_many, 'return', value='false')
    create = ET.SubElement(actions, 'do_if', value='not $TM_KnownMarketWares.{$Ware}?')
    ET.SubElement(create, 'set_value', name='$TM_KnownMarketWares.{$Ware}', exact='table[]')
    ET.SubElement(actions, 'set_value', name='$SectorNeighbourTable.{$Sector}', exact='table[]')
    ET.SubElement(actions, 'set_value', name='$TM_Complete', exact='true')
    ET.SubElement(actions, 'set_value', name='$TM_Searches', exact='0')
    ET.SubElement(actions, 'set_value', name='$TM_Pending', exact='false')
    nearby = ET.SubElement(actions, 'do_for_each', name='$TM_MarketSector', **{'in':'$TM_NearbySectors'})
    ET.SubElement(nearby, 'set_value', name='$TM_Distance', exact='$TM_Distances.{$TM_MarketSector}')
    distance = ET.SubElement(nearby, 'do_if', value='not $SectorNeighbourTable.{$Sector}.{$TM_Distance}?')
    ET.SubElement(distance, 'set_value', name='$SectorNeighbourTable.{$Sector}.{$TM_Distance}', exact='[]')
    ET.SubElement(nearby, 'append_to_list', name='$SectorNeighbourTable.{$Sector}.{$TM_Distance}', exact='$TM_MarketSector')
    cached = ET.SubElement(nearby, 'do_if', value='$TM_KnownMarketWares.{$Ware}.{$TM_MarketSector}?')
    failed = ET.SubElement(cached, 'do_if', value='not $TM_KnownMarketWares.{$Ware}.{$TM_MarketSector}')
    ET.SubElement(failed, 'set_value', name='$TM_Complete', exact='false')
    ET.SubElement(cached, 'continue')
    exhausted = ET.SubElement(nearby, 'do_if', value='$TM_Searches ge 8')
    ET.SubElement(exhausted, 'set_value', name='$TM_Pending', exact='true')
    ET.SubElement(exhausted, 'break')
    ET.SubElement(nearby, 'set_value', name='$TM_Searches', exact='1', operation='add')
    search = ET.SubElement(nearby, 'find_sell_offer', result='$TM_KnownSellOffers',
                           wares='$Ware', space='$TM_MarketSector', multiple='true')
    seller = ET.SubElement(search, 'match_seller', tradesknownto='faction.player')
    ET.SubElement(seller, 'match_relation_to', object='player.entity',
                  comparison='ge', relation='dock')
    incomplete = ET.SubElement(nearby, 'do_if', value='$TM_KnownSellOffers.count gt 128')
    ET.SubElement(incomplete, 'set_value', name='$TM_KnownMarketWares.{$Ware}.{$TM_MarketSector}', exact='false')
    ET.SubElement(incomplete, 'set_value', name='$TM_Complete', exact='false')
    ET.SubElement(incomplete, 'continue')
    scan = ET.SubElement(nearby, 'do_all', exact='$TM_KnownSellOffers.count', counter='$TM_OfferIndex')
    ET.SubElement(scan, 'set_value', name='$TM_Offer', exact='$TM_KnownSellOffers.{$TM_OfferIndex}')
    valid = ET.SubElement(scan, 'do_if', value='$TM_Offer.owner.exists and '
                          'not $TM_Offer.owner.isplayerowned and $TM_Offer.owner.isknown and '
                          '$TM_Offer.owner.isoperational and $TM_Offer.owner.sector.exists and '
                          '$TM_Offer.owner.sector.isknown')
    ET.SubElement(valid, 'set_value', name='$TM_OfferSector', exact='$TM_Offer.owner.sector')
    create = ET.SubElement(valid, 'do_if', value='not $SectorSellOfferAmountsTable.{$TM_OfferSector}?')
    ET.SubElement(create, 'set_value', name='$SectorSellOfferAmountsTable.{$TM_OfferSector}', exact='table[]')
    ET.SubElement(valid, 'set_value', name='$SectorSellOfferAmountsTable.{$TM_OfferSector}.{$Ware}',
                  exact='$TM_Offer.offeramount', operation='add')
    ET.SubElement(nearby, 'set_value', name='$TM_KnownMarketWares.{$Ware}.{$TM_MarketSector}', exact='true')
    ET.SubElement(actions, 'return', value="if $TM_Pending then 'pending' else $TM_Complete")


def adapt_patrol_registration(root):
    if root.get('name') != 'TM_Empire_FactionGoal_PatrolCoordinationService':
        return
    registration = root.find(".//cue[@name='Register_Factions']/actions/do_all")
    if registration is None:
        raise ValueError('native patrol registration boundary missing')
    existing = registration.find("do_elseif[@exact='event.param.$Faction']")
    if existing is None:
        raise ValueError('native existing faction registration missing')
    # A native NPC faction has one long-lived manager. Our private player
    # manager restarts on reassignment, so attach the new instance to the
    # existing faction entry without duplicating or clearing distress calls.
    existing.clear()
    existing.set('value', '$MasterList_DistressCalls.{$Counter_MasterList_DistressCalls}.{1}')
    existing.set('exact', 'event.param.$Faction')
    ET.SubElement(existing, 'set_value', name='event.param.$PCS_FactionIndex',
                  exact='$Counter_MasterList_DistressCalls')
    ET.SubElement(existing, 'set_value', name='event.param.$PCS_CIC', exact='namespace')
    ET.SubElement(existing, 'break')


def adapt_temporary_military_support(root):
    if root.get('name') != 'TM_Empire_FactionGoal_PatrolCoordinationService':
        return
    # Keep the native closest-ship choice, but apply the same eligibility
    # contract to every candidate rather than failing on one unsuitable ship.
    scout = root.find(".//cue[@name='Designate_Scout']")
    loop = scout.find(".//do_all[@counter='$Counter_OurLocalShips']")
    if loop is None:
        raise ValueError('native distress scout selection missing')
    call = ET.Element('run_actions', ref='md.TM_Empire_Runtime.CanUseMilitarySupport', result='$TM_CandidateReason')
    for name, value in [('Ship', '$OurLocalShips.{$Counter_OurLocalShips}'), ('ManagerCue', '@$TM_ManagerCue'), ('GoalCue', 'namespace')]:
        ET.SubElement(call, 'param', name=name, value=value)
    loop.insert(0, call)
    blocked = ET.Element('do_if', value="$TM_CandidateReason != 'available'")
    ET.SubElement(blocked, 'continue')
    loop.insert(1, blocked)
    for gate in scout.iter('do_else'):
        if any(n.get('name') == '$TM_WaitReason' for n in list(gate)):
            ET.SubElement(gate, 'set_value', name='$Feedback', exact='-10')
            ET.SubElement(gate, 'signal_cue', cue='End')
    replacements = {'CanUseOwnedShip': 'CanUseMilitarySupport',
                    'ClaimOwnedShip': 'ClaimMilitarySupport',
                    'ReleaseOwnedClaim': 'ReleaseMilitarySupport'}
    for call in root.iter('run_actions'):
        ref = call.get('ref', '')
        if ref.startswith('md.TM_Empire_Runtime.'):
            name = ref.rsplit('.', 1)[1]
            if name in replacements:
                call.set('ref', 'md.TM_Empire_Runtime.' + replacements[name])


def adapt_economy_observations(root):
    if root.get('name') != 'TM_Empire_FactionLogic_Economy':
        return
    manager = root.find(".//library[@name='Econ_Manager']/actions")
    if manager is None:
        raise ValueError('native economic manager initialization missing')
    ET.SubElement(manager, 'set_value', name='$TM_OwnerManager',
                  exact='$FactionManagerCue')
    # Bootstrap the same native shortage pipeline once when our economy cue is
    # created. Stock periodic analysis otherwise starts only after 25-30min;
    # no private planner or repeated tick-triggered recalculation is added.
    bootstrap = ET.SubElement(manager, 'do_if',
        value='$FactionManagerCue.exists and '
              '$FactionManagerCue == @md.TM_Empire_Runtime.Registry.$ManagerCue and '
              "md.TM_Empire_Runtime.Registry.$State == 'active'")
    ET.SubElement(bootstrap, 'signal_cue', cue='md.TM_Empire_FactionLogic_Economy.GenerateShortageData_Delay')
    # Observe native completion; evaluation does not prove economic effects.
    completed = [node for node in root.iter('signal_cue_instantly')
                 if "'shortages evaluated'" in node.get('param', '')]
    if len(completed) != 1:
        raise ValueError('native economic evaluation completion ambiguous')
    parents = {child: parent for parent in root.iter() for child in parent}
    signal = completed[0]
    parent = parents[signal]
    record = ET.Element('do_if', value='$TM_OwnerManager.exists and '
        '$TM_OwnerManager == @md.TM_Empire_Runtime.Registry.$ManagerCue and '
        "md.TM_Empire_Runtime.Registry.$State == 'active'")
    ET.SubElement(record, 'set_value', name='$TM_OwnerManager.$tm_empire_economy_evaluation',
        exact="table[$observed=player.age, $state='observed', $reason='native_shortages_evaluated', "
              "$report_stations=@md.TM_Empire_FactionLogic_Economy.GlobalStorageData.$Reports.{$Faction}.keys.count, "
              "$product_sectors=$SectorInsufficientProductsTable.keys.count, "
              "$workforce_sectors=$SectorInsufficientWorkforceTable.keys.count, "
              "$build_sectors=$SectorInsufficientBuildTable.keys.count, "
              "$action_sectors=$ActionReports.keys.count, "
              "$no_action_records=$TM_NoActionRecords.count, "
              "$no_action_complete=$TM_NoActionRecordsComplete]")
    parent.insert(list(parent).index(signal), record)
    evaluation = root.find(".//cue[@name='EvaluateShortages']/actions")
    sector_evaluation = root.find(".//cue[@name='EvaluateSectorShortage']/actions")
    if evaluation is None or sector_evaluation is None:
        raise ValueError('native economic decision boundary missing')
    evaluation.insert(0, ET.Element('set_value', name='$TM_NoActionRecords', exact='[]'))
    evaluation.insert(1, ET.Element('set_value', name='$TM_NoActionRecordsComplete', exact='true'))
    no_action = sector_evaluation.find(".//do_if[@value='not $NewActionValid']")
    if no_action is None:
        raise ValueError('native economic no-action boundary missing')
    ET.SubElement(no_action, 'set_value', name='$TM_NoActionReason',
        exact="if not $PursueNewAction then 'native_existing_actions_cover_need' "
              "else if $AdjustedSectorValue lt (if $IsProductionIssue then "
              "$ProductionThresholds.$request_production else "
              "$TransportationThresholds.$request_commandeerable_freighter) then "
              "'native_need_below_action_threshold' else 'native_no_viable_economic_action'")
    bounded = ET.SubElement(no_action, 'do_if', value='$TM_NoActionRecords.count lt 32')
    ET.SubElement(bounded, 'append_to_list', name='$TM_NoActionRecords',
        exact='table[$sector=$Sector, $ware=$Ware, $reason=$TM_NoActionReason, $observed=player.age]')
    full = ET.SubElement(no_action, 'do_else')
    ET.SubElement(full, 'set_value', name='$TM_NoActionRecordsComplete', exact='false')
    process = root.find(".//cue[@name='ProcessStations']")
    if process is None:
        raise ValueError('native shortage processing boundary missing')
    operational = process.find("actions/do_all/do_if[@value='$Object.isoperational']")
    if operational is None:
        raise ValueError('native shortage ownership boundary missing')
    # Detailed production/cargo reports are private to our assets, including
    # build storage. Known foreign stations do not expose their private state.
    operational.set('value', '$Object.exists and $Object.isplayerowned and $Object.isoperational')
    # Native reports omit stations with no financial shortage/offer entries.
    # A missing mining subordinate is still a native station requirement;
    # retain that report so the ordinary EvaluateShortages provision pass can
    # see it. Do not manufacture production quantities or another executor.
    report_gate = operational.find("do_if[@value='$Report.keys.count']")
    assert report_gate is not None
    upkeep = ET.Element('do_if', value='$Object.isclass.station')
    ET.SubElement(upkeep, 'set_value', name='$TM_MissingMiningTypes', exact='[]')
    ET.SubElement(upkeep, 'set_value', name='$TM_TradeNeed',
                  exact='table[$needed=false, $complete=false, $ware=null]')
    bounded_upkeep = ET.SubElement(upkeep, 'do_if',
        value='$Object.resources.list.count le 32 and $Object.subordinates.count le 32')
    native_need = ET.SubElement(bounded_upkeep, 'run_actions',
        ref='md.Upkeep.Needs_Subordinate_Mining_Ship_Lib', result='$TM_MissingMiningTypes')
    ET.SubElement(native_need, 'param', name='Commander', value='$Object')
    retain = ET.SubElement(bounded_upkeep, 'do_if', value='$TM_MissingMiningTypes.count')
    ET.SubElement(retain, 'set_value', name='$Report.$TM_MissingMiningTypes',
                  exact='$TM_MissingMiningTypes')
    trade_need = ET.SubElement(bounded_upkeep, 'run_actions',
                              ref='md.TM_Empire_Runtime.ReadStationTradeNeed', result='$TM_TradeNeed')
    ET.SubElement(trade_need, 'param', name='Station', value='$Object')
    trade_missing = ET.SubElement(bounded_upkeep, 'do_if', value='$TM_TradeNeed.$needed')
    ET.SubElement(trade_missing, 'set_value', name='$Report.$TM_MissingTradeWare',
                  exact='$TM_TradeNeed.$ware')
    operational.insert(list(operational).index(report_gate), upkeep)
    # Reuse the completed native report. This is evidence, not a second
    # economic planner or an attribution of fault to the station manager.
    observation = ET.SubElement(operational, 'do_if', value='$Object.isclass.station')
    ET.SubElement(observation, 'set_value', name='$Object.$tm_empire_economy_observation',
        exact='table[$station=$Object, $employee=@$Object.assignedcontrolentity.{controlpost.manager}, '
              "$employee_name=if $Object.assignedcontrolentity.{controlpost.manager}.exists then $Object.assignedcontrolentity.{controlpost.manager}.knownname else 'Менеджер не назначен', "
              "$employee_seed=if $Object.assignedcontrolentity.{controlpost.manager}.exists then '' + $Object.assignedcontrolentity.{controlpost.manager}.seed else 'unknown', "
              '$observed=player.age, $session=@md.TM_Empire_Assets.State.$ObservationSession, '
              '$manager=@md.TM_Empire_Runtime.Registry.$ManagerCue, $modules=$Object.modules.all.count, '
              '$managementskill=@$Object.assignedcontrolentity.{controlpost.manager}.skill.{skilltype.management}, '
              '$ships=table[], $ships_total=$Object.subordinates.count, '
              '$ships_complete=$Object.subordinates.count le 32, $report=$Report, $tradeneed=$TM_TradeNeed, '
              '$ownaccount=$Object.hasownaccount, $restricted=$Object.istraderestricted, '
              '$last_attack=$Object.lastattacktime, '
              "$attacker=if $Object.lastattacker.exists and $Object.lastattacker.isknown then $Object.lastattacker.knownname else null, "
              '$money=if $Object.hasownaccount then $Object.money else null, '
              '$productionmoney=if $Object.hasownaccount then $Object.productionmoney else null, '
              '$underfunded=$Object.hasownaccount and not $Object.istraderestricted and '
              '($Object.money * 10) le ($Object.productionmoney * 9)]')
    # Stock production flags are observations, not an inferred idle duration
    # or a verdict against the station manager. Read once per native analysis.
    ET.SubElement(observation, 'set_value', name='$TM_ProductionState',
        exact='table[$total=0, $complete=$Object.productions.count le 32, '
              '$producing=0, $resources=0, $storage=0, $manual=0, $paused=0, $other=0]')
    production_scan = ET.SubElement(observation, 'do_all',
        exact='[32, $Object.productions.count].min', counter='$TM_ProductionIndex')
    ET.SubElement(production_scan, 'set_value', name='$TM_Production',
                  exact='$Object.productions.{$TM_ProductionIndex}')
    absent = ET.SubElement(production_scan, 'do_if', value='not $TM_Production.exists')
    ET.SubElement(absent, 'set_value', name='$TM_ProductionState.$complete', exact='false')
    ET.SubElement(absent, 'continue')
    # The stock HQ research module is also class.production, but its macro
    # has no manufactured products. Use the native macro product list rather
    # than interpreting research/no active queue as idle manufacturing.
    nonmanufacturing = ET.SubElement(production_scan, 'do_if',
        value='@$TM_Production.macro.products.list.count le 0')
    ET.SubElement(nonmanufacturing, 'continue')
    ET.SubElement(production_scan, 'set_value', name='$TM_ProductionState.$total',
                  operation='add', exact='1')
    flags = [('producing', 'isproducing'), ('manual', 'ispausedmanually'),
             ('paused', 'ispaused'), ('resources', 'iswaitingforresources'),
             ('storage', 'iswaitingforstorage')]
    for index, (label, prop) in enumerate(flags):
        branch = ET.SubElement(production_scan, 'do_if' if index == 0 else 'do_elseif',
                               value='$TM_Production.' + prop)
        ET.SubElement(branch, 'set_value', name='$TM_ProductionState.$' + label,
                      exact='$TM_ProductionState.$' + label + ' + 1')
    other = ET.SubElement(production_scan, 'do_else')
    ET.SubElement(other, 'set_value', name='$TM_ProductionState.$other',
                  exact='$TM_ProductionState.$other + 1')
    ET.SubElement(observation, 'set_value', name='$Object.$tm_empire_economy_observation.$production',
                  exact='$TM_ProductionState')
    # Stock station roles precede any assessment of profit or production.
    ET.SubElement(observation, 'set_value', name='$Object.$tm_empire_economy_observation.$purpose',
        exact="if @$Object.buildingmodule.isbuilding then 'building' else "
              "if $Object.canequipships then 'ship_support' else "
              "if $TM_ProductionState.$total gt 0 then 'production' else "
              "if $Object.istradestation then 'trading' else 'other'")
    mining = ET.SubElement(observation, 'do_if',
        value='$Object.resources.list.count le 32 and $Object.subordinates.count le 32')
    ET.SubElement(mining, 'set_value', name='$Object.$tm_empire_economy_observation.$miningtypes',
                  exact='$TM_MissingMiningTypes')
    # Read native owned cargo only; missing/truncated coverage is explicit.
    ET.SubElement(observation, 'set_value', name='$TM_StockWares', exact='[]')
    ET.SubElement(observation, 'set_value', name='$Object.$tm_empire_economy_observation.$stocks', exact='table[]')
    ET.SubElement(observation, 'set_value', name='$Object.$tm_empire_economy_observation.$stocks_complete',
                  exact='$Object.resources.list.count le 32 and $Object.products.list.count le 32')
    stock_sources = ET.SubElement(observation, 'do_for_each', name='$TM_StockSource',
                                 **{'in': '[$Object.resources.list, $Object.products.list]'})
    stock_scan = ET.SubElement(stock_sources, 'do_all', exact='[32, $TM_StockSource.count].min', counter='$TM_StockIndex')
    ET.SubElement(stock_scan, 'set_value', name='$TM_StockWare', exact='$TM_StockSource.{$TM_StockIndex}')
    duplicate = ET.SubElement(stock_scan, 'do_if', value='$TM_StockWares.indexof.{$TM_StockWare}')
    ET.SubElement(duplicate, 'continue')
    full = ET.SubElement(stock_scan, 'do_if', value='$TM_StockWares.count ge 32')
    ET.SubElement(full, 'set_value', name='$Object.$tm_empire_economy_observation.$stocks_complete', exact='false')
    ET.SubElement(full, 'continue')
    ET.SubElement(stock_scan, 'append_to_list', name='$TM_StockWares', exact='$TM_StockWare')
    ET.SubElement(stock_scan, 'set_value', name='$Object.$tm_empire_economy_observation.$stocks.{$TM_StockWare}',
        exact='table[$count=$Object.cargo.{$TM_StockWare}.count, $capacity=$Object.cargo.{$TM_StockWare}.max, '
              '$owner_only=$Object.istraderestricted.{$TM_StockWare}]')
    # A resource/product override may change while the global owner-only
    # flag stays unchanged. Do not carry observations across that boundary.
    # This flag does not claim to describe every faction-specific trade rule.
    ships = ET.SubElement(observation, 'do_all', exact='[32, $Object.subordinates.count].min', counter='$TM_SubordinateIndex')
    ET.SubElement(ships, 'set_value', name='$TM_Subordinate', exact='$Object.subordinates.{$TM_SubordinateIndex}')
    missing_ship = ET.SubElement(ships, 'do_if', value='not $TM_Subordinate.exists')
    ET.SubElement(missing_ship, 'set_value', name='$Object.$tm_empire_economy_observation.$ships_complete', exact='false')
    ET.SubElement(missing_ship, 'continue')
    ET.SubElement(ships, 'set_value', name='$Object.$tm_empire_economy_observation.$ships.{$TM_Subordinate}',
        exact='table[$assignment=$TM_Subordinate.assignment, $operational=$TM_Subordinate.isoperational, '
              '$owned=$TM_Subordinate.isplayerowned, $controlled=$TM_Subordinate == player.controlled, '
              '$working=$TM_Subordinate.orders.count gt 0 or '
              '($TM_Subordinate.order.exists and $TM_Subordinate.order.id != \'Wait\') or '
              '($TM_Subordinate.defaultorder.exists and $TM_Subordinate.defaultorder.id != \'Wait\'), '
              '$cargo_capacity=$TM_Subordinate.cargo.capacity.all, '
              '$pilot_seed=if $TM_Subordinate.pilot.exists then \'\' + $TM_Subordinate.pilot.seed else \'unknown\', '
              '$pilot_skill=if $TM_Subordinate.pilot.exists then $TM_Subordinate.pilot.skill.{skilltype.piloting} else \'unknown\', '
              '$cargo_used=$TM_Subordinate.cargo.capacity.all - $TM_Subordinate.cargo.free.all]')
    interrupted = ET.SubElement(ships, 'do_if', value=(
        'not $Object.$tm_empire_economy_observation.$delivery_interruption? and '
        '$TM_ProductionState.$resources gt 0 and $TM_Subordinate.isplayerowned and '
        '$TM_Subordinate.isoperational and $TM_Subordinate != player.controlled and '
        '$TM_Subordinate.commander == $Object and $TM_Subordinate.assignment == assignment.trade and '
        '$TM_Subordinate.order.exists and $TM_Subordinate.order.id == \'Flee\' and '
        '$TM_Subordinate.lastattacktime ge player.age - 5min and $TM_Subordinate.lastattacktime le player.age and '
        '$TM_Subordinate.lastattacker.exists and $TM_Subordinate.lastattacker.isknown and '
        '$TM_Subordinate.lastattacker.hasrelation.enemy.{faction.player}'))
    ET.SubElement(interrupted, 'set_value', name='$TM_InterruptedWares',
                  exact='if @$Report.$InsufficientProductionWares then $Report.$InsufficientProductionWares.keys.list else []')
    wares = ET.SubElement(interrupted, 'do_all', exact='[8, $TM_InterruptedWares.count].min', counter='$TM_InterruptedIndex')
    ET.SubElement(wares, 'set_value', name='$TM_InterruptedWare', exact='$TM_InterruptedWares.{$TM_InterruptedIndex}')
    matching = ET.SubElement(wares, 'do_if', value=(
        '$Object.resources.{$TM_InterruptedWare}.exists and $Object.cargo.{$TM_InterruptedWare}.count == 0 and '
        '$TM_Subordinate.cargo.{$TM_InterruptedWare}.count gt 0'))
    ET.SubElement(matching, 'set_value', name='$Object.$tm_empire_economy_observation.$delivery_interruption',
                  exact='table[$ship=$TM_Subordinate.knownname, $ware=$TM_InterruptedWare.name, '
                        '$amount=$TM_Subordinate.cargo.{$TM_InterruptedWare}.count, '
                        '$attacker=$TM_Subordinate.lastattacker.knownname, '
                        '$attack=$TM_Subordinate.lastattacktime, $observed=player.age]')
    ET.SubElement(matching, 'break')
    init = ET.Element('do_if', value='not $Object.$tm_empire_personnel_needs?')
    ET.SubElement(init, 'set_value', name='$Object.$tm_empire_personnel_needs', exact='table[]')
    operational.insert(0, init)
    for role, property_name in (('trade', 'tradenpc'), ('shiptrade', 'shiptrader')):
        observed = ET.Element('do_if', value=f'$Object.{property_name}.exists')
        ET.SubElement(observed, 'remove_value', name=f'$Object.$tm_empire_personnel_needs.${role}')
        operational.insert(1, observed)
    for parent in list(process.iter()):
        for node in list(parent):
            if node.tag != 'include_actions':
                continue
            ref = node.get('ref')
            role = {'md.InitUniverse.CreateTradeManagerEntity': 'trade',
                    'md.InitUniverse.CreateShipDealerEntity': 'shiptrade'}.get(ref)
            if role is None:
                continue
            index = list(parent).index(node)
            parent.remove(node)
            parent.insert(index, ET.Element('set_value',
                name=f'$Object.$tm_empire_personnel_needs.${role}',
                exact="table[$state='waiting', $reason='vacancy_requires_native_hire', $observed=player.age]"))
            for debug in list(parent):
                if debug.tag == 'debug_text' and 'restor' in debug.get('text', '').lower():
                    parent.remove(debug)
            for bookkeeping in list(parent):
                if bookkeeping.tag in ('set_value', 'remove_value') and bookkeeping.get('name') == '$controllable':
                    parent.remove(bookkeeping)
    for search in root.iter():
        if search.tag not in ('find_buy_offer', 'find_sell_offer'):
            continue
        match_tag = 'match_buyer' if search.tag == 'find_buy_offer' else 'match_seller'
        match = search.find(match_tag)
        if match is None:
            match = ET.SubElement(search, match_tag)
        match.set('tradesknownto', 'faction.player')


def adapt_buildstation_creation(root):
    if root.get('name') != 'TM_Empire_FactionSubgoal_BuildStation':
        return
    start = root.find("cues/cue[@name='Start']")
    branch = start.find(".//cue[@name='On_Phase_Change']/actions/do_elseif[@value=\"$Phase == 'build'\"]")
    assert branch is not None
    original = list(branch)
    branch.clear(); branch.set('value', "$Phase == 'build'")
    prepare = ET.SubElement(branch, 'do_if', value='not @$TM_BuildPrepared')
    post = []
    for node in original:
        if node.tag == 'create_station' or node.tag == 'add_build_to_expand_station':
            continue
        if node.tag == 'generate_loadout' or (node.tag == 'do_all' and node.get('exact') == '$Loadouts.count') or (node.tag == 'remove_value' and node.get('name') == '$Loadouts'):
            prepare.append(node)
        else:
            post.append(node)
    ET.SubElement(prepare, 'set_value', name='$TM_BuildPrepared', exact='true')
    timer = ET.SubElement(start.find('cues'), 'cue', name='TM_BuildStationProgress', checkinterval='15s')
    conditions = ET.SubElement(timer, 'conditions')
    ET.SubElement(conditions, 'check_value', value="$Phase == 'build' and @$TM_BuildPrepared and not @$TM_BuildAccepted")
    ET.SubElement(timer, 'delay', exact='15s')
    actions = ET.SubElement(timer, 'actions')
    restart_validation = ET.SubElement(actions, 'do_if', value="@$TM_BuildPlanKey and not @$tm_empire_station_creation and @md.TM_Empire_Construction.Request.$Receipt.$key == $TM_BuildPlanKey and md.TM_Empire_Construction.Request.$Receipt.$state == 'abandoned_before_effect'")
    ET.SubElement(restart_validation, 'remove_value', name='$TM_BuildPlanKey')
    def call(parent, ref, parameters, result):
        node = ET.SubElement(parent, 'run_actions', ref='md.TM_Empire_Construction.' + ref, result=result)
        for name, value in [('ManagerCue', '$TM_ManagerCue'), ('GoalCue', 'namespace'), *parameters]:
            ET.SubElement(node, 'param', name=name, value=value)
        return node
    missing = ET.SubElement(actions, 'do_if', value='not @$TM_BuildPlanKey')
    call(missing, 'RequestPlanValidation', [('Sequence', '$ConstructionPlan')], '$TM_PlanResult')
    accepted = ET.SubElement(missing, 'do_if', value='@md.TM_Empire_Construction.Request.$Receipt.$key == $TM_PlanResult')
    ET.SubElement(accepted, 'set_value', name='$TM_BuildPlanKey', exact='$TM_PlanResult')
    ET.SubElement(missing, 'set_value', name='$TM_BuildReason', exact='$TM_PlanResult')
    ready = ET.SubElement(actions, 'do_if', value='@$TM_BuildPlanKey')
    call(ready, 'CreateValidatedNativeStation', [('PlanKey', '$TM_BuildPlanKey'), ('Sector', '$Target'),
         ('Position', '$Position'), ('Macro', '$StationMacro'), ('RawName', '$StationRawName'), ('Budget', 'player.money')], '$TM_Creation')
    ET.SubElement(ready, 'set_value', name='$TM_BuildReason', exact='@$TM_Creation.$reason')
    created = ET.SubElement(ready, 'do_if', value='@$TM_Creation.$station.exists')
    ET.SubElement(created, 'set_value', name='$Station', exact='$TM_Creation.$station')
    ET.SubElement(created, 'set_value', name='$RegistryTable.$Station', exact='$Station')
    call(created, 'StepCreatedNativeStation', [], '$TM_Creation')
    ET.SubElement(created, 'set_value', name='$TM_BuildReason', exact='$TM_Creation.$reason')
    adopted = ET.SubElement(created, 'do_if', value="$TM_Creation.$state == 'adopted'")
    ET.SubElement(adopted, 'set_value', name='$BuildID', exact='$TM_Creation.$build')
    ET.SubElement(adopted, 'set_value', name='$TM_BuildAccepted', exact='true')
    adopted.extend(post)
    waiting = ET.SubElement(actions, 'do_if', value='not @$TM_BuildAccepted')
    ET.SubElement(waiting, 'reset_cue', cue='this')
    evaluation = start.find(".//cue[@name='Evaluate']/actions/do_else")
    stock = list(evaluation)
    for node in stock:
        evaluation.remove(node)
    waiting = ET.SubElement(evaluation, 'do_if', value='@$TM_BuildPrepared and not @$TM_BuildAccepted')
    ET.SubElement(waiting, 'set_value', name='$EvaluationResult', exact="'preparing'")
    otherwise = ET.SubElement(evaluation, 'do_else'); otherwise.extend(stock)


def adapt_finalise_plan_generation(root):
    if root.get('name') != 'TM_Empire_FinaliseStations':
        return
    # A dynamically selected factory can contain production without storage.
    # Reuse the economy's native sizing operation before native layout generation,
    # including storage already supplied by the selection/base plan.
    library = root.find(".//library[@name='NewStation_GenerateFactory']")
    branch = library.find('actions/do_else')
    anchor = next(i for i, node in enumerate(branch)
                  if node.get('name') == '$DebugFileName')
    storage = ET.Element('do_if', value='$PlannedModules.count')
    ET.SubElement(storage, 'set_value', name='$TM_FactoryProductions', exact='[]')
    ET.SubElement(storage, 'set_value', name='$TM_FactoryStorage', exact='[]')
    scan = ET.SubElement(storage, 'do_for_each', name='$TM_FactoryMacro', **{'in': '$PlannedModules'})
    production = ET.SubElement(scan, 'do_if', value='$TM_FactoryMacro.isclass.production')
    ET.SubElement(production, 'append_to_list', name='$TM_FactoryProductions', exact='$TM_FactoryMacro')
    existing = ET.SubElement(scan, 'do_elseif', value='$TM_FactoryMacro.isclass.storage')
    ET.SubElement(existing, 'append_to_list', name='$TM_FactoryStorage', exact='$TM_FactoryMacro')
    needed = ET.SubElement(storage, 'do_if', value='$TM_FactoryProductions.count')
    ET.SubElement(needed, 'get_module_definition', macro='$TM_FactoryStorageCandidates',
                  faction=native_catalog_factions()[0], tags='[tag.storage, tag.module]',
                  set='$ModuleSet', multiple='true')
    ET.SubElement(needed, 'get_suitable_storage_modules', result='$TM_FactoryAdditionalStorage',
                  production='$TM_FactoryProductions', storage='$TM_FactoryStorage',
                  macros='$TM_FactoryStorageCandidates')
    append = ET.SubElement(needed, 'do_for_each', name='$TM_FactoryStorageMacro',
                           **{'in': '$TM_FactoryAdditionalStorage'})
    ET.SubElement(append, 'append_to_list', name='$PlannedModules', exact='$TM_FactoryStorageMacro')
    ET.SubElement(append, 'append_to_list', name='$NewPlannedModules', exact='$TM_FactoryStorageMacro')
    branch.insert(anchor, storage)
    # The private generator supplies native layout and equipment only. Neither
    # AddBuild branch is allowed to turn that layout into player property.
    # Callers must consume 'prepared' through the paid construction adapter;
    # preserving 'finished' here would falsely acknowledge an actual build.
    completed = root.find(".//cue[@name='NewStation_ConstructionSequenceCompleted']/actions")
    assert completed is not None
    # The stock setup equipment table is read-only catalogue data, not copied
    # manager state. The isolated table was never initialized. Obtain the same
    # list through setup.xml's native operation and a single native faction.
    equipment = completed.find(".//do_if[@value='md.$TM_Empire_EquipmentTable']")
    assert equipment is not None
    equipment_parent = next(parent for parent in completed.iter() if equipment in list(parent))
    equipment_index = list(equipment_parent).index(equipment)
    equipment_parent.remove(equipment)
    equipment_parent.insert(equipment_index, ET.Element('get_ware_definition',
        result='$PossibleWares', flags='equipment',
        faction=native_factory_catalog_faction('$Station.owner')))
    for parent in list(completed.iter()):
        children = list(parent)
        for index, node in enumerate(children):
            if node.tag == 'do_if' and node.get('value') == '$AddBuild':
                assert node.find('add_build_to_expand_station') is not None
                alternate = children[index + 1]
                assert alternate.tag == 'do_else' and alternate.find('apply_construction_sequence') is not None
                parent.remove(node)
                parent.remove(alternate)
    reports = completed.findall('.//signal_cue_instantly')
    assert len(reports) == 1
    reports[0].set('param', "['prepared', $ConstructionSequence, null, $Station]")


def adapt_mission_minefields(root):
    if root.get('name') != 'TM_Empire_FactionLogic':
        return
    replaced = 0
    for parent in list(root.iter()):
        children = list(parent)
        for index, node in enumerate(children):
            if node.tag != 'do_if' or node.get('value') != '$MineType == 0':
                continue
            assert node.find("run_actions[@ref='md.LIB_Generic.PlaceRiggedAsteroids']") is not None
            ordinary = children[index + 1]
            assert ordinary.tag == 'do_else'
            position = list(parent).index(node)
            parent.remove(node)
            parent.remove(ordinary)
            for offset, action in enumerate(list(ordinary)):
                parent.insert(position + offset, action)
            replaced += 1
    assert replaced == 1
    # Keep the native sector/position choice and field strategy. Mission-only
    # asteroid selections now request the same deployable mine strategy used
    # by the generic native branch, rather than creating mission objects.
    for node in root.iter('set_value'):
        if node.get('name') == '$MineType' and node.get('exact') == '0':
            node.set('exact', '1')
            node.set('comment', 'Native deployable mines replace mission-only rigged asteroids')


def remove_native_debug_beacons(root):
    references = {'md.LIB_Generic.DebugPositions_AddBeacon',
                  'md.LIB_Generic.DebugPositions_DestroyAllBeacons'}
    for parent in list(root.iter()):
        for node in list(parent):
            if node.tag != 'run_actions' or node.get('ref') not in references:
                continue
            index = list(parent).index(node)
            parent.remove(node)
            if node.get('result'):
                parent.insert(index, ET.Element('set_value', name=node.get('result'), exact='null'))


def adapt_native_cleanup(root):
    if root.get('name') == 'TM_Empire_Job_Helper':
        # Эти библиотеки изменяют глобальные NPC jobs, не состав живых
        # флотов игрока. В private closure нет вызывающего их checker.
        for library in list(root.find('cues')):
            if library.get('name') in ('Fleet_Evolution', 'Fleet_Evolution_Conditions__Standard'):
                root.find('cues').remove(library)
    if root.get('name') == 'TM_Empire_FactionGoal_Invade_Space':
        evaluation = root.find("cues/library[@name='EvaluateSector']/actions")
        if evaluation is None:
            raise ValueError('native invasion sector evaluation boundary missing')
        visible = ET.Element('do_if', value='not $Sector.exists or not $Sector.isknown')
        ET.SubElement(visible, 'return', value='false')
        evaluation.insert(0, visible)
        start_conditions = root.find("cues/cue[@name='Start']/conditions")
        if start_conditions is None:
            raise ValueError('native invasion start boundary missing')
        ET.SubElement(start_conditions, 'check_value',
                      value='@event.param.$Target.exists and event.param.$Target.isknown')
        for parent in root.iter():
            for node in list(parent):
                if node.tag == 'get_suitable_job' and node.get('result') == '$ExpeditionJob':
                    index = list(parent).index(node)
                    parent.remove(node)
                    parent.insert(index, ET.Element('find_ship_by_true_owner', name='$ExpeditionJob', faction='faction.player', space='player.galaxy', primarypurpose='purpose.fight', known='true', checkoperational='true'))
                elif node.tag == 'set_value' and node.get('name') == '$FindMilitaryShipTags' and node.get('exact') == '[tag.expedition]':
                    node.set('exact', '[tag.military]')
    for parent in list(root.iter()):
        for node in list(parent):
            if node.tag == 'cue' and node.get('name', '').startswith('Debug_'):
                parent.remove(node)
    if root.get('name') == 'TM_Empire_FactionLogic_Economy':
        removal = root.find(".//cue[@name='Remove_Factory']")
        if removal is not None:
            actions = removal.find('actions')
            # Сохранить исходные критерии выбора, но заменить эвакуацию,
            # убийство персонала и отмену чужой строительной очереди.
            prefix = []
            for node in list(actions):
                if node.tag == 'do_if' and node.get('value') == '$Station.exists':
                    break
                prefix.append(node)
            actions.clear()
            actions.extend(prefix)
            ET.SubElement(actions, 'set_value', name='$TM_ManagerCue', exact='parent.$FactionManagerCue')
            ET.SubElement(actions, 'set_value', name='$ActionDefinition.$RequestGoal', exact='namespace')
            ET.SubElement(actions, 'set_value', name='$ActionDefinition.$Station', exact='$Station')
            children = removal.find('cues')
            if children is not None:
                removal.remove(children)
            children = ET.SubElement(removal, 'cues')
            tick = ET.SubElement(children, 'cue', name='TM_RecyclingTick', checkinterval='30s')
            ET.SubElement(ET.SubElement(tick, 'conditions'), 'check_value', value='$Station.exists or @$tm_empire_recycling')
            ET.SubElement(tick, 'delay', exact='30s')
            steps = ET.SubElement(tick, 'actions')
            call = ET.SubElement(steps, 'run_actions', ref='md.TM_Empire_Recycling.StepFactoryRecycling', result='this.$Result')
            for name, value in [('ManagerCue', '$TM_ManagerCue'), ('GoalCue', 'namespace'), ('Station', '$Station')]:
                ET.SubElement(call, 'param', name=name, value=value)
            ET.SubElement(steps, 'set_value', name='$ActionDefinition.$TM_RecyclingState', exact='this.$Result.$state')
            ET.SubElement(steps, 'set_value', name='$ActionDefinition.$WaitReason', exact='@this.$Result.$reason')
            completed = ET.SubElement(steps, 'do_if', value="this.$Result.$state == 'observed'")
            ET.SubElement(completed, 'set_value', name='$ActionDefinition.$RecycleEndTime', exact='player.age')
            ET.SubElement(completed, 'cancel_cue', cue='namespace')
            repeating = ET.SubElement(steps, 'do_else')
            ET.SubElement(repeating, 'reset_cue', cue='this')
    if root.get('name') == 'TM_Empire_FactionLogic':
        prefab = root.find(".//cue[@name='ExpandPrefabs']/actions")
        if prefab is not None:
            branch = prefab.find("do_if[@value='this.$SelectedPrefab']")
            override = ET.Element('do_if', value='@$tm_empire_prefab_expansion')
            ET.SubElement(override, 'set_value', name='this.$SelectedPrefab', exact='$tm_empire_prefab_expansion.$station')
            prefab.insert(list(prefab).index(branch), override)
            direct = branch.find('add_build_to_expand_station')
            index = list(branch).index(direct)
            branch.remove(direct)
            call = ET.Element('run_actions', ref='md.TM_Empire_Construction.StepPrefabExpansion', result='this.$PrefabResult')
            for name, value in [('ManagerCue', 'namespace'), ('GoalCue', 'namespace'), ('Station', 'this.$SelectedPrefab'), ('Sequence', 'this.$ConstructionPlan.finalsequence'), ('Stage', 'this.$ConstructionPlan.stage.current + 1'), ('Budget', 'player.money')]:
                ET.SubElement(call, 'param', name=name, value=value)
            branch.insert(index, call)
            branch.insert(index + 1, ET.Element('set_value', name='$TM_PrefabReason', exact="this.$PrefabResult.$state + ': ' + @this.$PrefabResult.$reason"))
            timer = branch.find("set_value[@name='$NextPrefabExpansionTime']")
            branch.remove(timer)
            queued = ET.SubElement(branch, 'do_if', value="this.$PrefabResult.$state == 'queued'")
            queued.append(timer)
            waiting = ET.SubElement(branch, 'do_else')
            ET.SubElement(waiting, 'set_value', name='$NextPrefabExpansionTime', exact='player.age + 1min')
        network = root.find(".//cue[@name='MaintainSatelliteNetwork_PeriodicCheck']/actions")
        if network is not None:
            network.clear()
            prepared = ET.fromstring('''<actions>
              <set_value name="$TM_ManagerCue" exact="namespace"/>
              <do_if value="@$TM_SatelliteSupplyKey">
                <run_actions ref="md.TM_Empire_Supply.StepRestockDelivery" result="this.$Supply"><param name="Key" value="$TM_SatelliteSupplyKey"/><param name="ManagerCue" value="namespace"/><param name="GoalCue" value="namespace"/></run_actions>
                <set_value name="$TM_SatelliteReason" exact="'satellite_supply_' + this.$Supply.$state + ': ' + @this.$Supply.$reason"/>
                <do_if value="this.$Supply.$state == 'consumed'"><remove_value name="$TM_SatelliteSupplyKey"/></do_if>
              </do_if>
              <do_if value="@$TM_SatellitePending">
                <set_value name="this.$Deployment" exact="@$TM_SatellitePending.$ship.$tm_empire_satellite_receipt"/>
                <do_if value="@this.$Deployment.$order == $TM_SatellitePending.$order and @this.$Deployment.$manager == namespace and @this.$Deployment.$state == 'observed' and @this.$Deployment.$satellite.exists and this.$Deployment.$satellite.isplayerowned">
                  <add_to_group groupname="$FactionSatellites" object="this.$Deployment.$satellite"/>
                  <do_if value="not @$TM_SatellitePending.$ship.$tm_empire_claim"><remove_value name="$TM_SatellitePending"/><set_value name="$TM_SatelliteReason" exact="'native_satellite_observed_claim_already_released'"/></do_if>
                  <do_else>
                    <run_actions ref="md.TM_Empire_Runtime.StopAndReleaseOwnedShip" result="$TM_SatelliteReason"><param name="Ship" value="$TM_SatellitePending.$ship"/><param name="ManagerCue" value="namespace"/><param name="GoalCue" value="namespace"/></run_actions>
                    <do_if value="$TM_SatelliteReason == 'released'"><remove_value name="$TM_SatellitePending"/></do_if>
                  </do_else>
                </do_if>
                <do_elseif value="not $TM_SatellitePending.$order.exists"><set_value name="$TM_SatellitePending.$state" exact="'unknown'"/><set_value name="$TM_SatelliteReason" exact="'native_satellite_delivery_unconfirmed'"/></do_elseif>
              </do_if>
              <do_elseif value="$FactionSatellites.count lt $SatelliteNetworkGoal and $ClaimedSectors.count">
                <set_value name="this.$Sector" exact="$ClaimedSectors.random"/>
                <do_if value="this.$Sector.isknown">
                  <set_value name="this.$Target" exact="null"/>
                  <do_any>
                    <find_station_by_true_owner name="this.$Target" faction="faction.player" space="this.$Sector" known="true"/>
                    <do_all>
                      <run_actions ref="md.LIB_Generic.FindSectorEntryPoints" result="this.$EntryPoints"><param name="Sector" value="this.$Sector"/></run_actions>
                      <shuffle_list list="this.$EntryPoints"/>
                      <do_all exact="[this.$EntryPoints.count, 16].min" counter="this.$entry_i">
                        <do_if value="this.$EntryPoints.{this.$entry_i}.exists and this.$EntryPoints.{this.$entry_i}.isknown and this.$EntryPoints.{this.$entry_i}.sector == this.$Sector"><set_value name="this.$Target" exact="this.$EntryPoints.{this.$entry_i}"/><break/></do_if>
                      </do_all>
                    </do_all>
                  </do_any>
                  <do_if value="this.$Target.exists">
                    <create_position name="this.$Position" object="this.$Target" space="this.$Sector" max="15km"/>
                    <find_ship_by_true_owner name="this.$Candidates" faction="faction.player" space="player.galaxy" multiple="true" checkoperational="true"/>
                    <do_if value="not @$TM_SatelliteCandidateCursor or $TM_SatelliteCandidateCursor gt this.$Candidates.count"><set_value name="$TM_SatelliteCandidateCursor" exact="1"/></do_if>
                    <do_all exact="[this.$Candidates.count, 32].min" counter="this.$i">
                      <set_value name="this.$Ship" exact="this.$Candidates.{$TM_SatelliteCandidateCursor}"/>
                      <set_value name="$TM_SatelliteCandidateCursor" operation="add"/>
                      <do_if value="$TM_SatelliteCandidateCursor gt this.$Candidates.count"><set_value name="$TM_SatelliteCandidateCursor" exact="1"/></do_if>
                      <set_value name="this.$Macro" exact="if this.$Ship.ammostorage.{macro.eq_arg_satellite_02_macro}.count then macro.eq_arg_satellite_02_macro else macro.eq_arg_satellite_01_macro"/>
                      <do_if value="this.$Ship.ammostorage.{this.$Macro}.count and not @$TM_SatellitePending">
                        <create_order name="this.$Order" object="this.$Ship" id="'TM_DeployObjectAtPosition'"><param name="destination" value="[this.$Sector, this.$Position]"/><param name="objectstodeploy" value="[this.$Macro]"/><param name="amountstodeploy" value="[1]"/></create_order>
                        <do_if value="this.$Order.exists"><set_value name="$TM_SatellitePending" exact="table[$state='sent', $ship=this.$Ship, $order=this.$Order, $sector=this.$Sector, $macro=this.$Macro, $issued=player.age]"/><set_value name="$TM_SatelliteReason" exact="'native_inventory_deployment_sent'"/><break/></do_if>
                      </do_if>
                      <do_elseif value="not @$TM_SatelliteSupplyKey and this.$Ship.ammostorage.deployable.capacity gt this.$Ship.ammostorage.deployable.count">
                        <run_actions ref="md.TM_Empire_Runtime.CanUseOwnedShip" result="this.$Available"><param name="Ship" value="this.$Ship"/><param name="ManagerCue" value="namespace"/><param name="GoalCue" value="namespace"/></run_actions>
                        <do_if value="this.$Available == 'available'">
                          <find_station name="this.$Supplier" space="player.galaxy" canequipclass="this.$Ship.class" canbuildfor="faction.player" hascontrolentity="controlpost.shiptrader" knownto="faction.player"/>
                          <do_if value="this.$Supplier.exists">
                            <run_actions ref="md.TM_Empire_Supply.QuoteRestock" result="this.$SupplyKey"><param name="ManagerCue" value="namespace"/><param name="GoalCue" value="namespace"/><param name="Ship" value="this.$Ship"/><param name="Builder" value="this.$Supplier"/><param name="Macro" value="macro.eq_arg_satellite_01_macro"/><param name="Amount" value="1"/><param name="Budget" value="player.money"/></run_actions>
                            <do_if value="@md.TM_Empire_Supply.Request.$Receipt.$key == this.$SupplyKey"><set_value name="$TM_SatelliteSupplyKey" exact="this.$SupplyKey"/><set_value name="$TM_SatelliteReason" exact="'satellite_supply_quote_requested'"/><break/></do_if>
                          </do_if>
                        </do_if>
                      </do_elseif>
                    </do_all>
                    <do_if value="not @$TM_SatellitePending and not @$TM_SatelliteSupplyKey"><set_value name="$TM_SatelliteReason" exact="'owned_idle_ship_with_satellite_required'"/></do_if>
                  </do_if>
                </do_if>
              </do_elseif>
            </actions>''')
            # Нативный выбор новой сетевой задачи остаётся раз в 1800s;
            # уже выданная доставка наблюдается отдельно каждые 15s.
            supply_step = prepared.find('do_if')
            prepared.remove(supply_step)
            network.extend(list(prepared))
            network_cues = root.find(".//cue[@name='MaintainSatelliteNetwork']/cues")
            progress = ET.SubElement(network_cues, 'cue', name='TM_SatelliteSupplyProgress', checkinterval='15s', instantiate='true')
            conditions = ET.SubElement(progress, 'conditions')
            ET.SubElement(conditions, 'check_value', value='@$TM_SatelliteSupplyKey')
            actions = ET.SubElement(progress, 'actions')
            actions.append(supply_step)
    for parent in list(root.iter()):
        for node in list(parent):
            if node.tag != 'destroy_object':
                continue
            index = list(parent).index(node)
            parent.remove(node)
            if root.get('name') == 'TM_Empire_FactionSubgoal_Recon':
                release = ET.Element('run_actions', ref='md.TM_Empire_Runtime.StopAndReleaseOwnedShip', result='$TM_ReleaseReason')
                for name, value in [('Ship', node.get('object')), ('ManagerCue', '$TM_ManagerCue'), ('GoalCue', 'namespace')]:
                    ET.SubElement(release, 'param', name=name, value=value)
                parent.insert(index, release)
            else:
                parent.insert(index, ET.Element('set_value', name='$TM_CleanupReason', exact="'native_goal_cleanup_retained_actual_property'"))


def adapt_station_plan_requests(root):
    if root.get('name') != 'TM_Empire_FactionLogic_Stations':
        return
    manager = root.find("cues/library[@name='Manage_Stations']")
    location = manager.find(".//library[@name='Find_Location_And_Build_Station']")
    actions = location.find('actions')
    initial = ET.Element('do_if', value='not @$tm_empire_station_requests')
    ET.SubElement(initial, 'set_value', name='$tm_empire_station_requests', exact='table[]')
    actions.insert(0, initial)
    pending = ET.Element('do_if', value='@$tm_empire_station_requests.{$ExistingStationValName}')
    observed = ET.SubElement(pending, 'do_if', value="@$tm_empire_station_requests.{$ExistingStationValName}.$station.exists and @ $tm_empire_station_requests.{$ExistingStationValName}.$state == 'adopted'")
    ET.SubElement(observed, 'remove_value', name='$tm_empire_station_requests.{$ExistingStationValName}')
    waiting = ET.SubElement(pending, 'do_else')
    ET.SubElement(waiting, 'return', value='[]')
    actions.insert(1, pending)
    for parent in list(actions.iter()):
        for node in list(parent):
            if node.tag == 'do_if' and node.get('value') == '@$GodEntryIDTable.{$ChosenSector}.count':
                siblings = list(parent)
                index = siblings.index(node)
                fallback = siblings[index + 1]
                assert fallback.tag == 'do_else'
                parent.remove(node); parent.remove(fallback)
                fallback.tag = 'do_all'
                parent.insert(index, fallback)
            elif node.tag == 'create_station':
                index = list(parent).index(node)
                parent.remove(node)
                if node.get('macro') == '$SelectedDefinition':
                    parent.insert(index, ET.Element('set_value', name='$TM_StationReason', exact="'station_definition_requires_construction_plan'"))
                    continue
                gate = ET.Element('do_if', value='not @$tm_empire_station_requests.{$ExistingStationValName}')
                parent.insert(index, gate)
                if node.get('zone'):
                    ET.SubElement(gate, 'create_position', name='$TM_StationPosition', object='$SpawnZone', space='$ChosenSector', x='$Position.x', y='$Position.y', z='$Position.z')
                else:
                    ET.SubElement(gate, 'set_value', name='$TM_StationPosition', exact='$Position')
                ET.SubElement(gate, 'set_value', name='$TM_StationRequest', exact="table[$manager=$TM_ManagerCue, $type=$ExistingStationValName, $sector=$ChosenSector, $position=$TM_StationPosition, $sequence=$SelectedDefinition.{1}, $rawname=$SelectedDefinition.{2}, $alternatives=$StationDefinitions.clone, $macro=$ModuleSetMacro, $loadout=$LoadoutLevel, $state='requested', $issued=player.age]")
                ET.SubElement(gate, 'set_value', name='$tm_empire_station_requests.{$ExistingStationValName}', exact='$TM_StationRequest')
                ET.SubElement(gate, 'signal_cue_instantly', cue='TM_StationBuildRequest', param='$TM_StationRequest')
            elif node.tag == 'do_if' and node.get('value') == '$NewStation and $IsConstructionPlanStation':
                parent.remove(node)
    request = ET.SubElement(manager.find('cues'), 'cue', name='TM_StationBuildRequest', instantiate='true', namespace='this')
    conditions = ET.SubElement(request, 'conditions')
    ET.SubElement(conditions, 'event_cue_signalled')
    init = ET.SubElement(request, 'actions')
    ET.SubElement(init, 'set_value', name='$Request', exact='event.param')
    ET.SubElement(init, 'set_value', name='$TM_ManagerCue', exact='$Request.$manager')
    ET.SubElement(init, 'set_value', name='$Request.$goal', exact='namespace')
    ET.SubElement(init, 'set_value', name='$CandidateIndex', exact='0')
    ET.SubElement(init, 'set_value', name='$CandidateCursor', exact='1')
    timer = ET.SubElement(ET.SubElement(request, 'cues'), 'cue', name='TM_StationBuildProgress', checkinterval='15s')
    ET.SubElement(timer, 'delay', exact='15s')
    tick = ET.SubElement(timer, 'actions')
    candidates = ET.SubElement(tick, 'do_if', value='not @$CandidateReady and (not @$NextCandidateAttempt or player.age ge $NextCandidateAttempt)')
    page = ET.SubElement(candidates, 'run_actions', ref='md.TM_Empire_Construction.ReadPlanPage', result='$CandidatePage')
    for name, value in [('Sequence', '$Request.$sequence'), ('Start', '$CandidateCursor'), ('ModulesOnly', 'true')]:
        ET.SubElement(page, 'param', name=name, value=value)
    good = ET.SubElement(candidates, 'do_if', value="$CandidatePage.$state == 'page_observed'")
    complete = ET.SubElement(good, 'do_if', value='$CandidatePage.$to == $CandidatePage.$total')
    ET.SubElement(complete, 'set_value', name='$CandidateReady', exact='true')
    ET.SubElement(complete, 'generate_loadout', sequence='$Request.$sequence', level='$Request.$loadout', result='$Loadouts', faction='faction.player')
    loadouts = ET.SubElement(complete, 'do_all', exact='$Loadouts.count', counter='$l')
    ET.SubElement(loadouts, 'apply_loadout', sequence='$Request.$sequence', index='$l', loadout='$Loadouts.{$l}')
    more = ET.SubElement(good, 'do_else')
    ET.SubElement(more, 'set_value', name='$CandidateCursor', exact='$CandidatePage.$next')
    unavailable = ET.SubElement(candidates, 'do_else')
    ET.SubElement(unavailable, 'set_value', name='$CandidateIndex', operation='add')
    exhausted = ET.SubElement(unavailable, 'do_if', value='$CandidateIndex gt $Request.$alternatives.count')
    ET.SubElement(exhausted, 'set_value', name='$CandidateIndex', exact='1')
    ET.SubElement(exhausted, 'set_value', name='$NextCandidateAttempt', exact='player.age + 1min')
    ET.SubElement(unavailable, 'set_value', name='$Request.$sequence', exact='$Request.$alternatives.{$CandidateIndex}.{1}')
    ET.SubElement(unavailable, 'set_value', name='$Request.$rawname', exact='$Request.$alternatives.{$CandidateIndex}.{2}')
    ET.SubElement(unavailable, 'set_value', name='$CandidateCursor', exact='1')
    ET.SubElement(candidates, 'set_value', name='$Reason', exact='$CandidatePage.$reason')
    def call(parent, ref, parameters, result):
        node = ET.SubElement(parent, 'run_actions', ref='md.TM_Empire_Construction.' + ref, result=result)
        for name, value in [('ManagerCue', '$TM_ManagerCue'), ('GoalCue', 'namespace'), *parameters]:
            ET.SubElement(node, 'param', name=name, value=value)
    missing = ET.SubElement(tick, 'do_if', value='@$CandidateReady and not @$PlanKey')
    call(missing, 'RequestPlanValidation', [('Sequence', '$Request.$sequence')], '$Reason')
    accepted = ET.SubElement(missing, 'do_if', value='@md.TM_Empire_Construction.Request.$Receipt.$key == $Reason and @md.TM_Empire_Construction.Request.$Receipt.$goal == namespace')
    ET.SubElement(accepted, 'set_value', name='$PlanKey', exact='$Reason')
    ready = ET.SubElement(tick, 'do_if', value='@$PlanKey')
    call(ready, 'CreateValidatedNativeStation', [('PlanKey', '$PlanKey'), ('Sector', '$Request.$sector'), ('Position', '$Request.$position'), ('Macro', '$Request.$macro'), ('RawName', '$Request.$rawname'), ('Budget', 'player.money')], '$Creation')
    ET.SubElement(ready, 'set_value', name='$Request.$state', exact='$Creation.$state')
    ET.SubElement(ready, 'set_value', name='$Reason', exact='$Creation.$reason')
    created = ET.SubElement(ready, 'do_if', value='@$Creation.$station.exists')
    ET.SubElement(created, 'set_value', name='$Request.$station', exact='$Creation.$station')
    call(created, 'StepCreatedNativeStation', [], '$Creation')
    ET.SubElement(created, 'set_value', name='$Request.$state', exact='$Creation.$state')
    ET.SubElement(created, 'set_value', name='$Reason', exact='$Creation.$reason')
    ET.SubElement(tick, 'set_value', name='$Request.$reason', exact='@$Reason')
    retry = ET.SubElement(tick, 'do_if', value="$Request.$state != 'adopted' and $Request.$state != 'unknown'")
    ET.SubElement(retry, 'reset_cue', cue='this')


def adapt_sector_factory_requests(root):
    if root.get('name') == 'TM_Empire_FactionLogic_Economy':
        manager = root.find("cues/library[@name='Econ_Manager']")
        ET.SubElement(manager.find('actions'), 'set_value', name='$FactionManagerCue.$tm_empire_economy_cue', exact='namespace')
        ET.SubElement(manager.find('actions'), 'set_value', name='$FactionManagerCue.$tm_empire_factory_receiver', exact='TM_RequestSectorFactory')
        registration = ET.SubElement(manager.find('cues'), 'cue', name='TM_RegisterFactoryReceiver', instantiate='true')
        registration_conditions = ET.SubElement(registration, 'conditions')
        ET.SubElement(registration_conditions, 'event_game_loaded')
        ET.SubElement(registration, 'delay', exact='5s')
        registration_actions = ET.SubElement(registration, 'actions')
        ET.SubElement(registration_actions, 'do_if', value='$FactionManagerCue.exists')
        ET.SubElement(registration_actions[0], 'set_value', name='$FactionManagerCue.$tm_empire_factory_receiver', exact='TM_RequestSectorFactory')
        receiver = ET.SubElement(manager.find('cues'), 'cue', name='TM_RequestSectorFactory', instantiate='true')
        conditions = ET.SubElement(receiver, 'conditions')
        ET.SubElement(conditions, 'event_cue_signalled')
        ET.SubElement(conditions, 'check_value', value='@event.param.$manager == $FactionManagerCue and @event.param.$goal.exists and @event.param.$sector.isknown')
        actions = ET.SubElement(receiver, 'actions')
        ET.SubElement(actions, 'set_value', name='this.$Sector', exact='event.param.$sector')
        ET.SubElement(actions, 'set_value', name='this.$Ware', exact='event.param.$ware')
        outer = ET.SubElement(actions, 'do_if', value='not @$tm_empire_sector_factory_requests')
        ET.SubElement(outer, 'set_value', name='$tm_empire_sector_factory_requests', exact='table[]')
        initialise = ET.SubElement(actions, 'do_if', value='not @$tm_empire_sector_factory_requests.{this.$Sector}')
        ET.SubElement(initialise, 'set_value', name='$tm_empire_sector_factory_requests.{this.$Sector}', exact='table[]')
        ET.SubElement(actions, 'set_value', name='this.$Previous', exact='@$tm_empire_sector_factory_requests.{this.$Sector}.{this.$Ware}')
        available = ET.SubElement(actions, 'do_if', value='not this.$Previous or (not @this.$Previous.$Station.exists and @this.$Previous.$RequestedAt + 5min lt player.age and (not @this.$Previous.$RequestGoal.exists or @this.$Previous.$RequestGoal.$tm_empire_cancelled))')
        ET.SubElement(available, 'set_value', name='this.$Action', exact="table[$Type='$request_factory', $RequestedAt=player.age, $Reason='native_holdspace_factory_requirement']")
        ET.SubElement(available, 'set_value', name='$tm_empire_sector_factory_requests.{this.$Sector}.{this.$Ware}', exact='this.$Action')
        ET.SubElement(available, 'signal_cue_instantly', cue='Request_Factory', param='[this.$Action, this.$Sector, this.$Ware, table[{0}=[this.$Sector]], null, @event.param.$limit]')
        request = manager.find("cues/cue[@name='Request_Factory']")
        actions = request.find('actions')
        index = next(i for i, node in enumerate(actions) if node.get('name') == '$ActionDefinition')
        actions.insert(index + 1, ET.Element('set_value', name='$ActionDefinition.$RequestGoal', exact='namespace'))
        for limit in actions.iter('set_value'):
            if limit.get('name') == '$ProductionLimit':
                limit.set('exact', 'if @event.param.{6} then event.param.{6} else (' + limit.get('exact') + ')')
    elif root.get('name') == 'TM_Empire_FactionGoal_Hold_Space':
        for parent in list(root.iter()):
            for node in list(parent):
                if node.tag == 'create_factory':
                    select = node.find('select')
                    index = list(parent).index(node)
                    parent.remove(node)
                    gate = ET.Element('do_if', value='@$TM_ManagerCue.$tm_empire_factory_receiver.exists')
                    parent.insert(index, ET.Element('set_value', name='$Station', exact='null'))
                    parent.insert(index + 1, gate)
                    ET.SubElement(gate, 'signal_cue_instantly', cue='$TM_ManagerCue.$tm_empire_factory_receiver', param=f'table[$manager=$TM_ManagerCue, $goal=namespace, $sector=$Target, $ware={select.get("ware")}, $limit=$ProductionLimit]')
                    # Не оставлять $Station от предыдущей итерации как успех.
                elif node.tag == 'signal_cue_instantly' and node.get('cue') == 'md.TM_Empire_FinaliseStations.NewStation_GenerateFactory_Signal':
                    parent.remove(node)
    elif root.get('name') == 'TM_Empire_FactionLogic':
        redeploy = root.find(".//cue[@name='RedeployJobShips']")
        if redeploy is None:
            raise ValueError('native NPC job redeployment boundary missing')
        branches = [node for node in redeploy.iter('do_if')
                    if node.get('value') == 'not $Ship.iscommandeered']
        if len(branches) != 1:
            raise ValueError('native NPC job redeployment guard ambiguous')
        # Player ships have no NPC job/main-sector/quota. Owned ships are
        # dispatched by the copied HoldSpace/DefendArea goals and shared claims.
        branches[0].set('value', '$Faction != faction.player and not $Ship.iscommandeered')


def adapt_factory_queue_handoff(root):
    """Reuse an orphaned factory only for the same native product/sector request."""
    if root.get('name') != 'TM_Empire_FactionLogic_Economy':
        return
    request = root.find(".//cue[@name='Request_Factory']")
    actions = request.find('actions')
    station_init = actions.find("set_value[@name='$Station']")
    assert station_init is not None and station_init.get('exact') == 'null'
    index = list(actions).index(station_init) + 1
    remaining = list(actions)[index:]
    for node in remaining:
        actions.remove(node)
    ET.SubElement(actions, 'set_value', name='$TM_OrphanQueue', exact='@md.TM_Empire_Construction.Expansion.$Receipt')
    candidate = ET.SubElement(actions, 'do_if', value="@$TM_OrphanQueue.$state == 'queued' and @$TM_OrphanQueue.$nativecreation and @$TM_OrphanQueue.$station.exists and $TM_OrphanQueue.$station.sector == $RequestSector and @global.$TM_EmpireComponentRecords.$creation.{$TM_OrphanQueue.$station}.$product == $Ware")
    ET.SubElement(candidate, 'set_value', name='$TM_ManagerCue', exact='parent.$FactionManagerCue')
    call = ET.SubElement(candidate, 'run_actions', ref='md.TM_Empire_Construction.ReconcileQueuedExpansionOwner', result='$TM_Handoff')
    for name, value in [('ManagerCue', '$TM_ManagerCue'), ('GoalCue', 'namespace'), ('Station', '$TM_OrphanQueue.$station')]:
        ET.SubElement(call, 'param', name=name, value=value)
    accepted = ET.SubElement(candidate, 'do_if', value='$TM_Handoff == $TM_OrphanQueue.$key')
    for name, value in [('$Station', '$TM_OrphanQueue.$station'), ('$IsPrefab', 'true'), ('$TM_PrefabPlan', '$TM_OrphanQueue.$sequence'), ('$TM_PrefabAccepted', 'true'), ('$TM_HandoffAccepted', 'true'), ('$ActionDefinition.$Station', '$Station'), ('$ActionDefinition.$SpawnTime', 'player.age'), ('$ActionDefinition.$TM_ConstructionState', "'queued'"), ('$ActionDefinition.$TM_ConstructionReason', "'native_construction_authority_reconciled'")]:
        ET.SubElement(accepted, 'set_value', name=name, exact=value)
    # No finalise or creation action after a verified adoption. Stock observers
    # continue to watch the same actual build; there is no second planner.
    fallback = ET.SubElement(actions, 'do_if', value='not @$TM_HandoffAccepted')
    fallback.extend(remaining)
    for node in request.iter('set_value'):
        if node.get('name') == '$tm_empire_factory_creation' and 'creation_sent' in node.get('exact', ''):
            node.set('exact', node.get('exact').replace('$issued=player.age', '$product=$Ware, $issued=player.age'))


def adapt_factory_prefab_creation(root):
    if root.get('name') != 'TM_Empire_FactionLogic_Economy':
        return
    request = root.find(".//cue[@name='Request_Factory']")
    prefab = request.find("actions//do_if[@value='$PrefabConstructionPlan']")
    assert prefab is not None
    prefab.clear()
    prefab.set('value', '$PrefabConstructionPlan')
    ET.SubElement(prefab, 'set_value', name='$IsPrefab', exact='true')
    ET.SubElement(prefab, 'set_value', name='$TM_PrefabPlan', exact='$PrefabConstructionPlan')
    ET.SubElement(prefab, 'set_value', name='$TM_ManagerCue', exact='parent.$FactionManagerCue')
    sector_placement = ET.SubElement(prefab, 'do_if', value='@$BuildInSector')
    ET.SubElement(sector_placement, 'set_value', name='$SectorCentre', exact='$RequestSector.coreposition')
    ET.SubElement(sector_placement, 'set_value', name='$SectorCoreSize', exact='$RequestSector.coresize / 2')
    ET.SubElement(sector_placement, 'set_value', name='$Yaw', min='0deg', max='360deg')
    ET.SubElement(sector_placement, 'set_value', name='$Y', min='$SectorCentre.y - 10km', max='$SectorCentre.y + 10km')
    ET.SubElement(sector_placement, 'set_value', name='$PlacementDist', min='0km', max='$SectorCoreSize', profile='bell', scale='2')
    ET.SubElement(sector_placement, 'create_position', name='$TM_PrefabPosition', x='$SectorCentre.x + sin($Yaw) * $PlacementDist', y='$Y', z='$SectorCentre.z + cos($Yaw) * $PlacementDist')
    zone_placement = ET.SubElement(prefab, 'do_else')
    ET.SubElement(zone_placement, 'create_position', name='$TM_PrefabPosition', object='$Zone', space='$RequestSector', max='40km', y='0m')
    # Ожидание валидации не означает отсутствие подходящей фабрики.
    # do_else — сосед do_if, а не его ребёнок.
    for node in request.find('actions'):
        if node.tag == 'do_else' and node.find("cancel_cue[@cue='Request_Factory']") is not None:
            cancellation = node.find('cancel_cue')
            node.remove(cancellation)
            waiting = ET.SubElement(node, 'do_if', value='not @$TM_PrefabPlan')
            waiting.append(cancellation)
    finalise = request.find("cues/cue[@name='Request_Factory_Finalise']")
    # Cue с ref допускает только param. Условие ставится на обычную
    # обёртку, а библиотека остаётся неизменным дочерним вызовом.
    children = request.find('cues')
    index = list(children).index(finalise)
    children.remove(finalise)
    wrapper = ET.Element('cue', name='Request_Factory_Finalise', checkinterval='1s')
    children.insert(index, wrapper)
    conditions = ET.SubElement(wrapper, 'conditions')
    ET.SubElement(conditions, 'check_value', value='$Station.exists and not @$TM_PrefabPlan')
    finalise.set('name', 'TM_GeneratedFactoryFinalise')
    ET.SubElement(wrapper, 'cues').append(finalise)
    observers = ET.SubElement(children, 'cue', name='TM_FactoryStationObservers', checkinterval='1s')
    conditions = ET.SubElement(observers, 'conditions')
    ET.SubElement(conditions, 'check_value', value='$Station.exists')
    observed_children = ET.SubElement(observers, 'cues')
    for name in ('Request_Factory_Disregarded', 'Request_Factory_Construction_Started',
                 'Request_Factory_Destroyed', 'Request_Factory_Finished'):
        watcher = children.find(f"cue[@name='{name}']")
        assert watcher is not None
        children.remove(watcher)
        observed_children.append(watcher)
    finished = observed_children.find("cue[@name='Request_Factory_Finished']/conditions")
    ET.SubElement(finished, 'check_value', value='$Station.isplayerowned and $Station.buildstorage.builds.queued.count + $Station.buildstorage.builds.inprogress.count == 0')
    station_check = ET.SubElement(finished, 'check_object', object='$Station')
    ET.SubElement(station_check, 'match_child', {'class': 'class.production', 'state': 'componentstate.operational', 'min': '1'})
    timer = ET.SubElement(request.find('cues'), 'cue', name='TM_FactoryPrefabProgress', checkinterval='15s')
    conditions = ET.SubElement(timer, 'conditions')
    ET.SubElement(conditions, 'check_value', value='@$TM_PrefabPlan and not @$TM_PrefabAccepted')
    ET.SubElement(timer, 'delay', exact='15s')
    actions = ET.SubElement(timer, 'actions')
    def call(parent, ref, parameters, result):
        node = ET.SubElement(parent, 'run_actions', ref='md.TM_Empire_Construction.' + ref, result=result)
        for name, value in [('ManagerCue', '$TM_ManagerCue'), ('GoalCue', 'namespace'), *parameters]:
            ET.SubElement(node, 'param', name=name, value=value)
    expired = ET.SubElement(actions, 'do_if', value="@$TM_PrefabKey and not @$tm_empire_station_creation and @md.TM_Empire_Construction.Request.$Receipt.$key == $TM_PrefabKey and md.TM_Empire_Construction.Request.$Receipt.$state == 'abandoned_before_effect'")
    ET.SubElement(expired, 'remove_value', name='$TM_PrefabKey')
    missing = ET.SubElement(actions, 'do_if', value='not @$TM_PrefabKey')
    call(missing, 'RequestPlanValidation', [('Sequence', '$TM_PrefabPlan')], '$TM_PrefabReason')
    accepted = ET.SubElement(missing, 'do_if', value='@md.TM_Empire_Construction.Request.$Receipt.$key == $TM_PrefabReason and @md.TM_Empire_Construction.Request.$Receipt.$goal == namespace')
    ET.SubElement(accepted, 'set_value', name='$TM_PrefabKey', exact='$TM_PrefabReason')
    ready = ET.SubElement(actions, 'do_if', value='@$TM_PrefabKey')
    call(ready, 'CreateValidatedNativeStation', [('PlanKey', '$TM_PrefabKey'), ('Sector', '$RequestSector'), ('Position', '$TM_PrefabPosition'), ('Macro', 'macro.station_gen_factory_base_01_macro'), ('OriginalProduct', '$Ware'), ('Budget', 'player.money')], '$TM_PrefabCreation')
    ET.SubElement(ready, 'set_value', name='$TM_PrefabReason', exact='$TM_PrefabCreation.$reason')
    created = ET.SubElement(ready, 'do_if', value='@$TM_PrefabCreation.$station.exists')
    ET.SubElement(created, 'set_value', name='$Station', exact='$TM_PrefabCreation.$station')
    ET.SubElement(created, 'set_value', name='$ActionDefinition.$Station', exact='$Station')
    call(created, 'StepCreatedNativeStation', [], '$TM_PrefabCreation')
    ET.SubElement(created, 'set_value', name='$TM_PrefabReason', exact='$TM_PrefabCreation.$reason')
    adopted = ET.SubElement(created, 'do_if', value="$TM_PrefabCreation.$state == 'adopted'")
    ET.SubElement(adopted, 'set_value', name='$TM_PrefabAccepted', exact='true')
    ET.SubElement(adopted, 'signal_cue_instantly', cue='Request_Factory_Finalised', param="['finished', $TM_PrefabPlan, $TM_PrefabCreation.$build, $Station]")
    ET.SubElement(actions, 'set_value', name='$ActionDefinition.$TM_ConstructionReason', exact='@$TM_PrefabReason')
    retry = ET.SubElement(actions, 'do_if', value='not @$TM_PrefabAccepted')
    ET.SubElement(retry, 'reset_cue', cue='this')


def adapt_factory_prepared_result(root):
    if root.get('name') != 'TM_Empire_FactionLogic_Economy':
        return
    request = root.find(".//cue[@name='Request_Factory']")
    # create_factory сохраняет штатный подбор совместимых модулей. Он
    # разрешён как пустая оболочка, а результат с готовыми модулями не принимаем.
    for parent in list(request.find('actions').iter()):
        for node in list(parent):
            if node.tag != 'create_factory':
                continue
            index = list(parent).index(node)
            parent.remove(node)
            guard = ET.Element('do_if', value='not @$tm_empire_factory_creation and (not @md.TM_Empire_Construction.Creation.$Receipt or md.TM_Empire_Construction.Creation.$Receipt.$state == \'adopted\') and (not @md.TM_Empire_Construction.Expansion.$Receipt or md.TM_Empire_Construction.Expansion.$Receipt.$state == \'observed\' or md.TM_Empire_Construction.Expansion.$Receipt.$state == \'abandoned_before_effect\')')
            parent.insert(index, guard)
            ET.SubElement(guard, 'set_value', name='$TM_ManagerCue', exact='parent.$FactionManagerCue')
            check = ET.SubElement(guard, 'run_actions', ref='md.TM_Empire_Runtime.CanActForGovernor', result='$TM_FactoryAccess')
            for name, value in [('Actor', '$TM_ManagerCue.$Governor'), ('Station', '$TM_ManagerCue.$GovernorStation'), ('Module', '$TM_ManagerCue.$GovernorModule'), ('ManagerCue', '$TM_ManagerCue')]:
                ET.SubElement(check, 'param', name=name, value=value)
            allowed = ET.SubElement(guard, 'do_if', value="$TM_FactoryAccess == 'available'")
            ET.SubElement(allowed, 'set_value', name='$tm_empire_factory_creation', exact="table[$state='creation_sent', $reason='factory_shell_pending', $manager=$TM_ManagerCue, $goal=namespace, $issued=player.age]")
            ET.SubElement(allowed, 'set_value', name='md.TM_Empire_Construction.Creation.$Receipt', exact='$tm_empire_factory_creation')
            allowed.append(node)
            ET.SubElement(allowed, 'set_value', name='$tm_empire_factory_creation.$station', exact='$Station')
            observed = ET.SubElement(allowed, 'do_if', value='$Station.exists and $Station.isplayerowned and $Station.buildplot.exists and $Station.buildstorage.exists and not $Station.modules.all.count and not $Station.buildstorage.builds.queued.count and not $Station.buildstorage.builds.inprogress.count')
            ET.SubElement(observed, 'set_value', name='$tm_empire_factory_creation.$state', exact="'bare_station_observed'")
            unknown = ET.SubElement(allowed, 'do_else')
            ET.SubElement(unknown, 'set_value', name='$tm_empire_factory_creation.$state', exact="'unknown'")
            ET.SubElement(unknown, 'set_value', name='$tm_empire_factory_creation.$reason', exact="'factory_shell_not_empty_or_unconfirmed'")
    cue = root.find(".//cue[@name='Request_Factory_Finalised']")
    assert cue is not None
    actions = cue.find('actions')
    stock = list(actions)
    actions.clear()
    prepared = ET.SubElement(actions, 'do_if', value="@event.param.{1} == 'prepared' and @event.param.{4} == $Station and typeof @event.param.{2} == datatype.constructionsequence")
    ET.SubElement(prepared, 'set_value', name='$TM_ManagerCue', exact='namespace.parent.$FactionManagerCue')
    ET.SubElement(prepared, 'set_value', name='$TM_PreparedFactoryPlan', exact='event.param.{2}')
    ET.SubElement(prepared, 'set_value', name='$ActionDefinition.$TM_ConstructionReason', exact="'native_factory_plan_prepared_validation_pending'")
    ET.SubElement(prepared, 'reset_cue', cue='this')
    # Retain the native bookkeeping, but it requires the actual queued build.
    # The new prepared signal deliberately cannot acknowledge this boundary.
    finished = ET.SubElement(actions, 'do_elseif', value="@event.param.{1} == 'finished' and @event.param.{4} == $Station and @event.param.{3}.exists and event.param.{3}.isexpansion and event.param.{3}.buildobject == $Station and event.param.{3}.object == $Station.buildstorage and ($Station.buildstorage.builds.queued.indexof.{event.param.{3}} or $Station.buildstorage.builds.inprogress.indexof.{event.param.{3}})")
    finished.extend(stock)
    request = root.find(".//cue[@name='Request_Factory']")
    timer = ET.SubElement(request.find('cues'), 'cue', name='TM_FactoryPlanValidation', checkinterval='15s')
    conditions = ET.SubElement(timer, 'conditions')
    ET.SubElement(conditions, 'check_value', value='@$TM_PreparedFactoryPlan')
    ET.SubElement(timer, 'delay', exact='15s')
    tick = ET.SubElement(timer, 'actions')
    missing = ET.SubElement(tick, 'do_if', value='not @$TM_FactoryPlanKey')
    validate = ET.SubElement(missing, 'run_actions', ref='md.TM_Empire_Construction.RequestPlanValidation', result='$TM_FactoryValidationReason')
    for name, value in [('ManagerCue', '$TM_ManagerCue'), ('GoalCue', 'namespace'), ('Sequence', '$TM_PreparedFactoryPlan')]:
        ET.SubElement(validate, 'param', name=name, value=value)
    # Validate every factory module: no existing-station exemption for a new
    # factory's base sequence before its acquisition path is qualified.
    correlated = ET.SubElement(missing, 'do_if', value='@md.TM_Empire_Construction.Request.$Receipt.$key == $TM_FactoryValidationReason and @md.TM_Empire_Construction.Request.$Receipt.$goal == namespace')
    ET.SubElement(correlated, 'set_value', name='$TM_FactoryPlanKey', exact='$TM_FactoryValidationReason')
    ET.SubElement(missing, 'set_value', name='$ActionDefinition.$TM_ConstructionReason', exact='$TM_FactoryValidationReason')
    ready = ET.SubElement(tick, 'do_if', value='@$TM_FactoryPlanKey')
    read = ET.SubElement(ready, 'run_actions', ref='md.TM_Empire_Construction.ReadValidatedPlan', result='$TM_FactoryValidatedPlan')
    for name, value in [('Key', '$TM_FactoryPlanKey'), ('ManagerCue', '$TM_ManagerCue'), ('GoalCue', 'namespace')]:
        ET.SubElement(read, 'param', name=name, value=value)
    ET.SubElement(ready, 'set_value', name='$ActionDefinition.$TM_ConstructionReason', exact='$TM_FactoryValidatedPlan.$reason')
    validated = ET.SubElement(ready, 'do_if', value="$TM_FactoryValidatedPlan.$state == 'blueprints_observed'")
    queue = ET.SubElement(validated, 'run_actions', ref='md.TM_Empire_Construction.QueueValidatedFactoryPlan', result='$TM_FactoryQueue')
    for name, value in [('ManagerCue', '$TM_ManagerCue'), ('GoalCue', 'namespace'), ('Station', '$Station'), ('PlanKey', '$TM_FactoryPlanKey'), ('Budget', 'player.money')]:
        ET.SubElement(queue, 'param', name=name, value=value)
    ET.SubElement(validated, 'set_value', name='$ActionDefinition.$TM_ConstructionReason', exact='$TM_FactoryQueue.$reason')
    queued = ET.SubElement(validated, 'do_if', value="$TM_FactoryQueue.$state == 'adopted'")
    ET.SubElement(queued, 'set_value', name='$TM_FactoryQueued', exact='true')
    ET.SubElement(queued, 'signal_cue_instantly', cue='Request_Factory_Finalised', param="['finished', $TM_PreparedFactoryPlan, $TM_FactoryQueue.$build, $Station]")
    retry = ET.SubElement(tick, 'do_if', value="not @$TM_FactoryQueued and (not @$TM_FactoryValidatedPlan or $TM_FactoryValidatedPlan.$state != 'abandoned_before_effect')")
    ET.SubElement(retry, 'reset_cue', cue='this')


def adapt_habitation_construction(root):
    if root.get('name') != 'TM_Empire_FactionLogic_Economy':
        return
    goal = root.find(".//cue[@name='Habitation_Helper_Production_Finished']")
    actions = goal.find('actions')
    actions.insert(0, ET.Element('set_value', name='$TM_ManagerCue', exact='@md.TM_Empire_Runtime.Registry.$ManagerCue'))
    def call(ref, extra=(), result=None):
        attributes = {'ref': 'md.TM_Empire_Construction.' + ref}
        if result:
            attributes['result'] = result
        node = ET.Element('run_actions', **attributes)
        for name, value in [('ManagerCue', '$TM_ManagerCue'), ('GoalCue', 'namespace'), ('Station', '$Station'), *extra]:
            ET.SubElement(node, 'param', name=name, value=value)
        return node
    for parent in list(actions.iter()):
        for node in list(parent):
            if node.tag == 'create_construction_sequence':
                index = list(parent).index(node)
                parent.remove(node)
                parent.insert(index, call('BeginExpansionGeneration', [('Modules', '$NewModules'), ('Connectors', '$ViableConnectionModules')], '$TM_GenerationReason'))
                failed = ET.SubElement(parent, 'do_if', value="$TM_GenerationReason != 'generating'")
                ET.SubElement(failed, 'add_to_group', groupname='parent.$Factories', object='$Station')
                ET.SubElement(failed, 'cancel_cue', cue='this')
    finished = goal.find("cues/cue[@name='Habitation_Helper_Generation_Finished']/actions")
    finished.clear()
    success = ET.SubElement(finished, 'do_if', value='event.param and event.param2')
    success.append(call('AcceptGeneratedExpansion', [('Sequence', 'event.param'), ('Budget', 'player.money'),
        ('EventStation', 'event.object'), ('EventSequence', 'event.param'), ('EventSuccess', 'event.param2')], '$TM_ConstructionKey'))
    rejected = ET.SubElement(success, 'do_if', value='@md.TM_Empire_Construction.Expansion.$Receipt.$key != $TM_ConstructionKey')
    ET.SubElement(rejected, 'add_to_group', groupname='namespace.parent.$Factories', object='$Station')
    ET.SubElement(rejected, 'cancel_cue', cue='namespace')
    failed = ET.SubElement(finished, 'do_else')
    failed.append(call('ReleaseUnappliedGeneration'))
    ET.SubElement(failed, 'add_to_group', groupname='namespace.parent.$Factories', object='$Station')
    ET.SubElement(failed, 'cancel_cue', cue='namespace')
    aborted = goal.find("cues/cue[@name='Habitation_Helper_Generation_Aborted']/actions")
    stock = list(aborted)
    aborted.clear()
    before_acceptance = ET.SubElement(aborted, 'do_if', value='not @$TM_ConstructionKey')
    before_acceptance.append(call('ReleaseUnappliedGeneration'))
    before_acceptance.extend(stock)
    observer = ET.SubElement(goal.find('cues'), 'cue', name='TM_HabitationObserved', checkinterval='15s')
    conditions = ET.SubElement(observer, 'conditions')
    ET.SubElement(conditions, 'check_value', value='@$TM_ConstructionKey')
    ET.SubElement(observer, 'delay', exact='15s')
    observed = ET.SubElement(observer, 'actions')
    read = ET.SubElement(observed, 'run_actions', ref='md.TM_Empire_Construction.ReadExpansionResult', result='$TM_ExpansionResult')
    for name, value in [('ManagerCue', '$TM_ManagerCue'), ('GoalCue', 'namespace'), ('Key', '$TM_ConstructionKey')]:
        ET.SubElement(read, 'param', name=name, value=value)
    done = ET.SubElement(observed, 'do_if', value="$TM_ExpansionResult.$state == 'observed' or $TM_ExpansionResult.$state == 'abandoned_before_effect'")
    ET.SubElement(done, 'cancel_cue', cue='namespace')
    waiting = ET.SubElement(observed, 'do_else')
    ET.SubElement(waiting, 'reset_cue', cue='this')


def adapt_economy_construction(root):
    if root.get('name') != 'TM_Empire_FactionLogic_Economy':
        return
    request = root.find(".//cue[@name='Request_Production_Module']")
    assert request is not None
    request.find('actions').insert(0, ET.Element(
        'set_value', name='$TM_ManagerCue', exact='parent.$FactionManagerCue'))
    generate = request.find(".//cue[@name='Request_Production_Module_Generate_Sequence']")
    generated = request.find(".//cue[@name='Request_Production_Module_Sequence_Generated']")
    assert generate is not None and generated is not None
    # The native size threshold and symmetric extensions remain unchanged.
    # Geometry waits for a quote and native safety check, then real licence.
    generation_actions = generate.find('actions')
    generation_actions.insert(1, ET.Element('set_value', name='$TM_WaitPlot', exact='false'))
    plot_extension = generate.find("actions/do_if")
    assert plot_extension is not None and list(plot_extension.iter('extend_build_plot'))
    plot_extension.clear()
    plot_extension.set('value', "$PlotLength gt 0m and $PlotLength lt 15km and (1.0f / ($PlotLength * 2.0f) * $Station.size) ge 0.75f")
    def plot_request(actions, extend):
        call = ET.SubElement(actions, 'run_actions', ref='md.TM_Empire_Construction.RequestPlotChange', result='$TM_PlotKey')
        for name, value in [('ManagerCue', '$TM_ManagerCue'), ('GoalCue', 'namespace'),
                            ('Station', '$Station'), ('Budget', 'player.money'), ('Extend', extend)]:
            ET.SubElement(call, 'param', name=name, value=value)
        pending = ET.SubElement(actions, 'do_if', value='@md.TM_Empire_Construction.Plot.$Receipt.$key == $TM_PlotKey')
        ET.SubElement(pending, 'set_value', name='$TM_WaitPlot', exact='true')
        ET.SubElement(pending, 'set_value', name='$ActionDefinition.$TM_ConstructionReason', exact="'plot_quote_or_licence_pending'")
    plot_request(plot_extension, 'true')
    licence = ET.Element('do_if', value='not $TM_WaitPlot')
    call = ET.SubElement(licence, 'run_actions', ref='md.TM_Empire_Construction.ReadPlotLicence', result='$TM_PlotReason')
    ET.SubElement(call, 'param', name='Station', value='$Station')
    missing = ET.SubElement(licence, 'do_if', value="$TM_PlotReason != 'observed'")
    plot_request(missing, 'false')
    generation_actions.insert(list(generation_actions).index(plot_extension) + 1, licence)
    count = 0
    for parent in list(generate.iter()):
        for node in list(parent):
            if node.tag != 'create_construction_sequence':
                continue
            call = ET.Element('run_actions', ref='md.TM_Empire_Construction.BeginExpansionGeneration', result='$TM_GenerationReason')
            for name, value in [('ManagerCue', '$TM_ManagerCue'), ('GoalCue', 'namespace'),
                                ('Station', node.get('station')), ('Modules', node.get('macros')),
                                ('Connectors', node.get('connectors'))]:
                ET.SubElement(call, 'param', name=name, value=value)
            index = list(parent).index(node)
            parent.remove(node)
            ready = ET.Element('do_if', value='not $TM_WaitPlot')
            ready.append(call); parent.insert(index, ready)
            failed = ET.Element('do_if', value="$TM_GenerationReason != 'generating'")
            ET.SubElement(failed, 'set_value', name='$ActionDefinition.$TM_ConstructionReason', exact='$TM_GenerationReason')
            ET.SubElement(failed, 'cancel_cue', cue='Request_Production_Module')
            ready.append(failed)
            begin_call, begin_failure = copy.deepcopy(call), copy.deepcopy(failed)
            count += 1
    assert count == 1
    plot_ready = ET.SubElement(generate.find('cues'), 'cue', name='TM_PlotReady', checkinterval='5s')
    conditions = ET.SubElement(plot_ready, 'conditions')
    ET.SubElement(conditions, 'check_value', value='$TM_WaitPlot and @md.TM_Empire_Construction.Plot.$Receipt.$key == $TM_PlotKey')
    ET.SubElement(plot_ready, 'delay', exact='5s')
    actions = ET.SubElement(plot_ready, 'actions')
    ET.SubElement(actions, 'set_value', name='$ActionDefinition.$TM_ConstructionReason', exact='@md.TM_Empire_Construction.Plot.$Receipt.$reason')
    ready = ET.SubElement(actions, 'do_if', value="md.TM_Empire_Construction.Plot.$Receipt.$state == 'observed' or md.TM_Empire_Construction.Plot.$Receipt.$state == 'rejected_before_effect'")
    ET.SubElement(ready, 'set_value', name='$TM_WaitPlot', exact='false')
    ready.append(begin_call); ready.append(begin_failure)
    still_waiting = ET.SubElement(actions, 'do_if', value='@$TM_WaitPlot')
    ET.SubElement(still_waiting, 'reset_cue', cue='this')
    # Native load aborts pending async generation. Remove only this goal's
    # unapplied generation claim before the stock branch restarts it.
    aborted = request.find(".//cue[@name='Request_Production_Module_Sequence_Aborted']")
    assert aborted is not None
    release = ET.Element('run_actions', ref='md.TM_Empire_Construction.ReleaseUnappliedGeneration')
    for name, value in [('ManagerCue', '$TM_ManagerCue'), ('GoalCue', 'namespace'), ('Station', '$Station')]:
        ET.SubElement(release, 'param', name=name, value=value)
    aborted.find('actions').insert(0, release)
    # A load during plot quoting/licensing resumes that exact key. It must
    # not restart geometry generation and replace the still-live goal.
    abort_actions = aborted.find('actions')
    stock_abort = list(abort_actions)[1:]
    for node in stock_abort:
        abort_actions.remove(node)
    waiting = ET.SubElement(abort_actions, 'do_if', value='$TM_WaitPlot and @md.TM_Empire_Construction.Plot.$Receipt.$key == $TM_PlotKey')
    ET.SubElement(waiting, 'reset_cue', cue='TM_PlotReady')
    otherwise = ET.SubElement(abort_actions, 'do_else')
    otherwise.extend(stock_abort)
    # A failed native generator has finished too; it must not leave a stale
    # station claim preventing the next legitimate economic goal.
    generation_failure = generated.find("actions/do_else")
    assert generation_failure is not None
    generation_failure.insert(0, copy.deepcopy(release))
    count = 0
    for parent in list(generated.iter()):
        for node in list(parent):
            if node.tag != 'add_build_to_expand_station':
                continue
            assert node.get('constructionplan') == '$ConstructionSequence'
            call = ET.Element('run_actions', ref='md.TM_Empire_Construction.AcceptGeneratedExpansion', result='$TM_ConstructionKey')
            for name, value in [('ManagerCue', '$TM_ManagerCue'), ('GoalCue', 'namespace'),
                                ('Station', '$Station'), ('Sequence', '$ConstructionSequence'),
                                ('Budget', 'player.money'), ('EventStation', 'event.object'),
                                ('EventSequence', 'event.param'), ('EventSuccess', 'event.param2')]:
                ET.SubElement(call, 'param', name=name, value=value)
            index = list(parent).index(node)
            parent.remove(node); parent.insert(index, call)
            ET.SubElement(parent, 'set_value', name='$ActionDefinition.$TM_ConstructionKey', exact='$TM_ConstructionKey')
            failed = ET.SubElement(parent, 'do_if', value='@md.TM_Empire_Construction.Expansion.$Receipt.$key != $TM_ConstructionKey')
            ET.SubElement(failed, 'set_value', name='$ActionDefinition.$TM_ConstructionReason', exact='$TM_ConstructionKey')
            ET.SubElement(failed, 'cancel_cue', cue='Request_Production_Module')
            count += 1
    assert count == 1


def main():
    # Assemble the complete isolated closure before domain adaptation.
    # These files are staging sources, never an activation/installation list.
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    for original in sorted(SOURCE.parent.glob('*.xml')):
        shutil.copy2(original, TARGET.parent / original.name)
    root = ET.parse(SOURCE).getroot()
    manager = root.find("cues/library[@name='Manager']")
    assert manager is not None and manager.get('version') == '18'
    # The library instance registers itself after native initialization.
    # A reference to an unstarted child definition is not an active manager.
    initialized = manager.find('actions')
    ET.SubElement(initialized, 'set_value', name='md.TM_Empire_Runtime.Registry.$ManagerCue', exact='namespace')
    ET.SubElement(initialized, 'set_value', name='md.TM_Empire_Runtime.Registry.$State', exact="'active'")
    ET.SubElement(initialized, 'remove_value', name='md.TM_Empire_Runtime.Registry.$StopReason')
    manager.set('version', '1')
    params = manager.find('params')
    for name in ('Governor', 'GovernorStation', 'GovernorModule'):
        ET.SubElement(params, 'param', name=name)
    # Контроллер входит в копию: пока staged MD не установлен, он не запускается.
    # Registry держит единственный экземпляр; старые claims блокируют новый старт.
    lifecycle = ET.fromstring('''<cues>
      <cue name="TM_PlayerManagerWatch" checkinterval="5s" namespace="this">
        <conditions><check_value value="player.entity.exists"/></conditions><delay exact="5s"/>
        <actions>
          <run_actions ref="md.TM_Empire_Runtime.ValidateBinding"/>
          <do_if value="md.TM_Empire_Runtime.Registry.$State == 'bound' and not @md.TM_Empire_Runtime.Registry.$ManagerCue.exists">
            <!-- Old claims stay protected by manager identity and their own
                 reconciliation guards. They must not stop unrelated assets. -->
              <set_value name="md.TM_Empire_Runtime.Registry.$State" exact="'starting'"/>
              <signal_cue_instantly cue="TM_PlayerManagerStart" param="[md.TM_Empire_Runtime.Registry.$Governor, md.TM_Empire_Runtime.Registry.$Station, md.TM_Empire_Runtime.Registry.$Module]"/>
          </do_if>
          <reset_cue cue="this"/>
        </actions>
      </cue>
      <cue name="TM_PlayerManagerStart" instantiate="true" namespace="this">
        <conditions><event_cue_signalled/></conditions>
        <actions>
          <run_actions ref="md.TM_Empire_Runtime.ValidateBinding"/>
          <do_if value="md.TM_Empire_Runtime.Registry.$State == 'starting' and not @md.TM_Empire_Runtime.Registry.$ManagerCue.exists and @event.param.{1} == @md.TM_Empire_Runtime.Registry.$Governor and @event.param.{2} == @md.TM_Empire_Runtime.Registry.$Station and @event.param.{3} == @md.TM_Empire_Runtime.Registry.$Module">
            <set_value name="$Governor" exact="event.param.{1}"/><set_value name="$GovernorStation" exact="event.param.{2}"/><set_value name="$GovernorModule" exact="event.param.{3}"/>
          </do_if>
          <do_else><cancel_cue cue="this"/></do_else>
        </actions>
        <cues><cue name="TM_PlayerManager" ref="Manager"><param name="Faction" value="faction.player"/><param name="Governor" value="$Governor"/><param name="GovernorStation" value="$GovernorStation"/><param name="GovernorModule" value="$GovernorModule"/></cue></cues>
      </cue>
    </cues>''')
    root.find('cues').extend(list(lifecycle))
    params.find("param[@name='HasMissions']").set('default', 'false')
    # Прежний нулевой default библиотеки не является конфигурацией NPC.
    # Берём цель сети из реального аргонского экземпляра исходной игры.
    native_setup = ET.parse(MOD.parent / 'examples/x4_unpacked/md/factionlogic.xml').getroot()
    argon_satellites = native_setup.find(".//cue[@name='ArgonFactionLogic_Manager']/param[@name='SatelliteNetworkGoal']")
    if argon_satellites is None:
        raise ValueError('Не найдена штатная аргонская цель сети спутников')
    params.find("param[@name='SatelliteNetworkGoal']").set('default', argon_satellites.get('value'))
    manager_actions = manager.find('actions')
    satellite_group = manager_actions.find("create_group[@groupname='$FactionSatellites']")
    scan = ET.Element('find_object', name='$TM_ExistingSatellites', space='player.galaxy', class_='class.satellite', owner='faction.player', multiple='true', known='true')
    scan.set('class', scan.attrib.pop('class_'))
    manager_actions.insert(list(manager_actions).index(satellite_group) + 1, scan)
    register = ET.Element('do_for_each', name='$TM_Satellite', **{'in': '$TM_ExistingSatellites'})
    own = ET.SubElement(register, 'do_if', value='$TM_Satellite.exists and $TM_Satellite.isplayerowned and $TM_Satellite.isoperational')
    ET.SubElement(own, 'add_to_group', groupname='$FactionSatellites', object='$TM_Satellite')
    manager_actions.insert(list(manager_actions).index(scan) + 1, register)
    # Setup initializes only NPC rows. Our HQ must have its own metadata row
    # before any child writes to it; never alias the original FactionData.
    initialization = ET.Element('do_if', value='not md.$TM_EmpireFactionData?')
    ET.SubElement(initialization, 'set_value', name='md.$TM_EmpireFactionData', exact='table[]')
    manager.find('actions').insert(0, initialization)
    row = ET.Element('do_if', value='not md.$TM_EmpireFactionData.{$Faction}?')
    ET.SubElement(row, 'set_value', name='md.$TM_EmpireFactionData.{$Faction}', exact='table[]')
    manager.find('actions').insert(1, row)
    # The private script has no saves from the original NPC versions.
    for patch in list(manager.findall('patch')):
        manager.remove(patch)
    for parent in root.iter():
        for node in list(parent):
            if node.tag == 'set_faction_mood':
                parent.remove(node)

    cues = manager.find('cues')
    # Keep the goal instance and its cursors alive; only its timer resets.
    personnel_goal = ET.SubElement(cues, 'cue', name='TM_PersonnelGoal', namespace='this')
    personnel = ET.SubElement(ET.SubElement(personnel_goal, 'cues'), 'cue', name='TM_PersonnelTick', checkinterval='30s')
    conditions = ET.SubElement(personnel, 'conditions')
    ET.SubElement(conditions, 'check_value', value='parent.exists')
    ET.SubElement(personnel, 'delay', exact='30s')
    actions = ET.SubElement(personnel, 'actions')
    ET.SubElement(actions, 'set_value', name='parent.parent.$tm_empire_personnel_goal', exact='parent')
    call = ET.SubElement(actions, 'run_actions', ref='md.TM_Empire_Personnel.StepPersonnel', result='$TM_PersonnelResult')
    ET.SubElement(call, 'param', name='ManagerCue', value='parent.parent')
    ET.SubElement(call, 'param', name='GoalCue', value='parent')
    ET.SubElement(actions, 'set_value', name='parent.$LastResult', exact='$TM_PersonnelResult')
    ET.SubElement(actions, 'set_value', name='parent.$LastReason',
        exact="if $TM_PersonnelResult == 'sent' and @parent.$Reason then parent.$Reason else $TM_PersonnelResult")
    ET.SubElement(actions, 'set_value', name='parent.$LastObserved', exact='player.age')
    ET.SubElement(actions, 'reset_cue', cue='this')
    removed = {'FactionDeactivated', 'FactionRepresentativeKilled_Check',
               'CreateNewFactionRepresentative', 'Ship_Construction_Manager',
               'Fleet_Evolution_Checker'}
    for node in list(cues):
        if node.get('name') in removed:
            cues.remove(node)
    for parent in root.iter():
        for node in list(parent):
            if node.tag in ('signal_cue', 'signal_cue_instantly', 'reset_cue') and node.get('cue') in removed:
                parent.remove(node)

    find = cues.find("cue[@name='Find_Faction_Headquarters']")
    find.clear()
    find.set('name', 'Find_Faction_Headquarters')
    actions = ET.SubElement(find, 'actions')
    ET.SubElement(actions, 'set_value', name='$HQNecessary', exact='false')
    ET.SubElement(actions, 'set_value', name='$HQ', exact='$GovernorStation')
    ET.SubElement(actions, 'set_value', name='md.$TM_EmpireFactionData.{$Faction}.$Headquarters', exact='$HQ')

    cleanup = cues.find("cue[@name='Cleanup_Faction_Headquarters']")
    cleanup.clear()
    cleanup.set('name', 'Cleanup_Faction_Headquarters')
    conditions = ET.SubElement(cleanup, 'conditions')
    ET.SubElement(conditions, 'event_cue_signalled')
    actions = ET.SubElement(cleanup, 'actions')
    ET.SubElement(actions, 'set_value', name='$HQ', exact='null')
    ET.SubElement(actions, 'remove_value', name='md.$TM_EmpireFactionData.{$Faction}.$Headquarters')
    ET.SubElement(actions, 'reset_cue', cue='Cleanup_Faction_Headquarters')
    # RelocateHQ retains its signal contract, but now only refreshes our link.
    # No native representative or faction headquarters is created/removed.
    forbidden = {'set_faction_mood', 'set_faction_headquarters',
                 'remove_representative', 'create_representative_actor'}
    assert not any(node.tag in forbidden for node in root.iter())
    # Retain native strength/class selection and its random tier distribution;
    # substitute only job availability with accessible player purchase options.
    job_selection = root.find("cues/library[@name='Get_Suitable_Jobs_Lib']")
    for parent in job_selection.iter():
        for node in list(parent):
            if node.tag != 'get_suitable_job': continue
            call = ET.Element('run_actions', ref='md.TM_Empire_Purchase.ReadPurchaseOptions', result=node.get('result'))
            ET.SubElement(call, 'param', name='Tags', value=node.get('tags'))
            ET.SubElement(call, 'param', name='Classes', value=node.get('size'))
            index = list(parent).index(node)
            parent.remove(node); parent.insert(index, call)
    ET.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    ET.indent(root, space='  ')
    data = ET.tostring(root, encoding='utf-8', xml_declaration=True)
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_bytes(data)
    economy_source = MOD / 'native/md/tm_factionlogic_economy.xml'
    economy_root = ET.parse(economy_source).getroot()
    claims = ET.SubElement(economy_root.find('cues'), 'cue', name='OwnedClaims', namespace='this')
    ET.SubElement(ET.SubElement(claims, 'actions'), 'create_group', groupname='$Ships')
    ended = ET.SubElement(economy_root.find('cues'), 'cue', name='OwnedOrderEnded', instantiate='true', namespace='this')
    conditions = ET.SubElement(ended, 'conditions')
    events = ET.SubElement(conditions, 'check_any')
    for event in ('event_object_order_finished', 'event_object_order_cancelled'):
        ET.SubElement(events, event, group='OwnedClaims.$Ships')
    ET.SubElement(conditions, 'check_value', value='not event.param.exists')
    ET.SubElement(conditions, 'check_value', value='@event.object.$tm_empire_claim.$orders.indexof.{event.param}')
    ended_actions = ET.SubElement(ended, 'actions')
    ET.SubElement(ended_actions, 'remove_from_list', name='event.object.$tm_empire_claim.$orders', exact='event.param')
    release = ET.SubElement(ended_actions, 'do_if', value='event.object.$tm_empire_claim.$orders.count == 0 and not event.object.$tm_empire_claim.$missing')
    ET.SubElement(release, 'set_value', name='event.object.$tm_empire_last_order_end', exact="table[$ended=player.age, $outcome='orders_ended_not_trade_success']")
    ET.SubElement(release, 'release_commandeered_object', object='event.object')
    ET.SubElement(release, 'remove_value', name='event.object.$tm_empire_claim')
    ET.SubElement(release, 'remove_from_group', group='OwnedClaims.$Ships', object='event.object')
    request = economy_root.find(".//cue[@name='Request_Commandeerable_Freighter']")
    assert request is not None
    request_actions = request.find('actions')
    guard = ET.SubElement(economy_root.find('cues'), 'library',
                          name='CanUseOwnedShip', purpose='run_actions', namespace='this')
    guard_params = ET.SubElement(guard, 'params')
    ET.SubElement(guard_params, 'param', name='Ship')
    ET.SubElement(guard_params, 'param', name='ManagerCue')
    ET.SubElement(guard_params, 'param', name='GoalCue')
    guard_actions = ET.SubElement(guard, 'actions')
    lifecycle = ET.SubElement(guard_actions, 'run_actions', ref='md.TM_Empire_Runtime.CanActForGovernor', result='$LifecycleReason')
    for name, value in [('Actor', '$ManagerCue.$Governor'), ('Station', '$ManagerCue.$GovernorStation'),
                        ('Module', '$ManagerCue.$GovernorModule'), ('ManagerCue', '$ManagerCue')]:
        ET.SubElement(lifecycle, 'param', name=name, value=value)
    inactive = ET.SubElement(guard_actions, 'do_if', value="$LifecycleReason != 'available'")
    ET.SubElement(inactive, 'return', value='$LifecycleReason')
    checks = [
        ('not $Ship.exists or not $Ship.isplayerowned or not $Ship.isoperational', 'asset_unavailable'),
        ('$Ship == player.controlled', 'player_helm'),
        ('$Ship.$tm_empire_claim?', 'claimed'),
        ('$Ship.hasorderloop or $Ship.orders.count gt 0', 'existing_orders'),
        ('@$Ship.order.isoverride or @$Ship.order.haspriority', 'priority_order'),
        ('$Ship.defaultorder.exists and $Ship.defaultorder.id != \'Wait\'', 'existing_behavior'),
        ('$Ship.order.exists and $Ship.order.id != \'Wait\'', 'existing_behavior'),
    ]
    for expression, reason in checks:
        branch = ET.SubElement(guard_actions, 'do_if', value=expression)
        ET.SubElement(branch, 'return', value=repr(reason))
    ET.SubElement(guard_actions, 'return', value="'available'")
    # Use the same ownership/order boundary as every other player domain.
    guard_actions.clear()
    delegated = ET.SubElement(guard_actions, 'run_actions', ref='md.TM_Empire_Runtime.CanUseOwnedShip', result='$Reason')
    for name in ('Ship', 'ManagerCue', 'GoalCue'):
        ET.SubElement(delegated, 'param', name=name, value='$' + name)
    ET.SubElement(guard_actions, 'return', value='$Reason')
    job = request_actions.find("get_suitable_job[@result='$TestJob']")
    assert job is not None
    request_actions.remove(job)
    gate = request_actions.find("do_if[@value='$TestJob']")
    assert gate is not None
    gate.set('value', '$Faction == faction.player')
    gate.remove(gate.find("remove_value[@name='$TestJob']"))
    # Preserve native distance/priority/mining capability selection, replacing
    # NPC job/basket membership with actual ownership and usable cargo space.
    for search in request.iter('find_ship_by_true_owner'):
        for attribute in ('commandeerable', 'requestedjobship', 'jobtags'):
            search.attrib.pop(attribute, None)
        for basket in list(search.findall('match_basket_wares')):
            search.remove(basket)
    candidates = request.find(".//do_all[@exact='$PotentialShips.count']")
    candidate_check = ET.Element('do_if', value='not $PotentialShip.cargo.{$Ware}.max')
    ET.SubElement(candidate_check, 'continue')
    candidates.insert(1, candidate_check)
    check_candidate = ET.Element('run_actions', ref='CanUseOwnedShip', result='$UseShipReason')
    ET.SubElement(check_candidate, 'param', name='Ship', value='$PotentialShip')
    ET.SubElement(check_candidate, 'param', name='ManagerCue', value='parent.$FactionManagerCue')
    ET.SubElement(check_candidate, 'param', name='GoalCue', value='namespace')
    candidates.insert(2, check_candidate)
    skip = ET.Element('do_if', value="$UseShipReason != 'available'")
    ET.SubElement(skip, 'continue')
    candidates.insert(3, skip)
    effect = gate.find("do_if[@value='$Ship.exists']")
    assert effect is not None
    check_effect = ET.Element('run_actions', ref='CanUseOwnedShip', result='$UseShipReason')
    ET.SubElement(check_effect, 'param', name='Ship', value='$Ship')
    ET.SubElement(check_effect, 'param', name='ManagerCue', value='parent.$FactionManagerCue')
    ET.SubElement(check_effect, 'param', name='GoalCue', value='namespace')
    gate.insert(list(gate).index(effect), check_effect)
    effect.set('value', "$Ship.exists and $UseShipReason == 'available'")
    # The shared ClaimOwnedShip creates the sole complete manager/goal claim.
    # A legacy local claim would fail manager identity before native commandeer.
    # Use real native order handles, not an invented order ID or label.
    sequence = 0
    for parent_node in list(effect.iter()):
        for order in list(parent_node):
            if order.tag != 'create_order':
                continue
            sequence += 1
            handle = f'$TM_Order_{sequence}'
            order.set('name', handle)
            observed = ET.Element('do_if', value=f'{handle}.exists and {handle}.object == $Ship')
            ET.SubElement(observed, 'append_to_list', name='$Ship.$tm_empire_claim.$orders', exact=handle)
            missing = ET.Element('do_else')
            ET.SubElement(missing, 'set_value', name='$Ship.$tm_empire_claim.$state', exact="'unknown'")
            ET.SubElement(missing, 'set_value', name='$Ship.$tm_empire_claim.$missing', exact='true')
            position = list(parent_node).index(order) + 1
            parent_node.insert(position, observed)
            parent_node.insert(position + 1, missing)
    # A captured handle is evidence of issuing an order, never task completion.
    # Claims survive uncertain results and exclude the ship from a second goal.
    for cleanup_cue in request.findall('cues/cue'):
        cleanup_actions = cleanup_cue.find('actions')
        for parent_node in list(cleanup_actions.iter()):
            for node in list(parent_node):
                if node.tag == 'remove_object_commander':
                    parent_node.remove(node)
                elif node.tag == 'release_commandeered_object':
                    index = list(parent_node).index(node)
                    parent_node.remove(node)
                    own = ET.Element('do_if', value='@$Ship.$tm_empire_claim.$goal == namespace')
                    own.append(node)
                    parent_node.insert(index, own)
        if cleanup_cue.get('name').endswith('_Destroyed'):
            continue
        # Native disregard/timeout does not prove orders have ended. Keep a
        # claim until later reconciliation, rather than treating it as success.
        hold = ET.Element('do_if', value='@$Ship.$tm_empire_claim.$goal == namespace')
        ET.SubElement(hold, 'set_value', name='$Ship.$tm_empire_claim.$state', exact="'unknown'")
        cleanup_actions.insert(0, hold)
    for node in list(economy_root.find('cues')):
        if node.get('name') in ('OwnedClaims', 'OwnedOrderEnded'):
            economy_root.find('cues').remove(node)
    for node in economy_root.iter('add_to_group'):
        if node.get('groupname') == 'OwnedClaims.$Ships':
            node.set('groupname', 'md.TM_Empire_Runtime.OwnedClaims.$Ships')
    ET.indent(economy_root, space='  ')
    economy_data = ET.tostring(economy_root, encoding='utf-8', xml_declaration=True)
    economy_target = TARGET.with_name('tm_factionlogic_economy.xml')
    economy_target.write_bytes(economy_data)
    guard_coverage = {}
    for staged in sorted(TARGET.parent.glob('*.xml')):
        staged_root = ET.parse(staged).getroot()
        adapt_native_catalog_selection(staged_root)
        adapt_goal_purchase(staged_root)
        adapt_static_purchase(staged_root)
        adapt_economy_purchase(staged_root)
        adapt_economy_observations(staged_root)
        adapt_station_mining_provision(staged_root)
        adapt_patrol_registration(staged_root)
        adapt_economy_construction(staged_root)
        adapt_finalise_plan_generation(staged_root)
        adapt_station_plan_requests(staged_root)
        adapt_sector_factory_requests(staged_root)
        adapt_factory_prefab_creation(staged_root)
        adapt_factory_prepared_result(staged_root)
        adapt_factory_queue_handoff(staged_root)
        remove_native_debug_beacons(staged_root)
        adapt_mission_minefields(staged_root)
        adapt_habitation_construction(staged_root)
        adapt_buildstation_creation(staged_root)
        adapt_native_cleanup(staged_root)
        adapt_economy_prefab_expansion(staged_root)
        guard_coverage[staged.name] = adapt_owned_ship_boundaries(staged_root)
        adapt_static_defense_receipts(staged_root)
        adapt_goal_cancellation(staged_root)
        adapt_temporary_military_support(staged_root)
        bound_military_ship_selection(staged_root)
        batch_economic_ship_selection(staged_root)
        isolate_static_defense_protocol(staged_root)
        normalize_tree(staged_root)
        ET.indent(staged_root, space='  ')
        staged.write_bytes(ET.tostring(staged_root, encoding='utf-8', xml_declaration=True))
    data, economy_data = TARGET.read_bytes(), economy_target.read_bytes()
    manifest = {
        'catalogue': {'factions': native_catalog_factions()[0], 'inputs': native_catalog_factions()[1], 'qualification': 'source_categories_only_blueprints_still_required'},
        'qualification': 'partial_adaptation_not_runtime', 'installed': False,
        'aiscripts': [copy_static_defense_order(), copy_satellite_deployment_order(), copy_station_reassignment_order()],
        'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'target_sha256': hashlib.sha256(data).hexdigest(),
        'native_manager_version': 18, 'private_manager_version': 1,
        'removed_npc_cues': sorted(removed),
        'forbidden_effects': sorted(forbidden),
        'economy_selection': {
            'source_sha256': hashlib.sha256(economy_source.read_bytes()).hexdigest(),
            'target_sha256': hashlib.sha256(economy_data).hexdigest(),
            'qualification': 'owned_candidate_selection_only',
            'remaining': ['guard gameplay qualification and managed-order provenance',
                          'claim reconciliation and execution read-back', 'Request_Freighter purchase adapter'],
        },
        'remaining': ['registry lifecycle guards',
                      'economy/build/purchase/military/personnel effect adapters'],
    }
    boundaries = {
        'npc_jobs': {'get_suitable_job', 'request_job_ship', 'create_job_ship'},
        'acquisition': {'create_object', 'create_ship', 'create_factory', 'create_station', 'create_god_station', 'add_build_to_construct_ship', 'destroy_object'},
        'disposal': {'set_owner', 'set_true_owner', 'set_object_hull', 'abort_scripts', 'add_build_to_recycle_station'},
        'station_construction': {'create_construction_sequence', 'apply_construction_sequence',
                                 'add_build_to_expand_station', 'process_build'},
        'assignment': {'commandeer_object', 'release_commandeered_object', 'create_order', 'remove_object_commander', 'set_object_commander'},
        'finance': {'transfer_money', 'add_money', 'set_money'},
        'faction_policy': {'set_faction_mood', 'set_faction_relation'},
        'personnel': {'create_actor', 'create_cue_actor', 'create_platform_actor',
                      'assign_control_entity', 'add_skill', 'set_skills'},
    }
    closure = []
    for staged in sorted(TARGET.parent.glob('*.xml')):
        staged_root = ET.parse(staged).getroot()
        occurrences = []
        external_calls = []
        def visit(node, context=()):
            if node.tag in ('cue', 'library'):
                context = context + (node.get('name', '<unnamed>'),)
            for category, tags in boundaries.items():
                if node.tag in tags:
                    occurrences.append({'category': category, 'cue': '/'.join(context),
                                        'tag': node.tag, 'attributes': dict(node.attrib)})
            if node.tag in ('include_actions', 'run_actions', 'cue', 'signal_cue', 'signal_cue_instantly'):
                reference = node.get('ref') if node.tag in ('include_actions', 'run_actions', 'cue') else node.get('cue')
                if reference and reference.startswith('md.') and not reference.startswith('md.TM_Empire_'):
                    external_calls.append({'cue': '/'.join(context), 'tag': node.tag,
                                           'reference': reference, 'attributes': dict(node.attrib)})
            for child in node:
                visit(child, context)
        visit(staged_root)
        closure.append({'path': staged.relative_to(MOD).as_posix(),
                        'sha256': hashlib.sha256(staged.read_bytes()).hexdigest(),
                        'qualification': 'partial' if staged.name in ('tm_factionlogic.xml', 'tm_factionlogic_economy.xml') else 'boundary_adaptation_pending',
                        'boundaries': occurrences, 'external_calls': external_calls})
    manifest['closure'] = closure
    manifest['owned_ship_guards'] = guard_coverage
    (MOD / 'docs/native-manager-adapted.json').write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'PASS: staged closure assembled ({len(closure)} scripts); domain effects remain unqualified')


if __name__ == '__main__':
    main()
