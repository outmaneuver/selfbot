import { Client, Message, User } from 'discord.js-selfbot-v13';
import { Command } from 'discord-akairo';
import { fetchNameHistory, fetchAvatarHistory } from '../../utils/database';
import { errorHandler } from '../../utils/error_handler';
import { hasPermissionsToSendMessages, hasPermissionsToSendImages } from '../../utils/permissions';

class NameHistoryCog {
    private client: Client;
    private localCache: any;

    constructor(client: Client) {
        this.client = client;
        this.localCache = client.localCache;
    }

    @Command({
        aliases: ['namehistory'],
        description: 'Fetch name history of a user.',
        args: [
            { id: 'user', type: 'user', default: null }
        ]
    })
    @errorHandler
    @hasPermissionsToSendMessages()
    async nameHistory(message: Message, { user }: { user: User | null }) {
        if (!user) {
            user = message.author;
        }

        const nameHistory = this.fetchNameHistory(user.id);
        if (nameHistory.length > 0) {
            await message.channel.send(`Here's the name history for ${user.username}: ${nameHistory.join(', ')}`);
        } else {
            await message.channel.send(`Sorry, I couldn't find any name history for ${user.username}.`);
        }
    }

    fetchNameHistory(userId: string) {
        return fetchNameHistory(userId, this.localCache);
    }

    fetchAvatarHistory(userId: string) {
        return fetchAvatarHistory(userId, this.localCache);
    }
}

export function setup(client: Client) {
    return new NameHistoryCog(client);
}
