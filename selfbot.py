import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import importlib
from utils.database import determine_database, store_custom_activity_settings, retrieve_custom_activity_settings
from utils.user_info import store_user_info
from utils.rate_limiter import RateLimiter
import asyncio
import time

load_dotenv()

class SelfBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=os.getenv("PREFIX"))
        self.local_db_conn, self.mongo_client, self.mysql_conn, self.redis_client = determine_database()
        self.load_cogs()
        self.rate_limiter = RateLimiter()

    def load_cogs(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                cog_name = filename[:-3]
                cog_module = importlib.import_module(f'cogs.{cog_name}')
                self.add_cog(cog_module.setup(self))

    async def on_ready(self):
        print(f'Logged in as {self.user}')
        await self.load_custom_activity_settings()

    async def on_member_update(self, before, after):
        if before.name != after.name or before.avatar != after.avatar or before.display_name != after.display_name:
            store_user_info(after, self.local_db_conn, self.mongo_client, self.mysql_conn, self.redis_client)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Sorry, I didn't understand that command.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("It looks like you're missing a required argument.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("There was an issue with one of the arguments you provided.")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("There was an error while executing the command.")
        else:
            await ctx.send("An unexpected error occurred. Please try again later.")

    async def load_custom_activity_settings(self):
        try:
            settings = retrieve_custom_activity_settings(self.user.id, self.local_db_conn, self.mongo_client, self.mysql_conn, self.redis_client)
            if settings:
                await self.change_presence(activity=discord.Activity(**settings))
        except Exception as e:
            print(f"Error loading custom activity settings: {e}")

    async def save_custom_activity_settings(self, settings):
        try:
            store_custom_activity_settings(self.user.id, settings, self.local_db_conn, self.mongo_client, self.mysql_conn, self.redis_client)
        except Exception as e:
            print(f"Error saving custom activity settings: {e}")

    async def api_call(self, *args, **kwargs):
        await self.rate_limiter.wait()
        try:
            response = await super().api_call(*args, **kwargs)
            if response.status == 429:
                retry_after = response.headers.get("Retry-After")
                if retry_after:
                    self.rate_limiter.update_rate_limit(float(retry_after))
            return response
        except Exception as e:
            print(f"Error making API call: {e}")
            raise

if __name__ == "__main__":
    bot = SelfBot()
    bot.run(os.getenv("TOKEN"))
