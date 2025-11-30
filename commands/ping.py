import discord
from discord.ext import commands

@commands.command()
async def ping(ctx):
    """Check bot latency."""
    latency = round(ctx.bot.latency * 1000)
    await ctx.send(f"Pong! Latency: {latency}ms")

async def setup(bot):
    bot.add_command(ping)
