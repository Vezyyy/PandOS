import discord
from discord.ext import commands

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
async def call_command(ctx, user: discord.Member):
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

# ---------------------
# SETUP FUNCTION
# ---------------------
async def setup(bot):
    bot.add_command(commands.Command(call_command, name="call"))

