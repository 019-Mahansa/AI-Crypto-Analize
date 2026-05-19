# import requests

# def get_chart(symbol:str = "BTCUSDT", interval:str = "1d", limit:int = 5):
#     URL_target = "https://data-api.binance.vision/api/v3/klines"

#     param = {
#         'symbol': symbol,
#         'interval': interval,
#         'limit': limit
#     }
    
#     takeINformation = requests.get(URL_target,params=param)

#     return takeINformation.json()

# dataMentah = get_chart()

# for arr in dataMentah:
#     print(float(arr[4]))

    