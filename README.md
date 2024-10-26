# selfbot

## Description

This selfbot utilizes a local database and has the option to utilize external databases such as MongoDB, MySQL, and Redis. It handles multiple users and subscribes to guilds, storing username, avatar, and display name changes of users for every guild a user using the selfbot is in. Redis is now utilized as a cache rather than a database.

## Features

- Local database support
- External database support (MongoDB, MySQL, Redis)
- Handles multiple users
- Subscribes to guilds
- Stores username, avatar, and display name changes
- Global error handler for better error management
- Modularized database connection logic for better code organization
- Determines which database to use if other databases aren't configured
- Warns the user if other databases aren't set up and uses a local database
- Global rate limiter utilizing the retry-after response from Discord
- Redis caching for avatar and name history
- Caching for other functionalities even if no external database is set up

## Commands

- `!namehistory [user]`: Request a user's name history. Defaults to the selfbot user if no user is mentioned.
- `!avhistory [user]`: Request a user's avatar history. Defaults to the selfbot user if no user is mentioned.
- `!currentav [user]`: Request a user's current avatar. Defaults to the selfbot user if no user is mentioned.
- `!kick <user> [reason]`: Kick a user from the server
- `!ban <user> [reason]`: Ban a user from the server
- `!masskick <user1> <user2> ... [reason]`: Kick multiple users from the server
- `!massban <user1> <user2> ... [reason]`: Ban multiple users from the server
- `!kickrole <role> [reason]`: Kick all users with a specific role from the server
- `!banrole <role> [reason]`: Ban all users with a specific role from the server
- `!setactivity <activity_type> <activity_name>`: Set a custom activity status
- `!clearactivity`: Clear the custom activity status

The output will be formatted in codeblocks.

## Configuration

To configure the selfbot, you need to provide the necessary database connection details in the `.env` file. The selfbot supports the following configuration options:

- Local database
- MongoDB
- MySQL
- Redis (used as a cache)

If no external databases are configured, the selfbot will set up a local database and warn the user. Redis will be used as a cache for avatar and name history, as well as other functionalities. If Redis is not set up, an alternative caching mechanism will be used.

## Setup and Running

1. Clone the repository:
   ```
   git clone https://github.com/outmaneuver/selfbot.git
   cd selfbot
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure the selfbot by editing the `.env` file with your database connection details and other configurations.

4. Run the selfbot:
   ```
   python selfbot.py
   ```

## Examples

Here are some examples of how to use the commands:

- Request a user's name history:
  ```
  !namehistory @username
  ```

- Request a user's avatar history:
  ```
  !avhistory @username
  ```

- Request a user's current avatar:
  ```
  !currentav @username
  ```

- Kick a user from the server:
  ```
  !kick @username [reason]
  ```

- Ban a user from the server:
  ```
  !ban @username [reason]
  ```

- Kick multiple users from the server:
  ```
  !masskick @username1 @username2 ... [reason]
  ```

- Ban multiple users from the server:
  ```
  !massban @username1 @username2 ... [reason]
  ```

- Kick all users with a specific role from the server:
  ```
  !kickrole @role [reason]
  ```

- Ban all users with a specific role from the server:
  ```
  !banrole @role [reason]
  ```

- Set a custom activity status:
  ```
  !setactivity playing Minecraft
  ```

- Clear the custom activity status:
  ```
  !clearactivity
  ```

## Rich Presence Elements

The custom activity now supports setting rich presence elements. Here are the available elements and their descriptions:

- `status`: Enable or disable the status (True/False)
- `presence`: Enable or disable the presence (True/False)
- `type`: The type of activity (e.g., gaming, streaming, etc.)
- `mode`: The mode of the activity (e.g., idle, dnd, etc.)
- `application_id`: The application ID for the activity
- `url`: The URL for the activity (requires a valid Twitch stream URL)
- `details`: Additional details about the activity
- `state`: The state of the activity
- `name`: The name of the activity
- `timestamp`: Enable or disable the timestamp (True/False)
- `hidden`: Hide or show the activity (True/False)
- `party`: Enable or disable the party (True/False)
- `party_size_min`: The minimum party size
- `party_size_max`: The maximum party size
- `small_text`: Small text for the activity
- `large_text`: Large text for the activity
- `small_image_key`: The key for the small image
- `large_image_key`: The key for the large image
- `button_one`: The first button (URL and text)
- `button_two`: The second button (URL and text)

## Storing Custom Activity Settings

To store custom activity settings so they persist across sessions, the selfbot supports storing the settings in both local and external databases. The settings will be loaded on startup and saved when they are set.

## Library

This selfbot utilizes the `discord.py-self` library for its functionality.

## Contributing

We welcome contributions to the selfbot project! If you would like to contribute, please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file for detailed instructions on how to get started.
