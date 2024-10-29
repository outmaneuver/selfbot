import { Client, Message, GuildMember } from 'discord.js-selfbot-v13';
import { Command } from 'discord-akairo';
import { RateLimiter } from '../../utils/rate_limiter';
import { hasPermissionsToUseExternalEmojis } from '../../utils/permissions';

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
            await this.listReactions(message);
            return;
        }

        const userIdArray = userIds ? userIds.split(' ').map(id => id.trim()) : [message.author.id];
        const emojiArray = emojis ? emojis.split(' ').map(emoji => emoji.trim()) : [];

        for (const userId of userIdArray) {
            if (action.toLowerCase() === 'enable') {
                await this.enableReactions(message, userId, emojiArray);
            } else if (action.toLowerCase() === 'disable') {
                await this.disableReactions(message, userId);
            }
        }
    }

    async listReactions(message: Message) {
        if (Object.keys(this.userReactions).length > 0) {
            let response = "Auto-react enabled for the following users:\n";
            for (const [userId, emojis] of Object.entries(this.userReactions)) {
                response += `User ID: ${userId}, Emojis: ${Array.from(emojis).join(', ')}\n`;
            }
            await message.channel.send(`\`\`\`${response}\`\`\``);
        } else {
            await message.channel.send("No users have auto-react enabled.");
        }
    }

    async enableReactions(message: Message, userId: string, emojis: string[]) {
        if (!this.userReactions[userId]) {
            this.userReactions[userId] = new Set();
        }
        emojis.forEach(emoji => this.userReactions[userId].add(emoji));
        await message.channel.send(`Auto-react enabled for user: ${userId} with emojis: ${emojis.join(', ')}`);
    }

    async disableReactions(message: Message, userId: string) {
        if (this.userReactions[userId]) {
            delete this.userReactions[userId];
            await message.channel.send(`Auto-react disabled for user: ${userId}`);
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
