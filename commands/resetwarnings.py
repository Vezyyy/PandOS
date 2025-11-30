import discord
from discord.ext import commands
from PandOS_functions import reset_warnings

@commands.command()
@commands.has_permissions(administrator=True)
async def resetwarnings(ctx, user: discord.Member):
    """Reset the warnings for a user."""
    reset_warnings(user.id)
    await ctx.send(f"**{user}**'s warnings have been reset.")

async def setup(bot):
    bot.add_command(resetwarnings)
