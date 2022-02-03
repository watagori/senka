from xmlrpc.client import boolean
from senkalib.chain.transaction import Transaction 
from senkalib.caaj_journal import CaajJournal

class TestZeroPlugin():
  chain = 'test_zero'

  @classmethod
  def can_handle(cls, transaction:Transaction) -> boolean:
    pass

  @classmethod
  def get_caajs(cls, address:str, transaction:Transaction) -> CaajJournal:
    pass