"""Отрицательная приёмка границ, а не проверка штатного внутреннего AI."""
import copy
import unittest
from effect_receipts import valid


def observed(kind):
    return dict(goal='supply_1', session='save_004', asset='owned_asset', issued=388900,
                kind=kind, state='observed', owned=True, player_helm=False,
                manual_order=False, emergency=False, claim_held=True,
                evidence=dict(native_handle='native_1', owned=True, price=1000, paid=1000,
                    seed='person_1', arrived=True, unique_person=True, skill_before=3,
                    skill_after=6, seminar_consumed=True, native_experience=False,
                    normal_resources=True, ready=True, linked_to_order=True,
                    plot=True, blueprints=True, builder=True))


class ReceiptTests(unittest.TestCase):
    def test_effect_guards_and_passenger(self):
        receipt = observed('order')
        receipt['player_onboard'] = True
        self.assertTrue(valid(receipt))
        for key in ('player_helm', 'manual_order', 'emergency'):
            invalid = copy.deepcopy(receipt)
            invalid[key] = True
            self.assertFalse(valid(invalid), key)
        receipt['owned'] = False
        self.assertFalse(valid(receipt))

    def test_domain_readback_required(self):
        failures = {'hire': [('paid', 0), ('paid', 999), ('arrived', False)],
                    'transfer': [('arrived', False), ('unique_person', False)],
                    'training': [('seminar_consumed', False), ('skill_after', 3)],
                    'ship_purchase': [('paid', 0), ('ready', False), ('linked_to_order', False)],
                    'station_build': [('plot', False), ('blueprints', False), ('normal_resources', False)]}
        for kind, changes in failures.items():
            self.assertTrue(valid(observed(kind)), kind)
            for key, value in changes:
                invalid = observed(kind)
                invalid['evidence'][key] = value
                self.assertFalse(valid(invalid), (kind, key))
        receipt = observed('training')
        receipt['evidence']['seminar_consumed'] = False
        receipt['evidence']['native_experience'] = True
        self.assertTrue(valid(receipt))

    def test_unknown_keeps_claim_and_acceptance_is_not_observation(self):
        receipt = observed('transfer')
        receipt['evidence'] = {'accepted': True}
        self.assertFalse(valid(receipt))
        receipt['state'] = 'sent'
        self.assertTrue(valid(receipt))
        receipt['state'] = 'unknown'
        self.assertTrue(valid(receipt))
        receipt['claim_held'] = False
        self.assertFalse(valid(receipt))

    def test_missing_is_not_zero_or_true_and_no_raw_command(self):
        for value in (None, float('nan'), float('inf'), -1, True):
            receipt = observed('order')
            receipt['issued'] = value
            self.assertFalse(valid(receipt))
        receipt = observed('order')
        receipt['kind'] = 'create_ship'
        self.assertFalse(valid(receipt))
        receipt = observed('hire')
        del receipt['evidence']['paid']
        self.assertFalse(valid(receipt))


if __name__ == '__main__':
    unittest.main()
