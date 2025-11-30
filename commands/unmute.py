import discord
from discord.ext import commands

@commands.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, user: discord.Member):
    """Delete mute from user"""
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")

    if not mute_role:
        await ctx.send("The 'Muted' role does not exist.")
        return

    if mute_role in user.roles:
        await user.remove_roles(mute_role, reason="Unmuted by staff")
        await ctx.send(f"{user} has been unmuted.")
    else:
        await ctx.send(f"{user} is not muted.")

async def setup(bot):
    bot.add_command(unmute)
