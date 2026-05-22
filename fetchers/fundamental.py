import requests
import os
# import json
from dotenv import load_dotenv


load_dotenv()
COIN_GEKO_API =  os.getenv("COIN_GEKO_API")


def get_fundamentals(ids:str = "bitcoin", pro_Plan: bool = False):
    if pro_Plan:
        Url_target = "https://pro-api.coingecko.com/api/v3/coins/{ids}".format(ids=ids)
    else:
        Url_target = "https://api.coingecko.com/api/v3/coins/{ids}".format(ids=ids)

    param = {
        "localization": "false",
        "tickers": "false",
        "community_data": "false",
        "developer_data": "false",
    }

    try:
        takeInformation = requests.get(Url_target,params=param)
        data = takeInformation.json()

        clean_fundamental = {
                    "Coin": ids.upper(),
                    "Price (USD)": data['market_data']['current_price']['usd'],
                    "Market Cap": data['market_data']['market_cap']['usd'],
                    "Volume 24h": data['market_data']['total_volume']['usd'],
                    "Change 24h (%)": data['market_data']['price_change_percentage_24h'],
                    "Circulating Supply": data['market_data']['circulating_supply']
                }
        return clean_fundamental
    
    except:
        print("Data failed to reach")
        return "maybe you have exceeded the API limit or the coin id is not correct"
        


print(get_fundamentals())


