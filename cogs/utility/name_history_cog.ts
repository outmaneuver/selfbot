import { Client, Message, User } from 'discord.js-selfbot-v13';
import { Command } from 'discord-akairo';
import { fetchNameHistory } from '../../utils/database';
import { errorHandler } from '../../utils/error_handler';
import { hasPermissionsToSendMessages } from '../../utils/permissions';

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
        const targetUser = user || message.author;

        try {
            const nameHistory = this.fetchNameHistory(targetUser.id);
            if (nameHistory.length > 0) {
                await message.channel.send(`Here's the name history for ${targetUser.username}: ${nameHistory.join(', ')}`);
            } else {
                await message.channel.send(`Sorry, I couldn't find any name history for ${targetUser.username}.`);
            }
        } catch (error) {
            console.error(`Failed to fetch name history. Error: ${error.message}`);
            await message.channel.send(`An error occurred while fetching name history for ${targetUser.username}. Please try again later.`);
        }
    }

    fetchNameHistory(userId: string) {
        return fetchNameHistory(userId, this.localCache);
    }
}

export function setup(client: Client) {
    return new NameHistoryCog(client);
}
