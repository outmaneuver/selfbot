import { Client, Message, GuildMember, Role } from 'discord.js-selfbot-v13';
import { Command } from 'discord-akairo';
import { errorHandler } from '../../utils/error_handler';
import { hasPermissionsToSendMessages } from '../../utils/permissions';
import { kickOrBan } from '../../utils/moderation_utils';

class ModerationCog {
    private client: Client;

    constructor(client: Client) {
        this.client = client;
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
        if (!user) {
            await message.channel.send("Invalid user. Please mention a valid user.");
            return;
        }
        await kickOrBan(message, [user], action as 'kick' | 'ban', reason);
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
        await kickOrBan(message, users, action as 'kick' | 'ban', reason);
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
        await kickOrBan(message, members, action as 'kick' | 'ban', reason);
    }
}

export function setup(client: Client) {
    return new ModerationCog(client);
}
