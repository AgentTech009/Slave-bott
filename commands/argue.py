from discord.ext import commands
import discord
import random
import asyncio

SIMON_CHANNEL_ID = 1500000000000000000  # replace with your channel id

WORDS = [
    "meow", "lebron", "water", "koni", "real", "banana", "apple", "pizza", "hello", "bye",
    "brainrot", "aura", "npc", "lag", "skill", "issue", "cooked", "hydrate", "raisin", "fish",
    "math", "walls", "grass", "dry", "wet", "socks", "spoon", "fork", "table", "chair",
    "pickle", "cheese", "noodle", "rice", "beans", "yap", "goofy", "bonk", "boop", "mango",
    "vibes", "crime", "court", "guilty", "judge", "snitch", "wizard", "rat", "cat", "dog",
    "frog", "duck", "bread", "toast", "jam", "juice", "milk", "sleep", "chaos", "panic",
    "sus", "valid", "error", "glitch", "system", "loading", "buffer", "legacy", "bench", "hoop",
    "planet", "moon", "sun", "star", "cloud", "rain", "storm", "sand", "desert", "keyboard",
    "mouse", "screen", "server", "bot", "command", "prefix", "termux", "github", "oxygen",
    "bucket", "mirror", "blanket", "pillow", "remote", "battery", "charger", "button", "signal"
]

REAL_PREFIX = "Simon says"

FAKE_PREFIXES = [
    "SIMON SAYS", "simon says", "Simon Says", "Simson says", "Saimon says", "Simon say",
    "Simon sayss", "S1mon says", "Sim0n says", "Simon said", "Simon maybe says",
    "Simon kinda says", "Simon totally says", "Simon whispers", "Simon asks",
    "Simon commands", "Simon begs", "Simon demands", "Not Simon says",
    "Definitely Simon says", "Koni says", "Lebron says", "System says", "Bot says",
    "S i m o n says", "Simon says??", "Simon says...", "Simon says:", "Simon says -",
    "Simon: says", "SImon says", "SiMon says", "Simon SAYs"
]

FAKE_ACTIONS = [
    "say", "type", "reply", "send", "write", "scream", "whisper", "confess",
    "declare", "announce", "report", "leak", "admit", "yap", "respond with"
]

BUTTON_LABELS = [
    "press me", "do not press", "water", "meow", "lebron", "panic", "real", "fake",
    "safe", "danger", "button", "not this", "this one", "wrong", "correct", "maybe",
    "trust me", "ignore me", "click", "bonk"
]


class SimonButton(discord.ui.Button):
    def __init__(self, label, expected_label, real):
        super().__init__(
            label=label,
            style=random.choice([
                discord.ButtonStyle.primary,
                discord.ButtonStyle.secondary,
                discord.ButtonStyle.success,
                discord.ButtonStyle.danger
            ])
        )
        self.expected_label = expected_label
        self.real = real

    async def callback(self, interaction: discord.Interaction):
        view = self.view

        if view.answered:
            return await interaction.response.send_message("too late", ephemeral=True)

        uid = interaction.user.id
        clicked_correct = self.label == self.expected_label

        if self.real and clicked_correct:
            view.cog.scores[uid] = view.cog.scores.get(uid, 0) + 1
            view.answered = True
            await interaction.response.send_message(f"{interaction.user.mention} +1")
            view.stop()

        elif (not self.real) and clicked_correct:
            view.cog.scores[uid] = view.cog.scores.get(uid, 0) - 1
            view.answered = True
            await interaction.response.send_message(f"{interaction.user.mention} -1")
            view.stop()

        else:
            view.cog.scores[uid] = view.cog.scores.get(uid, 0) - 1
            await interaction.response.send_message(f"{interaction.user.mention} -1")


class SimonButtonView(discord.ui.View):
    def __init__(self, cog, expected_label, real, timeout):
        super().__init__(timeout=timeout)
        self.cog = cog
        self.expected_label = expected_label
        self.real = real
        self.answered = False

        labels = [expected_label]

        while len(labels) < 4:
            label = random.choice(BUTTON_LABELS)
            if label not in labels:
                labels.append(label)

        random.shuffle(labels)

        for label in labels:
            self.add_item(SimonButton(label, expected_label, real))


class Simon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.running = False
        self.scores = {}

    def make_text_prompt(self, force_real=None):
        word = random.choice(WORDS)

        real = random.random() < 0.65 if force_real is None else force_real
        action = "say" if real else random.choice(FAKE_ACTIONS)
        prefix = REAL_PREFIX if real else random.choice(FAKE_PREFIXES)

        styles = [
            f"{prefix} {action} `{word}`",
            f"{prefix} {action} **{word}**",
            f"{prefix} {action} __{word}__",
            f"{prefix} {action} ||{word}||",
            f"{prefix} {action}: {word}",
            f"{prefix} {action}\n{word}",
            f"{prefix} {action} {word}",
            f"{prefix}\n{action} `{word}`"
        ]

        return random.choice(styles), word, real

    def make_button_prompt(self, force_real=None):
        expected = random.choice(BUTTON_LABELS)

        real = random.random() < 0.65 if force_real is None else force_real
        prefix = REAL_PREFIX if real else random.choice(FAKE_PREFIXES)

        fake_button_actions = [
            "press the button", "click the button", "tap the button",
            "smack the button", "press", "click", "touch"
        ]

        action = "press" if real else random.choice(fake_button_actions)

        styles = [
            f"{prefix} {action} `{expected}`",
            f"{prefix} {action} **{expected}**",
            f"{prefix} {action}: {expected}",
            f"{prefix}\n{action} `{expected}`"
        ]

        return random.choice(styles), expected, real

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

        if rounds < 1 or rounds > 100:
            return await ctx.send("Rounds must be between 1 and 100")

        if answer_time < 1 or answer_time > 60:
            return await ctx.send("Timer must be between 1 and 60 seconds")

        if round_pause < 0 or round_pause > 60:
            return await ctx.send("Break must be between 0 and 60 seconds")

        self.running = True
        self.scores = {}

        await ctx.send(
            f"Rules\n"
            f"Rounds: {rounds}\n"
            f"Answer time: {answer_time}s\n"
            f"Break: {round_pause}s\n"
            f"Only exact `Simon says` is real\n"
            f"Fake prompts punish you\n"
            f"Wrong answers lose 1 point\n"
            f"Wrong buttons lose 1 point\n"
            f"First correct answer gains 1 point\n"
            f"Starting in 7 seconds"
        )

        await asyncio.sleep(7)

        fake_streak = 0

        for round_num in range(1, rounds + 1):
            if not self.running:
                break

            await asyncio.sleep(round_pause)

            force_real = True if fake_streak >= 2 else None
            is_button_round = random.random() < 0.35

            if is_button_round:
                prompt, expected, real = self.make_button_prompt(force_real)
            else:
                prompt, expected, real = self.make_text_prompt(force_real)

            if not real:
                fake_streak += 1
            else:
                fake_streak = 0

            await ctx.send(f"Round {round_num}/{rounds}\n{prompt}")

            if is_button_round:
                view = SimonButtonView(self, expected, real, answer_time)
                await ctx.send("choose", view=view)

                await view.wait()

                if not view.answered:
                    await ctx.send("No response")

                continue

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
                    content = msg.content.strip().lower()
                    expected_clean = expected.lower()

                    if real:
                        if content == expected_clean:
                            self.scores[uid] = self.scores.get(uid, 0) + 1
                            await ctx.send(f"{msg.author.mention} +1")
                            round_ended = True
                        else:
                            self.scores[uid] = self.scores.get(uid, 0) - 1
                            await ctx.send(f"{msg.author.mention} -1")
                    else:
                        if content == expected_clean:
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
