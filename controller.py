import random
import gspread
import discord

from discord.ext import commands
from discord.ui import Button, View
from oauth2client.service_account import ServiceAccountCredentials


scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
member_buffer = []


def load_prompts(sheet_key: str):
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


class ToyBoxCog(commands.Cog):
    def __init__(self, bot, sheet_key: str):
        self.bot = bot
        self.sheet_key = sheet_key

    @commands.command()
    async def ogiri(self, ctx):
        prompts = load_prompts(self.sheet_key)
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
