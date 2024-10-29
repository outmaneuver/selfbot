import { Client, Message, TextChannel } from 'discord.js-selfbot-v13';
import { Command } from 'discord-akairo';
import { RateLimiter } from '../../utils/rate_limiter';
import { errorHandler } from '../../utils/error_handler';

class PurgeCog {
    private client: Client;
    private rateLimiter: RateLimiter;

    constructor(client: Client) {
        this.client = client;
        this.rateLimiter = new RateLimiter();
    }

    @Command({
        aliases: ['purge'],
        description: 'Purge selfbot user messages in a specified channel with an optional delay between deletions.',
        args: [
            { id: 'channelId', type: 'number', default: null },
            { id: 'delay', type: 'number', default: 1.0 }
        ]
    })
    @errorHandler
    async purge(message: Message, { channelId, delay }: { channelId: number | null, delay: number }) {
        let channel: TextChannel | null = null;

        if (channelId === null) {
            channel = message.channel as TextChannel;
        } else {
            channel = this.client.channels.cache.get(channelId.toString()) as TextChannel;
        }

        if (!channel) {
            await message.channel.send("Invalid channel ID.");
            return;
        }

        const messages = await channel.messages.fetch({ limit: 100 });
        for (const msg of messages.values()) {
            if (msg.author.id === this.client.user?.id) {
                await this.rateLimiter.wait();
                await msg.delete();
                await new Promise(resolve => setTimeout(resolve, delay * 1000));
            }
        }
    }
}

export function setup(client: Client) {
    return new PurgeCog(client);
}
