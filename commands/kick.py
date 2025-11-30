import discord
from discord.ext import commands

@commands.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.User, reason: str = "No reason provided"):
    await ctx.guild.kick(user, reason=reason)
    await ctx.send(f"{user} has been kicked for: {reason}")

async def setup(bot):
    bot.add_command(kick)
