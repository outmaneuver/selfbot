import { Client, Message, User } from 'discord.js-selfbot-v13';
import { Command } from 'discord-akairo';
import { errorHandler } from '../../utils/error_handler';
import { hasPermissionsToSendImages } from '../../utils/permissions';
import DatabaseManager from '../../utils/database';

class AvatarHistoryCog {
    private client: Client;
    private databaseManager: DatabaseManager;

    constructor(client: Client) {
        this.client = client;
        this.databaseManager = new DatabaseManager();
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

        try {
            if (action.toLowerCase() === 'history') {
                const avatarHistory = await this.databaseManager.fetch_avatar_history(user.id);
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
        } catch (error) {
            console.error(`Failed to fetch avatar history. Error: ${error.message}`);
            await message.channel.send(`An error occurred while fetching avatar history for ${user.username}. Please try again later.`);
        }
    }
}

export function setup(client: Client) {
    return new AvatarHistoryCog(client);
}
