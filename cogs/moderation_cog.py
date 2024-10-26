import discord
from discord.ext import commands

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kick')
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        try:
            await user.kick(reason=reason)
            await ctx.send(f'Kicked {user.name} for reason: {reason}')
        except discord.Forbidden:
            await ctx.send(f'Failed to kick {user.name}. I do not have permission.')
        except discord.HTTPException as e:
            await ctx.send(f'Failed to kick {user.name}. An error occurred: {str(e)}')

    @commands.command(name='ban')
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        try:
            await user.ban(reason=reason)
            await ctx.send(f'Banned {user.name} for reason: {reason}')
        except discord.Forbidden:
            await ctx.send(f'Failed to ban {user.name}. I do not have permission.')
        except discord.HTTPException as e:
            await ctx.send(f'Failed to ban {user.name}. An error occurred: {str(e)}')

    @commands.command(name='masskick')
    async def mass_kick(self, ctx, users: commands.Greedy[discord.Member], *, reason=None):
        kicked_users = []
        for user in users:
            try:
                await user.kick(reason=reason)
                kicked_users.append(user.name)
            except discord.Forbidden:
                await ctx.send(f'Failed to kick {user.name}. I do not have permission.')
            except discord.HTTPException as e:
                await ctx.send(f'Failed to kick {user.name}. An error occurred: {str(e)}')
        await ctx.send(f'Kicked {len(kicked_users)} users for reason: {reason}')

    @commands.command(name='massban')
    async def mass_ban(self, ctx, users: commands.Greedy[discord.Member], *, reason=None):
        banned_users = []
        for user in users:
            try:
                await user.ban(reason=reason)
                banned_users.append(user.name)
            except discord.Forbidden:
                await ctx.send(f'Failed to ban {user.name}. I do not have permission.')
            except discord.HTTPException as e:
                await ctx.send(f'Failed to ban {user.name}. An error occurred: {str(e)}')
        await ctx.send(f'Banned {len(banned_users)} users for reason: {reason}')

    @commands.command(name='kickrole')
    async def kick_role(self, ctx, role: discord.Role, *, reason=None):
        members = [member for member in ctx.guild.members if role in member.roles]
        kicked_members = []
        for member in members:
            try:
                await member.kick(reason=reason)
                kicked_members.append(member.name)
            except discord.Forbidden:
                await ctx.send(f'Failed to kick {member.name}. I do not have permission.')
            except discord.HTTPException as e:
                await ctx.send(f'Failed to kick {member.name}. An error occurred: {str(e)}')
        await ctx.send(f'Kicked {len(kicked_members)} users with role {role.name} for reason: {reason}')

    @commands.command(name='banrole')
    async def ban_role(self, ctx, role: discord.Role, *, reason=None):
        members = [member for member in ctx.guild.members if role in member.roles]
        banned_members = []
        for member in members:
            try:
                await member.ban(reason=reason)
                banned_members.append(member.name)
            except discord.Forbidden:
                await ctx.send(f'Failed to ban {member.name}. I do not have permission.')
            except discord.HTTPException as e:
                await ctx.send(f'Failed to ban {member.name}. An error occurred: {str(e)}')
        await ctx.send(f'Banned {len(banned_members)} users with role {role.name} for reason: {reason}')

def setup(bot):
    bot.add_cog(ModerationCog(bot))
