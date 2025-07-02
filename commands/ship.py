import discord
from discord.ext import commands
import random
import time
import requests
from io import BytesIO
from PIL import Image

# Zwischenspeicher für 24h: (user1_id, user2_id): (percent, timestamp)
love_cache = {}

def register(bot):
    @bot.command()
    async def ship(ctx, user1: discord.Member = None, user2: discord.Member = None):
        if not user1 and not user2:
            return await ctx.send("❤️ Wen liebst du denn? Bitte markiere mindestens eine Person!")

        # Wenn nur eine Person angegeben ist, nimm den Autor als Gegenstück
        if user1 and not user2:
            user2 = user1
            user1 = ctx.author
        elif not user1 and user2:
            user1 = ctx.author

        # Immer gleiche Reihenfolge für das Paar (A, B) oder (B, A)
        pair = tuple(sorted((user1.id, user2.id)))
        now = time.time()

        # Prozentwert aus Cache oder neu berechnen
        if pair in love_cache:
            percent, timestamp = love_cache[pair]
            if now - timestamp >= 86400:
                percent = random.randint(0, 100)
                love_cache[pair] = (percent, now)
        else:
            percent = random.randint(0, 100)
            love_cache[pair] = (percent, now)

        # Emoji nach Prozent
        if percent <= 9:
            emoji = "🖤"
        elif percent <= 29:
            emoji = "💔"
        elif percent <= 59:
            emoji = "💞"
        elif percent <= 84:
            emoji = "💘"
        else:
            emoji = "💖"

        # Beschreibungstext
        if user1.id == user2.id:
            text = f"{user1.mention} liebt sich selbst zu **{percent}%** {emoji}"
        else:
            text = f"{user1.mention} & {user2.mention} haben eine Liebes-Kompatibilität von **{percent}%** {emoji}"

        embed = discord.Embed(
            title="🔮 Love Ship",
            description=text,
            color=discord.Color.from_rgb(255, 182, 193)  # bleibt wie bei knife
        )
        embed.set_footer(text=f"{ctx.author.display_name}")

        # Avatare kombinieren
        try:
            avatar1_url = user1.display_avatar.replace(size=128).url
            avatar2_url = user2.display_avatar.replace(size=128).url

            avatar1 = Image.open(BytesIO(requests.get(avatar1_url).content)).convert("RGBA")
            avatar2 = Image.open(BytesIO(requests.get(avatar2_url).content)).convert("RGBA")

            combined = Image.new("RGBA", (256, 128))
            combined.paste(avatar1, (0, 0))
            combined.paste(avatar2, (128, 0))

            buffer = BytesIO()
            combined.save(buffer, format="PNG")
            buffer.seek(0)

            file = discord.File(buffer, filename="ship.png")
            embed.set_image(url="attachment://ship.png")
            await ctx.send(embed=embed, file=file)
        except Exception as e:
            # Fallback ohne Bild
            await ctx.send(embed=embed)