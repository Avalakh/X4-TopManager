"""Собственные записи компонентов в штатном global, без записи полей на component."""
from pathlib import Path
import re
import xml.etree.ElementTree as ET

FIELDS = ('claim', 'last_order_end', 'station_reassignment', 'station_reassignment_result',
          'construction_claim', 'creation', 'generation', 'plot_claim', 'recycling_receipt',
          'economy_observation', 'personnel_needs', 'personnel_prerequisites', 'satellite_receipt')
RECEIVER = r'(?:\$[A-Za-z_]\w*|this|event|parent|Plot)(?:\.\$?\w+|\.\{[^{}]+\})*'
PATTERN = re.compile('(' + RECEIVER + r')\.\$tm_empire_(' + '|'.join(FIELDS) + r')\b')


def normalize_tree(graph):
    if graph.tag == 'aiscript':
        for node in graph.iter():
            for key, value in list(node.attrib.items()):
                value = value.replace('md.TM_Empire_Runtime.Registry.$State', 'global.$TM_EmpireAIState.$state')
                value = value.replace('md.TM_Empire_Runtime.Registry.$ManagerCue', 'global.$TM_EmpireAIState.$manager')
                value = value.replace('md.TM_Empire_Assets.State.$ObservationSession', 'global.$TM_EmpireAIState.$session')
                node.set(key, value)
    if graph.tag == 'mdscript':
        for parent in list(graph.iter()):
            for node in list(parent):
                if node.tag in ('set_value', 'remove_value') and node.get('name') in (
                    'Registry.$State', 'Registry.$ManagerCue',
                    'md.TM_Empire_Runtime.Registry.$State', 'md.TM_Empire_Runtime.Registry.$ManagerCue'):
                    index = list(parent).index(node) + 1
                    following = list(parent)[index:index+1]
                    if not following or following[0].get('ref') != 'md.TM_Empire_Runtime.PublishAIState':
                        parent.insert(index, ET.Element('run_actions', ref='md.TM_Empire_Runtime.PublishAIState'))
    for node in graph.iter():
        for key, value in list(node.attrib.items()):
            node.set(key, PATTERN.sub(lambda m: 'global.$TM_EmpireComponentRecords.$'
                                     + m[2] + '.{' + m[1] + '}', value))


def normalize_helpers():
    root = Path(__file__).resolve().parents[1]
    for path in sorted((root / 'md').glob('*.xml')):
        tree = ET.parse(path)
        graph = tree.getroot()
        normalize_tree(graph)
        if graph.get('name') == 'TM_Empire_Runtime':
            cues = graph.find('cues')
            if cues.find("cue[@name='ComponentRecords']") is None:
                cue = ET.Element('cue', name='ComponentRecords', namespace='this')
                actions = ET.SubElement(cue, 'actions')
                missing = ET.SubElement(actions, 'do_if', value='not global.$TM_EmpireComponentRecords?')
                ET.SubElement(missing, 'set_value', name='global.$TM_EmpireComponentRecords', exact='table[]')
                for field in FIELDS:
                    missing = ET.SubElement(actions, 'do_if', value='not global.$TM_EmpireComponentRecords.$' + field + '?')
                    ET.SubElement(missing, 'set_value', name='global.$TM_EmpireComponentRecords.$' + field, exact='table[]')
                cues.insert(0, cue)
        ET.indent(tree, space='  ')
        tree.write(path, encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    normalize_helpers()
