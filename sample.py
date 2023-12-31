import os
import sys

import json
import random

import discord
import gspread
from discord.ext import commands
from discord.ui import Button, View
from oauth2client.service_account import ServiceAccountCredentials


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


member_buffer = []


class ToyBoxCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ogiri(self, ctx):
        prompts = load_prompts()
        p = random.choice(prompts)
        await ctx.send(f"お題: {p['prompt']}(by{p['post_by']})")

    @commands.command()
    async def insider(self, ctx):
        view = View()

        async def button_callback(interaction: discord.Interaction):
            member_buffer.append(interaction.user)
            member_names = [m.global_name for m in member_buffer]
            message = f"{interaction.user.global_name}が参加！ 現在：{member_names}"
            await interaction.response.send_message(message)

        async def on_submit(interaction: discord.Interaction):
            if len(member_buffer) < 3:
                await interaction.response.send_message("十分な数の参加者が居ません")
                return

            shuffled = member_buffer[:]
            random.shuffle(shuffled)

            master = shuffled[0]
            insider_user = shuffled[1]

            await master.send("インサイダー・ゲーム：あなたがマスターです")
            await insider_user.send("インサイダー・ゲーム：あなたがインサイダーです")
            for u in shuffled[2:]:
                await u.send("インサイダー・ゲーム：あなたは市民です")

            await interaction.response.send_message("ロールを配布しました")

        entry_button = Button(label="参加", style=discord.ButtonStyle.primary)
        entry_button.callback = button_callback
        submit_button = Button(label="締切", style=discord.ButtonStyle.primary)
        submit_button.callback = on_submit
        view.add_item(entry_button)
        view.add_item(submit_button)

        member_names = [m.global_name for m in member_buffer]
        await ctx.send(f'インサイダー・ゲームを始めます:({member_names})', view=view)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.event
async def setup_hook():
    await bot.add_cog(ToyBoxCog(bot))


bot.run(token)
