import os
import asyncio
import discord
from discord.ext import commands
from discord import app_commands

class TicketPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # Persistent view

    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.primary, custom_id="persistent_view:create_ticket", emoji="🎫")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        category_id = os.getenv('TICKET_CATEGORY_ID')
        mod_role_id = os.getenv('MODERATOR_ROLE_ID')

        if not category_id or not mod_role_id:
            await interaction.response.send_message("Bot configuration error: Missing Category or Mod Role IDs.", ephemeral=True)
            return

        category_obj = guild.get_channel(int(category_id))
        category = None
        if isinstance(category_obj, discord.CategoryChannel):
            category = category_obj
        elif category_obj and hasattr(category_obj, 'category'):
            category = category_obj.category

        mod_role = guild.get_role(int(mod_role_id))

        if not mod_role:
            await interaction.response.send_message("Bot configuration error: Mod Role not found in this server.", ephemeral=True)
            return

        # Check if the user already has a ticket
        ticket_name = f"ticket-{interaction.user.name.lower()}"
        existing_channel = discord.utils.get(guild.text_channels, name=ticket_name)
        if existing_channel:
            await interaction.response.send_message(f"You already have a ticket open at {existing_channel.mention}!", ephemeral=True)
            return

        # Define permissions
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            mod_role: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True, manage_channels=True)
        }

        # Create the ticket channel
        ticket_channel = await guild.create_text_channel(
            name=ticket_name,
            category=category,
            overwrites=overwrites,
            topic=f"Ticket created by {interaction.user.name} (ID: {interaction.user.id})"
        )

        await interaction.response.send_message(f"Ticket created! Head over to {ticket_channel.mention}.", ephemeral=True)

        # Send initial message in the ticket channel
        embed = discord.Embed(
            title="Ticket Support",
            description=f"Welcome {interaction.user.mention}!\n\nPlease describe your issue and a member of our {mod_role.mention} team will assist you shortly.",
            color=discord.Color.blue()
        )
        await ticket_channel.send(content=f"{interaction.user.mention} {mod_role.mention}", embed=embed, view=TicketCloseView())

        # Send DMs to moderators
        for member in mod_role.members:
            if not member.bot:
                try:
                    await member.send(f"🎟️ **New Ticket Alert:** {interaction.user.name} has opened a new ticket in {guild.name}.\nChannel: {ticket_channel.mention}")
                except discord.Forbidden:
                    pass # User has DMs disabled

class TicketCloseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.danger, custom_id="persistent_view:close_ticket", emoji="🔒")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Closing this ticket in 5 seconds...")
        await asyncio.sleep(5)
        await interaction.channel.delete()

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setup_ticket_panel", description="Set up the ticket creation panel in the current channel.")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_panel(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Support Tickets",
            description="Click the button below to open a private ticket.",
            color=discord.Color.green()
        )
        await interaction.response.send_message("Panel created.", ephemeral=True)
        await interaction.channel.send(embed=embed, view=TicketPanelView())

async def setup(bot):
    await bot.add_cog(Ticket(bot))
