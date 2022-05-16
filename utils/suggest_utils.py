import datetime as dt
import os
import re
from statistics import mean

import numpy as np
import pandas as pd
from binance import (
    AsyncClient,
    Client,
    ThreadedDepthCacheManager,
    ThreadedWebsocketManager,
)
from scipy import stats

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
client = Client(API_KEY, API_SECRET)


def get_start_date(period):
    today = dt.date.today()
    week_ago = today - dt.timedelta(days=period - 1)
    start_time = week_ago.strftime("%d %B %Y")
    return start_time


def check_ticker(ticker):
    quote = ["GBP", "USDT"]
    if any(ticker["symbol"].endswith(currency) for currency in quote):
        return True
    return False


async def get_tickers():
    client = await AsyncClient.create(API_KEY, API_SECRET)
    tickers = await client.get_all_tickers()
    await client.close_connection()
    filtered_tickers = list(
        map(lambda x: x["symbol"], list((filter(check_ticker, tickers))))
    )
    return filtered_tickers


def compute_price_change(today_close, last_close):
    return ((today_close - last_close) / last_close) * 100


async def process_ticker_data(tickers):
    ticker = []
    price = []

    oney_price_change = []
    oney_percentilescore = []

    sixm_price_change = []
    sixm_percentilescore = []

    threem_price_change = []
    threem_percentilescore = []

    onem_price_change = []
    onem_percentilescore = []

    momentum_score = []

    client = await AsyncClient.create(API_KEY, API_SECRET)

    for symbol in tickers:
        historical = await client.get_historical_klines(
            symbol, "1M", get_start_date(365)
        )

        if len(historical) != 12:
            continue

        ticker.append(symbol)

        today_close = float(historical[len(historical) - 1][4])

        price.append(today_close)

        oney_price = float(historical[0][4])
        sixm_price = float(historical[5][4])
        threem_price = float(historical[8][4])
        onem_price = float(historical[10][4])

        oney_price_change.append(compute_price_change(today_close, oney_price))
        sixm_price_change.append(compute_price_change(today_close, sixm_price))
        threem_price_change.append(compute_price_change(today_close, threem_price))
        onem_price_change.append(compute_price_change(today_close, onem_price))

    await client.close_connection()

    for oney_score, sixm_score, threem_score, onem_score in zip(
        oney_price_change, sixm_price_change, threem_price_change, onem_price_change
    ):
        oney_percentilescore.append(
            stats.percentileofscore(oney_price_change, oney_score) / 100
        )
        sixm_percentilescore.append(
            stats.percentileofscore(sixm_price_change, sixm_score) / 100
        )
        threem_percentilescore.append(
            stats.percentileofscore(threem_price_change, threem_score) / 100
        )
        onem_percentilescore.append(
            stats.percentileofscore(onem_price_change, onem_score) / 100
        )

    for oney_score, sixm_score, threem_score, onem_score in zip(
        oney_percentilescore,
        sixm_percentilescore,
        threem_percentilescore,
        onem_percentilescore,
    ):
        momentum_score.append(mean([oney_score, sixm_score, threem_score, onem_score]))

    df = pd.DataFrame(
        {
            "Symbol": ticker,
            "Price": price,
            "1Year Price Change": oney_price_change,
            "1Year Change Percentile": oney_percentilescore,
            "6Months Price Change": sixm_price_change,
            "6Months Change Percentile": sixm_percentilescore,
            "3Months Price Change": threem_price_change,
            "3Months Change Percentile": threem_percentilescore,
            "1Month Price Change": onem_price_change,
            "1Month Change Percentile": onem_percentilescore,
            "Momentum Score": momentum_score,
        }
    )
    df.sort_values(by=["Momentum Score"], ascending=False, inplace=True)

    return df


def display(df, quality):
    df["Price"] = df["Price"].round(2)
    df["Momentum Score"] = df["Momentum Score"].round(2)

    if quality == "default" or quality == "w":
        data = df.head(20)
    else:
        data = df.tail(10)

    symbols = "\n".join(str(f"`{_}`") for _ in data["Symbol"].to_list())
    prices = "\n".join(str(f"`${_}`") for _ in data["Price"].to_list())
    score = "\n".join(str(f"`{_}`") for _ in data["Momentum Score"].to_list())

    return symbols, prices, score
