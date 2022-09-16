import os
from pycoingecko import CoinGeckoAPI
from datetime import datetime
from utils.optim import highest_valid_binary_search
import pandas as pd
import time
import logging

COINGECKO_THROTTLE = 2

logging.basicConfig(level=logging.DEBUG)

cg = CoinGeckoAPI()


def get_markets(page: int) -> pd.DataFrame:
    content = cg.get_coins_markets(
        vs_currency="usd", valid_values="market_cap_desc", per_page=250, page=page, price_change_percentage="1h,24h,7d,14d,30d,200d,1y")
    df = pd.DataFrame(content)
    df["page"] = page
    return df

# get_markets(page=1)


def page_is_valid(page: float) -> bool:
    logging.debug("sleeping before getting page: {}".format(page))
    time.sleep(COINGECKO_THROTTLE)
    return len(get_markets(int(page))) > 0


# binary search for the max number of pages
_, page_max = highest_valid_binary_search(
    page_is_valid, 1, 500, 4, low_valid=True, high_valid=False, lower_bound=False)


today = datetime.now().strftime("%Y%m%d")

for page in range(1, page_max):
    filepath = os.path.join(
        "static", "output", "cg_markets_{}".format(today), "cg_markets_{}_p{:03d}.csv".format(today, page))
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    print(filepath)

    logging.debug("Sleeping before getting page: {:03d}.".format(page))
    time.sleep(COINGECKO_THROTTLE)
    df = get_markets(page)
    if len(df) > 0:
        df.to_csv(filepath, sep=";")
    else:
        logging.debug("0 len output from market. stop.")
        break
