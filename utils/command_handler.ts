import { Client, Intents } from 'discord.js-selfbot-v13';
import { config } from 'dotenv';
import { readdirSync } from 'fs';
import { join } from 'path';
import { DatabaseManager } from './database';
import { CacheManager } from './cache';
import { RateLimiter } from './rate_limiter';
import { errorHandler } from './error_handler';

config();

class CommandHandler extends Client {
    private databaseManager: DatabaseManager;
    private cacheManager: CacheManager;
    private rateLimiter: RateLimiter;

    constructor() {
        super({ ws: { intents: Intents.ALL } });
        this.databaseManager = new DatabaseManager();
        this.cacheManager = new CacheManager();
        this.rateLimiter = new RateLimiter();
        this.loadCogs();
    }

    private loadCogs() {
        const cogDirectories = ['cogs/utility', 'cogs/moderation'];
        for (const directory of cogDirectories) {
            const cogFiles = readdirSync(join(__dirname, '..', directory)).filter(file => file.endsWith('.ts'));
            for (const file of cogFiles) {
                const { setup } = require(join(__dirname, '..', directory, file));
                setup(this);
            }
        }
    }

    @errorHandler
    async onCommandError(message, error) {
        if (error.name === 'CommandNotFound') {
            await message.channel.send("Sorry, I didn't understand that command.");
        } else if (error.name === 'MissingRequiredArgument') {
            await message.channel.send("It looks like you're missing a required argument.");
        } else if (error.name === 'BadArgument') {
            await message.channel.send("There was an issue with one of the arguments you provided.");
        } else if (error.name === 'CommandInvokeError') {
            await message.channel.send("There was an error while executing the command.");
        } else {
            await message.channel.send("An unexpected error occurred. Please try again later.");
        }
    }

    async onReady() {
        console.log(`Logged in as ${this.user.tag}`);
        await this.loadCustomActivitySettings();
    }

    async onMemberUpdate(oldMember, newMember) {
        if (oldMember.user.username !== newMember.user.username || oldMember.user.avatar !== newMember.user.avatar || oldMember.displayName !== newMember.displayName) {
            this.databaseManager.storeUserInfo(newMember);
        }
    }

    private async loadCustomActivitySettings() {
        try {
            const settings = this.databaseManager.retrieveCustomActivitySettings(this.user.id);
            if (settings) {
                await this.user.setActivity(settings);
            }
        } catch (e) {
            console.error(`Error loading custom activity settings: ${e}`);
        }
    }

    async saveCustomActivitySettings(settings) {
        try {
            this.databaseManager.storeCustomActivitySettings(this.user.id, settings);
        } catch (e) {
            console.error(`Error saving custom activity settings: ${e}`);
        }
    }

    async apiCall(...args) {
        await this.rateLimiter.wait();
        try {
            const response = await super.apiCall(...args);
            if (response.status === 429) {
                const retryAfter = response.headers.get("Retry-After");
                if (retryAfter) {
                    this.rateLimiter.updateRateLimit(parseFloat(retryAfter));
                }
            }
            return response;
        } catch (e) {
            console.error(`Error making API call: ${e}`);
            throw e;
        }
    }

    fetchFromCache(key: string) {
        return this.cacheManager.fetchFromCache(key);
    }

    storeInCache(key: string, value: any) {
        this.cacheManager.storeInCache(key, value);
    }
}

export { CommandHandler };
