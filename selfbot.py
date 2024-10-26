import discord
from discord.ext import commands
import sqlite3
import pymongo
import mysql.connector
import redis
import os
from dotenv import load_dotenv
import importlib

load_dotenv()

class SelfBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=os.getenv("PREFIX"))
        self.local_db_conn = None
        self.mongo_client = None
        self.mysql_conn = None
        self.redis_client = None
        self.setup_databases()
        self.load_cogs()

    def setup_databases(self):
        try:
            if os.getenv("LOCAL_DB_PATH"):
                self.local_db_conn = sqlite3.connect(os.getenv("LOCAL_DB_PATH"))
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
        
        try:
            if os.getenv("MONGODB_URI"):
                self.mongo_client = pymongo.MongoClient(os.getenv("MONGODB_URI"))
        except pymongo.errors.PyMongoError as e:
            print(f"MongoDB error: {e}")
        
        try:
            if os.getenv("MYSQL_HOST"):
                self.mysql_conn = mysql.connector.connect(
                    host=os.getenv("MYSQL_HOST"),
                    user=os.getenv("MYSQL_USER"),
                    password=os.getenv("MYSQL_PASSWORD"),
                    database=os.getenv("MYSQL_DATABASE")
                )
        except mysql.connector.Error as e:
            print(f"MySQL error: {e}")
        
        try:
            if os.getenv("REDIS_HOST"):
                self.redis_client = redis.StrictRedis(
                    host=os.getenv("REDIS_HOST"),
                    port=os.getenv("REDIS_PORT"),
                    password=os.getenv("REDIS_PASSWORD")
                )
        except redis.RedisError as e:
            print(f"Redis error: {e}")

    def load_cogs(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                cog_name = filename[:-3]
                cog_module = importlib.import_module(f'cogs.{cog_name}')
                self.add_cog(cog_module.setup(self))

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_member_update(self, before, after):
        if before.name != after.name or before.avatar != after.avatar or before.display_name != after.display_name:
            self.store_user_info(after)

    def store_user_info(self, member):
        user_info = {
            "id": member.id,
            "name": member.name,
            "avatar": str(member.avatar_url),
            "display_name": member.display_name
        }
        try:
            if self.local_db_conn:
                self.store_user_info_local(user_info)
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
        
        try:
            if self.mongo_client:
                self.store_user_info_mongo(user_info)
        except pymongo.errors.PyMongoError as e:
            print(f"MongoDB error: {e}")
        
        try:
            if self.mysql_conn:
                self.store_user_info_mysql(user_info)
        except mysql.connector.Error as e:
            print(f"MySQL error: {e}")
        
        try:
            if self.redis_client:
                self.store_user_info_redis(user_info)
        except redis.RedisError as e:
            print(f"Redis error: {e}")

    def store_user_info_local(self, user_info):
        cursor = self.local_db_conn.cursor()
        cursor.execute("""
            INSERT INTO users (id, name, avatar, display_name)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
            name=excluded.name,
            avatar=excluded.avatar,
            display_name=excluded.display_name
        """, (user_info["id"], user_info["name"], user_info["avatar"], user_info["display_name"]))
        self.local_db_conn.commit()

    def store_user_info_mongo(self, user_info):
        db = self.mongo_client[os.getenv("MONGODB_DATABASE")]
        collection = db["users"]
        collection.update_one({"id": user_info["id"]}, {"$set": user_info}, upsert=True)

    def store_user_info_mysql(self, user_info):
        cursor = self.mysql_conn.cursor()
        cursor.execute("""
            INSERT INTO users (id, name, avatar, display_name)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            name=VALUES(name),
            avatar=VALUES(avatar),
            display_name=VALUES(display_name)
        """, (user_info["id"], user_info["name"], user_info["avatar"], user_info["display_name"]))
        self.mysql_conn.commit()

    def store_user_info_redis(self, user_info):
        self.redis_client.hmset(f"user:{user_info['id']}", user_info)

if __name__ == "__main__":
    bot = SelfBot()
    bot.run(os.getenv("TOKEN"))
