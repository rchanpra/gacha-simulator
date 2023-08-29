import discord
import os
import gachasim
from dotenv import load_dotenv

PREFIX = '!'

count5 = 0
count4 = 0

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} is online')

@client.event
async def on_message(message):
    global count5
    global count4
    if message.author == client.user:
        return
    
#    print(f'{message.author} said "{message.content}" in #{message.channel}')
    
    if message.content.startswith(PREFIX + 'roll'):
        pulled, count5, count4 = gachasim.pull(count5, count4)
        await message.channel.send(pulled)

load_dotenv()
client.run(os.getenv('TOKEN'))