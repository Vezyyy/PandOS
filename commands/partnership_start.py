import discord
from discord.ext import commands
from PandOS_Config import GUILD_ID, PARTNERSHIP_ROLE_ID

@commands.command(name="partnership_start")
async def partnership_start(ctx, user_id: int):
    """Assigns the 'Partnership Program' role to a user and sends a welcome DM."""
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
        if role in member.roles:
            await ctx.send(f"⚠️ <@{user_id}> already has the partnership role!")
            return

        await member.add_roles(role)

        embed = discord.Embed(
            title="🎉 Welcome to the BetterSideOfGaming Partnership Program! 🎉",
            description=(
                "Thank you for joining our partnership program on Discord! We are excited to have you as part of our community, "
                "and we hope our collaboration will be beneficial to both parties.\n\n"
                "If you have any questions or concerns, feel free to reach out to the server admins or contact us through our website:\n\n"
                "🔗 [Better Side Of Gaming - Discord Server](https://vezyyy.github.io/BetterSideOfGaming/)\n\n"
                "Once again, thank you, and we look forward to a successful partnership! 🚀🎮"
            ),
            color=discord.Color.green()
        )
        embed.set_footer(text="BetterSideOfGaming")

        try:
            await member.send(embed=embed)
            await ctx.send(f"✅ **Partnership started for <@{user_id}>!**")
        except discord.Forbidden:
            await ctx.send(f"⚠️ Could not send a message to <@{user_id}>. Please check if their DMs are open.")
        except Exception as e:
            await ctx.send(f"⚠️ An error occurred while sending the message: {e}")

    except discord.NotFound:
        await ctx.send("❌ **User or server not found!**")
    except discord.Forbidden:
        await ctx.send("⚠️ The bot does not have permission to assign roles or send messages.")
    except Exception as e:
        await ctx.send(f"⚠️ An error occurred: {e}")

async def setup(bot):
    bot.add_command(partnership_start)
