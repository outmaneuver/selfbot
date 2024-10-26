import discord
from discord.ext import commands
from utils.database import (
    connect_sqlite,
    connect_mongodb,
    connect_mysql,
    connect_redis,
    fetch_avatar_history_sqlite,
    fetch_avatar_history_mongodb,
    fetch_avatar_history_mysql,
    fetch_avatar_history_redis,
    fetch_avatar_history_cache
)

class AvatarHistoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.local_db_conn = connect_sqlite()
        self.mongo_client = connect_mongodb()
        self.mysql_conn = connect_mysql()
        self.redis_client = connect_redis()
        self.local_cache = bot.local_cache

    @commands.command(name='avhistory')
    async def avatar_history(self, ctx, user: discord.User):
        avatar_history = self.fetch_avatar_history(user.id)
        if avatar_history:
            await ctx.send(f"Here's the avatar history for {user.name}: {', '.join(avatar_history)}")
        else:
            await ctx.send(f"Sorry, I couldn't find any avatar history for {user.name}.")

    def fetch_avatar_history(self, user_id):
        avatar_history = []
        if self.redis_client:
            avatar_history.extend(fetch_avatar_history_redis(self.redis_client, user_id))
        else:
            avatar_history.extend(fetch_avatar_history_cache(self.local_cache, user_id))
        if self.local_db_conn:
            avatar_history.extend(fetch_avatar_history_sqlite(self.local_db_conn, user_id))
        if self.mongo_client:
            avatar_history.extend(fetch_avatar_history_mongodb(self.mongo_client, user_id))
        if self.mysql_conn:
            avatar_history.extend(fetch_avatar_history_mysql(self.mysql_conn, user_id))
        return avatar_history

def setup(bot):
    bot.add_cog(AvatarHistoryCog(bot))
