import discord
from discord.ext import commands
import sqlite3
import pymongo
import mysql.connector
import redis
import os

class NameHistoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.local_db_conn = sqlite3.connect(os.getenv("LOCAL_DB_PATH")) if os.getenv("LOCAL_DB_PATH") else None
        self.mongo_client = pymongo.MongoClient(os.getenv("MONGODB_URI")) if os.getenv("MONGODB_URI") else None
        self.mysql_conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        ) if os.getenv("MYSQL_HOST") else None
        self.redis_client = redis.StrictRedis(
            host=os.getenv("REDIS_HOST"),
            port=os.getenv("REDIS_PORT"),
            password=os.getenv("REDIS_PASSWORD")
        ) if os.getenv("REDIS_HOST") else None

    @commands.command(name='namehistory')
    async def name_history(self, ctx, user: discord.User):
        name_history = self.fetch_name_history(user.id)
        if name_history:
            await ctx.send(f"Name history for {user.name}: {', '.join(name_history)}")
        else:
            await ctx.send(f"No name history found for {user.name}")

    def fetch_name_history(self, user_id):
        name_history = []
        if self.local_db_conn:
            cursor = self.local_db_conn.cursor()
            cursor.execute("SELECT name FROM name_history WHERE user_id = ?", (user_id,))
            name_history.extend([row[0] for row in cursor.fetchall()])
        if self.mongo_client:
            db = self.mongo_client[os.getenv("MONGODB_DATABASE")]
            collection = db["name_history"]
            name_history.extend([doc["name"] for doc in collection.find({"user_id": user_id})])
        if self.mysql_conn:
            cursor = self.mysql_conn.cursor()
            cursor.execute("SELECT name FROM name_history WHERE user_id = %s", (user_id,))
            name_history.extend([row[0] for row in cursor.fetchall()])
        if self.redis_client:
            names = self.redis_client.lrange(f"name_history:{user_id}", 0, -1)
            name_history.extend([name.decode("utf-8") for name in names])
        return name_history

def setup(bot):
    bot.add_cog(NameHistoryCog(bot))
