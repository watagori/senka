from typing import List
from glob import glob
import importlib
import os
import re

class PluginManager():
  @classmethod
  def get_plugins(cls, chain:str, path:str) -> List:
    plugins = []
    files = os.listdir(path)
    dirs = sorted([f for f in files if os.path.isdir(os.path.join(path, f)) and "_plugin" in f and "." not in f])
    for dir in dirs:
      module = importlib.import_module(f"plugin.{dir}.{dir}", "plugin")
      dir = list(dir)
      dir[0] = dir[0].upper()
      dir = "".join(dir)
      dir = re.sub("_(.)",lambda x:x.group(1).upper(), dir)
      plugin_class = getattr(module, dir)
      if plugin_class.chain.lower() == chain.lower(): plugins.append(plugin_class)
    return plugins