from discord.ext import commands
import random
import difflib

FUNNY_REPLIES = [
    "that is not a command genius 💀",
    "bro invented a command 😭",
    "command not found. brain also not found.",
    "what spell did you just cast 💀",
    "nah that command is fake",
    "try again but with electricity in the brain",
    "that command does not exist lil bro",
    "server said no.",
    "wrong command final answer.",
    "bro typed ancient language",
    "invalid command but confidence was 10/10",
    "that command left the server",
    "no such command exists you absolute toaster",
    "command machine broke.",
    "you cooked nothing 🔥"
]

class Unknown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if not isinstance(error, commands.CommandNotFound):
            return

        typed = ctx.invoked_with

        commands_list = [
            cmd.name for cmd in self.bot.commands
            if not cmd.hidden
        ]

        matches = difflib.get_close_matches(
            typed,
            commands_list,
            n=1,
            cutoff=0.55
        )

        funny = random.choice(FUNNY_REPLIES)

        if matches:
            await ctx.send(f"{funny}\nDid you mean `.{matches[0]}`?")
        else:
            await ctx.send(funny)

async def setup(bot):
    await bot.add_cog(Unknown(bot))