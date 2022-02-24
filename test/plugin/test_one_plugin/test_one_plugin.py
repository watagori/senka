
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
  def get_caajs(cls, address:str, transaction:Transaction, token_original_ids:List) -> List[CaajJournal]:
    caaj = CaajJournal()
    caaj.set_caaj_meta("2022-01-01 00:00:00", "test_platform", "0x1111111111111111111111111111", "no comment")
    caaj.set_caaj_destination("0x0000000000000", "0x11111111111", "0x22222222222", "0x33333333333")
    amount = [
      {
        "token": {
          "symbol":"testone",
          "original_id":"ibc/46B44899322F3CD854D2D46DEEF881958467CDD4B3B10086DA49296BBED94BED",
          "symbol_uuid":"3a2570c5-15c4-2860-52a8-bff14f27a236"
        },
        "amount": "10"
      }
    ]
    
    caaj.set_caaj_value("SPOT", amount, "SPOT", amount)
    return [caaj]