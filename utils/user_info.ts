import sqlite3 from 'sqlite3';
import { MongoClient } from 'mongodb';
import mysql from 'mysql2/promise';
import redis from 'redis';
import { config } from 'dotenv';

config();

class UserInfoManager {
    private localDbConn: sqlite3.Database | null;
    private mongoClient: MongoClient | null;
    private mysqlConn: mysql.Connection | null;
    private redisClient: redis.RedisClientType | null;

    constructor(localDbConn: sqlite3.Database | null, mongoClient: MongoClient | null, mysqlConn: mysql.Connection | null, redisClient: redis.RedisClientType | null) {
        this.localDbConn = localDbConn;
        this.mongoClient = mongoClient;
        this.mysqlConn = mysqlConn;
        this.redisClient = redisClient;
    }

    async storeUserInfo(user: any): Promise<void> {
        await this._storeUserInfoSqlite(user);
        await this._storeUserInfoMongodb(user);
        await this._storeUserInfoMysql(user);
        await this._storeUserInfoRedis(user);
    }

    private async _storeUserInfoSqlite(user: any): Promise<void> {
        try {
            if (this.localDbConn) {
                this.localDbConn.run("INSERT INTO user_info (user_id, name, avatar, display_name) VALUES (?, ?, ?, ?)",
                    [user.id, user.name, user.avatar, user.display_name]);
            }
        } catch (e) {
            console.error(`SQLite error while storing user info: ${e}`);
        }
    }

    private async _storeUserInfoMongodb(user: any): Promise<void> {
        try {
            if (this.mongoClient) {
                const db = this.mongoClient.db(process.env.MONGODB_DATABASE);
                const collection = db.collection("user_info");
                await collection.insertOne({ user_id: user.id, name: user.name, avatar: user.avatar, display_name: user.display_name });
            }
        } catch (e) {
            console.error(`MongoDB error while storing user info: ${e}`);
        }
    }

    private async _storeUserInfoMysql(user: any): Promise<void> {
        try {
            if (this.mysqlConn) {
                await this.mysqlConn.execute("INSERT INTO user_info (user_id, name, avatar, display_name) VALUES (?, ?, ?, ?)",
                    [user.id, user.name, user.avatar, user.display_name]);
            }
        } catch (e) {
            console.error(`MySQL error while storing user info: ${e}`);
        }
    }

    private async _storeUserInfoRedis(user: any): Promise<void> {
        try {
            if (this.redisClient) {
                await this.redisClient.hSet(`user_info:${user.id}`, { name: user.name, avatar: user.avatar, display_name: user.display_name });
            }
        } catch (e) {
            console.error(`Redis error while storing user info: ${e}`);
        }
    }

    async monitorUserInfoChanges(user: any): Promise<void> {
        await this._monitorUserInfoChangesSqlite(user);
        await this._monitorUserInfoChangesMongodb(user);
        await this._monitorUserInfoChangesMysql(user);
        await this._monitorUserInfoChangesRedis(user);
    }

    private async _monitorUserInfoChangesSqlite(user: any): Promise<void> {
        try {
            if (this.localDbConn) {
                this.localDbConn.get("SELECT name, avatar, display_name FROM user_info WHERE user_id = ?", [user.id], (err, row) => {
                    if (err) {
                        console.error(`SQLite error while monitoring user info changes: ${err}`);
                    } else if (row) {
                        const { name: oldName, avatar: oldAvatar, display_name: oldDisplayName } = row;
                        if (oldName !== user.name || oldAvatar !== user.avatar || oldDisplayName !== user.display_name) {
                            this.storeUserInfo(user);
                        }
                    }
                });
            }
        } catch (e) {
            console.error(`SQLite error while monitoring user info changes: ${e}`);
        }
    }

    private async _monitorUserInfoChangesMongodb(user: any): Promise<void> {
        try {
            if (this.mongoClient) {
                const db = this.mongoClient.db(process.env.MONGODB_DATABASE);
                const collection = db.collection("user_info");
                const result = await collection.findOne({ user_id: user.id });
                if (result) {
                    const { name: oldName, avatar: oldAvatar, display_name: oldDisplayName } = result;
                    if (oldName !== user.name || oldAvatar !== user.avatar || oldDisplayName !== user.display_name) {
                        this.storeUserInfo(user);
                    }
                }
            }
        } catch (e) {
            console.error(`MongoDB error while monitoring user info changes: ${e}`);
        }
    }

    private async _monitorUserInfoChangesMysql(user: any): Promise<void> {
        try {
            if (this.mysqlConn) {
                const [rows] = await this.mysqlConn.execute("SELECT name, avatar, display_name FROM user_info WHERE user_id = ?", [user.id]);
                if (rows.length) {
                    const { name: oldName, avatar: oldAvatar, display_name: oldDisplayName } = rows[0];
                    if (oldName !== user.name || oldAvatar !== user.avatar || oldDisplayName !== user.display_name) {
                        this.storeUserInfo(user);
                    }
                }
            }
        } catch (e) {
            console.error(`MySQL error while monitoring user info changes: ${e}`);
        }
    }

    private async _monitorUserInfoChangesRedis(user: any): Promise<void> {
        try {
            if (this.redisClient) {
                const result = await this.redisClient.hGetAll(`user_info:${user.id}`);
                if (result) {
                    const { name: oldName, avatar: oldAvatar, display_name: oldDisplayName } = result;
                    if (oldName !== user.name || oldAvatar !== user.avatar || oldDisplayName !== user.display_name) {
                        this.storeUserInfo(user);
                    }
                }
            }
        } catch (e) {
            console.error(`Redis error while monitoring user info changes: ${e}`);
        }
    }
}

export default UserInfoManager;
