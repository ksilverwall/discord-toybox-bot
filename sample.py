import os
import sys

import json

import discord
from discord.ext import commands

from controller import ToyBoxCog


secrets = {}
try:
    secrets = json.loads(os.getenv('SECRETS_ENVIRONMENT'))
except json.JSONDecodeError:
    print(f"Failed to load SECRETS_ENVIRONMENT {os.getenv('SECRETS_ENVIRONMENT')}")
    sys.exit(-1)

token = secrets.get("DISCORD_TOKEN")
sheet_key = secrets.get('SHEET_KEY')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/toybox ', intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.event
async def setup_hook():
    await bot.add_cog(ToyBoxCog(bot, sheet_key))


bot.run(token)
