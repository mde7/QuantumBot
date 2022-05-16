import asyncio

from arsenic import browsers, get_session, keys, services

async def test(currency):
    service = services.Chromedriver(
        binary=r"C:\Users\mdema\Documents\chromedriver_win32\chromedriver.exe"
    )
    browser = browsers.Chrome()
    browser.capabilities = {
        "goog:chromeOptions": {"args": ["--disable-gpu"]}
    }
    async with get_session(service, browser) as session:
        await session.get("https://coinmarketcap.com/")
        search_icon = await session.wait_for_element(15, ".sc-16r8icm-0.jZwKai")
        await search_icon.click()
        search_bar = await session.wait_for_element(15, ".bzyaeu-3.jUraic")
        await search_bar.send_keys(f"{currency}{keys.ENTER}")

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(test("eth"))
