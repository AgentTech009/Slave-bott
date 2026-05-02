from discord.ext import commands
import random
import asyncio

SIMON_CHANNEL_ID = 1500168505184485577  # your channel

ROUNDS = 15
ANSWER_TIME = 7
ROUND_PAUSE = 5

WORDS = [
    "meow","lebron","water","koni","real","banana","apple","pizza","hello","bye",
    "brainrot","aura","npc","lag","skill","issue","cooked","hydrate","raisin","fish",
    "math","walls","grass","dry","wet","socks","spoon","fork","table","chair",
    "pickle","cheese","noodle","rice","beans","yap","goofy","bonk","boop","mango",
    "vibes","crime","court","guilty","judge","snitch","wizard","rat","cat","dog",
    "frog","duck","bread","toast","jam","juice","milk","sleep","chaos","panic",
    "sus","valid","error","glitch","system","loading","buffer","legacy","bench","hoop",
    "planet","moon","sun","star","cloud","rain","storm","sand","desert","keyboard",
    "mouse","screen","server","bot","command","prefix","termux","github"
]

FAKE_PREFIXES = [
    "SIMON SAYS",
    "simon says",
    "Simon Says",
    "Simon sayss",
    "Simon say",
    "S1mon says",
    "Sim0n says",
    "Simon said",
    "Simon maybe says",
    "Simon kinda says",
    "Simon lowkey says",
    "Simon highkey says",
    "Simon whispers",
    "Simon asks",
    "Simon screams",
    "Simon commands",
    "Simon doesnt say",
    "Not Simon says",
    "Definitely Simon says",
    "Koni says",
    "Lebron says",
    "System says",
    "Bot says",
    "S i m o n says",
    "Simon says??",
    "Simon says...",
    "Simon: says",
    "Simon says -",
    "Simon says:",
]

class Simon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.running = False
        self.scores = {}

    def make_prompt(self, force_real=None):
        word = random.choice(WORDS)

        # 🔥 control fake frequency
        if force_real is None:
            real = random.random() < 0.65  # 65% real 35% fake
        else:
            real = force_real

        if real:
            prefix = "Simon says"  # ONLY valid one
        else:
            prefix = random.choice(FAKE_PREFIXES)

        style = random.choice([
            f"{prefix} {word}",
            f"{prefix} `{word}`",
            f"{prefix} **{word}**",
            f"{prefix}\n{word}",
            f"{prefix}: {word}",
            f"{prefix} ||{word}||"
        ])

        return style, word, real

    @commands.command(name="simonstart")
    async def start(self, ctx):
        if ctx.channel.id != SIMON_CHANNEL_ID:
            return

        if self.running:
            return await ctx.send("Simon already running")

        self.running = True
        self.scores = {}

        await ctx.send("Simon Says started")

        fake_streak = 0

        for round_num in range(1, ROUNDS + 1):
            if not self.running:
                break

            await asyncio.sleep(ROUND_PAUSE)

            # 🔥 prevent too many fake rounds
            if fake_streak >= 2:
                prompt, expected, real = self.make_prompt(force_real=True)
                fake_streak = 0
            else:
                prompt, expected, real = self.make_prompt()
                if not real:
                    fake_streak += 1
                else:
                    fake_streak = 0

            await ctx.send(f"Round {round_num}/{ROUNDS}\n{prompt}")

            answered = False

            def check(msg):
                return msg.channel.id == SIMON_CHANNEL_ID and not msg.author.bot

            end_time = asyncio.get_event_loop().time() + ANSWER_TIME

            while asyncio.get_event_loop().time() < end_time and not answered:
                try:
                    remaining = end_time - asyncio.get_event_loop().time()
                    msg = await self.bot.wait_for("message", timeout=remaining, check=check)

                    uid = msg.author.id
                    content = msg.content.strip()
                    correct = content == expected

                    if real:
                        if correct:
                            self.scores[uid] = self.scores.get(uid, 0) + 1
                            await ctx.send(f"{msg.author.mention} +1")
                            answered = True
                        else:
                            self.scores[uid] = self.scores.get(uid, 0) - 1
                            await ctx.send(f"{msg.author.mention} -1")
                    else:
                        if correct:
                            self.scores[uid] = self.scores.get(uid, 0) - 1
                            await ctx.send(f"{msg.author.mention} -1")
                            answered = True
                        else:
                            self.scores[uid] = self.scores.get(uid, 0) - 1
                            await ctx.send(f"{msg.author.mention} -1")

                except asyncio.TimeoutError:
                    break

            if not answered:
                await ctx.send("No score")

        self.running = False

        if not self.scores:
            return await ctx.send("Game ended")

        leaderboard = "Final scores\n"
        for uid, pts in sorted(self.scores.items(), key=lambda x: x[1], reverse=True):
            leaderboard += f"<@{uid}> — {pts}\n"

        winner_id = max(self.scores, key=self.scores.get)
        winner_score = self.scores[winner_id]

        await ctx.send(leaderboard)
        await ctx.send(f"Winner: <@{winner_id}> with {winner_score}")

    @commands.command(name="simonstop")
    async def stop(self, ctx):
        if ctx.channel.id != SIMON_CHANNEL_ID:
            return

        self.running = False
        await ctx.send("Simon stopped")

async def setup(bot):
    await bot.add_cog(Simon(bot))
