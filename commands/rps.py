from discord.ext import commands
import discord

class RPSView(discord.ui.View):
    def __init__(self, player):
        super().__init__(timeout=60)
        self.player = player
        self.choice = None

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user != self.player:
            await interaction.response.send_message("Not your game 😭", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Rock", style=discord.ButtonStyle.primary)
    async def rock(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.choice = "rock"
        await interaction.response.send_message("You chose Rock 🪨", ephemeral=True)
        self.stop()

    @discord.ui.button(label="Paper", style=discord.ButtonStyle.success)
    async def paper(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.choice = "paper"
        await interaction.response.send_message("You chose Paper 📄", ephemeral=True)
        self.stop()

    @discord.ui.button(label="Scissors", style=discord.ButtonStyle.danger)
    async def scissors(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.choice = "scissors"
        await interaction.response.send_message("You chose Scissors ✂️", ephemeral=True)
        self.stop()


class RPS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_winner(self, p1, c1, p2, c2):
        if c1 == c2:
            return None

        if (
            (c1 == "rock" and c2 == "scissors") or
            (c1 == "paper" and c2 == "rock") or
            (c1 == "scissors" and c2 == "paper")
        ):
            return p1
        else:
            return p2

    @commands.command(name="rps")
    async def rps(self, ctx, opponent: discord.Member):
        p1 = ctx.author
        p2 = opponent

        await ctx.send(f"{p1.mention} choose your move 👇")
        view1 = RPSView(p1)
        msg1 = await ctx.send("Pick:", view=view1)
        await view1.wait()

        if not view1.choice:
            return await ctx.send("Game cancelled (timeout)")

        await msg1.delete()

        await ctx.send(f"{p2.mention} choose your move 👇")
        view2 = RPSView(p2)
        msg2 = await ctx.send("Pick:", view=view2)
        await view2.wait()

        if not view2.choice:
            return await ctx.send("Game cancelled (timeout)")

        await msg2.delete()

        winner = self.get_winner(p1, view1.choice, p2, view2.choice)

        if winner is None:
            result = "It's a tie 🤝"
        else:
            result = f"{winner.mention} wins 😏"

        await ctx.send(
            f"{p1.mention} chose **{view1.choice}**\n"
            f"{p2.mention} chose **{view2.choice}**\n\n"
            f"{result}"
        )

async def setup(bot):
    await bot.add_cog(RPS(bot))