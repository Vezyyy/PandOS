import discord
from discord.ext import commands

@commands.command()
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, user: discord.Member, role: discord.Role):
    """Add a role to a user"""
    if role not in user.roles:
        await user.add_roles(role)
        await ctx.send(
            f"The {role.name} role has been successfully added to {user.mention}."
        )
    else:
        await ctx.send(f"{user.mention} already has the {role.name} role.")

async def setup(bot):
    bot.add_command(addrole)
