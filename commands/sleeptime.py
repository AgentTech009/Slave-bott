from discord.ext import commands
from datetime import datetime, timedelta

class SleepTime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def parse_time(self, t):
        return datetime.strptime(t.upper(), "%I:%M%p")

    @commands.command(name="sleeptime")
    async def sleeptime(self, ctx, start, end):
        try:
            start_time = self.parse_time(start)
            end_time = self.parse_time(end)

            # if end is earlier, assume next day
            if end_time <= start_time:
                end_time += timedelta(days=1)

            delta = end_time - start_time

            hours = delta.seconds // 3600
            minutes = (delta.seconds % 3600) // 60

            await ctx.send(f"slept for {hours}h {minutes}m 💤")

        except:
            await ctx.send("use like: `.sleeptime 11:00PM 9:30AM`")

async def setup(bot):
    await bot.add_cog(SleepTime(bot))