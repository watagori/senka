import os
import sys
from pathlib import Path

from senka.senka import Senka

if __name__ == "__main__":
    args = sys.argv
    # chain = args[1]
    # address = args[2]
    # chain = "osmosis"
    # address = "osmo175na5rxm3y7e2ejhnxfasgwf68q2uz9cdfavj6"
    # caaj = senka.get_caaj_csv(chain, address)

    setting = {}
    chain = "bitbank"
    if chain == "bsc":
        setting["bscscan_key"] = os.environ["BSCSCAN_KEY"]
    senka = Senka(setting, "./pyproject.toml")
    data = Path(
        "%s/../test/testdata/bitbank/bitbank_exchange.csv" % os.path.dirname(__file__)
    ).read_text()

    caaj = senka.get_caaj_from_data(chain, data)
    print(caaj)
