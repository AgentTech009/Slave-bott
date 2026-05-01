from discord.ext import commands
import json
import os

CONFIG_FILE = "lebron_channel.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump({"channel_id": None}, f)

    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

class Lebron(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = load_config()

    @commands.command(name="setlebron")
    async def set_lebron(self, ctx):
        self.config["channel_id"] = ctx.channel.id
        save_config(self.config)

        await ctx.send("Lebron replies enabled 💀")

    @commands.command(name="offlebron")
    async def off_lebron(self, ctx):
        self.config["channel_id"] = None
        save_config(self.config)

        await ctx.send("Lebron replies disabled 😔")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.content.startswith("."):
            return

        channel_id = self.config.get("channel_id")

        if channel_id is None:
            return

        if message.channel.id != channel_id:
            return

        await message.reply("lebron", mention_author=False)

async def setup(bot):
    await bot.add_cog(Lebron(bot))
