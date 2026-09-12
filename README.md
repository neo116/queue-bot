## ANOTHER BOT MADE FOR IMRI

so last time i made a bot they didnt understand how to use it so hopefully ai managed to explains it better then me...
you arent gonna read this but....

# Queue Bot

A Discord bot for tracking queue numbers in one or more text channels. Users can
register multiple alts, change an alt's queue, or remove an alt from the queue.

## Requirements

- Python 3.10 or newer
- A Discord bot application and token
- The bot invited to the server with these permissions in the queue channel:
	- View Channel
	- Send Messages
	- Embed Links
	- Manage Messages
- **Message Content Intent** enabled in the Discord Developer Portal and in the
	bot code

## Installation

1. Open a terminal in this project folder.
2. Install the dependencies:

	 ```powershell
	 py -m pip install -r requirements.txt
	 ```

3. Create a `.env` file in the project folder with your bot token:

	 ```text
	 TOKEN=your_discord_bot_token
	 ```

	 Keep this file private. It is ignored by Git, and the token should be rotated
	 immediately if it is ever shared.

4. Start the bot:

	 ```powershell
	 py main.py
	 ```

	 A successful start prints the bot's Discord username in the terminal.

## Starting A Queue

Run this command in Discord:

```text
!queuer #channel
```

For example:

```text
!queuer #game-queue
```

The person running the command must have the **Manage Messages** permission. The
bot posts one embed in the selected channel with the heading `currents queues:`.
Running `!queuer` again for the same channel resets that channel's current queue
and creates a new queue embed.

## User Commands

Users type these messages directly in a tracked queue channel:

| Message | Meaning |
| --- | --- |
| `q4` | Put alt 1 in queue 4 |
| `2q4` | Put alt 2 in queue 4 |
| `3q7` | Put alt 3 in queue 7 |
| `l` | Remove alt 1 from the queue |
| `2l` | Remove alt 2 from the queue |

The number before `q` or `l` is the alt number. If it is omitted, the bot uses
alt 1. The number after `q` is the queue number.

When an alt submits another queue command, its existing entry is replaced and
its update time is refreshed. Different alts belonging to the same Discord user
are stored separately.

## Queue Display

Each entry is shown in the embed in this format:

```text
@User | alt 2 | q4 | 2 minutes ago
```

Entries are sorted by queue number. Discord renders the update time relative to
the current time, so it continues to update as time passes.

## Message Handling

- Messages matching `{alt}q{queue}` are added or updated.
- Messages matching `{alt}l` remove that user's alt.
- A missing alt number defaults to `1`.
- Every message sent in a tracked queue channel is deleted after it is checked.
- Messages in channels that have not been started with `!queuer` are untouched.

## Important Limitations

- Queue data is stored in memory only. Restarting the bot clears all tracked
	queues and queue channel configuration.
- The bot must remain online to update the embed.
- The bot must be able to delete messages and edit its queue embed.



