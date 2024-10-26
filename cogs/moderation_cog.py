import discord
from discord.ext import commands

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kick')
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        await user.kick(reason=reason)
        await ctx.send(f'{user.name} has been kicked from the server. Reason: {reason if reason else "No reason provided"}.')

    @commands.command(name='ban')
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        await user.ban(reason=reason)
        await ctx.send(f'{user.name} has been banned from the server. Reason: {reason if reason else "No reason provided"}.')

    @commands.command(name='masskick')
    async def mass_kick(self, ctx, users: commands.Greedy[discord.Member], *, reason=None):
        kicked_users = []
        for user in users:
            await user.kick(reason=reason)
            kicked_users.append(user.name)
        await ctx.send(f'{len(kicked_users)} users have been kicked from the server. Reason: {reason if reason else "No reason provided"}.')

    @commands.command(name='massban')
    async def mass_ban(self, ctx, users: commands.Greedy[discord.Member], *, reason=None):
        banned_users = []
        for user in users:
            await user.ban(reason=reason)
            banned_users.append(user.name)
        await ctx.send(f'{len(banned_users)} users have been banned from the server. Reason: {reason if reason else "No reason provided"}.')

    @commands.command(name='kickrole')
    async def kick_role(self, ctx, role: discord.Role, *, reason=None):
        members = [member for member in ctx.guild.members if role in member.roles]
        kicked_members = []
        for member in members:
            await member.kick(reason=reason)
            kicked_members.append(member.name)
        await ctx.send(f'{len(kicked_members)} users with the role {role.name} have been kicked from the server. Reason: {reason if reason else "No reason provided"}.')

    @commands.command(name='banrole')
    async def ban_role(self, ctx, role: discord.Role, *, reason=None):
        members = [member for member in ctx.guild.members if role in member.roles]
        banned_members = []
        for member in members:
            await member.ban(reason=reason)
            banned_members.append(member.name)
        await ctx.send(f'{len(banned_members)} users with the role {role.name} have been banned from the server. Reason: {reason if reason else "No reason provided"}.')

def setup(bot):
    bot.add_cog(ModerationCog(bot))
