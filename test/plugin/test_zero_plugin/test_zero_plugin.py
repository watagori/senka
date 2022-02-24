from xmlrpc.client import boolean
from senkalib.chain.transaction import Transaction 
from senkalib.caaj_journal import CaajJournal
from typing import List

class TestZeroPlugin():
  chain = 'test_zero'

  @classmethod
  def can_handle(cls, transaction:Transaction) -> boolean:
    pass

  @classmethod
  def get_caajs(cls, address:str, transaction:Transaction, token_original_ids:List) -> CaajJournal:
    pass