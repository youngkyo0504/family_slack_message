import requests
import os


def get_risk_info(symbol):
    url = f"https://alphasquared.io/wp-json/as/v1/asset-info?symbol={symbol}"
    headers = {"Authorization": os.environ["ALPHASQUARED_API_KEY"]}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
