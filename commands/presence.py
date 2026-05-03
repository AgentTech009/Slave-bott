import discord
from discord.ext import commands
from datetime import datetime, timezone

LOG_CHANNEL_ID = 1500403352763236382

TRACKED_USERS = [
    123456789012345678,  # your id
    987654321098765432   # other person id
]


class PresenceLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_status_info(self, status):
        status = str(status)

        if status == "online":
            return "🟢 Online", discord.Color.green()
        elif status == "offline":
            return "⚫ Offline", discord.Color.dark_grey()
        elif status == "idle":
            return "🌙 Idle", discord.Color.gold()
        elif status == "dnd":
            return "⛔ Do Not Disturb", discord.Color.red()
        else:
            return f"❓ {status}", discord.Color.blurple()

    def make_embed(self, member, before_status, after_status):
        now = datetime.now(timezone.utc)

        before_text, _ = self.get_status_info(before_status)
        after_text, color = self.get_status_info(after_status)

        embed = discord.Embed(
            title="Presence Update",
            color=color,
            timestamp=now
        )

        embed.add_field(
            name="User",
            value=f"{member.mention}\n`{member}`",
            inline=False
        )

        embed.add_field(
            name="Status Change",
            value=f"{before_text} → {after_text}",
            inline=False
        )

        embed.add_field(
            name="Time",
            value=f"<t:{int(now.timestamp())}:F>\n<t:{int(now.timestamp())}:R>",
            inline=False
        )

        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text="Live Presence Tracker")

        return embed

    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        if after.id not in TRACKED_USERS:
            return

        before_status = str(before.status)
        after_status = str(after.status)

        # only log if actually changed
        if before_status == after_status:
            return

        channel = self.bot.get_channel(LOG_CHANNEL_ID)

        if channel is None:
            try:
                channel = await self.bot.fetch_channel(LOG_CHANNEL_ID)
            except:
                return

        embed = self.make_embed(after, before_status, after_status)
        await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(PresenceLogger(bot))
