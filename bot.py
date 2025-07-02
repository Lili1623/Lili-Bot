import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()


intents = discord.Intents.all()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=",", intents=intents)

@bot.event
async def on_ready():
    print(f" {bot.user} bot online")

@bot.command()
async def test(ctx):
    embed = discord.Embed(
        title="Lili Bot",
        description=f"❤️ Latenz: `{round(bot.latency * 1000)}ms`",
        color=discord.Color.pink()
    )
    embed.set_footer(text="bin online🌸")
    await ctx.send(embed=embed)

from commands import register
register.register(bot)

token = os.getenv("DISCORD_TOKEN")
if not token:
    raise ValueError("❌ DISCORD_TOKEN wurde nicht gefunden. Hast du die .env-Datei korrekt erstellt?")
bot.run(token)