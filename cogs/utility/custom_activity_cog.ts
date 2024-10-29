import { Client, Message } from 'discord.js-selfbot-v13';
import { Command } from 'discord-akairo';
import { errorHandler } from '../../utils/error_handler';
import { hasPermissionsToSendMessages } from '../../utils/permissions';
import { ActivityType } from 'discord.js-selfbot-v13';

class CustomActivityCog {
    private client: Client;

    constructor(client: Client) {
        this.client = client;
    }

    private createActivity(activityType: string, activityName: string | null) {
        switch (activityType.toLowerCase()) {
            case 'playing':
                return { type: ActivityType.Playing, name: activityName };
            case 'streaming':
                return { type: ActivityType.Streaming, name: activityName, url: 'https://twitch.tv/streamer' };
            case 'listening':
                return { type: ActivityType.Listening, name: activityName };
            case 'watching':
                return { type: ActivityType.Watching, name: activityName };
            case 'custom':
                return { type: ActivityType.Custom, name: activityName };
            default:
                return null;
        }
    }

    @Command({
        aliases: ['setactivity'],
        description: 'Set a custom activity status.',
        args: [
            { id: 'activityType', type: 'string' },
            { id: 'activityName', type: 'string', default: null }
        ]
    })
    @errorHandler
    @hasPermissionsToSendMessages()
    async setActivity(message: Message, { activityType, activityName }: { activityType: string, activityName: string | null }) {
        const activity = this.createActivity(activityType, activityName);
        if (!activity) {
            await message.channel.send("Invalid activity type. Please choose from playing, streaming, listening, watching, or custom.");
            return;
        }

        await this.client.user.setActivity(activityName, { type: activity.type, url: activity.url });
        await message.channel.send(`Activity set to ${activityType} ${activityName}`);
    }

    @Command({
        aliases: ['clearactivity'],
        description: 'Clear the custom activity status.'
    })
    @errorHandler
    @hasPermissionsToSendMessages()
    async clearActivity(message: Message) {
        await this.client.user.setActivity(null);
        await message.channel.send("Activity cleared");
    }
}

export function setup(client: Client) {
    return new CustomActivityCog(client);
}
