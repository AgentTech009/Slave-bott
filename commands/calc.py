from discord.ext import commands
import math

ALLOWED = {
    "__builtins__": None,
    "abs": abs,
    "round": round,
    "sqrt": math.sqrt,
    "pow": pow,
    "pi": math.pi,
    "e": math.e
}

class Calc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="calc")
    async def calc(self, ctx, *, expr):
        try:
            result = eval(expr, ALLOWED)
            await ctx.send(f"= {result}")
        except Exception:
            await ctx.send("invalid math expression 💀")

async def setup(bot):
    await bot.add_cog(Calc(bot))