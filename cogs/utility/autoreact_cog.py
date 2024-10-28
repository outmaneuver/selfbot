import discord
from discord.ext import commands
from utils.rate_limiter import RateLimiter
from utils.permissions import has_permissions_to_use_external_emojis
import asyncio

class AutoReactCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_reactions = {}
        self.rate_limiter = RateLimiter()

    @commands.command(name='react')
    @has_permissions_to_use_external_emojis()
    async def react(self, ctx, action: str, user_ids: commands.Greedy[int] = None, *emojis):
        if action.lower() not in ['enable', 'disable', 'list']:
            await ctx.send("Invalid action. Please choose 'enable', 'disable', or 'list'.")
            return

        if action.lower() == 'list':
            await self.list_reactions(ctx)
            return

        if not user_ids:
            user_ids = [ctx.author.id]

        for user_id in user_ids:
            if action.lower() == 'enable':
                await self.enable_reactions(ctx, user_id, emojis)
            elif action.lower() == 'disable':
                await self.disable_reactions(ctx, user_id)

    async def list_reactions(self, ctx):
        if self.user_reactions:
            response = "Auto-react enabled for the following users:\n"
            for user_id, emojis in self.user_reactions.items():
                response += f"User ID: {user_id}, Emojis: {', '.join(emojis)}\n"
            await ctx.send(f"```{response}```")
        else:
            await ctx.send("No users have auto-react enabled.")

    async def enable_reactions(self, ctx, user_id, emojis):
        if user_id not in self.user_reactions:
            self.user_reactions[user_id] = set()
        self.user_reactions[user_id].update(emojis)
        await ctx.send(f"Auto-react enabled for user: {user_id} with emojis: {', '.join(emojis)}")

    async def disable_reactions(self, ctx, user_id):
        if user_id in self.user_reactions:
            del self.user_reactions[user_id]
            await ctx.send(f"Auto-react disabled for user: {user_id}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id in self.user_reactions:
            for emoji in self.user_reactions[message.author.id]:
                await self.rate_limiter.wait()
                await message.add_reaction(emoji)

def setup(bot):
    bot.add_cog(AutoReactCog(bot))
