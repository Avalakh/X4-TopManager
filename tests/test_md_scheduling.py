"""Регрессия ID-map overflow: checkinterval не заменяет delay при reset_cue."""
import sys
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from check_md_scheduling import unsafe_resets, polling_without_interval, unsupported_cue_returns, invalid_run_actions_libraries


class SchedulingTests(unittest.TestCase):
    def test_called_library_requires_explicit_run_actions_purpose(self):
        root = ET.fromstring('''<mdscript name="Probe"><cues>
          <cue name="issue"><actions><run_actions ref="IssueTrade"/></actions></cue>
          <library name="IssueTrade"><actions><return value="sent"/></actions></library>
          <library name="OrdinaryCueLibrary"/>
        </cues></mdscript>''')
        self.assertEqual(invalid_run_actions_libraries(root), ['IssueTrade'])
        root.find('cues/cue/actions/run_actions').set('ref', 'md.Probe.IssueTrade')
        self.assertEqual(invalid_run_actions_libraries(root), ['IssueTrade'])
        root.find('cues/library').set('purpose', 'run_actions')
        self.assertEqual(invalid_run_actions_libraries(root), [])

    def test_return_does_not_guard_ordinary_cue_effects(self):
        root = ET.fromstring('''<cues><cue name="purchase"><actions>
          <do_if value="blocked"><return/></do_if><set_value name="sent"/></actions></cue>
          <library name="guard" purpose="run_actions"><actions><return value="blocked"/></actions></library></cues>''')
        self.assertEqual(unsupported_cue_returns(root), ['purchase'])
        root.find('cue/actions/do_if').remove(root.find('cue/actions/do_if/return'))
        self.assertEqual(unsupported_cue_returns(root), [])
    def test_non_event_condition_requires_interval_even_with_delay(self):
        root = ET.fromstring('''<cue name="scan"><conditions><check_value value="true"/></conditions>
          <delay exact="5s"/><actions><reset_cue cue="this"/></actions></cue>''')
        self.assertEqual(polling_without_interval(root), ['scan'])
        root.set('checkinterval', '5s')
        self.assertEqual(polling_without_interval(root), [])

    def test_interval_alone_does_not_bound_restart(self):
        root = ET.fromstring('''<cues><cue name="poll" checkinterval="5s">
          <conditions><check_value value="true"/></conditions>
          <actions><reset_cue cue="this"/></actions></cue></cues>''')
        self.assertEqual(unsafe_resets(root), ['poll'])
        ET.SubElement(root.find('cue'), 'delay', exact='5s')
        self.assertEqual(unsafe_resets(root), [])

    def test_zero_delay_rejected_and_event_wait_allowed(self):
        root = ET.fromstring('''<cue name="poll"><delay exact="0s"/>
          <actions><reset_cue cue="this"/></actions></cue>''')
        self.assertEqual(unsafe_resets(root), ['poll'])
        conditions = ET.SubElement(root, 'conditions')
        ET.SubElement(conditions, 'event_cue_signalled')
        self.assertEqual(unsafe_resets(root), [])


if __name__ == '__main__':
    unittest.main()
