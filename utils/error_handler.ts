import { Message } from 'discord.js-selfbot-v13';

export async function errorHandler(func: Function) {
    return async function (message: Message, ...args: any[]) {
        try {
            await func(message, ...args);
        } catch (error) {
            if (error.name === 'CommandNotFound') {
                await message.channel.send("Sorry, I didn't understand that command.");
            } else if (error.name === 'MissingRequiredArgument') {
                await message.channel.send("It looks like you're missing a required argument.");
            } else if (error.name === 'BadArgument') {
                await message.channel.send("There was an issue with one of the arguments you provided.");
            } else if (error.name === 'CommandInvokeError') {
                await message.channel.send("There was an error while executing the command.");
            } else {
                await message.channel.send(`An unexpected error occurred: ${error.message}`);
            }
        }
    };
}
