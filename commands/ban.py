import discord
from discord.ext import commands

@commands.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.User, reason: str = "No reason provided"):
    await ctx.guild.ban(user, reason=reason)
    await ctx.send(f"{user} has been banned for: {reason}")

async def setup(bot):
    bot.add_command(ban)
