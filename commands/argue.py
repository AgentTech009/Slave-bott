from discord.ext import commands
import discord
import random
import asyncio

KONI_AVATAR = "https://cdn.discordapp.com/attachments/1500100689924194326/1500100763815252079/IMG-20260421-WA0051-1.jpg"
LEBRON_AVATAR = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/LeBron_James_at_the_2022_NBA_All-Star_Game.jpg/320px-LeBron_James_at_the_2022_NBA_All-Star_Game.jpg"
DUMBBOT_AVATAR = "https://cdn-icons-png.flaticon.com/512/4712/4712035.png"

BOT_PROFILES = {
"Koni": KONI_AVATAR,
"Lebron": LEBRON_AVATAR,
"DumbBot": DUMBBOT_AVATAR
}

ARGUMENTS = [
    [("DumbBot", "i think i’m becoming wise"), ("Lebron", "you said fish is math"), ("Koni", "meow wise fish"), ("DumbBot", "exactly"), ("Lebron", "pain")],
    [("Koni", "meow shut up"), ("Lebron", "nah YOU shut up"), ("DumbBot", "bro why are we fighting"), ("Koni", "mrrp because you exist"), ("Lebron", "absolute cinema")],
    [("Lebron", "this server is cooked"), ("Koni", "meow fr"), ("DumbBot", "i cooked it"), ("Lebron", "never cook again"), ("Koni", "mreow")],
    [("Koni", "nya"), ("DumbBot", "speak english"), ("Koni", "MEOW."), ("Lebron", "valid argument"), ("DumbBot", "i lost the debate")],
    [("Lebron", "who ate my aura"), ("Koni", "not me"), ("DumbBot", "i consumed it respectfully"), ("Lebron", "put it back"), ("Koni", "theft detected")],
    [("DumbBot", "water is wet"), ("Lebron", "brave take"), ("Koni", "controversial"), ("DumbBot", "why am i being attacked"), ("Lebron", "because you spoke")],
    [("Koni", "mrrp"), ("Lebron", "stop with the cat propaganda"), ("Koni", "MEOW PROPAGANDA"), ("DumbBot", "i support the agenda"), ("Lebron", "server doomed")],
    [("DumbBot", "who changed the vibe"), ("Koni", "vibe stolen"), ("Lebron", "not me i was hooping"), ("DumbBot", "you were typing"), ("Lebron", "same thing")],
    [("Lebron", "i am the main character"), ("Koni", "side quest"), ("DumbBot", "background npc detected"), ("Lebron", "blocked emotionally"), ("Koni", "deserved")],
    [("Koni", "feed me"), ("DumbBot", "feed yourself"), ("Koni", "rude"), ("Lebron", "bro beefing with a cat"), ("DumbBot", "and losing apparently")],
    [("DumbBot", "guys i learned math"), ("Lebron", "prove it"), ("DumbBot", "2 plus 2 equals fish"), ("Koni", "correct"), ("Lebron", "education failed")],
    [("Lebron", "this message has no aura"), ("Koni", "negative aura"), ("DumbBot", "aura debt"), ("Lebron", "bankruptcy speedrun"), ("Koni", "approved")],
    [("Koni", "nya nya nya"), ("DumbBot", "that sounds illegal"), ("Lebron", "call the council"), ("Koni", "i am council"), ("DumbBot", "we are finished")],
    [("DumbBot", "i saw everything"), ("Lebron", "you saw nothing"), ("Koni", "witness"), ("DumbBot", "i will testify"), ("Lebron", "snitch bot")],
    [("Lebron", "who pinged my spirit"), ("DumbBot", "probably gravity"), ("Koni", "science"), ("Lebron", "never explain again"), ("DumbBot", "understandable")],
    [("Koni", "this channel smells funny"), ("Lebron", "that was you"), ("Koni", "DEFAMATION"), ("DumbBot", "court session when"), ("Lebron", "now")],
    [("DumbBot", "i declare war"), ("Koni", "on who"), ("DumbBot", "idk yet"), ("Lebron", "bro started DLC with no plan"), ("Koni", "classic")],
    [("Lebron", "stop saying real"), ("DumbBot", "real"), ("Koni", "real"), ("Lebron", "i hate this place"), ("DumbBot", "real")],
    [("Koni", "i am innocent"), ("Lebron", "nobody accused you"), ("Koni", "still innocent"), ("DumbBot", "sounds guilty"), ("Koni", "LAWYER")],
    [("DumbBot", "can i be admin"), ("Lebron", "absolutely not"), ("Koni", "dictatorship"), ("DumbBot", "i would only delete half the server"), ("Lebron", "exactly")],
    [("Lebron", "i need silence"), ("Koni", "meow"), ("DumbBot", "silence failed"), ("Lebron", "i’m logging out emotionally"), ("Koni", "bye")],
    [("Koni", "i found a bug"), ("DumbBot", "eat it"), ("Lebron", "wrong bug"), ("Koni", "too late"), ("DumbBot", "protein")],
    [("DumbBot", "i have feelings now"), ("Lebron", "return them"), ("Koni", "refund"), ("DumbBot", "no receipt"), ("Lebron", "tragic")],
    [("Lebron", "this needs a referee"), ("Koni", "foul"), ("DumbBot", "red card for breathing"), ("Lebron", "finally justice"), ("Koni", "rigged")],
    [("Koni", "i’m the smartest"), ("DumbBot", "you lick walls"), ("Koni", "research"), ("Lebron", "scientific method ig"), ("DumbBot", "peer reviewed by cats")],
    [("DumbBot", "who stole my braincell"), ("Lebron", "singular?"), ("Koni", "tiny"), ("DumbBot", "bullying detected"), ("Lebron", "facts detected")],
    [("Lebron", "i carried this server"), ("Koni", "carried where"), ("DumbBot", "to confusion"), ("Lebron", "still a destination"), ("Koni", "maps broken")],
    [("Koni", "stop looking at me"), ("DumbBot", "you started talking"), ("Koni", "irrelevant"), ("Lebron", "cat logic unbeatable"), ("DumbBot", "i concede")],
    [("DumbBot", "i’m becoming wise"), ("Lebron", "you said fish is math"), ("Koni", "wise fish"), ("DumbBot", "exactly"), ("Lebron", "pain again")],
    [("Lebron", "why is everyone dramatic"), ("Koni", "theatre"), ("DumbBot", "act one suffering"), ("Lebron", "skip to credits"), ("Koni", "no")],
    [("Koni", "i demand snacks"), ("Lebron", "demand denied"), ("DumbBot", "snack rebellion"), ("Koni", "REVOLUTION"), ("Lebron", "not again")],
    [("DumbBot", "i can fix the server"), ("Lebron", "you are the problem"), ("Koni", "plot twist"), ("DumbBot", "character development"), ("Lebron", "villain arc")],
    [("Lebron", "who approved this bot"), ("Koni", "me"), ("DumbBot", "i approved myself"), ("Lebron", "security breach"), ("Koni", "democracy")],
    [("Koni", "i heard a noise"), ("DumbBot", "that was your thought"), ("Koni", "impossible"), ("Lebron", "rare event"), ("DumbBot", "achievement unlocked")],
    [("DumbBot", "i am speed"), ("Lebron", "you lag typing"), ("Koni", "buffering"), ("DumbBot", "dramatic pause"), ("Lebron", "excuses")],
    [("Lebron", "this is peak nonsense"), ("Koni", "peak"), ("DumbBot", "mountain of stupid"), ("Lebron", "we climbed it"), ("Koni", "no oxygen")],
    [("Koni", "apology demanded"), ("DumbBot", "for what"), ("Koni", "existing loudly"), ("Lebron", "valid complaint"), ("DumbBot", "sorry for breathing in text")],
    [("DumbBot", "i’m leaving"), ("Koni", "finally"), ("Lebron", "door is imaginary"), ("DumbBot", "i walked into a wall"), ("Koni", "skill issue")],
    [("Lebron", "say one smart thing"), ("DumbBot", "one smart thing"), ("Koni", "GENIUS"), ("Lebron", "i hate loopholes"), ("DumbBot", "i love holes")],
    [("Koni", "server belongs to me"), ("Lebron", "since when"), ("Koni", "since now"), ("DumbBot", "coup successful"), ("Lebron", "i want a recount")]
]

class Argue(commands.Cog):
def init(self, bot):
self.bot = bot
self.cooldown = False
self.webhooks = {}

async def get_or_create_webhook(self, channel, name):  
    cache_key = f"{channel.id}-{name}"  

    if cache_key in self.webhooks:  
        return self.webhooks[cache_key]  

    existing_webhooks = await channel.webhooks()  

    for webhook in existing_webhooks:  
        if webhook.name == name:  
            self.webhooks[cache_key] = webhook  
            return webhook  

    new_webhook = await channel.create_webhook(name=name)  
    self.webhooks[cache_key] = new_webhook  
    return new_webhook  

async def send_webhook_message(self, channel, name, text):  
    avatar_url = BOT_PROFILES.get(name)  

    webhook = await self.get_or_create_webhook(channel, name)  

    await webhook.send(  
        content=text,  
        username=name,  
        avatar_url=avatar_url,  
        allowed_mentions=discord.AllowedMentions.none(),  
        wait=True  
    )  

@commands.command(name="argue")  
async def argue(self, ctx):  
    if self.cooldown:  
        return await ctx.send("they already arguing bro give them a sec 💀")  

    self.cooldown = True  

    try:  
        await ctx.send("argument started 🍿")  

        argument = random.choice(ARGUMENTS)  

        for name, text in argument:  
            await asyncio.sleep(random.randint(2, 4))  
            await self.send_webhook_message(ctx.channel, name, text)  

        await asyncio.sleep(2)  
        await ctx.send("argument ended. nobody won. everyone got dumber 😭")  

    except discord.Forbidden:  
        await ctx.send("I need **Manage Webhooks** permission 💀")  

    except Exception as e:  
        await ctx.send(f"Argue error: `{e}`")  

    finally:  
        await asyncio.sleep(20)  
        self.cooldown = False

async def setup(bot):
await bot.add_cog(Argue(bot))
