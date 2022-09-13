import os
from dal.coincodex import _parse_market_cap_content


def get_coincodex_mock_html():
    filepath = os.path.join("static", "tests", "mock", "coincodex.html")
    with open(filepath, "r") as file:
        return file.read()


def test_parse_table():
    req_content = get_coincodex_mock_html()
    df = _parse_market_cap_content(req_content)
    assert df.iloc[0]["name"] == "Bitcoin"
    assert len(df) == 100
