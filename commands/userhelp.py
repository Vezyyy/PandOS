import discord
from discord.ext import commands

class UserHelpCommand(commands.DefaultHelpCommand):
    async def send_bot_help(self, ctx):
        embed1 = discord.Embed(
            title="PandOS Bot Help (Part 1)",
            description="Below are the basic commands you can use:",
            color=discord.Color.blue(),
        )
        embed1.add_field(name="$VerifyMe", value="Receive your verification code in DMs.", inline=False)
        embed1.add_field(name="$start <code>", value="Use the code received via `$VerifyMe` to verify yourself.", inline=False)
        embed1.add_field(name="$ping", value="Check the bot's latency.", inline=False)
        embed1.add_field(name="$uptime", value="Shows the bot's uptime.", inline=False)
        await ctx.send(embed=embed1)

        embed2 = discord.Embed(
            title="PandOS Bot Help (Part 2)",
            description="Here are some user-related commands:",
            color=discord.Color.blue(),
        )
        embed2.add_field(name="$gambuildjson", value="Rebuild your gambling.json account in the system.", inline=False)
        embed2.add_field(name="$lvl <user>", value="Check the level and XP of a user.", inline=False)
        embed2.add_field(name="$toplvl", value="View the top 10 users based on level and XP.", inline=False)
        embed2.add_field(name="$balance", value="Check your current balance of PanDollars ($P).", inline=False)
        embed2.add_field(name="$gambling <game> <amount>", value="Play a gambling game with your PanDollars ($P).", inline=False)
        embed2.add_field(name="$roulette <color> <amount>", value="Play roulette with PanDollars ($P).", inline=False)
        embed2.add_field(name="$russianroulette <amount>", value="Play Russian Roulette with 50% chance.", inline=False)
        embed2.add_field(name="$teamrank", value="Check the ranking of teams based on points.", inline=False)
        embed2.add_field(name="$topg or $topgambling", value="Top 10 richest users based on PanDollars ($P).", inline=False)
        embed2.add_field(name="$topl", value="Shortcut to `$toplvl` top 10 users.", inline=False)
        embed2.add_field(name="$buyprotection <time_period>", value="Buy protection from robbers.", inline=False)
        embed2.add_field(name="$rob <user>", value="Attempt to rob another user.", inline=False)
        embed2.add_field(name="$shop", value="Browse and buy items or services.", inline=False)
        embed2.add_field(name="$buy <item>", value="Purchase an item from the shop.", inline=False)
        embed2.add_field(name="$buyrank <rank_name>", value="Buy a special rank from the server.", inline=False)
        embed2.add_field(name="$ranks", value="View available ranks to buy with PandoCoin.", inline=False)
        embed2.add_field(name="$pcoin", value="Check the current exchange rate of PandoCoin.", inline=False)
        embed2.add_field(name="$exchange", value="Exchange your currency to PandoCoin.", inline=False)
        embed2.add_field(name="$inv", value="Check your inventory.", inline=False)
        await ctx.send(embed=embed2)

        embed3 = discord.Embed(
            title="PandOS Bot Help (Part 3)",
            description="Fun user commands:",
            color=discord.Color.blue(),
        )
        embed3.add_field(name="$bonk <@user>", value="Bonk anyone you want! 🪄", inline=False)
        embed3.add_field(name="$kill <@user>", value="Kill someone hilariously! 💀", inline=False)
        embed3.add_field(name="$hug <@user>", value="Send a virtual hug! 🤗", inline=False)
        embed3.add_field(name="$slap <@user>", value="Playfully slap someone! 👋😆", inline=False)
        embed3.add_field(name="$simp <@user>", value="Check simping percentage! 😳", inline=False)
        embed3.add_field(name="$gooner <@user>", value="Check gooner percentage! 😳", inline=False)
        embed3.add_field(name="$ship <@user1> <@user2>", value="Love compatibility between two users. ❤️", inline=False)
        embed3.add_field(name="$fullscan <@user1> <@user2>", value="Complete compatibility and personality scan. 🔍", inline=False)
        embed3.add_field(name="$gooneroftheday", value="Ultimate gooner of the day shoutout! 👑", inline=False)
        embed3.add_field(name="$call <@user>", value="Call the user to your VC with a private notification.", inline=False)
        await ctx.send(embed=embed3)

@commands.command(name="userhelp")
async def userhelp(ctx):
    """Shows help for normal users."""
    await UserHelpCommand().send_bot_help(ctx)

async def setup(bot):
    bot.add_command(userhelp)
    bot.help_command = UserHelpCommand()
