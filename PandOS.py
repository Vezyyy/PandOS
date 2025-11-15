import discord
from discord.ext import commands
import random
import string
import asyncio
import PandOS_Config 
import time
import datetime
import re
import logging
from PandOS_greetings_data import greetings, conversations 
from BSOG_Team import team_points 
from PandOS_Config import (
    CHAIN_WORDS_CHANNEL_ID,
    PARTNERSHIP_ROLE_ID,
    SERVERS_MESSAGES_CHANNEL_ID,
    NEW_USER_CHANNEL_ID,
    PROTECTED_CHANNELS_IDS,
)
import importlib
import os
import json 
from collections import defaultdict
from discord.ext import commands, tasks
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from io import BytesIO

#################################################################################

# BUILD INFO
# VEZYY BY VPanda & VPanda Studio
# VERSION 6.1.7 - 24.06.2024 Verification System 3.0

#################################################################################

# Download current time for date channel update

current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

#################################################################################

# Bot info
BOT_STATUS = "Online"  
BOT_VERSION = "6.1.7" 

#################################################################################

# ID kanałów do edycji
STATUS_CHANNEL_ID = 1330230361342611588 
VERSION_CHANNEL_ID = 1330230299031896074 
DATE_CHANNEL_ID = 1330235429730910233 

#################################################################################

# Bot configuration
TOKEN = PandOS_Config.TOKEN  
GUILD_ID = PandOS_Config.GUILD_ID  

#################################################################################

# Channel and role IDs
WELCOME_CHANNEL_ID = PandOS_Config.WELCOME_CHANNEL_ID
WWW_CHANNEL_ID = PandOS_Config.WWW_CHANNEL_ID
INVITE_CHANNEL_ID = PandOS_Config.INVITE_CHANNEL_ID
VERIFY_ROLE_ID = PandOS_Config.VERIFY_ROLE_ID
LOG_CHANNEL_ID = PandOS_Config.LOG_CHANNEL_ID
SAY_USER_ID = PandOS_Config.SAY_USER_ID
# Channel ID where media will be shared
MEDIA_SHARE_CHANNEL_ID = PandOS_Config.MEDIA_SHARE_CHANNEL_ID
TARGET_MEDIA_CHANNEL_ID = PandOS_Config.TARGET_MEDIA_CHANNEL_ID
PARTNERSHIP_ROLE_ID = PandOS_Config.PARTNERSHIP_ROLE_ID
GENERAL_CHANNEL_ID = PandOS_Config.GENERAL_CHANNEL_ID
VERIFY_CATEGORY_ID = PandOS_Config.VERIFY_CATEGORY_ID
RULES_LINK = "https://vezyyy.github.io/BetterSideOfGaming/rules.html"

#################################################################################

# VERIFICATION CODES TABLES

verification_codes = {}
accepted_rules = set()

#################################################################################

# STEAM ANNOUNCMENTS

# URL Steam API for featured categories
STEAM_API_URL = "https://store.steampowered.com/api/featuredcategories"

# Steam sales Discord channel ID
DISCORD_CHANNEL_ID_STEAM_SALES = 1295000576211292212 

#################################################################################

# Setting up intents
intents = discord.Intents.default()
intents.members = True  
intents.messages = True
intents.message_content = True  
intents.voice_states = True 

#################################################################################

# Initialize the bot
bot = commands.Bot(command_prefix="$", intents=intents)

#################################################################################

# Dictionary to store verification codes
verification_codes = {}

#################################################################################

# RANDOM PANDOS CONVERSATIONS
# -----------------------------------

# Function to load words from JSON file

def load_words_from_json():
    try:
        with open("words.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data["words"]
    except FileNotFoundError:
        print("Plik 'words.json' nie został znaleziony.")
        return []


# Function to save words to JSON file

def save_words_to_json(words):
    data = {"words": words}
    with open("words.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("Słowa zostały zapisane do pliku 'words.json'.")

# function to remove links from text

def remove_links(text):
    return re.sub(r"http[s]?://\S+|www\.\S+", "", text)

# Collect words from messages in specified channels

async def collect_words(message):
    if message.channel.id in PROTECTED_CHANNELS_IDS:
        return  


    words = load_words_from_json()

    cleaned_message = remove_links(message.content)

    new_words = cleaned_message.split()

    unique_words = set(words)  
    for word in new_words:
        if (
            word.lower() not in unique_words
        ):  
            unique_words.add(
                word.lower()
            )  

    save_words_to_json(list(unique_words))


# Function to generate a random sentence

def generate_random_sentence():
    words = load_words_from_json()
    if not words:
        return "Sorry, no words available to generate a sentence."

    sentence_length = random.randint(3, 10)  
    sentence = random.sample(words, sentence_length)  
    return " ".join(sentence) 


#################################################################################

# NEW USER GAMBLING ACCOUNT IN PANDOS SYSTEM

# This function adds a new user to the gambling system with default values when they join.
# If the user already exists but has missing data fields, it adds those fields with default values.
# Finally, it saves the updated data back to the JSON file.

def add_user_on_join(user_id):
    user_id = str(user_id) 

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}  
    else:
        data = {}

    if user_id not in data:
        data[user_id] = {
            "balance": 0,
            "last_work": 0,
            "last_robbery": 0,
            "failed_rob_attempts": 0,
            "protection_end": 0,
            "inventory": {"PandoCoin": 0}, 
            "last_rob_time": 0,
            "pando_balance": 0,
        }
        print(
            f"✅ Użytkownik {user_id} został dodany do pliku z domyślnymi wartościami."
        )
    else:
        user_data = data[user_id]
        updated = False

        required_fields = {
            "balance": 0,
            "last_work": 0,
            "last_robbery": 0,
            "failed_rob_attempts": 0,
            "protection_end": 0,
            "inventory": {}, 
            "last_rob_time": 0,
            "pando_balance": 0,
        }

        for field, default_value in required_fields.items():
            if field not in user_data:
                user_data[field] = default_value
                updated = True

        if "inventory" not in user_data or not isinstance(user_data["inventory"], dict):
            user_data["inventory"] = {"PandoCoin": 0}
            updated = True
        elif "PandoCoin" not in user_data["inventory"]:
            user_data["inventory"]["PandoCoin"] = 0
            updated = True

        if updated:
            data[user_id] = user_data
            print(f"🔄 Użytkownik {user_id} miał brakujące dane, które zostały dodane.")
        else:
            print(f"✅ Użytkownik {user_id} ma już wszystkie wymagane dane.")

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


#################################################################################

# GAMBLING
# GAMBLING LOAD
# This section handles loading and saving user data for the gambling system.
# The data is stored in a JSON file named "gambling.json".
# Functions are provided to load and save the data.
# Usage: load_data() and save_data(data)

file_path = "gambling.json"


def load_data():
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            json.dump({}, file)

    if os.path.getsize(file_path) == 0:
        return {}

    with open(file_path, "r") as file:
        return json.load(file)

def save_data(data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


# -----------------------------------------------------------------

# PANDO COIN RATE UPDATE
# This section handles the dynamic exchange rate of PandoCoin.
# The rate changes every 30 seconds within a range of -2% to +2%.
# The current rate and its history are stored in a JSON file.
# A command is provided to display the current rate and a graph of historical rates.

rate_file_path = "pandocoin_rate.json"
gambling_file_path = "gambling.json"


def load_pandocoin_data():
    if not os.path.exists(rate_file_path):
        return {"rate": 1, "history": [1]} 
    with open(rate_file_path, "r") as file:
        return json.load(file)


def save_pandocoin_data(data):
    with open(rate_file_path, "w") as file:
        json.dump(data, file, indent=4)


def simulate_rate_change(current_rate):
    change_percentage = random.uniform(
        -0.02, 0.02
    )  
    new_rate = current_rate * (1 + change_percentage)
    return round(new_rate, 2)


@tasks.loop(seconds=30)  
async def update_pandocoin_rate():
    data = load_pandocoin_data()  
    new_rate = simulate_rate_change(data["rate"])  

    data["rate"] = new_rate
    data["history"].append(new_rate)

    if len(data["history"]) > 100:
        data["history"].pop(0)

    save_pandocoin_data(data)

# -----------------------------------------------------------------
# PANDO COIN COMMAND
# This command displays the current exchange rate of PandoCoin and a graph of its historical rates.
# Usage: $pandocoin or $pcoin

@bot.command(name="pandocoin", aliases=["pcoin"])
async def pandocoin(ctx):
    data = load_pandocoin_data()
    current_rate = data["rate"]

    plt.figure(figsize=(8, 5))
    plt.plot(data["history"], color="purple", marker="o")
    plt.title("PandoCoin Exchange Rate History", fontsize=14)
    plt.xlabel("Time (30 second intervals)", fontsize=12)
    plt.ylabel("1 PandoCoin = $P", fontsize=12)
    plt.grid(True)

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)

    embed = discord.Embed(
        title="💎 **PandoCoin (P₿) Exchange Rate** 💰",
        description=f"Current exchange rate for **1 PandoCoin** is **{current_rate} $P**.\n"
        "Want to buy less than 1 PandoCoin? You can purchase fractional PandoCoins!",
        color=discord.Color.purple(),
    )
    embed.set_image(url="attachment://pandocoin_rate.png")

    await ctx.send(embed=embed, file=discord.File(buf, "pandocoin_rate.png"))


def load_user_data():
    if not os.path.exists(gambling_file_path):
        return {}  
    with open(gambling_file_path, "r") as file:
        return json.load(file)


def save_user_data(data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def load_user_data():
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r") as file:
        return json.load(file)


def save_user_data(data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


# -----------------------------------------------------------------

# EXCHANGE COMMAND
# This command allows users to exchange their in-game currency ($P) for PandoCoin.
# Usage: $exchange <amount>

@bot.command(name="exchange")
async def exchange_pando(ctx, amount: float):
    user_id = str(ctx.author.id)
    file_path = "gambling.json"

    data = load_pandocoin_data()
    exchange_rate = data["rate"]  

    with open(file_path, "r") as file:
        user_data = json.load(file)

    if user_id not in user_data:
        await ctx.send("❌ You don't have any funds to exchange!")
        return

    if user_data[user_id]["balance"] < amount:
        await ctx.send(
            f"❌ You don't have enough $P to exchange! You have only {user_data[user_id]['balance']} $P."
        )
        return

    pando_coins = round(
        amount / exchange_rate, 2
    )  

    if pando_coins < 0.01: 
        await ctx.send("❌ Minimum exchange is 0.01 PandoCoin!")
        return

    user_data[user_id]["balance"] -= amount

    if "inventory" not in user_data[user_id]:
        user_data[user_id]["inventory"] = {}

    if "PandoCoin" in user_data[user_id]["inventory"]:
        user_data[user_id]["inventory"]["PandoCoin"] += pando_coins
    else:
        user_data[user_id]["inventory"]["PandoCoin"] = pando_coins

    with open(file_path, "w") as file:
        json.dump(user_data, file, indent=4)

    await ctx.send(
        f"✅ You exchanged **{amount} $P** for **{pando_coins} PandoCoin(s)**! 🎉\n"
        f"📦 **Added to inventory:** {pando_coins} PandoCoin 🏦\n"
        f"💰 **Remaining balance:** {user_data[user_id]['balance']} $P"
    )


# -----------------------------------------------------------------

# SET PANDO COIN RATE
# This command allows administrators to set a new exchange rate for PandoCoin.
# Usage: $setrate <new_rate>

@bot.command(name="setrate")
@commands.has_permissions(administrator=True)
async def admin_set_exchange_rate(ctx, new_rate: int):
    global exchange_rate
    exchange_rate = new_rate
    await ctx.send(f"✅ Nowy kurs wymiany: **10,000 $P = {new_rate} PandoCoin**")


# -----------------------------------------------------------------

# GIVE PANDO COIN
# This command allows administrators to give PandoCoin to a specified user.
# Usage: $givepando @user <amount>

@bot.command(name="givepando")
@commands.has_permissions(administrator=True)
async def admin_give_pando(ctx, member: discord.Member, amount: int):
    user_id = str(member.id)
    file_path = "gambling.json"

    with open(file_path, "r") as file:
        data = json.load(file)

    if user_id not in data:
        data[user_id] = {"balance": 0, "pando_balance": 0, "inventory": {}}

    data[user_id]["pando_balance"] += amount

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

    await ctx.send(f"✅ Dodano **{amount} PandoCoin** dla {member.mention}!")


# -----------------------------------------------------------------

# Buy Ranks For Panda Coins
# This command allows users to buy ranks using their PandoCoin balance.
# Usage: $buyrank <rank_name>

@bot.command(name="buyrank")
async def buy_rank(ctx, rank_name: str):
    user_id = str(ctx.author.id)
    file_path = "gambling.json"

    ranks = {"VIP": 2, "Megalodon": 5, "Crypto King": 10}  

    if rank_name not in ranks:
        await ctx.send("❌ This rank does not exist in the shop!")
        return

    with open(file_path, "r") as file:
        data = json.load(file)

    if user_id not in data or data[user_id].get("pando_balance", 0) < ranks[rank_name]:
        await ctx.send("❌ You don't have enough PandoCoin!")
        return

    data[user_id]["pando_balance"] -= ranks[rank_name]

    role = discord.utils.get(ctx.guild.roles, name=rank_name)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(
            f"✅ You have bought the rank **{rank_name}** for **{ranks[rank_name]} PandoCoin**!"
        )
    else:
        await ctx.send("❌ Role not found on the server!")

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


# -----------------------------------------------------------------

# RANKS LIST
# This command displays the available ranks that users can purchase with PandoCoin.
# Usage: $ranks

@bot.command(name="ranks")
async def ranks(ctx):
    ranks = {"VIP": 2, "Megalodon": 5, "Crypto King": 10}

    embed = discord.Embed(
        title="🌟 Available Ranks to Purchase 🌟",
        description="🎉 Choose the rank you want to buy with your PandoCoin! 🎉",
        color=discord.Color.green(), 
    )

    embed.add_field(
        name="💎 **VIP**",
        value=f"Price: {ranks['VIP']} PandoCoin\nA prestigious rank to show off your status!",
        inline=False,
    )

    embed.set_footer(text="Get your PandoCoin and claim your rank now! 🚀")

    await ctx.send(embed=embed)


# -----------------------------------------------------------------

# TOP GAMBLING
# This command displays the top 10 richest players based on their balance in the gambling system.
# Usage: $topgambling or $topg
# The command retrieves user data from a JSON file, sorts users by their balance, and formats the output in an embedded message.

@bot.command(name="topgambling", aliases=["topg"])
async def top_gambling(ctx):
    data = load_data()
    leaderboard = sorted(data.items(), key=lambda x: x[1]["balance"], reverse=True)[:10]

    def format_number(n):
        return f"{n:,}".replace(",", " ")

    embed = discord.Embed(
        title="🏆 **Top 10 Richest Players** 💰",
        description="These are the players with the highest balance in $P! 🔥💸",
        color=discord.Color.purple(),  
    )

    for i, (user_id, stats) in enumerate(leaderboard, start=1):
        user = await bot.fetch_user(int(user_id))

        formatted_balance = format_number(stats["balance"])

        if i == 1:
            rank_emoji = "🥇"
        elif i == 2:
            rank_emoji = "🥈"
        elif i == 3:
            rank_emoji = "🥉"
        else:
            rank_emoji = "💎"

        embed.add_field(
            name=f"{rank_emoji} **{user.display_name}**",
            value=f"**Balance:** {formatted_balance} $P",
            inline=False,
        )

    embed.set_footer(text="Compete to climb to the top! 💸🔥")

    await ctx.send(embed=embed)


# -----------------------------------------------------------------

# BUY PROTECTION
# This command allows users to buy protection from being robbed for a specified time period.
# Usage: $buyprotection <time_period>
# Available time periods: 1h, 24h, 7d, 30d

@bot.command(name="buyprotection")
async def buy_protection(ctx, time_period: str = None):
    user_id = str(ctx.author.id)
    file_path = "gambling.json"

    protection_prices = {
        "1h": 10000,  
        "24h": 50000, 
        "7d": 250000,  
        "30d": 1000000, 
    }

    if time_period is None:
        await ctx.send(
            "❓ You must specify the protection period! Available options are:\n"
            "`1h` - 1 hour protection for 10,000 $P\n"
            "`24h` - 24 hours protection for 50,000 $P\n"
            "`7d` - 7 days protection for 250,000 $P\n"
            "`30d` - 30 days protection for 1,000,000 $P\n"
            "Usage: `$buyprotection <time_period>`"
        )
        return

    if time_period not in protection_prices:
        await ctx.send(
            "❌ Invalid protection period. Available options are: 1h, 24h, 7d, 30d."
        )
        return

    with open(file_path, "r") as file:
        data = json.load(file)

    price = protection_prices[time_period]
    if data[user_id]["balance"] < price:
        await ctx.send(
            f"❌ You don't have enough balance to buy {time_period} protection."
        )
        return

    data[user_id]["balance"] -= price

    if time_period == "1h":
        protection_end = int(time.time()) + 3600 
    elif time_period == "24h":
        protection_end = int(time.time()) + 86400 
    elif time_period == "7d":
        protection_end = int(time.time()) + 604800 
    elif time_period == "30d":
        protection_end = int(time.time()) + 2592000 

    data[user_id]["protection_end"] = protection_end

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

    await ctx.send(
        f"🎉 You have successfully purchased {time_period} protection for {price} $P."
    )


# -----------------------------------------------------------------

# WORK AND EARN MONEY

# This command allows users to work and earn a random amount of in-game currency with a cooldown period.
# Usage: $work

@bot.command(name="work")
async def work(ctx):
    data = load_data()
    user_id = str(ctx.author.id)

    user_data = data.get(user_id, {"balance": 1000, "last_work": 0})

    last_work = user_data.get("last_work", 0)

    now = int(time.time()) 

    cooldown = 6 * 60 * 60

    if now - last_work < cooldown:
        time_left = cooldown - (now - last_work)
        hours, remainder = divmod(time_left, 3600)
        minutes, _ = divmod(remainder, 60)
        await ctx.send(
            f"{ctx.author.mention}, you can work again in {hours}h {minutes}m."
        )
        return

    earnings = random.randint(100, 2000)
    data[user_id] = {
        "balance": user_data["balance"] + earnings,
        "last_work": now,  
    }
    save_data(data)
    await ctx.send(
        f"{ctx.author.mention}, you worked hard and earned {earnings} $P! 💼"
    )

# -----------------------------------------------------------------
# ROB COMMAND
# This command allows users to attempt to rob another user with a cooldown period.
# Successful robberies yield a percentage of the target's balance, while failed attempts result in a penalty.
# The command checks for target protection and updates user data accordingly.
# Usage: $rob @target_user

@bot.command(name="rob")
async def rob(ctx, target: discord.User):
    user_id = str(ctx.author.id)
    target_id = str(target.id)
    file_path = "gambling.json"

    with open(file_path, "r") as file:
        data = json.load(file)

    print(f"Data before modification: {data}") 

    default_user_data = {
        "balance": 1000,
        "last_work": 0,
        "last_robbery": 0,
        "failed_rob_attempts": 0,
        "protection_end": 0,
        "inventory": {"PandoCoin": 0},
        "last_rob_time": 0,
        "pando_balance": 0,
    }

    if user_id not in data:
        data[user_id] = default_user_data.copy()
    if target_id not in data:
        data[target_id] = default_user_data.copy()

    if data[target_id].get("protection_end", 0) > int(time.time()):
        await ctx.send(f"❌ {target.name} has protection and cannot be robbed!")
        return
    
    current_time = int(time.time())
    cooldown_time = 24 * 60 * 60
    last_rob_time = data[user_id].get("last_robbery", 0)

    if current_time - last_rob_time < cooldown_time:
        remaining_time = cooldown_time - (current_time - last_rob_time)
        remaining_hours = remaining_time // 3600
        remaining_minutes = (remaining_time % 3600) // 60
        await ctx.send(
            f"❌ **{ctx.author.name}**, you can only rob **{target.name}** once every 24 hours. Please wait {remaining_hours}h {remaining_minutes}m."
        )
        return

    success_chance = 50
    chance = random.randint(1, 100)

    if chance <= success_chance:
        rob_amount = int(data[target_id]["balance"] * 0.10)  
        data[user_id]["balance"] += rob_amount
        data[target_id]["balance"] -= rob_amount
        data[user_id]["last_robbery"] = current_time

        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

        await ctx.send(
            f"🎉 **{ctx.author.name}** successfully robbed **{target.name}** and stole {rob_amount} $P!"
        )
        await target.send(
            f"❗️ **{ctx.author.name}** robbed you and stole {rob_amount} $P."
        )
    else:
        penalty = int(data[user_id]["balance"] * 0.10)
        data[user_id]["balance"] -= penalty
        data[target_id]["balance"] += penalty
        data[user_id]["last_robbery"] = current_time
        data[user_id]["failed_rob_attempts"] += 1

        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

        await ctx.send(
            f"❌ **{ctx.author.name}** tried to rob **{target.name}** but failed! You lost {penalty} $P as a penalty, and **{target.name}** gained {penalty} $P."
        )
        await target.send(
            f"❗️ **{ctx.author.name}** tried to rob you but failed! They lost {penalty} $P, and you gained that amount."
        )

# -----------------------------------------------------------------
# ROB BANK COMMAND
# This command allows users to attempt to rob a bank with a cooldown period.
# Successful robberies yield earnings, while failed attempts result in a loss.
# The command checks for cooldowns and updates user data accordingly.
# Usage: $robbank

@bot.command(name="robbank", aliases=["robberybank"])
async def rob(ctx):
    data = load_data()
    user_id = str(ctx.author.id)

    user_data = data.get(
        user_id, {"balance": 1000, "last_robbery": 0}
    )  

    if "last_robbery" not in user_data:
        user_data["last_robbery"] = 0  

    now = int(time.time())

    cooldown = 6 * 60 * 60

    if now - user_data["last_robbery"] < cooldown:
        time_left = cooldown - (now - user_data["last_robbery"])
        hours, remainder = divmod(time_left, 3600)
        minutes, _ = divmod(remainder, 60)
        await ctx.send(
            f"{ctx.author.mention}, you can attempt a robbery again in {hours}h {minutes}m."
        )
        return
    
    if random.random() < 0.3: 
        earnings = random.randint(2000, 5000) 
        user_data["balance"] += earnings 
        user_data["last_robbery"] = now  
        data[user_id] = user_data 
        save_data(data)
        await ctx.send(
            f"{ctx.author.mention}, you successfully robbed the bank and earned {earnings} $P! 🏦"
        )
    else:
        loss = 1000 
        user_data["balance"] -= loss  
        user_data["last_robbery"] = now  
        data[user_id] = user_data 
        save_data(data)
        await ctx.send(
            f"{ctx.author.mention}, you got caught during the robbery and lost {loss} $P. 🚓"
        )


# -----------------------------------------------------------------

# GAMBLING ACCOUNT REPAIR COMMAND

# Register command to create a gambling account for the user
# This command checks if the user is already registered in the gambling system.
# If not, it creates a new entry for the user with default values.
# If the user is already registered but has missing data fields, it adds those fields with default values.
# Finally, it sends a confirmation message to the user.

@bot.command(name="gambuildjson")
async def register(ctx):
    user_id = str(ctx.author.id)  #

    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            json.dump({}, file)
        data = {}
    else:
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
        except json.JSONDecodeError:

            with open(file_path, "w") as file:
                json.dump({}, file)
            data = {}

    if user_id in data:
        await ctx.send(f"❌ **{ctx.author.name}**, you are already registered!")
        return

    data[user_id] = {
        "balance": 1000,  
        "last_work": int(time.time()), 
        "last_robbery": 0,  
        "failed_rob_attempts": 0,  
        "protection_end": 0,  
        "inventory": {},  
        "last_rob_time": 0,  
        "pando_balance": 0,  
    }

    user_data = data[user_id]
    updated = False

    if "balance" not in user_data:
        user_data["balance"] = 1000
        updated = True
    if "last_work" not in user_data:
        user_data["last_work"] = int(time.time())
        updated = True
    if "last_robbery" not in user_data:
        user_data["last_robbery"] = 0
        updated = True
    if "failed_rob_attempts" not in user_data:
        user_data["failed_rob_attempts"] = 0
        updated = True
    if "protection_end" not in user_data:
        user_data["protection_end"] = 0
        updated = True
    if "inventory" not in user_data:
        user_data["inventory"] = {}
        updated = True
    if "last_rob_time" not in user_data:
        user_data["last_rob_time"] = 0
        updated = True
    if "pando_balance" not in user_data:
        user_data["pando_balance"] = 0
        updated = True

    if updated:
        data[user_id] = user_data
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Użytkownik {user_id} miał brakujące dane, które zostały dodane.")

    await ctx.send(
        f"🎉 **{ctx.author.name}**, you have been successfully registered in the gambling system!"
    )


# -----------------------------------------------------------------

# GAMBLING / ACCOUNT

# BALANCE COMMAND
# This command allows users to check their current balance in the gambling system.
# It retrieves the user's data from a JSON file and displays it in an organized embed format.

@bot.command(name="balance", aliases=["bal"])
async def balance(ctx):
    user = str(ctx.author.id)
    file_path = "gambling.json"

    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            json.dump({}, file)

    with open(file_path, "r") as file:
        data = json.load(file)

    if user not in data:
        data[user] = {
            "balance": 1000,
            "inventory": {"PandoCoin": 0},  
        }
    else:
        if "inventory" not in data[user]:
            data[user]["inventory"] = {}

        if "PandoCoin" not in data[user]["inventory"]:
            data[user]["inventory"]["PandoCoin"] = 0

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

    user_balance = data[user]["balance"]
    pando_balance = data[user]["inventory"]["PandoCoin"]

    def format_number(n):
        return f"{n:,}".replace(",", " ")

    formatted_balance = format_number(user_balance)
    formatted_pando = format_number(pando_balance)

    avatar_url = (
        ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
    )

    embed_balance = discord.Embed(
        title=f"💎 **{ctx.author.name}'s Balance** 💰",
        description=(
            f"💵 **PanDollars ($P):** {formatted_balance}\n"
            f"🏦 **PandoCoin (P₿):** {formatted_pando}\n\n"
            "🌟 **Want to earn more?** 🌟\n"
            "Use `$gambling` to play games and grow your balance! 🎰💵"
        ),
        color=discord.Color.blue(), 
    )

    embed_balance.set_thumbnail(url=avatar_url)

    embed_balance.set_footer(text="PandOS Gambling System - Play, Win, Repeat! 🎮")

    await ctx.send(embed=embed_balance)


# -----------------------------------------------------------------

# SHOPPING
# This command allows users to check their inventory, including items they have purchased and the status of any active protection they may have.
# It retrieves the user's data from a JSON file and displays it in an organized embed format.

from datetime import datetime


@bot.command(name="inventory", aliases=["inv"])
async def check_inventory(ctx):
    user_id = str(ctx.author.id)
    file_path = "gambling.json"

    with open(file_path, "r") as file:
        data = json.load(file)

    if user_id not in data:
        data[user_id] = {"balance": 1000, "inventory": {}, "protection_end": 0}
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    user_data = data[user_id]
    inventory = user_data.get("inventory", {})
    protection_end_time = user_data.get("protection_end", 0)

    embed = discord.Embed(
        title=f"📦 {ctx.author.display_name}'s Inventory",
        description="Here are the items you've bought!",
        color=discord.Color.blue(),
    )

    if not inventory:
        embed.add_field(name="No items yet!", value="You haven't bought anything yet.")
    else:
        for item, quantity in inventory.items():
            embed.add_field(name=item, value=f"Quantity: {quantity}", inline=False)

    if protection_end_time > 0:
        current_time = int(datetime.now().timestamp()) 
        remaining_time = protection_end_time - current_time

        if remaining_time > 0:
            remaining_minutes = remaining_time // 60
            remaining_seconds = remaining_time % 60
            embed.add_field(
                name="Protection Status",
                value=f"Your protection is active! Time remaining: {remaining_minutes} minute(s) and {remaining_seconds} second(s).",
                inline=False,
            )
        else:
            embed.add_field(
                name="Protection Status",
                value="Your protection has expired.",
                inline=False,
            )
    else:
        embed.add_field(
            name="Protection Status",
            value="You don't have protection active.",
            inline=False,
        )

    # Wysyłamy embed z ekwipunkiem
    await ctx.send(embed=embed)

# shop command
# this command allows users to view and purchase items from different categories such as Houses, Cars, Clothes, and Luxury Items using their in-game currency ($P). 
# Each category contains a variety of items with their respective prices and descriptions. Users can specify a category to view the items available for purchase within t
# hat category. If no category is specified, the command will display the available categories. The command also checks the user's balance to ensure they have enough funds to make a purchase.
# -----------------------------------------------------------------

@bot.command(name="shop")
async def shop(ctx, category: str = None):
    user = str(ctx.author.id)
    file_path = "gambling.json"

    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            json.dump({}, file)

    with open(file_path, "r") as file:
        data = json.load(file)

    if user not in data:
        data[user] = {"balance": 1000} 
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    user_balance = data[user]["balance"]

    categories = {
        "🏠 **Houses**": {
            "Luxury Studio": {
                "price": 50000,
                "description": "A stylish studio in a premium location with stunning city views.",
            },
            "Penthouse in New York": {
                "price": 200000,
                "description": "A luxurious penthouse in the heart of Manhattan.",
            },
            "Beachfront Mansion": {
                "price": 500000,
                "description": "A magnificent mansion on the beach, perfect for elite living.",
            },
            "Private Island Villa": {
                "price": 2000000,
                "description": "Your own private island with a luxurious villa and pool.",
            },
            "Mountain Retreat": {
                "price": 750000,
                "description": "A beautiful house nestled in the mountains with serene views.",
            },
            "Parisian Loft": {
                "price": 350000,
                "description": "A chic loft in Paris, with a perfect view of the Eiffel Tower.",
            },
            "Dubai Skyscraper Penthouse": {
                "price": 5000000,
                "description": "A stunning penthouse in one of the tallest buildings in Dubai.",
            },
            "Japanese Zen House": {
                "price": 1000000,
                "description": "A peaceful Japanese-style home surrounded by nature and tranquility.",
            },
        },
        "🚗 **Cars**": {
            "Tesla Model S": {
                "price": 100000,
                "description": "A futuristic electric car with cutting-edge technology.",
            },
            "Lamborghini Aventador": {
                "price": 500000,
                "description": "An exotic supercar, designed for speed and style.",
            },
            "Bugatti Chiron": {
                "price": 2500000,
                "description": "One of the fastest cars in the world, an ultimate luxury vehicle.",
            },
            "Rolls-Royce Phantom": {
                "price": 1000000,
                "description": "The epitome of luxury cars with an iconic design.",
            },
            "Ferrari LaFerrari": {
                "price": 2500000,
                "description": "A hybrid supercar with immense power and speed.",
            },
            "McLaren P1": {
                "price": 2000000,
                "description": "A hypercar designed for unmatched performance and beauty.",
            },
            "Aston Martin DB11": {
                "price": 1500000,
                "description": "A stunning British sports car with elegant design.",
            },
            "Porsche 918 Spyder": {
                "price": 2000000,
                "description": "A high-performance hybrid sports car, both fast and fuel-efficient.",
            },
            "Bentley Continental GT": {
                "price": 300000,
                "description": "A luxury grand tourer, blending power and refinement.",
            },
        },
        "👗 **Clothes**": {
            "Versace Suit": {
                "price": 15000,
                "description": "A custom-made Versace suit for the most elegant occasions.",
            },
            "Chanel Evening Gown": {
                "price": 50000,
                "description": "A breathtaking gown from Chanel's latest collection.",
            },
            "Rolex Submariner": {
                "price": 25000,
                "description": "A premium Rolex Submariner watch, perfect for any elite individual.",
            },
            "Louis Vuitton Bag": {
                "price": 20000,
                "description": "An exclusive Louis Vuitton bag, perfect for any occasion.",
            },
            "Gucci Leather Jacket": {
                "price": 12000,
                "description": "A high-quality leather jacket from Gucci, perfect for cool evenings.",
            },
            "Hermès Scarf": {
                "price": 8000,
                "description": "A luxurious silk scarf from Hermès, designed for elegance.",
            },
            "Prada High Heels": {
                "price": 25000,
                "description": "Stylish high heels by Prada, a statement piece for any outfit.",
            },
            "Christian Louboutin Sneakers": {
                "price": 30000,
                "description": "Exclusive sneakers by Christian Louboutin with iconic red soles.",
            },
            "Dior Suit": {
                "price": 50000,
                "description": "An exquisite, tailor-made Dior suit for any high-class event.",
            },
        },
        "💎 **Luxury Items**": {
            "Gold-Plated Private Jet": {
                "price": 5000000,
                "description": "Fly in ultimate style with your own gold-plated private jet.",
            },
            "Diamond-Encrusted Necklace": {
                "price": 1000000,
                "description": "A necklace studded with flawless diamonds.",
            },
            "Superyacht": {
                "price": 15000000,
                "description": "A private superyacht for you and your guests, offering unmatched luxury.",
            },
            "Space Travel Ticket": {
                "price": 50000000,
                "description": "A ticket to space, for the ultimate adventurous experience.",
            },
            "Mona Lisa Painting": {
                "price": 8000000,
                "description": "Own the world's most famous painting, a symbol of elegance and history.",
            },
            "Gold Bullion Bar": {
                "price": 2000000,
                "description": "A solid gold bar for investment or as a symbol of wealth.",
            },
            "Private Submarine": {
                "price": 10000000,
                "description": "A state-of-the-art submarine for exploring the depths of the ocean.",
            },
            "Antique Ferrari 250 GTO": {
                "price": 35000000,
                "description": "An ultra-rare, collectible car that’s a piece of automotive history.",
            },
            "Million-Dollar Watch Collection": {
                "price": 1000000,
                "description": "A collection of world-renowned luxury watches, the ultimate status symbol.",
            },
        },
        "✈️ **Travel Experiences**": {
            "Luxury Safari in Africa": {
                "price": 500000,
                "description": "A first-class safari experience in Africa, with private guides and lodges.",
            },
            "Private Island Resort": {
                "price": 2000000,
                "description": "A luxurious resort experience on a secluded private island.",
            },
            "Antarctica Expedition": {
                "price": 1000000,
                "description": "An exclusive expedition to Antarctica with first-class accommodations.",
            },
            "World Tour by Private Jet": {
                "price": 15000000,
                "description": "A lavish round-the-world tour with your own private jet.",
            },
            "Champagne Tasting in France": {
                "price": 10000,
                "description": "A private champagne tasting tour in the heart of France.",
            },
        },
    }

    if category:
        category = category.lower().strip()

        category_found = False
        for cat_name, items in categories.items():
            if category in cat_name.lower():
                category_found = True
                embed_category = discord.Embed(
                    title=f"🛒 **{cat_name}** 🛍️",
                    description=f"Here are the items available in the **{cat_name}** category.",
                    color=discord.Color.purple(),
                )
                for item_name, item_info in items.items():
                    embed_category.add_field(
                        name=f"**{item_name}**",
                        value=f"Price: {item_info['price']} $P\n*{item_info['description']}*",
                        inline=False,
                    )
                embed_category.add_field(
                    name="Your Balance", value=f"{user_balance} $P", inline=False
                )
                embed_category.set_footer(
                    text="Use `$buy <item_name>` to purchase an item!"
                )
                await ctx.send(embed=embed_category)
                break

        if not category_found:
            await ctx.send(
                f"{ctx.author.mention}, the category **{category}** could not be found. Please check the spelling or try a different category."
            )
        return

    embed_shop = discord.Embed(
        title="🛒 **Welcome to the Luxury Shop!** 🛍️",
        description="Here are the ultra-expensive items you can buy with your $P. Choose wisely! 💸",
        color=discord.Color.purple(),
    )

    for category_name in categories:
        embed_shop.add_field(
            name=category_name,
            value=f"Use `$shop {category_name.split(' ')[1].lower()}` to view items in this category.",
            inline=False,
        )

    embed_shop.add_field(name="Your Balance", value=f"{user_balance} $P", inline=False)

    embed_shop.set_footer(
        text="Use `$shop <category_name>` to view items in a category."
    )

    await ctx.send(embed=embed_shop)

# buy command
# -----------------------------------------------------------------
# This command allows users to purchase items from the shop using their in-game currency ($P).
# It checks if the item exists, verifies the user's balance, and updates their inventory and balance accordingly.
# Usage: $buy <item_name>

@bot.command(name="buy")
async def buy_item(ctx, *, item_name: str):
    user_id = str(ctx.author.id)
    file_path = "gambling.json"

    categories = {
        "🏠 **Houses**": {
            "Luxury Studio": 50000,
            "Penthouse in New York": 200000,
            "Beachfront Mansion": 500000,
            "Private Island Villa": 2000000,
            "Mountain Retreat": 750000,
            "Parisian Loft": 350000,
            "Dubai Skyscraper Penthouse": 5000000,
            "Japanese Zen House": 1000000,
        },
        "🚗 **Cars**": {
            "Tesla Model S": 100000,
            "Lamborghini Aventador": 500000,
            "Bugatti Chiron": 2500000,
            "Rolls-Royce Phantom": 1000000,
            "Ferrari LaFerrari": 2500000,
            "McLaren P1": 2000000,
            "Aston Martin DB11": 1500000,
            "Porsche 918 Spyder": 2000000,
            "Bentley Continental GT": 300000,
        },
        "👗 **Clothes**": {
            "Versace Suit": 15000,
            "Chanel Evening Gown": 50000,
            "Rolex Submariner": 25000,
            "Louis Vuitton Bag": 20000,
            "Gucci Leather Jacket": 12000,
            "Hermès Scarf": 8000,
            "Prada High Heels": 25000,
            "Christian Louboutin Sneakers": 30000,
            "Dior Suit": 50000,
        },
        "💎 **Luxury Items**": {
            "Gold-Plated Private Jet": 5000000,
            "Diamond-Encrusted Necklace": 1000000,
            "Superyacht": 15000000,
            "Space Travel Ticket": 50000000,
            "Mona Lisa Painting": 8000000,
            "Gold Bullion Bar": 2000000,
            "Private Submarine": 10000000,
            "Antique Ferrari 250 GTO": 35000000,
            "Million-Dollar Watch Collection": 1000000,
        },
        "✈️ **Travel Experiences**": {
            "Luxury Safari in Africa": 500000,
            "Private Island Resort": 2000000,
            "Antarctica Expedition": 1000000,
            "World Tour by Private Jet": 15000000,
            "Champagne Tasting in France": 10000,
        },
    }

    with open(file_path, "r") as file:
        data = json.load(file)

    if user_id not in data:
        data[user_id] = {"balance": 1000, "inventory": {}}
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    if "inventory" not in data[user_id]:
        data[user_id]["inventory"] = {}

    item_found = False
    for category, items in categories.items():
        for available_item in items:
            if (
                item_name.lower() in available_item.lower()
            ):  
                item_found = True
                price = items[available_item]

                if data[user_id]["balance"] >= price:
                    data[user_id]["balance"] -= price
                    if available_item in data[user_id]["inventory"]:
                        data[user_id]["inventory"][available_item] += 1
                    else:
                        data[user_id]["inventory"][available_item] = 1

                    with open(file_path, "w") as file:
                        json.dump(data, file, indent=4)

                    await ctx.send(
                        f"🎉 You've successfully bought **{available_item}** for {price} $P!"
                    )
                else:
                    await ctx.send(
                        f"❌ You don't have enough balance to buy **{available_item}**."
                    )
                break  

        if item_found:
            break  

    if not item_found:
        await ctx.send(f"❌ No item matching **{item_name}** found in the store.")


# -----------------------------------------------------------------

# GAMBLING / GAMES
# -------------------
# This command allows users to play various gambling games to win or lose in-game currency ($P).
# It supports multiple games including jackpot, double, safe, risky, roulette, and russianroulette


@bot.command(name="gambling", aliases=["gam"])
async def gambling(ctx, game_name: str = None, *args):
    user = str(ctx.author.id)
    file_path = "gambling.json"

    if not game_name:
        embed_help = discord.Embed(
            title="🎰 **PandOS Gambling** 🎲",
            description=(
                "Welcome to the **PandOS Gambling System**! 🎉 Ready to try your luck?\n\n"
                "Use the command to play any of the following games:\n"
                "`$gambling <game_name> [args]`\n\n"
                "**🎮 Available Games:**\n"
                "1. **`jackpot`** - 🎯 10% chance to win **6x** your bet\n"
                "2. **`double`** - 🔄 45% chance to **double** your bet\n"
                "3. **`safe`** - ✅ 65% chance to win **1.3x** your bet\n"
                "4. **`risky`** - ⚠️ 25% chance to win **3.5x** your bet\n"
                "5. **`roulette`** - 🎡 Play roulette by choosing a **color** (red, black, green, white) and bet an amount\n"
                "6. **`russianroulette`** - 💣 50% chance to win or lose everything!\n\n"
                "**💡 Example Commands:**\n"
                "- `$gambling double 100`\n"
                "- `$gambling roulette red 200`\n"
                "- `$gambling russianroulette`\n\n"
                "**🔄 Your balance will be updated automatically after each game!**"
            ),
            color=discord.Color.blurple(), 
        )
        embed_help.set_footer(
            text="PandOS Gambling System 💰 | Luck is just a spin away!"
        )
        await ctx.send(embed=embed_help)
        return

    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            json.dump({}, file)
    with open(file_path, "r") as file:
        data = json.load(file)

    if user not in data:
        data[user] = {"balance": 1000}
    user_data = data[user]
    balance = user_data["balance"]

    if game_name.lower() == "russianroulette":
        if balance <= 0:
            await ctx.send(
                f"{ctx.author.mention}, you don't have any $P to play Russian Roulette!"
            )
            return

        bet_amount = balance

        embed_start = discord.Embed(
            title="🎮 Russian Roulette 🎲",
            description=f"💀 **You've bet all your $P!** 💀\n\nGet ready... The chamber is loaded!\n\nYour bet: {bet_amount} $P\n\nA 50/50 chance... Will you survive?",
            color=discord.Color.dark_red(),
        )
        embed_start.set_footer(text="Will you live... or will you lose everything? 😱")
        embed_start.set_thumbnail(
            url="https://example.com/roulette-icon.png"
        )  
        message = await ctx.send(embed=embed_start)

        for i in range(3, 0, -1):
            embed_start.description = f"💀 **Bet:** {bet_amount} $P\nStarting in: {i} seconds...\n\nThe tension is rising..."
            await message.edit(embed=embed_start)
            await asyncio.sleep(1)

        outcome = random.choice([True, False]) 

        if outcome: 
            winnings = bet_amount * 2
            data[user]["balance"] += winnings - bet_amount 
            embed_result = discord.Embed(
                title="🎉 You Survived Russian Roulette! 🎉",
                description=(
                    f"**You won your life back!** 💥\nYour bet: {bet_amount} $P\nYour winnings: {winnings} $P\n"
                    f"**New Balance:** {data[user]['balance']} $P"
                ),
                color=discord.Color.green(),
            )
            embed_result.set_footer(text="You’ve made it out alive... For now...")
            embed_result.set_thumbnail(url="https://example.com/winning-icon.png")
        else:  
            data[user]["balance"] = 0 
            embed_result = discord.Embed(
                title="💀 You Lost Russian Roulette 💀",
                description=(
                    f"**You lost everything!** ⚰️\nYour bet: {bet_amount} $P\n"
                    f"**New Balance:** {data[user]['balance']} $P\n"
                    f"\n**Game Over.** Your fate was sealed."
                ),
                color=discord.Color.red(),
            )
            embed_result.set_footer(text="The chamber was not kind... 💔")
            embed_result.set_thumbnail(url="https://example.com/lose-icon.png")

        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        await ctx.send(embed=embed_result)
        return

    # Handle roulette

    if game_name.lower() == "roulette":
        if len(args) < 2:
            await ctx.send(
                f"{ctx.author.mention}, usage: `$gambling roulette <color> <amount>`."
            )
            return

        color, amount = args[0].lower(), int(args[1])
        if amount <= 0:
            await ctx.send(f"{ctx.author.mention}, you need to bet a positive amount!")
            return

        if balance < amount:
            await ctx.send(
                f"{ctx.author.mention}, you don't have enough $P! Your balance is {balance} $P."
            )
            return

        colors = {
            "red": (40, 2),  # 40% chance, 2x multiplier
            "black": (40, 2),  # 40% chance, 2x multiplier
            "green": (10, 10),  # 10% chance, 10x multiplier
            "white": (10, 5),  # 10% chance, 5x multiplier
        }

        if color not in colors:
            valid_colors = ", ".join(colors.keys())
            await ctx.send(f"{ctx.author.mention}, valid colors are: {valid_colors}.")
            return

        embed_start = discord.Embed(
            title=f"🎮 Starting the game 'Roulette'!",
            description=f"💰 **Bet:** {amount} $P\nColor: {color.capitalize()}\n\nGet ready for the spin...",
            color=discord.Color.orange(),
        )
        embed_start.set_footer(text="The wheel is turning... Will you be lucky?")
        message = await ctx.send(embed=embed_start)

        color_emojis = {"red": "🔴", "black": "⚫", "green": "🟢", "white": "⚪"}

        for i in range(3, 0, -1):
            embed_start.description = f"💰 **Bet:** {amount} $P\nColor: {color.capitalize()}\n\nStarting in: {i} seconds...\nGet ready for the spin!"
            await message.edit(embed=embed_start)
            await asyncio.sleep(1)

        spin_duration = 3 
        spin_colors = list(color_emojis.values())
        for _ in range(spin_duration * 2): 
            current_color = random.choice(spin_colors)
            embed_start.title = (
                f"🎮 Spinning... {current_color} {current_color} {current_color}"
            )
            await message.edit(embed=embed_start)
            await asyncio.sleep(0.3)

        outcome_color = random.choice(
            list(colors.keys())
        ) 
        chance, multiplier = colors[outcome_color]
        win = outcome_color == color

        final_emoji = color_emojis[outcome_color]
        embed_start.title = (
            f"🎮 The Spin Is Over... {final_emoji} {final_emoji} {final_emoji}"
        )

        if win:
            winnings = amount * multiplier
            data[user]["balance"] += winnings - amount
            embed_result = discord.Embed(
                title=f"🎉 You Won! {final_emoji}",
                description=(
                    f"**Color:** {color.capitalize()}\n"
                    f"**Bet:** {amount} $P\n"
                    f"**Winnings:** {winnings} $P\n"
                    f"**New Balance:** {data[user]['balance']} $P\n"
                    f"\nYou've beaten the odds! 🎉"
                ),
                color=discord.Color.green(),
            )
            embed_result.set_footer(text="Luck is on your side!")
        else:
            data[user]["balance"] -= amount
            embed_result = discord.Embed(
                title=f"💀 You Lost! {final_emoji}",
                description=(
                    f"**Color:** {color.capitalize()}\n"
                    f"**Bet:** {amount} $P\n"
                    f"**Outcome:** Lost\n"
                    f"**New Balance:** {data[user]['balance']} $P\n"
                    f"\nThe wheel was not in your favor this time. Better luck next time..."
                ),
                color=discord.Color.red(),
            )
            embed_result.set_footer(text="The wheel doesn't lie... ⚡")

        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        await ctx.send(embed=embed_result)
        return

    if game_name.lower() not in ["jackpot", "double", "safe", "risky"]:
        available_games = "jackpot, double, safe, risky, roulette"
        await ctx.send(
            f"{ctx.author.mention}, the available games are: {available_games}."
        )
        return

    if len(args) < 1 or int(args[0]) <= 0:
        await ctx.send(f"{ctx.author.mention}, you need to bet a positive amount!")
        return

    amount = int(args[0])

    if balance < amount:
        await ctx.send(
            f"{ctx.author.mention}, you don't have enough $P! Your balance is {balance} $P."
        )
        return

    games = {
        "jackpot": {"win_chance": 10, "multiplier": 6},  
        "double": {"win_chance": 45, "multiplier": 2},  
        "safe": {
            "win_chance": 65,
            "multiplier": 1.3,
        }, 
        "risky": {
            "win_chance": 25,
            "multiplier": 3.5,
        }, 
    }

    game = games[game_name.lower()]
    outcome = random.randint(1, 100)

    embed_start = discord.Embed(
        title=f"🎮 Game '{game_name.capitalize()}' in Progress!",
        description=f"💰 **Bet:** {amount} $P\n🔄 Get ready... the wheel is spinning...",
        color=discord.Color.orange(),
    )
    embed_start.set_footer(text="Hold on tight! ⏳")
    message = await ctx.send(embed=embed_start)

    for i in range(3, 0, -1):
        embed_start.description = f"💰 **Bet:** {amount} $P\n🔄 Starting in: {i} seconds...\nGet ready for the spin!"
        await message.edit(embed=embed_start)
        await asyncio.sleep(1)

    await asyncio.sleep(1)

    if outcome <= game["win_chance"]: 
        winnings = int(amount * game["multiplier"])
        data[user]["balance"] += winnings - amount
        result_embed = discord.Embed(
            title="🎉 You Won! 🎉",
            description=(
                f"✨ **Congratulations!** You won **{winnings} $P** in the game '{game_name.capitalize()}'.\n"
                f"🔝 Your new balance is: **{data[user]['balance']} $P**\n"
                f"Keep the luck rolling! 🍀"
            ),
            color=discord.Color.green(),
        )
        result_embed.set_footer(text="Great things are coming! 🚀")

    else:  
        data[user]["balance"] -= amount
        result_embed = discord.Embed(
            title="💀 You Lost... 💔",
            description=(
                f"😞 **Ouch!** You lost **{amount} $P** in the game '{game_name.capitalize()}'.\n"
                f"💳 Your new balance is: **{data[user]['balance']} $P**\n"
                f"Don't worry, better luck next time! 🌟"
            ),
            color=discord.Color.red(),
        )
        result_embed.set_footer(text="Don't give up, try again soon! 💪")

    await message.edit(embed=result_embed)

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


#################################################################################

# Keeping track of user XP and levels

user_data = defaultdict(
    lambda: {"xp": 0, "level": 1, "last_message_time": 0, "voice_start_time": 0}
)


# Function to calculate XP needed for next level

def xp_to_next_level(level):
    return 100 + (level - 1) * 50


# Path to the JSON data file

DATA_FILE = "user_data.json"

# Initial load of user data

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as file:
        user_data = json.load(file)


# Fuction to save user data to JSON file

def save_user_data():
    with open(DATA_FILE, "w") as file:
        json.dump(user_data, file, indent=4)


# Function to get user data or initialize if not present

def get_user_data(user_id):
    if str(user_id) not in user_data:
        user_data[str(user_id)] = {
            "xp": 0,
            "level": 1,
            "last_message_time": 0,
            "voice_start_time": 0,
        }
    return user_data[str(user_id)]


# Function to check and handle level up

def check_level_up(user):
    leveled_up = False
    while user["xp"] >= xp_to_next_level(user["level"]):
        user["xp"] -= xp_to_next_level(user["level"])
        user["level"] += 1
        leveled_up = True
        print(f"Użytkownik awansował na poziom {user['level']}!")
    return leveled_up


# Cyclic save task

@tasks.loop(minutes=5)
async def periodic_save():
    save_user_data()


# Giving XP for voice chat activity

@tasks.loop(seconds=60) 
async def grant_voice_xp():
    for guild in bot.guilds:
        for voice_channel in guild.voice_channels:
            for member in voice_channel.members:
                if not member.bot:
                    user_id = str(member.id) 
                    user = get_user_data(user_id) 

                    print(
                        f"User ID: {user_id}, XP: {user['xp']}, Level: {user['level']}"
                    )

                    leveled_up = add_xp(user_id, 5) 

                    if leveled_up:  
                        check_level_up(user)
                        try:
                            embed = discord.Embed(
                                title="🎉 Congratulations!",
                                description=f"**{member.display_name}**, you've reached level **{user['level']}**! 🏆",
                                color=discord.Color.green(),
                            )
                            embed.set_thumbnail(
                                url=member.avatar.url
                            )  
                            embed.set_image(
                                url="https://example.com/path_to_background_image.png"
                            )  
                            embed.add_field(
                                name="Your Stats",
                                value=f"**XP**: {user['xp']}\n**Level**: {user['level']}",
                                inline=False,
                            )
                            embed.add_field(
                                name="Keep it up!",
                                value="Keep grinding and level up even more! 🚀",
                                inline=False,
                            )
                            embed.set_footer(
                                text="Congrats again! Thanks for being part of the community!",
                                icon_url="https://example.com/path_to_footer_icon.png",
                            )  

                            await member.send(embed=embed)
                            print(f"Sent level-up embed to {member.display_name}")
                        except discord.errors.Forbidden:
                            print(
                                f"Could not send message to {member.display_name} (DMs are closed)"
                            )
                        except Exception as e:
                            print(f"An error occurred: {e}")


# Function to add XP and check for level up

def add_xp(user_id, xp_amount):
    user = get_user_data(user_id)
    user["xp"] += xp_amount 
    leveled_up = check_level_up(user) 
    save_user_data() 
    return leveled_up 


@bot.event
async def on_voice_state_update(member, before, after):
    user_id = str(member.id)
    current_time = time.time()

    if after.channel is not None and before.channel is None:
        user_data[user_id]["voice_start_time"] = current_time

    elif before.channel is not None and after.channel is None:
        time_spent = current_time - user_data[user_id].get(
            "voice_start_time", current_time
        )
        xp_gained = int(time_spent / 60) * 5 
        leveled_up = add_xp(user_id, xp_gained) 
        if leveled_up:
            print(
                f"Gratulacje! {member.display_name} osiągnął poziom {user_data[user_id]['level']}!"
            )


# initial load of user data with error handling

if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, "r") as file:
            content = file.read().strip()
            if not content: 
                raise json.JSONDecodeError("Plik jest pusty.", content, 0)
            user_data = json.loads(content)
    except json.JSONDecodeError:
        print(
            "Plik user_data.json jest pusty lub uszkodzony. Tworzenie nowego pliku..."
        )
        user_data = defaultdict(
            lambda: {"xp": 0, "level": 1, "last_message_time": 0, "voice_start_time": 0}
        )
        save_user_data()
else:
    user_data = defaultdict(
        lambda: {"xp": 0, "level": 1, "last_message_time": 0, "voice_start_time": 0}
    )
    save_user_data()

#################################################################################

# Configuration for logging

logging.basicConfig(level=logging.DEBUG)

#################################################################################

# Warnings Defs

# Path to warnings file
WARNINGS_FILE = "warnings.json"

# Function to load warnings data

def load_warnings():
    if not os.path.exists(WARNINGS_FILE):
        with open(WARNINGS_FILE, "w") as f:
            json.dump({}, f)
        return {}

    try:
        with open(WARNINGS_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Error: The warnings file is corrupted. Reinitializing...")
        with open(WARNINGS_FILE, "w") as f:
            json.dump({}, f)
        return {}


# Function to save warnings data

def save_warnings(warnings_data):
    with open(WARNINGS_FILE, "w") as f:
        json.dump(warnings_data, f, indent=4)


# Function to add a warning

def add_warning(user_id, reason):
    warnings_data = load_warnings()

    if str(user_id) in warnings_data:
        warnings_data[str(user_id)]["count"] += 1
        warnings_data[str(user_id)]["reasons"].append(reason)
    else:
        warnings_data[str(user_id)] = {"count": 1, "reasons": [reason]}

    save_warnings(warnings_data)
    return warnings_data[str(user_id)]["count"]


# Function to get the number of warnings

def get_warnings(user_id):
    warnings_data = load_warnings()
    return warnings_data.get(str(user_id), {"count": 0, "reasons": []})["count"]


# Function to reset warnings

def reset_warnings(user_id):
    warnings_data = load_warnings()
    if str(user_id) in warnings_data:
        del warnings_data[str(user_id)]
        save_warnings(warnings_data)


#################################################################################

# TEAMS FUNCTIONS

# Configuratiion for logging

logging.basicConfig(
    filename="bot_activity.log", 
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s", 
)

# function to load team points from a file

def load_team_points():
    if os.path.exists("BSOG_Team.py"):
        team_data = importlib.import_module("BSOG_Team")
        logging.info("Successfully loaded team points from BSOG_Team.py")
        return team_data.team_points
    else:
        logging.warning("BSOG_Team.py not found. Initializing with default points.")
        return {
            "❤️ Team Red": 0,
            "💙 Team Blue": 0,
            "💚 Team Green": 0,
            "💛 Team Yellow": 0,
            "💜 Team Purple": 0,
            "🧡 Team Orange": 0,
            "💖 Team Pink": 0,
            "💠 Team Cyan": 0,
            "⚫ Team Black": 0,
            "⚪ Team White": 0,
        }


# Function to save the team points to a file

def save_team_points(team_points):
    try:
        with open("BSOG_Team.py", "w") as file:
            file.write("team_points = {\n")
            for team, points in team_points.items():
                file.write(f'    "{team}": {points},\n')
            file.write("}\n")
        logging.info("Successfully saved team points to BSOG_Team.py")
    except Exception as e:
        logging.error(f"Error saving team points to file: {e}")


# initialize team points

team_points = load_team_points()


@bot.command()
async def teamrank(ctx):
    if hasattr(ctx, "teamrank_sent"):
        return  

    ctx.teamrank_sent = True

    try:
        embed = discord.Embed(
            title="🏆 **Team Ranking** 🏆", 
            description="Points earned by teams:\n\n",
            color=discord.Color.blue(),  
        )

        embed.set_thumbnail(url=ctx.guild.icon.url)  
        embed.set_author(
            name="PandOS Bot", icon_url=ctx.bot.user.avatar.url
        )  
        embed.set_footer(
            text="Good luck to all teams!", icon_url=ctx.bot.user.avatar.url
        )

        for idx, (team, points) in enumerate(
            sorted(team_points.items(), key=lambda x: x[1], reverse=True)
        ):
            rank_emoji = ""
            if idx == 0:
                rank_emoji = "🥇"
            elif idx == 1:
                rank_emoji = "🥈"
            elif idx == 2:
                rank_emoji = "🥉"

            embed.add_field(
                name=f"{rank_emoji} {team}", value=f"{points} points", inline=False
            )

        await ctx.send(embed=embed)
    finally:
        del ctx.teamrank_sent


@bot.command()
@commands.has_permissions(administrator=True)
async def teamreset(ctx):
    global team_points
    team_points = {  
        "Team Red": 0,
        "Team Blue": 0,
        "Team Green": 0,
        "Team Yellow": 0,
        "Team Purple": 0,
        "Team Orange": 0,
        "Team Pink": 0,
        "Team Cyan": 0,
        "Team Black": 0,
        "Team White": 0,
    }

    save_team_points(team_points)

    await ctx.send(f"### 🏆 The team points have been reset! by {ctx.author} 🏆")


@teamreset.error
async def teamreset_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need administrator permissions to use this command.")


#################################################################################


# Function to send a message to a user

async def send_message_to_user(user_id: int, message: str):
    try:
        user = await bot.fetch_user(user_id)

        await user.send(message)
        print(f"Wiadomość wysłana do {user.name}")
    except discord.DiscordException as e:
        print(f"Nie udało się wysłać wiadomości: {e}")


#################################################################################


# Function to send log embed

async def send_log_embed(channel, title, description):
    embed = discord.Embed(
        title=title, description=description, color=discord.Color.blue()
    )
    await channel.send(embed=embed)


#################################################################################


# Function to send private message embed

async def send_private_embed(user, title, description):
    embed = discord.Embed(
        title=title, description=description, color=discord.Color.green()
    )
    await user.send(embed=embed)


#################################################################################


async def send_welcome_message_to_user(member):
    embed = discord.Embed(
        title="🎉 Welcome to Better Side Of Gaming! 🎮",
        description=(
            f"Hi {member.mention}, welcome to **Better Side Of Gaming**! 🕹️\n"
            "We're thrilled to have you here! Here's what you need to know:"
        ),
        color=discord.Color.green(),
    )

    embed.add_field(
        name="📜 Rules",
        value=(
            f"Make sure to read our rules: {bot.get_channel(1295000524654903337).mention}.\n"
            f"Full rules are also available [here](https://vezyyy.github.io/BetterSideOfGaming/rules.html)."
        ),
        inline=False,
    )

    embed.add_field(
        name="🎮 Roles & Channels",
        value=(
            "Personalize your experience! Head over to the Roles & Channels section "
            "to choose roles and unlock special areas tailored to your interests."
        ),
        inline=False,
    )

    embed.add_field(
        name="📢 Updates",
        value=(
            f"Stay informed about the latest news and announcements: "
            f"{bot.get_channel(1295000546033401876).mention}."
        ),
        inline=False,
    )

    embed.add_field(
        name="🌐 Visit Our Website",
        value="[Better Side Of Gaming](https://vezyyy.github.io/BetterSideOfGaming/).",
        inline=False,
    )

    embed.set_thumbnail(url=member.avatar.url if member.avatar else bot.user.avatar.url)
    embed.set_footer(text="Better Side Of Gaming | Where Fun Meets Professionalism")

    await member.send(embed=embed)

    verification_embed = discord.Embed(
        title="🔒 Verification Required",
        description=(
            "A private verification channel has been created **just for you** on the server!\n\n"
            "🔹 To gain full access to the server, you need to verify your account.\n"
            "🔹 Please go to the channel and follow the steps provided there.\n\n"
            "Not sure how to verify? Click [here](https://vezyyy.github.io/BetterSideOfGaming/invite.html) and scroll to the bottom for help!"
        ),
        color=discord.Color.blue(),
    )

    verification_embed.set_footer(
        text="Better Side Of Gaming | Verification ensures a safe community."
    )

    try:
        await member.send(embed=verification_embed)
    except discord.Forbidden:
        pass 


#################################################################################

# function to detect greetings in different languages

def detect_greeting(message):
    logging.debug(f"Detecting greeting in message: {message.content}")
    user_message = (
        message.content.lower().strip()
    ) 

    for lang, words in greetings.items():
        for word in words:
            if re.search(
                rf"\b{re.escape(word)}\b", user_message
            ): 
                logging.debug(f"Greeting detected: {lang} with word: {word}")
                return lang
    logging.debug("No greeting detected.")
    return None


#################################################################################

# Function to get a random greeting response based on language

def get_greeting_response(lang):
    greetings_responses = {
        "en": ["Hello!", "Hi there!", "Hey, how's it going?", "Greetings!"],
        "pl": ["Cześć!", "Hejka!", "Witaj!", "Siema!", "Jak się masz?"],
        "de": ["Hallo!", "Servus!", "Guten Tag!", "Wie geht's?"],
        "es": ["¡Hola!", "¡Qué tal!", "¡Buenos días!", "¡Buenas tardes!"],
    }
    return random.choice(greetings_responses.get(lang, ["Hello!"]))


#################################################################################

# Function to detect conversation keywords and respond

def get_conversation_response(message, lang):
    logging.debug(f"Processing message: {message.content} in language: {lang}")
    user_message = message.content.lower().strip()

    for keyword, responses in conversations.items():
        if re.search(rf"\b{re.escape(keyword)}\b", user_message):
            response_list = responses.get(lang, [])
            if response_list:
                return random.choice(response_list)
    return None


#################################################################################


@bot.event
async def on_ready():
    start_time = time.time()
    periodic_save.start()
    grant_voice_xp.start()
    # send_steam_sales.start()  # Start the Steam sales task
    update_pandocoin_rate.start()

    ping = bot.latency * 1000 

    system_message = (
        f"### [PandOS - Version: {BOT_VERSION}]\n\n"
        "** [PandOS - 05.07.2025]**\n"
        "** [PandOS - VERIFICATION 3.0 Fix]**\n"
        "** [PandOS - Creator: Vezyy | VPanda]**\n\n"
        "🖥️ **▬▬▬ PandOS System Startup ▬▬▬**\n\n"
        "🔧 **PandOS Package** has been launched.\n"
        "🎮 **BSOG Gaming Package** has been launched.\n"
        "🔐 **Security Package** has been launched.\n"
        "✅ **User Verification Package** has been launched.\n"
        "💻 **PandOS Agent Package** has been launched.\n"
        "📝 **PandOS Logs Package** has been launched.\n"
        "📊 **Monitoring System** has been launched.\n\n"
        "🧑‍💻 **▬▬▬ System Information ▬▬▬**\n"
        f"🤖 **Bot:** {bot.user} is online and ready for work.\n"
        f"📶 **Ping:** {ping:.2f} ms.\n"
        f"⏳ **Uptime:** {int(time.time() - start_time)} seconds.\n\n"
        "**__All systems are functioning properly.__** ✅\n\n"
        "🌐 **More information on the website:** [Better Side Of Gaming](https://vezyyy.github.io/BetterSideOfGaming/)"
    )

    embed = discord.Embed(
        title="PandOS System Started",
        description=system_message,
        color=discord.Color.green(),
    )

    log_channel = bot.get_channel(LOG_CHANNEL_ID)

    if log_channel:
        await log_channel.send(embed=embed)
        print("The system startup message has been sent to the channel.")
    else:
        print(f"Channel with ID {LOG_CHANNEL_ID} not found.")

    print(f"Bot {bot.user} is online and ready to work.")
    print(f"Ping: {ping:.2f} ms")
    print(f"Uptime: {int(time.time() - start_time)} seconds")
    print("System packages have been successfully launched.")

    try:
        status_channel = await bot.fetch_channel(STATUS_CHANNEL_ID)
        version_channel = await bot.fetch_channel(VERSION_CHANNEL_ID)
        date_channel = await bot.fetch_channel(DATE_CHANNEL_ID) 

        if status_channel:
            print(f"Attempting to update status channel: {status_channel.name}")
            await status_channel.edit(name=f"✅ STATUS: [{BOT_STATUS}]")
            print(f"Updated status channel name to: ✅ STATUS: [{BOT_STATUS}]")
        else:
            print(f"Status channel with ID {STATUS_CHANNEL_ID} not found.")

        if version_channel:
            print(f"Attempting to update version channel: {version_channel.name}")
            await version_channel.edit(name=f"🌐 BUILD: [{BOT_VERSION}]")
            print(f"Updated version channel name to: 🌐 BUILD: [{BOT_VERSION}]")
        else:
            print(f"Version channel with ID {VERSION_CHANNEL_ID} not found.")

        if date_channel:
            print(f"Attempting to update date channel: {date_channel.name}")
            await date_channel.edit(name=f"📅 Last Update: {current_time}")
            print(f"Updated date channel name to: 📅 Last Update: {current_time}")
        else:
            print(f"Date channel with ID {DATE_CHANNEL_ID} not found.")

    except discord.Forbidden:
        print("Error: Bot doesn't have permissions to edit channels.")
    except discord.NotFound:
        print("Error: One of the channels was not found.")
    except Exception as e:
        print(f"Error updating channel names: {e}")


#################################################################################


@bot.command(name="bug")
async def report_bug(ctx, *, reason: str):
    channel_id = 1295001133202411531
    channel = bot.get_channel(channel_id)

    embed = discord.Embed(
        title="Bug Report",
        description=f"Bug report from {ctx.author.name}#{ctx.author.discriminator}",
        color=discord.Color.red(),
    )
    embed.add_field(name="Bug Description", value=reason, inline=False)
    embed.add_field(
        name="Reported by",
        value=f"{ctx.author.name}#{ctx.author.discriminator}",
        inline=False,
    )

    await channel.send(embed=embed)

    await ctx.send("Your bug report has been submitted successfully!")


#################################################################################

############################
# FUNNY SERVER COMMANDS
############################

# BONK COMMAND
# -----------------


@bot.command()
async def bonk(ctx, user: discord.Member):
    gify = [
        "GIF LINK",
        "GIF LINK",
        "GIF LINK",
        "GIF LINK",
        "GIF LINK",
        "GIF LINK",
        "GIF LINK",
        "ADD MORE GIF's if you want ...",
    ]

    bonkujacy = ctx.author.mention
    bonkowany = user.mention
    gif = random.choice(gify)
    gif_spoiler = f"{gif}"

    await ctx.send(f"{bonkujacy} bonking you! {bonkowany}!\n{gif_spoiler}")


# SLAP COMMAND
# -----------------


@bot.command()
async def slap(ctx, user: discord.Member):
    gifs = [
        "GIF LINK",
        "GIF LINK",
        "GIF LINK",
        "GIF LINK",
        "GIF LINK",
        "ADD MORE GIF's if you want ...",
    ]
    await ctx.send(
        f"{ctx.author.mention} slapped {user.mention}! 👋\n{random.choice(gifs)}"
    )


# HUG COMMAND
# -----------------


@bot.command()
async def hug(ctx, user: discord.Member):
    gifs = [
        "GIF LINK",
        "GIF LINK",
        "GIF LINK",
        "GIF LINK",
        "GIF LINK",
        "GIF LINK",
        "ADD MORE GIF's if you want ...",
    ]
    await ctx.send(
        f"{ctx.author.mention} gives a big hug to {user.mention}! 🤗\n{random.choice(gifs)}"
    )


# KILL COMMAND
# -----------------

@bot.command()
async def kill(ctx, user: discord.Member):
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
        "GIF LINK",
        "GIF LINK",
        "GIF LINK",
        "GIF LINK",
        "GIF LINK",
        "GIF LINK",
        "GIF LINK",
        "ADD MORE GIF's if you want ...",
    ]

    embed = discord.Embed(
        title="💀 Absurd Kill Executed!",
        description=random.choice(deaths),
        color=discord.Color.red(),
    )
    embed.set_footer(text=f"{ctx.author.display_name} tried to kill them...")

    await ctx.send(embed=embed)
    await ctx.send(f"{random.choice(gifs)}")


# PROGRESS BAR
# -----------------


def get_progress_bar(percent):
    total_blocks = 10
    filled_blocks = int(percent / 10)
    empty_blocks = total_blocks - filled_blocks
    return "█" * filled_blocks + "░" * empty_blocks


# SHIP COMMAND
# -----------------


@bot.command()
async def ship(ctx, user1: discord.Member, user2: discord.Member):
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


# SIMP COMMAND
# -----------------


@bot.command()
async def simp(ctx, user: discord.Member):
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


# GOONER COMMAND
# -----------------

@bot.command()
async def gooner(ctx, user: discord.Member):
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


# FULLSCAN COMMAND
# -----------------


@bot.command()
async def fullscan(ctx, user1: discord.Member, user2: discord.Member):
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


# GOONER OF THE DAY COMMAND
# ----------------------------

COOLDOWN_FILE = "gooneroftheday.json"
CHANNEL_ID = 1295000603679916042 
gooneroftheday = ""


def load_cooldown():
    try:
        with open(COOLDOWN_FILE, "r") as f:
            return json.load(f)
    except:
        return {"last_used": 0, "last_user_id": None}


def save_cooldown(data):
    with open(COOLDOWN_FILE, "w") as f:
        json.dump(data, f)


@bot.command()
async def gooneroftheday(ctx):
    cooldown = load_cooldown()
    now = time.time()
    elapsed = now - cooldown["last_used"]

    if elapsed < 86400:
        remaining = int(86400 - elapsed)
        hours = remaining // 3600
        minutes = (remaining % 3600) // 60

        last_user_id = cooldown.get("last_user_id")
        if last_user_id:
            last_member = ctx.guild.get_member(last_user_id)
            if last_member:
                await ctx.send(
                    f"😈 Today's gooner was already chosen: **{last_member.mention}**"
                )

        await ctx.send(
            f"⏳ This command can be used again in **{hours}h {minutes}min**."
        )
        return

    members = [m for m in ctx.guild.members if not m.bot]
    if not members:
        await ctx.send("❌ No valid members found.")
        return

    selected = random.choice(members)

    cooldown["last_used"] = now
    cooldown["last_user_id"] = selected.id
    save_cooldown(cooldown)

    embed = discord.Embed(
        title="👑 Gooner of the Day",
        description=f"Today’s honorary gooner is: **{selected.mention}**\nNo hiding now... we see you. 😈",
        color=discord.Color.red(),
    )
    embed.set_footer(text="Awarded with great shame and honor.")
    embed.set_thumbnail(url=selected.display_avatar.url)

    await ctx.send(embed=embed)

    gooner_reset_check.start(ctx.guild)


@tasks.loop(seconds=60)
async def gooner_reset_check(guild):
    cooldown = load_cooldown()
    if time.time() - cooldown["last_used"] >= 86400:
        channel = guild.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(
                "🔁 The `$gooneroftheday` command is now available again!"
            )
        gooner_reset_check.stop()

#################################################################################
# PandOS Call View with Buttons
# This view allows users to respond to a call invitation with buttons.

# ---------------------
# CALL VIEW WITH BUTTONS
# ---------------------

class CallView(discord.ui.View):
    def __init__(self, author: discord.Member, channel: discord.VoiceChannel):
        super().__init__(timeout=60)
        self.author = author
        self.channel = channel

    @discord.ui.button(label="🟢 I'm joining", style=discord.ButtonStyle.green)
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = self.channel.guild.get_member(interaction.user.id)
        if member is None:
            await interaction.response.send_message("❌ Could not find your account on the server.", ephemeral=True)
            return
        try:
            if member.voice is not None:
                await member.move_to(self.channel)
                await interaction.response.send_message(
                    f"✅ You've been moved to **{self.channel.name}**!", ephemeral=True
                )
                await self.author.send(f"✅ {member.mention} has joined your voice channel!")
            else:
                await interaction.response.send_message(
                    f"🟡 You responded positively! Please join **{self.channel.name}** manually.", ephemeral=True
                )
                await self.author.send(f"🟡 {member.mention} reacted positively and may join soon.")
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to move you.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message("❌ An error occurred while trying to move you.", ephemeral=True)
            print(e)

    @discord.ui.button(label="🔴 I'm busy", style=discord.ButtonStyle.red)
    async def busy_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🔕 Noted! You are busy.", ephemeral=True)
        try:
            await self.author.send(f"🔴 {interaction.user.mention} is busy and won’t join right now.")
        except discord.Forbidden:
            pass

# ---------------------
# CALL COMMAND
# ---------------------

@bot.command()
async def call(ctx, user: discord.Member):
    if ctx.author.voice is None:
        await ctx.send("🔊 You must be in a voice channel to use this command.")
        return

    voice_channel = ctx.author.voice.channel

    embed = discord.Embed(
        title="📞 Game Invite!",
        description=f"{ctx.author.mention} is inviting {user.mention} to join the voice channel **{voice_channel.name}**!",
        color=discord.Color.green()
    )
    embed.set_thumbnail(url=ctx.author.display_avatar.url)
    embed.set_footer(text="Click one of the buttons in your DM to respond.")

    await ctx.send(embed=embed)

    view = CallView(ctx.author, voice_channel)

    try:
        await user.send("📢 You've been invited to a game! Respond below:", view=view)
    except discord.Forbidden:
        await ctx.send(f"❌ I can't send a private message to {user.mention}. Make sure their DMs are enabled.")


#################################################################################


# $ping - Check bot latency

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000) 
    await ctx.send(f"Pong! Latency: {latency}ms")


#################################################################################


@bot.command()
async def pvsend(ctx, user_id: int, *, message: str):
    if ctx.author == bot.user:
        return

    if not ctx.author.guild_permissions.administrator:
        await ctx.send("Nie masz uprawnień do używania tej komendy.")
        return

    await send_message_to_user(user_id, message)
    await ctx.send(f"Wiadomość została wysłana do użytkownika o ID {user_id}")


#################################################################################


# $uptime - shows bot uptime

@bot.command()
async def uptime(ctx):
    bot_creation_time = bot.user.created_at.replace(tzinfo=datetime.timezone.utc)

    current_time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)

    delta_uptime = current_time - bot_creation_time

    await ctx.send(f"Bot has been online for: {delta_uptime}")


#################################################################################


# $serverinfo - shows detailed info about the server

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(
        title=f"{guild.name} Server Info",
        description="Information about the server.",
        color=discord.Color.green(),
    )
    embed.add_field(name="Server Name", value=guild.name, inline=False)
    embed.add_field(name="Server ID", value=guild.id, inline=False)
    embed.add_field(name="Member Count", value=guild.member_count, inline=False)
    embed.add_field(
        name="Created At", value=guild.created_at.strftime("%b %d, %Y"), inline=False
    )
    await ctx.send(embed=embed)


#################################################################################


# $userinfo <user> - shows detailed info about a user

@bot.command()
async def userinfo(ctx, user: discord.User):
    """Wyświetla szczegółowe informacje o użytkowniku"""

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

    embed.add_field(
        name="Nickname", value=member.nick if member.nick else "None", inline=False
    )
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


#################################################################################


# $ban <user> - ban user

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.User, reason: str = "No reason provided"):
    await ctx.guild.ban(user, reason=reason)
    await ctx.send(f"{user} has been banned for: {reason}")


#################################################################################


# $kick <user> - kick user

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.User, reason: str = "No reason provided"):
    await ctx.guild.kick(user, reason=reason)
    await ctx.send(f"{user} has been kicked for: {reason}")


#################################################################################


# $mute <user> <time> <reason> - mute user for a specified time

@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(
    ctx, user: discord.Member, time: str, reason: str = "No reason provided"
):
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
    embed.set_author(
        name="PandOS Bot", icon_url=ctx.bot.user.avatar.url
    ) 

    await ctx.send(embed=embed)

    log_channel = bot.get_channel(
        1295001133202411531
    )  
    if log_channel:
        await log_channel.send(embed=embed)

    dm_embed = discord.Embed(
        title="🔕 You have been muted",
        description=f"Hello **{user.name}**, you have been muted in **{ctx.guild.name}** for **{time} minutes**.\n\n"
        f"**Reason**: {reason}\n\n"
        f"⏳ This is a temporary mute. You will be unmuted automatically after the time is up.\n\n"
        "If you believe this is a mistake or have any questions, please reach out to an administrator.",
        color=discord.Color.red(),
    )
    dm_embed.add_field(name="📝 Muted by", value=f"{ctx.author}", inline=False)
    dm_embed.set_footer(text="If you have any issues, please contact an administrator.")
    dm_embed.set_thumbnail(url=ctx.guild.icon.url)  
    dm_embed.set_author(
        name="PandOS Bot", icon_url=ctx.bot.user.avatar.url
    )  

    try:
        await user.send(embed=dm_embed)
    except discord.Forbidden:
        print(f"Unable to send DM to {user.name} as they have DMs disabled.")

    await asyncio.sleep(time * 60) 

    await user.remove_roles(mute_role)
    await ctx.send(f"{user} has been unmuted.")


#################################################################################


# Warn Command with JSON storage

@bot.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, user: discord.Member, *, reason: str = "No reason provided"):
    try:
        await ctx.message.delete()
    except discord.NotFound:
        pass  

    """Warn a user with an optional reason."""
    warnings_count = add_warning(user.id, reason)

    warn_embed = discord.Embed(
        title="⚠️ You have been warned",
        description=f"Hello **{user.name}**, you have been warned in **{ctx.guild.name}**.",
        color=discord.Color.orange(),
    )
    warn_embed.add_field(name="📝 Reason", value=reason, inline=False)
    warn_embed.add_field(name="🕒 Warned by", value=f"{ctx.author}", inline=False)
    warn_embed.add_field(
        name="⚠️ Total Warnings", value=str(warnings_count), inline=False
    )
    warn_embed.set_footer(text="This warning will be logged.")
    warn_embed.set_thumbnail(url=ctx.guild.icon.url)  
    warn_embed.set_author(
        name="PandOS Bot", icon_url=ctx.bot.user.avatar.url
    )  
    try:
        await user.send(embed=warn_embed)
    except discord.Forbidden:
        print(f"Unable to send DM to {user.name} as they have DMs disabled.")

    log_channel = bot.get_channel(
        1295001133202411531
    ) 
    if log_channel:
        log_embed = discord.Embed(
            title="⚠️ User Warned",
            description=f"**{user}** has been warned.",
            color=discord.Color.orange(),
        )
        log_embed.add_field(name="📝 Reason", value=reason, inline=False)
        log_embed.add_field(name="🕒 Warned by", value=f"{ctx.author}", inline=False)
        log_embed.add_field(
            name="⚠️ Total Warnings", value=str(warnings_count), inline=False
        )
        log_embed.set_footer(text="Warning logged automatically.")
        log_embed.set_thumbnail(url=ctx.guild.icon.url)
        log_embed.set_author(name="PandOS Bot", icon_url=ctx.bot.user.avatar.url)

        await log_channel.send(embed=log_embed)

    await ctx.send(
        f"**{user}** has been warned. Reason: {reason} (Total warnings: {warnings_count})"
    )


# Command $warnings - Check user warnings

import json


def get_warnings(user_id):
    """Pobiera ostrzeżenia użytkownika z pliku JSON."""
    with open("warnings.json", "r", encoding="utf-8") as f:
        warnings_data = json.load(f)

    return warnings_data.get(
        str(user_id), {"count": 0, "reasons": []}
    ) 


@bot.command()
async def warnings(ctx, user: discord.Member):
    """Sprawdza ostrzeżenia użytkownika i wysyła je w embedzie."""

    warnings_data = get_warnings(user.id) 

    embed = discord.Embed(
        title=f"⚠️ Warnings for {user.name}", color=discord.Color.orange()
    )
    embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)

    if warnings_data["count"] == 0:
        embed.description = "✅ This user has no warnings!"
    else:
        for index, reason in enumerate(warnings_data["reasons"], 1):
            embed.add_field(
                name=f"⚠️ Warning {index}", value=f"**Reason:** {reason}", inline=False
            )

        embed.set_footer(text=f"Total warnings: {warnings_data['count']}")

    await ctx.send(embed=embed)


# Command resetwarnings - Reset user warnings

@bot.command()
@commands.has_permissions(
    administrator=True
) 
async def resetwarnings(ctx, user: discord.Member):
    """Reset the warnings for a user."""
    reset_warnings(user.id)
    await ctx.send(f"**{user}**'s warnings have been reset.")

# Command Pwarn - Warning by the bot itself

@bot.command()
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
    warn_embed.add_field(
        name="⚠️ Total Warnings", value=str(warnings_count), inline=False
    )
    warn_embed.set_footer(text="This warning will be logged.")
    warn_embed.set_thumbnail(url=ctx.guild.icon.url)
    warn_embed.set_author(name="PandOS Bot", icon_url=ctx.bot.user.avatar.url)

    try:
        await user.send(embed=warn_embed)
    except discord.Forbidden:
        print(f"Unable to send DM to {user.name} as they have DMs disabled.")

    log_channel = bot.get_channel(1295001133202411531) 
    if log_channel:
        log_embed = discord.Embed(
            title="⚠️ User Warned",
            description=f"**{user}** has been warned.",
            color=discord.Color.orange(),
        )
        log_embed.add_field(name="📝 Reason", value=reason, inline=False)
        log_embed.add_field(name="🕒 Warned by", value="PandOS Bot", inline=False)
        log_embed.add_field(
            name="⚠️ Total Warnings", value=str(warnings_count), inline=False
        )
        log_embed.set_footer(text="Warning logged automatically.")
        log_embed.set_thumbnail(url=ctx.guild.icon.url)
        log_embed.set_author(name="PandOS Bot", icon_url=ctx.bot.user.avatar.url)

        await log_channel.send(embed=log_embed)

    await ctx.send(
        f"**{user}** has been warned by PandOS Bot. Reason: {reason} (Total warnings: {warnings_count})"
    )


#################################################################################


# $unmute <user> - Delete mute from user

@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(
    ctx, user: discord.Member
):  
    mute_role = discord.utils.get(
        ctx.guild.roles, name="Muted"
    )  

    if not mute_role:
        await ctx.send("The 'Muted' role does not exist.")
        return

    if mute_role in user.roles:
        await user.remove_roles(mute_role, reason="Unmuted by staff")
        await ctx.send(f"{user} has been unmuted.")
    else:
        await ctx.send(f"{user} is not muted.")


#################################################################################

# $addrole - Add role to user

@bot.command()
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, user: discord.Member, role: discord.Role):
    """Dodanie roli użytkownikowi"""
    if role not in user.roles: 
        await user.add_roles(role)
        await ctx.send(
            f"The {role.name} role has been successfully added to {user.mention}."
        )
    else:
        await ctx.send(f"{user.mention} already has the {role.name} role.")


#################################################################################

# $removerole - Deleted role from user

@bot.command()
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, user: discord.Member, role: discord.Role):
    """Usuwanie roli od użytkownika"""
    if role in user.roles:
        await user.remove_roles(role)
        await ctx.send(
            f"The {role.name} role has been successfully removed from {user.mention}."
        )
    else:
        await ctx.send(f"{user.mention} doesn't have the {role.name} role.")


#################################################################################

# $twm - Tested welcome message command

@bot.command(name="twm")
@commands.has_permissions(
    administrator=True
) 
async def test_welcome_message(ctx):
    await send_welcome_message_to_user(
        ctx.author
    ) 
    await ctx.send(f"Test welcome message has been sent to {ctx.author.mention}.")


#################################################################################

# Custom Help Command
# ---------------------

class UserHelpCommand(commands.DefaultHelpCommand):
    async def send_bot_help(self, ctx):
        embed1 = discord.Embed(
            title="PandOS Bot Help (Part 1)",
            description="Below are the basic commands you can use:",
            color=discord.Color.blue(),
        )
        embed1.add_field(
            name="$VerifyMe",
            value="Receive your verification code in DMs.",
            inline=False,
        )
        embed1.add_field(
            name="$start <code>",
            value="Use the code received via `$VerifyMe` to verify yourself.",
            inline=False,
        )
        embed1.add_field(
            name="$ping",
            value="Check the bot's latency.",
            inline=False,
        )
        embed1.add_field(
            name="$uptime",
            value="Shows the bot's uptime.",
            inline=False,
        )
        await ctx.send(embed=embed1)

        embed2 = discord.Embed(
            title="PandOS Bot Help (Part 2)",
            description="Here are some user-related commands:",
            color=discord.Color.blue(),
        )
        embed2.add_field(
            name="$gambuildjson",
            value="If you have some problems with gambling system, try using this command to build your gambling.json account in our system.",
            inline=False,
        )
        embed2.add_field(
            name="$lvl <user>",
            value="Check the level and XP of a user.",
            inline=False,
        )
        embed2.add_field(
            name="$toplvl",
            value="View the top 10 users based on their level and XP.",
            inline=False,
        )
        embed2.add_field(
            name="$balance",
            value="Check your current balance of PanDollars ($P).",
            inline=False,
        )
        embed2.add_field(
            name="$gambling <game> <amount>",
            value="Play a gambling game with your PanDollars ($P). Choose from games like `jackpot`, `double`, `safe`, and `risky`.",
            inline=False,
        )
        embed2.add_field(
            name="$roulette <color> <amount>",
            value="Play the roulette game and test your luck with PanDollars ($P)!",
            inline=False,
        )
        embed2.add_field(
            name="$russianroulette <amount>",
            value="Play Russian Roulette with 50% chance of winning! If you win, you'll double your bet, but if you lose, you lose everything.",
            inline=False,
        )
        embed2.add_field(
            name="$teamrank",
            value="Check the ranking of teams based on points.",
            inline=False,
        )
        embed2.add_field(
            name="$topg or $topgambling",
            value="View the top 10 richest users based on PanDollars ($P) earnings.",
            inline=False,
        )
        embed2.add_field(
            name="$topl",
            value="Shortcut to `$toplvl` to view the top 10 users based on their level and XP.",
            inline=False,
        )

        embed2.add_field(
            name="$buyprotection <time_period>",
            value="Buy protection to prevent being robbed! Choose from:\n"
            "`1h` - 1 hour protection for 10,000 $P\n"
            "`24h` - 24 hours protection for 50,000 $P\n"
            "`7d` - 7 days protection for 250,000 $P\n"
            "`30d` - 30 days protection for 1,000,000 $P",
            inline=False,
        )
        embed2.add_field(
            name="$rob <user>",
            value="Attempt to rob another user! But beware, there are consequences for failed attempts. You can only rob users who aren't currently protected.",
            inline=False,
        )

        embed2.add_field(
            name="$shop",
            value="Browse the shop and buy various items or services. You can purchase:\n"
            "`Protection` - Buy protection from robbers\n"
            "`Upgrades` - Upgrade your stats or items\n"
            "`Special Items` - Unique items with special benefits",
            inline=False,
        )

        embed2.add_field(
            name="$buy <item>",
            value="Purchase an item or service from the shop. For example:\n"
            "`$buy Protection` - Buy protection to prevent robbing\n"
            "`$buy Upgrade` - Purchase an upgrade for your stats or items",
            inline=False,
        )

        embed2.add_field(
            name="$buyrank <rank_name>",
            value="Buy a special rank from the server! For example:\n"
            "`$buyrank VIP` - Purchase the **VIP** rank to enjoy exclusive perks and privileges.",
            inline=False,
        )

        embed2.add_field(
            name="$ranks",
            value="View the available ranks that you can purchase with PandoCoin!\n"
            "`$ranks` - Display all the ranks you can buy, along with their prices and benefits.",
            inline=False,
        )

        embed2.add_field(
            name="$pcoin",
            value="Check the current exchange rate of PandoCoin!\n"
            "`$pcoin` - View the current rate for PandoCoin in comparison to other currencies.",
            inline=False,
        )

        embed2.add_field(
            name="$exchange",
            value="Exchange your currency to PandoCoin!\n"
            "`$exchange <amount>` - Convert your coins to PandoCoin.\n"
            "Example: `$exchange 100` will convert 100 of your currency to PandoCoin based on the current exchange rate.",
            inline=False,
        )

        embed2.add_field(
            name="$inv",
            value="Check your inventory and see all the items you've purchased.\n"
            "Use this command to view items like `Protection`, `Upgrades`, or `Special Items`.",
            inline=False,
        )

        await ctx.send(embed=embed2)

        embed3 = discord.Embed(
            title="PandOS Bot Help (Part 3)",
            description="Here are some user-related commands:",
            color=discord.Color.blue(),
        )
        embed3.add_field(
            name="$bonk <@user>",
            value="Use this command to bonk anyone you want! 🪄",
            inline=False,
        )
        embed3.add_field(
            name="$kill <@user>",
            value="Use this command to kill someone in the most absurd and hilarious way! 💀",
            inline=False,
        )
        embed3.add_field(
            name="$hug <@user>",
            value="Send a warm virtual hug to someone with a cute gif! 🤗",
            inline=False,
        )
        embed3.add_field(
            name="$slap <@user>",
            value="Slap someone playfully with a funny gif! 👋😆",
            inline=False,
        )
        embed3.add_field(
            name="$simp <@user>",
            value="Check how much someone is simping with a random percentage! 😳",
            inline=False,
        )
        embed3.add_field(
            name="$gooner <@user>",
            value="Check how much someone is gooner with a random percentage! 😳",
            inline=False,
        )
        embed3.add_field(
            name="$ship <@user1> <@user2>",
            value="Find out the love compatibility between two users! ❤️",
            inline=False,
        )
        embed3.add_field(
            name="$fullscan <@user1> <@user2>",
            value="Get a complete compatibility and personality scan of a user in one detailed report! 🔍",
            inline=False,
        )
        embed3.add_field(
            name="$gooneroftheday",
            value="Discover who’s the ultimate gooner of the day with a special shoutout! 👑",
            inline=False,
        )
        embed3.add_field(
            name="$call <@user>",
            value="Calls the mentioned user to join your current voice channel and sends them a private notification via PandOS Bot.",
            inline=False,
        )

        await ctx.send(embed=embed3)

# Custom Admin Help Command
# --------------------------

class AdminHelpCommand(commands.DefaultHelpCommand):
    async def send_bot_help(self, ctx):
        embed3 = discord.Embed(
            title="PandOS Bot Help (Admin Commands)",
            description="These are the administrative commands:",
            color=discord.Color.red(),
        )
        embed3.add_field(
            name="$ban <user>",
            value="Ban a user from the server.",
            inline=False,
        )
        embed3.add_field(
            name="$kick <user>",
            value="Kick a user from the server.",
            inline=False,
        )
        embed3.add_field(
            name="$mute <user> <time>",
            value="Mute a user for a specific time (in minutes).",
            inline=False,
        )
        embed3.add_field(
            name="$unmute <user>",
            value="Unmute a user.",
            inline=False,
        )
        embed3.add_field(
            name="$addrole <user> <role>",
            value="Add a role to a user.",
            inline=False,
        )
        embed3.add_field(
            name="$removerole <user> <role>",
            value="Remove a role from a user.",
            inline=False,
        )
        embed3.add_field(
            name="$serverinfo",
            value="Display server info such as member count, server creation date.",
            inline=False,
        )
        embed3.add_field(
            name="$Pwarn <user> <reason>",
            value="Warn a user with an optional reason as PandOS (Bot). (Admin only)",
            inline=False,
        )
        embed3.add_field(
            name="$warnings <user>",
            value="Check the warnings of a user.",
            inline=False,
        )
        embed3.add_field(
            name="$resetwarnings <user>",
            value="Reset the warnings of a user.",
            inline=False,
        )
        embed3.add_field(
            name="$twm",
            value="Test the welcome message.",
            inline=False,
        )
        embed3.add_field(
            name="$ping",
            value="Check the bot's latency.",
            inline=False,
        )
        embed3.add_field(
            name="$uptime",
            value="Shows the bot's uptime.",
            inline=False,
        )
        embed3.add_field(
            name="$say <message>",
            value="Send a message as the bot (Admin only).",
            inline=False,
        )
        embed3.add_field(
            name="$announcement <message>",
            value="Send an announcement to all members (Admin only).",
            inline=False,
        )

        embed3.add_field(
            name="$partnership_start (ID)",
            value="Assign the **Partnership Program** role to a user and send a welcome message to them. This action is available only for admins.\n"
            "Example: `$$partnership_start 123456789` - Assigns the partnership role to the user with ID 123456789.",
            inline=False,
        )

        embed3.add_field(
            name="$partnership_end (ID)",
            value="Remove the **Partnership Program** role from a user and send a goodbye message. This action is available only for admins.\n"
            "Example: `$$partnership_end 123456789` - Removes the partnership role from the user with ID 123456789.",
            inline=False,
        )
        embed3.add_field(
            name="$sendrateserverinfo (ID)",
            value=(
                "🌟 **Send Rate Server Info**\n"
                "Send a friendly reminder to a user, encouraging them to rate our server.\n"
                "**Usage:** Only for admins.\n"
                "🛠️ **Example:** \n"
                "`$sendrateserverinfo 123456789` - Sends a rating reminder to the user with ID **123456789**."
            ),
            inline=False,
        )

        await ctx.send(embed=embed3)

@bot.command(name="userhelp")
async def userhelp(ctx):
    """Shows help for normal users."""
    await UserHelpCommand().send_bot_help(ctx)

@bot.command(name="adminhelp")
async def adminhelp(ctx):
    """Shows help for admin commands."""
    if ctx.author.guild_permissions.administrator:
        await AdminHelpCommand().send_bot_help(ctx)
    else:
        await ctx.send(
            "You need to have administrator permissions to use this command."
        )

bot.help_command = UserHelpCommand()

#################################################################################

@bot.event
async def on_member_join(member):
    print(f"{member.name} joined the server.")

    # Add user to database / tracking (if you use this)
    add_user_on_join(str(member.id))

    # ---- SELECT CHANNELS ----
    new_user_channel = bot.get_channel(NEW_USER_CHANNEL_ID)
    if new_user_channel is None:
        new_user_channel = discord.utils.get(member.guild.text_channels, name="general")

    log_channel = bot.get_channel(LOG_CHANNEL_ID)

    # ---- SEND PUBLIC WELCOME MESSAGE ----
    if new_user_channel:
        await new_user_channel.send(
            f"👋 Welcome to the server, {member.mention}! Feel free to say hello!"
        )

        embed = discord.Embed(
            title="🎉 Welcome to Better Side Of Gaming! 🎮",
            description=(
                f"Hey {member.mention}, welcome to **Better Side Of Gaming**!\n\n"
                f"Be sure to check out our server rules 📜\n"
                f"And most importantly... **Have Fun!** 🚀\n\n"
                f"🔗 **Website:** [BetterSideOfGaming](https://vezyyy.github.io/BetterSideOfGaming/)\n"
                f"🤝 **Invite Friends:** https://discord.gg/Tr3BQPER34"
            ),
            color=discord.Color.purple(),
            timestamp=member.joined_at,
        )

        embed.set_author(
            name=f"{member.name} just joined!",
            icon_url=member.avatar.url if member.avatar else None,
        )

        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)

        embed.add_field(name="🆔 User ID", value=member.id, inline=True)
        embed.add_field(
            name="📆 Account Created",
            value=discord.utils.format_dt(member.created_at, style="F"),
            inline=True
        )

        embed.set_footer(
            text="Better Side Of Gaming • Let’s play together!",
            icon_url=member.guild.icon.url if member.guild.icon else None,
        )

        await new_user_channel.send(embed=embed)

    # ---- SEND PRIVATE WELCOME MESSAGE ----
    await send_welcome_message_to_user(member)

    # ---- LOG JOIN IN LOG CHANNEL ----
    if log_channel:
        await send_log_embed(
            log_channel,
            "Member Joined",
            f"{member.name} has joined the server. (ID: {member.id})"
        )

    # ---- CREATE VERIFICATION CHANNEL IF NEEDED ----
    if VERIFY_ROLE_ID not in [role.id for role in member.roles]:
        await create_verification_channel(member)


#################################################################################

# ------------------------
# WELCOME MESSAGE FUNCTION
# ------------------------

async def send_welcome_message_to_user(member):
    embed = discord.Embed(
        title="🎉 Welcome to Better Side Of Gaming! 🎮",
        description=(
            f"Hi {member.mention}, welcome to **Better Side Of Gaming**! 🕹️\n"
            "We're thrilled to have you here! Here's what you need to know:"
        ),
        color=discord.Color.green(),
    )

    embed.add_field(
        name="📜 Rules",
        value=(
            f"Make sure to read our rules: {bot.get_channel(1295000524654903337).mention}.\n"
            f"Full rules are also available [here](https://vezyyy.github.io/BetterSideOfGaming/rules.html)."
        ),
        inline=False,
    )

    embed.add_field(
        name="🎮 Roles & Channels",
        value=(
            "Personalize your experience! Head over to the Roles & Channels section "
            "to choose roles and unlock special areas tailored to your interests."
        ),
        inline=False,
    )

    embed.add_field(
        name="📢 Updates",
        value=(
            f"Stay informed about the latest news and announcements: "
            f"{bot.get_channel(1295000546033401876).mention}."
        ),
        inline=False,
    )

    embed.add_field(
        name="🌐 Visit Our Website",
        value="[Better Side Of Gaming](https://vezyyy.github.io/BetterSideOfGaming/).",
        inline=False,
    )

    embed.set_thumbnail(url=member.avatar.url if member.avatar else bot.user.avatar.url)
    embed.set_footer(text="Better Side Of Gaming | Where Fun Meets Professionalism")

    await member.send(embed=embed)

    verification_embed = discord.Embed(
        title="🔒 Verification Required",
        description=(
            "A private verification channel has been created **just for you** on the server!\n\n"
            "🔹 To gain full access to the server, you need to verify your account.\n"
            "🔹 Please go to the channel and follow the steps provided there.\n\n"
            "Not sure how to verify? Click [here](https://vezyyy.github.io/BetterSideOfGaming/invite.html) and scroll to the bottom for help!"
        ),
        color=discord.Color.blue(),
    )

    verification_embed.set_footer(
        text="Better Side Of Gaming | Verification ensures a safe community."
    )

    try:
        await member.send(embed=verification_embed)
    except discord.Forbidden:
        pass


#################################################################################

# LVL COMMANDS & SYSTEM
#-----------------------------------------------------------------------------

@bot.command(name="lvl")
async def check_level(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    user = get_user_data(str(member.id)) 

    level_color = discord.Color.blue()

    embed = discord.Embed(
        title=f"🎮 **{member.display_name}'s Level** 💫",
        color=level_color, 
    )

    embed.add_field(name="**Level** 🌟", value=f"{user['level']}", inline=True)
    embed.add_field(
        name="**XP** ✨",
        value=f"{user['xp']} / {xp_to_next_level(user['level'])}",
        inline=True,
    )

    xp_progress = (user["xp"] / xp_to_next_level(user["level"])) * 100
    embed.add_field(
        name="**XP Progress** 📊",
        value=f"**{xp_progress:.2f}%** to next level! Keep it up! 💪",
        inline=False,
    )

    embed.set_thumbnail(url=member.avatar.url)

    embed.set_footer(text="Keep chatting to level up! 🚀")

    await ctx.send(embed=embed)


@bot.command(name="toplvl", aliases=["topl"])
async def toplvl(ctx):

    sorted_users = sorted(
        user_data.items(), key=lambda x: (x[1]["level"], x[1]["xp"]), reverse=True
    )

    server_icon_url = ctx.guild.icon.url if ctx.guild.icon else None

    embed = discord.Embed(
        title="🏆 Top 10 Leaderboard 🌟",
        description="🚀 These are the top 10 users with the highest levels and XP on the server! 🌟",
        color=discord.Color.gold(),
    )

    if server_icon_url:
        embed.set_thumbnail(url=server_icon_url)

    for index, (user_id, data) in enumerate(sorted_users[:10], start=1):
        member = await bot.fetch_user(int(user_id)) 

        next_level_xp = xp_to_next_level(data["level"])
        xp_needed = next_level_xp - data["xp"]

        embed.add_field(
            name=f"🏅 #{index} {member.display_name}",
            value=(
                f"**Level**: {data['level']} | **XP**: {data['xp']} / {next_level_xp}\n"
                f"**XP needed for next level**: {xp_needed}"
            ),
            inline=False,
        )

    embed.set_footer(text="💪 Keep grinding to climb higher! 🔝")

    await ctx.send(embed=embed)



def xp_to_next_level(level):
    return level * 100 + 100  


#################################################################################

@bot.event
async def on_message(message):
    await collect_words(message)
    if message.author.bot:
        return  

    if message.content.startswith("$"):
        await bot.process_commands(message)
        return

    #################################################################################

    # Giving XP for messages
    #-----------------------------------------------------------------------------

    user = get_user_data(str(message.author.id))
    current_time = time.time()

    if current_time - user["last_message_time"] > 10: 
        user["xp"] += 10  
        user["last_message_time"] = current_time
        check_level_up(user)  
        save_user_data() 

    await bot.process_commands(message)

    #################################################################################

    # PATHOS RANDOM SENTENCE GENERATOR
    #-----------------------------------------------------------------------------

    channel_history = {}

    def update_channel_history(channel_id, content, limit=5):
        if channel_id not in channel_history:
            channel_history[channel_id] = []
        channel_history[channel_id].append(content)
        channel_history[channel_id] = channel_history[channel_id][-limit:]

    def extract_words_from_history(channel_id):
        if channel_id not in channel_history:
            return []
        text = " ".join(channel_history[channel_id])
        words = [w.strip(".,!?()[]{}").lower() for w in text.split() if len(w) > 3]
        return list(set(words))  

    def generate_contextual_random_sentence(channel_id):

        bot_word = generate_random_sentence()

        user_words = extract_words_from_history(channel_id)
        if user_words:
            context_word = random.choice(user_words)
            return f"{context_word} {bot_word}"
        else:
            return bot_word

    emoji_reactions = [
        "😀",
        "😁",
        "😂",
        "🤣",
        "😊",
        "😇",
        "😍",
        "😎",
        "🥳",
        "😜",
        "🤪",
        "😻",
        "😏",
        "😃",
        "🤗",
        "😅",
        "🥺",
        "😈",
        "👻",
        "💀",
    ]

    bot_mentions = (
        "bot",
        "pandos",
        "Pandos",
        "PandOS",
        "PandOs",
        "PandoS",
        "PANDOS",
        "Panda",
        "panda",
        "1372899410933186640",
        "@PandOS",
    )

    update_channel_history(message.channel.id, message.content)

    if message.reference:
        referenced_message = await message.channel.fetch_message(
            message.reference.message_id
        )
        if referenced_message.author == bot.user:
            response = generate_contextual_random_sentence(message.channel.id)
            await message.reply(response)
            await message.add_reaction(random.choice(emoji_reactions))

    elif any(mention in message.content.lower() for mention in bot_mentions):
        response = generate_contextual_random_sentence(message.channel.id)
        await message.reply(response)
        await message.add_reaction(random.choice(emoji_reactions))

    await bot.process_commands(message)

    #################################################################################

    # MESSAGE EMBED GENERATOR
    #-----------------------------------------------------------------------------

    if message.channel.id == 1330223637478903858:

        await message.delete()

        embed = discord.Embed(
            title=f"Message from {message.author.name}",
            description=f"**Message:**\n{message.content}",
            color=discord.Color.blue(), 
        )

        embed.set_thumbnail(url=message.author.avatar.url)

        embed.add_field(name="Date & Time", value="🎮• 1/30/2025 7:46 PM", inline=False)

        role_ping = "<@&1330225008290693190>"  

        embed.set_footer(
            text="React below to show your interest!", icon_url=bot.user.avatar.url
        )

        embed.add_field(
            name="\u200b", value="━━━━━━━━━━━━━━━━━━━━━━━━━━━━", inline=False
        )

        message_to_send = await message.channel.send(f"{role_ping}", embed=embed)

        await message_to_send.add_reaction("👍")
        await message_to_send.add_reaction("👎")

    await bot.process_commands(message)

    #################################################################################

    # LEVELING SYSTEM XP & LEVELS
    #-----------------------------------------------------------------------------

    user_id = str(message.author.id) 
    user = get_user_data(
        user_id
    ) 

    current_time = time.time()
    if (
        current_time - user.get("last_message_time", 0) > 10
    ):  
        user["xp"] += 10  
        user["last_message_time"] = (
            current_time  
        )

        if user["xp"] >= xp_to_next_level(user["level"]):
            user["xp"] -= xp_to_next_level(user["level"]) 
            user["level"] += 1  

            await message.channel.send(
                f"{message.author.mention} has leveled up to level {user['level']}!"
            )

            try:
                embed = discord.Embed(
                    title="🎉 Congratulations!",
                    description=f"**{message.author.display_name}**, you've reached level **{user['level']}**! 🏆",
                    color=discord.Color.green(),
                )
                embed.set_thumbnail(
                    url=message.author.avatar.url
                )  
                embed.add_field(
                    name="Your Stats",
                    value=f"**XP**: {user['xp']}\n**Level**: {user['level']}",
                    inline=False,
                )
                embed.add_field(
                    name="Keep it up!",
                    value="Keep grinding and level up even more! 🚀",
                    inline=False,
                )
                embed.set_footer(
                    text="Congrats again! Thanks for being part of the community!",
                    icon_url="https://example.com/path_to_footer_icon.png", 
                )  

                await message.author.send(embed=embed)
                print(f"Sent level-up embed to {message.author.display_name}")
            except discord.errors.Forbidden:
                print(
                    f"Could not send message to {message.author.display_name} (DMs are closed)"
                )
            except Exception as e:
                print(f"An error occurred: {e}")

        save_user_data() 

    await bot.process_commands(message)  

    #################################################################################

    # Chain Words Game
    #-----------------------------------------------------------------------------

    STORY_FILE = "story_data.json"
    current_story = []
    MAX_WORDS = 20  

    def load_story():
        try:
            with open(STORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_story():
        with open(STORY_FILE, "w", encoding="utf-8") as f:
            json.dump(current_story, f)

    current_story = load_story()

    if message.channel.id == CHAIN_WORDS_CHANNEL_ID:
        content = message.content.strip()

        guild_icon_url = message.guild.icon.url if message.guild.icon else None

        if len(content.split()) > 1 or re.search(r"[^\w\sąćęłńóśźżĄĆĘŁŃÓŚŹŻ]", content):
            embed = discord.Embed(
                title="❌ Error!",
                description="Proszę podaj **tylko jedno słowo**, bez znaków interpunkcyjnych!",
                color=discord.Color.red(),
            )
            if guild_icon_url:
                embed.set_thumbnail(url=guild_icon_url)
            await message.channel.send(embed=embed)
            return

        current_story.append(content)
        save_story()

        if len(current_story) >= MAX_WORDS:
            story_text = " ".join(current_story)
            embed = discord.Embed(
                title="📖 Historia zakończona!",
                description=f"✍️ **{story_text}**",
                color=discord.Color.blue(),
            )
            embed.set_footer(text="Nowa historia rozpoczęta!")
            if guild_icon_url:
                embed.set_thumbnail(url=guild_icon_url)

            message_sent = await message.channel.send(embed=embed)
            await message_sent.add_reaction("👍")
            await message_sent.add_reaction("👎")

            current_story = []
            save_story() 
            return

        embed = discord.Embed(
            title="✨ Dodano nowe słowo!",
            description=f"📜 Aktualna historia: **{' '.join(current_story)}**",
            color=discord.Color.green(),
        )
        embed.set_footer(text=f"Długość historii: {len(current_story)}/{MAX_WORDS}")
        if guild_icon_url:
            embed.set_thumbnail(url=guild_icon_url)

        await message.channel.send(embed=embed)

    #################################################################################

    # ALL SERVERS MESSAGES COLLECTOR

    log_channel = bot.get_channel(SERVERS_MESSAGES_CHANNEL_ID)

    if log_channel is None:
        print(
            "Log Channel not exist!"
        )  
        return

    else:
        embed = discord.Embed(
            title="📨 MSL System (Messages Logger)",
            description=message.content or "[no content]",
            color=discord.Color.blue(),
            timestamp=message.created_at,
        )

        embed.set_author(
            name=f"{message.author} ({message.author.id})",
            icon_url=message.author.avatar.url if message.author.avatar else None,
        )

        embed.add_field(
            name="👤 Author", value=f"{message.author.mention}", inline=True
        )
        embed.add_field(
            name="🌐 Server",
            value=message.guild.name if message.guild else "DM",
            inline=True,
        )
        embed.add_field(name="📺 Channel", value=message.channel.mention, inline=True)

        if message.attachments:
            embed.add_field(
                name="📎 Attachments",
                value="\n".join(a.url for a in message.attachments),
                inline=False,
            )

        await log_channel.send(embed=embed)

        await bot.process_commands(message)

    #################################################################################

    # DO NAPRAWY LOGOWANIE Z DM
    # DO NAPRAWY LOGOWANIE Z DM
    # DO NAPRAWY LOGOWANIE Z DM
    # DO NAPRAWY LOGOWANIE Z DM
    # DO NAPRAWY LOGOWANIE Z DM
    # DO NAPRAWY LOGOWANIE Z DM

    # log_channel_id = 1326649373974593628  # Twoje ID kanału

    # if isinstance(message.channel, discord.DMChannel):
    #     log_channel = bot.get_channel(log_channel_id)

    #     if log_channel:
    #         embed = discord.Embed(
    #             title="Nowa wiadomość od użytkownika",
    #             description=message.content,
    #             color=discord.Color.blue()
    #         )
    #         embed.set_footer(text=f'Od: {message.author.name}#{message.author.discriminator}')

    #         embed.add_field(name="📺 Kanał", value="Prywatna wiadomość", inline=True)

    #         await log_channel.send(embed=embed)

    # await bot.process_commands(message)

    # DO NAPRAWY LOGOWANIE Z DM
    # DO NAPRAWY LOGOWANIE Z DM
    # DO NAPRAWY LOGOWANIE Z DM
    # DO NAPRAWY LOGOWANIE Z DM
    # DO NAPRAWY LOGOWANIE Z DM
    # DO NAPRAWY LOGOWANIE Z DM

    #################################################################################

    # Detekcja języka (np. pl, en)
    greeting_language = detect_greeting(message)

    if greeting_language:
        response = get_greeting_response(greeting_language)
        await message.channel.send(response)

    else:
        conversation_response = get_conversation_response(
            message, greeting_language or "en"
        )
        if conversation_response:
            await message.channel.send(conversation_response)

    #################################################################################

    team_name = None

    for role in message.author.roles:
        if role.name in team_points:
            team_name = role.name
            break

    if team_name:
        team_points[team_name] += 1
        save_team_points(team_points)
        print(f"{message.author.mention}, you have earned 1 point for {team_name}!")
    else:
        print(f"{message.author.mention}, you are not assigned to any team!")

    #################################################################################

    if message.channel.id == MEDIA_SHARE_CHANNEL_ID:
        if message.attachments:
            description = (
                message.content or "No description provided."
            )  

            for attachment in message.attachments:
                if attachment.content_type and (
                    attachment.content_type.startswith("image/")
                    or attachment.content_type.startswith("video/")
                ):
                    embed = discord.Embed(
                        title="🌟 New Media Share!",
                        description=f"{message.author.mention} shared an image or GIF:\n**Description:** {description}",
                        color=discord.Color.blue(),
                    )

                    embed.set_image(
                        url=attachment.proxy_url
                    )  

                    embed.set_footer(
                        text=f"Shared by {message.author.display_name}",
                        icon_url=message.author.avatar.url,
                    )

                    try:
                        new_message = await message.reply(embed=embed)

                        reactions = ["❤️", "👍", "😂", "😲", "😢", "👎"]
                        for reaction in reactions:
                            await new_message.add_reaction(reaction)

                        confirmation_embed = discord.Embed(
                            title="✅ Your Image/GIF Has Been Shared!",
                            description=f"Your media has been successfully shared in <#{TARGET_MEDIA_CHANNEL_ID}>.\n\nYou can view it [here]({new_message.jump_url}).",
                            color=discord.Color.green(),
                        )

                        await message.author.send(embed=confirmation_embed)

                    except Exception as e:
                        print(f"An error occurred while processing the media: {e}")

                    return 

        print("Nieprawidłowa wiadomość wykryta. Próba usunięcia...")
        deletion_embed = discord.Embed(
            title="❌ Invalid Media",
            description="Your message has been deleted because it didn't contain a valid image or GIF.",
            color=discord.Color.red(),
        )

        try:
            await message.author.send(embed=deletion_embed)
        except Exception as e:
            print(f"Błąd wysyłania wiadomości DM: {e}")

        try:
            await message.delete()
            print("Wiadomość została pomyślnie usunięta.")
        except Exception as e:
            print(f"Błąd usuwania wiadomości: {e}")

    #  VERIFICATION 3.0 PandOS

    if isinstance(message.author, discord.Member):
        if (
            VERIFY_ROLE_ID not in [role.id for role in message.author.roles]
            and not message.author.bot
        ):
            await message.delete()

            verification_channel = await create_verification_channel(message.author)
            await send_verification_dm(message.author, verification_channel)

            embed_public = discord.Embed(
                description=(
                    f"{message.author.mention}, your message was removed because you're not verified.\n"
                    f"Please complete verification here: {verification_channel.mention}"
                ),
                color=discord.Color.orange(),
            )
            try:
                await message.channel.send(embed=embed_public)
            except discord.Forbidden:
                print(
                    f"[Błąd] Bot nie ma uprawnień do wysyłania wiadomości na kanale: {message.channel.name}"
                )
            except Exception as e:
                print(f"[Błąd] Coś poszło nie tak: {e}")

            return

    await bot.process_commands(message)

#################################################################################


@bot.command(name="say")
@commands.has_permissions(administrator=True)
async def say(ctx, *, message: str):
    if ctx.author.id == SAY_USER_ID:
        sent_message = await ctx.send(message)
        try:
            await ctx.message.delete() 
        except discord.errors.NotFound:
            print("Message already deleted or not found.")
        except discord.errors.Forbidden:
            print("Bot does not have permission to delete the message.")


#################################################################################


@bot.command(name="announcement")
@commands.has_permissions(administrator=True)
async def announcement(ctx, *, message: str):
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


#################################################################################

@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount: int):
    if amount < 1 or amount > 100:
        embed = discord.Embed(
            title="⚠️ Invalid Amount!",
            description="Please enter a number between **1 and 100**.",
            color=discord.Color.orange(),
        )
        await ctx.send(embed=embed, delete_after=5)
        return

    deleted = await ctx.channel.purge(
        limit=amount + 1
    )  

    embed = discord.Embed(
        title="🧹 Messages Cleared!",
        description=f"Successfully deleted **{len(deleted)-1} messages**.",
        color=discord.Color.purple(),
    )
    embed.set_footer(text=f"Cleared by {ctx.author.name}")
    if ctx.guild.icon:
        embed.set_thumbnail(url=ctx.guild.icon.url)

    confirmation = await ctx.send(embed=embed)
    await confirmation.delete(delay=5) 



#################################################################################

# User Left Logging
#-----------------------------------------------------------------------------

@bot.event
async def on_member_remove(member):
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    await send_log_embed(
        log_channel, "Member Left", f"{member.name} has left the server."
    )


#################################################################################

# VERIFICATION 3.0 PandOS | BetterSideOfGaming | VPanda
#-----------------------------------------------------------------------------

def get_verification_channel_name(member):
    return f"access-{member.name.lower().replace(' ', '-')}-{member.discriminator}"


@bot.event
async def on_voice_state_update(member, before, after):
    if (
        VERIFY_ROLE_ID not in [role.id for role in member.roles]
        and after.channel is not None
    ):
        await member.move_to(None)
        channel = await create_verification_channel(member)
        


async def send_verification_dm(member, verification_channel):
    embed = discord.Embed(title="🔒 Verification Required", color=discord.Color.red())
    embed.add_field(
        name="🚫 Access Denied",
        value="You cannot use server features without verification.",
        inline=False,
    )
    embed.add_field(
        name="📌 How to Verify?",
        value=f"A private verification channel has been created for you: {verification_channel.mention}\n"
        f"Please follow the instructions there.",
        inline=False,
    )
    embed.set_footer(text="Thank you for understanding!")
    try:
        await member.send(embed=embed)

    except discord.Forbidden:
        pass 


async def create_verification_channel(member):
    guild = member.guild
    channel_name = get_verification_channel_name(member)
    existing_channel = discord.utils.get(guild.text_channels, name=channel_name)
    if existing_channel:
        return existing_channel

    category = discord.utils.get(guild.categories, id=VERIFY_CATEGORY_ID)
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        guild.me: discord.PermissionOverwrite(read_messages=True),
    }

    channel = await guild.create_text_channel(
        channel_name,
        category=category,
        overwrites=overwrites,
        reason="Verification required",
    )

    await send_verification_dm(member, channel) 
    await start_verification_process(member, channel)

    return channel

async def start_verification_process(member, channel):
    verification_code = "".join(
        random.choices(string.ascii_letters + string.digits, k=10)
    )
    verification_codes[member.id] = verification_code

    await channel.send(
        "# VERIFICATION SYSTEM 3.0 By BetterSideOfGaming | BSOG Team | © VPanda"
    )

    await channel.send("https://tenor.com/view/verification-gif-27378165")

    joined_at = (
        member.joined_at.strftime("%Y-%m-%d %H:%M:%S")
        if member.joined_at
        else "Unknown"
    )
    created_at = member.created_at.strftime("%Y-%m-%d %H:%M:%S")

    user_info_embed = discord.Embed(
        title=f"🔍 User Verification Info",
        description=f"Below are the details of **{member.mention}**:",
        color=discord.Color.blurple(),
        timestamp=discord.utils.utcnow(),
    )
    user_info_embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
    user_info_embed.add_field(name="🧾 Username", value=str(member), inline=True)
    user_info_embed.add_field(name="🆔 User ID", value=str(member.id), inline=True)
    user_info_embed.add_field(name="📆 Account Created", value=created_at, inline=False)
    user_info_embed.add_field(name="📥 Joined Server", value=joined_at, inline=False)
    user_info_embed.add_field(
        name="🔢 Discriminator", value=member.discriminator, inline=True
    )
    user_info_embed.add_field(
        name="🤖 Bot Account?", value="Yes" if member.bot else "No", inline=True
    )
    user_info_embed.set_footer(text="Better Side Of Gaming • Verification Details")

    await channel.send(embed=user_info_embed)

    code_embed = discord.Embed(
        title="✅ Welcome to the Server!", color=discord.Color.gold()
    )
    code_embed.add_field(
        name="🔐 Your Verification Code:", value=f"`{verification_code}`", inline=False
    )
    code_embed.add_field(
        name="📋 Steps to Verify:",
        value=(
            "1. Read the rules below.\n"
            "2. React with ✅ to accept them.\n"
            f"3. Type `$start {verification_code}` in **this channel**."
        ),
        inline=False,
    )
    code_embed.set_footer(text="⚠️ Do not share your code with anyone!")
    await channel.send(content=member.mention, embed=code_embed)

    rules_embed = discord.Embed(
        title="📜 Server Rules",
        description=(
            "Please read and accept the rules:\n"
            "🔗 [Better Side Of Gaming Rules](https://vezyyy.github.io/BetterSideOfGaming/rules.html)\n"
            "🔗 [Discord Guidelines](https://discord.com/guidelines)\n\n"
            "React with ✅ to confirm you understand and accept these rules."
        ),
        color=discord.Color.orange(),
    )
    msg = await channel.send(embed=rules_embed)
    await msg.add_reaction("✅")
    await channel.send("### ----------------------------------------")

    def check(reaction, user):
        return (
            user == member
            and str(reaction.emoji) == "✅"
            and reaction.message.id == msg.id
        )

    try:
        await channel.send(
            "**⏳ You have 15 minutes to accept the rules and verify yourself using the code. "
            "If you don’t complete the process in time, the verification code will expire.**"
        )
        await bot.wait_for("reaction_add", timeout=900.0, check=check)
        accepted_rules.add(member.id)
        await channel.send(
            "✅ Rules accepted! Now type your verification code like this: `$start <code>`"
        )
    except asyncio.TimeoutError:
        await channel.send("❌ Time expired. Please rejoin or contact staff.")
        await asyncio.sleep(10)
        await channel.delete()


async def send_welcome_embed(member):
    general_channel = member.guild.get_channel(GENERAL_CHANNEL_ID)
    if general_channel:
        embed = discord.Embed(
            title="✅ Verification Complete! 🎉",
            description=(
                f"{member.mention} has just completed verification and officially joined our virtual family here at Better Side Of Gaming! 💜"
            ),
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow(),
        )
        embed.add_field(
            name="👋 Give a warm welcome!",
            value=f"Let’s all welcome {member.mention} in <#1295000603679916042> — show them what our community is all about! 🙌",
            inline=False,
        )
        embed.set_footer(text="Better Side Of Gaming • You’re one of us now ✨")
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)
        await general_channel.send(embed=embed)


async def send_verification_log(member, success: bool):
    channel = member.guild.get_channel(LOG_CHANNEL_ID)
    if channel:
        if success:
            embed = discord.Embed(
                title="✅ User Verified",
                description=f"{member.mention} has successfully completed verification.",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow(),
            )
        else:
            embed = discord.Embed(
                title="❌ Verification Required",
                description=f"{member.mention} needs to complete verification.",
                color=discord.Color.red(),
                timestamp=discord.utils.utcnow(),
            )
        await channel.send(embed=embed)


@bot.command()
async def start(ctx, code: str):
    member = ctx.author
    if member.id not in accepted_rules:
        await ctx.send("❗ You must accept the rules first by reacting with ✅.")
        await send_verification_log(
            member, success=False
        )  
        return

    if verification_codes.get(member.id) == code:
        role = ctx.guild.get_role(VERIFY_ROLE_ID)
        await member.add_roles(role)

        await ctx.send("🎉 You are now verified! Welcome!")

        await send_welcome_embed(member)  

        try:
            dm_embed = discord.Embed(
                title="✅ Verification Complete!",
                description="You have successfully completed verification and now have access to the server features.",
                color=discord.Color.green(),
            )
            await member.send(embed=dm_embed)
        except discord.Forbidden:
            pass  

        await send_verification_log(
            member, success=True
        )  

        del verification_codes[member.id]
        accepted_rules.discard(member.id)

        try:
            await ctx.channel.delete()
        except:
            pass 
    else:
        await ctx.send("❌ Incorrect code. Please try again.")
        await send_verification_log(
            member, success=False
        ) 


#################################################################################

async def fetch_steam_sales():
    """Fetches current Steam sales and sends them to Discord."""
    try:
        response = requests.get(STEAM_API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        sales = data.get("specials", {}).get("items", [])

        if not sales:
            print("No available sales.")
            return

        channel = bot.get_channel(DISCORD_CHANNEL_ID_STEAM_SALES)
        if not channel:
            print("Discord channel not found. Check the channel ID.")
            return

        embeds = []
        for sale in sales:
            title = sale.get("name", "Unknown game")
            discount_price = sale.get("final_price")
            normal_price = sale.get("initial_price")
            game_url = sale.get("url", "https://store.steampowered.com/")
            discount_percentage = sale.get("discount_percent", 0)
            header_image = sale.get(
                "header_image", "https://store.steampowered.com/favicon.ico"
            )

            if discount_price is None:
                print(f"Skipping {title}, missing discount price.")
                continue

            normal_price_text = (
                f"Original price: {normal_price / 100:.2f} USD"
                if normal_price
                else "No data on original price"
            )

            embed = discord.Embed(
                title=f"🔥 {title} - {discount_percentage}% OFF!",
                description=(
                    f"💰 **Discounted Price**: `{discount_price / 100:.2f} USD`\n"
                    f"💸 **{normal_price_text}**\n\n"
                    f"[🛒 Click here to visit the store]({game_url})"
                ),
                color=discord.Color.gold(),
            )
            embed.set_thumbnail(url=header_image)
            embed.set_footer(
                text="Steam Sales Tracker",
                icon_url="https://store.steampowered.com/favicon.ico",
            )
            embeds.append(embed)

        for embed in embeds:
            await channel.send(embed=embed)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Steam: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

@tasks.loop(hours=24)
async def send_steam_sales():
    await fetch_steam_sales()

# DEBUG Command For Admins!
#-----------------------------------------------------------------------------
@bot.command()
async def check_sales(ctx):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send(
            "❌ **You do not have permission to use this command. Only admins can do this.**"
        )
        return
    else:   
        await fetch_steam_sales()
        await ctx.send("✅ **Steam sales have been checked and sent!**")


#################################################################################

# PARTNERSHIP PROGRAM START AND END COMMANDS
#-----------------------------------------------------------------------------

@bot.command()
async def partnership_start(ctx, user_id: int):
    """Assigns the 'Partnership Program' role to the user and sends a welcome message."""
    if not ctx.author.guild_permissions.administrator:
        await ctx.send(
            "❌ **You do not have permission to use this command. Only admins can do this.**"
        )
        return

    try:
        guild = await bot.fetch_guild(GUILD_ID)
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
                "Thank you for joining our partnership program on Discord! We are excited to have you as part of our community, and we hope our collaboration will be beneficial to both parties.\n\n"
                "If you have any questions or concerns, feel free to reach out to the server admins or contact us through our website:\n\n"
                "🔗 [Better Side Of Gaming - Discord Server](https://vezyyy.github.io/BetterSideOfGaming/)\n\n"
                "Once again, thank you, and we look forward to a successful partnership! 🚀🎮"
            ),
            color=discord.Color.green(),
        )
        embed.set_footer(text="BetterSideOfGaming")

        try:
            await member.send(embed=embed)
            await ctx.send(f"✅ **Partnership started for <@{user_id}>!**")
        except discord.Forbidden:
            await ctx.send(
                f"⚠️ Could not send a message to <@{user_id}>. Please check if their DMs are open."
            )
        except Exception as e:
            await ctx.send(f"⚠️ An error occurred while sending the message: {e}")

    except discord.NotFound:
        await ctx.send("❌ **User or server not found!**")
    except discord.Forbidden:
        await ctx.send(
            "⚠️ The bot does not have permission to assign roles or send messages."
        )
    except Exception as e:
        await ctx.send(f"⚠️ An error occurred: {e}")

# Partnership Start Command 
#-----------------------------------------------------------------------------

@bot.command()
async def partnership_end(ctx, user_id: int):
    """Removes the 'Partnership Program' role from the user and sends a termination message."""
    if not ctx.author.guild_permissions.administrator:
        await ctx.send(
            "❌ **You do not have permission to use this command. Only admins can do this.**"
        )
        return

    try:
        guild = await bot.fetch_guild(GUILD_ID)
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
            color=discord.Color.red(),
        )
        embed.set_footer(text="BetterSideOfGaming")

        try:
            await member.send(embed=embed)
            await ctx.send(f"✅ **Partnership terminated for <@{user_id}>!**")
        except discord.Forbidden:
            await ctx.send(
                f"⚠️ Could not send a message to <@{user_id}>. Please check if their DMs are open."
            )
        except Exception as e:
            await ctx.send(f"⚠️ An error occurred while sending the message: {e}")

    except discord.NotFound:
        await ctx.send("❌ **User or server not found!**")
    except discord.Forbidden:
        await ctx.send(
            "⚠️ The bot does not have permission to remove roles on the server."
        )
    except Exception as e:
        await ctx.send(f"⚠️ An error occurred: {e}")


#################################################################################

# RATE OUR SERVER BSOG
#-----------------------------------------------------------------------------

@bot.command(name="sendrateserverinfo")
async def send_rate_server_info(ctx, user_id: int):
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
        color=discord.Color.blue(),
    )
    embed.add_field(
        name="📝 Rate Us!",
        value=rating_description,
        inline=False,
    )
    embed.add_field(
        name="Your Star Rating:",
        value=star_rating,
        inline=False,
    )
    embed.add_field(
        name="🌟 Leave Feedback!",
        value="You can do that here: [Rate us on Disboard](https://disboard.org/pl/server/1294993835717562470)",
        inline=False,
    )
    embed.set_footer(text="Your feedback is important to us!")

    embed.set_thumbnail(
        url="https://example.com/path_to_your_thumbnail.png"
    ) 

    try:
        await user.send(embed=embed)
        await ctx.send(f"Message sent to {user.display_name}!")
    except discord.errors.Forbidden:
        await ctx.send(
            f"I can't send a message to {user.display_name} because their DMs are closed."
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        await ctx.send("An error occurred while trying to send the message.")


#################################################################################

# Run the bot
bot.run(TOKEN)
