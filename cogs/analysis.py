import io

import discord
from discord.ext import commands
from discord.ui import Button, View

from utils.analysis_utils import *
from utils.predict_utils import *
from utils.graph_utils import *
from utils.info_utils import *
from utils.suggest_utils import *


class analysis(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        description="Predict Ethereum's next-day closure price",
        usage="`*predict`",
    )
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def predict(self, ctx):
        date, price = await model_predict()

        embed = discord.Embed(
            title=f"`ETH`   Ethereum\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯",
            description=f"**Forecast for {date}\n\nPrice: £{price}**",
            colour=discord.Colour.purple(),
        )
        await ctx.reply(embed=embed)

    @commands.command(
        description="Displays cryptocurrency data"
        "\n\nParameter: Description `[EXAMPLE]`"
        "\n\nCrypto: Supports all cryptocurrencies listed on coinmarketcap `[ETH | ethereum]`",
        usage="`*info <symbol>`",
    )
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def info(self, ctx, currency):
        msg = await ctx.reply(f"Processing parameters... [ETC: 4.2 seconds]")

        data = await get_crypto_data(currency)

        embed = discord.Embed(
            title=f"`{data['symbol']}`   {data['name']}\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯",
            description=f"**Rank:** `{data['rank']}`"
            f"\n\n**Price:** `{data['price']}`"
            f"\n\n**Price Change `24h`:** `{data['price_change']} [{data['price_change_percent']}]`"
            f"\n\n**24h Low / 24h High:** `{data['price_low']} / {data['price_high']}`"
            f"\n\n**Trading Volume `24h`:** `{data['trading_volume']} [{data['trading_volume_percent']}]`"
            f"\n\n**Market Cap:** `{data['market_cap']} [{data['market_cap_percent']}]`"
            f"\n\n**Volume / Market Cap:** `{data['volume_to_market_cap']}`"
            f"\n\n**Market Dominance:** `{data['market_dominance']}`",
            colour=discord.Colour.purple(),
        )
        logo = (
            data["crypto_logo"]
            if data["crypto_logo"] is not None
            else "attachment://missing.png"
        )
        whitepaper_url = (
            data["whitepaper_url"]
            if data["whitepaper_url"] is not None
            else "https://coinmarketcap.com/"
        )
        whitepaper_disabled = False if data["whitepaper_url"] is not None else True
        info_url = (
            data["info_url"]
            if data["info_url"] is not None
            else "https://coinmarketcap.com/"
        )
        info_disabled = False if data["info_url"] is not None else True

        embed.set_thumbnail(url=logo)
        whitepaper_button = Button(
            label="Whitepaper",
            url=whitepaper_url,
            emoji="📄",
            disabled=whitepaper_disabled,
        )
        info_button = Button(
            label="More Information", url=info_url, disabled=info_disabled
        )
        view = View()
        view.add_item(whitepaper_button)
        view.add_item(info_button)

        if logo == "attachment://missing.png":
            with open("missing.png", "rb") as f:
                file = io.BytesIO(f.read())
            image = discord.File(file, filename="missing.png")
            await msg.edit(content=None, file=image, embed=embed, view=view)
        else:
            await msg.edit(content=None, embed=embed, view=view)

    @commands.command(
        description="Graph a cryptocurrency"
        "\n\nParameter: Description `[EXAMPLE]`"
        "\n\nType: Support line and candlestick graph `[line | candle]`"
        "\nTicker: Supports all tickers listed in Binance `[ETHUSDT]`"
        "\nPeriod: Number of days to be graphed `[420]`"
        "\nInterval: Interval between prices `[1m | 3m | ... | 1M]`"
        "\nVolume: Show volume `[True]`"
        "\nIndicator: Graph a technical indicator `[daySMA | dayEMA | MACD : where day is the indicator period]`",
        usage="`*graph <type> <ticker> <period> <interval> <volume> [indicator]`",
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def graph(self, ctx, *, params):
        msg = await ctx.reply(f"Processing parameters...")
        style, ticker, period, interval, volume, indicator = await parseGraphArg(params)
        if None not in (style, ticker, period, interval, volume, indicator):
            await msg.edit(f"Streaming data...")
            raw_data = await get_price_data(ticker, interval, period)
            await msg.edit(f"Processing data...")
            data = process_price_data(raw_data, indicator, interval)
            await msg.edit(f"Graphing data...")
            plot(data, ticker, style, volume)
            embed = discord.Embed(
                title=f"{ticker} over {period} days",
                colour=discord.Colour.purple(),
            )
            with open("plot.png", "rb") as f:
                file = io.BytesIO(f.read())
            image = discord.File(file, filename="plot.png")
            embed.set_image(url=f"attachment://plot.png")
            await msg.edit(content=None, file=image, embed=embed)
            os.remove("plot.png")
        else:
            await msg.edit(
                "Invalid argument has been passed. Check attributes and try again."
            )

    @commands.command(
        description="Rank cryptocurrencies based on their momentum"
        "\nParameter: Description `[EXAMPLE]`"
        "\nQuality: Quality of momentum [w -> High quality; l -> Low quality]",
        usage="`*suggest [quality]`",
    )
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def suggest(self, ctx, *, params="default"):
        msg = await ctx.reply(
            f"Please note that it may take a while for the results to be displayed. [ETC: 3 minutes]"
            f"\nProcessing parameters..."
        )

        quality = parseSuggestArg(params)

        if quality:
            await msg.edit(
                f"Please note that it may take a while for the results to be displayed. [ETC: 3 minutes]"
                f"\nStreaming data..."
            )
            raw_data = await get_tickers()
            await msg.edit(
                f"Please note that it may take a while for the results to be displayed. [ETC: 3 minutes]"
                f"\nProcessing {len(raw_data)} data objects..."
            )
            data = await process_ticker_data(raw_data)
            await msg.edit(f"Displaying data...")
            symbols, prices, scores = display(data, quality)
            embed = discord.Embed(
                title="Momentum Investing Strategy",
                description=f"{'High' if (quality=='default' or quality=='w') else 'Low'} quality momentum cryptocurrencies",
                colour=discord.Colour.purple(),
            )
            embed.add_field(name="Symbol", value=symbols, inline=True)
            embed.add_field(name="Price", value=prices, inline=True)
            embed.add_field(name="Momentum Score", value=scores, inline=True)
            embed.set_footer(
                icon_url=ctx.author.display_avatar,
                text=f"Requested by {ctx.author.name}",
            )
            await msg.delete()
            await ctx.reply(embed=embed)
        else:
            await ctx.reply(
                "Invalid argument has been passed. Check attributes and try again."
            )


def setup(bot):
    bot.add_cog(analysis(bot))
