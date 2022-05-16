import os

import discord
from discord.ext import commands

from dotenv import load_dotenv

from utils.help import Help

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

COMMAND_PREFIX = commands.when_mentioned_or("*")
INTENTS = discord.Intents.all()
ACTIVITY = discord.Game(name="*help")
HELP = Help()

client = commands.Bot(
    command_prefix=COMMAND_PREFIX,
    intents=INTENTS,
    activity=ACTIVITY,
    help_command=HELP,
)


@client.event
async def on_ready():
    print("Quantum is online.")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run(TOKEN)
