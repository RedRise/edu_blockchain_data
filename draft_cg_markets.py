import os
from datetime import datetime
import pandas as pd


today = "20220914"  # datetime.now().strftime("%Y%m%d")

data_dir = os.path.join("static", "output", "cg_markets_{}".format(today))

dfs = []
for item in os.listdir(data_dir):
    filepath = os.path.join(data_dir, item)
    print(filepath)
    dfs.append(pd.read_csv(filepath, sep=";"))

df = pd.concat(dfs)

df[["id", "symbol", "name"]].nunique()


df.loc[df["id"].duplicated()]
df.loc[df["id"] == "penky"]["image"].to_list()
