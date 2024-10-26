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
                password=os.getenv("REDIS_PASSWORD")
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
