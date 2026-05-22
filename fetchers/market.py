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


def makeTable():
    df = pd.DataFrame(rawData, columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime', 'QuoteAssetVolume', 'Trades', 'TakerBuyBase', 'TakerBuyQuote', 'Ignore'])
    df= df.iloc[:, 0:6]
    df = df.astype(float) #change into float
    df['Time'] = pd.to_datetime(df["Time"], unit='ms') 

    delta = df['Close'].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    window_length = 14 # per 2 weekly data, we use 14 as window length
    avg_gain = gain.ewm(com=window_length-1, min_periods=window_length).mean()
    avg_loss = loss.ewm(com=window_length-1, min_periods=window_length).mean()
    rs = avg_gain / avg_loss

    df['RSI_14'] = 100 - (100 / (1 + rs))
    return df

print(makeTable())
        
    