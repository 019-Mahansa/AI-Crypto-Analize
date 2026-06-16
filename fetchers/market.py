import requests
import pandas as pd
import pandas_ta_classic as ta
import os
import sys
from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.abspath("."))

from utils import promptUser2


def get_chart(symbol:str = "SOLUSDT", interval:str = "1d", limit:int = 100):
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

    delta = df['Close'].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    window_length = 60 # per 2 weekly data, we use 14 as window length
    avg_gain = gain.ewm(com=window_length-1, min_periods=window_length).mean()
    avg_loss = loss.ewm(com=window_length-1, min_periods=window_length).mean()
    rs = avg_gain / avg_loss

    # RSI
    df['RSI_60'] = 100 - (100 / (1 + rs))

    # SIMPLE MOVING AVERAGE 
    df['sma_20'] = ta.sma(df['Close'], length=20)
    df['sma_60'] = ta.sma(df['Close'], length=60)
    # df['sma_100'] = ta.sma(df['Close'], length=100)

    # Stockhastic
    df['Stockhastic'] = ta.stoch(df['Close'], length=60)

    return df

print(makeTable())
        
    