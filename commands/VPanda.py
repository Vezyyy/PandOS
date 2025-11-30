from discord.ext import commands

@commands.command()
async def VPanda(ctx):
    await ctx.send("VPanda & VPanda Studio © 2024-2025 All Rights Reserved.")
    await ctx.send("Visit our website at :point_right:  [VPanda Studio](https://vezyyy.github.io/VPanda/) for more information.")

async def setup(bot):
    bot.add_command(VPanda)
