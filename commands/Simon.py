from discord.ext import commands
import discord
import random
import asyncio
import re

SIMON_CHANNEL_ID = 1500168505184485577
WINNER_ROLE_ID = None  # put role ID here or keep None

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

EMOJIS = ["👍", "👎", "🔥", "💀", "😭", "✅", "❌", "🐟", "🍕", "🍌"]

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
    def __init__(self, cog, channel, expected, real, answer_time):
        super().__init__(timeout=answer_time)
        self.cog = cog
        self.channel = channel
        self.expected = expected
        self.real = real
        self.finished = False
        self.got_any_reply = False
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

            uid = interaction.user.id

            if self.cog.alive and uid not in self.cog.alive:
                return await interaction.response.send_message("You are eliminated 💀", ephemeral=True)

            if self.finished:
                return await interaction.response.send_message("Round ended lil bro", ephemeral=True)

            self.got_any_reply = True

            if self.real:
                if label == self.expected:
                    bonus = self.cog.award_correct(uid)
                    self.finished = True

                    for item in self.children:
                        item.disabled = True

                    await interaction.response.edit_message(view=self)
                    await self.channel.send(f"{interaction.user.mention} +{bonus}")
                    self.stop()
                else:
                    self.cog.punish(uid)
                    await interaction.response.send_message("-1 wrong button 💀", ephemeral=True)
                    await self.channel.send(f"{interaction.user.mention} -1")
            else:
                self.cog.punish(uid)
                await interaction.response.send_message("-1 fake Simon bait 😭", ephemeral=True)
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
        self.join_open = False
        self.players = set()
        self.alive = set()
        self.scores = {}
        self.total_scores = {}
        self.streaks = {}
        self.memory_words = []

    def add_score(self, uid, amount):
        self.scores[uid] = self.scores.get(uid, 0) + amount
        self.total_scores[uid] = self.total_scores.get(uid, 0) + amount

    def punish(self, uid):
        self.add_score(uid, -1)
        self.streaks[uid] = 0

        if self.alive:
            self.alive.discard(uid)

    def award_correct(self, uid):
        base = 1
        self.streaks[uid] = self.streaks.get(uid, 0) + 1

        if self.streaks[uid] >= 3:
            base += 1
            self.streaks[uid] = 0

        self.add_score(uid, base)
        return base

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

    def real_or_fake(self, chance=0.58):
        real = random.random() < chance
        prefix = REAL_PREFIX if real else random.choice(FAKE_PREFIXES)
        return prefix, real

    def style_prompt(self, prefix, text):
        styles = [
            f"{prefix} {text}",
            f"**{prefix}** {text}",
            f"{prefix}\n> {text}",
            f"```{prefix} {text}```",
            f"{prefix} ||{text}||",
            f"{prefix} __{text}__",
            f"[SYSTEM] {prefix} {text}",
            f"{prefix} ~~fake~~ {text}",
            f"{prefix}\n# {text}",
            f">>> {prefix} {text}"
        ]
        return random.choice(styles)

    def make_text_round(self):
        word = random.choice(WORDS)
        prefix, real = self.real_or_fake()
        action = random.choice(ACTIONS if real else FAKE_ACTIONS)
        prompt = self.style_prompt(prefix, f"{action} `{word}`")
        return prompt, word, real

    def make_button_round(self):
        word = random.choice(BUTTON_WORDS)
        prefix, real = self.real_or_fake()
        prompt = self.style_prompt(prefix, f"press `{word}`")
        return prompt, word, real

    def make_reverse_round(self):
        word = random.choice(WORDS).lower()
        expected = word[::-1]
        prefix, real = self.real_or_fake()
        prompt = self.style_prompt(prefix, f"type `{word}` backwards")
        return prompt, expected, real

    def make_math_round(self):
        a = random.randint(2, 15)
        b = random.randint(2, 15)
        expected = str(a + b)
        prefix, real = self.real_or_fake()
        prompt = self.style_prompt(prefix, f"type `{a} + {b}`")
        return prompt, expected, real

    def make_multi_round(self):
        first = random.choice(WORDS)
        second = random.choice(WORDS)
        expected = f"{first} {second}"
        prefix, real = self.real_or_fake()
        prompt = self.style_prompt(prefix, f"type `{first}` then `{second}`")
        return prompt, expected, real

    def make_memory_round(self):
        word = random.choice(WORDS)

        if len(self.memory_words) >= 2 and random.random() < 0.6:
            expected = self.memory_words[-2]
            prefix, real = self.real_or_fake()
            prompt = self.style_prompt(prefix, "type the word from 2 real memory rounds ago")
            return prompt, expected, real

        self.memory_words.append(word)
        prefix, real = self.real_or_fake()
        prompt = self.style_prompt(prefix, f"remember `{word}` and type it")
        return prompt, word, real

    def make_silence_round(self):
        prefix, real = self.real_or_fake()
        prompt = self.style_prompt(prefix, "do NOTHING")
        return prompt, None, real

    def make_reaction_round(self):
        emoji = random.choice(EMOJIS)
        prefix, real = self.real_or_fake()
        prompt = self.style_prompt(prefix, f"react with {emoji}")
        return prompt, emoji, real

    def make_voice_round(self):
        prefix, real = self.real_or_fake()
        prompt = self.style_prompt(prefix, "join any voice channel")
        return prompt, None, real

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

    async def handle_text_like_round(self, ctx, prompt, expected, real, answer_time, round_num, rounds):
        msg = await ctx.send(f"**Round {round_num}/{rounds}**\n{prompt}")

        if random.random() < 0.18:
            await asyncio.sleep(0.7)
            fake_prompt = prompt.replace("Simon says", random.choice(FAKE_PREFIXES), 1)
            try:
                await msg.edit(content=f"**Round {round_num}/{rounds}**\n{fake_prompt}")
                real = False
            except:
                pass

        got_any_reply = False
        round_ended = False
        message_counts = {}

        def check(m):
            return m.channel.id == SIMON_CHANNEL_ID and not m.author.bot

        end_time = asyncio.get_event_loop().time() + answer_time

        while asyncio.get_event_loop().time() < end_time and not round_ended:
            try:
                remaining = end_time - asyncio.get_event_loop().time()
                msg = await self.bot.wait_for("message", timeout=remaining, check=check)
                uid = msg.author.id

                if self.alive and uid not in self.alive:
                    continue

                got_any_reply = True
                message_counts[uid] = message_counts.get(uid, 0) + 1

                if message_counts[uid] >= 5:
                    self.add_score(uid, -2)
                    await ctx.send(f"{msg.author.mention} -2 spam punishment 💀")
                    message_counts[uid] = 0

                content = msg.content.strip()

                if real:
                    if content == expected:
                        bonus = self.award_correct(uid)
                        await ctx.send(f"{msg.author.mention} +{bonus}")
                        round_ended = True
                    else:
                        self.punish(uid)
                        await ctx.send(f"{msg.author.mention} -1")
                else:
                    self.punish(uid)
                    await ctx.send(f"{msg.author.mention} -1")

                    if content == expected:
                        round_ended = True

            except asyncio.TimeoutError:
                break

        if not got_any_reply:
            await ctx.send("No response")

    async def handle_silence_round(self, ctx, prompt, expected, real, answer_time, round_num, rounds):
        await ctx.send(f"**Round {round_num}/{rounds}**\n{prompt}")

        got_any_reply = False

        def check(m):
            return m.channel.id == SIMON_CHANNEL_ID and not m.author.bot

        end_time = asyncio.get_event_loop().time() + answer_time

        while asyncio.get_event_loop().time() < end_time:
            try:
                remaining = end_time - asyncio.get_event_loop().time()
                msg = await self.bot.wait_for("message", timeout=remaining, check=check)
                uid = msg.author.id

                if self.alive and uid not in self.alive:
                    continue

                got_any_reply = True

                if real:
                    self.punish(uid)
                    await ctx.send(f"{msg.author.mention} -1 you were told to shut up 😭")
                else:
                    self.punish(uid)
                    await ctx.send(f"{msg.author.mention} -1 fake Simon bait")

            except asyncio.TimeoutError:
                break

        if not got_any_reply:
            await ctx.send("No response")

    async def handle_reaction_round(self, ctx, prompt, expected, real, answer_time, round_num, rounds):
        msg = await ctx.send(f"**Round {round_num}/{rounds}**\n{prompt}")

        for emoji in random.sample(EMOJIS, 5):
            try:
                await msg.add_reaction(emoji)
            except:
                pass

        got_any_reply = False
        round_ended = False

        def check(reaction, user):
            return (
                reaction.message.id == msg.id
                and not user.bot
            )

        end_time = asyncio.get_event_loop().time() + answer_time

        while asyncio.get_event_loop().time() < end_time and not round_ended:
            try:
                remaining = end_time - asyncio.get_event_loop().time()
                reaction, user = await self.bot.wait_for(
                    "reaction_add",
                    timeout=remaining,
                    check=check
                )

                uid = user.id

                if self.alive and uid not in self.alive:
                    continue

                got_any_reply = True
                emoji = str(reaction.emoji)

                if real:
                    if emoji == expected:
                        bonus = self.award_correct(uid)
                        await ctx.send(f"{user.mention} +{bonus}")
                        round_ended = True
                    else:
                        self.punish(uid)
                        await ctx.send(f"{user.mention} -1")
                else:
                    self.punish(uid)
                    await ctx.send(f"{user.mention} -1 fake reaction bait")

                    if emoji == expected:
                        round_ended = True

            except asyncio.TimeoutError:
                break

        if not got_any_reply:
            await ctx.send("No response")

    async def handle_voice_round(self, ctx, prompt, expected, real, answer_time, round_num, rounds):
        await ctx.send(f"**Round {round_num}/{rounds}**\n{prompt}")

        got_any_reply = False
        round_ended = False

        def check(member, before, after):
            return (
                member.guild == ctx.guild
                and not member.bot
                and before.channel is None
                and after.channel is not None
            )

        try:
            member, before, after = await self.bot.wait_for(
                "voice_state_update",
                timeout=answer_time,
                check=check
            )

            uid = member.id

            if self.alive and uid not in self.alive:
                return await ctx.send("No response")

            got_any_reply = True

            if real:
                bonus = self.award_correct(uid)
                await ctx.send(f"{member.mention} +{bonus}")
                round_ended = True
            else:
                self.punish(uid)
                await ctx.send(f"{member.mention} -1 fake VC bait 💀")

        except asyncio.TimeoutError:
            pass

        if not got_any_reply and not round_ended:
            await ctx.send("No response")

    @commands.command(name="simonjoin")
    async def simonjoin(self, ctx):
        if ctx.channel.id != SIMON_CHANNEL_ID:
            return

        if not self.join_open:
            return await ctx.send("Join is not open")

        self.players.add(ctx.author.id)
        await ctx.send(f"{ctx.author.mention} joined Simon")

    @commands.command(name="simonleave")
    async def simonleave(self, ctx):
        if ctx.channel.id != SIMON_CHANNEL_ID:
            return

        self.players.discard(ctx.author.id)
        self.alive.discard(ctx.author.id)
        await ctx.send(f"{ctx.author.mention} left Simon")

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

        sudden_death_after = await self.ask_int(ctx, "Sudden death starts after which round? `0 = off`", 0, rounds)
        if sudden_death_after is None:
            return await ctx.send("Invalid sudden death round")

        self.players = set()
        self.join_open = True

        await ctx.send("Join opened for `20 seconds`. Type `.simonjoin` to play.")
        await asyncio.sleep(20)

        self.join_open = False

        if not self.players:
            self.players.add(ctx.author.id)

        self.running = True
        self.scores = {uid: 0 for uid in self.players}
        self.streaks = {}
        self.memory_words = []
        self.alive = set()

        rules = (
            "**SIMON SAYS DELUXE RULES**\n"
            f"Rounds: `{rounds}`\n"
            f"Answer time: `{answer_time}s`\n"
            f"Break: `{round_pause}s`\n\n"
            "**Only exact `Simon says` is real.**\n"
            "`simon says`, `SIMON SAYS`, `Simon Says`, `S1mon says` are fake.\n\n"
            "**Modes:** text, buttons, reactions, reverse, math, memory, silence, VC, edit traps.\n"
            "Text is case sensitive.\n"
            "Fake Simon means do nothing.\n"
            "Wrong answer: `-1`\n"
            "Correct answer: `+1`\n"
            "Streak bonus after 3 correct: extra `+1`\n"
            "Spam 5 messages in one round: `-2`\n\n"
            f"Sudden death: `{sudden_death_after if sudden_death_after else 'off'}`\n"
            "Starting in `10 seconds`."
        )

        await self.send_rules_webhook(ctx.channel, rules)
        await asyncio.sleep(10)

        fake_streak = 0

        for round_num in range(1, rounds + 1):
            if not self.running:
                break

            if sudden_death_after and round_num == sudden_death_after:
                self.alive = set(self.players)
                await ctx.send("**SUDDEN DEATH STARTED** 💀\nWrong move = eliminated.")

            if self.alive and len(self.alive) <= 1:
                break

            await asyncio.sleep(round_pause)

            if round_num <= 3:
                round_type = random.choice(["text", "button", "reaction"])
            else:
                round_type = random.choice([
                    "text",
                    "button",
                    "reaction",
                    "reverse",
                    "math",
                    "multi",
                    "memory",
                    "silence",
                    "voice"
                ])

            if round_type == "text":
                prompt, expected, real = self.make_text_round()
            elif round_type == "button":
                prompt, expected, real = self.make_button_round()
            elif round_type == "reaction":
                prompt, expected, real = self.make_reaction_round()
            elif round_type == "reverse":
                prompt, expected, real = self.make_reverse_round()
            elif round_type == "math":
                prompt, expected, real = self.make_math_round()
            elif round_type == "multi":
                prompt, expected, real = self.make_multi_round()
            elif round_type == "memory":
                prompt, expected, real = self.make_memory_round()
            elif round_type == "silence":
                prompt, expected, real = self.make_silence_round()
            else:
                prompt, expected, real = self.make_voice_round()

            if fake_streak >= 2:
                real = True
                fake_streak = 0

                if round_type == "button":
                    expected = random.choice(BUTTON_WORDS)
                    prompt = f"{REAL_PREFIX} press `{expected}`"
                elif round_type == "reaction":
                    expected = random.choice(EMOJIS)
                    prompt = f"{REAL_PREFIX} react with {expected}"
                elif round_type == "silence":
                    prompt = f"{REAL_PREFIX} do NOTHING"
                elif round_type == "voice":
                    prompt = f"{REAL_PREFIX} join any voice channel"
                else:
                    expected = random.choice(WORDS)
                    prompt = f"{REAL_PREFIX} type `{expected}`"

            fake_streak = 0 if real else fake_streak + 1

            if round_type == "button":
                view = SimonButtonView(self, ctx.channel, expected, real, answer_time)
                msg = await ctx.send(f"**Round {round_num}/{rounds}**\n{prompt}", view=view)
                view.message = msg
                await view.wait()

                if not view.got_any_reply:
                    await ctx.send("No response")

            elif round_type == "reaction":
                await self.handle_reaction_round(ctx, prompt, expected, real, answer_time, round_num, rounds)

            elif round_type == "silence":
                await self.handle_silence_round(ctx, prompt, expected, real, answer_time, round_num, rounds)

            elif round_type == "voice":
                await self.handle_voice_round(ctx, prompt, expected, real, answer_time, round_num, rounds)

            else:
                await self.handle_text_like_round(ctx, prompt, expected, real, answer_time, round_num, rounds)

        self.running = False
        self.join_open = False

        if not self.scores:
            return await ctx.send("Game ended. No scores.")

        leaderboard = "**Final scores**\n"
        for uid, pts in sorted(self.scores.items(), key=lambda x: x[1], reverse=True):
            leaderboard += f"<@{uid}> — `{pts}`\n"

        winner_id = max(self.scores, key=self.scores.get)
        winner_score = self.scores[winner_id]

        await ctx.send(leaderboard)
        await ctx.send(f"Winner: <@{winner_id}> with `{winner_score}`")

        if WINNER_ROLE_ID:
            role = ctx.guild.get_role(WINNER_ROLE_ID)
            member = ctx.guild.get_member(winner_id)

            if role and member:
                try:
                    await member.add_roles(role, reason="Simon Says winner")
                    await ctx.send(f"{member.mention} got the winner role")
                except:
                    await ctx.send("Could not give winner role")

    @commands.command(name="simonstop")
    async def stop(self, ctx):
        if ctx.channel.id != SIMON_CHANNEL_ID:
            return

        self.running = False
        self.join_open = False
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

    @commands.command(name="simontop")
    async def simontop(self, ctx):
        if ctx.channel.id != SIMON_CHANNEL_ID:
            return

        if not self.total_scores:
            return await ctx.send("No lifetime scores yet")

        leaderboard = "**Lifetime Simon leaderboard**\n"
        for uid, pts in sorted(self.total_scores.items(), key=lambda x: x[1], reverse=True)[:10]:
            leaderboard += f"<@{uid}> — `{pts}`\n"

        await ctx.send(leaderboard)


async def setup(bot):
    await bot.add_cog(Simon(bot))
