import { Client, Intents } from 'discord.js-selfbot-v13';
import { config } from 'dotenv';
import { CommandHandler } from './utils/command_handler';
import { errorHandler } from './utils/error_handler';
import DatabaseManager from './utils/database';

config();

class SelfBot extends CommandHandler {
    private databaseManager: DatabaseManager;

    constructor() {
        super();
        this.databaseManager = new DatabaseManager();
    }

    @errorHandler
    async onCommandError(message, error) {
        await super.onCommandError(message, error);
    }

    async onGuildJoin(guild) {
        for (const member of guild.members.cache.values()) {
            this.storeUserInfo(member);
        }
    }

    async onMemberUpdate(oldMember, newMember) {
        if (oldMember.user.username !== newMember.user.username || oldMember.user.avatar !== newMember.user.avatar || oldMember.displayName !== newMember.displayName) {
            this.storeUserInfo(newMember);
        }
    }

    async onReady() {
        console.log(`Logged in as ${this.user.tag}`);
        await this.loadCustomActivitySettings();
    }

    private async storeUserInfo(member) {
        await this.databaseManager.store_user_info(member);
    }
}

const client = new SelfBot({
    ws: { intents: Intents.ALL }
});

client.login(process.env.TOKEN);
