import { Message } from 'discord.js-selfbot-v13';

export function hasPermissionsToSendMessages() {
    return async function (message: Message) {
        if (!message.channel.permissionsFor(message.author)?.has('SEND_MESSAGES')) {
            await message.author.send("You do not have permission to send messages in this channel.");
            return false;
        }
        return true;
    };
}

export function hasPermissionsToSendImages() {
    return async function (message: Message) {
        if (!message.channel.permissionsFor(message.author)?.has('ATTACH_FILES')) {
            await message.author.send("You do not have permission to send images in this channel.");
            return false;
        }
        return true;
    };
}

export function hasPermissionsToUseExternalEmojis() {
    return async function (message: Message) {
        if (!message.channel.permissionsFor(message.author)?.has('USE_EXTERNAL_EMOJIS')) {
            await message.author.send("You do not have permission to use external emojis in this channel.");
            return false;
        }
        return true;
    };
}
