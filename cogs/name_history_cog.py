import discord
from discord.ext import commands
from utils.database import (
    connect_sqlite,
    connect_mongodb,
    connect_mysql,
    connect_redis,
    fetch_name_history_sqlite,
    fetch_name_history_mongodb,
    fetch_name_history_mysql,
    fetch_name_history_redis
)

class NameHistoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.local_db_conn = connect_sqlite()
        self.mongo_client = connect_mongodb()
        self.mysql_conn = connect_mysql()
        self.redis_client = connect_redis()

    @commands.command(name='namehistory')
    async def name_history(self, ctx, user: discord.User):
        name_history = self.fetch_name_history(user.id)
        if name_history:
            await ctx.send(f"Here's the name history for {user.name}: {', '.join(name_history)}")
        else:
            await ctx.send(f"Sorry, I couldn't find any name history for {user.name}.")

    def fetch_name_history(self, user_id):
        name_history = []
        if self.local_db_conn:
            name_history.extend(fetch_name_history_sqlite(self.local_db_conn, user_id))
        if self.mongo_client:
            name_history.extend(fetch_name_history_mongodb(self.mongo_client, user_id))
        if self.mysql_conn:
            name_history.extend(fetch_name_history_mysql(self.mysql_conn, user_id))
        if self.redis_client:
            name_history.extend(fetch_name_history_redis(self.redis_client, user_id))
        return name_history

def setup(bot):
    bot.add_cog(NameHistoryCog(bot))
