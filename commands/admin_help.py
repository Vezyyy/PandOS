import discord
from discord.ext import commands

class AdminHelpCommand(commands.DefaultHelpCommand):
    async def send_bot_help(self, ctx):
        embed3 = discord.Embed(
            title="PandOS Bot Help (Admin Commands)",
            description="These are the administrative commands:",
            color=discord.Color.red(),
        )
        embed3.add_field(name="$ban <user>", value="Ban a user from the server.", inline=False)
        embed3.add_field(name="$kick <user>", value="Kick a user from the server.", inline=False)
        embed3.add_field(name="$mute <user> <time>", value="Mute a user for a specific time (minutes).", inline=False)
        embed3.add_field(name="$unmute <user>", value="Unmute a user.", inline=False)
        embed3.add_field(name="$addrole <user> <role>", value="Add a role to a user.", inline=False)
        embed3.add_field(name="$removerole <user> <role>", value="Remove a role from a user.", inline=False)
        embed3.add_field(name="$serverinfo", value="Display server info like member count and creation date.", inline=False)
        embed3.add_field(name="$Pwarn <user> <reason>", value="Warn a user (Admin only).", inline=False)
        embed3.add_field(name="$warnings <user>", value="Check the warnings of a user.", inline=False)
        embed3.add_field(name="$resetwarnings <user>", value="Reset a user's warnings.", inline=False)
        embed3.add_field(name="$twm", value="Test the welcome message.", inline=False)
        embed3.add_field(name="$ping", value="Check bot's latency.", inline=False)
        embed3.add_field(name="$uptime", value="Shows the bot's uptime.", inline=False)
        embed3.add_field(name="$say <message>", value="Send a message as the bot (Admin only).", inline=False)
        embed3.add_field(name="$announcement <message>", value="Send an announcement to all members (Admin only).", inline=False)
        embed3.add_field(name="$partnership_start (ID)", value="Assign the Partnership Program role. Admin only.\nExample: `$$partnership_start 123456789`", inline=False)
        embed3.add_field(name="$partnership_end (ID)", value="Remove the Partnership Program role. Admin only.\nExample: `$$partnership_end 123456789`", inline=False)
        embed3.add_field(name="$sendrateserverinfo (ID)", value="Send rate server reminder to a user. Admin only.\nExample: `$sendrateserverinfo 123456789`", inline=False)
        await ctx.send(embed=embed3)

@commands.command(name="adminhelp")
async def adminhelp(ctx):
    """Shows help for admin commands."""
    if ctx.author.guild_permissions.administrator:
        await AdminHelpCommand().send_bot_help(ctx)
    else:
        await ctx.send("You need administrator permissions to use this command.")

async def setup(bot):
    bot.add_command(adminhelp)