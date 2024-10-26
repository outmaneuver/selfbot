import sqlite3
import pymongo
import mysql.connector
import redis
import os
from dotenv import load_dotenv

load_dotenv()

def connect_sqlite():
    try:
        if os.getenv("LOCAL_DB_PATH"):
            return sqlite3.connect(os.getenv("LOCAL_DB_PATH"))
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    return None

def connect_mongodb():
    try:
        if os.getenv("MONGODB_URI"):
            return pymongo.MongoClient(os.getenv("MONGODB_URI"))
    except pymongo.errors.PyMongoError as e:
        print(f"MongoDB error: {e}")
    return None

def connect_mysql():
    try:
        if os.getenv("MYSQL_HOST"):
            return mysql.connector.connect(
                host=os.getenv("MYSQL_HOST"),
                user=os.getenv("MYSQL_USER"),
                password=os.getenv("MYSQL_PASSWORD"),
                database=os.getenv("MYSQL_DATABASE")
            )
    except mysql.connector.Error as e:
        print(f"MySQL error: {e}")
    return None

def connect_redis():
    try:
        if os.getenv("REDIS_HOST"):
            return redis.StrictRedis(
                host=os.getenv("REDIS_HOST"),
                port=os.getenv("REDIS_PORT"),
                password=os.getenv("REDIS_PASSWORD"),
                decode_responses=True
            )
    except redis.RedisError as e:
        print(f"Redis error: {e}")
    return None

def determine_database():
    local_db_conn = connect_sqlite()
    mongo_client = connect_mongodb()
    mysql_conn = connect_mysql()
    redis_client = connect_redis()

    if not any([local_db_conn, mongo_client, mysql_conn, redis_client]):
        print("No external databases configured. Setting up a local database.")
        local_db_conn = sqlite3.connect("default_local_db.sqlite")
        print("Warning: Using local database as no other databases are configured.")

    return local_db_conn, mongo_client, mysql_conn, redis_client

def fetch_avatar_history_sqlite(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT avatar FROM avatar_history WHERE user_id = ?", (user_id,))
    return [row[0] for row in cursor.fetchall()]

def fetch_avatar_history_mongodb(client, user_id):
    db = client[os.getenv("MONGODB_DATABASE")]
    collection = db["avatar_history"]
    return [doc["avatar"] for doc in collection.find({"user_id": user_id})]

def fetch_avatar_history_mysql(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT avatar FROM avatar_history WHERE user_id = %s", (user_id,))
    return [row[0] for row in cursor.fetchall()]

def fetch_avatar_history_redis(client, user_id):
    avatars = client.lrange(f"avatar_history:{user_id}", 0, -1)
    return avatars

def fetch_name_history_sqlite(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM name_history WHERE user_id = ?", (user_id,))
    return [row[0] for row in cursor.fetchall()]

def fetch_name_history_mongodb(client, user_id):
    db = client[os.getenv("MONGODB_DATABASE")]
    collection = db["name_history"]
    return [doc["name"] for doc in collection.find({"user_id": user_id})]

def fetch_name_history_mysql(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM name_history WHERE user_id = %s", (user_id,))
    return [row[0] for row in cursor.fetchall()]

def fetch_name_history_redis(client, user_id):
    names = client.lrange(f"name_history:{user_id}", 0, -1)
    return names

def store_user_info(user, local_db_conn, mongo_client, mysql_conn, redis_client):
    try:
        if local_db_conn:
            cursor = local_db_conn.cursor()
            cursor.execute("INSERT INTO user_info (user_id, name, avatar, display_name) VALUES (?, ?, ?, ?)",
                           (user.id, user.name, user.avatar, user.display_name))
            local_db_conn.commit()
    except sqlite3.Error as e:
        print(f"SQLite error while storing user info: {e}")

    try:
        if mongo_client:
            db = mongo_client[os.getenv("MONGODB_DATABASE")]
            collection = db["user_info"]
            collection.insert_one({"user_id": user.id, "name": user.name, "avatar": user.avatar, "display_name": user.display_name})
    except pymongo.errors.PyMongoError as e:
        print(f"MongoDB error while storing user info: {e}")

    try:
        if mysql_conn:
            cursor = mysql_conn.cursor()
            cursor.execute("INSERT INTO user_info (user_id, name, avatar, display_name) VALUES (%s, %s, %s, %s)",
                           (user.id, user.name, user.avatar, user.display_name))
            mysql_conn.commit()
    except mysql.connector.Error as e:
        print(f"MySQL error while storing user info: {e}")

    try:
        if redis_client:
            redis_client.hmset(f"user_info:{user.id}", {"name": user.name, "avatar": user.avatar, "display_name": user.display_name})
    except redis.RedisError as e:
        print(f"Redis error while storing user info: {e}")

def store_custom_activity_settings(user_id, settings, local_db_conn, mongo_client, mysql_conn, redis_client):
    try:
        if local_db_conn:
            cursor = local_db_conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO custom_activity_settings (user_id, settings) VALUES (?, ?)",
                           (user_id, settings))
            local_db_conn.commit()
    except sqlite3.Error as e:
        print(f"SQLite error while storing custom activity settings: {e}")

    try:
        if mongo_client:
            db = mongo_client[os.getenv("MONGODB_DATABASE")]
            collection = db["custom_activity_settings"]
            collection.update_one({"user_id": user_id}, {"$set": {"settings": settings}}, upsert=True)
    except pymongo.errors.PyMongoError as e:
        print(f"MongoDB error while storing custom activity settings: {e}")

    try:
        if mysql_conn:
            cursor = mysql_conn.cursor()
            cursor.execute("INSERT INTO custom_activity_settings (user_id, settings) VALUES (%s, %s) ON DUPLICATE KEY UPDATE settings = %s",
                           (user_id, settings, settings))
            mysql_conn.commit()
    except mysql.connector.Error as e:
        print(f"MySQL error while storing custom activity settings: {e}")

    try:
        if redis_client:
            redis_client.hmset(f"custom_activity_settings:{user_id}", {"settings": settings})
    except redis.RedisError as e:
        print(f"Redis error while storing custom activity settings: {e}")

def retrieve_custom_activity_settings(user_id, local_db_conn, mongo_client, mysql_conn, redis_client):
    settings = None
    try:
        if local_db_conn:
            cursor = local_db_conn.cursor()
            cursor.execute("SELECT settings FROM custom_activity_settings WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()
            if result:
                settings = result[0]
    except sqlite3.Error as e:
        print(f"SQLite error while retrieving custom activity settings: {e}")

    try:
        if mongo_client and not settings:
            db = mongo_client[os.getenv("MONGODB_DATABASE")]
            collection = db["custom_activity_settings"]
            result = collection.find_one({"user_id": user_id})
            if result:
                settings = result["settings"]
    except pymongo.errors.PyMongoError as e:
        print(f"MongoDB error while retrieving custom activity settings: {e}")

    try:
        if mysql_conn and not settings:
            cursor = mysql_conn.cursor()
            cursor.execute("SELECT settings FROM custom_activity_settings WHERE user_id = %s", (user_id,))
            result = cursor.fetchone()
            if result:
                settings = result[0]
    except mysql.connector.Error as e:
        print(f"MySQL error while retrieving custom activity settings: {e}")

    try:
        if redis_client and not settings:
            settings = redis_client.hget(f"custom_activity_settings:{user_id}", "settings")
            if settings:
                settings = settings.decode("utf-8")
    except redis.RedisError as e:
        print(f"Redis error while retrieving custom activity settings: {e}")

    return settings

def fetch_avatar_history_cache(cache, user_id):
    return cache.get(f"avatar_history:{user_id}", [])

def fetch_name_history_cache(cache, user_id):
    return cache.get(f"name_history:{user_id}", [])

def store_user_info_cache(user, cache):
    cache[f"user_info:{user.id}"] = {"name": user.name, "avatar": user.avatar, "display_name": user.display_name}

def store_custom_activity_settings_cache(user_id, settings, cache):
    cache[f"custom_activity_settings:{user_id}"] = settings

def retrieve_custom_activity_settings_cache(user_id, cache):
    return cache.get(f"custom_activity_settings:{user_id}")
