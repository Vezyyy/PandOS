import discord
from discord.ext import commands

@commands.command(name="announcement")
@commands.has_permissions(administrator=True)
async def announcement(ctx, *, message: str):
    """Send a DM announcement to all members of the server."""
    if ctx.guild is None:
        await ctx.send("This command cannot be used in DMs.")
        return

    sent_count = 0
    failed_members = []
    sent_to = set()

    for member in ctx.guild.members:
        if member.id not in sent_to:
            try:
                if member.dm_channel is None:
                    await member.create_dm()
                await member.send(message)
                sent_count += 1
                sent_to.add(member.id)
            except discord.Forbidden:
                print(f"Could not send DM to {member.name}: DMs disabled.")
                failed_members.append(member.name)
            except discord.HTTPException as e:
                print(f"HTTPException while sending DM to {member.name}: {e}")
                failed_members.append(member.name)
            except Exception as e:
                print(f"Unexpected error with {member.name}: {e}")
                failed_members.append(member.name)

    await ctx.send(f"Announcement has been sent to {sent_count} members!")

    if failed_members:
        await ctx.send(
            f"Failed to send the announcement to: {', '.join(failed_members)}."
        )

async def setup(bot):
    bot.add_command(announcement)