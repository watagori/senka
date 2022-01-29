import unittest
from unittest.mock import *
from senka.senka import Senka
import os

class TestSenka(unittest.TestCase):
  def test_get_available_chains(self):
    senka = Senka({})
    chains = senka.get_available_chains()
    assert chains[0] == 'bsc'
    assert chains[1] == 'osmosis'

  def test_get_caaj(self):
    senka = Senka({"bscscan_key":os.environ['BSCSCAN_KEY']})
    caaj = senka.get_caaj('bsc', '0xfFceBED170CE0230D513a0a388011eF9c2F97503')
    print(caaj)

if __name__ == '__main__':
  unittest.main()