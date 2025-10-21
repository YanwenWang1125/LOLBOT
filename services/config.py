#!/usr/bin/env python3
"""
统一配置管理
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """统一配置类"""
    
    # API配置
    RIOT_API_KEY = os.getenv("RIOT_API_KEY")
    VAL_API_KEY = os.getenv("VAL_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    VOICV_API_KEY = os.getenv("VOICV_API_KEY")
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    
    # 游戏配置
    GAME_NAME = os.getenv("GAME_NAME")
    TAG_LINE = os.getenv("TAG_LINE")
    REGION = os.getenv("REGION", "na1")
    REGION_ROUTE = os.getenv("REGION_ROUTE", "americas")
    
    # 文件配置
    ANALYSIS_DIR = "analysis"
    AUDIO_DIR = "audio"
    KEEP_FILES_COUNT = 5
    
    # Presence管理配置
    DISCORD_POLL_INTERVAL = int(os.getenv("DISCORD_POLL_INTERVAL", "300"))  # 状态检测间隔（秒）
    RIOT_POLL_INTERVAL = int(os.getenv("RIOT_POLL_INTERVAL", "180"))      # 比赛检测间隔（秒）
    PLAYER_LINKS_PATH = os.getenv("PLAYER_LINKS_PATH", "data/player_links.json")
    
    # KDA评分配置
    KDA_KILL_WEIGHT = 1.0
    KDA_ASSIST_WEIGHT = 0.5
    
    @classmethod
    def validate_required_keys(cls):
        """验证必需的API密钥"""
        required_keys = [
            ("RIOT_API_KEY", cls.RIOT_API_KEY),
            ("OPENAI_API_KEY", cls.OPENAI_API_KEY),
            ("VOICV_API_KEY", cls.VOICV_API_KEY),
            ("DISCORD_TOKEN", cls.DISCORD_TOKEN)
        ]
        
        missing_keys = []
        for key_name, key_value in required_keys:
            if not key_value:
                missing_keys.append(key_name)
        
        if missing_keys:
            raise ValueError(f"缺少必需的环境变量: {', '.join(missing_keys)}")
        
        return True
