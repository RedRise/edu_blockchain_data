import os
import pandas as pd
from strsimpy.jaro_winkler import JaroWinkler

# read cc ref file
filepath = os.path.join("data", "ref", "cc", "ref_cc_20220914.csv")
rcc = pd.read_csv(filepath, sep=";")

# build cg ref equivalent, from aggregated mkt file
filepath = os.path.join("data", "markets", "cg", "markets_cg_20220914.csv")
mcg = pd.read_csv(filepath, sep=";")
rcg = mcg[["id", "symbol"]].drop_duplicates()

rcg.nunique()
rcc.nunique()

# 1) perfect match
# 2) match without dash
rcc["name_upper"] = rcc["name"].str.upper()
rcg["id_upper"] = rcg["id"].str.upper()
rcg["id_upper_no_dash"] = rcg["id_upper"].str.replace("-", " ")

mref = rcc.set_index("name_upper") \
    .join(rcg.set_index("id_upper")["id"]) \
    .join(rcg.set_index("id_upper_no_dash")["id"], rsuffix="2")


# 3) guesses best matches
# see : https://github.com/luozhouyang/python-string-similarity#jaro-winkler

# define matching mechanics
sim_model = JaroWinkler()
guesses_df = rcg.set_index("id")


def str_best_match(x: str) -> str:
    x = x.upper()
    return guesses_df["id_upper"].apply(lambda y: sim_model.similarity(x, y)).idxmax()


nomatch_df = mref.loc[mref[["id", "id2"]].isna().all(axis=1)
                      ]["name"].copy().to_frame()
nomatch_df["id3"] = nomatch_df.reset_index()["name_upper"].apply(
    lambda x: str_best_match(x)).to_list()

# combine and write
mref = mref.join(nomatch_df["id3"])
mref.reset_index()
filepath = os.path.join("data", "ref", "main", "ref_main.csv")
os.makedirs(os.path.dirname(filepath), exist_ok=True)
mref.to_csv(filepath, sep=";", index=False)


nomatch_df.loc["VALIDITY"]
mref.loc["VALIDITY"]
rcg.set_index("id").loc["ripple"]
rcg.loc[rcg["id"].apply(lambda x: 'valid' in x)]
