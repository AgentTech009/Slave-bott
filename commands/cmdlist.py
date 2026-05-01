from discord.ext import commands
import discord

PAGES = [
    {
        "title": "📌 Basic Commands",
        "commands": [
            ("`.ping`", "Checks if bot is alive"),
            ("`.test`", "Simple test command"),
            ("`.reload`", "Reloads all command files"),
            ("`.cmdlist`", "Shows this clean command menu"),
            ("`.ask [question]`", "Ask AI a question"),
            ("`.calc [expression]`", "Simple calculator"),
            ("`.howlong`", "Shows time since July 18 2025"),
            ("`.sleeptime 11:00PM 9:30AM`", "Calculates sleep duration"),
        ]
    },
    {
        "title": "🛠️ Server Commands",
        "commands": [
            ("`.create [name]`", "Creates a channel in current category"),
            ("`.rn [new name]`", "Renames current channel"),
            ("`.dlt`", "Deletes current channel"),
            ("`.purge [number]`", "Deletes given number of messages"),
            ("`.kick @user [reason]`", "Kicks a user"),
            ("`.mute @user`", "Timeouts user for 30 seconds"),
            ("`.nick @user [name]`", "Changes nickname"),
        ]
    },
    {
        "title": "🎭 Role Commands",
        "commands": [
            ("`.crole [name] [color]`", "Creates a role with color word"),
            ("`.grole @user @role`", "Gives role to user"),
            ("`.rrole @user @role`", "Removes role from user"),
        ]
    },
    {
        "title": "💬 Response / AI / Chat",
        "commands": [
            ("`.respondto [trigger] [reply]`", "Creates custom auto response"),
            ("`.delresponse [trigger]`", "Deletes custom response"),
            ("`.responses`", "Lists saved responses"),
            ("`.setdumbbot`", "Enables dumb AI in current channel"),
            ("`.offdumbbot`", "Disables dumb AI"),
        ]
    },
    {
        "title": "🎮 Fun Commands",
        "commands": [
            ("`.rps @user`", "Rock paper scissors with buttons"),
            ("`.ttt @user`", "Button tic tac toe"),
            ("`.remind [time] [reason]`", "Sets reminder like 10m or 2h"),
        ]
    },
    {
        "title": "💀 Chaos Channel Modes",
        "commands": [
            ("`.setlebron`", "Bot replies lebron to every message"),
            ("`.offlebron`", "Turns off lebron mode"),
            ("`.setrandomreply`", "Randomly replies to old messages"),
            ("`.offrandomreply`", "Turns off random replies"),
            ("`.setkoni`", "Koni cat webhook replies meows"),
            ("`.offkoni`", "Turns off Koni"),
        ]
    },
    {
        "title": "🔒 Slash Commands",
        "commands": [
            ("`/dm user`", "Opens private DM box with modal"),
        ]
    }
]

class CmdListView(discord.ui.View):
    def __init__(self, author):
        super().__init__(timeout=120)
        self.author = author
        self.page = 0

    def make_embed(self):
        data = PAGES[self.page]

        embed = discord.Embed(
            title=data["title"],
            description=f"Page `{self.page + 1}/{len(PAGES)}`",
            color=discord.Color.blurple()
        )

        for cmd, desc in data["commands"]:
            embed.add_field(
                name=cmd,
                value=desc,
                inline=False
            )

        embed.set_footer(text="Use the buttons below to switch pages")
        return embed

    async def interaction_check(self, interaction):
        if interaction.user != self.author:
            await interaction.response.send_message("Not your menu 💀", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="⬅️ Back", style=discord.ButtonStyle.secondary)
    async def back(self, interaction, button):
        self.page -= 1
        if self.page < 0:
            self.page = len(PAGES) - 1

        await interaction.response.edit_message(embed=self.make_embed(), view=self)

    @discord.ui.button(label="➡️ Next", style=discord.ButtonStyle.primary)
    async def next(self, interaction, button):
        self.page += 1
        if self.page >= len(PAGES):
            self.page = 0

        await interaction.response.edit_message(embed=self.make_embed(), view=self)


class CmdList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="cmdlist")
    async def cmdlist(self, ctx):
        view = CmdListView(ctx.author)
        await ctx.send(embed=view.make_embed(), view=view)

async def setup(bot):
    await bot.add_cog(CmdList(bot))