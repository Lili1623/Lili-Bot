import discord
from discord.ext import commands
import asyncio

def register(bot):
    @bot.command()
    async def mute(ctx, member: discord.Member, duration: str):
        muted_role = discord.utils.get(ctx.guild.roles, name="muted")
        if not muted_role:
            return await ctx.send("❌ Es gibt keine Rolle namens `Muted`.")

        await member.add_roles(muted_role)

        embed = discord.Embed(
            description=f"➕ {ctx.author.mention} Added {muted_role.mention} to {member.mention}",
            color=discord.Color.from_rgb(255, 182, 193)  # hellrosa
        )
        await ctx.send(embed=embed)

        time_multipliers = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        try:
            seconds = int(duration[:-1]) * time_multipliers[duration[-1]]
        except:
            return await ctx.send("❌ Ungültige Dauer. Nutze z.B. `5m`, `1h`, `1d` ...")

        await asyncio.sleep(seconds)
        await member.remove_roles(muted_role)

        unmute_embed = discord.Embed(
            description=f"➖ {ctx.author.mention} Removed {muted_role.mention} from {member.mention}",
            color=discord.Color.from_rgb(255, 182, 193)  # hellrosa
        )
        await ctx.send(embed=unmute_embed)