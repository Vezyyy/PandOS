import discord
from discord.ext import commands

@commands.command()
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, user: discord.Member, role: discord.Role):
    """Remove a role from a user"""
    if role in user.roles:
        await user.remove_roles(role)
        await ctx.send(
            f"The {role.name} role has been successfully removed from {user.mention}."
        )
    else:
        await ctx.send(f"{user.mention} doesn't have the {role.name} role.")

# Funkcja setup dla load_extension
async def setup(bot):
    bot.add_command(removerole)
