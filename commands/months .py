from discord.ext import commands
from datetime import datetime

class Months(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # target date (year, month, day)
        self.start_date = datetime(2025, 7, 18)

    @commands.command(name="howlong")
    async def months(self, ctx):
        now = datetime.now()

        delta = now - self.start_date

        days = delta.days
        seconds = delta.total_seconds()

        # approximate months (30.44 avg)
        months = int(days / 30.44)

        await ctx.send(
            f"since july 18 2025:\n"
            f"{months} months\n"
            f"{days} days\n"
            f"{int(seconds)} seconds"
        )

async def setup(bot):
    await bot.add_cog(Months(bot))