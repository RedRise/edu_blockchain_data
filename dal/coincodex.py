import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date, datetime, timedelta
import logging

URL_HISTO_MARKETS = r"https://coincodex.com/historical-data/crypto/?date={0}"


nRank = "rank"
nTicker = "ticker"
nName = "name"
nPrice = "price"
nChange = "change"
nDatetime = "datetime"
nMktCap = "mktcap"
nVolume = "volume"


def _request_market_caps(date: datetime.date) -> bytes:
    req = requests.get(URL_HISTO_MARKETS.format(date.isoformat()))
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


def download_all_coins() -> pd.DataFrame:

    url = r"https://coincodex.com/apps/coincodex/cache/all_coins.json"
    req = requests.get(url)
    rdf = pd.DataFrame(req.json()).sort_values(
        "market_cap_rank", ascending=True).reset_index(drop=True)
    return rdf


def _get_coin_history(symbol: str, start: datetime.date, end: datetime.date, sample: int) -> pd.DataFrame:

    url = r"https://coincodex.com/api/coincodex/get_coin_history/{sym}/{start}/{end}/{sample}".format(
        sym=symbol,
        start=start.strftime("%Y-%m-%d"),
        end=end.strftime("%Y-%m-%d"),
        sample=sample)

    content = requests.get(url).json()
    rdf = pd.DataFrame(next(iter(content.values())))
    rdf[0] = rdf[0].apply(datetime.fromtimestamp)
    rdf.columns = [nDatetime, nPrice, nVolume, nMktCap]

    return rdf


def download_daily_prices(symbol, start: datetime.date, end: datetime.date) -> pd.DataFrame:

    pass


# start = datetime(2016, 1, 1)
# steps = 365
# rdf = _get_coin_history("BTC", start, start + timedelta(days=steps), steps+1)
# rdf

# next(iter({"f": 1}.values()))
# rdf = hp(20)
# rdf
# rdfrdf[0].apply(datetime.fromtimestamp)
