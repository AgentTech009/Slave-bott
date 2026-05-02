from discord.ext import commands
import random
import asyncio

SIMON_CHANNEL_ID = 1500168505184485577  # ← your channel

ROUNDS = 15

PROMPTS = [
    "type `meow`","type `lebron`","type `water`","type `koni`","type `real`",
    "type `banana`","type `apple`","type `pizza`","type `hello`","type `bye`",
    "send `💀`","send `😭`","send `😂`","send `🔥`","send `🐈`",
    "send `👀`","send `😈`","send `🤨`","send `😡`","send `😎`",
    "say `i am cooked`","say `hydration is important`","say `simon is watching`",
    "say `skill issue`","say `i love discord`","say `brainrot`",
    "say `absolute cinema`","say `never cook again`","say `i need water`",
    "say `this server is cooked`","say `i have no enemies`","say `main character`",
    "say `npc moment`","say `lowkey`","say `highkey`",
    "say `this is crazy`","say `bro what`","say `no way`",
    "type `123`","type `abc`","type `xyz`",
    "type `gg`","type `ez`","type `win`","type `loss`",
    "send `❤️`","send `💔`","send `💯`","send `✨`","send `🎯`"
]

class Simon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.running = False
        self.scores = {}

    @commands.command(name="simonstart")
    async def start(self, ctx):
        if ctx.channel.id != SIMON_CHANNEL_ID:
            return

        if self.running:
            return await ctx.send("Simon already running 💀")

        self.running = True
        self.scores = {}

        await ctx.send("Simon Says started 😈 First correct reply wins each round")

        for round_num in range(1, ROUNDS + 1):
            if not self.running:
                break

            await asyncio.sleep(2)

            prompt = random.choice(PROMPTS)
            real = random.choice([True, False])

            if real:
                text = f"Simon says {prompt}"
            else:
                text = prompt

            await ctx.send(f"**Round {round_num}/{ROUNDS}**\n{text}")

            expected = prompt.replace("type `","").replace("send `","").replace("say `","").replace("`","")

            def check(msg):
                return (
                    msg.channel.id == SIMON_CHANNEL_ID
                    and not msg.author.bot
                )

            try:
                msg = await self.bot.wait_for("message", timeout=6, check=check)

                if real:
                    if msg.content.lower().strip() == expected.lower():
                        self.scores[msg.author.id] = self.scores.get(msg.author.id, 0) + 1
                        await ctx.send(f"{msg.author.mention} got it FIRST ✅ +1 point")
                    else:
                        await ctx.send(f"{msg.author.mention} wrong 💀")
                else:
                    if msg.content.lower().strip() == expected.lower():
                        await ctx.send(f"{msg.author.mention} fell for it 💀 no Simon says")
                    else:
                        await ctx.send("no one got baited 🧠")

            except asyncio.TimeoutError:
                await ctx.send("no one responded 💀")

        # 🔥 END GAME
        self.running = False

        if not self.scores:
            return await ctx.send("game ended. nobody scored 💀")

        winner_id = max(self.scores, key=self.scores.get)
        winner_score = self.scores[winner_id]

        leaderboard = "🏆 **Final Scores**\n"
        for uid, pts in sorted(self.scores.items(), key=lambda x: x[1], reverse=True):
            leaderboard += f"<@{uid}> — {pts}\n"

        await ctx.send(leaderboard)
        await ctx.send(f"👑 WINNER: <@{winner_id}> with **{winner_score} points** 😈")

    @commands.command(name="simonstop")
    async def stop(self, ctx):
        if ctx.channel.id != SIMON_CHANNEL_ID:
            return

        self.running = False
        await ctx.send("Simon stopped 🛑")

async def setup(bot):
    await bot.add_cog(Simon(bot))
