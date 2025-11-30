import discord
from discord.ext import commands
from PandOS_Config import SAY_USER_ID  

@commands.command(name="say")
@commands.has_permissions(administrator=True)
async def say(ctx, *, message: str):
    """Repeats a message as the bot, only for a specific user."""
    if ctx.author.id == SAY_USER_ID:
        sent_message = await ctx.send(message)
        try:
            await ctx.message.delete()
        except discord.errors.NotFound:
            print("Message already deleted or not found.")
        except discord.errors.Forbidden:
            print("Bot does not have permission to delete the message.")

async def setup(bot):
    bot.add_command(say)
