from mimetypes import suffix_map
import os
import pandas as pd

# read cc ref file
filepath = os.path.join("data", "ref", "cc", "ref_cc_20220914.csv")
rcc = pd.read_csv(filepath, sep=";")

# build cg ref equivalent, from aggregated mkt file
filepath = os.path.join("data", "markets", "cg", "markets_cg_20220914.csv")
mcg = pd.read_csv(filepath, sep=";")
rcg = mcg[["id", "symbol"]].drop_duplicates()

rcg.nunique()
rcc.nunique()

# id proposal

rcc["name_upper"] = rcc["name"].str.upper()
rcg["id_upper"] = rcg["id"].str.upper()
rcg["id_upper_no_dash"] = rcg["id_upper"].str.replace("-", " ")

mref = rcc.set_index("name_upper") \
    .join(rcg.set_index("id_upper")["id"]) \
    .join(rcg.set_index("id_upper_no_dash")["id"], rsuffix="2")

mref.loc[mref["id"].isna() & mref["id2"].isna()]


no_match = set(rcc["name_upper"])
match_1 = no_match.intersection(set(rcg["id_upper"]))
no_match = no_match.remove(match_1)
match_2 =

.to_list().intersection
# 1) perfect match
# 2) - removal
rcg.set_index("id_upper")


rcc["match"] = rcc["name"].str.upper().apply(lambda x: x in cg_id)

tcc = rcc.loc[~ rcc["match"]].copy()

cg_id2 = rcg["id"].str.replace("-", " ").str.upper().to_list()
tcc["match"] = tcc["name"].str.upper().apply(lambda x: x in cg_id2)

tcc.loc[~ tcc["match"]].copy()

rcg.loc[rcg["id"].str.contains("ethereum")]
rcg.loc[rcg["id"].str.contains("agora")]

[x in cg_id for x in cc_id]
