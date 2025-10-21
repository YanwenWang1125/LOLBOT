"""
Presence Manager Module
Manages Riot ID to Discord ID bindings and checks Discord presence status
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
import discord

class PresenceManager:
    def __init__(self, data_path: str = "data/player_links.json"):
        self.data_path = data_path
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        """Ensure the data directory exists"""
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
        if not os.path.exists(self.data_path):
            self.save_bindings({"players": []})
    
    def load_bindings(self) -> Dict[str, Any]:
        """
        Load binding data from JSON file
        Returns: dict containing players list
        """
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"players": []}
    
    def save_bindings(self, data: Dict[str, Any]) -> bool:
        """
        Save binding data to JSON file
        Args:
            data: dict containing players list
        Returns: bool indicating success
        """
        try:
            with open(self.data_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving bindings: {e}")
            return False
    
    def register_binding(self, discord_id: str, riot_id: str, game: str = "LOL") -> bool:
        """
        Register a new Discord to Riot ID binding
        Args:
            discord_id: Discord user ID
            riot_id: Riot ID (Name#TAG format)
            game: Game type (default: LOL)
        Returns: bool indicating success
        """
        try:
            data = self.load_bindings()
            
            # Check if Discord ID already exists
            for player in data["players"]:
                if player["discord_id"] == discord_id:
                    return False
            
            # Check if Riot ID already exists
            for player in data["players"]:
                if player["riot_id"] == riot_id:
                    return False
            
            # Add new binding
            new_binding = {
                "discord_id": discord_id,
                "riot_id": riot_id,
                "game": game,
                "registered_at": datetime.now().isoformat(),
                "last_match_id": None
            }
            
            data["players"].append(new_binding)
            return self.save_bindings(data)
            
        except Exception as e:
            print(f"Error registering binding: {e}")
            return False
    
    def unregister_binding(self, discord_id: str) -> bool:
        """
        Unregister a Discord to Riot ID binding
        Args:
            discord_id: Discord user ID
        Returns: bool indicating success
        """
        try:
            data = self.load_bindings()
            
            # Find and remove the binding
            original_count = len(data["players"])
            data["players"] = [
                player for player in data["players"] 
                if player["discord_id"] != discord_id
            ]
            
            # Check if any binding was removed
            if len(data["players"]) < original_count:
                return self.save_bindings(data)
            return False
            
        except Exception as e:
            print(f"Error unregistering binding: {e}")
            return False
    
    def get_binding_by_discord(self, discord_id: str) -> Optional[Dict[str, Any]]:
        """
        Get binding information by Discord ID
        Args:
            discord_id: Discord user ID
        Returns: dict with binding info or None
        """
        try:
            data = self.load_bindings()
            
            for player in data["players"]:
                if player["discord_id"] == discord_id:
                    return player
            return None
            
        except Exception as e:
            print(f"Error getting binding by Discord ID: {e}")
            return None
    
    def get_binding_by_riot(self, riot_id: str) -> Optional[Dict[str, Any]]:
        """
        Get binding information by Riot ID
        Args:
            riot_id: Riot ID (Name#TAG format)
        Returns: dict with binding info or None
        """
        try:
            data = self.load_bindings()
            
            for player in data["players"]:
                if player["riot_id"] == riot_id:
                    return player
            return None
            
        except Exception as e:
            print(f"Error getting binding by Riot ID: {e}")
            return None
    
    def get_all_active_bindings(self) -> List[Dict[str, Any]]:
        """
        Get all active bindings
        Returns: list of all binding dictionaries
        """
        try:
            data = self.load_bindings()
            return data["players"]
        except Exception as e:
            print(f"Error getting all bindings: {e}")
            return []
    
    def update_last_match(self, riot_id: str, match_id: str) -> bool:
        """
        Update the last match ID for a Riot ID
        Args:
            riot_id: Riot ID (Name#TAG format)
            match_id: Match ID to update
        Returns: bool indicating success
        """
        try:
            data = self.load_bindings()
            
            for player in data["players"]:
                if player["riot_id"] == riot_id:
                    player["last_match_id"] = match_id
                    return self.save_bindings(data)
            return False
            
        except Exception as e:
            print(f"Error updating last match: {e}")
            return False
    
    def check_discord_presence(self, riot_id: str, bot_client: discord.Client) -> Optional[Dict[str, Any]]:
        """
        Check Discord presence status for a Riot ID
        Args:
            riot_id: Riot ID to check
            bot_client: Discord bot client
        Returns: dict with presence info or None
        """
        try:
            # Get binding info
            binding = self.get_binding_by_riot(riot_id)
            if not binding:
                return None
            
            discord_id = int(binding["discord_id"])
            
            # Search through all guilds for the user
            for guild in bot_client.guilds:
                member = guild.get_member(discord_id)
                if member:
                    # Check if user is online and in voice
                    is_online = member.status in [discord.Status.online, discord.Status.idle]
                    in_voice = member.voice is not None
                    
                    presence_info = {
                        "discord_id": str(discord_id),
                        "riot_id": riot_id,
                        "is_online": is_online,
                        "in_voice": in_voice,
                        "voice_channel": member.voice.channel.name if member.voice else None,
                        "voice_channel_id": member.voice.channel.id if member.voice else None,
                        "guild_name": guild.name,
                        "guild_id": guild.id,
                        "member": member
                    }
                    
                    return presence_info
            
            # User not found in any guild
            return {
                "discord_id": str(discord_id),
                "riot_id": riot_id,
                "is_online": False,
                "in_voice": False,
                "voice_channel": None,
                "voice_channel_id": None,
                "guild_name": None,
                "guild_id": None,
                "member": None
            }
            
        except Exception as e:
            print(f"Error checking Discord presence: {e}")
            return None
    
    def get_online_players(self, bot_client: discord.Client) -> List[Dict[str, Any]]:
        """
        Get all online players with their presence status
        Args:
            bot_client: Discord bot client
        Returns: list of presence info for all bound players
        """
        try:
            bindings = self.get_all_active_bindings()
            online_players = []
            
            for binding in bindings:
                presence = self.check_discord_presence(binding["riot_id"], bot_client)
                if presence and presence["is_online"]:
                    online_players.append(presence)
            
            return online_players
            
        except Exception as e:
            print(f"Error getting online players: {e}")
            return []
    
    def get_voice_players(self, bot_client: discord.Client) -> List[Dict[str, Any]]:
        """
        Get all players currently in voice channels
        Args:
            bot_client: Discord bot client
        Returns: list of presence info for players in voice
        """
        try:
            bindings = self.get_all_active_bindings()
            voice_players = []
            
            for binding in bindings:
                presence = self.check_discord_presence(binding["riot_id"], bot_client)
                if presence and presence["in_voice"]:
                    voice_players.append(presence)
            
            return voice_players
            
        except Exception as e:
            print(f"Error getting voice players: {e}")
            return []
