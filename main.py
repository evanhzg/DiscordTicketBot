import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from cogs.ticket import TicketPanelView, TicketCloseView

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class TicketBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents=discord.Intents.default(),
            help_command=None
        )

    async def setup_hook(self):
        # Load the ticketing cog
        await self.load_extension('cogs.ticket')
        
        # Register persistent views so buttons work after bot restarts
        self.add_view(TicketPanelView())
        self.add_view(TicketCloseView())
        
        try:
            # Sync slash commands
            guild_id = os.getenv('GUILD_ID')
            if guild_id:
                guild = discord.Object(id=int(guild_id))
                self.tree.copy_global_to(guild=guild)
                await self.tree.sync(guild=guild)
            else:
                await self.tree.sync()
            print("Slash commands synced successfully.")
        except discord.Forbidden:
            print("WARNING: Failed to sync slash commands! The bot is either not invited to the server or is missing the 'applications.commands' scope.")
        except Exception as e:
            print(f"WARNING: Error syncing slash commands: {e}")

    async def on_ready(self):
        print('------')
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

if __name__ == '__main__':
    if not TOKEN or TOKEN == "your_bot_token_here":
        print("Error: DISCORD_TOKEN is not configured in the .env file.")
    else:
        bot = TicketBot()
        bot.run(TOKEN)
