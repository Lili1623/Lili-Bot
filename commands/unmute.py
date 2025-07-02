import discord
from discord.ext import commands

async def unmute(ctx, member: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name="muted")
    if not muted_role:
        return await ctx.send("❌ Es gibt keine Rolle namens `Muted`.")

    if muted_role not in member.roles:
        return await ctx.send(f"{member.mention} hat die `Muted`-Rolle nicht.")

    await member.remove_roles(muted_role)

    embed = discord.Embed(
        description=f"➖ {ctx.author.mention} Removed {muted_role.mention} from {member.mention}",
        color=discord.Color.from_rgb(255, 182, 193)
    )
    await ctx.send(embed=embed)

def register(bot):
    @bot.command(name="unmute")
    async def unmute_command(ctx, member: discord.Member):
        await unmute(ctx, member)