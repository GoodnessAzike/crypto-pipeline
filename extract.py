import requests


def extract():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&per_page=10&page=1"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()