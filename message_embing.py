import asyncio

import discord
from datetime import datetime
from utils.emoji import emojiMap


async def send_embed(ctx, tasks):
    embed = discord.Embed(title="To Do : " + ctx.author.name, color=0x381919)
    # embed.set_author(name="mayank")
    if len(tasks) == 0:
        embed.add_field(name="\u200b", value="You do not have any open tasks.\n Please add using add command", inline=False)
    for task in tasks:
        bullet =  emojiMap.get('bullet_done') if task.status else emojiMap.get('bullet_not_done')
        embed.add_field(name="\u200b", value=bullet + " " + task.task_text + "\n", inline=False)
    message = await ctx.send(embed=embed)
    for i in range(len(tasks)):
        await message.add_reaction(emoji=emojiMap.get(i+1))
    return message


def get_edited_embed(user,tasks):
    embed = discord.Embed(title="To Do : " + user.name, color=0x381919)
    for task in tasks:
        bullet = emojiMap.get('bullet_done') if task.status else emojiMap.get('bullet_not_done')
        embed.add_field(name="\u200b", value=bullet + " " + task.task_text + "\n", inline=False)
    return embed


def send_help_embed(ctx):
    embed = discord.Embed(title="To Do : Help" , color=0x381919)
    embed.add_field(name="add", value="Use !td add <task name > to add your task in daily todo list")
    embed.add_field(name="view", value="Use !td view to voew your task in daily todo list")
    embed.add_field(name="delete", value="Use !td delete <task no>  to delete task in daily todo list")
    return embed


