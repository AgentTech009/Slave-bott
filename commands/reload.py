from discord.ext import commands
import os

class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reload")
    @commands.is_owner()
    async def reload_cmd(self, ctx):
        loaded = 0
        failed = []

        for file in os.listdir("./commands"):
            if file.endswith(".py") and file != "__init__.py":
                ext = f"commands.{file[:-3]}"

                try:
                    if ext in self.bot.extensions:
                        await self.bot.reload_extension(ext)
                    else:
                        await self.bot.load_extension(ext)

                    loaded += 1

                except Exception as e:
                    failed.append(f"{file}: {e}")

        if failed:
            await ctx.send("Some failed:\n```" + "\n".join(failed[:5]) + "```")
        else:
            await ctx.send(f"Reloaded {loaded} cmds 🔁")

async def setup(bot):
    await bot.add_cog(Reload(bot))