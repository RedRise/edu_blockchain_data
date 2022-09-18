from nis import cat
import os
import pandas as pd
import time
from datetime import datetime
import dal.coingecko as cg
import dal.coincodex as cc
import logging

filepath = os.path.join("data", "temp", "ref_main_10.csv")
rdf = pd.read_csv(filepath, sep=";")

ccd = {}
cgd = {}


def get_prices(cc_ticker: str, cg_id: str):
    logging.debug("CC: {} - CG: {}".format(cc_ticker, cg_id))
    as_of_date = datetime(2021, 1, 10)

    cc_price = None
    try:
        _, cc_price = cc.download_price_asofdate(cc_ticker, as_of_date)
        ccd["cc_ticker"] = cc_price
    except:
        logging.error("Cant get CC price for: {}".format(cc_ticker))

    cg_price = None
    try:
        cg_price = cg.download_price_asofdate(cg_id, as_of_date)
        cgd["cg_id"] = cg_price
    except:
        logging.error("Cant get CG price for: {}".format(cg_id))

    time.sleep(2)
    return pd.Series([cc_price, cg_price])


logging.basicConfig(level=logging.DEBUG)
pdf = rdf.apply(lambda x: get_prices(x["cc-ticker"], x["cg-id"]), axis=1)
rdf[["cc_p", "cg_p"]] = pdf
# rdf.to_csv("temp.csv")
cc_ticker = "BSV"
get_prices("BTC", "bitcoin")
