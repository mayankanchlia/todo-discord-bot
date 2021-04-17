# bot.py
import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
from collections import defaultdict
from taskRetriver import Task
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
intents = discord.Intents().all()
# client = discord.Client(prefix='', intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)
taskList = defaultdict(list)

@bot.event
async def on_ready():
    print("All systems online and working " + bot.user.name)

@bot.command()
async def td(ctx,*, message: str):
    arg1 = message.split(" ")[0]
    if arg1.lower() == "add":
        add_task_to_user_list(ctx.guild.id, ctx.author.id, datetime.today().strftime('%Y%m%d'),message)
    if arg1.lower() == "view":
        await view(ctx)


def add_task_to_user_list(guild, member, date, taskDiscription):
    if member in taskList:
        taskList.get(member).append(Task(guild, member, date, taskDiscription))
    else :
        print("hello")
        taskList[member] = [Task(guild, member, date, taskDiscription)]

async def view(ctx):
    memberId = ctx.author.id
    if memberId in taskList:
        for task in taskList[memberId]:
            message = await ctx.send(task.message)
            if task.isCompleted:
                await message.add_reaction("✅")
            else :
                await message.add_reaction("❎")
    else :
        await ctx.send("There is no Task list for you")
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

