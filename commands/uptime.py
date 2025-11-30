import discord
from discord.ext import commands
import datetime

@commands.command()
async def uptime(ctx):
    """Shows the bot's uptime."""
    bot_creation_time = ctx.bot.user.created_at.replace(tzinfo=datetime.timezone.utc)
    current_time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    delta_uptime = current_time - bot_creation_time

    days, seconds = delta_uptime.days, delta_uptime.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    formatted_uptime = f"{days}d {hours}h {minutes}m {seconds}s"

    await ctx.send(f"Bot has been online for: {formatted_uptime}")

async def setup(bot):
    bot.add_command(uptime)
