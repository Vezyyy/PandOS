import discord
from discord.ext import commands

@commands.command()
async def userinfo(ctx, user: discord.User):
    """Shows detailed info about a user"""
    member = ctx.guild.get_member(user.id)

    if member is None:
        await ctx.send(f"{user} is not a member of this server.")
        return

    embed = discord.Embed(
        title=f"User Info: {user}",
        description=f"Information about {user.mention}",
        color=discord.Color.blue(),
    )

    embed.add_field(name="User ID", value=user.id, inline=False)
    embed.add_field(
        name="Account Created",
        value=user.created_at.strftime("%b %d, %Y"),
        inline=False,
    )
    embed.add_field(
        name="Joined Server", value=member.joined_at.strftime("%b %d, %Y"), inline=False
    )
    embed.add_field(name="Status", value=str(member.status).title(), inline=False)
    embed.add_field(name="Nickname", value=member.nick if member.nick else "None", inline=False)
    embed.add_field(name="Highest Role", value=member.top_role.name, inline=False)
    embed.add_field(name="Is Bot?", value="Yes" if user.bot else "No", inline=False)

    if member.activity:
        embed.add_field(name="Activity", value=str(member.activity), inline=False)
    else:
        embed.add_field(name="Activity", value="No current activity", inline=False)

    embed.set_thumbnail(url=user.avatar.url)

    roles = [role.name for role in member.roles]
    embed.add_field(name="Roles", value=", ".join(roles), inline=False)

    await ctx.send(embed=embed)

async def setup(bot):
    bot.add_command(userinfo)
