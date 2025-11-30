import discord
from discord.ext import commands

@commands.command(name="sendrateserverinfo")
async def send_rate_server_info(ctx, user_id: int):
    """Send a 'Rate our server' embed to a specific user via DM."""
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("Only administrators can use this command.")
        return

    guild = ctx.guild
    user = guild.get_member(user_id)

    if user is None:
        await ctx.send("I couldn't find a user with that ID.")
        return
    
    star_rating = "⭐" * 5
    rating_description = "How would you rate our server? Please leave your feedback! 😎"

    embed = discord.Embed(
        title="😇 Thank You for Being With Us! 😇",
        description=f"**{user.display_name}**, you've been on our server for a while! Would you like to rate our server? 🥰",
        color=discord.Color.blue()
    )
    embed.add_field(name="📝 Rate Us!", value=rating_description, inline=False)
    embed.add_field(name="Your Star Rating:", value=star_rating, inline=False)
    embed.add_field(
        name="🌟 Leave Feedback!",
        value="You can do that here: [Rate us on Disboard](https://disboard.org/pl/server/1294993835717562470)",
        inline=False
    )
    embed.set_footer(text="Your feedback is important to us!")
    embed.set_thumbnail(url="https://example.com/path_to_your_thumbnail.png")  # zamień URL na właściwy

    try:
        await user.send(embed=embed)
        await ctx.send(f"Message sent to {user.display_name}!")
    except discord.Forbidden:
        await ctx.send(f"I can't send a message to {user.display_name} because their DMs are closed.")
    except Exception as e:
        print(f"An error occurred: {e}")
        await ctx.send("An error occurred while trying to send the message.")

async def setup(bot):
    bot.add_command(send_rate_server_info)
