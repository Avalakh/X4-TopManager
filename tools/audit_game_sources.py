"""Read-only comparison of extracted X4 sources against installed CAT/DAT.

This tool does not enable runtime compatibility or modify the game.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import xml.etree.ElementTree as ET


def catalogue(path):
    offset = 0
    result = {}
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if not line.strip():
            continue
        name, size, timestamp, digest = line.rsplit(" ", 3)
        size = int(size)
        if size < 0 or not re.fullmatch(r"[0-9a-fA-F]{32}", digest):
            raise ValueError(f"Invalid catalogue record: {path}: {name}")
        result[name.lower()] = (offset, size, digest.lower())
        offset += size
    data = path.with_suffix(".dat")
    if data.stat().st_size != offset:
        raise ValueError(f"DAT size mismatch: {data}")
    return result


def installed_index(game):
    result = {}
    for cat in sorted(game.glob("*.cat")):
        if cat.stem.endswith("_sig"):
            continue
        for name, entry in catalogue(cat).items():
            result[name] = (cat, entry)
    return result


def packed_bytes(cat, entry):
    offset, size, expected = entry
    with cat.with_suffix(".dat").open("rb") as stream:
        stream.seek(offset)
        data = stream.read(size)
    if len(data) != size or hashlib.md5(data).hexdigest() != expected:
        raise ValueError(f"CAT digest mismatch: {cat}:{offset}")
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--game", type=Path, required=True)
    parser.add_argument("--sources", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    index = installed_index(args.game)
    scripts = {}
    for path in sorted((args.sources / "md").glob("*.xml")):
        tree = ET.parse(path)
        scripts[tree.getroot().get("name", "").lower()] = path
    pending = ["factionlogic", "factionlogic_economy", "factionlogic_stations",
               "factionlogic_staticdefense", "job_helper"]
    seen = set()
    records = []
    unresolved = []
    while pending:
        name = pending.pop(0)
        if name in seen:
            continue
        seen.add(name)
        path = scripts.get(name)
        if not path:
            unresolved.append(name)
            continue
        text = path.read_text(encoding="utf-8-sig")
        # Comments are navigation, not executable dependencies.
        executable = re.sub(r"<!--.*?-->", "", text, flags=re.S)
        refs = sorted(set(m.lower() for m in re.findall(r"\bmd\.([A-Za-z_][\w]*)\.", executable)))
        pending.extend(r for r in refs if r not in seen)
        relative = path.relative_to(args.sources).as_posix()
        source_data = path.read_bytes()
        native = index.get(relative.lower())
        packed = packed_bytes(*native) if native else None
        effects = {}
        for tag in ["create_station", "create_god_station", "create_ship", "destroy_object",
                    "request_job_ship", "get_suitable_job", "commandeer_object",
                    "add_build_to_construct_ship", "add_build_to_expand_station",
                    "create_order", "set_faction_mood", "create_representative_actor"]:
            locations = [i for i, line in enumerate(text.splitlines(), 1)
                         if re.search(r"<" + tag + r"(?:\s|>)", line)]
            if locations:
                effects[tag] = locations
        records.append({"path": relative, "md_name": ET.fromstring(source_data).get("name"),
                        "sha256": hashlib.sha256(source_data).hexdigest(),
                        "installed_cat": str(native[0]) if native else None,
                        "installed_sha256": hashlib.sha256(packed).hexdigest() if packed else None,
                        "matches_installed_base": source_data == packed,
                        "md_references": refs, "effect_locations": effects,
                        "global_keys": sorted(set(re.findall(r"global\.\$([A-Za-z_]\w*)", executable))),
                        "libraries": [e.get("name") for e in ET.fromstring(source_data).iter("library")]})
    supporting = ["assets/structures/defence/macros/defence_arg_claim_01_macro.xml",
                  "libraries/wares.xml", "libraries/modulegroups.xml", "index/macros.xml",
                  "libraries/people.xml", "libraries/experiences.xml",
                  "ui/addons/ego_detailmonitor/menu_playerinfo.lua",
                  "md/conversations.xml", "md/skill_gain.xml",
                  "md/upkeep.xml", "md/upkeep_management.xml",
                  "aiscripts/order.trade.crewexchange.xml"]
    for relative in supporting:
        path = args.sources / relative
        data = path.read_bytes()
        native = index.get(relative.lower())
        packed = packed_bytes(*native) if native else None
        records.append({"path": relative, "sha256": hashlib.sha256(data).hexdigest(),
                        "installed_cat": str(native[0]) if native else None,
                        "installed_sha256": hashlib.sha256(packed).hexdigest() if packed else None,
                        "matches_installed_base": data == packed})
    affected = {r["path"].lower() for r in records}
    patches = []
    extension_indexes = {}
    for extension in sorted((args.game / "extensions").iterdir()):
        if not extension.is_dir():
            continue
        for cat in sorted(extension.glob("*.cat")):
            if cat.stem.endswith("_sig"):
                continue
            entries = catalogue(cat)
            extension_indexes.setdefault(extension.name, {}).update(
                {relative: (cat, entry) for relative, entry in entries.items()})
            for relative, entry in entries.items():
                if relative in affected:
                    data = packed_bytes(cat, entry)
                    patches.append({"extension": extension.name, "cat": str(cat),
                                    "path": relative, "sha256": hashlib.sha256(data).hexdigest(),
                                    "root_tag": ET.fromstring(data).tag if relative.endswith(".xml") else None,
                                    "activation": "not_qualified"})
        for relative in affected:
            loose = extension / relative
            if loose.is_file():
                data = loose.read_bytes()
                patches.append({"extension": extension.name, "loose_file": str(loose),
                                "path": relative, "sha256": hashlib.sha256(data).hexdigest(),
                                "root_tag": ET.fromstring(data).tag if relative.endswith(".xml") else None,
                                "activation": "not_qualified"})
    dlc_boundaries = []
    still_missing = []
    for name in unresolved:
        candidates = list(args.sources.glob(f"_*/md/{name}.xml"))
        if not candidates:
            still_missing.append(name)
        for path in candidates:
            extension_name = path.relative_to(args.sources).parts[0].removeprefix("_")
            relative = f"md/{name}.xml"
            native = extension_indexes.get(extension_name, {}).get(relative)
            data = path.read_bytes()
            packed = packed_bytes(*native) if native else None
            dlc_boundaries.append({"md_name": name, "source": str(path),
                                   "extension": extension_name,
                                   "sha256": hashlib.sha256(data).hexdigest(),
                                   "installed_cat": str(native[0]) if native else None,
                                   "matches_installed_dlc": data == packed,
                                   "classification": "external_story_boundary_not_copy_candidate"})
    mismatches = [r["path"] for r in records if not r["matches_installed_base"]]
    report = {"game_version_dat": (args.game / "version.dat").read_text().strip(),
              "qualification": "static_base_comparison_only",
              "runtime_compatibility_enabled": False,
              "records": records, "extension_overlays": patches,
              "external_dlc_boundaries": dlc_boundaries,
              "unresolved_md_names": still_missing, "base_mismatches": mismatches,
              "notes": ["MD reference closure includes shared/story boundaries; not a copy list.",
                        "Installed extension presence does not establish activation or effective XML.",
                        "No game files modified; CAT records validated against DAT MD5."]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"records": len(records), "mismatches": mismatches,
                      "unresolved": still_missing, "overlays": len(patches),
                      "dlc_boundaries": len(dlc_boundaries)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
