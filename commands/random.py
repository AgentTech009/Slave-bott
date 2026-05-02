from discord.ext import commands
import random

# 🔒 HARD CODED CHANNEL
RANDOM_CHANNEL_ID = 1500165632266735747

# default chance
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

class RandomReply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chance = CHANCE  # 🔥 runtime editable

    @commands.command(name="chance")
    async def change_chance(self, ctx, number: int):
        if number < 1:
            return await ctx.send("number must be >= 1 💀")

        self.chance = number
        await ctx.send(f"chance set to 1 in {number} 😈")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.content.startswith("."):
            return

        if message.channel.id != RANDOM_CHANNEL_ID:
            return

        if random.randint(1, self.chance) != 1:
            return

        try:
            reply = random.choice(RANDOM_REPLIES)
            await message.reply(reply, mention_author=False)

        except Exception as e:
            print(f"Random reply error: {e}")

async def setup(bot):
    await bot.add_cog(RandomReply(bot))
