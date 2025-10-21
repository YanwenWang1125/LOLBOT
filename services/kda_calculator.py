#!/usr/bin/env python3
"""
KDA评分计算器
"""

from services.config import Config

class KDACalculator:
    """KDA评分计算器"""
    
    def __init__(self, kill_weight: float = None, assist_weight: float = None):
        self.kill_weight = kill_weight or Config.KDA_KILL_WEIGHT
        self.assist_weight = assist_weight or Config.KDA_ASSIST_WEIGHT
    
    def calculate_score(self, kills: int, deaths: int, assists: int) -> float:
        """
        计算KDA评分
        
        Args:
            kills: 击杀数
            deaths: 死亡数
            assists: 助攻数
            
        Returns:
            KDA评分
        """
        # 加权评分：击杀权重更高，助攻权重较低
        weighted_score = (kills * self.kill_weight) + (assists * self.assist_weight)
        
        if deaths == 0:
            return weighted_score
        
        return weighted_score / deaths
    
    def calculate_player_score(self, player_data: dict) -> float:
        """
        从玩家数据计算KDA评分
        
        Args:
            player_data: 玩家数据字典
            
        Returns:
            KDA评分
        """
        stats = player_data.get("stats", {})
        kills = stats.get("kills", 0)
        deaths = stats.get("deaths", 0)
        assists = stats.get("assists", 0)
        
        return self.calculate_score(kills, deaths, assists)
    
    def find_mvp_lvp(self, players: list) -> tuple:
        """
        从玩家列表中找到MVP和LVP
        
        Args:
            players: 玩家数据列表
            
        Returns:
            (mvp_player, lvp_player)
        """
        if not players:
            return None, None
        
        # 计算每个玩家的KDA评分
        scored_players = []
        for player in players:
            score = self.calculate_player_score(player)
            scored_players.append((player, score))
        
        # 按评分排序
        scored_players.sort(key=lambda x: x[1], reverse=True)
        
        mvp = scored_players[0][0] if scored_players else None
        lvp = scored_players[-1][0] if scored_players else None
        
        return mvp, lvp
