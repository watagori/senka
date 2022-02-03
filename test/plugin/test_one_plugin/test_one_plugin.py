
from xmlrpc.client import boolean
from senkalib.chain.transaction import Transaction
from senkalib.caaj_journal import CaajJournal
from typing import List

class TestOnePlugin():
  chain = 'test_one'

  @classmethod
  def can_handle(cls, transaction:Transaction) -> boolean:
    return True

  @classmethod
  def get_caajs(cls, address:str, transaction:Transaction) -> List[CaajJournal]:
    caaj = CaajJournal()
    caaj.set_caaj_meta("2022-01-01 00:00:00", "test_platform", "0x1111111111111111111111111111", "no comment")
    caaj.set_caaj_destination("0x0000000000000", "0x11111111111", "0x22222222222", "0x33333333333")
    caaj.set_caaj_value("SPOT", {"TESTONE": "10"}, "SPOT", {"TESTONE": "10"})
    return [caaj]