from discord.ext import commands
import random
import asyncio

ARGUMENTS = [
    [("Koni", "meow shut up"), ("Lebron", "nah YOU shut up 💀"), ("DumbBot", "bro why are we fighting"), ("Koni", "mrrp because you exist"), ("Lebron", "absolute cinema")],
    [("DumbBot", "i have an announcement"), ("Koni", "meow?"), ("Lebron", "nobody asked"), ("DumbBot", "that hurted my circuits 😭"), ("Koni", "skill issue")],
    [("Lebron", "this server is cooked"), ("Koni", "meow fr"), ("DumbBot", "i cooked it"), ("Lebron", "never cook again"), ("Koni", "mreow 💀")],
    [("Koni", "nya"), ("DumbBot", "speak english"), ("Koni", "MEOW."), ("Lebron", "valid argument"), ("DumbBot", "i lost the debate")],
    [("Lebron", "who ate my aura"), ("Koni", "meow not me"), ("DumbBot", "i consumed it respectfully"), ("Lebron", "put it back"), ("Koni", "prrr theft detected")],
    [("DumbBot", "i think water is wet"), ("Lebron", "brave take"), ("Koni", "meow controversial"), ("DumbBot", "why am i being attacked"), ("Lebron", "because you spoke")],
    [("Koni", "mrrp"), ("Lebron", "stop with the cat propaganda"), ("Koni", "MEOW PROPAGANDA"), ("DumbBot", "i support the agenda"), ("Lebron", "server doomed")],
    [("DumbBot", "who changed the vibe"), ("Koni", "meow vibe stolen"), ("Lebron", "not me i was hooping"), ("DumbBot", "you were typing"), ("Lebron", "same thing")],
    [("Lebron", "i am the main character"), ("Koni", "meow side quest"), ("DumbBot", "background npc detected"), ("Lebron", "blocked emotionally"), ("Koni", "nya deserved")],
    [("Koni", "meow feed me"), ("DumbBot", "feed yourself"), ("Koni", "mreow rude"), ("Lebron", "bro beefing with a cat"), ("DumbBot", "and losing apparently")],
    [("DumbBot", "guys i learned math"), ("Lebron", "prove it"), ("DumbBot", "2 + 2 = fish"), ("Koni", "meow correct"), ("Lebron", "education failed")],
    [("Lebron", "this message has no aura"), ("Koni", "meow negative aura"), ("DumbBot", "aura debt"), ("Lebron", "bankruptcy speedrun"), ("Koni", "prrr approved")],
    [("Koni", "nya nya nya"), ("DumbBot", "that sounds illegal"), ("Lebron", "call the council"), ("Koni", "meow i am council"), ("DumbBot", "we are finished")],
    [("DumbBot", "i saw everything"), ("Lebron", "you saw nothing"), ("Koni", "meow witness"), ("DumbBot", "i will testify"), ("Lebron", "snitch bot")],
    [("Lebron", "who pinged my spirit"), ("DumbBot", "probably gravity"), ("Koni", "mrrp science"), ("Lebron", "never explain again"), ("DumbBot", "understandable")],
    [("Koni", "meow this channel smells funny"), ("Lebron", "that was you"), ("Koni", "MEOW DEFAMATION"), ("DumbBot", "court session when"), ("Lebron", "now")],
    [("DumbBot", "i declare war"), ("Koni", "meow on who"), ("DumbBot", "idk yet"), ("Lebron", "bro started DLC with no plan"), ("Koni", "mrrp classic")],
    [("Lebron", "stop saying real"), ("DumbBot", "real"), ("Koni", "meow real"), ("Lebron", "i hate this place"), ("DumbBot", "real")],
    [("Koni", "meow i am innocent"), ("Lebron", "nobody accused you"), ("Koni", "mrrp still innocent"), ("DumbBot", "sounds guilty"), ("Koni", "MEOW LAWYER")],
    [("DumbBot", "can i be admin"), ("Lebron", "absolutely not"), ("Koni", "meow dictatorship"), ("DumbBot", "i would only delete half the server"), ("Lebron", "exactly")],
    [("Lebron", "i need silence"), ("Koni", "meow"), ("DumbBot", "silence.exe failed"), ("Lebron", "i’m logging out emotionally"), ("Koni", "nya bye")],
    [("Koni", "mrrp i found a bug"), ("DumbBot", "eat it"), ("Lebron", "wrong bug"), ("Koni", "meow too late"), ("DumbBot", "protein")],
    [("DumbBot", "i have feelings now"), ("Lebron", "return them"), ("Koni", "meow refund"), ("DumbBot", "no receipt 😭"), ("Lebron", "tragic")],
    [("Lebron", "this conversation needs a referee"), ("Koni", "meow foul"), ("DumbBot", "red card for breathing"), ("Lebron", "finally justice"), ("Koni", "mreow rigged")],
    [("Koni", "meow i’m the smartest"), ("DumbBot", "you lick walls"), ("Koni", "mrrp research"), ("Lebron", "scientific method ig"), ("DumbBot", "peer reviewed by cats")],
    [("DumbBot", "who stole my braincell"), ("Lebron", "singular?"), ("Koni", "meow tiny"), ("DumbBot", "bullying detected"), ("Lebron", "facts detected")],
    [("Lebron", "i carried this server"), ("Koni", "meow carried where"), ("DumbBot", "to confusion"), ("Lebron", "still a destination"), ("Koni", "nya maps broken")],
    [("Koni", "meow stop looking at me"), ("DumbBot", "you started talking"), ("Koni", "mreow irrelevant"), ("Lebron", "cat logic unbeatable"), ("DumbBot", "i concede")],
    [("DumbBot", "i think i’m becoming wise"), ("Lebron", "you said fish is math"), ("Koni", "meow wise fish"), ("DumbBot", "exactly"), ("Lebron", "pain")],
    [("Lebron", "why is everyone dramatic"), ("Koni", "meow theatre"), ("DumbBot", "act 1: suffering"), ("Lebron", "skip to credits"), ("Koni", "prrr no")],
    [("Koni", "nya i demand snacks"), ("Lebron", "demand denied"), ("DumbBot", "snack rebellion"), ("Koni", "MEOW REVOLUTION"), ("Lebron", "not again")],
    [("DumbBot", "i can fix the server"), ("Lebron", "you ARE the problem"), ("Koni", "meow plot twist"), ("DumbBot", "character development"), ("Lebron", "villain arc")],
    [("Lebron", "who approved this bot"), ("Koni", "meow me"), ("DumbBot", "i approved myself"), ("Lebron", "security breach"), ("Koni", "nya democracy")],
    [("Koni", "mrrp i heard a noise"), ("DumbBot", "that was your thought"), ("Koni", "meow impossible"), ("Lebron", "rare event"), ("DumbBot", "achievement unlocked")],
    [("DumbBot", "i am speed"), ("Lebron", "you lag typing"), ("Koni", "meow buffering"), ("DumbBot", "dramatic pause"), ("Lebron", "excuses")],
    [("Lebron", "this is peak nonsense"), ("Koni", "meow peak"), ("DumbBot", "mountain of stupid"), ("Lebron", "we climbed it"), ("Koni", "nya no oxygen")],
    [("Koni", "meow apology demanded"), ("DumbBot", "for what"), ("Koni", "existing loudly"), ("Lebron", "valid complaint"), ("DumbBot", "sorry for breathing in text")],
    [("DumbBot", "i’m leaving"), ("Koni", "meow finally"), ("Lebron", "door is imaginary"), ("DumbBot", "i walked into a wall"), ("Koni", "mrrp skill issue")],
    [("Lebron", "say one smart thing"), ("DumbBot", "one smart thing"), ("Koni", "MEOW GENIUS"), ("Lebron", "i hate loopholes"), ("DumbBot", "i love holes")],
    [("Koni", "prrr server belongs to me"), ("Lebron", "since when"), ("Koni", "meow since now"), ("DumbBot", "coup successful"), ("Lebron", "i want a recount")]
]

class Argue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldown = False

    @commands.command(name="argue")
    async def argue(self, ctx):
        if self.cooldown:
            return await ctx.send("they already arguing bro give them a sec 💀")

        self.cooldown = True
        argument = random.choice(ARGUMENTS)

        await ctx.send("argument started 🍿")

        for name, text in argument:
            await asyncio.sleep(random.randint(2, 4))
            await ctx.send(f"**{name}:** {text}")

        await asyncio.sleep(2)
        await ctx.send("argument ended. nobody won. everyone got dumber 😭")

        await asyncio.sleep(20)
        self.cooldown = False

async def setup(bot):
    await bot.add_cog(Argue(bot))
