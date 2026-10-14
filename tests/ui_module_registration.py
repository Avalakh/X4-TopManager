"""Проверка установочного графа Lua на реальном пакете и неполных копиях."""
import shutil
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from install_mod import validate_ui_modules


class RegistrationTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / '.cache/tmp/ui-module-registration'
        base.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=base)
        self.root = Path(self.temp.name)
        shutil.copy2(ROOT / 'ui.xml', self.root / 'ui.xml')
        shutil.copytree(ROOT / 'ui', self.root / 'ui')

    def tearDown(self):
        self.temp.cleanup()

    def test_current_package(self):
        validate_ui_modules(self.root)

    def test_missing_purchase_module(self):
        tree = ET.parse(self.root / 'ui.xml')
        environment = tree.getroot().find('environment')
        environment.remove(environment.find("file[@name='ui/purchase_submit.lua']"))
        tree.write(self.root / 'ui.xml')
        with self.assertRaisesRegex(ValueError, 'Lua-зависимость отсутствует'):
            validate_ui_modules(self.root)

    def test_missing_helper_registration(self):
        path = self.root / 'ui/construction_reserve.lua'
        source = path.read_text(encoding='utf-8')
        path.write_text('\n'.join(line for line in source.splitlines()
                                  if 'Register_Require_With_Init' not in line), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Lua-модуль не зарегистрирован'):
            validate_ui_modules(self.root)


if __name__ == '__main__':
    unittest.main()
