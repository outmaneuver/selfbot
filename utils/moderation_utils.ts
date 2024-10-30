import { Message, GuildMember } from 'discord.js-selfbot-v13';

export async function kickOrBan(message: Message, users: GuildMember[], action: 'kick' | 'ban', reason: string | null) {
    for (const user of users) {
        try {
            if (action === 'kick') {
                await user.kick(reason);
                await message.channel.send(`Successfully kicked ${user.user.tag}.`);
            } else if (action === 'ban') {
                await user.ban({ reason });
                await message.channel.send(`Successfully banned ${user.user.tag}.`);
            }
        } catch (error) {
            await message.channel.send(`Failed to ${action} ${user.user.tag}. Error: ${error.message}`);
        }
    }
}
