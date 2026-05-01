from discord.ext import commands
import discord

class Nickname(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="nick")
    @commands.has_permissions(manage_nicknames=True)
    async def change_nick(self, ctx, member: discord.Member, *, nickname=None):
        try:
            await member.edit(nick=nickname)
            await ctx.send(f"Changed nickname for {member.mention}")
        except:
            await ctx.send("Bot role must be above user")

async def setup(bot):
    await bot.add_cog(Nickname(bot))