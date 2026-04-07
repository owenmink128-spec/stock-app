import yfinance as yf
import pandas as pd
import numpy as np

def check_trade(symbol="AAPL", box_period=30):
    data = yf.download(symbol, period="1mo", interval="5m")
    if len(data) < box_period:
        return None

    data['EMA50'] = data['Close'].ewm(span=50).mean()
    data['EMA200'] = data['Close'].ewm(span=200).mean()

    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

    high_low = data['High'] - data['Low']
    high_close = np.abs(data['High'] - data['Close'].shift())
    low_close = np.abs(data['Low'] - data['Close'].shift())
    true_range = np.maximum(high_low, np.maximum(high_close, low_close))
    data['ATR'] = true_range.rolling(14).mean()

    window = data.iloc[-box_period:]
    support = window['Low'].min()
    resistance = window['High'].max()

    last = data.iloc[-1]
    price = last['Close']
    rsi = last['RSI']
    trend_up = last['EMA50'] > last['EMA200']

    signals = []
    if price <= support * 1.01 and rsi < 35 and trend_up:
        signals.append("Bounce Buy")
    if price > resistance and trend_up:
        signals.append("Breakout Buy")

    return {
        "price": price,
        "support": support,
        "resistance": resistance,
        "trend_up": trend_up,
        "RSI": rsi,
        "signals": signals
    }
