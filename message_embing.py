import asyncio

import discord
from datetime import datetime
from utils.emoji import emojiMap


async def send_embed(ctx, tasks, page_no):
    embed = discord.Embed(title="To Do : " + ctx.author.name, color=0x381919)
    # embed.set_author(name="mayank")
    if len(tasks) == 0:
        embed.add_field(name="\u200b", value="You do not have any open tasks.\n Please add using add command", inline=False)
    start = (page_no-1)*5
    end = min(len(tasks), (page_no)*5)
    for i in range(start,end):
        bullet =  emojiMap.get('bullet_done') if tasks[i].status else emojiMap.get('bullet_not_done')
        embed.add_field(name="\u200b", value=bullet + " " + tasks[i].task_text + "\n", inline=False)
    embed.add_field(name="Page", value=str(start+1) + "/" + str((len(tasks)//5 + 1)), inline=False)
    message = await ctx.send(embed=embed)
    if end < len(tasks):
        await message.add_reaction(emoji=emojiMap.get('next'))
    for i in range(start,end):
        await message.add_reaction(emoji=emojiMap.get(i+1))
    return message

async def get_edited_embed(react, user, tasks, reset_reaction, current_page_no):
    print("Edit " , current_page_no)
    embed = discord.Embed(title="To Do : " + user.name, color=0x381919)
    start = (current_page_no -1) * 5
    end = min(len(tasks), (current_page_no) * 5)
    for i in range(start, end):
        bullet = emojiMap.get('bullet_done') if tasks[i].status else emojiMap.get('bullet_not_done')
        embed.add_field(name="\u200b", value=bullet + " " + tasks[i].task_text + "\n", inline=False)
    embed.add_field(name="Page", value=str(current_page_no) + "/" + str((len(tasks)//5 + 1)), inline=False)
    await react.message.edit(embed = embed)
    if reset_reaction:
        await react.message.clear_reactions()
        if current_page_no > 1:
            await react.message.add_reaction(emoji=emojiMap.get('previous'))
        if end < len(tasks):
            await react.message.add_reaction(emoji=emojiMap.get('next'))
        for i in range(end - start):
            await react.message.add_reaction(emoji=emojiMap.get(i + 1))


def send_help_embed(ctx):
    embed = discord.Embed(title="To Do : Help" , color=0x381919)
    embed.add_field(name="add", value="Use !td add <task name > to add your task in daily todo list")
    embed.add_field(name="view", value="Use !td view to voew your task in daily todo list")
    embed.add_field(name="delete", value="Use !td delete <task no>  to delete task in daily todo list")
    return embed



