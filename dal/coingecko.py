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


def download_markets_by_page(page: int) -> pd.DataFrame:
    content = cg.get_coins_markets(
        vs_currency="usd", valid_values="market_cap_desc", per_page=250, page=page, price_change_percentage="1h,24h,7d,14d,30d,200d,1y")
    df = pd.DataFrame(content)
    df["page"] = page
    return df

# get_markets(page=1)


def _page_is_valid(page: float) -> bool:
    logging.debug("sleeping before getting page: {}".format(page))
    time.sleep(COINGECKO_THROTTLE)
    return len(download_markets_by_page(int(page))) > 0


def download_markets() -> pd.DataFrame:
    # binary search for the max number of pages
    _, page_max = highest_valid_binary_search(
        _page_is_valid, 1, 500, 4, low_valid=True, high_valid=False, lower_bound=False)

    today = datetime.now().strftime("%Y%m%d")
    output_dir = os.path.join("temp", "get_markets_all_pages_{}".format(today))
    os.makedirs(output_dir, exist_ok=True)

    dfs = []
    for page in range(1, page_max):
        filepath = os.path.join(
            output_dir, "cg_markets_{}_p{:03d}.csv".format(today, page))

        logging.debug("Sleeping before getting page: {:03d}.".format(page))
        time.sleep(COINGECKO_THROTTLE)
        df = download_markets_by_page(page)
        if len(df) > 0:
            df.to_csv(filepath, sep=";", index=False)
        else:
            logging.debug("0 len output from market. stop.")
            break

    return pd.concat(dfs)


def download_price_asofdate(id: str, as_of_date: datetime, versus_currency: str = "usd") -> float:
    content = cg.get_coin_history_by_id(
        id, date=as_of_date.strftime("%d-%m-%Y"))
    return content["market_data"]["current_price"].get(versus_currency, None)
