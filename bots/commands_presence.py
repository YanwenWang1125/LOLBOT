"""
Discord Presence Commands Module
Provides Discord command interfaces for Riot ID binding and presence management
"""

import discord
from discord.ext import commands
import json
import os
from datetime import datetime
from services.presence_manager import PresenceManager

class PresenceCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.presence_manager = PresenceManager()
    
    @commands.command(name='register_riot')
    async def register_riot(self, ctx, riot_id: str):
        """
        Register a Riot ID for the current Discord user
        Usage: !register_riot YanwenWang#NA1
        """
        try:
            # Validate Riot ID format (basic validation)
            if '#' not in riot_id:
                await ctx.send("❌ Invalid Riot ID format. Please use: `Name#TAG` (e.g., YanwenWang#NA1)")
                return
            
            discord_id = str(ctx.author.id)
            
            # Check if user is already registered
            existing_binding = self.presence_manager.get_binding_by_discord(discord_id)
            if existing_binding:
                await ctx.send(f"❌ You are already registered with Riot ID: `{existing_binding['riot_id']}`\n"
                              f"Use `!unregister_riot` first to change your binding.")
                return
            
            # Check if Riot ID is already taken by another user
            existing_riot = self.presence_manager.get_binding_by_riot(riot_id)
            if existing_riot:
                await ctx.send(f"❌ Riot ID `{riot_id}` is already registered by another user.")
                return
            
            # Register the binding
            success = self.presence_manager.register_binding(discord_id, riot_id, "LOL")
            
            if success:
                await ctx.send(f"✅ Successfully registered Riot ID: `{riot_id}`\n"
                              f"🎮 Game: League of Legends\n"
                              f"📅 Registered: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                await ctx.send("❌ Failed to register Riot ID. Please try again.")
                
        except Exception as e:
            await ctx.send(f"❌ Error registering Riot ID: {str(e)}")
    
    @commands.command(name='unregister_riot')
    async def unregister_riot(self, ctx):
        """
        Unregister the current Discord user's Riot ID
        Usage: !unregister_riot
        """
        try:
            discord_id = str(ctx.author.id)
            
            # Check if user is registered
            existing_binding = self.presence_manager.get_binding_by_discord(discord_id)
            if not existing_binding:
                await ctx.send("❌ You are not currently registered with any Riot ID.")
                return
            
            # Unregister the binding
            success = self.presence_manager.unregister_binding(discord_id)
            
            if success:
                await ctx.send("✅ Successfully unregistered your Riot ID.")
            else:
                await ctx.send("❌ Failed to unregister Riot ID. Please try again.")
                
        except Exception as e:
            await ctx.send(f"❌ Error unregistering Riot ID: {str(e)}")
    
    @commands.command(name='myriot')
    async def myriot(self, ctx):
        """
        Show the current Discord user's registered Riot ID
        Usage: !myriot
        """
        try:
            discord_id = str(ctx.author.id)
            binding = self.presence_manager.get_binding_by_discord(discord_id)
            
            if binding:
                await ctx.send(f"📋 **Your Registration Info:**\n"
                              f"🎮 Riot ID: `{binding['riot_id']}`\n"
                              f"🎯 Game: {binding['game']}\n"
                              f"📅 Registered: {binding['registered_at']}")
            else:
                await ctx.send("❌ You are not currently registered with any Riot ID.\n"
                              f"Use `!register_riot <RiotName#TAG>` to register.")
                
        except Exception as e:
            await ctx.send(f"❌ Error retrieving registration info: {str(e)}")
    
    @commands.command(name='whois')
    async def whois(self, ctx, riot_id: str):
        """
        Find Discord user by Riot ID (admin only)
        Usage: !whois YanwenWang#NA1
        """
        try:
            # Check if user has admin permissions
            if not ctx.author.guild_permissions.administrator:
                await ctx.send("❌ This command requires administrator permissions.")
                return
            
            binding = self.presence_manager.get_binding_by_riot(riot_id)
            
            if binding:
                # Get Discord user object
                discord_user = self.bot.get_user(int(binding['discord_id']))
                if discord_user:
                    await ctx.send(f"🔍 **Riot ID Lookup:**\n"
                                  f"🎮 Riot ID: `{riot_id}`\n"
                                  f"👤 Discord User: {discord_user.mention} ({discord_user.name})\n"
                                  f"📅 Registered: {binding['registered_at']}")
                else:
                    await ctx.send(f"🔍 **Riot ID Lookup:**\n"
                                  f"🎮 Riot ID: `{riot_id}`\n"
                                  f"👤 Discord ID: {binding['discord_id']}\n"
                                  f"⚠️ User not found in current guilds")
            else:
                await ctx.send(f"❌ Riot ID `{riot_id}` is not registered.")
                
        except Exception as e:
            await ctx.send(f"❌ Error looking up Riot ID: {str(e)}")
    
    @commands.command(name='list_bindings')
    async def list_bindings(self, ctx):
        """
        List all registered bindings (admin only)
        Usage: !list_bindings
        """
        try:
            # Check if user has admin permissions
            if not ctx.author.guild_permissions.administrator:
                await ctx.send("❌ This command requires administrator permissions.")
                return
            
            bindings = self.presence_manager.get_all_active_bindings()
            
            if not bindings:
                await ctx.send("📋 No registered bindings found.")
                return
            
            # Create embed for better formatting
            embed = discord.Embed(
                title="📋 Registered Riot ID Bindings",
                color=0x00ff00
            )
            
            for i, binding in enumerate(bindings[:10], 1):  # Limit to 10 for readability
                discord_user = self.bot.get_user(int(binding['discord_id']))
                user_name = discord_user.name if discord_user else f"User {binding['discord_id']}"
                
                embed.add_field(
                    name=f"{i}. {user_name}",
                    value=f"🎮 {binding['riot_id']}\n📅 {binding['registered_at']}",
                    inline=False
                )
            
            if len(bindings) > 10:
                embed.set_footer(text=f"Showing 10 of {len(bindings)} total bindings")
            
            await ctx.send(embed=embed)
                
        except Exception as e:
            await ctx.send(f"❌ Error listing bindings: {str(e)}")

def setup(bot):
    bot.add_cog(PresenceCommands(bot))
