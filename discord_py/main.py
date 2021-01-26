import discord
from baselogger import get_logger
from database import DataBase
from discord.ext import commands
from settings import TOKEN, db_path
log = get_logger("bot")
db = DataBase(db_path)

custom_prefixes = {}
default_prefixes = ['>']


async def get_prefix(bot, message):
    guild = message.guild
    if guild:
        return custom_prefixes.get(guild.id, default_prefixes)
    return default_prefixes
bot = commands.Bot(command_prefix=get_prefix)


@bot.event
async def on_connect():
    log.info(f"{bot.user} has connected to Discord! Preparing...")

    db.create_table("Guilds", "prefix")
    db_guilds = db.read_all("Guilds", "id, prefix")
    if db_guilds:
        guilds = {}
        for g in db_guilds:
            guilds[g[0]] = g[1]

        for bot_guild in bot.guilds:
            if bot_guild.id in guilds:
                custom_prefixes[bot_guild.id] = guilds[bot_guild.id] or default_prefixes
            else:
                db.insert("Guilds", "id", f"{bot_guild.id}")
                custom_prefixes[bot_guild.id] = default_prefixes

    else:
        for bot_guild in bot.guilds:
            db.insert("Guilds", "id", f"{bot_guild.id}")
            custom_prefixes[bot_guild.id] = default_prefixes

    cur_activity = discord.Game(">help")
    await bot.change_presence(status=discord.Status.online, activity=cur_activity)


@bot.event
async def on_ready():
    log.info(f"{bot.user} is done preparing the data. Now we online!")


@bot.event
async def on_disconnect():
    log.warning(f"{bot.user} has disconnected from Discord.")


@bot.event
async def on_resumed():
    log.info(f"{bot.user} has resumed a session!")


@bot.command()
@commands.guild_only()
async def set_prefix(ctx, *, prefix):
    db.update("Guilds", "id", ctx.guild.id, "prefix", f"'{prefix}'")
    custom_prefixes[ctx.guild.id] = prefix
    await ctx.send("Prefix set!")


@set_prefix.error
async def set_prefix_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("> Введены не все аргументы. Проверьте правильносьт введенной комманды.")
        log.error(f"Raised error on set_prefix command: {error}")
    else:
        await ctx.send(f"> Raised an unexpected error on colored command: {error}")
        log.error(f"Raised an unexpected error on set_prefix command: {error}")


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


if __name__ == '__main__':
    import os
    import platform
    log.info(f"\n\nStart on {platform.platform()}; "
             f"Python {platform.python_version()} {platform.python_compiler()}; "
             f"PID: {os.getpid()}")
    bot.run(TOKEN)
