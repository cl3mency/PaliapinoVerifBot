import discord
from discord.ext import commands, tasks
import logging
from dotenv import load_dotenv
import os
from discord.utils import get
import time
from keep_alive import keep_alive

keep_alive()

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='.', intents=intents)
channel = bot.get_channel(1420449721402654750)


@tasks.loop(minutes=3)
async def scheduled_message():
    channel_id = 1420343132242972715
    channel = bot.get_channel(channel_id)
    await channel.send("This bot is still running")

@bot.event
async def on_ready():
    scheduled_message.start()

@bot.event
async def on_member_join(member):

    #assigns new member role to newmember variable
    newmember = discord.utils.get(member.guild.roles, name = 'new member')

    #adds new member role to new joined member  
    await member.add_roles(newmember)

@bot.event
async def on_message(message):
    channel_id = 1420449721402654750
    channel = bot.get_channel(channel_id)
    if message.guild is None:
        return
    elif message.author == bot.user:
        return
    if message.channel.id != channel_id:
        await bot.process_commands(message)
        return
    if message.channel.id == channel_id:
        guild = message.guild
        VerifiedMember = discord.utils.get(guild.roles, name = 'Mga Pipino')
        newmemberRemove = discord.utils.get(guild.roles, name = 'new member')
        await message.author.remove_roles(newmemberRemove)
        await message.author.add_roles(VerifiedMember)
        urmsg = message.content
        newNick = "IGN | " + urmsg
        await message.author.edit(nick=newNick)
    
    await bot.process_commands(message)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)





