import discord
from discord.ext import commands
import random
import asyncio

GTN_CHANNEL_ID = None  # set channel ID or keep None for all channels


class GuessTheNumber(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_games = set()

    def embed(self, title, desc, color=discord.Color.blurple()):
        e = discord.Embed(title=title, description=desc, color=color)
        e.set_footer(text="Guess The Number Duel")
        return e

    async def send_embed(self, ctx, title, desc, color=discord.Color.blurple()):
        return await ctx.send(embed=self.embed(title, desc, color))

    def user_in_game(self, *users):
        return any(user.id in self.active_games for user in users)

    @commands.command(name="gtn")
    async def gtn(self, ctx, opponent: discord.Member = None):
        if GTN_CHANNEL_ID and ctx.channel.id != GTN_CHANNEL_ID:
            return

        if opponent is None:
            return await self.send_embed(
                ctx,
                "Missing Opponent",
                "Use `.gtn @user`",
                discord.Color.red()
            )

        if opponent.bot:
            return await self.send_embed(ctx, "Invalid Opponent", "You cannot play against a bot.", discord.Color.red())

        if opponent.id == ctx.author.id:
            return await self.send_embed(ctx, "Bro.", "You cannot duel yourself 💀", discord.Color.red())

        if self.user_in_game(ctx.author, opponent):
            return await self.send_embed(ctx, "Game Blocked", "One of you is already in a game.", discord.Color.red())

        self.active_games.add(ctx.author.id)
        self.active_games.add(opponent.id)

        try:
            rules = (
                f"**Players**\n"
                f"{ctx.author.mention} vs {opponent.mention}\n\n"
                "**How it works**\n"
                "1. The command runner chooses the upper limit.\n"
                "2. Both players get a DM.\n"
                "3. Each player secretly picks a number from `1` to the upper limit.\n"
                "4. The bot randomly chooses who guesses first.\n"
                "5. Players take turns guessing the other person's number.\n"
                "6. After every guess the bot says if the answer is **higher** or **lower**.\n"
                "7. First person to correctly guess the opponent's number wins.\n\n"
                "**Important**\n"
                "Reply with numbers only.\n"
                "You have `60 seconds` for setup replies."
            )

            await self.send_embed(ctx, "Guess The Number Duel", rules, discord.Color.blurple())

            await self.send_embed(
                ctx,
                "Choose Upper Limit",
                f"{ctx.author.mention}, type the upper limit now.\nExample: `100`, `1000`, `5000`",
                discord.Color.gold()
            )

            def limit_check(m):
                return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

            try:
                limit_msg = await self.bot.wait_for("message", timeout=60, check=limit_check)
                upper_limit = int(limit_msg.content.strip())
            except:
                return await self.send_embed(ctx, "Game Cancelled", "Invalid or no upper limit given.", discord.Color.red())

            if upper_limit < 2:
                return await self.send_embed(ctx, "Game Cancelled", "Upper limit must be at least `2`.", discord.Color.red())

            numbers = {}

            async def ask_secret_number(member):
                dm_embed = self.embed(
                    "Pick Your Secret Number",
                    f"Pick a number from `1` to `{upper_limit}`.\n"
                    "Reply with the number only.\n\n"
                    "Do not tell anyone. Not even your toaster.",
                    discord.Color.gold()
                )

                await member.send(embed=dm_embed)

                def dm_check(m):
                    return m.author.id == member.id and isinstance(m.channel, discord.DMChannel)

                while True:
                    msg = await self.bot.wait_for("message", timeout=60, check=dm_check)

                    try:
                        num = int(msg.content.strip())
                    except:
                        await member.send(embed=self.embed("Invalid", "Send numbers only.", discord.Color.red()))
                        continue

                    if 1 <= num <= upper_limit:
                        numbers[member.id] = num
                        await member.send(embed=self.embed("Number Saved", f"Your number `{num}` was saved.", discord.Color.green()))
                        return

                    await member.send(embed=self.embed("Invalid", f"Pick from `1` to `{upper_limit}` only.", discord.Color.red()))

            try:
                await asyncio.gather(
                    ask_secret_number(ctx.author),
                    ask_secret_number(opponent)
                )
            except discord.Forbidden:
                return await self.send_embed(
                    ctx,
                    "Game Cancelled",
                    "One of you has DMs closed. Open DMs and try again.",
                    discord.Color.red()
                )
            except asyncio.TimeoutError:
                return await self.send_embed(
                    ctx,
                    "Game Cancelled",
                    "Someone did not pick a number in time.",
                    discord.Color.red()
                )

            await self.send_embed(
                ctx,
                "Game Starting",
                f"{ctx.author.mention} {opponent.mention}\nBoth numbers are locked.\nGame starts in `10 seconds`.",
                discord.Color.green()
            )

            await asyncio.sleep(10)

            players = [ctx.author, opponent]
            current = random.choice(players)

            await self.send_embed(
                ctx,
                "Game Started",
                f"{current.mention} goes first.\nGuess your opponent's secret number.",
                discord.Color.green()
            )

            while True:
                other = opponent if current.id == ctx.author.id else ctx.author
                actual_number = numbers[other.id]

                await self.send_embed(
                    ctx,
                    "Turn",
                    f"{current.mention}, guess {other.mention}'s number.\nRange: `1` to `{upper_limit}`",
                    discord.Color.gold()
                )

                def guess_check(m):
                    return m.author.id == current.id and m.channel.id == ctx.channel.id

                try:
                    guess_msg = await self.bot.wait_for("message", timeout=60, check=guess_check)
                    guess = int(guess_msg.content.strip())
                except asyncio.TimeoutError:
                    winner = other
                    return await self.send_embed(
                        ctx,
                        "Game Over",
                        f"{current.mention} took too long.\n{winner.mention} wins by timeout.",
                        discord.Color.green()
                    )
                except:
                    await self.send_embed(ctx, "Invalid Guess", "Numbers only. Turn skipped.", discord.Color.red())
                    current = other
                    continue

                if guess < 1 or guess > upper_limit:
                    await self.send_embed(
                        ctx,
                        "Invalid Guess",
                        f"Guess must be from `1` to `{upper_limit}`.\nTurn skipped.",
                        discord.Color.red()
                    )
                    current = other
                    continue

                if guess == actual_number:
                    return await self.send_embed(
                        ctx,
                        "Winner",
                        f"{current.mention} guessed correctly.\n"
                        f"{other.mention}'s number was `{actual_number}`.\n\n"
                        f"🏆 {current.mention} wins!",
                        discord.Color.green()
                    )

                if guess < actual_number:
                    await self.send_embed(
                        ctx,
                        "Hint",
                        f"{current.mention}'s guess `{guess}` was too **low**.",
                        discord.Color.orange()
                    )
                else:
                    await self.send_embed(
                        ctx,
                        "Hint",
                        f"{current.mention}'s guess `{guess}` was too **high**.",
                        discord.Color.orange()
                    )

                current = other

        finally:
            self.active_games.discard(ctx.author.id)
            self.active_games.discard(opponent.id)


async def setup(bot):
    await bot.add_cog(GuessTheNumber(bot))
