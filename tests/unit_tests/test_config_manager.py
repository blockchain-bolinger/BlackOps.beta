import unittest
from core.config_manager import ConfigManager

class TestConfigManager(unittest.TestCase):
    def test_load_config(self):
        cm = ConfigManager()
        self.assertIsNotNone(cm.get('framework'))