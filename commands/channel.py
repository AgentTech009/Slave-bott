from discord.ext import commands

class Channel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="create")
    @commands.has_permissions(manage_channels=True)
    async def create_channel(self, ctx, *, name):
        category = ctx.channel.category
        channel = await ctx.guild.create_text_channel(name, category=category)
        await ctx.send(f"Created {channel.mention}")

    @commands.command(name="rn")
    @commands.has_permissions(manage_channels=True)
    async def rename_channel(self, ctx, *, new_name):
        await ctx.channel.edit(name=new_name)
        await ctx.send(f"Renamed this channel to `{new_name}`")

    @commands.command(name="dlt")
    @commands.has_permissions(manage_channels=True)
    async def delete_channel(self, ctx):
        await ctx.channel.delete()

async def setup(bot):
    await bot.add_cog(Channel(bot))