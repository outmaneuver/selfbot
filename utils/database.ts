import sqlite3 from 'sqlite3';
import { MongoClient } from 'mongodb';
import mysql from 'mysql2/promise';
import redis from 'redis';
import { config } from 'dotenv';

config();

class SQLiteConnection {
    connection: sqlite3.Database | null;

    constructor() {
        this.connection = this.connectDatabase();
    }

    connectDatabase(): sqlite3.Database | null {
        try {
            if (process.env.LOCAL_DB_PATH) {
                return new sqlite3.Database(process.env.LOCAL_DB_PATH);
            }
        } catch (e) {
            console.error(`SQLite error: ${e}`);
        }
        return null;
    }
}

class MongoDBConnection {
    connection: MongoClient | null;

    constructor() {
        this.connection = this.connectDatabase();
    }

    connectDatabase(): MongoClient | null {
        try {
            if (process.env.MONGODB_URI) {
                return new MongoClient(process.env.MONGODB_URI);
            }
        } catch (e) {
            console.error(`MongoDB error: ${e}`);
        }
        return null;
    }
}

class MySQLConnection {
    connection: mysql.Connection | null;

    constructor() {
        this.connection = this.connectDatabase();
    }

    async connectDatabase(): Promise<mysql.Connection | null> {
        try {
            if (process.env.MYSQL_HOST) {
                return await mysql.createConnection({
                    host: process.env.MYSQL_HOST,
                    user: process.env.MYSQL_USER,
                    password: process.env.MYSQL_PASSWORD,
                    database: process.env.MYSQL_DATABASE
                });
            }
        } catch (e) {
            console.error(`MySQL error: ${e}`);
        }
        return null;
    }
}

class RedisConnection {
    connection: redis.RedisClientType | null;

    constructor() {
        this.connection = this.connectDatabase();
    }

    connectDatabase(): redis.RedisClientType | null {
        try {
            if (process.env.REDIS_HOST) {
                return redis.createClient({
                    url: `redis://${process.env.REDIS_HOST}:${process.env.REDIS_PORT}`,
                    password: process.env.REDIS_PASSWORD
                });
            }
        } catch (e) {
            console.error(`Redis error: ${e}`);
        }
        return null;
    }
}

class DatabaseManager {
    local_db_conn: sqlite3.Database | null;
    mongo_client: MongoClient | null;
    mysql_conn: mysql.Connection | null;
    redis_client: redis.RedisClientType | null;

    constructor() {
        this.local_db_conn = new SQLiteConnection().connection;
        this.mongo_client = new MongoDBConnection().connection;
        this.mysql_conn = new MySQLConnection().connection;
        this.redis_client = new RedisConnection().connection;

        if (!this.local_db_conn && !this.mongo_client && !this.mysql_conn && !this.redis_client) {
            console.log("No external databases configured. Setting up a local database.");
            this.local_db_conn = new sqlite3.Database("default_local_db.sqlite");
            console.log("Warning: Using local database as no other databases are configured.");
        }
    }

    async fetch_avatar_history(user_id: string): Promise<string[]> {
        if (this.local_db_conn) {
            return this.fetch_avatar_history_sqlite(user_id);
        } else if (this.mongo_client) {
            return this.fetch_avatar_history_mongodb(user_id);
        } else if (this.mysql_conn) {
            return this.fetch_avatar_history_mysql(user_id);
        } else if (this.redis_client) {
            return this.fetch_avatar_history_redis(user_id);
        }
        return [];
    }

    async fetch_name_history(user_id: string): Promise<string[]> {
        if (this.local_db_conn) {
            return this.fetch_name_history_sqlite(user_id);
        } else if (this.mongo_client) {
            return this.fetch_name_history_mongodb(user_id);
        } else if (this.mysql_conn) {
            return this.fetch_name_history_mysql(user_id);
        } else if (this.redis_client) {
            return this.fetch_name_history_redis(user_id);
        }
        return [];
    }

    async fetch_avatar_history_sqlite(user_id: string): Promise<string[]> {
        return new Promise((resolve, reject) => {
            this.local_db_conn!.all("SELECT avatar FROM avatar_history WHERE user_id = ?", [user_id], (err, rows) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(rows.map(row => row.avatar));
                }
            });
        });
    }

    async fetch_avatar_history_mongodb(user_id: string): Promise<string[]> {
        const db = this.mongo_client!.db(process.env.MONGODB_DATABASE);
        const collection = db.collection("avatar_history");
        const docs = await collection.find({ user_id }).toArray();
        return docs.map(doc => doc.avatar);
    }

    async fetch_avatar_history_mysql(user_id: string): Promise<string[]> {
        const [rows] = await this.mysql_conn!.execute("SELECT avatar FROM avatar_history WHERE user_id = ?", [user_id]);
        return (rows as any[]).map(row => row.avatar);
    }

    async fetch_avatar_history_redis(user_id: string): Promise<string[]> {
        const avatars = await this.redis_client!.lRange(`avatar_history:${user_id}`, 0, -1);
        return avatars;
    }

    async fetch_name_history_sqlite(user_id: string): Promise<string[]> {
        return new Promise((resolve, reject) => {
            this.local_db_conn!.all("SELECT name FROM name_history WHERE user_id = ?", [user_id], (err, rows) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(rows.map(row => row.name));
                }
            });
        });
    }

    async fetch_name_history_mongodb(user_id: string): Promise<string[]> {
        const db = this.mongo_client!.db(process.env.MONGODB_DATABASE);
        const collection = db.collection("name_history");
        const docs = await collection.find({ user_id }).toArray();
        return docs.map(doc => doc.name);
    }

    async fetch_name_history_mysql(user_id: string): Promise<string[]> {
        const [rows] = await this.mysql_conn!.execute("SELECT name FROM name_history WHERE user_id = ?", [user_id]);
        return (rows as any[]).map(row => row.name);
    }

    async fetch_name_history_redis(user_id: string): Promise<string[]> {
        const names = await this.redis_client!.lRange(`name_history:${user_id}`, 0, -1);
        return names;
    }

    async store_user_info(user: any): Promise<void> {
        try {
            if (this.local_db_conn) {
                this.local_db_conn.run("INSERT INTO user_info (user_id, name, avatar, display_name) VALUES (?, ?, ?, ?)",
                    [user.id, user.name, user.avatar, user.display_name]);
            }
        } catch (e) {
            console.error(`SQLite error while storing user info: ${e}`);
        }

        try {
            if (this.mongo_client) {
                const db = this.mongo_client.db(process.env.MONGODB_DATABASE);
                const collection = db.collection("user_info");
                await collection.insertOne({ user_id: user.id, name: user.name, avatar: user.avatar, display_name: user.display_name });
            }
        } catch (e) {
            console.error(`MongoDB error while storing user info: ${e}`);
        }

        try {
            if (this.mysql_conn) {
                await this.mysql_conn.execute("INSERT INTO user_info (user_id, name, avatar, display_name) VALUES (?, ?, ?, ?)",
                    [user.id, user.name, user.avatar, user.display_name]);
            }
        } catch (e) {
            console.error(`MySQL error while storing user info: ${e}`);
        }

        try {
            if (this.redis_client) {
                await this.redis_client.hSet(`user_info:${user.id}`, { name: user.name, avatar: user.avatar, display_name: user.display_name });
            }
        } catch (e) {
            console.error(`Redis error while storing user info: ${e}`);
        }
    }

    async store_custom_activity_settings(user_id: string, settings: any): Promise<void> {
        try {
            if (this.local_db_conn) {
                this.local_db_conn.run("INSERT OR REPLACE INTO custom_activity_settings (user_id, settings) VALUES (?, ?)",
                    [user_id, settings]);
            }
        } catch (e) {
            console.error(`SQLite error while storing custom activity settings: ${e}`);
        }

        try {
            if (this.mongo_client) {
                const db = this.mongo_client.db(process.env.MONGODB_DATABASE);
                const collection = db.collection("custom_activity_settings");
                await collection.updateOne({ user_id }, { $set: { settings } }, { upsert: true });
            }
        } catch (e) {
            console.error(`MongoDB error while storing custom activity settings: ${e}`);
        }

        try {
            if (this.mysql_conn) {
                await this.mysql_conn.execute("INSERT INTO custom_activity_settings (user_id, settings) VALUES (?, ?) ON DUPLICATE KEY UPDATE settings = ?",
                    [user_id, settings, settings]);
            }
        } catch (e) {
            console.error(`MySQL error while storing custom activity settings: ${e}`);
        }

        try {
            if (this.redis_client) {
                await this.redis_client.hSet(`custom_activity_settings:${user_id}`, { settings });
            }
        } catch (e) {
            console.error(`Redis error while storing custom activity settings: ${e}`);
        }
    }

    async retrieve_custom_activity_settings(user_id: string): Promise<any> {
        let settings: any = null;
        try {
            if (this.local_db_conn) {
                this.local_db_conn.get("SELECT settings FROM custom_activity_settings WHERE user_id = ?", [user_id], (err, row) => {
                    if (err) {
                        console.error(`SQLite error while retrieving custom activity settings: ${err}`);
                    } else {
                        settings = row ? row.settings : null;
                    }
                });
            }
        } catch (e) {
            console.error(`SQLite error while retrieving custom activity settings: ${e}`);
        }

        try {
            if (this.mongo_client && !settings) {
                const db = this.mongo_client.db(process.env.MONGODB_DATABASE);
                const collection = db.collection("custom_activity_settings");
                const result = await collection.findOne({ user_id });
                settings = result ? result.settings : null;
            }
        } catch (e) {
            console.error(`MongoDB error while retrieving custom activity settings: ${e}`);
        }

        try {
            if (this.mysql_conn && !settings) {
                const [rows] = await this.mysql_conn.execute("SELECT settings FROM custom_activity_settings WHERE user_id = ?", [user_id]);
                settings = rows.length ? rows[0].settings : null;
            }
        } catch (e) {
            console.error(`MySQL error while retrieving custom activity settings: ${e}`);
        }

        try {
            if (this.redis_client && !settings) {
                settings = await this.redis_client.hGet(`custom_activity_settings:${user_id}`, "settings");
            }
        } catch (e) {
            console.error(`Redis error while retrieving custom activity settings: ${e}`);
        }

        return settings;
    }

    async fetch_avatar_history_cache(cache: any, user_id: string): Promise<string[]> {
        return cache.get(`avatar_history:${user_id}`, []);
    }

    async fetch_name_history_cache(cache: any, user_id: string): Promise<string[]> {
        return cache.get(`name_history:${user_id}`, []);
    }

    async store_user_info_cache(user: any, cache: any): Promise<void> {
        cache[`user_info:${user.id}`] = { name: user.name, avatar: user.avatar, display_name: user.display_name };
    }

    async store_custom_activity_settings_cache(user_id: string, settings: any, cache: any): Promise<void> {
        cache[`custom_activity_settings:${user_id}`] = settings;
    }

    async retrieve_custom_activity_settings_cache(user_id: string, cache: any): Promise<any> {
        return cache.get(`custom_activity_settings:${user_id}`);
    }

    async store_username_change(user_id: string, new_username: string): Promise<void> {
        try {
            if (this.local_db_conn) {
                this.local_db_conn.run("INSERT INTO username_history (user_id, username) VALUES (?, ?)", [user_id, new_username]);
            }
        } catch (e) {
            console.error(`SQLite error while storing username change: ${e}`);
        }

        try {
            if (this.mongo_client) {
                const db = this.mongo_client.db(process.env.MONGODB_DATABASE);
                const collection = db.collection("username_history");
                await collection.insertOne({ user_id, username: new_username });
            }
        } catch (e) {
            console.error(`MongoDB error while storing username change: ${e}`);
        }

        try {
            if (this.mysql_conn) {
                await this.mysql_conn.execute("INSERT INTO username_history (user_id, username) VALUES (?, ?)", [user_id, new_username]);
            }
        } catch (e) {
            console.error(`MySQL error while storing username change: ${e}`);
        }

        try {
            if (this.redis_client) {
                await this.redis_client.lPush(`username_history:${user_id}`, new_username);
            }
        } catch (e) {
            console.error(`Redis error while storing username change: ${e}`);
        }
    }

    async store_avatar_change(user_id: string, new_avatar: string): Promise<void> {
        try {
            if (this.local_db_conn) {
                this.local_db_conn.run("INSERT INTO avatar_history (user_id, avatar) VALUES (?, ?)", [user_id, new_avatar]);
            }
        } catch (e) {
            console.error(`SQLite error while storing avatar change: ${e}`);
        }

        try {
            if (this.mongo_client) {
                const db = this.mongo_client.db(process.env.MONGODB_DATABASE);
                const collection = db.collection("avatar_history");
                await collection.insertOne({ user_id, avatar: new_avatar });
            }
        } catch (e) {
            console.error(`MongoDB error while storing avatar change: ${e}`);
        }

        try {
            if (this.mysql_conn) {
                await this.mysql_conn.execute("INSERT INTO avatar_history (user_id, avatar) VALUES (?, ?)", [user_id, new_avatar]);
            }
        } catch (e) {
            console.error(`MySQL error while storing avatar change: ${e}`);
        }

        try {
            if (this.redis_client) {
                await this.redis_client.lPush(`avatar_history:${user_id}`, new_avatar);
            }
        } catch (e) {
            console.error(`Redis error while storing avatar change: ${e}`);
        }
    }

    async store_display_name_change(user_id: string, new_display_name: string): Promise<void> {
        try {
            if (this.local_db_conn) {
                this.local_db_conn.run("INSERT INTO display_name_history (user_id, display_name) VALUES (?, ?)", [user_id, new_display_name]);
            }
        } catch (e) {
            console.error(`SQLite error while storing display name change: ${e}`);
        }

        try {
            if (this.mongo_client) {
                const db = this.mongo_client.db(process.env.MONGODB_DATABASE);
                const collection = db.collection("display_name_history");
                await collection.insertOne({ user_id, display_name: new_display_name });
            }
        } catch (e) {
            console.error(`MongoDB error while storing display name change: ${e}`);
        }

        try {
            if (this.mysql_conn) {
                await this.mysql_conn.execute("INSERT INTO display_name_history (user_id, display_name) VALUES (?, ?)", [user_id, new_display_name]);
            }
        } catch (e) {
            console.error(`MySQL error while storing display name change: ${e}`);
        }

        try {
            if (this.redis_client) {
                await this.redis_client.lPush(`display_name_history:${user_id}`, new_display_name);
            }
        } catch (e) {
            console.error(`Redis error while storing display name change: ${e}`);
        }
    }
}

export default DatabaseManager;
