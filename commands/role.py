from discord.ext import commands
import discord

COLOR_MAP = {
    "red": discord.Color.red(),
    "blue": discord.Color.blue(),
    "green": discord.Color.green(),
    "purple": discord.Color.purple(),
    "orange": discord.Color.orange(),
    "yellow": discord.Color.gold(),
    "gold": discord.Color.gold(),
    "pink": discord.Color.magenta(),
    "magenta": discord.Color.magenta(),
    "black": discord.Color.dark_grey(),
    "white": discord.Color.light_grey(),
    "grey": discord.Color.greyple(),
    "gray": discord.Color.greyple(),
    "dark": discord.Color.dark_grey(),
    "light": discord.Color.light_grey(),
    "random": discord.Color.random()
}

class Role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="crole")
    @commands.has_permissions(manage_roles=True)
    async def create_role(self, ctx, name, color="white"):
        color = color.lower()

        if color not in COLOR_MAP:
            return await ctx.send(
                "Unknown color. Use: red blue green purple orange yellow gold pink black white grey gray random"
            )

        try:
            role = await ctx.guild.create_role(name=name, colour=COLOR_MAP[color])
            await ctx.send(f"Created role `{role.name}` with color `{color}`")
        except Exception as e:
            await ctx.send(f"Failed to create role: {e}")

    @commands.command(name="grole")
    @commands.has_permissions(manage_roles=True)
    async def give_role(self, ctx, member: discord.Member, role: discord.Role):
        try:
            await member.add_roles(role)
            await ctx.send(f"Gave `{role.name}` to {member.mention}")
        except Exception as e:
            await ctx.send(f"Failed: {e}")

    @commands.command(name="rrole")
    @commands.has_permissions(manage_roles=True)
    async def remove_role(self, ctx, member: discord.Member, role: discord.Role):
        try:
            await member.remove_roles(role)
            await ctx.send(f"Removed `{role.name}` from {member.mention}")
        except Exception as e:
            await ctx.send(f"Failed: {e}")

async def setup(bot):
    await bot.add_cog(Role(bot))