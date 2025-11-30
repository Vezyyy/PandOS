import discord
from discord.ext import commands

@commands.command()
async def serverinfo(ctx):
    """Shows detailed info about the server"""
    guild = ctx.guild
    embed = discord.Embed(
        title=f"{guild.name} Server Info",
        description="Information about the server.",
        color=discord.Color.green(),
    )
    embed.add_field(name="Server Name", value=guild.name, inline=False)
    embed.add_field(name="Server ID", value=guild.id, inline=False)
    embed.add_field(name="Member Count", value=guild.member_count, inline=False)
    embed.add_field(
        name="Created At", value=guild.created_at.strftime("%b %d, %Y"), inline=False
    )

    await ctx.send(embed=embed)

async def setup(bot):
    bot.add_command(serverinfo)
