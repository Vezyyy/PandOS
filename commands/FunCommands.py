import discord
from discord.ext import commands
import random
import PandOS_functions
from PandOS_functions import get_progress_bar

class FunCommands(commands.Cog):
    """Fun user commands like bonk, slap, hug, kill."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bonk(self, ctx, user: discord.Member):
        gify = [
            "https://tenor.com/view/vorzek-vorzneck-oglg-og-lol-gang-gif-24901093",
            "https://tenor.com/view/bonk-v%C3%A0o-m%E1%BA%B7t-c%C3%A1i-c%C3%A1m-bonk-anime-bonk-meme-bonk-dog-gif-26069974",
            "https://tenor.com/view/bonk-gif-19410756",
            "https://tenor.com/view/bubu-bonk-bubu-dudu-gif-8932107540415697346",
            "https://tenor.com/view/bonk-gif-13392138837084579216",
            "https://tenor.com/view/cat-cat-bonk-bonk-cat-attack-white-cat-bonk-camera-gif-12579285308205623581",
            "https://tenor.com/view/bonk-hurt-pain-gif-19380087",
            "https://tenor.com/view/dog-enforcement-agency-dea-on-solana-dog-meme-solana-blockchain-meme-wif-bitcoin-eth-pumpfun-crypto-meme-gif-460534289763482698",
        ]
        await ctx.send(f"{ctx.author.mention} bonking you! {user.mention}!\n{random.choice(gify)}")

    @commands.command()
    async def slap(self, ctx, user: discord.Member):
        gifs = [
            "https://tenor.com/view/shut-up-stfu-shut-your-mouth-slap-slapping-gif-8050553153066707611",
            "https://tenor.com/view/powerslap-slap-ko-knockout-slap-huge-slap-big-slap-gif-7471918422486227772",
            "https://tenor.com/view/batman-robin-slap-cachetada-meme-cachetazo-gif-14588588888076113146",
            "https://tenor.com/view/blu-zushi-black-and-white-emotes-gif-13851867247344432124",
            "https://tenor.com/view/slap-gif-20040176",
            "https://tenor.com/view/penguin-slap-gif-5263949288532448516",
            "https://tenor.com/view/taiga-toradora-fast-slap-slap-baka-gif-11264049955690132886",
        ]
        await ctx.send(f"{ctx.author.mention} slapped {user.mention}! 👋\n{random.choice(gifs)}")

    @commands.command()
    async def hug(self, ctx, user: discord.Member):
        gifs = [
            "https://tenor.com/view/cat-gif-6892218099699146160",
            "https://tenor.com/view/hug-hugs-cuddle-gif-17754615575577561160",
            "https://tenor.com/view/don-gif-9520776680112053549",
            "https://tenor.com/view/mocha-and-milk-bears-milk-mocha-cuddle-squeeze-gif-7102673578086768359",
            "https://tenor.com/view/milk-mocha-milkandmochabears-hug-gif-2028452320346344814",
            "https://tenor.com/view/gm-gif-14332100165411847198",
            "https://tenor.com/view/j3pot2-gif-2557771429576618217",
        ]
        await ctx.send(f"{ctx.author.mention} gives a big hug to {user.mention}! 🤗\n{random.choice(gifs)}")

    @commands.command()
    async def fuck(self, ctx, user: discord.Member):
        """A chaotic fun command with absurd interactions."""
        actions = [
            f"{ctx.author.mention} absolutely annihilated {user.mention} with pure chaos! 💥",
            f"{ctx.author.mention} summoned a horde of angry hamsters to chase {user.mention}! 🐹🔥",
            f"{ctx.author.mention} turned {user.mention} into a dancing pineapple. 🍍💃",
            f"{ctx.author.mention} unleashed a meme storm on {user.mention}. 🌪️😂",
            f"{ctx.author.mention} sent {user.mention} into an alternate dimension of confusion. 🌀",
        ]
        gifs = [
            "https://tenor.com/view/six-sex-sex-gif-6103032727660715783",
            "https://tenor.com/view/sex-angry-sex-gif-9749140323280595314",
            "https://tenor.com/view/dudu-massage-bubu-ass-oh-yeah-baby-cute-couples-i-am-in-love-we-having-sex-tonight-gif-7417278152853129619",
            "https://tenor.com/view/ted-teddy-bear-bear-hump-humping-gif-4762693",
        ]
        embed = discord.Embed(
            title="💥 Absolute Chaos!",
            description=random.choice(actions),
            color=discord.Color.dark_red()
        )
        embed.set_footer(text=f"{ctx.author.display_name} is feeling chaotic...")
        await ctx.send(embed=embed)
        await ctx.send(f"{random.choice(gifs)}")

    @commands.command()
    async def kill(self, ctx, user: discord.Member):
        deaths = [
            f"{user.mention} got obliterated by a stampede of rubber ducks shooting lasers from their eggs. 🥚🔫🦆",
            f"{user.mention} was folded into a burrito by sentient IKEA manuals. 🌯📘",
            f"{user.mention} tripped over a quantum banana and fell into the backrooms of reality. 🍌🌀",
            f"{user.mention} got reverse-born by a potato priest chanting in Latin. 🥔✝️",
            f"{user.mention} was 360 no-scoped by a toaster with WiFi. 🔫🍞📶",
            f"{user.mention} was abducted by cows riding UFOs powered by memes. 👽🐄😂",
            f"{user.mention} exploded after hearing the forbidden Shrek dub in reverse. 💚🔊",
            f"{user.mention} got yeeted into the 4th dimension by a screaming goose with a frying pan. 🪿🥄",
            f"{user.mention} was compressed into a JPEG by ancient TikTok magic. 🧙‍♂️📸",
            f"{user.mention} got deleted by a Windows XP update that never finished installing. 💀💾",
            f"{user.mention} was hypnotized by dancing pickles and walked into the sun. 🥒🌞",
            f"{user.mention} lost a staring contest with a cursed Furby and ceased to exist. 👁️👁️",
            f"{user.mention} was kissed by a walrus with nuclear lips. 💋🐋💥",
            f"{user.mention} merged with a gopnik dimension and became eternal slav energy. 🧢🚬",
            f"{user.mention} was bonked into oblivion by a sentient frying pan shouting “BONK!” 🔨👻",
            f"{user.mention} got evaporated by a Google Doc that learned how to scream. 📄📢",
            f"{user.mention} was hugged too hard by a spaghetti monster. 🍝❤️",
            f"{user.mention} was devoured by a black hole made entirely of dad jokes. 🕳️😅",
            f"{user.mention} got Rickrolled so hard they entered the shadow realm. 🎵🚪",
            f"{user.mention} was crushed to death by the mighty thighs of BONCAJ674. 💪🍑",
            f"{user.mention} got fricked to death by a horny beetroot named BARSZCZU. 🥵🥄🌶️",
        ]
        gifs = [
            "https://tenor.com/view/kill-me-gif-19956322",
            "https://tenor.com/view/gun-shooting-dont-be-a-menace-funny-lmao-gif-6119299",
            "https://tenor.com/view/gun-gif-22839895",
            "https://tenor.com/view/rambo-shooting-gif-23980108",
            "https://tenor.com/view/fireworks-4th-of-july-fourth-of-july-drunk-man-shooting-fireworks-gif-6998278431839877101",
            "https://tenor.com/view/atheer-gun-michael-scott-the-office-ath-gif-23470765",
            "https://tenor.com/view/shooting-fire-gun-bang-falling-down-gif-14742266",
            "https://tenor.com/view/jumpinpenguin-carry-jp-jp-carry-jumpinpenguin19-official-jp-carry-gif-1962217404091130615",
        ]
        embed = discord.Embed(
            title="💀 Absurd Kill Executed!",
            description=random.choice(deaths),
            color=discord.Color.red(),
        )
        embed.set_footer(text=f"{ctx.author.display_name} tried to kill them...")
        await ctx.send(embed=embed)
        await ctx.send(f"{random.choice(gifs)}")

    @commands.command()
    async def ship(self, ctx, user1: discord.Member, user2: discord.Member):
        score = random.randint(0, 100)
        bar = get_progress_bar(score)
        if score >= 90:
            comment = "💘 Soulmates. Get a room already!"
            emoji = "💘"
        elif score >= 80:
            comment = "💖 True love! That spark is real."
            emoji = "💖"
        elif score >= 70:
            comment = "💕 Super compatible – you’d make a cute couple."
            emoji = "💕"
        elif score >= 60:
            comment = "💞 Something is definitely there."
            emoji = "💞"
        elif score >= 50:
            comment = "💗 Getting warm. This could work!"
            emoji = "💗"
        elif score >= 40:
            comment = "💬 Maybe after a few dates..."
            emoji = "💬"
        elif score >= 30:
            comment = "💔 Friends with potential, but not quite there."
            emoji = "💔"
        elif score >= 20:
            comment = "❄️ Just friends. Or maybe not even that..."
            emoji = "❄️"
        elif score >= 10:
            comment = "🚧 Compatibility error. Please reboot."
            emoji = "🚧"
        else:
            comment = "🚫 Not meant to be. Abort mission!"
            emoji = "🚫"

        embed = discord.Embed(
            title="💘 Shipping Calculator",
            description=f"{user1.mention} + {user2.mention} = **{score}%** match!\n`{bar}`",
            color=discord.Color.purple(),
        )
        embed.add_field(name="Result", value=comment)
        embed.set_footer(text="Love is in the code 💻❤️")
        message = await ctx.send(embed=embed)
        await message.add_reaction(emoji)

    @commands.command()
    async def simp(self, ctx, user: discord.Member):
        percent = random.randint(0, 100)
        bar = get_progress_bar(percent)

        if percent >= 90:
            comment = "🫡 The ultimate simp. Knees permanently bent."
            emoji = "🫡"
        elif percent >= 80:
            comment = "🚨 Major simp alert. Get help."
            emoji = "🚨"
        elif percent >= 70:
            comment = "😳 You're simping a bit too hard."
            emoji = "😳"
        elif percent >= 60:
            comment = "😩 High simp energy. Take a break."
            emoji = "😩"
        elif percent >= 50:
            comment = "😬 Slightly down bad..."
            emoji = "😬"
        elif percent >= 40:
            comment = "😅 Some simp traces detected."
            emoji = "😅"
        elif percent >= 30:
            comment = "🙂 Not too simpy. Could go either way."
            emoji = "🙂"
        elif percent >= 20:
            comment = "🧊 Almost clean. Stay strong."
            emoji = "🧊"
        elif percent >= 10:
            comment = "💤 Simp levels nearly undetectable."
            emoji = "💤"
        else:
            comment = "✅ 100% certified non-simp. Respect."
            emoji = "✅"

        embed = discord.Embed(
            title="😳 Simp Scanner",
            description=f"{user.mention} is simping at **{percent}%** level!\n`{bar}`",
            color=discord.Color.blurple(),
        )
        embed.add_field(name="Analysis", value=comment, inline=False)
        embed.set_footer(text="No judgement... maybe.")
        message = await ctx.send(embed=embed)
        await message.add_reaction(emoji)

    @commands.command()
    async def gooner(self, ctx, user: discord.Member):
        percent = random.randint(0, 100)
        bar = get_progress_bar(percent)

        if percent == 100:
            rank = "🧠 Infinite Loop Gooner"
            comment = "You've reached the peak. You're not even gooning — you **are** the goon. The tab is now your home screen."
            emoji = "🧠"
        elif percent >= 90:
            rank = "👑 Gooner Master Supreme"
            comment = "You have ascended. There's no coming back."
            emoji = "👑"
        elif percent >= 80:
            rank = "🚨 Goon General"
            comment = "You've lost the plot. Absolute madlad."
            emoji = "🚨"
        elif percent >= 70:
            rank = "💀 Tab Collector"
            comment = "15 tabs open. You’re in deep."
            emoji = "💀"
        elif percent >= 60:
            rank = "🌀 Edging Enthusiast"
            comment = "You've been here before. And stayed."
            emoji = "🌀"
        elif percent >= 50:
            rank = "😵‍💫 Session Starter"
            comment = "We see you. And so does your browser history."
            emoji = "😵‍💫"
        elif percent >= 40:
            rank = "😶‍🌫️ Goon Initiate"
            comment = "You've entered the path of the goon."
            emoji = "😶‍🌫️"
        elif percent >= 30:
            rank = "😳 Soft Stroker"
            comment = "A bit of motion detected... tread carefully."
            emoji = "😳"
        elif percent >= 20:
            rank = "🫣 Curious Clicker"
            comment = "Mild curiosity. You’ve opened the tab."
            emoji = "🫣"
        elif percent >= 10:
            rank = "🙈 Mild Observer"
            comment = "You peek, but you don’t participate... yet."
            emoji = "🙈"
        else:
            rank = "🧊 Ice-Hearted Monk"
            comment = "Zero goon vibes detected. Cold as steel."
            emoji = "🧊"

        embed = discord.Embed(
            title="🧠 Gooner Intensity Scanner",
            description=f"{user.mention} is gooning at **{percent}%** level!\n`{bar}`",
            color=discord.Color.purple(),
        )
        embed.add_field(name="Rank", value=rank, inline=True)
        embed.add_field(name="Analysis", value=comment, inline=False)
        embed.set_footer(text="Don't hate the goon, hate the game.")
        message = await ctx.send(embed=embed)
        await message.add_reaction(emoji)

    @commands.command()
    async def fullscan(self, ctx, user1: discord.Member, user2: discord.Member):
        gooner_percent = random.randint(0, 100)
        simp_percent = random.randint(0, 100)
        ship_percent = random.randint(0, 100)

        gooner_bar = get_progress_bar(gooner_percent)
        simp_bar = get_progress_bar(simp_percent)
        ship_bar = get_progress_bar(ship_percent)

        average_percent = (gooner_percent + simp_percent + ship_percent) // 3
        overall_bar = get_progress_bar(average_percent)

        final_emoji = (
            "🔥" if average_percent >= 75 else "💤" if average_percent < 30 else "😬"
        )

        embed = discord.Embed(
            title="📊 Full Degeneracy Scan",
            description=f"Target: **{user1.mention}**\nPartner: **{user2.mention}**",
            color=discord.Color.gold(),
        )

        embed.add_field(
            name="🧠 Gooner Rating",
            value=f"`{gooner_bar}` **{gooner_percent}%**",
            inline=False,
        )
        embed.add_field(
            name="😳 Simp Rating", value=f"`{simp_bar}` **{simp_percent}%**", inline=False
        )
        embed.add_field(
            name="💘 Ship Compatibility",
            value=f"{user1.mention} + {user2.mention} = **{ship_percent}%**\n`{ship_bar}`",
            inline=False,
        )
        embed.add_field(
            name="📈 Overall Degeneracy Score",
            value=f"`{overall_bar}` **{average_percent}%**",
            inline=False,
        )

        embed.set_footer(text="Science doesn't lie. Mostly.")
        embed.set_thumbnail(url=user1.display_avatar.url)

        message = await ctx.send(embed=embed)
        await message.add_reaction(final_emoji)

async def setup(bot):
    await bot.add_cog(FunCommands(bot))
