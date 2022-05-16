import logging

from arsenic import browsers, get_session, keys, services


async def get_crypto_data(currency):
    data = {
        "symbol": "No Data",
        "name": "No Data",
        "rank": "No Data",
        "price": "No Data",
        "price_change": "No Data",
        "price_change_percent": "No Data",
        "price_low": "No Data",
        "price_high": "No Data",
        "trading_volume": "No Data",
        "trading_volume_percent": "No Data",
        "market_cap": "No Data",
        "market_cap_percent": "No Data",
        "volume_to_market_cap": "No Data",
        "market_dominance": "No Data",
        "crypto_logo": None,
        "whitepaper_url": None,
        "info_url": None,
    }

    service = services.Chromedriver(
        binary=r"C:\Users\mdema\Documents\chromedriver_win32\chromedriver.exe"
    )
    browser = browsers.Chrome()
    browser.capabilities = {
        "goog:chromeOptions": {"args": ["--headless", "--disable-gpu"]}
    }
    async with get_session(service, browser) as session:
        await session.get("https://coinmarketcap.com/")
        search_icon = await session.wait_for_element(15, ".sc-16r8icm-0.jZwKai")
        await search_icon.click()
        search_bar = await session.wait_for_element(15, ".bzyaeu-3.jUraic")
        await search_bar.send_keys(f"{currency}{keys.ENTER}")

        if await session.get_url() == "https://coinmarketcap.com/":
            return data

        data["name"], data["symbol"] = await get_symbol_name(session)
        data["rank"] = await get_rank(session)
        data["price"] = await get_price(session)
        data["price_change"], data["price_change_percent"] = await get_price_change(
            session
        )
        data["price_low"], data["price_high"] = await get_price_low_high(session)
        (
            data["trading_volume"],
            data["trading_volume_percent"],
        ) = await get_trading_volume(session)
        data["market_cap"], data["market_cap_percent"] = await get_market_cap(session)
        data["volume_to_market_cap"] = await get_volume_to_market_cap(session)
        data["market_dominance"] = await get_market_dominance(session)
        data["crypto_logo"] = await get_crypto_logo(session)
        data["whitepaper_url"] = await get_whitepaper(session)
        data["info_url"] = await get_info_url(session)

        await session.close()

    return data


async def get_symbol_name(session):
    try:
        element = await session.wait_for_element(15, ".sc-1q9q90x-0.jCInrl.h1")
        name_symbol = await element.get_text()
        elements = name_symbol.split("\n")
        return elements[0], elements[1]
    except:
        return "No Data", "No Data"


async def get_rank(session):
    try:
        element = await session.wait_for_element(15,
            ".sc-16r8icm-0.nds9rn-0.dAxhCK div:first-of-type table tbody tr:last-child td"
        )
        rank = await element.get_property("textContent")
        return rank
    except:
        return "No Data"


async def get_price(session):
    try:
        element = await session.wait_for_element(15,
            ".sc-16r8icm-0.nds9rn-0.dAxhCK div:first-of-type table tbody tr:first-child td"
        )
        price = await element.get_property("textContent")
        return price
    except:
        return "No Data"


async def get_price_change(session):
    try:
        pc_element = await session.wait_for_element(15,
            ".sc-16r8icm-0.nds9rn-0.dAxhCK div:first-of-type table tbody tr:nth-child(2) td span:first-child"
        )
        price_change = await pc_element.get_property("textContent")

        pcp_element = await session.wait_for_element(15,
            ".sc-16r8icm-0.nds9rn-0.dAxhCK div:first-of-type table tbody tr:nth-child(2) td span:last-child"
        )
        price_change_percent = await pcp_element.get_property("textContent")

        sign_element = await session.wait_for_element(15,
            ".sc-16r8icm-0.nds9rn-0.dAxhCK div:first-of-type table tbody tr:nth-child(2) td span:last-child span"
        )
        sign = await sign_element.get_property("className")

        if sign == "icon-Caret-up":
            price_change_percent = "↑" + price_change_percent
        else:
            price_change_percent = "↓" + price_change_percent

        return price_change, price_change_percent
    except:
        return "No Data", "No Data"


async def get_price_low_high(session):
    try:
        element = await session.wait_for_element(15,
            ".sc-16r8icm-0.nds9rn-0.dAxhCK div:first-of-type table tbody tr:nth-child(3) td"
        )
        price_change_percent = await element.get_property("textContent")
        elements = price_change_percent.split(" /")
        return elements[0], elements[1]
    except:
        return "No Data", "No Data"


async def get_trading_volume(session):
    try:
        tv_element = await session.wait_for_element(15,
            ".sc-16r8icm-0.nds9rn-0.dAxhCK div:first-of-type table tbody tr:nth-child(4) td span:first-child"
        )
        trading_volume = await tv_element.get_property("textContent")

        tvp_element = await session.wait_for_element(15,
            ".sc-16r8icm-0.nds9rn-0.dAxhCK div:first-of-type table tbody tr:nth-child(4) td span:last-child"
        )
        trading_volume_percent = await tvp_element.get_property("textContent")

        sign_element = await session.wait_for_element(15,
            ".sc-16r8icm-0.nds9rn-0.dAxhCK div:first-of-type table tbody tr:nth-child(4) td span:last-child span"
        )
        sign = await sign_element.get_property("className")

        if sign == "icon-Caret-up":
            trading_volume_percent = "↑" + trading_volume_percent
        else:
            trading_volume_percent = "↓" + trading_volume_percent

        return trading_volume, trading_volume_percent
    except:
        return "No Data", "No Data"


async def get_market_cap(session):
    try:
        mc_element = await session.wait_for_element(15,
            ".sc-16r8icm-0.nds9rn-0.dAxhCK div:nth-of-type(2) table tbody tr:first-child td span:first-child"
        )
        market_cap = await mc_element.get_property("textContent")

        mcp_element = await session.wait_for_element(15,
            ".sc-16r8icm-0.nds9rn-0.dAxhCK div:nth-of-type(2) table tbody tr:first-child td span:last-child"
        )
        market_cap_percent = await mcp_element.get_property("textContent")

        sign_element = await session.wait_for_element(15,
            ".sc-16r8icm-0.nds9rn-0.dAxhCK div:nth-of-type(2) table tbody tr:first-child td span:last-child span"
        )
        sign = await sign_element.get_property("className")

        if sign == "icon-Caret-up":
            market_cap_percent = "↑" + market_cap_percent
        else:
            market_cap_percent = "↓" + market_cap_percent

        return market_cap, market_cap_percent
    except:
        return "No Data", "No Data"


async def get_volume_to_market_cap(session):
    try:
        element = await session.wait_for_element(15,
            ".sc-16r8icm-0.nds9rn-0.dAxhCK div:first-of-type table tbody tr:nth-child(5) td"
        )
        volume_to_market_cap = await element.get_property("textContent")
        return volume_to_market_cap
    except:
        return "No Data"


async def get_market_dominance(session):
    try:
        element = await session.wait_for_element(15,
            ".sc-16r8icm-0.nds9rn-0.dAxhCK div:first-of-type table tbody tr:nth-child(6) td"
        )
        market_dominance = await element.get_property("textContent")
        return market_dominance
    except:
        return "No Data"


async def get_crypto_logo(session):
    try:
        element = await session.wait_for_element(15, ".sc-16r8icm-0.gpRPnR.nameHeader img")
        logo = await element.get_property("src")
        return logo
    except:
        return None


async def get_whitepaper(session):
    try:
        element = await session.wait_for_element(15,
            ".sc-16r8icm-0.sc-10up5z1-1.eUVvdh .content li:last-child a"
        )
        whitepaper = await element.get_property("href")
        return whitepaper
    except:
        return None


async def get_info_url(session):
    try:
        return await session.get_url()
    except:
        return None
