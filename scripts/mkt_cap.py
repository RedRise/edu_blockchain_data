import os
import argparse
from datetime import datetime
from utils.datetime import range_end_of_month
from dal.coincodex import download_market_caps
import time


for eom in range_end_of_month(datetime(2017, 4, 1).date()):
    print(eom)
    df = download_market_caps(eom)
    filepath = os.path.join(
        "static", "output", "{0}_mktcap_coincodex.csv".format(eom.strftime("%Y%m%d")))
    print(filepath)
    df.to_csv(filepath, sep=";")
    time.sleep(61)
