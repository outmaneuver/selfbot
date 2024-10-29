import { Client, Message } from 'discord.js-selfbot-v13';
import { Command } from 'discord-akairo';

class ListCog {
    private client: Client;

    constructor(client: Client) {
        this.client = client;
    }

    @Command({
        aliases: ['list'],
        description: 'List users with auto-react enabled and their respective emojis.'
    })
    async listCommand(message: Message) {
        const autoreactCog = this.client.cogs.get('AutoReactCog');
        if (autoreactCog) {
            const userReactions = autoreactCog.userReactions;
            if (userReactions && Object.keys(userReactions).length > 0) {
                let response = "Auto-react enabled for the following users:\n";
                for (const [userId, emojis] of Object.entries(userReactions)) {
                    response += `User ID: ${userId}, Emojis: ${Array.from(emojis).join(', ')}\n`;
                }
                await message.channel.send(`\`\`\`${response}\`\`\``);
            } else {
                await message.channel.send("No users have auto-react enabled.");
            }
        } else {
            await message.channel.send("AutoReactCog is not loaded.");
        }
    }
}

export function setup(client: Client) {
    return new ListCog(client);
}
