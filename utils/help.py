import discord
from discord.ext import commands


class Help(commands.HelpCommand):
    icons = {
        "trading": ":coin:",
        "analysis": ":chart_with_upwards_trend:",
        "support": ":shield:",
        "info": ":book:",
    }

    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title="CryptoBot",
            description="CryptoBot Command List",
            colour=discord.Colour.purple(),
        )
        for cog in mapping:
            if cog is not None:
                embed.add_field(
                    name=f"{self.icons[cog.qualified_name]} {cog.qualified_name.capitalize()}",
                    value=f"`*help {cog.qualified_name}`",
                    inline=True,
                )
        embed.set_footer(text="Developed by MDE#1870")
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        description = ""
        # commands_list = cog.get_commands()
        commands_list = [command for command in cog.walk_commands()]
        for i in range(len(commands_list)):
            if i == len(commands_list) - 1:
                description += f"`{commands_list[i].name}`"
            else:
                description += f"`{commands_list[i].name}`, "
        embed = discord.Embed(
            title=f"{self.icons[cog.qualified_name]} {cog.qualified_name.capitalize()} Commands",
            description=description,
            colour=discord.Colour.purple(),
        )
        embed.set_footer(text="use * before each command!")
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        await self.get_destination().send("group")

    async def send_command_help(self, command):
        embed = discord.Embed(
            title=f"*{command.name} information", colour=discord.Colour.purple()
        )
        embed.add_field(
            name="Description", value=f"{command.description}", inline=False
        )
        embed.add_field(name="Usage", value=f"{command.usage}", inline=False)
        embed.set_footer(text="Usage Syntax: <required> [optional]")
        await self.get_destination().send(embed=embed)
