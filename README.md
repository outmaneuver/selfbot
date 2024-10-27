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

## Basic Usage

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
- `!purge [channel_id] [delay]`: Purge a selfbot user's messages in a specified channel with an optional delay between deletions. If no channel ID is provided, it will purge messages in the current channel. The delay is in seconds and defaults to 1.0.

## Rich Presence Elements

### Playing

- `!setactivity playing <game_name>`: Set the activity to "Playing <game_name>".

### Streaming

- `!setactivity streaming <stream_name> url=<stream_url>`: Set the activity to "Streaming <stream_name>" with the specified URL.

### Listening

- `!setactivity listening <music_name>`: Set the activity to "Listening to <music_name>".

### Watching

- `!setactivity watching <show_name>`: Set the activity to "Watching <show_name>".

### Custom

- `!setactivity custom <custom_name> state=<state> details=<details> application_id=<application_id> url=<url> timestamps=<timestamps> assets=<assets> party=<party> secrets=<secrets> instance=<instance> buttons=<buttons>`: Set a custom activity with the specified parameters.

## GitHub Actions Workflow for Automatic Merging

This repository includes a GitHub Actions workflow to automatically merge pull requests if all checks pass. The workflow is defined in the `.github/workflows/auto_merge.yml` file.

The workflow is triggered on pull request events and includes the following jobs:

1. **Run Checks and Tests**: This job runs the necessary checks and tests to ensure the pull request meets the required standards.
2. **Automatic Merge**: If all checks pass, this job automatically merges the pull request.

To configure the workflow, make sure to update the `.github/workflows/auto_merge.yml` file with the appropriate settings for your project.

The check for conflicts with the base branch is implemented in the GitHub Actions workflow file `.github/workflows/auto_merge.yml`. The current implementation fetches the base branch, checks out the base branch, and attempts to merge the head branch without committing or fast-forwarding. If a conflict is detected during the merge attempt, the merge is aborted, and the workflow exits with a non-zero status. The check for conflicts is located in the `run_checks` job under the `Check for conflicts with base branch` step in `.github/workflows/auto_merge.yml`. The `git merge --abort || exit 1` command is now replaced with `git merge --abort || { echo "Merge conflict detected"; exit 1; }` to provide a clear message.
