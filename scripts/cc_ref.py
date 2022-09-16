import os
from datetime import datetime
from dal.coincodex import download_all_coins


today = datetime.today().strftime("%Y%m%d")
filepath = os.path.join("data", "ref", "cc", "ref_all_cc_{}.csv".format(today))
os.makedirs(os.path.dirname(filepath), exist_ok=True)

rdf = download_all_coins()
rdf.to_csv(filepath, sep=";", index=False)
