# bot.py
import asyncio
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from collections import defaultdict
from model import *
from utils import constants, emoji
import message_embing
from utils.constants import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
intents = discord.Intents().all()
bot = commands.Bot(command_prefix=TRIGGER_WORD, intents=intents)
taskList = defaultdict(list)
init_db()


@bot.event
async def on_ready():
    print("All systems online and working " + bot.user.name)


@bot.command()
async def td(ctx, *, message: str):
    await ctx.message.delete()
    try:
        arg1, data = message.split(" ", 1)
    except:
        arg1 = message
    if arg1.lower() == COMMAND_ADD.lower():
        if ctx.guild is not None:
            add_task_to_user_list(ctx.guild.id, ctx.author.id, datetime.today(), data)
        else:
            add_task_to_user_list(ctx.author.id, ctx.author.id, datetime.today(), data)
    if arg1.lower() == COMMAND_VIEW.lower():
        message = await message_embing.send_ember(ctx, get_task_for_member_id(ctx.author.id))

        def check(reaction, user):
            return user == ctx.author
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=10.0, check=check)
        except asyncio.TimeoutError:
            await message.clear_reactions()
        else:
            await ctx.send('👍')


def add_task_to_user_list(guild, member, date, task_description):
    insert_to_task(member, guild, date, task_description, False)


async def view(ctx):
    member_id = ctx.author.id
    task_lists = get_task_for_member_id(member_id, datetime.today())
    for task in task_lists:
        print(task)
        message = await ctx.send(task.task_text)
        if task.status:
            await message.add_reaction(emoji.emojiMap.get('bullet_done'))
        else:
            await message.add_reaction(emoji.emojiMap.get('not_done_emoji'))


@bot.event
async def on_reaction_add(reaction, user):
    if user.id == bot.user.id:
        return
    if reaction.emoji in emoji.Mapemoji:
        task_number = emoji.Mapemoji.get(reaction.emoji)
        task_list = get_task_for_member_id(user.id)
        task = update_task_by_id(task_list[task_number-1].id)
        await reaction.message.edit(embed=message_embing.get_edited_embed(get_task_for_member_id(user.id)))
        await reaction.remove(user)


bot.run(TOKEN, bot=True)

