import sqlite3
import pymongo
import mysql.connector
import redis
import os
from dotenv import load_dotenv

load_dotenv()

class UserInfoManager:
    def __init__(self, local_db_conn, mongo_client, mysql_conn, redis_client):
        self.local_db_conn = local_db_conn
        self.mongo_client = mongo_client
        self.mysql_conn = mysql_conn
        self.redis_client = redis_client

    def store_user_info(self, user):
        try:
            if self.local_db_conn:
                cursor = self.local_db_conn.cursor()
                cursor.execute("INSERT INTO user_info (user_id, name, avatar, display_name) VALUES (?, ?, ?, ?)",
                               (user.id, user.name, user.avatar, user.display_name))
                self.local_db_conn.commit()
        except sqlite3.Error as e:
            print(f"SQLite error while storing user info: {e}")

        try:
            if self.mongo_client:
                db = self.mongo_client[os.getenv("MONGODB_DATABASE")]
                collection = db["user_info"]
                collection.insert_one({"user_id": user.id, "name": user.name, "avatar": user.avatar, "display_name": user.display_name})
        except pymongo.errors.PyMongoError as e:
            print(f"MongoDB error while storing user info: {e}")

        try:
            if self.mysql_conn:
                cursor = self.mysql_conn.cursor()
                cursor.execute("INSERT INTO user_info (user_id, name, avatar, display_name) VALUES (%s, %s, %s, %s)",
                               (user.id, user.name, user.avatar, user.display_name))
                self.mysql_conn.commit()
        except mysql.connector.Error as e:
            print(f"MySQL error while storing user info: {e}")

        try:
            if self.redis_client:
                self.redis_client.hmset(f"user_info:{user.id}", {"name": user.name, "avatar": user.avatar, "display_name": user.display_name})
        except redis.RedisError as e:
            print(f"Redis error while storing user info: {e}")

    def monitor_user_info_changes(self, user):
        try:
            if self.local_db_conn:
                cursor = self.local_db_conn.cursor()
                cursor.execute("SELECT name, avatar, display_name FROM user_info WHERE user_id = ?", (user.id,))
                result = cursor.fetchone()
                if result:
                    old_name, old_avatar, old_display_name = result
                    if old_name != user.name or old_avatar != user.avatar or old_display_name != user.display_name:
                        self.store_user_info(user)
        except sqlite3.Error as e:
            print(f"SQLite error while monitoring user info changes: {e}")

        try:
            if self.mongo_client:
                db = self.mongo_client[os.getenv("MONGODB_DATABASE")]
                collection = db["user_info"]
                result = collection.find_one({"user_id": user.id})
                if result:
                    old_name, old_avatar, old_display_name = result["name"], result["avatar"], result["display_name"]
                    if old_name != user.name or old_avatar != user.avatar or old_display_name != user.display_name:
                        self.store_user_info(user)
        except pymongo.errors.PyMongoError as e:
            print(f"MongoDB error while monitoring user info changes: {e}")

        try:
            if self.mysql_conn:
                cursor = self.mysql_conn.cursor()
                cursor.execute("SELECT name, avatar, display_name FROM user_info WHERE user_id = %s", (user.id,))
                result = cursor.fetchone()
                if result:
                    old_name, old_avatar, old_display_name = result
                    if old_name != user.name or old_avatar != user.avatar or old_display_name != user.display_name:
                        self.store_user_info(user)
        except mysql.connector.Error as e:
            print(f"MySQL error while monitoring user info changes: {e}")

        try:
            if self.redis_client:
                result = self.redis_client.hgetall(f"user_info:{user.id}")
                if result:
                    old_name, old_avatar, old_display_name = result["name"], result["avatar"], result["display_name"]
                    if old_name != user.name or old_avatar != user.avatar or old_display_name != user.display_name:
                        self.store_user_info(user)
        except redis.RedisError as e:
            print(f"Redis error while monitoring user info changes: {e}")
