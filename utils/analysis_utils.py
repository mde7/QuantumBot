import os

import re

from binance import (
    AsyncClient,
    Client,
    ThreadedDepthCacheManager,
    ThreadedWebsocketManager,
)

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")


async def parseGraphArg(args: str):
    parsed_args = args.split(" ")
    try:
        style = parsed_args[0]
        ticker = parsed_args[1]
        period = int(parsed_args[2])
        interval = parsed_args[3]
        volume = parsed_args[4]
        indicator = parsed_args[5:]
    except:
        return [None for _ in range(6)]
    else:
        style = check_style(style)
        ticker = await check_ticker(ticker)
        period = check_period(period)
        interval = check_interval(period, interval)
        volume = check_volume(volume)
        indicator = check_indicator(period, indicator)

        return style, ticker, period, interval, volume, indicator


def check_style(style: str):
    if style == "line" or style == "candle":
        return style
    return None


async def check_ticker(ticker: str):
    client = await AsyncClient.create(API_KEY, API_SECRET)
    info = await client.get_symbol_info(ticker)
    await client.close_connection()
    if info is not None:
        return ticker
    return None


def check_period(period: int):
    if 500 > period >= 1:
        return period
    return None


def check_interval(period: int, interval: str):
    valid_intervals = {
        "1m": 1,
        "3m": 1,
        "5m": 1,
        "15m": 1,
        "30m": 1,
        "1h": 1,
        "2h": 1,
        "4h": 1,
        "6h": 1,
        "8h": 1,
        "12h": 1,
        "1d": 2,
        "3d": 4,
        "1w": 8,
        "1M": 32,
    }
    if interval in valid_intervals and period >= valid_intervals[interval]:
        return interval
    return None


def check_volume(volume: str):
    if volume.lower() == "y":
        return True
    elif volume.lower() == "n":
        return False
    else:
        return None


def check_indicator(period: int, indicators: list):
    valid_indicators = ["MACD", "SMA", "EMA"]
    indicators = list(set(indicators))
    if len(indicators) == 0:
        return indicators
    if ("MACD" in indicators and len(indicators) > 4) or (
        "MACD" not in indicators and len(indicators) > 3
    ):
        return None
    all_valid = [False for _ in range(len(indicators))]
    for index, indicator in enumerate(indicators):
        if indicator == valid_indicators[0]:
            all_valid[index] = True
        elif any(ind in indicator for ind in valid_indicators[1:]):
            indicator_period = list(map(int, re.findall(r"\d+", indicator)))
            if len(indicator_period) == 0:
                all_valid[index] = False
            elif (period > indicator_period[0]) and len(indicator_period) == 1:
                all_valid[index] = True
        else:
            all_valid[index] = False

    if all(all_valid):
        return indicators
    else:
        return None


def parseSuggestArg(args: str):
    try:
        quality = args
    except:
        return [None for _ in range(1)]
    else:
        quality = check_type(quality)

        return quality


def check_type(quality: str):
    if quality.lower() == "default":
        return "default"
    elif quality.lower() == "w":
        return "w"
    elif quality.lower() == "l":
        return "l"
    else:
        return None
