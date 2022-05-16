import datetime as dt
import math
import os
import re

import mplfinance as mpf
import numpy as np
import pandas as pd
from binance import (AsyncClient, Client, ThreadedDepthCacheManager,
                     ThreadedWebsocketManager)
from sklearn.linear_model import LinearRegression

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")


def get_start_date(period):
    today = dt.date.today()
    week_ago = today - dt.timedelta(days=period - 1)
    start_time = week_ago.strftime("%d %B %Y")
    return start_time


async def get_price_data(ticker, interval, period):
    client = await AsyncClient.create(API_KEY, API_SECRET)
    start_date = get_start_date(period)
    historical = await client.get_historical_klines(ticker, interval, start_date)
    await client.close_connection()
    df = pd.DataFrame(historical)
    return df


def find_indicator_fn(indicator, interval):
    exponents = {
        "1m": 1440,
        "3m": 480,
        "5m": 288,
        "15m": 96,
        "30m": 48,
        "1h": 24,
        "2h": 12,
        "4h": 6,
        "6h": 4,
        "8h": 3,
        "12h": 2,
        "1d": 1,
        "3d": 1/3,
        "1w": 1/7,
        "1M": 1/30.42,
    }
    exponent = exponents[interval]
    if "SMA" in indicator:
        return compute_sma, exponent
    elif "EMA" in indicator:
        return compute_ema, exponent
    else:
        return compute_macd, exponent


def compute_sma(df, period, exponent):
    if isinstance(exponent, float):
        window = int(math.ceil(period*exponent))
    else:
        window = period*exponent
    df.insert(
        df.columns.get_loc("Volume"), f"{period}SMA", df["Close"].rolling(window).mean()
    )
    return df


def compute_ema(df, period, exponent):
    if isinstance(exponent, float):
        window = int(math.ceil(period*exponent))
    else:
        window = period*exponent
    df.insert(
        df.columns.get_loc("Volume"),
        f"{period}EMA",
        df["Close"].ewm(span=window, adjust=False).mean(),
    )
    return df


def compute_macd(df, exponent):
    if isinstance(exponent, float):
        span_12 = int(math.ceil(12*exponent))
        span_26 = int(math.ceil(26*exponent))
        span_9 = int(math.ceil(9*exponent))
    else:
        span_12 = 12*exponent
        span_26 = 26*exponent
        span_9 = 9*exponent
    ema12 = df["Close"].ewm(span=span_12, adjust=False).mean()
    ema26 = df["Close"].ewm(span=span_26, adjust=False).mean()
    macd = ema12 - ema26
    df.insert(df.columns.get_loc("Volume"), "MACD", macd)
    df.insert(
        df.columns.get_loc("Volume"),
        "MACD Signal",
        macd.ewm(span=span_9, adjust=False).mean(),
    )
    df.insert(
        df.columns.get_loc("Volume"), "MACD Histogram", df["MACD"] - df["MACD Signal"]
    )
    return df


def process_price_data(df, indicators, interval):
    df.columns = [
        "Open time",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "Close time",
        "Quote asset volume",
        "Number of trades",
        "Taker buy base asset volume",
        "Taker buy quote asset volume",
        "Ignore",
    ]
    df.drop(
        [
            "Close time",
            "Quote asset volume",
            "Taker buy base asset volume",
            "Taker buy quote asset volume",
            "Ignore",
        ],
        axis=1,
        inplace=True,
    )

    df["Open time"] = df["Open time"].apply(lambda d: pd.to_datetime(d, unit="ms"))

    df.rename(columns={"Open time": "Date"}, inplace=True)
    df.set_index("Date", inplace=True)
    numeric_cols = ["Open", "High", "Low", "Close", "Volume", "Number of trades"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, axis=1)

    for indicator in indicators:
        indicator_fn, exponent = find_indicator_fn(indicator, interval)
        if indicator == "MACD":
            indicator_fn(df, exponent)
        else:
            indicator_period = list(map(int, re.findall(r"\d+", indicator)))[0]
            indicator_fn(df, indicator_period, exponent)
    return df


def plot(df, ticker, style, volume):
    mc = mpf.make_marketcolors(
        up="#77DD77",
        down="#FF6961",
        wick={"up": "#77DD77", "down": "#FF6961"},
        volume="inherit",
    )
    style_sheet = mpf.make_mpf_style(
        base_mpl_style="dark_background",
        marketcolors=mc,
        facecolor="#36393E",
        edgecolor="#FFFFFF",
        figcolor="#36393E",
    )
    volume_panel = 1
    if "MACD" in df.columns:
        apds = [
            mpf.make_addplot(
                df.iloc[
                    :, df.columns.get_loc("Close") + 1 : df.columns.get_loc("Volume")
                ].drop(["MACD Histogram", "MACD", "MACD Signal"], axis=1)
            ),
            mpf.make_addplot(
                df["MACD Histogram"],
                panel=1,
                color="#FFFFFF",
                alpha=0.3,
                type="bar",
                secondary_y=False,
            ),
            mpf.make_addplot(df["MACD"], panel=1, color="#AEC6CF", ylabel="MACD"),
            mpf.make_addplot(
                df["MACD Signal"], panel=1, color="#FF6961", ylabel="MACD Signal"
            ),
        ]
        if volume:
            volume_panel = 2
    else:
        apds = mpf.make_addplot(
            df.iloc[:, df.columns.get_loc("Close") + 1 : df.columns.get_loc("Volume")]
        )
    fig, axes = mpf.plot(
        df,
        addplot=apds,
        type=style,
        volume=volume,
        volume_panel=volume_panel,
        style=style_sheet,
        returnfig=True,
    )
    axes[0].set_title(ticker)

    legend_label = list(
        df.iloc[:, df.columns.get_loc("Close") : df.columns.get_loc("Volume")].columns
    )

    if style == "candle":
        legend_label = list(
            df.iloc[
                :, df.columns.get_loc("Close") + 1 : df.columns.get_loc("Volume")
            ].columns
        )

    if "MACD" in df.columns:
        legend_label.remove("MACD Histogram")
        legend_label.remove("MACD")
        legend_label.remove("MACD Signal")

        MACD_Line = axes[2].lines[0]
        MACD_Signal_Line = axes[3].lines[0]
        MACD_Line.set_label("MACD")
        MACD_Signal_Line.set_label("Signal Line")

    for i, line in enumerate(axes[0].lines):
        line.set_label(legend_label[i])

    fig.legend()
    fig.set_size_inches(14, 8)
    fig.savefig("plot.png")
    return
