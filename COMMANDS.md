# Command Examples

## Basic Commands

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
