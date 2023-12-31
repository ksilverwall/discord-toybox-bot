import os

import random

import discord
import gspread
from discord.ext import commands
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials


load_dotenv()
token = os.getenv('DISCORD_TOKEN')
sheet_key = os.getenv('SHEET_KEY')

intents = discord.Intents.default()
intents.message_content = True

discord_client = commands.Bot(command_prefix='/toybox ', intents=intents)

scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]


def load_prompts():
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'credentials.json', scope)
    client = gspread.authorize(creds)

    spreadsheet = client.open_by_key(sheet_key)
    worksheet = spreadsheet.sheet1

    col_status = worksheet.col_values(1)
    col_title = worksheet.col_values(3)
    col_from = worksheet.col_values(4)

    buffer = []
    for s, t, f in zip(col_status, col_title, col_from):
        if s != '使用済':
            continue

        buffer.append({
            'prompt': t,
            'post_by': f,
        })

    return buffer


@discord_client.event
async def on_ready():
    print(f'We have logged in as {discord_client.user}')


@discord_client.command()
async def ogiri(ctx):
    prompts = load_prompts()
    p = random.choice(prompts)
    await ctx.send(f"お題: {p['prompt']}(by{p['post_by']})")


discord_client.run(token)
