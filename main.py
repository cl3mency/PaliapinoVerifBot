import discord
from discord.ext import commands, tasks
import logging
from dotenv import load_dotenv
import os
from discord.utils import get
import keep_alive

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(
    filename='discord.log',
    encoding='utf-8',
    mode='w'
)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents)

CHANNEL_ID = 1420449721402654750
NEW_MEMBER_ROLE = 'new member'
VERIFIED_ROLE = 'Mga Pipino'


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.event
async def on_member_join(member):
    newmember = get(member.guild.roles, name=NEW_MEMBER_ROLE)
    if newmember:
        await member.add_roles(newmember)


@bot.event
async def on_message(message):
    # ignore DMs
    if message.guild is None:
        return

    # ignore bots
    if message.author.bot:
        return

    # process normal commands outside verification channel
    if message.channel.id != CHANNEL_ID:
        await bot.process_commands(message)
        return

    guild = message.guild
    verified_role = get(guild.roles, name=VERIFIED_ROLE)
    new_member_role = get(guild.roles, name=NEW_MEMBER_ROLE)

    # safety checks
    if not verified_role or not new_member_role:
        return

    # STOP if already verified
    if verified_role in message.author.roles:
        return

    # prevent empty / spam messages
    content = message.content.strip()
    if len(content) < 2:
        return

    try:
        await message.author.remove_roles(new_member_role)
        await message.author.add_roles(verified_role)

        # limit nickname length to avoid errors
        new_nick = f"IGN | {content[:24]}"
        await message.author.edit(nick=new_nick)

    except discord.Forbidden:
        print("❌ Missing permissions")
    except discord.HTTPException:
        print("⚠️ Rate limit hit")

    await bot.process_commands(message)


keep_alive.keep_alive()
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
