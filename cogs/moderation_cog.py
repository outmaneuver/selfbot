import discord
from discord.ext import commands

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kick')
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        await user.kick(reason=reason)
        await ctx.send(f'Kicked {user.name} for reason: {reason}')

    @commands.command(name='ban')
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        await user.ban(reason=reason)
        await ctx.send(f'Banned {user.name} for reason: {reason}')

    @commands.command(name='masskick')
    async def mass_kick(self, ctx, users: commands.Greedy[discord.Member], *, reason=None):
        for user in users:
            await user.kick(reason=reason)
        await ctx.send(f'Kicked {len(users)} users for reason: {reason}')

    @commands.command(name='massban')
    async def mass_ban(self, ctx, users: commands.Greedy[discord.Member], *, reason=None):
        for user in users:
            await user.ban(reason=reason)
        await ctx.send(f'Banned {len(users)} users for reason: {reason}')

    @commands.command(name='kickrole')
    async def kick_role(self, ctx, role: discord.Role, *, reason=None):
        members = [member for member in ctx.guild.members if role in member.roles]
        for member in members:
            await member.kick(reason=reason)
        await ctx.send(f'Kicked {len(members)} users with role {role.name} for reason: {reason}')

    @commands.command(name='banrole')
    async def ban_role(self, ctx, role: discord.Role, *, reason=None):
        members = [member for member in ctx.guild.members if role in member.roles]
        for member in members:
            await member.ban(reason=reason)
        await ctx.send(f'Banned {len(members)} users with role {role.name} for reason: {reason}')

def setup(bot):
    bot.add_cog(ModerationCog(bot))
