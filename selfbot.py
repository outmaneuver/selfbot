import discord
from discord.ext import commands
import sqlite3
import pymongo
import mysql.connector
import redis
import json

class SelfBot(commands.Bot):
    def __init__(self, config_file):
        super().__init__(command_prefix="!")
        self.config = self.load_config(config_file)
        self.local_db_conn = None
        self.mongo_client = None
        self.mysql_conn = None
        self.redis_client = None
        self.setup_databases()

    def load_config(self, config_file):
        with open(config_file, 'r') as f:
            return json.load(f)

    def setup_databases(self):
        if self.config.get("local_db"):
            self.local_db_conn = sqlite3.connect(self.config["local_db"]["path"])
        if self.config.get("mongodb"):
            self.mongo_client = pymongo.MongoClient(self.config["mongodb"]["uri"])
        if self.config.get("mysql"):
            self.mysql_conn = mysql.connector.connect(
                host=self.config["mysql"]["host"],
                user=self.config["mysql"]["user"],
                password=self.config["mysql"]["password"],
                database=self.config["mysql"]["database"]
            )
        if self.config.get("redis"):
            self.redis_client = redis.StrictRedis(
                host=self.config["redis"]["host"],
                port=self.config["redis"]["port"],
                password=self.config["redis"]["password"]
            )

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
        if self.local_db_conn:
            self.store_user_info_local(user_info)
        if self.mongo_client:
            self.store_user_info_mongo(user_info)
        if self.mysql_conn:
            self.store_user_info_mysql(user_info)
        if self.redis_client:
            self.store_user_info_redis(user_info)

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
        db = self.mongo_client[self.config["mongodb"]["database"]]
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
    bot = SelfBot("config.json")
    bot.run(bot.config["token"])
