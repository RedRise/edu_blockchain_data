from multiprocessing.resource_sharer import DupFd
import os
from datetime import datetime
from utils.datetime import range_end_of_month
from dal.coincodex import download_market_caps
import time

for eom in range_end_of_month(datetime(2016, 1, 1).date()):
    # eom = datetime(2020, 8, 8)
    print(eom)
    df = download_market_caps(eom)
    filepath = os.path.join(
        "static", "output", "markets_cc_{}.csv".format(eom.strftime("%Y%m%d")))
    # os.makedirs(os.path.dirname(filepath))
    print(filepath)
    df.to_csv(filepath, sep=";", index=False)
    time.sleep(5)
