# Discord Ticket Bot

A fully automated, clean, and professional Discord ticketing bot written in Python using `discord.py`.

## Features
- 🎫 **Persistent Ticket Panel**: Use `/setup_ticket_panel` to create a message with a "Open Ticket" button.
- 🔒 **Private Channels**: Automatically creates a private text channel for the user and the moderation team.
- 📬 **Moderator Notifications**: DMs moderators whenever a new ticket is opened.
- 🗑️ **Easy Closure**: "Close Ticket" button inside the ticket to easily archive and delete the channel.

## Hosting on a VPS

### Prerequisites
1. Python 3.10 or higher installed on your VPS.
2. A Discord Bot Token (Get one at the [Discord Developer Portal](https://discord.com/developers/applications)).
   - **Important**: You must enable the **Server Members Intent** in the Discord Developer Portal so the bot can DM moderators.

### Setup Instructions
1. Clone this repository to your VPS:
   ```bash
   git clone https://github.com/evanhzg/DiscordTicketBot.git
   cd DiscordTicketBot
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Configure Environment Variables:
   - Rename `.env.example` to `.env`:
     ```bash
     mv .env.example .env
     ```
   - Edit the `.env` file (`nano .env`) and fill in your details:
     - `DISCORD_TOKEN`: Your bot token.
     - `GUILD_ID`: Your Discord Server ID.
     - `TICKET_CATEGORY_ID`: The ID of the category where tickets should be created.
     - `MODERATOR_ROLE_ID`: The ID of the role that handles tickets.

4. Run the Bot:
   ```bash
   python main.py
   ```

### Keeping the Bot Online
To keep the bot running 24/7 on your VPS even after you close the terminal, you can use `pm2` or a `systemd` service. 
Using PM2 (Requires Node.js):
```bash
npm install -g pm2
pm2 start main.py --name "TicketBot" --interpreter ./venv/bin/python
pm2 save
pm2 startup
```

## Usage
Once the bot is online and invited to your server:
1. Ensure the bot has the `Administrator` permission.
2. Type `/setup_ticket_panel` in the channel where you want users to open tickets (e.g., `#tickets`).
3. Users can now click the button to get help!
