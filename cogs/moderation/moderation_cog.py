import discord
from discord.ext import commands
from utils.error_handler import error_handler
from utils.permissions import has_permissions_to_send_messages

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

    @commands.command(name='moderate')
    @error_handler
    @has_permissions_to_send_messages()
    async def moderate(self, ctx, action: str, user: discord.Member, *, reason=None):
        if action.lower() not in ['kick', 'ban']:
            await ctx.send("Invalid action. Please choose 'kick' or 'ban'.")
            return
        await self._kick_or_ban(ctx, [user], action, reason)

    @commands.command(name='massmoderate')
    @error_handler
    @has_permissions_to_send_messages()
    async def mass_moderate(self, ctx, action: str, users: commands.Greedy[discord.Member], *, reason=None):
        if action.lower() not in ['kick', 'ban']:
            await ctx.send("Invalid action. Please choose 'kick' or 'ban'.")
            return
        await self._kick_or_ban(ctx, users, action, reason)

    @commands.command(name='moderaterole')
    @error_handler
    @has_permissions_to_send_messages()
    async def moderate_role(self, ctx, action: str, role: discord.Role, *, reason=None):
        if action.lower() not in ['kick', 'ban']:
            await ctx.send("Invalid action. Please choose 'kick' or 'ban'.")
            return
        members = [member for member in ctx.guild.members if role in member.roles]
        await self._kick_or_ban(ctx, members, action, reason)

def setup(bot):
    bot.add_cog(ModerationCog(bot))
