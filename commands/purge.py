from discord.ext import commands

class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="purge")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        if amount <= 0:
            return await ctx.send("Give a valid number 💀")

        try:
            deleted = await ctx.channel.purge(limit=amount + 1)

            msg = await ctx.send(f"Deleted {len(deleted)-1} messages 🧹")
            await msg.delete(delay=3)

        except Exception as e:
            await ctx.send(f"Failed: {e}")

async def setup(bot):
    await bot.add_cog(Purge(bot))