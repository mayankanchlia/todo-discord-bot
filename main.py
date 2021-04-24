# bot.py
import asyncio
import os
import traceback

import discord
from discord.ext import commands
from dotenv import load_dotenv
from collections import defaultdict

from message_embing import send_help_embed
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
    if ctx.guild is not None:
        await ctx.message.delete()
    try:
        arg1, data = message.split(" ", 1)
    except:
        print(traceback.format_exc())
        arg1 = message
    if arg1.lower() == COMMAND_ADD.lower():
        if ctx.guild is not None:
            add_task_to_user_list(ctx.guild.id, ctx.author.id, datetime.today(), data)
        else:
            add_task_to_user_list(ctx.author.id, ctx.author.id, datetime.today(), data)
        await message_embing.send_embed(ctx, get_task_for_member_id(ctx.author.id), 1)
    elif arg1.lower() == COMMAND_VIEW.lower():
        message = await message_embing.send_embed(ctx, get_task_for_member_id(ctx.author.id), 1)

        def check(reaction, user):
            print("check here")
            return reaction.message == message and user == ctx.author
        while True :
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=15.0, check=check)
            except asyncio.TimeoutError:
                await message.clear_reactions()
                await delete_message(message, 30)
                break
    elif arg1.lower() in COMMAND_DELETE:
        try :
            task_no = int(data)
            await delete_task_by_list_number(ctx,task_no,datetime.today())
        except :
            print(traceback.format_exc())
            if data == "all":
                delete_all_task_by_member_id(ctx.author.id, datetime.today())
                await message_embing.send_embed(ctx, get_task_for_member_id(ctx.author.id),0)
            else:
                await send_message(ctx,"Please enter correct task no")
    elif arg1.lower() == COMMAND_help:
        print(help)
        await ctx.send(embed=message_embing.send_help_embed(ctx))
    else:
        await ctx.send("Invalid command, type help command ")


async def send_message(ctx, txt):
    await ctx.send(txt)


async def delete_message(message, time):
    await asyncio.sleep(time)
    await message.delete()


def add_task_to_user_list(guild, member, date, task_description):
    insert_to_task(member, guild, date, task_description, False)


async def delete_task_by_list_number(ctx, task_no,date):
    task_list = get_task_for_member_id(ctx.author.id, date)
    delete_task_by_id_from_db(task_list[task_no -1].id)
    message = await message_embing.send_embed(ctx, get_task_for_member_id(ctx.author.id),0)




@bot.event
async def on_reaction_add(reaction, user):
    if user.id == bot.user.id:
        return
    if reaction.emoji in emoji.emojiMap.values():
        embeds = reaction.message.embeds
        name = embeds[0].to_dict().get('title').split('To Do : ')[1]
        page_no = 0
        message = reaction.message
        if name == user.name :
            for field in embeds[0].to_dict().get('fields'):
                print(field)
                if field['name'] == "Page":
                    page_no = int(field['value'].split('/')[0])
                    break
            if reaction.emoji in emoji.mapemoji.keys():
                task_number = emoji.mapemoji.get(reaction.emoji) + ((page_no-1)*10)
                task_list = get_task_for_member_id(user.id)
                task = update_task_by_id(task_list[task_number-1].id)
                await message_embing.get_edited_embed(reaction,user, get_task_for_member_id(user.id), False, page_no)
            elif reaction.emoji == emoji.emojiMap.get('next'):
                print("next page")
                await message_embing.get_edited_embed(reaction,user, get_task_for_member_id(user.id), True, page_no+1)
            elif reaction.emoji == emoji.emojiMap.get('previous'):
                print('previous page')
                await message_embing.get_edited_embed(reaction, user, get_task_for_member_id(user.id), True,
                                                      page_no -1 )
        await reaction.remove(user)
        await delete_message(message, 30)


bot.run(TOKEN, bot=True)

