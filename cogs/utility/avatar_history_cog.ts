import { Client, Message, User } from 'discord.js-selfbot-v13';
import { Command } from 'discord-akairo';
import { fetchAvatarHistory, fetchNameHistory } from '../../utils/database';
import { errorHandler } from '../../utils/error_handler';
import { hasPermissionsToSendImages } from '../../utils/permissions';

class AvatarHistoryCog {
    private client: Client;
    private localCache: any;

    constructor(client: Client) {
        this.client = client;
        this.localCache = client.localCache;
    }

    @Command({
        aliases: ['avatar'],
        description: 'Fetch avatar history or current avatar of a user.',
        args: [
            { id: 'action', type: 'string' },
            { id: 'user', type: 'user', default: null }
        ]
    })
    @errorHandler
    @hasPermissionsToSendImages()
    async avatarCommand(message: Message, { action, user }: { action: string, user: User | null }) {
        if (!user) {
            user = message.author;
        }

        if (action.toLowerCase() === 'history') {
            const avatarHistory = this.fetchAvatarHistory(user.id);
            if (avatarHistory.length > 0) {
                await message.channel.send(`Here's the avatar history for ${user.username}: ${avatarHistory.join(', ')}`);
            } else {
                await message.channel.send(`Sorry, I couldn't find any avatar history for ${user.username}.`);
            }
        } else if (action.toLowerCase() === 'current') {
            await message.channel.send(`Hey there! Here's the current avatar for ${user.username}: ${user.displayAvatarURL()}`);
        } else {
            await message.channel.send("Invalid action. Please choose 'history' or 'current'.");
        }
    }

    fetchAvatarHistory(userId: string) {
        return fetchAvatarHistory(userId, this.localCache);
    }

    fetchNameHistory(userId: string) {
        return fetchNameHistory(userId, this.localCache);
    }
}

export function setup(client: Client) {
    return new AvatarHistoryCog(client);
}
