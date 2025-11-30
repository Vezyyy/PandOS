import discord
from discord.ext import commands
from PandOS_Config import GUILD_ID, PARTNERSHIP_ROLE_ID  

@commands.command(name="partnership_end")
async def partnership_end(ctx, user_id: int):
    """Removes the 'Partnership Program' role from a user and sends a termination DM."""
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ **You do not have permission to use this command. Only admins can do this.**")
        return

    try:
        guild = await ctx.bot.fetch_guild(GUILD_ID)
        member = await guild.fetch_member(user_id)

        if not member:
            await ctx.send("❌ **User not found on the server!**")
            return

        role = guild.get_role(PARTNERSHIP_ROLE_ID)
        if role not in member.roles:
            await ctx.send(f"⚠️ <@{user_id}> does not have the partnership role!")
            return

        await member.remove_roles(role)

        embed = discord.Embed(
            title="❌ Partnership Termination with BetterSideOfGaming ❌",
            description=(
                "Your partnership with BetterSideOfGaming has been terminated. Thank you for the cooperation so far!\n\n"
                "If you ever wish to join us again, we are open to discussions. 😊\n\n"
                "🔗 [Better Side Of Gaming - Discord Server](https://vezyyy.github.io/BetterSideOfGaming/)\n\n"
                "We wish you the best in your future endeavors! 🎮"
            ),
            color=discord.Color.red()
        )
        embed.set_footer(text="BetterSideOfGaming")

        try:
            await member.send(embed=embed)
            await ctx.send(f"✅ **Partnership terminated for <@{user_id}>!**")
        except discord.Forbidden:
            await ctx.send(f"⚠️ Could not send a message to <@{user_id}>. Please check if their DMs are open.")
        except Exception as e:
            await ctx.send(f"⚠️ An error occurred while sending the message: {e}")

    except discord.NotFound:
        await ctx.send("❌ **User or server not found!**")
    except discord.Forbidden:
        await ctx.send("⚠️ The bot does not have permission to remove roles on the server.")
    except Exception as e:
        await ctx.send(f"⚠️ An error occurred: {e}")

async def setup(bot):
    bot.add_command(partnership_end)
