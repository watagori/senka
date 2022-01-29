from typing import List
from senkalib.senka_lib import SenkaLib
from senkalib.senka_setting import SenkaSetting
from senka.plugin_manager import PluginManager
import os

class Senka:
  def __init__(self, setting_dict):
    self.setting = SenkaSetting(setting_dict)
    pass
 
  def get_caaj(self, chain:str, address:str) -> List:
    available_chains = self.get_available_chains()
    if chain.lower() not in available_chains:
      raise Exception('this chain is not supported.')

    caaj = []
    transaction_generator = list(filter(lambda x:x.chain.lower() == chain.lower(),SenkaLib.get_available_chain()))[0]
    transactions = transaction_generator.get_transactions(self.setting, address)
    plugins = PluginManager.get_plugins(chain, '%s/../plugin' % os.path.dirname(__file__))

    for transaction in transactions:
      for plugin in plugins:
        if plugin.can_handle(transaction):
          caaj_peace = plugin.get_caajs(address, transaction)
          caaj.extend(caaj_peace)

    return caaj

  def get_available_chains(self) -> List[str]:
    chains = SenkaLib.get_available_chain()
    chains = list(map(lambda x:x.chain,chains))
    return chains