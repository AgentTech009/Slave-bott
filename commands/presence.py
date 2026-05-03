import discord
from discord.ext import commands
from datetime import datetime, timezone

LOG_CHANNEL_ID = 1500403352763236382

# Put only the 2 user IDs you want to track
TRACKED_USERS = [
    1496825794364702812,
    1496495520120569880
]


class PresenceLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_status = {}

    def make_embed(self, member, before_status, after_status):
        now = datetime.now(timezone.utc)

        if str(after_status) == "online":
            color = discord.Color.green()
            title = "User Online"
        elif str(after_status) == "offline":
            color = discord.Color.red()
            title = "User Offline"
        elif str(after_status) == "idle":
            color = discord.Color.gold()
            title = "User Idle"
        elif str(after_status) == "dnd":
            color = discord.Color.purple()
            title = "User DND"
        else:
            color = discord.Color.blurple()
            title = "Status Changed"

        embed = discord.Embed(
            title=title,
            color=color,
            timestamp=now
        )

        embed.add_field(
            name="User",
            value=f"{member.mention}\n`{member}`",
            inline=False
        )

        embed.add_field(
            name="Change",
            value=f"`{before_status}` → `{after_status}`",
            inline=False
        )

        embed.add_field(
            name="Exact Time",
            value=f"<t:{int(now.timestamp())}:F>\n<t:{int(now.timestamp())}:R>",
            inline=False
        )

        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text="Presence Logger")

        return embed

    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        if after.id not in TRACKED_USERS:
            return

        before_status = str(before.status)
        after_status = str(after.status)

        if before_status == after_status:
            return

        # Only log online/offline
        if after_status not in ["online", "offline"]:
            return

        channel = self.bot.get_channel(LOG_CHANNEL_ID)

        if channel is None:
            try:
                channel = await self.bot.fetch_channel(LOG_CHANNEL_ID)
            except:
                return

        await channel.send(embed=self.make_embed(after, before_status, after_status))


async def setup(bot):
    await bot.add_cog(PresenceLogger(bot))
