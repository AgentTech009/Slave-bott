from discord.ext import commands
import discord
import random
import asyncio

SIMON_CHANNEL_ID = 1500168505184485577

REAL_PREFIX = "Simon says"

WORDS = [
    "meow", "Meow", "MEOW", "lebron", "Lebron", "water", "Water",
    "koni", "Koni", "real", "Real", "banana", "Banana", "apple",
    "Apple", "pizza", "Pizza", "hello", "Hello", "bye", "Bye",
    "brainrot", "Brainrot", "aura", "Aura", "npc", "NPC", "lag",
    "Lag", "skill", "Skill", "issue", "Issue", "cooked", "Cooked",
    "hydrate", "Hydrate", "raisin", "Raisin", "fish", "Fish",
    "math", "Math", "grass", "Grass", "dry", "Dry", "wet", "Wet",
    "beans", "Beans", "yap", "Yap", "goofy", "Goofy", "bonk",
    "Bonk", "chaos", "Chaos", "panic", "Panic", "sus", "Sus",
    "valid", "Valid", "error", "Error", "glitch", "Glitch",
    "system", "System", "loading", "Loading", "server", "Server",
    "bot", "Bot", "command", "Command", "termux", "Termux"
]

BUTTON_WORDS = [
    "RED", "BLUE", "GREEN", "YELLOW", "MEOW", "NPC", "AURA",
    "KONI", "WATER", "APPLE", "BOT", "LAG", "BONK", "CHAOS",
    "PANIC", "VALID", "ERROR", "FISH", "PIZZA", "BEANS"
]

FAKE_PREFIXES = [
    "simon says", "SIMON SAYS", "Simon Says", "sImon says",
    "SImon says", "SiMon says", "SimoN says", "Simon say",
    "Simon said", "Simon sayss", "Simon ssys", "Simon syas",
    "Simon saays", "Simon sayz", "S1mon says", "Sim0n says",
    "S!mon says", "SIm0n says", "S1m0n says", "Simson says",
    "Saimon says", "Semon says", "S i m o n says",
    "Simon says:", "Simon says -", "Simon says...",
    "Simon says??", "Not Simon says", "Definitely Simon says",
    "Koni says", "Lebron says", "Bot says", "System says"
]

ACTIONS = ["say", "type", "send", "reply with"]
FAKE_ACTIONS = ["say", "type", "send", "reply", "write", "yap", "whisper"]


class SimonButtonView(discord.ui.View):
    def __init__(self, cog, channel, expected, real, timeout):
        super().__init__(timeout=timeout)
        self.cog = cog
        self.channel = channel
        self.expected = expected
        self.real = real
        self.got_any_reply = False
        self.finished = False
        self.message = None

        labels = random.sample(BUTTON_WORDS, 5)
        if expected not in labels:
            labels[random.randint(0, 4)] = expected

        random.shuffle(labels)

        styles = [
            discord.ButtonStyle.primary,
            discord.ButtonStyle.secondary,
            discord.ButtonStyle.success,
            discord.ButtonStyle.danger
        ]

        for label in labels:
            button = discord.ui.Button(
                label=label,
                style=random.choice(styles),
                custom_id=f"simon_{label}_{random.randint(1000, 9999)}"
            )
            button.callback = self.make_callback(label)
            self.add_item(button)

    def make_callback(self, label):
        async def callback(interaction: discord.Interaction):
            if interaction.user.bot:
                return

            if self.finished:
                return await interaction.response.send_message(
                    "Round already ended lil bro",
                    ephemeral=True
                )

            self.got_any_reply = True
            uid = interaction.user.id

            if self.real:
                if label == self.expected:
                    self.cog.add_score(uid, 1)
                    self.finished = True

                    for item in self.children:
                        item.disabled = True

                    await interaction.response.edit_message(view=self)
                    await self.channel.send(f"{interaction.user.mention} +1")
                    self.stop()
                else:
                    self.cog.add_score(uid, -1)
                    await interaction.response.send_message("-1 wrong button 💀", ephemeral=True)
                    await self.channel.send(f"{interaction.user.mention} -1")
            else:
                self.cog.add_score(uid, -1)
                await interaction.response.send_message("-1 you fell for fake Simon 😭", ephemeral=True)
                await self.channel.send(f"{interaction.user.mention} -1")

        return callback

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True

        if self.message:
            try:
                await self.message.edit(view=self)
            except:
                pass


class Simon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.running = False
        self.scores = {}

    def add_score(self, uid, amount):
        self.scores[uid] = self.scores.get(uid, 0) + amount

    async def get_webhook(self, channel):
        webhooks = await channel.webhooks()
        for webhook in webhooks:
            if webhook.name == "Simon Rules":
                return webhook
        return await channel.create_webhook(name="Simon Rules")

    async def send_rules_webhook(self, channel, rules):
        try:
            webhook = await self.get_webhook(channel)
            await webhook.send(
                content=rules,
                username="Simon Rules",
                avatar_url="https://cdn-icons-png.flaticon.com/512/942/942748.png",
                allowed_mentions=discord.AllowedMentions.none()
            )
        except:
            await channel.send(rules)

    def make_text_prompt(self):
        word = random.choice(WORDS)
        real = random.random() < 0.58

        prefix = REAL_PREFIX if real else random.choice(FAKE_PREFIXES)
        action = random.choice(ACTIONS if real else FAKE_ACTIONS)

        styles = [
            f"{prefix} {action} `{word}`",
            f"{prefix} {action} **{word}**",
            f"{prefix} {action}: `{word}`",
            f"{prefix}\n> {action} `{word}`",
            f"```{prefix} {action} {word}```",
            f"{prefix} {action} ||{word}||",
            f"**{prefix}** {action} `{word}`",
            f"{prefix} __{action}__ `{word}`",
            f"{prefix} {action}\n# {word}",
            f"{prefix} {action} ~~fake~~ `{word}`",
            f"{prefix} {action} [ {word} ]",
            f"{prefix} {action} >>> `{word}`"
        ]

        return random.choice(styles), word, real

    def make_button_prompt(self):
        expected = random.choice(BUTTON_WORDS)
        real = random.random() < 0.55

        prefix = REAL_PREFIX if real else random.choice(FAKE_PREFIXES)

        styles = [
            f"{prefix} press `{expected}`",
            f"{prefix} click **{expected}**",
            f"{prefix}\n> press `{expected}`",
            f"```{prefix} press {expected}```",
            f"{prefix} press ||{expected}||",
            f"**{prefix}** press `{expected}`",
            f"{prefix} press the button named `{expected}`"
        ]

        return random.choice(styles), expected, real

    async def ask_int(self, ctx, question, minimum, maximum):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.send(question)

        try:
            msg = await self.bot.wait_for("message", timeout=30, check=check)
            value = int(msg.content)
        except:
            return None

        if value < minimum or value > maximum:
            return None

        return value

    @commands.command(name="simonstart")
    async def start(self, ctx):
        if ctx.channel.id != SIMON_CHANNEL_ID:
            return

        if self.running:
            return await ctx.send("Simon already running")

        rounds = await self.ask_int(ctx, "How many rounds? `1-50`", 1, 50)
        if rounds is None:
            return await ctx.send("Invalid rounds")

        answer_time = await self.ask_int(ctx, "Timer per question in seconds? `3-60`", 3, 60)
        if answer_time is None:
            return await ctx.send("Invalid timer")

        round_pause = await self.ask_int(ctx, "Break after each question in seconds? `0-30`", 0, 30)
        if round_pause is None:
            return await ctx.send("Invalid break time")

        self.running = True
        self.scores = {}

        rules = (
            "**SIMON SAYS RULES**\n"
            f"Rounds: `{rounds}`\n"
            f"Answer time: `{answer_time}s`\n"
            f"Break: `{round_pause}s`\n\n"
            "**Only exact `Simon says` is real.**\n"
            "`simon says`, `SIMON SAYS`, `Simon Says`, `S1mon says` are fake.\n\n"
            "**Text answers are case sensitive.**\n"
            "`Water` and `water` are different.\n\n"
            "**Button rounds exist now.**\n"
            "If Simon is real, press the correct button.\n"
            "If Simon is fake, press nothing.\n\n"
            "Correct first answer: `+1`\n"
            "Wrong text/button: `-1`\n"
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

            round_type = random.choice(["text", "text", "button"])

            if round_type == "text":
                prompt, expected, real = self.make_text_prompt()

                if fake_streak >= 2:
                    expected = random.choice(WORDS)
                    prompt = f"{REAL_PREFIX} {random.choice(ACTIONS)} `{expected}`"
                    real = True
                    fake_streak = 0

                fake_streak = 0 if real else fake_streak + 1

                await ctx.send(f"**Round {round_num}/{rounds}**\n{prompt}")

                round_ended = False
                got_any_reply = False

                def answer_check(msg):
                    return msg.channel.id == SIMON_CHANNEL_ID and not msg.author.bot

                end_time = asyncio.get_event_loop().time() + answer_time

                while asyncio.get_event_loop().time() < end_time and not round_ended:
                    try:
                        remaining = end_time - asyncio.get_event_loop().time()
                        msg = await self.bot.wait_for(
                            "message",
                            timeout=remaining,
                            check=answer_check
                        )

                        got_any_reply = True
                        uid = msg.author.id
                        content = msg.content.strip()

                        if real:
                            if content == expected:
                                self.add_score(uid, 1)
                                await ctx.send(f"{msg.author.mention} +1")
                                round_ended = True
                            else:
                                self.add_score(uid, -1)
                                await ctx.send(f"{msg.author.mention} -1")
                        else:
                            self.add_score(uid, -1)
                            await ctx.send(f"{msg.author.mention} -1")

                            if content == expected:
                                round_ended = True

                    except asyncio.TimeoutError:
                        break

                if not got_any_reply:
                    await ctx.send("No response")

            else:
                prompt, expected, real = self.make_button_prompt()

                if fake_streak >= 2:
                    expected = random.choice(BUTTON_WORDS)
                    prompt = f"{REAL_PREFIX} press `{expected}`"
                    real = True
                    fake_streak = 0

                fake_streak = 0 if real else fake_streak + 1

                view = SimonButtonView(
                    cog=self,
                    channel=ctx.channel,
                    expected=expected,
                    real=real,
                    timeout=answer_time
                )

                msg = await ctx.send(
                    f"**Round {round_num}/{rounds}**\n{prompt}",
                    view=view
                )

                view.message = msg
                await view.wait()

                if not view.got_any_reply:
                    await ctx.send("No response")

        self.running = False

        if not self.scores:
            return await ctx.send("Game ended. No scores.")

        leaderboard = "**Final scores**\n"
        for uid, pts in sorted(self.scores.items(), key=lambda x: x[1], reverse=True):
            leaderboard += f"<@{uid}> — `{pts}`\n"

        winner_id = max(self.scores, key=self.scores.get)
        winner_score = self.scores[winner_id]

        await ctx.send(leaderboard)
        await ctx.send(f"Winner: <@{winner_id}> with `{winner_score}`")

    @commands.command(name="simonstop")
    async def stop(self, ctx):
        if ctx.channel.id != SIMON_CHANNEL_ID:
            return

        self.running = False
        await ctx.send("Simon stopped")

    @commands.command(name="simonscores")
    async def scores_cmd(self, ctx):
        if ctx.channel.id != SIMON_CHANNEL_ID:
            return

        if not self.scores:
            return await ctx.send("No scores yet")

        leaderboard = "**Current scores**\n"
        for uid, pts in sorted(self.scores.items(), key=lambda x: x[1], reverse=True):
            leaderboard += f"<@{uid}> — `{pts}`\n"

        await ctx.send(leaderboard)


async def setup(bot):
    await bot.add_cog(Simon(bot))
