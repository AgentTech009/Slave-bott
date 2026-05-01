import discord
from discord.ext import commands
import os
import asyncio
import traceback

GUILD_ID = 1496826379809853563  # replace with your server ID

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print("Bot online ✅")

    try:
        guild = discord.Object(id=GUILD_ID)
        synced = await bot.tree.sync(guild=guild)
        print(f"Synced {len(synced)} slash commands ✅")
    except Exception as e:
        print(f"Slash sync failed: {e}")

    print("Loaded prefix commands:")
    for cmd in bot.commands:
        print(f".{cmd.name}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    print(f"MSG: {message.content}")
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    print("COMMAND ERROR:")
    traceback.print_exception(type(error), error, error.__traceback__)

    if isinstance(error, commands.CommandNotFound):
        return

    try:
        await ctx.send(f"Error: `{error}`")
    except:
        pass

async def load_commands():
    if not os.path.exists("./commands"):
        os.makedirs("./commands")

    for file in os.listdir("./commands"):
        if file.endswith(".py") and file != "__init__.py":
            try:
                await bot.load_extension(f"commands.{file[:-3]}")
                print(f"Loaded {file}")
            except Exception as e:
                print(f"Failed to load {file}: {e}")

def get_token():
    return os.getenv("TOKEN")

async def main():
    token = get_token()

    if not token:
        print("TOKEN environment variable missing.")
        return

    async with bot:
        await load_commands()
        await bot.start(token)

try:
    asyncio.run(main())
except Exception as e:
    print(f"Crash: {e}")