import asyncio

import discord
from datetime import datetime
from utils.emoji import emojiMap


async def send_ember(ctx, tasks):
    embed = discord.Embed(color=0x8e6767)

    for task in tasks:
        bullet =  emojiMap.get('bullet_done') if task.status else emojiMap.get('bullet_not_done')
        embed.add_field(name="\u200b", value=bullet + " " + task.task_text + "\n", inline=False)
    message = await ctx.send(embed=embed)
    for i in range(len(tasks)):
        await message.add_reaction(emoji=emojiMap.get(i+1))
    return message


def get_edited_embed(tasks):
    embed = discord.Embed(color=0x8e6767)
    for task in tasks:
        bullet = emojiMap.get('bullet_done') if task.status else emojiMap.get('bullet_not_done')
        embed.add_field(name="\u200b", value=bullet + " " + task.task_text + "\n", inline=False)
    return embed
