import unittest
from unittest.mock import *
from senka.senka import Senka
from senkalib.senka_lib import SenkaLib
from senkalib.chain.transaction_generator import TransactionGenerator
from senkalib.senka_setting import SenkaSetting
from senkalib.chain.transaction import Transaction
from typing import List
from decimal import Decimal
import os
import json
from pathlib import Path
import pandas as pd
import sys

sys.path.append('%s/plugin' % os.path.dirname(__file__))


class TestSenka(unittest.TestCase):
  def test_get_available_chains(self):
    with patch.object(SenkaLib, 'get_available_chain', new=TestSenka.mock_get_available_chains):
      senka = Senka({}, '%s/test_senka_plugin.toml' % os.path.dirname(__file__))
      chains = senka.get_available_chains()
      assert chains[0] == 'test_one'
      assert chains[1] == 'test_zero'

  def test_get_caaj_no_chain(self):
    with patch.object(SenkaLib, 'get_available_chain', new=TestSenka.mock_get_available_chains):
      with self.assertRaises(ValueError):
        senka = Senka({}, '%s/test_senka_plugin.toml' % os.path.dirname(__file__))
        caaj = senka.get_caaj('no_existence_chain', '0xfFceBED170CE0230D513a0a388011eF9c2F97503')

  def test_get_caaj(self):
    with patch.object(SenkaLib, 'get_available_chain', new=TestSenka.mock_get_available_chains):
      with patch.object(SenkaLib, 'get_token_original_ids', new=TestSenka.mock_get_token_original_ids):
        senka = Senka({}, '%s/test_senka_plugin.toml' % os.path.dirname(__file__))
        caaj_list, unknown_transactions_list = senka.get_caaj('test_one', '0xfFceBED170CE0230D513a0a388011eF9c2F97503')
        cj = caaj_list[0]
        unknown_transaction = unknown_transactions_list[0]
        assert len(caaj_list) == 2
        assert len(unknown_transactions_list) == 1
        assert cj.executed_at == '2022-01-12 11:11:11'
        assert cj.chain == 'chain'
        assert cj.platform == 'platform'
        assert cj.application == 'application'
        assert cj.transaction_id == '0x36512c7e09e3570dfc53176252678ee9617660550d36f4da797afba6fc55bba6'
        assert cj.trade_uuid == 'bbbbbbddddddd'
        assert cj.type == 'deposit'
        assert cj.amount == Decimal('0.005147')
        assert cj.token_symbol == 'testone'
        assert cj.token_original_id == 'ibc/46B44899322F3CD854D2D46DEEF881958467CDD4B3B10086DA49296BBED94BED'
        assert cj.token_symbol_uuid == '3a2570c5-15c4-2860-52a8-bff14f27a236'
        assert cj.caaj_from == '0x111111111111111111111'
        assert cj.caaj_to == '0x222222222222222222222'
        assert cj.comment == 'hello world'
        assert unknown_transaction.transaction_id == 'unknown'
        assert unknown_transaction.chain == 'test_one'
        assert unknown_transaction.address == '0xfFceBED170CE0230D513a0a388011eF9c2F97503'
        assert unknown_transaction.reason == 'there is no applicable plugin'

  def test_get_caaj_csv(self):
    with patch.object(SenkaLib, 'get_available_chain', new=TestSenka.mock_get_available_chains):
      with patch.object(SenkaLib, 'get_token_original_ids', new=TestSenka.mock_get_token_original_ids):
        senka = Senka({}, '%s/test_senka_plugin.toml' % os.path.dirname(__file__))
        caaj_csv = senka.get_caaj_csv('test_one', '0xfFceBED170CE0230D513a0a388011eF9c2F97503')
        caaj_csv_lines = caaj_csv.splitlines()
        assert len(caaj_csv_lines) == 3
        assert caaj_csv_lines[0] == 'executed_at,chain,platform,application,\
transaction_id,trade_uuid,type,amount,token_symbol,token_original_id,token_symbol_uuid,caaj_from,caaj_to,comment'
        assert caaj_csv_lines[1] == '2022-01-12 11:11:11,chain,platform,application,\
0x36512c7e09e3570dfc53176252678ee9617660550d36f4da797afba6fc55bba6,bbbbbbddddddd,deposit,\
0.005147,testone,ibc/46B44899322F3CD854D2D46DEEF881958467CDD4B3B10086DA49296BBED94BED,\
3a2570c5-15c4-2860-52a8-bff14f27a236,0x111111111111111111111,0x222222222222222222222,hello world'
        assert caaj_csv_lines[2] == '2022-01-12 11:11:11,chain,platform,application,\
0x36512c7e09e3570dfc53176252678ee9617660550d36f4da797afba6fc55bba6,bbbbbbddddddd,deposit,\
0.005147,testone,ibc/46B44899322F3CD854D2D46DEEF881958467CDD4B3B10086DA49296BBED94BED,\
3a2570c5-15c4-2860-52a8-bff14f27a236,0x111111111111111111111,0x222222222222222222222,hello world'

  @classmethod
  def mock_get_available_chains(cls):
    return [OneTransactionGenerator, ZeroTransactionGenerator]

  @classmethod
  def mock_get_token_original_ids(cls):
    df = pd.read_csv('%s/testdata/token_original_ids/token_original_id.csv' % os.path.dirname(__file__))
    return df

class OneTransactionGenerator(TransactionGenerator):
  chain = 'test_one'
  @classmethod
  def get_transactions(cls, settings:SenkaSetting, address:str, timerange:dict = None, blockrange:dict = None) -> List[Transaction]:
    header = json.loads(Path('%s/testdata/header.json' % os.path.dirname(__file__)).read_text())
    receipt = json.loads(Path('%s/testdata/approve.json' % os.path.dirname(__file__)).read_text())
    transaction_a = OneTransaction(header['hash'], receipt, header['timeStamp'], header['gasUsed'], header['gasPrice'])
    transaction_b = OneTransaction(header['hash'], receipt, header['timeStamp'], header['gasUsed'], header['gasPrice'])
    transaction_unknown = OneTransaction('unknown', receipt, header['timeStamp'], header['gasUsed'], header['gasPrice'])

    return [transaction_a, transaction_b, transaction_unknown]

class OneTransaction(Transaction):
  chain = 'test_one'

  def __init__(self, transaction_id:str, transaction_receipt:dict, timestamp:str, gasused:str, gasprice:str):
    super().__init__(transaction_id)
    self.transaction_receipt = transaction_receipt
    self.timestamp = timestamp
    self.gasused = Decimal(gasused)
    self.gasprice = Decimal(gasprice)
  def get_timestamp(self) -> str:
    pass

  def get_transaction_fee(self) -> Decimal:
    pass

class ZeroTransactionGenerator(TransactionGenerator):
  chain = 'test_zero'
  @classmethod
  def get_transactions(cls, settings:SenkaSetting, address:str, timerange:dict = None, blockrange:dict = None) -> List[Transaction]:
    pass

if __name__ == '__main__':
  unittest.main()