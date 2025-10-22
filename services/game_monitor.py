#!/usr/bin/env python3
"""
Game Monitor Service
Handles async monitoring of Riot games and automatic workflow triggering
"""

import asyncio
import os
import sys
from datetime import datetime
from typing import Dict, Optional, Any
import discord
from dotenv import load_dotenv

# Add services directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))

from services.riot_checker import get_summoner_info, get_recent_matches, get_match_details
from services.valorant_checker import get_last_valorant_match
from services.presence_manager import PresenceManager

# Load environment variables
load_dotenv()

# Global task management
active_monitors: Dict[str, 'GameMonitor'] = {}

class GameMonitor:
    """Individual game monitoring task for a specific user"""
    
    def __init__(self, discord_user: discord.Member, riot_id: str, voice_channel: discord.VoiceChannel, game_type: str = "LOL"):
        self.discord_user = discord_user
        self.riot_id = riot_id
        self.voice_channel = voice_channel
        self.game_type = game_type.upper()
        self.task = None
        self.is_running = False
        self.last_match_id = None
        self.check_interval = 30  # Default 30 seconds
        self.idle_interval = 90   # 90 seconds when not in game
        self.max_idle_checks = 10  # Stop after 10 idle checks
        self.idle_count = 0
        self.presence_manager = PresenceManager()  # Initialize presence manager
        
        print(f"Creating game monitor: {riot_id} ({self.game_type})")
    
    async def start(self):
        """Start the monitoring task"""
        if self.is_running:
            print(f"WARNING: Monitor already running: {self.riot_id}")
            return
        
        self.is_running = True
        self.task = asyncio.create_task(self._monitor_loop())
        print(f"SUCCESS: Started monitoring: {self.riot_id}")
        
        # Send notification to voice channel
        try:
            embed = discord.Embed(
                title="Game Monitoring Started",
                description=f"正在监控 {self.riot_id} 的 {self.game_type} 游戏状态",
                color=0x00ff00,
                timestamp=datetime.now()
            )
            embed.add_field(name="GAME Game Type", value=self.game_type, inline=True)
            embed.add_field(name="MUSIC Voice Channel", value=self.voice_channel.name, inline=True)
            embed.add_field(name="TIME Check Interval", value=f"{self.check_interval} seconds", inline=True)
            
            # Find text channel in same guild
            guild = self.voice_channel.guild
            text_channel = None
            for channel in guild.text_channels:
                if channel.name == "红温时刻":
                    text_channel = channel
                    break
            
            if text_channel:
                await text_channel.send(embed=embed)
        except Exception as e:
            print(f"ERROR: Failed to send monitoring start notification: {e}")
    
    async def stop(self):
        """Stop the monitoring task safely"""
        if not self.is_running:
            print(f"WARNING: Monitor not running: {self.riot_id}")
            return
        
        self.is_running = False
        
        if self.task and not self.task.done():
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        
        print(f"STOPPED: Monitoring stopped: {self.riot_id}")
        
        # Send notification to voice channel
        try:
            embed = discord.Embed(
                title="STOP Game Monitoring Stopped",
                description=f"已停止监控 {self.riot_id}",
                color=0xff6600,
                timestamp=datetime.now()
            )
            
            # Find text channel in same guild
            guild = self.voice_channel.guild
            text_channel = None
            for channel in guild.text_channels:
                if channel.name == "红温时刻":
                    text_channel = channel
                    break
            
            if text_channel:
                await text_channel.send(embed=embed)
        except Exception as e:
            print(f"ERROR Failed to send monitoring stop notification: {e}")
    
    async def _monitor_loop(self):
        """Main monitoring loop"""
        try:
            while self.is_running:
                try:
                    # Check if user is still in voice channel
                    if not self.discord_user.voice or self.discord_user.voice.channel != self.voice_channel:
                        print(f"MUTE 用户 {self.riot_id} 已离开Voice Channel，停止监控")
                        await self._update_user_status(is_in_voice=False, is_in_game=False, active_match=None)
                        await self.stop()
                        break
                    
                    # Check for active match
                    active_match = await self._get_active_match()
                    
                    if active_match:
                        print(f"GAME Active match detected: {self.riot_id} - {active_match}")
                        await self._handle_active_match(active_match)
                        await self._update_user_status(is_in_voice=True, is_in_game=True, active_match=active_match)
                        self.check_interval = 30  # Reset to active monitoring
                        self.idle_count = 0
                    else:
                        print(f"PAUSE 用户 {self.riot_id} not in game")
                        await self._update_user_status(is_in_voice=True, is_in_game=False, active_match=None)
                        self.idle_count += 1
                        
                        # Use longer interval when not in game
                        self.check_interval = self.idle_interval
                        
                        # Stop monitoring if idle too long
                        if self.idle_count >= self.max_idle_checks:
                            print(f"⏰ 用户 {self.riot_id} 长时间未游戏，停止监控")
                            await self._update_user_status(is_in_voice=True, is_in_game=False, active_match=None)
                            await self.stop()
                            break
                    
                    # Wait before next check
                    await asyncio.sleep(self.check_interval)
                    
                except Exception as e:
                    print(f"ERROR Monitoring loop error: {e}")
                    await asyncio.sleep(30)  # Wait before retry
                    
        except asyncio.CancelledError:
            print(f"STOP Monitoring task cancelled: {self.riot_id}")
        except Exception as e:
            print(f"ERROR Serious monitoring loop error: {e}")
        finally:
            self.is_running = False
            # Update status to offline when monitoring stops
            await self._update_user_status(is_in_voice=False, is_in_game=False, active_match=None)
            # Remove from active monitors
            if self.riot_id in active_monitors:
                del active_monitors[self.riot_id]
    
    async def _get_active_match(self) -> Optional[str]:
        """Check if user has an active match"""
        try:
            if self.game_type == "LOL":
                return await self._get_lol_active_match()
            elif self.game_type == "VALORANT":
                return await self._get_valorant_active_match()
            else:
                print(f"ERROR 不支持的Game Type: {self.game_type}")
                return None
        except Exception as e:
            print(f"ERROR Error getting active match: {e}")
            return None
    
    async def _get_lol_active_match(self) -> Optional[str]:
        """Check for active LOL match"""
        try:
            # Parse riot_id to get game_name and tag_line
            if '#' not in self.riot_id:
                return None
            
            game_name, tag_line = self.riot_id.split('#', 1)
            
            # Get summoner info
            summoner_info = get_summoner_info(game_name, tag_line)
            if not summoner_info:
                return None
            
            # Get recent matches (check if any are very recent)
            recent_matches = get_recent_matches(summoner_info['puuid'], 1)
            if not recent_matches:
                return None
            
            # Get match details to check if it's still active
            match_id = recent_matches[0]
            match_data = get_match_details(match_id)
            if not match_data:
                return None
            
            # Check if match is still in progress
            game_duration = match_data['info']['gameDuration']
            game_creation = match_data['info']['gameCreation']
            current_time = datetime.now().timestamp() * 1000
            
            # Calculate time since game started
            time_since_creation = current_time - game_creation
            
            # More flexible detection logic:
            # 1. If game is very recent (within 10 minutes) - likely still active
            # 2. If game duration is reasonable (between 1-60 minutes) - likely active
            # 3. If game is very recent AND short duration - definitely active
            
            is_recent = time_since_creation < 600000  # 10 minutes
            is_short_duration = game_duration < 600  # 10 minutes
            is_reasonable_duration = 60 <= game_duration <= 3600  # 1-60 minutes
            
            # Debug information
            print(f"DEBUG: {self.riot_id} - Duration: {game_duration}s, Time since creation: {time_since_creation/1000/60:.1f}min")
            
            if is_recent and (is_short_duration or is_reasonable_duration):
                print(f"DEBUG: {self.riot_id} - Match detected as active")
                return match_id
            elif is_recent and game_duration < 60:  # Very short duration, likely just started
                print(f"DEBUG: {self.riot_id} - Very recent match detected")
                return match_id
            
            return None
            
        except Exception as e:
            print(f"ERROR Error getting LOL active match: {e}")
            return None
    
    async def _get_valorant_active_match(self) -> Optional[str]:
        """Check for active Valorant match"""
        try:
            # Parse riot_id to get game_name and tag_line
            if '#' not in self.riot_id:
                return None
            
            game_name, tag_line = self.riot_id.split('#', 1)
            
            # Get last Valorant match
            match_info = get_last_valorant_match(game_name, tag_line)
            if not match_info:
                return None
            
            # Check if match is recent (within last 5 minutes)
            # This is a simplified check - in reality you'd need to check match status
            return "valorant_match"  # Simplified for now
            
        except Exception as e:
            print(f"ERROR Error getting Valorant active match: {e}")
            return None
    
    async def _handle_active_match(self, match_id: str):
        """Handle when an active match is detected"""
        try:
            # Check if this is a new match
            if self.last_match_id != match_id:
                print(f"GAME New match started: {self.riot_id} - {match_id}")
                self.last_match_id = match_id
                
                # Send notification
                await self._notify_match_start(match_id)
            else:
                # Same match, check if it ended
                if await self._is_match_ended(match_id):
                    print(f"FINISH Match ended: {self.riot_id} - {match_id}")
                    await self._handle_match_end(match_id)
                    self.last_match_id = None
        except Exception as e:
            print(f"ERROR Error handling active match: {e}")
    
    async def _is_match_ended(self, match_id: str) -> bool:
        """Check if a match has ended"""
        try:
            if self.game_type == "LOL":
                match_data = get_match_details(match_id)
                if match_data:
                    # Check if match duration is reasonable (not too short, not too long)
                    game_duration = match_data['info']['gameDuration']
                    return game_duration > 600  # More than 10 minutes
            elif self.game_type == "VALORANT":
                # For Valorant, we'd need to implement proper match status checking
                return False
            
            return False
        except Exception as e:
            print(f"ERROR 检查Match ended状态错误: {e}")
            return False
    
    async def _handle_match_end(self, match_id: str):
        """Handle when a match ends - trigger automatic workflow"""
        try:
            print(f"LAUNCH Triggering automatic workflow: {self.riot_id}")
            
            # Import workflow classes
            from bots.discord_bot import LOLWorkflow, VAWorkflow
            
            # Create appropriate workflow
            if self.game_type == "LOL":
                workflow = LOLWorkflow()
                # Parse riot_id for workflow
                game_name, tag_line = self.riot_id.split('#', 1)
                success = await workflow.run_full_workflow_with_user(
                    voice_channel_id=self.voice_channel.id,
                    game_name=game_name,
                    tag_line=tag_line,
                    style="default"
                )
            elif self.game_type == "VALORANT":
                workflow = VAWorkflow()
                # Parse riot_id for workflow
                game_name, tag_line = self.riot_id.split('#', 1)
                success = await workflow.run_full_workflow(
                    voice_channel_id=self.voice_channel.id,
                    game_name=game_name,
                    tag_line=tag_line,
                    style="default"
                )
            else:
                print(f"ERROR 不支持的Game Type: {self.game_type}")
                return
            
            if success:
                print(f"SUCCESS Automatic workflow completed: {self.riot_id}")
                # Stop monitoring after successful workflow
                await self.stop()
            else:
                print(f"ERROR Automatic workflow failed: {self.riot_id}")
                
        except Exception as e:
            print(f"ERROR 处理Match ended错误: {e}")
    
    async def _notify_match_start(self, match_id: str):
        """Notify that a match has started"""
        try:
            embed = discord.Embed(
                title="GAME Match Start Detection",
                description=f"检测到 {self.riot_id} 开始新的 {self.game_type} 比赛",
                color=0x0099ff,
                timestamp=datetime.now()
            )
            embed.add_field(name="GAME Match ID", value=match_id, inline=True)
            embed.add_field(name="MUSIC Voice Channel", value=self.voice_channel.name, inline=True)
            
            # Find text channel
            guild = self.voice_channel.guild
            text_channel = None
            for channel in guild.text_channels:
                if channel.name == "红温时刻":
                    text_channel = channel
                    break
            
            if text_channel:
                await text_channel.send(embed=embed)
        except Exception as e:
            print(f"ERROR Failed to send match start notification: {e}")
    
    async def _update_user_status(self, is_in_voice: bool, is_in_game: bool, active_match: Optional[str] = None):
        """Update user status in player_links.json"""
        try:
            # Get current timestamp
            current_time = datetime.now().isoformat()
            
            # Update status in presence manager
            success = self.presence_manager.update_user_status(
                riot_id=self.riot_id,
                is_in_voice=is_in_voice,
                is_in_game=is_in_game,
                active_match=active_match,
                last_check=current_time
            )
            
            if success:
                print(f"STATUS Updated: {self.riot_id} - Voice: {is_in_voice}, Game: {is_in_game}, Match: {active_match}")
            else:
                print(f"WARNING Failed to update status for {self.riot_id}")
                
        except Exception as e:
            print(f"ERROR Failed to update user status: {e}")


class GameMonitorManager:
    """Manages all game monitoring tasks"""
    
    def __init__(self):
        self.presence_manager = PresenceManager()
    
    async def start_monitoring_for_user(self, discord_user: discord.Member, voice_channel: discord.VoiceChannel) -> bool:
        """Start monitoring for a specific user"""
        try:
            # Get user's riot binding
            discord_id = str(discord_user.id)
            binding = self.presence_manager.get_binding_by_discord(discord_id)
            
            if not binding:
                print(f"ERROR 用户 {discord_user.name} not bound to Riot ID")
                return False
            
            riot_id = binding['riot_id']
            game_type = binding.get('game', 'LOL')
            
            # Check if already monitoring
            if riot_id in active_monitors:
                print(f"WARNING 用户 {riot_id} already being monitored")
                return False
            
            # Create and start monitor
            monitor = GameMonitor(discord_user, riot_id, voice_channel, game_type)
            active_monitors[riot_id] = monitor
            await monitor.start()
            
            return True
            
        except Exception as e:
            print(f"ERROR Failed to start monitoring: {e}")
            return False
    
    async def stop_monitoring_for_user(self, discord_user: discord.Member) -> bool:
        """Stop monitoring for a specific user"""
        try:
            # Get user's riot binding
            discord_id = str(discord_user.id)
            binding = self.presence_manager.get_binding_by_discord(discord_id)
            
            if not binding:
                print(f"ERROR 用户 {discord_user.name} not bound to Riot ID")
                return False
            
            riot_id = binding['riot_id']
            
            # Check if monitoring
            if riot_id not in active_monitors:
                print(f"WARNING 用户 {riot_id} not being monitored")
                return False
            
            # Stop monitor
            monitor = active_monitors[riot_id]
            await monitor.stop()
            
            return True
            
        except Exception as e:
            print(f"ERROR Failed to stop monitoring: {e}")
            return False
    
    async def stop_all_monitoring(self):
        """Stop all active monitoring tasks"""
        try:
            print(f"Stopping all monitoring tasks ({len(active_monitors)} active)")
            
            tasks = []
            for riot_id, monitor in active_monitors.items():
                tasks.append(monitor.stop())
            
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
            
            active_monitors.clear()
            print("SUCCESS: All monitoring tasks stopped")
            
        except Exception as e:
            print(f"ERROR: Failed to stop all monitoring: {e}")
    
    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get current monitoring status"""
        try:
            status = {
                "active_count": len(active_monitors),
                "monitors": []
            }
            
            for riot_id, monitor in active_monitors.items():
                status["monitors"].append({
                    "riot_id": riot_id,
                    "discord_user": monitor.discord_user.name,
                    "voice_channel": monitor.voice_channel.name,
                    "game_type": monitor.game_type,
                    "is_running": monitor.is_running,
                    "check_interval": monitor.check_interval,
                    "idle_count": monitor.idle_count
                })
            
            return status
            
        except Exception as e:
            print(f"ERROR Failed to get monitoring status: {e}")
            return {"active_count": 0, "monitors": []}


# Global manager instance
monitor_manager = GameMonitorManager()
