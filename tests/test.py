from arsenic import browsers, get_session, keys, services
from binance import (
    AsyncClient,
    Client,
    ThreadedDepthCacheManager,
    ThreadedWebsocketManager,
)
from firebase import db
import unittest
import os


class WebScrape(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.service = services.Chromedriver(
            binary=r"C:\Users\mdema\Documents\chromedriver_win32\chromedriver.exe"
        )
        self.browser = browsers.Chrome()
        self.browser.capabilities = {
            "goog:chromeOptions": {"args": ["--headless", "--disable-gpu"]}
        }

    async def test_scrape(self):
        async with get_session(self.service, self.browser) as session:
            await session.get("https://coinmarketcap.com/")
            search_icon = await session.wait_for_element(15, ".sc-16r8icm-0.jZwKai")
            await search_icon.click()
            search_bar = await session.wait_for_element(15, ".bzyaeu-3.jUraic")
            await search_bar.send_keys(f"ETH{keys.ENTER}")

            if await session.get_url() == "https://coinmarketcap.com/":
                return "Not Found"

            name, symbol = await self.get_symbol_name(session)
            await session.close()
        self.assertEqual((name, symbol), ("Ethereum", "ETH"))

    async def get_symbol_name(self, session):
        try:
            element = await session.wait_for_element(15, ".sc-1q9q90x-0.jCInrl.h1")
            name_symbol = await element.get_text()
            elements = name_symbol.split("\n")
            return elements[0], elements[1]
        except:
            return "No Data", "No Data"


class BinanceAPI(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.API_KEY = os.getenv("API_KEY")
        self.API_SECRET = os.getenv("API_SECRET")
        self.client = AsyncClient(self.API_KEY, self.API_SECRET)

    async def test_binance(self):
        info = await self.client.get_symbol_info('ETHGBP')
        self.assertEqual(dict, type(info))

    async def asyncTearDown(self):
        await self.client.close_connection()


class FirebaseAPI(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.db = db
        self.data = {
            "TestKey": "TestValue"
        }

    async def test_firebase(self):
        await self.db.collection("TestCollection").document("TestDocument").set(self.data)
        doc_ref = self.db.collection("TestCollection").document("TestDocument")
        doc = await doc_ref.get()
        self.assertEqual(self.data, doc.to_dict())


if __name__ == '__main__':
    unittest.main()
