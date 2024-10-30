export async function enableReactions(message, userId, emojiArray, userReactions) {
    if (!userReactions[userId]) {
        userReactions[userId] = new Set();
    }
    for (const emoji of emojiArray) {
        userReactions[userId].add(emoji);
    }
    await message.channel.send(`Auto-react enabled for user ID: ${userId} with emojis: ${emojiArray.join(', ')}`);
}

export async function disableReactions(message, userId, userReactions) {
    if (userReactions[userId]) {
        delete userReactions[userId];
        await message.channel.send(`Auto-react disabled for user ID: ${userId}`);
    } else {
        await message.channel.send(`No auto-react found for user ID: ${userId}`);
    }
}

export async function listReactions(message, userReactions) {
    if (userReactions && Object.keys(userReactions).length > 0) {
        let response = "Auto-react enabled for the following users:\n";
        for (const [userId, emojis] of Object.entries(userReactions)) {
            response += `User ID: ${userId}, Emojis: ${Array.from(emojis).join(', ')}\n`;
        }
        await message.channel.send(`\`\`\`${response}\`\`\``);
    } else {
        await message.channel.send("No users have auto-react enabled.");
    }
}
