import discord
from datetime import datetime
from utils.emoji import emojiMap
async def send_ember(Tasks):
    embed = discord.Embed(title="title ~~(did you know you can have markdown here too?)~~",
                          colour=discord.Colour(0x61c443), url="https://discordapp.com",
                          description="this supports [named links](https://discordapp.com) on top of the previously shown subset of markdown. ```\nyes, even code blocks```",
                          timestamp=datetime.utcfromtimestamp(1618772662))

    embed.set_image(url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_author(name="author name", url="https://discordapp.com",
                     icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_footer(text="footer text", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    bullet = emojiMap.get('+')
    embed.add_field(name="\u200b", value= bullet + " task 1", inline=True)
    await ctx.send(
        content="this `supports` __a__ **subset** *of* ~~markdown~~ 😃 ```js\nfunction foo(bar) {\n  console.log(bar);\n}\n\nfoo(1);```",
        embed=embed)