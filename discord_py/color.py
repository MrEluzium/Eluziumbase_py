import discord
from discord.ext import commands
from settings import TOKEN
bot = commands.Bot(command_prefix=">")


@bot.command()
async def colored(ctx, r, g, b):
    color = discord.Colour.from_rgb(int(r), int(g), int(b))
    embed = discord.Embed(color=color)
    await ctx.send(embed=embed)


if __name__ == '__main__':
    bot.run(TOKEN)
