from pycoingecko import CoinGeckoAPI
from datetime import datetime
import numpy as np
import pandas as pd


cg = CoinGeckoAPI()

# historical prices
ddata = cg.get_coin_market_chart_by_id(id = "bitcoin", vs_currency="USD", days=250)

x = ddata["prices"][-1][0]

datetime.fromtimestamp(x / 1000)

dfs = []
for k in ddata.keys():
  dfs.append(pd.DataFrame(ddata["prices"], columns=["timestamp", k]).set_index("timestamp"))

df = pd.concat(dfs, axis=1)
df["id"] = "bitcoin"
df["numeraire"] = "usd"
df


# historical markets

mdata = cg.get_coins_markets(vs_currency="USD")
pd.DataFrame(mdata)
len(mdata)

