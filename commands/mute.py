from discord.ext import commands
import discord
from datetime import timedelta

class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mute")
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member):
        try:
            await member.timeout(timedelta(seconds=30), reason=f"Muted by {ctx.author}")

            await ctx.send(
                f"stop yapping and chill for a sec {member.mention}"
            )

        except discord.Forbidden:
            await ctx.send("I cannot mute them. My role is probably too low.")
        except Exception as e:
            await ctx.send(f"Failed: {e}")

async def setup(bot):
    await bot.add_cog(Mute(bot))