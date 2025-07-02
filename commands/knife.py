import discord
from discord.ext import commands
import random
import time

self_stabs = {}
death_cooldowns = {}  # user_id: timestamp (Sekunden)

def get_battery_emoji(stabs):
    if stabs >= 4:
        return "🪫"
    elif stabs == 3:
        return "🔋"
    elif stabs == 2:
        return "🔋🔋"
    elif stabs == 1:
        return "🔋🔋🔋"
    else:
        return "🔋🔋🔋🔋"

def register(bot):
    @bot.command()
    async def knife(ctx, target: discord.Member = None):
        if not target:
            return await ctx.send("❗ Bitte markiere jemanden!")

        emojis = ["🔪", "🗡️", "⚔️", "🪓", "🪚", "🥷", "💉", "💥", "🩸"]
        emoji = random.choice(emojis)

        if target.id == ctx.author.id:
            user_id = ctx.author.id
            now = time.time()

            # Check ob user "tot" ist und cooldown aktiv
            if user_id in death_cooldowns:
                cooldown_end = death_cooldowns[user_id]
                if now < cooldown_end:
                    remaining = int((cooldown_end - now) // 60)
                    return await ctx.send(f"👻 Du bist noch tot, {ctx.author.mention}..\nWarte noch **{remaining} Minuten** zur Wiederbelebung.")
                else:
                    # Cooldown abgelaufen → reset
                    self_stabs[user_id] = 0
                    del death_cooldowns[user_id]

            self_stabs[user_id] = self_stabs.get(user_id, 0) + 1
            battery = get_battery_emoji(self_stabs[user_id])
            if self_stabs[user_id] >= 4:
                death_cooldowns[user_id] = now + 60 * 60  # 1 Stunde Cooldown
                text = f"{ctx.author.mention} hat sich endgültig selbst umgebracht. 💀\nDer Server schweigt.\n"
            else:
                text = f"{ctx.author.mention} hat sich **selbst** abgestochen! 😵\nEnergie: {battery}"
        else:
            texts = [
                "{} hat {} heimlich abgestochen!",
                "{} hat {} in einer Gasse überfallen!",
                "{} hat {} einen tödlichen Stich verpasst!",
                "{} hat {} mit einem Ninja-Move eliminiert!",
                "{} hat {} brutal aus dem Weg geräumt!",
                "{} hat {} eiskalt erwischt!",
                "{} hat {} messerscharf erledigt!",
                "{} hat {} mit Stil ins Jenseits befördert!",
                "{} hat {} mit einem Kartoffelschäler attackiert!",
                "{} hat {} hinterrücks abgestochen wie in einem Mafia-Film!",
                "{} hat {} auf offener Straße herausgefordert und besiegt!",
                "{} hat {} mit einem Lächeln auf den Lippen erstochen!",
                "{} hat {} mit einer Rose in der Hand eliminiert – poetisch!",
                "{} hat {} mitten in der Nacht lautlos erledigt.",
                "{} hat {} mit einer Rakete verwechselt und ausgelöscht! 💥",
                "{} hat {} beim Frühstück abgestochen. Guten Morgen!",
                "{} hat {} direkt vor allen erledigt – keine Gnade!",
                "{} hat {} beim AFK-Sein aus dem Leben entfernt!",
                "{} hat {} im Schlaf attackiert – böse, aber effektiv.",
                "{} hat {} mit einem gezielten Stich ins Meme-Herz getroffen!",
                "{} hat {} mit einem Superschwert durchbohrt wie in Anime!"
            ]
            text = random.choice(texts).format(ctx.author.mention, target.mention)

        embed = discord.Embed(
            title=f"{emoji} Angriff!",
            description=text,
            color=discord.Color(0xFFB6C1)  # Helles Rosa
        )

        await ctx.send(embed=embed)
        