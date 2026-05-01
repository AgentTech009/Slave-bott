import discord
from discord.ext import commands
from discord import app_commands

GUILD_ID = 1496826379809853563  # replace with your server ID

class DMModal(discord.ui.Modal):
    def __init__(self, target):
        super().__init__(title=f"DM {target.name}")
        self.target = target

        self.message = discord.ui.TextInput(
            label="Message",
            placeholder="Type your DM here...",
            style=discord.TextStyle.paragraph,
            max_length=1500
        )

        self.add_item(self.message)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            await self.target.send(str(self.message.value))
            await interaction.response.send_message("DM sent ✅", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("DM failed. Their DMs are closed 💀", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Failed: {e}", ephemeral=True)

class DM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="dm", description="Send someone a private DM")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def dm(self, interaction: discord.Interaction, user: discord.Member):
        await interaction.response.send_modal(DMModal(user))

async def setup(bot):
    await bot.add_cog(DM(bot))