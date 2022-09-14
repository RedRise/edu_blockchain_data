from operator import index
import os
import pandas as pd

filepath = os.path.join("data", "ref", "cc", "ref_cc_20220914.csv")
rcc = pd.read_csv(filepath, sep=";")

filepath = os.path.join("data", "markets", "cg", "markets_cg_20220914.csv")
mcg = pd.read_csv(filepath, sep=";")
rcg = mcg[["id", "symbol"]].drop_duplicates()


rcg.nunique()
rcc.nunique()

cg_id = rcg["id"].str.upper().to_list()


# 1) perfect match
# 2) - removal
rcc["match"] = rcc["name"].str.upper().apply(lambda x: x in cg_id)

tcc = rcc.loc[~ rcc["match"]].copy()

cg_id2 = rcg["id"].str.replace("-", " ").str.upper().to_list()
tcc["match"] = tcc["name"].str.upper().apply(lambda x: x in cg_id2)

tcc.loc[~ tcc["match"]].copy()

rcg.loc[rcg["id"].str.contains("ethereum")]
rcg.loc[rcg["id"].str.contains("agora")]

[x in cg_id for x in cc_id]
