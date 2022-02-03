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

class TestSenka(unittest.TestCase):
  def test_get_available_chains(self):
    with patch.object(SenkaLib, 'get_available_chain', new=TestSenka.mock_get_available_chains):
      senka = Senka({})
      chains = senka.get_available_chains()
      assert chains[0] == 'test_one'
      assert chains[1] == 'test_zero'

  def test_get_caaj_no_chain(self):
    with patch.object(SenkaLib, 'get_available_chain', new=TestSenka.mock_get_available_chains):
      with self.assertRaises(ValueError):
        senka = Senka({})
        caaj = senka.get_caaj('no_existence_chain', '0xfFceBED170CE0230D513a0a388011eF9c2F97503')

  def test_get_caaj(self):
    with patch.object(SenkaLib, 'get_available_chain', new=TestSenka.mock_get_available_chains):
      with patch.object(Senka, 'get_plugin_dir_path', new=TestSenka.mock_get_plugin_dir_path):
        senka = Senka({})
        caaj_list = senka.get_caaj('test_one', '0xfFceBED170CE0230D513a0a388011eF9c2F97503')
        cj = caaj_list[0]
        assert len(caaj_list) == 2
        assert cj.time == "2022-01-01 00:00:00"
        assert cj.platform == "test_platform"
        assert cj.transaction_id == "0x1111111111111111111111111111"
        assert cj.comment == "no comment"
        assert cj.debit_from == "0x0000000000000"
        assert cj.debit_to == "0x11111111111"
        assert cj.credit_from == "0x22222222222"
        assert cj.credit_to == "0x33333333333"
        assert cj.debit_title == "SPOT"
        assert cj.debit_amount == {"TESTONE": "10"}
        assert cj.credit_title == "SPOT"
        assert cj.credit_amount == {"TESTONE": "10"}

  def test_get_caaj_csv(self):
    with patch.object(SenkaLib, 'get_available_chain', new=TestSenka.mock_get_available_chains):
      with patch.object(Senka, 'get_plugin_dir_path', new=TestSenka.mock_get_plugin_dir_path):
        senka = Senka({})
        caaj_csv = senka.get_caaj_csv('test_one', '0xfFceBED170CE0230D513a0a388011eF9c2F97503')
        caaj_csv_lines = caaj_csv.splitlines()
        assert len(caaj_csv_lines) == 3
        assert caaj_csv_lines[0] == 'time,platform,transaction_id,comment,debit_from,debit_to,\
credit_from,credit_to,debit_title,debit_amount,credit_title,credit_amount'
        assert caaj_csv_lines[1] == '2022-01-01 00:00:00,test_platform,0x1111111111111111111111111111,\
no comment,0x0000000000000,0x11111111111,0x22222222222,0x33333333333,SPOT,{\'TESTONE\': \'10\'},SPOT,{\'TESTONE\': \'10\'}'
        assert caaj_csv_lines[2] == '2022-01-01 00:00:00,test_platform,0x1111111111111111111111111111,\
no comment,0x0000000000000,0x11111111111,0x22222222222,0x33333333333,SPOT,{\'TESTONE\': \'10\'},SPOT,{\'TESTONE\': \'10\'}'

  @classmethod
  def mock_get_available_chains(cls):
    return [TestOneTransactionGenerator, TestZeroTransactionGenerator]

  @classmethod
  def mock_get_plugin_dir_path(cls):
    return '%s/plugin' % os.path.dirname(__file__)

class TestOneTransactionGenerator(TransactionGenerator):
  chain = 'test_one'
  @classmethod
  def get_transactions(cls, settings:SenkaSetting, address:str, timerange:dict = None, blockrange:dict = None) -> List[Transaction]:
    header = json.loads(Path('%s/testdata/header.json' % os.path.dirname(__file__)).read_text())
    receipt = json.loads(Path('%s/testdata/approve.json' % os.path.dirname(__file__)).read_text())
    transaction_a = TestOneTransaction(header['hash'], receipt, header['timeStamp'], header['gasUsed'], header['gasPrice'])
    transaction_b = TestOneTransaction(header['hash'], receipt, header['timeStamp'], header['gasUsed'], header['gasPrice'])
    return [transaction_a, transaction_b]

class TestOneTransaction(Transaction):
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

class TestZeroTransactionGenerator(TransactionGenerator):
  chain = 'test_zero'
  @classmethod
  def get_transactions(cls, settings:SenkaSetting, address:str, timerange:dict = None, blockrange:dict = None) -> List[Transaction]:
    pass

if __name__ == '__main__':
  unittest.main()