import discord
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


async def process_toybox(message, words):
    await message.channel.send(f'Hello!: {words}')


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
