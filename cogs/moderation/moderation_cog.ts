import { Client, Message, GuildMember, Role } from 'discord.js-selfbot-v13';
import { Command } from 'discord-akairo';
import { errorHandler } from '../../utils/error_handler';
import { hasPermissionsToSendMessages } from '../../utils/permissions';

class ModerationCog {
    private client: Client;

    constructor(client: Client) {
        this.client = client;
    }

    private async _kickOrBan(message: Message, users: GuildMember[], action: 'kick' | 'ban', reason: string | null) {
        const actionFunc = action === 'kick' ? 'kick' : 'ban';
        const affectedUsers: string[] = [];
        for (const user of users) {
            await user[actionFunc](reason || undefined);
            affectedUsers.push(user.user.username);
        }
        await message.channel.send(`${affectedUsers.length} users have been ${action}ed from the server. Reason: ${reason || 'No reason provided'}.`);
    }

    @Command({
        aliases: ['moderate'],
        description: 'Moderate a user by kicking or banning them from the server.',
        args: [
            { id: 'action', type: 'string' },
            { id: 'user', type: 'member' },
            { id: 'reason', type: 'string', match: 'rest', default: null }
        ]
    })
    @errorHandler
    @hasPermissionsToSendMessages()
    async moderate(message: Message, { action, user, reason }: { action: string, user: GuildMember, reason: string | null }) {
        if (!['kick', 'ban'].includes(action.toLowerCase())) {
            await message.channel.send("Invalid action. Please choose 'kick' or 'ban'.");
            return;
        }
        await this._kickOrBan(message, [user], action as 'kick' | 'ban', reason);
    }

    @Command({
        aliases: ['massmoderate'],
        description: 'Moderate multiple users by kicking or banning them from the server.',
        args: [
            { id: 'action', type: 'string' },
            { id: 'users', type: 'members' },
            { id: 'reason', type: 'string', match: 'rest', default: null }
        ]
    })
    @errorHandler
    @hasPermissionsToSendMessages()
    async massModerate(message: Message, { action, users, reason }: { action: string, users: GuildMember[], reason: string | null }) {
        if (!['kick', 'ban'].includes(action.toLowerCase())) {
            await message.channel.send("Invalid action. Please choose 'kick' or 'ban'.");
            return;
        }
        await this._kickOrBan(message, users, action as 'kick' | 'ban', reason);
    }

    @Command({
        aliases: ['moderaterole'],
        description: 'Moderate all users with a specific role by kicking or banning them from the server.',
        args: [
            { id: 'action', type: 'string' },
            { id: 'role', type: 'role' },
            { id: 'reason', type: 'string', match: 'rest', default: null }
        ]
    })
    @errorHandler
    @hasPermissionsToSendMessages()
    async moderateRole(message: Message, { action, role, reason }: { action: string, role: Role, reason: string | null }) {
        if (!['kick', 'ban'].includes(action.toLowerCase())) {
            await message.channel.send("Invalid action. Please choose 'kick' or 'ban'.");
            return;
        }
        const members = role.members.array();
        await this._kickOrBan(message, members, action as 'kick' | 'ban', reason);
    }
}

export function setup(client: Client) {
    return new ModerationCog(client);
}
