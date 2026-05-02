from discord.ext import commands
import discord
import random
import asyncio

SIMON_CHANNEL_ID = 1500168505184485577  # replace with your channel ID

REAL_PREFIX = "Simon says"

WORDS = [
    "meow", "Meow", "MEOW", "lebron", "Lebron", "water", "Water", "koni", "Koni",
    "real", "Real", "banana", "Banana", "apple", "Apple", "pizza", "Pizza",
    "hello", "Hello", "bye", "Bye", "brainrot", "Brainrot", "aura", "Aura",
    "npc", "NPC", "lag", "Lag", "skill", "Skill", "issue", "Issue",
    "cooked", "Cooked", "hydrate", "Hydrate", "raisin", "Raisin", "fish", "Fish",
    "math", "Math", "grass", "Grass", "dry", "Dry", "wet", "Wet",
    "beans", "Beans", "yap", "Yap", "goofy", "Goofy", "bonk", "Bonk",
    "chaos", "Chaos", "panic", "Panic", "sus", "Sus", "valid", "Valid",
    "error", "Error", "glitch", "Glitch", "system", "System", "loading", "Loading",
    "server", "Server", "bot", "Bot", "command", "Command", "termux", "Termux"
]

FAKE_PREFIXES = [
    "simon says", "SIMON SAYS", "Simon Says", "sImon says", "SImon says",
    "SiMon says", "SimoN says", "Simon Says", "Simon say", "Simon said",
    "Simon sayss", "Simon ssys", "Simon syas", "Simon saays", "Simon sayz",
    "S1mon says", "Sim0n says", "S!mon says", "SIm0n says", "S1m0n says",
    "Simson says", "Saimon says", "Semon says", "S i m o n says",
    "Simon says:", "Simon says -", "Simon says...", "Simon says??",
    "Not Simon says", "Definitely Simon says", "Koni says", "Lebron says",
    "Bot says", "System says"
]

ACTIONS = ["say", "type", "send", "reply with"]
FAKE_ACTIONS = ["say", "type", "send", "reply", "write", "yap", "whisper"]

class Simon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.running = False
        self.scores = {}

    async def get_webhook(self, channel):
        webhooks = await channel.webhooks()
        for webhook in webhooks:
            if webhook.name == "Simon Rules":
                return webhook
        return await channel.create_webhook(name="Simon Rules")

    async def send_rules_webhook(self, channel, rules):
        webhook = await self.get_webhook(channel)
        await webhook.send(
            content=rules,
            username="Simon Rules",
            avatar_url="https://cdn-icons-png.flaticon.com/512/942/942748.png",
            allowed_mentions=discord.AllowedMentions.none()
        )

    def make_prompt(self):
        word = random.choice(WORDS)

        real = random.random() < 0.6

        if real:
            prefix = REAL_PREFIX
            action = random.choice(ACTIONS)
        else:
            prefix = random.choice(FAKE_PREFIXES)
            action = random.choice(FAKE_ACTIONS)

        styles = [
            f"{prefix} {action} `{word}`",
            f"{prefix} {action} **{word}**",
            f"{prefix} {action}: {word}",
            f"{prefix}\n{action} `{word}`",
            f"{prefix} {action} ||{word}||",
        ]

        return random.choice(styles), word, real

    @commands.command(name="simonstart")
    async def start(self, ctx):
        if ctx.channel.id != SIMON_CHANNEL_ID:
            return

        if self.running:
            return await ctx.send("Simon already running")

        def setup_check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.send("How many rounds?")
        try:
            rounds_msg = await self.bot.wait_for("message", timeout=30, check=setup_check)
            rounds = int(rounds_msg.content)
        except:
            return await ctx.send("Invalid rounds")

        await ctx.send("Timer per question in seconds?")
        try:
            timer_msg = await self.bot.wait_for("message", timeout=30, check=setup_check)
            answer_time = int(timer_msg.content)
        except:
            return await ctx.send("Invalid timer")

        await ctx.send("Break after each question in seconds?")
        try:
            break_msg = await self.bot.wait_for("message", timeout=30, check=setup_check)
            round_pause = int(break_msg.content)
        except:
            return await ctx.send("Invalid break time")

        self.running = True
        self.scores = {}

        rules = (
            "**SIMON SAYS RULES**\n"
            f"Rounds: `{rounds}`\n"
            f"Answer time: `{answer_time}s`\n"
            f"Break between rounds: `{round_pause}s`\n\n"
            "**Only this exact phrase is real:** `Simon says`\n"
            "Everything else is fake.\n"
            "`simon says`, `SIMON SAYS`, `S1mon says`, `Simon Says` are fake.\n\n"
            "**Answers are case sensitive.**\n"
            "`Water` and `water` are different.\n\n"
            "First correct answer: `+1`\n"
            "Wrong answer: `-1`\n"
            "Falling for fake Simon: `-1`\n\n"
            "Starting in `10 seconds`."
        )

        await self.send_rules_webhook(ctx.channel, rules)
        await asyncio.sleep(10)

        fake_streak = 0

        for round_num in range(1, rounds + 1):
            if not self.running:
                break

            await asyncio.sleep(round_pause)

            prompt, expected, real = self.make_prompt()

            if fake_streak >= 2:
                real = True
                prefix = REAL_PREFIX
                action = random.choice(ACTIONS)
                expected = random.choice(WORDS)
                prompt = f"{prefix} {action} `{expected}`"
                fake_streak = 0

            if real:
                fake_streak = 0
            else:
                fake_streak += 1

            await ctx.send(f"Round {round_num}/{rounds}\n{prompt}")

            round_ended = False
            got_any_reply = False

            def answer_check(msg):
                return msg.channel.id == SIMON_CHANNEL_ID and not msg.author.bot

            end_time = asyncio.get_event_loop().time() + answer_time

            while asyncio.get_event_loop().time() < end_time and not round_ended:
                try:
                    remaining = end_time - asyncio.get_event_loop().time()
                    msg = await self.bot.wait_for("message", timeout=remaining, check=answer_check)

                    got_any_reply = True
                    uid = msg.author.id
                    content = msg.content.strip()

                    if real:
                        if content == expected:
                            self.scores[uid] = self.scores.get(uid, 0) + 1
                            await ctx.send(f"{msg.author.mention} +1")
                            round_ended = True
                        else:
                            self.scores[uid] = self.scores.get(uid, 0) - 1
                            await ctx.send(f"{msg.author.mention} -1")
                    else:
                        if content == expected:
                            self.scores[uid] = self.scores.get(uid, 0) - 1
                            await ctx.send(f"{msg.author.mention} -1")
                            round_ended = True
                        else:
                            self.scores[uid] = self.scores.get(uid, 0) - 1
                            await ctx.send(f"{msg.author.mention} -1")

                except asyncio.TimeoutError:
                    break

            if not got_any_reply:
                await ctx.send("No response")

        self.running = False

        if not self.scores:
            return await ctx.send("Game ended. No scores.")

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
