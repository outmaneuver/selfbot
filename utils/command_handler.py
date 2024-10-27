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
import cachetools

load_dotenv()

class CacheManager:
    def __init__(self):
        self.local_cache = cachetools.LRUCache(maxsize=1000)

    def fetch_from_cache(self, key):
        return self.local_cache.get(key)

    def store_in_cache(self, key, value):
        self.local_cache[key] = value

class CommandHandler(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=os.getenv("PREFIX"), help_command=None)
        self.database_manager = DatabaseManager()
        self.cache_manager = CacheManager()
        self.load_cogs()
        self.rate_limiter = RateLimiter()

    def load_cogs(self):
        cog_directories = ['cogs.utility', 'cogs.moderation']
        for directory in cog_directories:
            cog_files = [f[:-3] for f in os.listdir(f'./{directory.replace(".", "/")}') if f.endswith('.py')]
            for cog_name in cog_files:
                cog_module = importlib.import_module(f'{directory}.{cog_name}')
                self.add_cog(cog_module.setup(self))

    async def on_ready(self):
        print(f'Logged in as {self.user}')
        await self.load_custom_activity_settings()

    async def on_member_update(self, before, after):
        if before.name != after.name or before.avatar != after.avatar or before.display_name != after.display_name:
            self.database_manager.store_user_info(after)

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
            settings = self.database_manager.retrieve_custom_activity_settings(self.user.id)
            if settings:
                await self.change_presence(activity=discord.Activity(**settings))
        except Exception as e:
            print(f"Error loading custom activity settings: {e}")

    async def save_custom_activity_settings(self, settings):
        try:
            self.database_manager.store_custom_activity_settings(self.user.id, settings)
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

    def fetch_from_cache(self, key):
        return self.cache_manager.fetch_from_cache(key)

    def store_in_cache(self, key, value):
        self.cache_manager.store_in_cache(key, value)
