import discord
from discord.ext import commands
from PandOS_functions import add_warning
from PandOS_Config import LOG_CHANNEL_ID


@commands.command()
@commands.has_permissions(kick_members=True)
async def Pwarn(ctx, user: discord.Member, *, reason: str = "No reason provided"):
    """Warn a user with an optional reason (executed by the bot)."""
    warnings_count = add_warning(user.id, reason)

    warn_embed = discord.Embed(
        title="⚠️ You have been warned",
        description=f"Hello **{user.name}**, you have been warned in **{ctx.guild.name}**.",
        color=discord.Color.orange(),
    )
    warn_embed.add_field(name="📝 Reason", value=reason, inline=False)
    warn_embed.add_field(name="🕒 Warned by", value="PandOS Bot", inline=False)
    warn_embed.add_field(name="⚠️ Total Warnings", value=str(warnings_count), inline=False)
    warn_embed.set_footer(text="This warning will be logged.")
    warn_embed.set_thumbnail(url=ctx.guild.icon.url)
    warn_embed.set_author(name="PandOS Bot", icon_url=ctx.bot.user.avatar.url)

    try:
        await user.send(embed=warn_embed)
    except discord.Forbidden:
        print(f"Unable to send DM to {user.name} as they have DMs disabled.")

    log_channel = ctx.bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        log_embed = discord.Embed(
            title="⚠️ User Warned",
            description=f"**{user}** has been warned.",
            color=discord.Color.orange(),
        )
        log_embed.add_field(name="📝 Reason", value=reason, inline=False)
        log_embed.add_field(name="🕒 Warned by", value="PandOS Bot", inline=False)
        log_embed.add_field(name="⚠️ Total Warnings", value=str(warnings_count), inline=False)
        log_embed.set_footer(text="Warning logged automatically.")
        log_embed.set_thumbnail(url=ctx.guild.icon.url)
        log_embed.set_author(name="PandOS Bot", icon_url=ctx.bot.user.avatar.url)

        await log_channel.send(embed=log_embed)

    await ctx.send(
        f"**{user}** has been warned by PandOS Bot. Reason: {reason} (Total warnings: {warnings_count})"
    )

async def setup(bot):
    bot.add_command(Pwarn)