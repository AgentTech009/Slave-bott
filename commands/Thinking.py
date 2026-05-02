from discord.ext import commands
import random
import asyncio

THOUGHTS = [
    "i should drink water but nah",
    "why did i open discord again",
    "i am literally the main character",
    "what if i just disappeared for 3 minutes",
    "i should reply but effort is expensive",
    "this server is cooked and i live here",
    "i miss who i was 5 seconds ago",
    "maybe being normal is overrated",
    "i have no enemies except basic tasks",
    "i should sleep but discord exists",
    "what if i type something and regret it instantly",
    "my brain is running on 2 percent",
    "i need food but moving is a scam",
    "why is everyone speaking in side quests",
    "i should be productive but nah",
    "my aura is buffering",
    "i could fix my life or send memes",
    "i am one inconvenience away from villain arc",
    "maybe the bot is watching me",
    "i have thoughts but none are useful",
    "why am i like this",
    "i should touch grass but grass is outside",
    "what if i become mysterious for no reason",
    "i am not lazy i am energy efficient",
    "this message will define my legacy",
    "i wonder if anyone noticed my dramatic silence",
    "i should stop yapping but no",
    "my brain just blue-screened",
    "i need a snack and emotional support",
    "what if i pretend i understood",
    "i am carrying this chat spiritually",
    "today feels like a loading screen",
    "i should drink water before the bot finds out",
    "my social battery is a Nokia with 1 percent",
    "i am losing the argument in my head",
    "maybe i was the NPC all along",
    "i should say something smart... nevermind",
    "my last braincell is on break",
    "i have entered dry mode",
    "why does breathing feel like a task",
    "i am plotting something harmless but stupid",
    "i should not send that... sending anyway",
    "this is not a thought this is a system error",
    "i need a dramatic soundtrack for this moment",
    "i am currently made of confusion",
    "what if i blame lag",
    "i am processing absolutely nothing",
    "i could be wrong but confidently",
    "this server changed me",
    "i need supervision"
]

class Think(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        content = message.content.lower()

        # 🔥 TRIGGER
        if "what is" in content and "thinking" in content and message.mentions:
            target = message.mentions[0]

            thought = random.choice(THOUGHTS)

            await message.channel.send(f"reading {target.mention}'s thoughts... 🧠")
            await asyncio.sleep(2)

            await message.channel.send(
                f"💭 **{target.display_name} is thinking:**\n`{thought}`"
            )

async def setup(bot):
    await bot.add_cog(Think(bot))
