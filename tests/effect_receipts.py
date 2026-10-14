"""Приёмочный валидатор read-back; не входит в мод и не исполняет действия."""
import math

KINDS = {'order', 'hire', 'transfer', 'training', 'ship_purchase', 'station_build'}
STATES = {'planned', 'sent', 'observed', 'unknown', 'waiting', 'excluded'}


def valid(receipt):
    if not isinstance(receipt, dict):
        return False
    if not all(isinstance(receipt.get(key), str) and 0 < len(receipt[key]) <= 256
               for key in ('goal', 'session', 'asset')):
        return False
    issued = receipt.get('issued')
    if isinstance(issued, bool) or not isinstance(issued, (int, float)) or not math.isfinite(issued) or issued < 0:
        return False
    if receipt.get('kind') not in KINDS or receipt.get('state') not in STATES:
        return False
    if receipt['state'] in ('sent', 'observed', 'unknown'):
        if receipt.get('owned') is not True or any(receipt.get(key) is not False
                for key in ('player_helm', 'manual_order', 'emergency')):
            return False
    if receipt['state'] == 'unknown' and receipt.get('claim_held') is not True:
        return False
    if receipt['state'] != 'observed':
        return True
    evidence = receipt.get('evidence')
    if not isinstance(evidence, dict) or evidence.get('owned') is not True or not evidence.get('native_handle'):
        return False
    kind = receipt['kind']
    if kind in ('hire', 'ship_purchase'):
        price, paid = evidence.get('price'), evidence.get('paid')
        if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or v <= 0
               for v in (price, paid)) or paid != price:
            return False
    if kind in ('hire', 'transfer'):
        if not evidence.get('seed') or evidence.get('arrived') is not True or evidence.get('unique_person') is not True:
            return False
    if kind == 'training':
        before, after = evidence.get('skill_before'), evidence.get('skill_after')
        if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in (before, after)):
            return False
        if not 0 <= before < after <= 15:
            return False
        if evidence.get('seminar_consumed') is not True and evidence.get('native_experience') is not True:
            return False
    if kind in ('ship_purchase', 'station_build'):
        if any(evidence.get(key) is not True for key in ('normal_resources', 'ready', 'linked_to_order')):
            return False
    if kind == 'station_build' and any(evidence.get(key) is not True for key in ('plot', 'blueprints', 'builder')):
        return False
    return True
