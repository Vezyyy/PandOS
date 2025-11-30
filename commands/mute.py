import discord
from discord.ext import commands
import asyncio

@commands.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, user: discord.Member, time: str, reason: str = "No reason provided"):
    """Mute a user for a specified amount of time (in minutes)"""
    try:
        time = int(time)
    except ValueError:
        await ctx.send(
            "Invalid time format. Please enter a valid number for the duration in minutes."
        )
        return

    if time <= 0:
        await ctx.send("Time must be a positive number.")
        return

    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")

    if not mute_role:
        mute_role = await ctx.guild.create_role(
            name="Muted", reason="Muted role does not exist."
        )
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(mute_role, speak=False, send_messages=False)

    if mute_role in user.roles:
        await ctx.send(f"{user} is already muted.")
        return
    
    await user.add_roles(mute_role, reason=reason)

    embed = discord.Embed(
        title="🔇 User Muted",
        description=f"**{user}** has been muted for **{time} minutes**.",
        color=discord.Color.red(),
    )
    embed.add_field(name="📝 Reason", value=reason, inline=False)
    embed.add_field(name="🕒 Muted by", value=ctx.author, inline=False)
    embed.add_field(name="⏳ Duration", value=f"{time} minutes", inline=False)
    embed.set_footer(text="Please contact an admin for any questions.")
    embed.set_thumbnail(url=ctx.guild.icon.url)
    embed.set_author(name="PandOS Bot", icon_url=ctx.bot.user.avatar.url)

    await ctx.send(embed=embed)

    log_channel = ctx.bot.get_channel(1295001133202411531)
    if log_channel:
        await log_channel.send(embed=embed)

    dm_embed = discord.Embed(
        title="🔕 You have been muted",
        description=(
            f"Hello **{user.name}**, you have been muted in **{ctx.guild.name}** for **{time} minutes**.\n\n"
            f"**Reason**: {reason}\n\n"
            "⏳ This is a temporary mute. You will be unmuted automatically after the time is up.\n\n"
            "If you believe this is a mistake or have any questions, please reach out to an administrator."
        ),
        color=discord.Color.red(),
    )
    dm_embed.add_field(name="📝 Muted by", value=f"{ctx.author}", inline=False)
    dm_embed.set_footer(text="If you have any issues, please contact an administrator.")
    dm_embed.set_thumbnail(url=ctx.guild.icon.url)
    dm_embed.set_author(name="PandOS Bot", icon_url=ctx.bot.user.avatar.url)

    try:
        await user.send(embed=dm_embed)
    except discord.Forbidden:
        print(f"Unable to send DM to {user.name} as they have DMs disabled.")

    await asyncio.sleep(time * 60)

    await user.remove_roles(mute_role)
    await ctx.send(f"{user} has been unmuted.")

async def setup(bot):
    bot.add_command(mute)
