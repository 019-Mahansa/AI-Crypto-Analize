import requests
import pandas as pd

def get_chart(symbol:str = "BTCUSDT", interval:str = "1d", limit:int = 100):
    URL_target = "https://data-api.binance.vision/api/v3/klines"

    param = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }
    
    takeInformation = requests.get(URL_target,params=param)

    return takeInformation.json()

rawData = get_chart()

# for arr in dataMentah:
#     print(float(arr[4]))
def makeTable():
    df = pd.DataFrame(rawData, columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime', 'QuoteAssetVolume', 'Trades', 'TakerBuyBase', 'TakerBuyQuote', 'Ignore'])
    df= df.iloc[:, 0:6]
    df = df.astype(float) #change into float
    df['Time'] = pd.to_datetime(df["Time"], unit='ms') #
    return df

print(makeTable())
        
    