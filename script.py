import discord
import discord.ext
import re
import random
import time
from yahoo_fin import stock_info as si
import asyncio

client = discord.Client()

@client.event
async def status_task():
    count = 0
    t = ["AAPL","TSLA","DOW","SPY"]
    while True:
        await asyncio.sleep(10)
        num = si.get_live_price(t[count])
        await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name='$'+t[count]+' %.2f' % num))
        count = (count+1)%4
        
@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    num = si.get_live_price("spy")
    await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name='$SPY %.2f' % num))
    client.loop.create_task(status_task())

@client.event
async def on_message(message):
    if message.content.startswith('$chart'):
        num = message.content[7:].upper()
        num = re.sub('[\W_]+', '', num)
        await message.delete()
        try:
            price = str(si.get_live_price(num))
            embed = discord.Embed(title=num, description=price, color=0x206594)
            embed.set_image(url="https://stockcharts.com/c-sc/sc?s="+num+"&p=D&b=5&g=0&i=0&r=1595274481420")
            await message.channel.send(embed=embed)
        except:
            print("Invalid ticker!")
    if message.content.startswith('$price'):
        num = message.content[7:].upper()
        num = re.sub('[\W_]+', '', num)
        await message.delete()
        try:
            price = str(si.get_live_price(num))
            embed = discord.Embed(title=num, description=price, color=0x206594)
            await message.channel.send(embed=embed)
        except:
            print("Invalid ticker!")
    

client.run('')


