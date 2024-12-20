# selfbot

## Description

This selfbot utilizes a local database and has the option to utilize external databases such as MongoDB, MySQL, and Redis. It handles multiple users and subscribes to guilds, storing username, avatar, and display name changes of users for every guild a user using the selfbot is in.

## Features

- Local database support
- External database support (MongoDB, MySQL, Redis)
- Handles multiple users
- Subscribes to guilds
- Monitors and stores changes in username, avatar history, and display name history for indexed Discord users
- Global error handler for better error management
- Modularized database connection logic for better code organization
- Determines which database to use if other databases aren't configured
- Warns the user if other databases aren't set up and uses a local database
- Caching for other functionalities even if no external database is set up
- Auto-updater functionality to keep the selfbot up-to-date with the repository

## Setup and Running

1. Clone the repository:
   ```
   git clone https://github.com/outmaneuver/selfbot.git
   cd selfbot
   ```

2. Install the required dependencies:
   ```
   bun install
   ```

3. Configure the selfbot by editing the `.env` file with your database connection details and other configurations.

4. Build the TypeScript project:
   ```
   bun run build
   ```

5. Run the selfbot:
   ```
   bun run start
   ```

## Configuring the Auto-Updater

To configure the auto-updater, add the following environment variables to your `.env` file:

```
# Auto-updater configuration
AUTO_UPDATE=true
UPDATE_INTERVAL=3600
```

- `AUTO_UPDATE`: Set to `true` to enable the auto-updater, or `false` to disable it.
- `UPDATE_INTERVAL`: The interval (in seconds) at which the auto-updater checks for updates. Default is `3600` seconds (1 hour).

## Basic Usage

### Utility Cogs

- `!namehistory [user]`: Request a user's name history. Defaults to the selfbot user if no user is mentioned.
- `!avatar <action> [user]`: Request a user's avatar history or current avatar. Defaults to the selfbot user if no user is mentioned.
- `!setactivity <activity_type> <activity_name> <rich_presence_settings>`: Set a custom activity status, including rich presence settings.
- `!clearactivity`: Clear the custom activity status
- `!purge [channel_id] [delay]`: Purge a selfbot user's messages in a specified channel with an optional delay between deletions. If no channel ID is provided, it will purge messages in the current channel. The delay is in seconds and defaults to 1.0.
- `!react <action> [user_ids] <emojis>`: Enable, disable, or list auto-react for specified users with given emojis.
- `!help [category]`: Display help information for all categories or a specific category.
- `!list`: List users with auto-react enabled and their respective emojis.

### Moderation Cogs

- `!moderate <action> <user> [reason]`: Moderate a user by kicking or banning them from the server.
- `!massmoderate <action> <user1> <user2> ... [reason]`: Moderate multiple users by kicking or banning them from the server.
- `!moderaterole <action> <role> [reason]`: Moderate all users with a specific role by kicking or banning them from the server.
- `!kick <user> [reason]`: Kick a user from the server
- `!ban <user> [reason]`: Ban a user from the server
- `!masskick <user1> <user2> ... [reason]`: Kick multiple users from the server
- `!massban <user1> <user2> ... [reason]`: Ban multiple users from the server
- `!kickrole <role> [reason]`: Kick all users with a specific role from the server
- `!banrole <role> [reason]`: Ban all users with a specific role from the server

### Example of Setting Rich Presence

To set a rich presence using the `!setactivity` command, you can use the following example:

```
!setactivity richpresence null {
  "applicationId": "367827983903490050",
  "type": "PLAYING",
  "url": "https://www.youtube.com/watch?v=5icFcPkVzMg",
  "state": "Arcade Game",
  "name": "osu!",
  "details": "MariannE - Yooh",
  "party": {
    "max": 8,
    "current": 1
  },
  "startTimestamp": 1633024800000,
  "assetsLargeImage": "https://assets.ppy.sh/beatmaps/1550633/covers/list.jpg",
  "assetsLargeText": "Idle",
  "assetsSmallImage": "373370493127884800",
  "assetsSmallText": "click the circles",
  "platform": "desktop",
  "buttonLabel": "Beatmap",
  "buttonURL": "https://osu.ppy.sh/beatmapsets/1391659#osu/2873429"
}
```
