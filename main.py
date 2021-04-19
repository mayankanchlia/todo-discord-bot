# bot.py
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from collections import defaultdict
from model import *
from utils import constants
import message_embing
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
intents = discord.Intents().all()
# client = discord.Client(prefix='', intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)
taskList = defaultdict(list)
init()

@bot.event
async def on_ready():
    print("All systems online and working " + bot.user.name)

@bot.command()
async def td(ctx,*, message: str):
    arg1 = message.split(" ")[0]
    if arg1.lower() == "add":
        task_text = message.split(" ",1)[1]
        if ctx.guild is not None:
            add_task_to_user_list(ctx.guild.id, ctx.author.id, datetime.today(),task_text)
        else :
            add_task_to_user_list(ctx.author.id, ctx.author.id, datetime.today(), task_text)
    if arg1.lower() == "view":
        await view(ctx)
    if arg1.lower() == "emb":
        await message_embing.send_ember(ctx)


def add_task_to_user_list(guild, member, date, taskDiscription):
    insert_to_task(member, guild,date, taskDiscription, False)

async def view(ctx):
    memberId = ctx.author.id
    task_lists = get_task_for_username(memberId)
    for task in task_lists:
        print(task)
        message = await ctx.send(task.task_text)
        if(task.status):
            await message.add_reaction(constants.done_emoji)
        else:
            await message.add_reaction(constants.not_done_emoji)


@bot.event
async def on_raw_reaction_add(payload):
    if bot.user.id == payload.user_id:
        print("this is bot react")
        return
    emoji = payload.emoji
    if str(emoji) == constants.done_emoji:
        channel = await bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        if message.content.startswith("!td"):
            txt = message.content.split(" ",2)[-1]
            task_row = get_task_by_username_and_text_update(message.author.id, txt, datetime.today(),True)
        # print(message.content)
    # print(emoji)
bot.run(TOKEN, bot=True)

