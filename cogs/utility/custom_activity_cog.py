import discord
from discord.ext import commands
from utils.error_handler import error_handler
from utils.permissions import has_permissions_to_send_messages

class CustomActivityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def create_activity(self, activity_type, activity_name):
        if activity_type.lower() == 'playing':
            return discord.Game(name=activity_name)
        elif activity_type.lower() == 'streaming':
            return discord.Streaming(name=activity_name, url='https://twitch.tv/streamer')
        elif activity_type.lower() == 'listening':
            return discord.Activity(type=discord.ActivityType.listening, name=activity_name)
        elif activity_type.lower() == 'watching':
            return discord.Activity(type=discord.ActivityType.watching, name=activity_name)
        elif activity_type.lower() == 'custom':
            return discord.Activity(type=discord.ActivityType.custom, name=activity_name)
        else:
            return None

    @commands.command(name='setactivity')
    @error_handler
    @has_permissions_to_send_messages()
    async def set_activity(self, ctx, activity_type: str, activity_name: str = None):
        activity = self.create_activity(activity_type, activity_name)
        if activity is None:
            await ctx.send("Invalid activity type. Please choose from playing, streaming, listening, watching, or custom.")
            return

        await self.bot.change_presence(activity=activity)
        await ctx.send(f"Activity set to {activity_type} {activity_name}")

    @commands.command(name='clearactivity')
    @error_handler
    @has_permissions_to_send_messages()
    async def clear_activity(self, ctx):
        await self.bot.change_presence(activity=None)
        await ctx.send("Activity cleared")

def setup(bot):
    bot.add_cog(CustomActivityCog(bot))
