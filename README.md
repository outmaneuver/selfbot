# selfbot

## Description

This selfbot utilizes a local database and has the option to utilize external databases such as MongoDB, MySQL, and Redis. It handles multiple users and subscribes to guilds, storing username, avatar, and display name changes of users for every guild a user using the selfbot is in.

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

## Commands

- `!namehistory <user>`: Request a user's name history
- `!avhistory <user>`: Request a user's avatar history
- `!currentav <user>`: Request a user's current avatar
- `!kick <user> [reason]`: Kick a user from the server
- `!ban <user> [reason]`: Ban a user from the server
- `!masskick <user1> <user2> ... [reason]`: Kick multiple users from the server
- `!massban <user1> <user2> ... [reason]`: Ban multiple users from the server
- `!kickrole <role> [reason]`: Kick all users with a specific role from the server
- `!banrole <role> [reason]`: Ban all users with a specific role from the server

The output will be formatted in codeblocks.

## Configuration

To configure the selfbot, you need to provide the necessary database connection details in the `.env` file. The selfbot supports the following configuration options:

- Local database
- MongoDB
- MySQL
- Redis

If no external databases are configured, the selfbot will set up a local database and warn the user.

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

## Library

This selfbot utilizes the `discord.py-self` library for its functionality.

## Contributing

We welcome contributions to the selfbot project! If you would like to contribute, please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file for detailed instructions on how to get started.
