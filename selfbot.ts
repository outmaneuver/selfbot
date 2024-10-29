import { Client, Intents } from 'discord.js-selfbot-v13';
import { config } from 'dotenv';
import { CommandHandler } from './utils/command_handler';
import { errorHandler } from './utils/error_handler';

config();

class SelfBot extends CommandHandler {
    constructor() {
        super();
    }

    @errorHandler
    async onCommandError(message, error) {
        await super.onCommandError(message, error);
    }

    async onGuildJoin(guild) {
        for (const member of guild.members.cache.values()) {
            this.databaseManager.storeUserInfo(member);
        }
    }

    async onMemberUpdate(oldMember, newMember) {
        if (oldMember.user.username !== newMember.user.username || oldMember.user.avatar !== newMember.user.avatar || oldMember.displayName !== newMember.displayName) {
            this.databaseManager.storeUserInfo(newMember);
        }
    }

    async onReady() {
        console.log(`Logged in as ${this.user.tag}`);
        await this.loadCustomActivitySettings();
        for (const guild of this.guilds.cache.values()) {
            for (const member of guild.members.cache.values()) {
                this.databaseManager.storeUserInfo(member);
            }
        }
    }
}

const client = new SelfBot({
    ws: { intents: Intents.ALL }
});

client.login(process.env.TOKEN);
