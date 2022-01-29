import unittest
from unittest.mock import *
from senka.plugin_manager import PluginManager
from pathlib import Path
import os

print('%s/plugin' % os.path.dirname(__file__))
class TestPluginManager(unittest.TestCase):
  def test_get_plugins(self):
    plugins = PluginManager.get_plugins('bsc', '%s/plugin' % os.path.dirname(__file__))
    assert len(plugins) == 1
    assert plugins[0].chain == 'bsc'

if __name__ == '__main__':
  unittest.main()