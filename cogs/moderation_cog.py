import discord
from discord.ext import commands

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _kick_or_ban(self, ctx, users, action, reason):
        action_func = getattr(users[0], action)
        affected_users = []
        for user in users:
            await action_func(reason=reason)
            affected_users.append(user.name)
        await ctx.send(f'{len(affected_users)} users have been {action}ed from the server. Reason: {reason if reason else "No reason provided"}.')

    @commands.command(name='kick')
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        await self._kick_or_ban(ctx, [user], 'kick', reason)

    @commands.command(name='ban')
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        await self._kick_or_ban(ctx, [user], 'ban', reason)

    @commands.command(name='masskick')
    async def mass_kick(self, ctx, users: commands.Greedy[discord.Member], *, reason=None):
        await self._kick_or_ban(ctx, users, 'kick', reason)

    @commands.command(name='massban')
    async def mass_ban(self, ctx, users: commands.Greedy[discord.Member], *, reason=None):
        await self._kick_or_ban(ctx, users, 'ban', reason)

    @commands.command(name='kickrole')
    async def kick_role(self, ctx, role: discord.Role, *, reason=None):
        members = [member for member in ctx.guild.members if role in member.roles]
        await self._kick_or_ban(ctx, members, 'kick', reason)

    @commands.command(name='banrole')
    async def ban_role(self, ctx, role: discord.Role, *, reason=None):
        members = [member for member in ctx.guild.members if role in member.roles]
        await self._kick_or_ban(ctx, members, 'ban', reason)

def setup(bot):
    bot.add_cog(ModerationCog(bot))
