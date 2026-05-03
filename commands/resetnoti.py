import discord
from discord.ext import commands
from datetime import datetime

STARTUP_CHANNEL_ID = 1500403352763236382


class StartupNotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sent = False

    @commands.Cog.listener()
    async def on_ready(self):
        if self.sent:
            return

        self.sent = True

        channel = self.bot.get_channel(STARTUP_CHANNEL_ID)

        if channel is None:
            try:
                channel = await self.bot.fetch_channel(STARTUP_CHANNEL_ID)
            except:
                return

        embed = discord.Embed(
            title="Bot Online",
            description="Bot has restarted or redeployed successfully.",
            color=discord.Color.green(),
            timestamp=datetime.utcnow()
        )

        embed.add_field(
            name="Status",
            value="Railway redeploy detected",
            inline=False
        )

        embed.set_footer(text="Startup Notification")

        await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(StartupNotify(bot))
