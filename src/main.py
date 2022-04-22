from senka.senka import Senka
import os
import sys


if __name__ == '__main__':
  args = sys.argv
  chain = 'osmosis'
  address = 'osmo1xcqshxpmhdc4tfcscxpmdlt9kwql6qm5wc9ger'
  setting = {}
  if chain == 'bsc':
    setting['bscscan_key'] = os.environ['BSCSCAN_KEY']
  senka = Senka(setting, '../pyproject.toml')
  # caaj = senka.get_caaj_csv(chain, address)
  caaj = senka.get_caaj_csv(chain, address, starttime=1650608478, endtime=1650608827)
  print(caaj)
