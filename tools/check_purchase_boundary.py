"""Compare purchase ABI declarations with the audited native UI sources."""
from pathlib import Path
import re

MOD = Path(__file__).resolve().parents[1]
SOURCE = MOD.parent / 'examples/X4_unpacked/ui/addons/ego_detailmonitor/menu_ship_configuration.lua'
HELPER = MOD.parent / 'examples/X4_unpacked/ui/addons/ego_detailmonitorhelper/helper.lua'
native = SOURCE.read_text(encoding='utf-8') + HELPER.read_text(encoding='utf-8')


def prototypes(text):
    result = {}
    for return_type, name, args in re.findall(r'\b(\w+)\s+(\w+)\(([^;{}\n]*)\);', text):
        types = []
        if args.strip() not in ('', 'void'):
            for arg in args.split(','):
                # Argument names do not form part of the C ABI.
                types.append(re.sub(r'\s+', '', re.sub(r'\b\w+\s*$', '', arg).strip()))
        signature = (return_type, tuple(types))
        if name in result:
            assert result[name] == signature, (name, 'inconsistent native ABI')
        result[name] = signature
    return result


expected = prototypes(native)
for filename in ('purchase_receipt.lua', 'purchase_quote.lua'):
    source = (MOD / 'ui' / filename).read_text(encoding='utf-8')
    declarations = re.search(r'ffi\.cdef\[\[(.*?)\]\]', source, re.S).group(1)
    for name, signature in prototypes(declarations).items():
        assert expected.get(name) == signature, (filename, name, signature, expected.get(name))

def build_fields(text):
    return re.sub(r'\s+', '', re.search(r'typedef struct\s*\{([^{}]*)\}\s*BuildTaskInfo;', text, re.S).group(1))

assert build_fields((MOD / 'ui/purchase_receipt.lua').read_text(encoding='utf-8')) == build_fields(native)
print('PASS: native purchase API signatures and BuildTaskInfo layout match audited sources')
