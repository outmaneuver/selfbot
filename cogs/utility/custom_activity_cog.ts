import { Client, Message, RichPresence, CustomStatus } from 'discord.js-selfbot-v13';
import { Command } from 'discord-akairo';
import { errorHandler } from '../../utils/error_handler';
import { hasPermissionsToSendMessages } from '../../utils/permissions';
import { ActivityType } from 'discord.js-selfbot-v13';

class CustomActivityCog {
    private client: Client;

    constructor(client: Client) {
        this.client = client;
    }

    private createRichPresence(richPresenceSettings: any) {
        const status = new RichPresence(this.client)
            .setApplicationId(richPresenceSettings.applicationId)
            .setType(richPresenceSettings.type)
            .setURL(richPresenceSettings.url)
            .setState(richPresenceSettings.state)
            .setName(richPresenceSettings.name)
            .setDetails(richPresenceSettings.details)
            .setParty(richPresenceSettings.party)
            .setStartTimestamp(richPresenceSettings.startTimestamp)
            .setAssetsLargeImage(richPresenceSettings.assetsLargeImage)
            .setAssetsLargeText(richPresenceSettings.assetsLargeText)
            .setAssetsSmallImage(richPresenceSettings.assetsSmallImage)
            .setAssetsSmallText(richPresenceSettings.assetsSmallText)
            .setPlatform(richPresenceSettings.platform)
            .addButton(richPresenceSettings.buttonLabel, richPresenceSettings.buttonURL);
        return status;
    }

    private createPlayingActivity(activityName: string) {
        return { type: ActivityType.Playing, name: activityName };
    }

    private createStreamingActivity(activityName: string) {
        return { type: ActivityType.Streaming, name: activityName, url: 'https://twitch.tv/streamer' };
    }

    private createListeningActivity(activityName: string) {
        return { type: ActivityType.Listening, name: activityName };
    }

    private createWatchingActivity(activityName: string) {
        return { type: ActivityType.Watching, name: activityName };
    }

    private createCustomActivity(activityName: string) {
        return { type: ActivityType.Custom, name: activityName };
    }

    private createActivity(activityType: string, activityName: string | null, richPresenceSettings: any = null) {
        if (activityType.toLowerCase() === 'richpresence' && richPresenceSettings) {
            return this.createRichPresence(richPresenceSettings);
        }

        switch (activityType.toLowerCase()) {
            case 'playing':
                return this.createPlayingActivity(activityName);
            case 'streaming':
                return this.createStreamingActivity(activityName);
            case 'listening':
                return this.createListeningActivity(activityName);
            case 'watching':
                return this.createWatchingActivity(activityName);
            case 'custom':
                return this.createCustomActivity(activityName);
            default:
                return null;
        }
    }

    @Command({
        aliases: ['setactivity'],
        description: 'Set a custom activity status.',
        args: [
            { id: 'activityType', type: 'string' },
            { id: 'activityName', type: 'string', default: null },
            { id: 'richPresenceSettings', type: 'json', default: null }
        ]
    })
    @errorHandler
    @hasPermissionsToSendMessages()
    async setActivity(message: Message, { activityType, activityName, richPresenceSettings }: { activityType: string, activityName: string | null, richPresenceSettings: any }) {
        const activity = this.createActivity(activityType, activityName, richPresenceSettings);
        if (!activity) {
            await message.channel.send("Invalid activity type. Please choose from playing, streaming, listening, watching, custom, or richpresence.");
            return;
        }

        try {
            if (activityType.toLowerCase() === 'richpresence') {
                await this.client.user.setPresence({ activities: [activity] });
            } else {
                await this.client.user.setActivity(activityName, { type: activity.type, url: activity.url });
            }
            await message.channel.send(`Activity set to ${activityType} ${activityName}`);
            await this.storeActivitySettings(activityType, activityName, richPresenceSettings);
        } catch (error) {
            console.error(`Failed to set activity. Error: ${error.message}`);
            await message.channel.send(`An error occurred while setting the activity. Please try again later.`);
        }
    }

    @Command({
        aliases: ['clearactivity'],
        description: 'Clear the custom activity status.'
    })
    @errorHandler
    @hasPermissionsToSendMessages()
    async clearActivity(message: Message) {
        try {
            await this.client.user.setActivity(null);
            await message.channel.send("Activity cleared");
        } catch (error) {
            console.error(`Failed to clear activity. Error: ${error.message}`);
            await message.channel.send(`An error occurred while clearing the activity. Please try again later.`);
        }
    }

    private async storeActivitySettings(activityType: string, activityName: string | null, richPresenceSettings: any) {
        const settings = {
            activityType,
            activityName,
            richPresenceSettings
        };
        try {
            await this.client.databaseManager.store_custom_activity_settings(this.client.user.id, settings);
        } catch (error) {
            console.error(`Failed to store activity settings. Error: ${error.message}`);
        }
    }
}

export function setup(client: Client) {
    return new CustomActivityCog(client);
}
