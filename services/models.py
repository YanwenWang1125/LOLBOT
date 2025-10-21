#!/usr/bin/env python3
"""
数据模型定义
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class PlayerInfo:
    """玩家信息"""
    name: str
    character: str
    kills: int = 0
    deaths: int = 0
    assists: int = 0
    kda_score: float = 0.0

@dataclass
class MatchInfo:
    """比赛信息基类"""
    map_name: str
    result: str
    mvp: PlayerInfo
    lvp: PlayerInfo

@dataclass
class LoLMatchInfo(MatchInfo):
    """LoL比赛信息"""
    player_result: str
    team_mvp: PlayerInfo
    team_lvp: PlayerInfo

@dataclass
class ValorantMatchInfo(MatchInfo):
    """Valorant比赛信息"""
    strongest_player: PlayerInfo
    weakest_player: PlayerInfo

def create_player_info(data: Dict[str, Any], game_type: str = "lol") -> PlayerInfo:
    """从数据字典创建PlayerInfo对象"""
    if game_type == "valorant":
        return PlayerInfo(
            name=data.get("name", "Unknown"),
            character=data.get("character", "Unknown"),
            kills=data.get("stats", {}).get("kills", 0),
            deaths=data.get("stats", {}).get("deaths", 0),
            assists=data.get("stats", {}).get("assists", 0)
        )
    else:  # LoL
        return PlayerInfo(
            name=data.get("name", "Unknown"),
            character=data.get("champion", "Unknown"),
            kills=data.get("kills", 0),
            deaths=data.get("deaths", 0),
            assists=data.get("assists", 0)
        )
