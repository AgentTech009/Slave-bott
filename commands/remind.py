from discord.ext import commands
import asyncio
import re

def parse_time(time_text):
    match = re.match(r"^(\d+)(s|m|h|d)$", time_text.lower())
    if not match:
        return None

    amount = int(match.group(1))
    unit = match.group(2)

    if unit == "s":
        return amount
    if unit == "m":
        return amount * 60
    if unit == "h":
        return amount * 3600
    if unit == "d":
        return amount * 86400

class Remind(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="remind")
    async def remind(self, ctx, time_text, *, reason):
        seconds = parse_time(time_text)

        if seconds is None:
            return await ctx.send("Use time like `30s`, `10m`, `2h`, `1d`")

        await ctx.send(f"Reminder set for `{time_text}` ✅")

        await asyncio.sleep(seconds)

        await ctx.send(f"{ctx.author.mention} reminder: {reason}")

async def setup(bot):
    await bot.add_cog(Remind(bot))