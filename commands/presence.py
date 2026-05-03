import discord
from discord.ext import commands
from datetime import datetime, timezone

TRACKED_USERS = [
    1496825794364702812,  # your id
    1496495520120569880   # other person's id
]

MAX_LOGS = 3


class PresenceLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sessions = {}
        self.current_online_since = {}

    def now(self):
        return datetime.now(timezone.utc)

    def is_online_state(self, status):
        return str(status) in ["online", "idle", "dnd"]

    def discord_time(self, dt, style="R"):
        if not dt:
            return "Not recorded"
        return f"<t:{int(dt.timestamp())}:{style}>"

    def duration(self, start, end):
        if not start or not end:
            return "Unknown"

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

    def status_display(self, status):
        status = str(status)

        if status == "online":
            return "🟢 Online", discord.Color.green()
        if status == "idle":
            return "🌙 Idle", discord.Color.gold()
        if status == "dnd":
            return "⛔ DND", discord.Color.red()
        if status == "offline":
            return "⚫ Offline", discord.Color.dark_grey()

        return "❔ Unknown", discord.Color.blurple()

    def save_session(self, user_id, online_at, offline_at):
        self.sessions.setdefault(user_id, [])

        self.sessions[user_id].insert(0, {
            "online": online_at,
            "offline": offline_at
        })

        self.sessions[user_id] = self.sessions[user_id][:MAX_LOGS]

    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        if after.id not in TRACKED_USERS:
            return

        before_online = self.is_online_state(before.status)
        after_online = self.is_online_state(after.status)

        if before_online == after_online:
            return

        now = self.now()

        if not before_online and after_online:
            self.current_online_since[after.id] = now

        elif before_online and not after_online:
            online_at = self.current_online_since.pop(after.id, None) or now
            self.save_session(after.id, online_at, now)

    @commands.command(name="lastonline")
    async def lastonline(self, ctx, member: discord.Member = None):
        if member is None:
            return await ctx.send(embed=discord.Embed(
                title="Missing User",
                description="Use `.lastonline @user`",
                color=discord.Color.red()
            ))

        if member.id not in TRACKED_USERS:
            return await ctx.send(embed=discord.Embed(
                title="Not Tracked",
                description="That user is not being tracked.",
                color=discord.Color.red()
            ))

        now = self.now()
        status_text, color = self.status_display(member.status)

        if self.is_online_state(member.status) and member.id not in self.current_online_since:
            self.current_online_since[member.id] = now

        embed = discord.Embed(
            title="Presence Summary",
            description=f"{member.mention}",
            color=color,
            timestamp=now
        )

        embed.set_thumbnail(url=member.display_avatar.url)

        embed.add_field(
            name="Current",
            value=status_text,
            inline=True
        )

        if self.is_online_state(member.status):
            since = self.current_online_since.get(member.id)

            embed.add_field(
                name="Online Since",
                value=f"{self.discord_time(since, 'R')}\n{self.discord_time(since, 'f')}",
                inline=True
            )
        else:
            embed.add_field(
                name="Online Since",
                value="Not online right now",
                inline=True
            )

        logs = self.sessions.get(member.id, [])

        if not logs:
            embed.add_field(
                name="Recent Sessions",
                value="No finished sessions yet.\nA session is saved after they go offline.",
                inline=False
            )
        else:
            for i, log in enumerate(logs, start=1):
                online_at = log["online"]
                offline_at = log["offline"]

                embed.add_field(
                    name=f"Session #{i}",
                    value=(
                        f"🟢 Joined: {self.discord_time(online_at, 'R')}\n"
                        f"⚫ Left: {self.discord_time(offline_at, 'R')}\n"
                        f"⏱️ Stayed: `{self.duration(online_at, offline_at)}`\n"
                        f"📅 Exact: {self.discord_time(online_at, 'f')} → {self.discord_time(offline_at, 'f')}"
                    ),
                    inline=False
                )

        embed.set_footer(text="Shows the last 3 completed online sessions")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(PresenceLogger(bot))
