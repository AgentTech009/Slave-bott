from discord.ext import commands, tasks
import random
import json
import os

CONFIG_FILE = "randomreply_config.json"

# change this later to 900 for 15 minutes
TIMER_SECONDS = 900

RANDOM_REPLIES = [
    "real",
    "bro what 😭",
    "ok",
    "that was crazy",
    "i agree for no reason",
    "nah this server is cooked 💀",
    "continue...",
    "i like ts msg ngl",
    "absolute cinema",
    "brain activity detected",
    "valid",
    "insane statement",
    "nah explain this",
    "i saw that",
    "interesting... not really tho",
    "that’s wild",
    "peak conversation",
    "who let bro cook",
    "keep cooking",
    "never cook again",
    "lowkey true",
    "highkey insane",
    "i support this nonsense",
    "that msg had aura",
    "aura deducted",
    "certified yap",
    "yap detected",
    "emotional damage",
    "npc dialogue",
    "main character moment",
    "side quest unlocked",
    "this is lore",
    "server history right here",
    "i’m telling the group chat",
    "noted by the council",
    "the council says no",
    "the council is confused",
    "chat is this real",
    "bro is onto nothing",
    "bro might be onto something",
    "source: trust me",
    "scientifically goofy",
    "i understood none of that",
    "same energy as a fridge",
    "this message smells illegal",
    "jail.",
    "straight to jail",
    "me when the when",
    "skill issue",
    "massive W",
    "tiny L",
    "medium rare take",
    "that take is microwaved",
    "go on...",
    "say that again but worse",
    "why did that make sense",
    "i fear you cooked",
    "i fear you burned the kitchen",
    "the voices agree",
    "the voices disagree",
    "bro is fighting demons",
    "demons are winning",
    "kinda poetic ngl",
    "this is why aliens avoid us",
    "brain buffering...",
    "loading response...",
    "error 404: sense not found",
    "fax no printer",
    "printer out of ink",
    "that was personal",
    "who hurt you",
    "i’m just a bot and even i’m tired",
    "unnecessary but funny",
    "that msg needs supervision",
    "delete this before the fbi sees",
    "i rate this 7/10 chaos",
    "solid nonsense",
    "premium brainrot",
    "rare sentence",
    "common nga W",
    "wild behavior",
    "suspiciously specific",
    "this has villain energy",
    "romanticize the delusion",
    "professional yapper",
    "minor spelling crime",
    "i pretend to understand",
    "say less",
    "say more actually",
    "nah this is cinema",
    "peak fiction",
    "unhinged but okay",
    "bro typed that with confidence",
    "confidence is scary",
    "that’s going in the records",
    "screenshot worthy",
    "i’m not built for this",
    "meow",
    "lebron",
    "koni would agree",
    "this channel needs therapy",
    "therapy is expensive tho",
    "anyway...",
    "moving on before it gets worse"
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
        self.random_reply_loop.start()

    def cog_unload(self):
        self.random_reply_loop.cancel()

    @commands.command(name="setrandomreply")
    @commands.has_permissions(administrator=True)
    async def set_random_reply(self, ctx):
        self.config["channel_id"] = ctx.channel.id
        save_config(self.config)
        await ctx.send("Random replies enabled in this channel 💀")

    @commands.command(name="offrandomreply")
    @commands.has_permissions(administrator=True)
    async def off_random_reply(self, ctx):
        self.config["channel_id"] = None
        save_config(self.config)
        await ctx.send("Random replies disabled 😔")

    @tasks.loop(seconds=TIMER_SECONDS)
    async def random_reply_loop(self):
        channel_id = self.config.get("channel_id")

        if channel_id is None:
            return

        channel = self.bot.get_channel(channel_id)

        if channel is None:
            return

        # random chance so it does not reply every single time
        if random.randint(1, 4) != 1:
            return

        try:
            messages = []

            async for msg in channel.history(limit=50):
                if not msg.author.bot and not msg.content.startswith("."):
                    messages.append(msg)

            if not messages:
                return

            chosen_msg = random.choice(messages)
            reply = random.choice(RANDOM_REPLIES)

            await chosen_msg.reply(reply, mention_author=False)

        except Exception as e:
            print(f"Random reply error: {e}")

    @random_reply_loop.before_loop
    async def before_random_reply_loop(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(RandomReply(bot))