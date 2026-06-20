import requests
import pandas as pd
import pandas_ta_classic as ta
import os
import sys
from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.abspath("."))

from utils import promptUser2


def get_chart(symbol:str = "BTCUSDT", interval:str = "1d", limit:int = 200):
    URL_target = "https://data-api.binance.vision/api/v3/klines"

    param = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }
    
    takeInformation = requests.get(URL_target,params=param)

    return takeInformation.json()

inputText = promptUser2()
rawData = get_chart(symbol=f"{inputText.upper()}USDT")


def makeTable():
    df = pd.DataFrame(rawData, columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime', 'QuoteAssetVolume', 'Trades', 'TakerBuyBase', 'TakerBuyQuote', 'Ignore'])
    df= df.iloc[:, 0:6]
    df = df.astype(float) #change into float
    df['Time'] = pd.to_datetime(df["Time"], unit='ms') 


    df.ta.rsi(close='Close', length=60, append=True)


    df.ta.ema(close='Close', length=20, append=True)
    df.ta.ema(close='Close', length=50, append=True)
    df.ta.ema(close='Close', length=200, append=True)


    df.ta.atr(close='Close', append=True)


    df.ta.bbands(close='Close', length=20, std=3, append=True)


    df.ta.stoch(high='High', low='Low', close='Close', k=60, d=3, append=True, suffix='_STOCH60')
    return df

print(makeTable())
        
    