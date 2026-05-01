from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command()
    async def test(self, ctx):
        await ctx.send("Bot working ✅")

async def setup(bot):
    await bot.add_cog(Ping(bot))