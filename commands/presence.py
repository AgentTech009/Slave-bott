import discord
from discord.ext import commands
from datetime import datetime, timezone

TRACKED_USERS = [
    1496825794364702812,  # your id
    1496495520120569880   # other person's id
]

MAX_LOGS = 10


class PresenceLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sessions = {}
        self.current_online_since = {}

    def now(self):
        return datetime.now(timezone.utc)

    def format_time(self, dt):
        if not dt:
            return "Not recorded"

        unix = int(dt.timestamp())
        return f"<t:{unix}:F> • <t:{unix}:R>"

    def format_duration(self, start, end):
        if not start or not end:
            return "Not recorded"

        seconds = int((end - start).total_seconds())

        if seconds < 60:
            return f"{seconds}s"

        minutes = seconds // 60
        if minutes < 60:
            return f"{minutes}m"

        hours = minutes // 60
        mins = minutes % 60
        if hours < 24:
            return f"{hours}h {mins}m"

        days = hours // 24
        hrs = hours % 24
        return f"{days}d {hrs}h"

    def get_status_text(self, status):
        status = str(status)

        if status == "online":
            return "🟢 Online", discord.Color.green()
        if status == "idle":
            return "🌙 Idle", discord.Color.gold()
        if status == "dnd":
            return "⛔ DND", discord.Color.red()
        if status == "offline":
            return "⚫ Offline", discord.Color.dark_grey()

        return status, discord.Color.blurple()

    def is_visible_online(self, status):
        return str(status) in ["online", "idle", "dnd"]

    def save_session(self, user_id, online_at, offline_at):
        if user_id not in self.sessions:
            self.sessions[user_id] = []

        self.sessions[user_id].insert(0, {
            "online": online_at,
            "offline": offline_at
        })

        self.sessions[user_id] = self.sessions[user_id][:MAX_LOGS]

    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        if after.id not in TRACKED_USERS:
            return

        before_online = self.is_visible_online(before.status)
        after_online = self.is_visible_online(after.status)

        if before_online == after_online:
            return

        now = self.now()

        if not before_online and after_online:
            self.current_online_since[after.id] = now

        elif before_online and not after_online:
            online_at = self.current_online_since.pop(after.id, None)

            if online_at is None:
                online_at = now

            self.save_session(after.id, online_at, now)

    @commands.command(name="lastonline")
    async def lastonline(self, ctx, member: discord.Member = None):
        if member is None:
            return await ctx.send("Use `.lastonline @user`")

        if member.id not in TRACKED_USERS:
            return await ctx.send("That user is not tracked.")

        now = self.now()
        current_status = str(member.status)
        status_text, color = self.get_status_text(current_status)

        if self.is_visible_online(member.status) and member.id not in self.current_online_since:
            self.current_online_since[member.id] = now

        embed = discord.Embed(
            title="Last Online Logs",
            description=f"{member.mention}\n`{member}`",
            color=color,
            timestamp=now
        )

        embed.add_field(
            name="Current Status",
            value=status_text,
            inline=False
        )

        if self.is_visible_online(member.status):
            online_since = self.current_online_since.get(member.id)
            embed.add_field(
                name="Currently Online Since",
                value=self.format_time(online_since),
                inline=False
            )

        logs = self.sessions.get(member.id, [])

        if not logs:
            embed.add_field(
                name="Last 10 Sessions",
                value="No completed online sessions recorded yet.",
                inline=False
            )
        else:
            text = ""

            for index, log in enumerate(logs, start=1):
                online_at = log["online"]
                offline_at = log["offline"]

                text += (
                    f"**#{index}**\n"
                    f"🟢 Online: {self.format_time(online_at)}\n"
                    f"⚫ Offline: {self.format_time(offline_at)}\n"
                    f"⏱️ Duration: `{self.format_duration(online_at, offline_at)}`\n\n"
                )

            embed.add_field(
                name="Last 10 Sessions",
                value=text[:1024],
                inline=False
            )

        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text="Silent Presence Tracker")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(PresenceLogger(bot))
