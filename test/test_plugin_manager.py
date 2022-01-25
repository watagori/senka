import unittest
from unittest.mock import *
from src.senka.plugin_manager import PluginManager
from pathlib import Path
import os

class TestPluginManager(unittest.TestCase):
  def test_get_plugins(self):
    plugins = PluginManager.get_plugins('bsc')

if __name__ == '__main__':
  unittest.main()