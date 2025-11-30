import discord
from discord.ext import commands
import json
import os
from PandOS_functions import get_warnings

WARNINGS_FILE = "warnings.json"

@commands.command()
async def warnings(ctx, user: discord.Member):
    """Check a user's warnings."""
    warnings_data = get_warnings(user.id)
    embed = discord.Embed(
        title=f"⚠️ Warnings for {user.name}", color=discord.Color.orange()
    )
    embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)

    if warnings_data["count"] == 0:
        embed.description = "✅ This user has no warnings!"
    else:
        for index, reason in enumerate(warnings_data["reasons"], 1):
            embed.add_field(
                name=f"⚠️ Warning {index}", value=f"**Reason:** {reason}", inline=False
            )
        embed.set_footer(text=f"Total warnings: {warnings_data['count']}")

    await ctx.send(embed=embed)

async def setup(bot):
    bot.add_command(warnings)