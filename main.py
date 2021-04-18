# bot.py
import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
from collections import defaultdict
from taskRetriver import Task
from Model import *
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
        add_task_to_user_list(ctx.guild.id, ctx.author.id, datetime.today(),message)
    if arg1.lower() == "view":
        await view(ctx)


def add_task_to_user_list(guild, member, date, taskDiscription):
    insert_to_task(member, guild,date, taskDiscription, False)
    #
    # if member in taskList:
    #     # taskList.get(member).append(Task(guild, member, date, taskDiscription))
    # else :
    #     print("hello")
    #     # taskList[member] = [Task(guild, member, date, taskDiscription)]

async def view(ctx):
    memberId = ctx.author.id
    task_lists = get_task_for_username(memberId)
    for task in task_lists:
        print(task)
        message = await ctx.send(task[-2])
        await message.add_reaction('✅')

@bot.event
async def on_raw_reaction_add(payload):
    emoji = payload.emoji
    if str(emoji) == '✅':
        print("DAsda")
        channel = await bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = await bot.fetch_user(payload.user_id)
        if message.content in [task.message for task in taskList[message.author.id]]:
            print("task found")

    print(emoji)
    # print(channel,message, user, emoji)
bot.run(TOKEN, bot=True)

