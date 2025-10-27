#!/usr/bin/env python3
"""
Data Maintenance Service
Lightweight maintenance for player_links.json
"""

import asyncio
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, Any

# Add services directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))

from services.presence_manager import PresenceManager

class DataMaintenance:
    """Lightweight data maintenance for player_links.json"""
    
    def __init__(self):
        self.presence_manager = PresenceManager()
        self.is_running = False
        self.task = None
        self.maintenance_interval = 300  # 5 minutes (not 1 minute to avoid overhead)
    
    async def start_maintenance(self):
        """Start the maintenance task"""
        if self.is_running:
            print("WARNING: Data maintenance already running")
            return
        
        self.is_running = True
        self.task = asyncio.create_task(self._maintenance_loop())
        print("SUCCESS: Data maintenance started")
    
    async def stop_maintenance(self):
        """Stop the maintenance task"""
        if not self.is_running:
            print("WARNING: Data maintenance not running")
            return
        
        self.is_running = False
        if self.task and not self.task.done():
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        
        print("SUCCESS: Data maintenance stopped")
    
    async def _maintenance_loop(self):
        """Main maintenance loop"""
        try:
            while self.is_running:
                try:
                    await self._perform_maintenance()
                    await asyncio.sleep(self.maintenance_interval)
                except Exception as e:
                    print(f"ERROR in maintenance loop: {e}")
                    await asyncio.sleep(60)  # Wait 1 minute before retry
        except asyncio.CancelledError:
            print("Data maintenance cancelled")
        except Exception as e:
            print(f"ERROR in maintenance loop: {e}")
        finally:
            self.is_running = False
    
    async def _perform_maintenance(self):
        """Perform maintenance tasks"""
        try:
            print("Performing data maintenance...")
            
            # Load current data
            data = self.presence_manager.load_bindings()
            updated = False
            
            # 清理过期的监控字段（如果存在）
            cutoff_time = datetime.now() - timedelta(minutes=10)
            
            for player in data["players"]:
                last_check = player.get('last_check')
                if last_check:
                    try:
                        last_check_time = datetime.fromisoformat(last_check)
                        if last_check_time < cutoff_time:
                            # 清理过期的监控字段
                            if 'is_in_voice' in player or 'is_in_game' in player or 'active_match' in player:
                                print(f"MAINTENANCE: Cleaning stale monitoring data for {player['riot_id']}")
                                player.pop('is_in_voice', None)
                                player.pop('is_in_game', None)
                                player.pop('active_match', None)
                                player.pop('last_check', None)
                                updated = True
                    except ValueError:
                        # 无效的时间戳，清理监控字段
                        player.pop('is_in_voice', None)
                        player.pop('is_in_game', None)
                        player.pop('active_match', None)
                        player.pop('last_check', None)
                        updated = True
            
            # Save if updated
            if updated:
                self.presence_manager.save_bindings(data)
                print("SUCCESS: Data maintenance completed with updates")
            else:
                print("SUCCESS: Data maintenance completed (no updates needed)")
                
        except Exception as e:
            print(f"ERROR during maintenance: {e}")
    
    def get_maintenance_status(self) -> Dict[str, Any]:
        """Get maintenance status"""
        return {
            "is_running": self.is_running,
            "interval_minutes": self.maintenance_interval // 60,
            "next_check_in": "N/A" if not self.is_running else "Active"
        }


# Global maintenance instance
data_maintenance = DataMaintenance()
