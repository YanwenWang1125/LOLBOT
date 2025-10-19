#!/usr/bin/env python3
"""
测试中文英雄名字提取功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.riot_checker import get_chinese_champion_name, CHAMPION_NAME_MAPPING

def test_chinese_champion_names():
    """测试中文英雄名字提取功能"""
    print("测试中文英雄名字提取功能")
    print("=" * 50)
    
    # 测试一些常见的英雄名字
    test_champions = [
        "Lissandra", "Lux", "Shaco", "Ahri", "Yasuo", 
        "Lee Sin", "Master Yi", "Teemo", "Unknown Champion"
    ]
    
    for champion in test_champions:
        chinese_name = get_chinese_champion_name(champion)
        print(f"{champion} -> {chinese_name}")
    
    print("\n映射表统计:")
    print(f"总共包含 {len(CHAMPION_NAME_MAPPING)} 个英雄")
    
    # 显示前10个映射
    print("\n前10个英雄映射:")
    for i, (english, chinese) in enumerate(list(CHAMPION_NAME_MAPPING.items())[:10]):
        print(f"{i+1}. {english} -> {chinese}")

if __name__ == "__main__":
    test_chinese_champion_names()
