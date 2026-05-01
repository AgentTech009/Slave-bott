from discord.ext import commands
import discord

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if member == ctx.author:
            return await ctx.send("You can't kick yourself 💀")

        try:
            await member.kick(reason=reason)

            try:
                await member.send(f"You were kicked from **{ctx.guild.name}**\nReason: {reason or 'No reason'}")
            except:
                pass

            await ctx.send(f"Kicked {member.mention} ✅")

        except discord.Forbidden:
            await ctx.send("I can't kick them. My role is too low ⚠️")
        except Exception as e:
            await ctx.send(f"Failed: {e}")

async def setup(bot):
    await bot.add_cog(Kick(bot))