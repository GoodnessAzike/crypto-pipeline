from datetime import datetime, timezone
import requests
from raw import save_raw

def extract():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&per_page=10&page=1" #call the api
    response = requests.get(url)   # call the api endpoint
    fetched_at = datetime.now(timezone.utc)   # note the time
    response.raise_for_status()    #stop if it failed
    save_raw("coingecko", response.text, fetched_at)   # save the raw copy
    return response.json()      # hand the coin back to the loader