from discord.ext import commands
import random
import json
import os

CONFIG_FILE = "randomreply_config.json"

# chance: 1 in X messages → increase number = rarer
CHANCE = 15  

RANDOM_REPLIES = [
    "real", "bro what 😭", "ok", "that was crazy",
    "i agree for no reason", "nah this server is cooked 💀",
    "continue...", "i like ts msg ngl", "absolute cinema",
    "brain activity detected", "valid", "insane statement",
    "nah explain this", "i saw that", "that’s wild",
    "who let bro cook", "keep cooking", "never cook again",
    "lowkey true", "highkey insane", "yap detected",
    "npc dialogue", "main character moment", "this is lore",
    "chat is this real", "bro is onto nothing",
    "bro might be onto something", "source: trust me",
    "skill issue", "massive W", "tiny L", "go on...",
    "say that again but worse", "i fear you cooked",
    "i fear you burned the kitchen", "the voices agree",
    "the voices disagree", "brain buffering...",
    "error 404: sense not found", "fax no printer",
    "who hurt you", "premium brainrot", "rare sentence",
    "common nga W", "professional yapper", "say less",
    "say more actually", "peak fiction", "unhinged but okay",
    "meow", "lebron", "koni would agree",
    "this channel needs therapy", "anyway..."
]

def load_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump({"channel_id": None}, f)

    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

class RandomReply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = load_config()

    @commands.command(name="setrandomreply")
    async def set_random_reply(self, ctx):
        self.config["channel_id"] = ctx.channel.id
        save_config(self.config)
        await ctx.send("Random reply mode ON 💀")

    @commands.command(name="offrandomreply")
    async def off_random_reply(self, ctx):
        self.config["channel_id"] = None
        save_config(self.config)
        await ctx.send("Random reply mode OFF 😔")

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

        # 🎯 random chance trigger
        if random.randint(1, CHANCE) != 1:
            return

        try:
            reply = random.choice(RANDOM_REPLIES)
            await message.reply(reply, mention_author=False)

        except Exception as e:
            print(f"Random reply error: {e}")

async def setup(bot):
    await bot.add_cog(RandomReply(bot))
