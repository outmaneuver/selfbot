import { Client, Message, GuildMember } from 'discord.js-selfbot-v13';
import { Command } from 'discord-akairo';
import { RateLimiter } from '../../utils/rate_limiter';
import { hasPermissionsToUseExternalEmojis } from '../../utils/permissions';
import { enableReactions, disableReactions, listReactions } from '../../utils/autoreact_utils';

class AutoReactCog {
    private client: Client;
    private userReactions: { [key: string]: Set<string> };
    private rateLimiter: RateLimiter;

    constructor(client: Client) {
        this.client = client;
        this.userReactions = {};
        this.rateLimiter = new RateLimiter();
    }

    @Command({
        aliases: ['react'],
        description: 'Enable, disable, or list auto-react for specified users with given emojis.',
        args: [
            { id: 'action', type: 'string' },
            { id: 'userIds', type: 'string', match: 'rest', default: null },
            { id: 'emojis', type: 'string', match: 'rest', default: null }
        ]
    })
    @hasPermissionsToUseExternalEmojis()
    async react(message: Message, { action, userIds, emojis }: { action: string, userIds: string | null, emojis: string | null }) {
        if (!['enable', 'disable', 'list'].includes(action.toLowerCase())) {
            await message.channel.send("Invalid action. Please choose 'enable', 'disable', or 'list'.");
            return;
        }

        if (action.toLowerCase() === 'list') {
            await listReactions(message, this.userReactions);
            return;
        }

        const userIdArray = userIds ? userIds.split(' ').map(id => id.trim()) : [message.author.id];
        const emojiArray = emojis ? emojis.split(' ').map(emoji => emoji.trim()) : [];

        for (const userId of userIdArray) {
            if (action.toLowerCase() === 'enable') {
                await enableReactions(message, userId, emojiArray, this.userReactions);
            } else if (action.toLowerCase() === 'disable') {
                await disableReactions(message, userId, this.userReactions);
            }
        }
    }

    @Client.on('message')
    async onMessage(message: Message) {
        try {
            if (this.userReactions[message.author.id]) {
                for (const emoji of this.userReactions[message.author.id]) {
                    await this.rateLimiter.wait();
                    await message.react(emoji);
                }
            }
        } catch (error) {
            console.error(`Failed to react to message. Error: ${error.message}`);
        }
    }
}

export function setup(client: Client) {
    return new AutoReactCog(client);
}
