import os

import random
import discord
import gspread
import enum
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
sheet_key = os.getenv('SHEET_KEY')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]


class Subcommand(enum.Enum):
    HELP = 'help'
    OGIRI = 'ogiri'


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


async def process_toybox(message, words):
    if len(words) == 0 or words[0] == Subcommand.HELP.value:
        await message.channel.send(f"コマンド:" + ','.join([member.value for member in Subcommand]))
        return

    print(words)

    if words[0] == Subcommand.OGIRI.value:
        prompts = load_prompts()
        p = random.choice(prompts)
        await message.channel.send(f"お題: {p['prompt']}(by{p['post_by']})")


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    words = message.content.split(' ')
    if words[0] == '/toybox':
        await process_toybox(message, words[1:])


client.run(token)
