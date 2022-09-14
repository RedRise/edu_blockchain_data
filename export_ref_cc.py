import os
import pandas as pd
from datetime import datetime
import plotly.express as px

data_dir = os.path.expanduser(r"D:\to_del\bs_data\cc_mkt")

# utils functions -------------------------------------------------------------


def dollar_to_float(series: pd.Series) -> pd.Series:
    return (series.replace('[\$,]', '', regex=True).astype(float))


# read all files
dfs = []
for item in os.listdir(data_dir):
    # item = os.listdir(data_dir)[0]
    filepath = os.path.join(data_dir, item)
    if os.path.isfile(filepath):
        df = pd.read_csv(filepath, sep=";").reset_index(drop=True)
        del df["Unnamed: 0"]
        dfs.append(df)

# concat
df = pd.concat(dfs).reset_index(drop=True)
del (dfs)


# BTC historical price viz
df = df.set_index("date").sort_index()
df["price"] = dollar_to_float(df["price"])
fig = px.line(df.loc[df["ticker"] == "ETH"].reset_index(),
              x="date", y="price")
fig.show()

# there is ticker duplicates
sdf = df.groupby(["date", "ticker"])[
    "name"].count().reset_index().sort_values("name", ascending=False).head()
sdf
df.loc[(df.index == sdf.iloc[0]["date"]) & (
    df["ticker"] == sdf.iloc[0]["ticker"])]

# does'nt seem to have any name duplicates
df.groupby(["date", "name"])[
    df.columns[0]].count().reset_index().sort_values("name", ascending=False).head()

# Count unique names and tickers
for col in ["name", "ticker"]:
    print("Unique {0}s : {1}".format(col, len(df[col].unique())))

ref_cc = df.reset_index()[["ticker", "name"]].drop_duplicates()
filepath = os.path.join("data", "ref", "cc", "ref_cc_{}.csv".format(
    datetime.now().strftime("%Y%m%d")))
os.makedirs(os.path.dirname(filepath), exist_ok=True)
ref_cc.to_csv(filepath, sep=";", index=False)
