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
        kicked_users = []
        for user in users:
            await user.kick(reason=reason)
            kicked_users.append(user.name)
        await ctx.send(f'Kicked {len(kicked_users)} users for reason: {reason}')

    @commands.command(name='massban')
    async def mass_ban(self, ctx, users: commands.Greedy[discord.Member], *, reason=None):
        banned_users = []
        for user in users:
            await user.ban(reason=reason)
            banned_users.append(user.name)
        await ctx.send(f'Banned {len(banned_users)} users for reason: {reason}')

    @commands.command(name='kickrole')
    async def kick_role(self, ctx, role: discord.Role, *, reason=None):
        members = [member for member in ctx.guild.members if role in member.roles]
        kicked_members = []
        for member in members:
            await member.kick(reason=reason)
            kicked_members.append(member.name)
        await ctx.send(f'Kicked {len(kicked_members)} users with role {role.name} for reason: {reason}')

    @commands.command(name='banrole')
    async def ban_role(self, ctx, role: discord.Role, *, reason=None):
        members = [member for member in ctx.guild.members if role in member.roles]
        banned_members = []
        for member in members:
            await member.ban(reason=reason)
            banned_members.append(member.name)
        await ctx.send(f'Banned {len(banned_members)} users with role {role.name} for reason: {reason}')

def setup(bot):
    bot.add_cog(ModerationCog(bot))
