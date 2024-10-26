import sqlite3
import pymongo
import mysql.connector
import redis
import os
from dotenv import load_dotenv

load_dotenv()

def connect_sqlite():
    if os.getenv("LOCAL_DB_PATH"):
        return sqlite3.connect(os.getenv("LOCAL_DB_PATH"))
    return None

def connect_mongodb():
    if os.getenv("MONGODB_URI"):
        return pymongo.MongoClient(os.getenv("MONGODB_URI"))
    return None

def connect_mysql():
    if os.getenv("MYSQL_HOST"):
        return mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        )
    return None

def connect_redis():
    if os.getenv("REDIS_HOST"):
        return redis.StrictRedis(
            host=os.getenv("REDIS_HOST"),
            port=os.getenv("REDIS_PORT"),
            password=os.getenv("REDIS_PASSWORD")
        )
    return None

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
    return [avatar.decode("utf-8") for avatar in avatars]

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
    return [name.decode("utf-8") for name in names]
