from senka.senka import Senka
import os
import sys


if __name__ == '__main__':
  args = sys.argv
  chain = args[1]
  address = args[2]  
  senka = Senka({"bscscan_key":os.environ['BSCSCAN_KEY']})
  caaj = senka.get_caaj(chain, address)
  print(caaj)