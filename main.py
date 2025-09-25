import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from discord.utils import get
import time


load_dotenv()
token = os.getenv('DISCORD_TOKEN')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='.', intents=intents)
channel = bot.get_channel(1420449721402654750)

@bot.event
async def on_ready():
    #Sends a message if the bot has started and is running
    print("Bot is running")

@bot.event
async def on_member_join(member):

    #assigns new member role to newmember variable
    newmember = discord.utils.get(member.guild.roles, name = 'new member')

    #adds new member role to new joined member  
    await member.add_roles(newmember)
    @bot.event
    #waits for user message
    async def on_message(message):
        if message.author == bot.user:
            return
        
        #checks if message is sent in specific text channel
        if message.channel.id == 1420449721402654750:
            if message.author == member:
            
            #await channel.send(f"You are now a Verified Member")
                time.sleep(2)

            #assigns Verified Member role to VerifiedMember variable
                VerifiedMember = discord.utils.get(member.guild.roles, name = 'Mga Pipino')

            #assigns new member role to newmemberRemove variable
                newmemberRemove = discord.utils.get(member.guild.roles, name = 'new member')

            #removes new member role from member
                await member.remove_roles(newmemberRemove)

            #adds Verified Member role to member
                await member.add_roles(VerifiedMember)

            #assigns user input message to newNick variable
                usrmsg = message.content
                newNick = "IGN | " + usrmsg
            #uses user input message to change nickname of new member
                await member.edit(nick=newNick)

            else:
                return
            
            await bot.process_commands(message)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
