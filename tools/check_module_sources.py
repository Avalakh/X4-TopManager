"""Check inherited module semantics and registration against audited game sources."""
from pathlib import Path
import copy
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[2]
mod = root / "X4_TopManager"
game = root / "examples/x4_unpacked"
original = ET.parse(game / "assets/structures/defence/macros/defence_arg_claim_01_macro.xml").getroot()
candidate = ET.parse(mod / "assets/structures/defence/macros/tm_empire_control_arg_macro.xml").getroot()
restored = copy.deepcopy(candidate)
restored.find("macro").set("name", original.find("macro").get("name"))
source_identification = original.find("macro/properties/identification")
identification = restored.find("macro/properties/identification")
for key in ("name", "shortname", "description"):
    identification.set(key, source_identification.get(key))


def canonical(element):
    return (element.tag, tuple(sorted(element.attrib.items())), (element.text or "").strip(),
            tuple(canonical(child) for child in element))


assert canonical(restored) == canonical(original), "Inherited macro gameplay changed"
base_ware = ET.parse(game / "libraries/wares.xml").find("ware[@id='module_arg_def_claim_01']")
ware = ET.parse(mod / "libraries/wares.xml").find("add/ware")
restored_ware = copy.deepcopy(ware)
for key in ("id", "name", "description"):
    restored_ware.set(key, base_ware.get(key))
restored_ware.find("component").set("ref", base_ware.find("component").get("ref"))
assert canonical(restored_ware) == canonical(base_ware), "Price/recipe/licence/owners changed"
entry = ET.parse(mod / "index/macros.xml").find("add/entry")
assert entry.get("name") == candidate.find("macro").get("name") == ware.find("component").get("ref")
indexed_path = entry.get("value").replace("\\", "/")
prefix = "extensions/tm_empire_management/"
assert indexed_path.startswith(prefix), "X4 index paths resolve from game root"
assert (mod / (indexed_path[len(prefix):] + ".xml")).is_file()
group_add = ET.parse(mod / "libraries/modulegroups.xml").find("add")
group_name = "tm_empire_control_arg"
assert ET.parse(game / "libraries/modulegroups.xml").find(f"group[@name='{group_name}']") is None
assert group_add.get("sel") == '/groups', "Do not alter NPC module selection groups"
assert group_add.find("group").get("name") == group_name
assert group_add.find("group/select").get("macro") == entry.get("name")
for language in (7, 44):
    page = ET.parse(mod / f"t/0001-L{language:03}.xml").find("page[@id='98761']")
    assert {"1", "2", "3"}.issubset({element.get("id") for element in page})
ru_ids = {node.get('id') for node in ET.parse(mod / 't/0001-L007.xml').find("page[@id='98761']")}
en_ids = {node.get('id') for node in ET.parse(mod / 't/0001-L044.xml').find("page[@id='98761']")}
assert ru_ids == en_ids, 'Missing RU/EN text IDs'
content = ET.parse(mod / "content.xml").getroot()
assert content.get("id") == "tm_empire_management"
assert content.find("dependency").get("version") == "900"
assert not any("diff" == ET.parse(path).getroot().tag for path in (mod / "assets").rglob("*.xml"))
print("PASS: inherited macro/claim/component/connections, recipe/price/licence/owners, registrations, RU/EN text, manifest")
