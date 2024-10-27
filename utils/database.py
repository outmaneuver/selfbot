import sqlite3
import pymongo
import mysql.connector
import redis
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnection:
    def __init__(self, db_type):
        self.db_type = db_type
        self.connection = self.connect_database()

    def connect_database(self):
        try:
            if self.db_type == "sqlite" and os.getenv("LOCAL_DB_PATH"):
                return sqlite3.connect(os.getenv("LOCAL_DB_PATH"))
            elif self.db_type == "mongodb" and os.getenv("MONGODB_URI"):
                return pymongo.MongoClient(os.getenv("MONGODB_URI"))
            elif self.db_type == "mysql" and os.getenv("MYSQL_HOST"):
                return mysql.connector.connect(
                    host=os.getenv("MYSQL_HOST"),
                    user=os.getenv("MYSQL_USER"),
                    password=os.getenv("MYSQL_PASSWORD"),
                    database=os.getenv("MYSQL_DATABASE")
                )
            elif self.db_type == "redis" and os.getenv("REDIS_HOST"):
                return redis.StrictRedis(
                    host=os.getenv("REDIS_HOST"),
                    port=os.getenv("REDIS_PORT"),
                    password=os.getenv("REDIS_PASSWORD"),
                    decode_responses=True
                )
        except (sqlite3.Error, pymongo.errors.PyMongoError, mysql.connector.Error, redis.RedisError) as e:
            print(f"{self.db_type.capitalize()} error: {e}")
        return None

class DatabaseManager:
    def __init__(self):
        self.local_db_conn = DatabaseConnection("sqlite").connection
        self.mongo_client = DatabaseConnection("mongodb").connection
        self.mysql_conn = DatabaseConnection("mysql").connection
        self.redis_client = DatabaseConnection("redis").connection

        if not any([self.local_db_conn, self.mongo_client, self.mysql_conn, self.redis_client]):
            print("No external databases configured. Setting up a local database.")
            self.local_db_conn = sqlite3.connect("default_local_db.sqlite")
            print("Warning: Using local database as no other databases are configured.")

    def fetch_avatar_history(self, user_id):
        if self.local_db_conn:
            return self.fetch_avatar_history_sqlite(user_id)
        elif self.mongo_client:
            return self.fetch_avatar_history_mongodb(user_id)
        elif self.mysql_conn:
            return self.fetch_avatar_history_mysql(user_id)
        elif self.redis_client:
            return self.fetch_avatar_history_redis(user_id)
        return []

    def fetch_name_history(self, user_id):
        if self.local_db_conn:
            return self.fetch_name_history_sqlite(user_id)
        elif self.mongo_client:
            return self.fetch_name_history_mongodb(user_id)
        elif self.mysql_conn:
            return self.fetch_name_history_mysql(user_id)
        elif self.redis_client:
            return self.fetch_name_history_redis(user_id)
        return []

    def fetch_avatar_history_sqlite(self, user_id):
        cursor = self.local_db_conn.cursor()
        cursor.execute("SELECT avatar FROM avatar_history WHERE user_id = ?", (user_id,))
        return [row[0] for row in cursor.fetchall()]

    def fetch_avatar_history_mongodb(self, user_id):
        db = self.mongo_client[os.getenv("MONGODB_DATABASE")]
        collection = db["avatar_history"]
        return [doc["avatar"] for doc in collection.find({"user_id": user_id})]

    def fetch_avatar_history_mysql(self, user_id):
        cursor = self.mysql_conn.cursor()
        cursor.execute("SELECT avatar FROM avatar_history WHERE user_id = %s", (user_id,))
        return [row[0] for row in cursor.fetchall()]

    def fetch_avatar_history_redis(self, user_id):
        avatars = self.redis_client.lrange(f"avatar_history:{user_id}", 0, -1)
        return avatars

    def fetch_name_history_sqlite(self, user_id):
        cursor = self.local_db_conn.cursor()
        cursor.execute("SELECT name FROM name_history WHERE user_id = ?", (user_id,))
        return [row[0] for row in cursor.fetchall()]

    def fetch_name_history_mongodb(self, user_id):
        db = self.mongo_client[os.getenv("MONGODB_DATABASE")]
        collection = db["name_history"]
        return [doc["name"] for doc in collection.find({"user_id": user_id})]

    def fetch_name_history_mysql(self, user_id):
        cursor = self.mysql_conn.cursor()
        cursor.execute("SELECT name FROM name_history WHERE user_id = %s", (user_id,))
        return [row[0] for row in cursor.fetchall()]

    def fetch_name_history_redis(self, user_id):
        names = self.redis_client.lrange(f"name_history:{user_id}", 0, -1)
        return names

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

    def store_custom_activity_settings(self, user_id, settings):
        try:
            if self.local_db_conn:
                cursor = self.local_db_conn.cursor()
                cursor.execute("INSERT OR REPLACE INTO custom_activity_settings (user_id, settings) VALUES (?, ?)",
                               (user_id, settings))
                self.local_db_conn.commit()
        except sqlite3.Error as e:
            print(f"SQLite error while storing custom activity settings: {e}")

        try:
            if self.mongo_client:
                db = self.mongo_client[os.getenv("MONGODB_DATABASE")]
                collection = db["custom_activity_settings"]
                collection.update_one({"user_id": user_id}, {"$set": {"settings": settings}}, upsert=True)
        except pymongo.errors.PyMongoError as e:
            print(f"MongoDB error while storing custom activity settings: {e}")

        try:
            if self.mysql_conn:
                cursor = self.mysql_conn.cursor()
                cursor.execute("INSERT INTO custom_activity_settings (user_id, settings) VALUES (%s, %s) ON DUPLICATE KEY UPDATE settings = %s",
                               (user_id, settings, settings))
                self.mysql_conn.commit()
        except mysql.connector.Error as e:
            print(f"MySQL error while storing custom activity settings: {e}")

        try:
            if self.redis_client:
                self.redis_client.hmset(f"custom_activity_settings:{user_id}", {"settings": settings})
        except redis.RedisError as e:
            print(f"Redis error while storing custom activity settings: {e}")

    def retrieve_custom_activity_settings(self, user_id):
        settings = None
        try:
            if self.local_db_conn:
                cursor = self.local_db_conn.cursor()
                cursor.execute("SELECT settings FROM custom_activity_settings WHERE user_id = ?", (user_id,))
                result = cursor.fetchone()
                if result:
                    settings = result[0]
        except sqlite3.Error as e:
            print(f"SQLite error while retrieving custom activity settings: {e}")

        try:
            if self.mongo_client and not settings:
                db = self.mongo_client[os.getenv("MONGODB_DATABASE")]
                collection = db["custom_activity_settings"]
                result = collection.find_one({"user_id": user_id})
                if result:
                    settings = result["settings"]
        except pymongo.errors.PyMongoError as e:
            print(f"MongoDB error while retrieving custom activity settings: {e}")

        try:
            if self.mysql_conn and not settings:
                cursor = self.mysql_conn.cursor()
                cursor.execute("SELECT settings FROM custom_activity_settings WHERE user_id = %s", (user_id,))
                result = cursor.fetchone()
                if result:
                    settings = result[0]
        except mysql.connector.Error as e:
            print(f"MySQL error while retrieving custom activity settings: {e}")

        try:
            if self.redis_client and not settings:
                settings = self.redis_client.hget(f"custom_activity_settings:{user_id}", "settings")
                if settings:
                    settings = settings.decode("utf-8")
        except redis.RedisError as e:
            print(f"Redis error while retrieving custom activity settings: {e}")

        return settings

    def fetch_avatar_history_cache(self, cache, user_id):
        return cache.get(f"avatar_history:{user_id}", [])

    def fetch_name_history_cache(self, cache, user_id):
        return cache.get(f"name_history:{user_id}", [])

    def store_user_info_cache(self, user, cache):
        cache[f"user_info:{user.id}"] = {"name": user.name, "avatar": user.avatar, "display_name": user.display_name}

    def store_custom_activity_settings_cache(self, user_id, settings, cache):
        cache[f"custom_activity_settings:{user_id}"] = settings

    def retrieve_custom_activity_settings_cache(self, user_id, cache):
        return cache.get(f"custom_activity_settings:{user_id}")

    def store_username_change(self, user_id, new_username):
        try:
            if self.local_db_conn:
                cursor = self.local_db_conn.cursor()
                cursor.execute("INSERT INTO username_history (user_id, username) VALUES (?, ?)", (user_id, new_username))
                self.local_db_conn.commit()
        except sqlite3.Error as e:
            print(f"SQLite error while storing username change: {e}")

        try:
            if self.mongo_client:
                db = self.mongo_client[os.getenv("MONGODB_DATABASE")]
                collection = db["username_history"]
                collection.insert_one({"user_id": user_id, "username": new_username})
        except pymongo.errors.PyMongoError as e:
            print(f"MongoDB error while storing username change: {e}")

        try:
            if self.mysql_conn:
                cursor = self.mysql_conn.cursor()
                cursor.execute("INSERT INTO username_history (user_id, username) VALUES (%s, %s)", (user_id, new_username))
                self.mysql_conn.commit()
        except mysql.connector.Error as e:
            print(f"MySQL error while storing username change: {e}")

        try:
            if self.redis_client:
                self.redis_client.lpush(f"username_history:{user_id}", new_username)
        except redis.RedisError as e:
            print(f"Redis error while storing username change: {e}")

    def store_avatar_change(self, user_id, new_avatar):
        try:
            if self.local_db_conn:
                cursor = self.local_db_conn.cursor()
                cursor.execute("INSERT INTO avatar_history (user_id, avatar) VALUES (?, ?)", (user_id, new_avatar))
                self.local_db_conn.commit()
        except sqlite3.Error as e:
            print(f"SQLite error while storing avatar change: {e}")

        try:
            if self.mongo_client:
                db = self.mongo_client[os.getenv("MONGODB_DATABASE")]
                collection = db["avatar_history"]
                collection.insert_one({"user_id": user_id, "avatar": new_avatar})
        except pymongo.errors.PyMongoError as e:
            print(f"MongoDB error while storing avatar change: {e}")

        try:
            if self.mysql_conn:
                cursor = self.mysql_conn.cursor()
                cursor.execute("INSERT INTO avatar_history (user_id, avatar) VALUES (%s, %s)", (user_id, new_avatar))
                self.mysql_conn.commit()
        except mysql.connector.Error as e:
            print(f"MySQL error while storing avatar change: {e}")

        try:
            if self.redis_client:
                self.redis_client.lpush(f"avatar_history:{user_id}", new_avatar)
        except redis.RedisError as e:
            print(f"Redis error while storing avatar change: {e}")

    def store_display_name_change(self, user_id, new_display_name):
        try:
            if self.local_db_conn:
                cursor = self.local_db_conn.cursor()
                cursor.execute("INSERT INTO display_name_history (user_id, display_name) VALUES (?, ?)", (user_id, new_display_name))
                self.local_db_conn.commit()
        except sqlite3.Error as e:
            print(f"SQLite error while storing display name change: {e}")

        try:
            if self.mongo_client:
                db = self.mongo_client[os.getenv("MONGODB_DATABASE")]
                collection = db["display_name_history"]
                collection.insert_one({"user_id": user_id, "display_name": new_display_name})
        except pymongo.errors.PyMongoError as e:
            print(f"MongoDB error while storing display name change: {e}")

        try:
            if self.mysql_conn:
                cursor = self.mysql_conn.cursor()
                cursor.execute("INSERT INTO display_name_history (user_id, display_name) VALUES (%s, %s)", (user_id, new_display_name))
                self.mysql_conn.commit()
        except mysql.connector.Error as e:
            print(f"MySQL error while storing display name change: {e}")

        try:
            if self.redis_client:
                self.redis_client.lpush(f"display_name_history:{user_id}", new_display_name)
        except redis.RedisError as e:
            print(f"Redis error while storing display name change: {e}")
