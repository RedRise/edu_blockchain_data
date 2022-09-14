import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import logging

COINCODEX_URL = r"https://coincodex.com/historical-data/crypto/?date={0}"


nRank = "rank"
nTicker = "ticker"
nName = "name"
nPrice = "price"
nChange = "change"


def _request_market_caps(date: datetime.date) -> bytes:
    req = requests.get(COINCODEX_URL.format(date.isoformat()))
    if req.status_code != 200:
        logging.error("CoinCodex get request failed", req.status_code)
        return None

    return req.content


def _parse_market_cap_content(content: bytes) -> pd.DataFrame:
    soup = BeautifulSoup(content, "html.parser")

    html_table = soup.find(class_="coins snapshot")
    # html_head = html_table.find("tr")
    html_body = html_table.findAll("tr")[1:]

    data_body = []
    for row in html_body:
        # row = html_body[0]
        row_dc = {}
        change_count = 0
        for cell in row:
            classes = [x.lower() for x in cell.attrs["class"]]
            if "name" in classes:
                row_dc["ticker"] = cell.find(class_="ticker").text.strip()
                row_dc["name"] = cell.find(class_="full-name").text.strip()
            elif "change" in classes:
                row_dc["change_{}".format(
                    change_count)] = cell.get_text().strip()
                change_count += 1
            else:
                row_dc[classes[0]] = cell.get_text().strip()

        data_body.append(row_dc)

    df = pd.DataFrame(data=data_body)
    return df


# for col in ["price", "mkt-cap"]
# df["market-cap"].replace('[\$,]', '', regex=True).astype(float)


def download_market_caps(date: datetime.date) -> pd.DataFrame:
    content = _request_market_caps(date)
    if not content:
        return None

    df = _parse_market_cap_content(content)
    df["date"] = date
    return df
