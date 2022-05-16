import asyncio

from discord.ext import commands

from utils.paginator import *

# from paginate import create_pages, paginate
# from utils import create_pages, paginate
from utils.support_utils import Bug, Feature, Ticket


class support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = f"You are on cooldown. Try again in {error.retry_after:.2f}s"
            await ctx.send(msg)

    @commands.command(
        description="Report a bug to the developers", usage="`*reportbug`"
    )
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def reportbug(self, ctx):
        await ctx.reply("Where did you run into the bug?")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        try:
            where = await self.bot.wait_for("message", timeout=50.0, check=check)
            await ctx.reply("Summarise the bug please")
            what = await self.bot.wait_for("message", timeout=50.0, check=check)
            await ctx.reply("Steps to reproduce bug")
            how = await self.bot.wait_for("message", timeout=50.0, check=check)
        except asyncio.TimeoutError:
            await ctx.reply("Bug report timed out due to lack of response")
        else:
            bug = Bug(
                where.content,
                what.content,
                how.content,
                ctx.author.name + "#" + ctx.author.discriminator,
                ctx.author.id,
            )
            await bug.report_bug()
            embed = discord.Embed(
                title="Bug report summary",
                description="Bug has been successfully reported",
                colour=discord.Colour.purple(),
            )
            embed.add_field(name="Bug report copy:", value=f"{bug}", inline=False)
            embed.set_footer(
                icon_url=ctx.author.display_avatar,
                text=f"Reported by {ctx.author.name}",
            )

            await ctx.reply(embed=embed)

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(description="View my reported bugs", usage="`*mybugs`")
    async def mybugs(self, ctx):
        # in_dm= True if isinstance(ctx.channel, discord.DMChannel) else False
        msg = await ctx.send(f"Fetching all reported bugs...")

        bugs = await Bug.get_bugs()

        if len(bugs) > 0:
            embeds = [
                discord.Embed(
                    title="Bugs",
                    description=f"Bug reported by ",
                    colour=discord.Colour.purple(),
                )
                for bug in bugs
            ]
            embeds_pages = create_pages(embeds, bugs, ctx.author, "Bug")
            paginator = Paginator(ctx.author, msg, pages=embeds_pages)
            await paginator.send(msg)
        else:
            await msg.edit("No Bug Reports Found!")

        # await paginate(ctx, embeds_pages) -> pages library
        # await paginate(self.bot, pages, msg, ctx, in_dm) -> reactions

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(
        description="Submit a support ticket to the developers", usage="`*submitticket`"
    )
    async def submitticket(self, ctx):
        channel = await ctx.author.create_dm()
        await ctx.author.send("Support ticket title")

        def check(msg):
            return msg.author == ctx.author and msg.channel == channel

        try:
            title = await self.bot.wait_for("message", timeout=50.0, check=check)
            await ctx.author.send("Please state your issue")
            desc = await self.bot.wait_for("message", timeout=50.0, check=check)
        except asyncio.TimeoutError:
            await ctx.author.send("Support ticket timed out due to lack of response")
        else:
            ticket = Ticket(
                title.content,
                desc.content,
                ctx.author.name + "#" + ctx.author.discriminator,
                ctx.author.id,
            )
            await ticket.submit_ticket()

            embed = discord.Embed(
                title="Support ticket summary",
                description="Ticket has been successfully submitted",
                colour=discord.Colour.purple(),
            )

            embed.add_field(
                name="Support ticket copy:", value=f"{ticket}", inline=False
            )
            embed.set_footer(
                icon_url=ctx.author.display_avatar,
                text=f"Submitted by {ctx.author.name}",
            )

            await ctx.author.send(embed=embed)

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(description="View my support tickets", usage="`*mytickets`")
    async def mytickets(self, ctx):
        # in_dm = True
        msg = await ctx.author.send(f"Fetching {ctx.author}'s support tickets...")

        tickets = await Ticket.get_tickets(ctx.author.id)

        if len(tickets) > 0:
            embeds = [
                discord.Embed(
                    title="Support Tickets",
                    description=f"Support ticket by ",
                    colour=discord.Colour.purple(),
                )
                for ticket in tickets
            ]

            embeds_pages = create_pages(embeds, tickets, ctx.author, "Ticket")

            paginator = Paginator(ctx.author, msg, pages=embeds_pages)
            await paginator.send(msg)
        else:
            await msg.edit("No Support Tickets Found!")

        # await paginate(ctx.author, embeds_pages) -> pages library
        # await paginate(self.bot, pages, msg, ctx, in_dm) -> reactions

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(
        description="Submit feature request to developers", usage="`*rqfeature`"
    )
    async def rqfeature(self, ctx):
        await ctx.reply("Feature name?")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        try:
            title = await self.bot.wait_for("message", timeout=50.0, check=check)
            await ctx.reply("Please describe the feature in detail")
            desc = await self.bot.wait_for("message", timeout=50.0, check=check)
        except asyncio.TimeoutError:
            await ctx.reply("Feature request timed out due to lack of response")
        else:
            feature = Feature(
                title.content,
                desc.content,
                ctx.author.name + "#" + ctx.author.discriminator,
                ctx.author.id,
            )

            await feature.request_feature()

            if feature is None:
                await ctx.reply("An error has occured!")
                return
            embed = discord.Embed(
                title="Feature request summary",
                description="Request has been successfully submitted",
                colour=discord.Colour.purple(),
            )
            embed.add_field(
                name="Feature request copy:", value=f"{feature}", inline=False
            )
            embed.set_footer(
                icon_url=ctx.author.display_avatar,
                text=f"Requested by {ctx.author.name}",
            )
            await ctx.reply(embed=embed)

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(description="View all feature requests", usage="`*pendingft`")
    async def pendingft(self, ctx):
        # in_dm = True if isinstance(ctx.channel, discord.DMChannel) else False
        msg = await ctx.send(f"Fetching all feature requests...")

        features = await Feature.get_feature()

        if len(features) > 0:
            embeds = [
                discord.Embed(
                    title="Feature requests",
                    description="Feature requested by ",
                    colour=discord.Colour.purple(),
                )
                for ft in features
            ]

            embeds_pages = create_pages(embeds, features, ctx.author, "Feature")

            paginator = Paginator(ctx.author, msg, pages=embeds_pages)
            await paginator.send(msg)
        else:
            await msg.edit("No Feature Requests Found!")

        # await paginate(ctx, embeds_pages) -> pages library
        # await paginate(self.bot, pages, msg, ctx, in_dm) -> reactions


def setup(bot):
    bot.add_cog(support(bot))
