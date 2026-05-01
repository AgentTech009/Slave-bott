from discord.ext import commands
import discord

class TTTButton(discord.ui.Button):
    def __init__(self, index):
        super().__init__(
            label=str(index + 1),
            style=discord.ButtonStyle.secondary,
            row=index // 3
        )
        self.index = index

    async def callback(self, interaction: discord.Interaction):
        view = self.view
        await view.make_move(interaction, self.index)


class TTTView(discord.ui.View):
    def __init__(self, player1, player2):
        super().__init__(timeout=120)
        self.players = [player1, player2]
        self.turn = 0
        self.board = [""] * 9
        self.message = None

        for i in range(9):
            self.add_item(TTTButton(i))

    def check_winner(self):
        wins = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]

        for a, b, c in wins:
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]

        if all(self.board):
            return "draw"

        return None

    async def make_move(self, interaction, index):
        current_player = self.players[self.turn]

        if interaction.user != current_player:
            return await interaction.response.send_message("Not your turn 😭", ephemeral=True)

        if self.board[index]:
            return await interaction.response.send_message("That spot is taken 💀", ephemeral=True)

        mark = "X" if self.turn == 0 else "O"
        self.board[index] = mark

        button = self.children[index]
        button.label = mark
        button.disabled = True
        button.style = discord.ButtonStyle.danger if mark == "X" else discord.ButtonStyle.success

        result = self.check_winner()

        if result == "draw":
            for item in self.children:
                item.disabled = True

            await interaction.response.edit_message(
                content="It is a draw 🤝",
                view=self
            )
            self.stop()
            return

        if result:
            winner = self.players[0] if result == "X" else self.players[1]

            for item in self.children:
                item.disabled = True

            await interaction.response.edit_message(
                content=f"{winner.mention} wins 🏆",
                view=self
            )
            self.stop()
            return

        self.turn = 1 - self.turn
        next_player = self.players[self.turn]

        await interaction.response.edit_message(
            content=f"{next_player.mention}'s turn",
            view=self
        )

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True

        if self.message:
            await self.message.edit(content="Tic tac toe timed out 💀", view=self)


class TTT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ttt")
    async def ttt(self, ctx, opponent: discord.Member):
        player1 = ctx.author
        player2 = opponent

        if opponent.bot:
            return await ctx.send("No bot opponents 💀")

        view = TTTView(player1, player2)

        msg = await ctx.send(
            f"Tic tac toe started\n{player1.mention} = X\n{player2.mention} = O\n\n{player1.mention}'s turn",
            view=view
        )

        view.message = msg

async def setup(bot):
    await bot.add_cog(TTT(bot))