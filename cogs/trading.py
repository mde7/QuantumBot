import sys

import discord
from discord.ext import commands

import firebase

'''
open_account + close_account into class methods
view_account (?)
'''


# class Portfolio(object):
#     def __new__(cls, *args, **kwargs):
#         caller = sys._getframe().f_back.f_code.co_name
#         if caller not in ["open_account", "toObj"]:
#             raise Exception("Portflio can only be created within the class!")
#         return super(Portfolio, cls).__new__(cls)


class trading(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(description="Open a cryptocurrency investment account", usage="`*openacc`")
    async def openacc(self, ctx):
        # msg = await ctx.send("Processing request...")
        # username = ctx.author.name+"#"+ctx.author.discriminator
        # status = Portfolio.open_account(username, ctx.author.id)
        # await msg.edit(content="Success") if status else await msg.edit(content="Failed")
        await ctx.reply("test")

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(description="Close an existing cryptocurrency investment account", usage="`*closeacc`")
    async def closeacc(self, ctx):
        # msg = await ctx.send("Processing request...")
        # status = Portfolio.close_account(ctx.author.id)
        # await msg.edit(content="Success") if status else await msg.edit(content="Failed")
        await ctx.reply("test")

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(description="View cryptocurrency portfolio", usage="`*viewportfolio`")
    async def viewportfolio(self, ctx):
        # msg = await ctx.send(f"Fetching {ctx.author}'s portfolio...")
        #
        # embed = discord.Embed(title=f"{ctx.author}'s Portfolio", description=f"Wallet ID: {ctx.author.id}",
        #                       colour=discord.Colour.purple())
        #
        # portfolio = Portfolio.getAccount(ctx.author.id)
        # if portfolio is not None:
        #     embed.add_field(name="Stats:", value=f"{portfolio}", inline=False)
        # else:
        #     embed.add_field(name="Error!", value="Please open an account!", inline=False)
        #
        # embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
        #
        # await msg.edit(content=None, embed=embed)
        await ctx.reply("test")

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(description="Deposit funds into cryptocurrency investment account", usage="`*deposit <number>`")
    async def deposit(self, ctx, value):
        # try:
        #     int(value)
        # except ValueError:
        #     return await ctx.send("Please enter an integer...")
        # msg = await ctx.send("Processing request...")
        # status = Portfolio.deposit(ctx.author.id, value)
        # await msg.edit(content="Success") if status else await msg.edit(content="Failed")
        await ctx.reply("test")

    @commands.command(description="Transfer funds to a user's investment account",
                      usage="*transfer <@username> <coin> <amount>")
    async def transfer(self, ctx, member: discord.Member, coin, amount):
        # if coin not in CryptoExchange.get_coins():
        #     return await ctx.send("Please enter a valid cryptocurrency...")
        # if not amount.isnumeric():
        #     return await ctx.send("Please enter an integer...")
        # if ctx.author.id == member.id:
        #     return await ctx.send("Cannot transfer to own self...")
        # msg = await ctx.send("Processing request...")
        # status = Portfolio.transfer(ctx.author.id, member.id, coin, amount)
        # await msg.edit(content="Success") if status else await msg.edit(content="Failed")
        await ctx.reply("test")

    @deposit.error
    @transfer.error
    async def missing_arg(self, ctx, error):
        # if isinstance(error, commands.MissingRequiredArgument):
        #     return await ctx.send("Please enter a value...")
        # else:
        #     raise error
        await ctx.reply("test")

    @transfer.error
    async def invalid_member(self, ctx, error):
        # if isinstance(error, commands.MemberNotFound):
        #     return await ctx.send("Please enter a valid user")
        # else:
        #     raise error
        await ctx.reply("test")


def setup(bot):
    bot.add_cog(trading(bot))
