import os
from datetime import datetime
import pandas as pd


today = "20220914"  # datetime.now().strftime("%Y%m%d")

data_dir = os.path.join("static", "output", "cg_markets_{}".format(today))
# data_dir = r"D:\to_del\bs_data\cg_mkt"

# read df for each page
dfs = []
for item in os.listdir(data_dir):
    filepath = os.path.join(data_dir, item)
    print(filepath)
    dfs.append(pd.read_csv(filepath, sep=";"))

# concat and clean
df = pd.concat(dfs).reset_index()
df["date"] = datetime.today().date()

for col in ["index", "image", "Unnamed: 0"]:
    del df[col]

# export to csv
df.to_csv("markets_cg_{}.csv".format(today), sep=";", index=False)
