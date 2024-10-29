import { Client, Message } from 'discord.js-selfbot-v13';
import { Command } from 'discord-akairo';
import { errorHandler } from '../../utils/error_handler';

class HelpCog {
    private client: Client;

    constructor(client: Client) {
        this.client = client;
    }

    @Command({
        aliases: ['help'],
        description: 'Display help information for all categories or a specific category.',
        args: [
            { id: 'input', type: 'string', match: 'rest', default: null }
        ]
    })
    @errorHandler
    async helpCommand(message: Message, { input }: { input: string | null }) {
        const prefix = this.client.commandPrefix;
        const version = "1.0";
        const author = "outmaneuver";

        if (!message.channel.permissionsFor(message.author)?.sendMessages) {
            await message.author.send("You do not have permission to send messages in this channel.");
            return;
        }

        if (!input) {
            await this.sendAllCategories(message, prefix);
        } else {
            await this.sendCategoryCommands(message, input, prefix);
        }
    }

    async sendAllCategories(message: Message, prefix: string) {
        let helpMessage = `Help\nUse \`${prefix}help <category>\` to get more information on a category.\n\nCategories:\n`;
        for (const cog of this.client.cogs.values()) {
            helpMessage += `\`${cog.id}\` ${cog.description}\n`;
        }
        await message.channel.send(`\`\`\`${helpMessage}\`\`\``);
    }

    async sendCategoryCommands(message: Message, category: string, prefix: string) {
        const cog = this.client.cogs.get(category);
        if (cog) {
            let helpMessage = `${category} - Commands\n${cog.description}\n\n`;
            for (const command of cog.commands.values()) {
                helpMessage += `\`${prefix}${command.id}\`: ${command.description}\n`;
            }
            await message.channel.send(`\`\`\`${helpMessage}\`\`\``);
        } else {
            await message.channel.send(`Category \`${category}\` not found.`);
        }
    }
}

export function setup(client: Client) {
    return new HelpCog(client);
}
