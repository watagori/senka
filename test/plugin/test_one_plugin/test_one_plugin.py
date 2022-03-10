
from xmlrpc.client import boolean
from senkalib.chain.transaction import Transaction
from senkalib.caaj_journal import CaajJournal
from senkalib.caaj_journal_meta import CaajJournalMeta
from senkalib.caaj_journal_amount import CaajJournalAmount
from senkalib.caaj_journal_side import CaajJournalSide
from decimal import Decimal
from typing import List

class TestOnePlugin():
  chain = 'test_one'

  @classmethod
  def can_handle(cls, transaction:Transaction) -> boolean:
    return True

  @classmethod
  def get_caajs(cls, address:str, transaction:Transaction, token_original_ids:List) -> List[CaajJournal]:
    meta = CaajJournalMeta("2022-01-01 00:00:00", "test_platform", 
      "0x1111111111111111111111111111", "no comment")
    amounts = [CaajJournalAmount('testone', 'ibc/46B44899322F3CD854D2D46DEEF881958467CDD4B3B10086DA49296BBED94BED', 
      '3a2570c5-15c4-2860-52a8-bff14f27a236', Decimal('0.005147'))]
    caaj_debit = CaajJournalSide("0x0000000000000", "0x11111111111", 'SPOT', amounts)
    caaj_credit = CaajJournalSide("0x22222222222", "0x33333333333", 'SPOT', amounts)
    caaj = CaajJournal(meta, caaj_debit, caaj_credit)

    return [caaj]