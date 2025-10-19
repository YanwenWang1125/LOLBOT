#!/usr/bin/env python3
"""
测试玩家名字提取功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.riot_checker import get_chinese_champion_name

def test_champion_name_mapping():
    """测试英雄名字映射功能"""
    print("测试英雄名字映射功能")
    print("=" * 50)
    
    # 测试一些英雄名字
    test_cases = [
        ("Lissandra", "冰女"),
        ("Lux", "拉克丝"),
        ("Shaco", "小丑"),
        ("Ahri", "阿狸"),
        ("Yasuo", "亚索"),
        ("Lee Sin", "盲僧"),
        ("Master Yi", "剑圣"),
        ("Teemo", "提莫"),
        ("Unknown Champion", "Unknown Champion")  # 测试未知英雄
    ]
    
    for english_name, expected_chinese in test_cases:
        chinese_name = get_chinese_champion_name(english_name)
        status = "✓" if chinese_name == expected_chinese else "✗"
        print(f"{status} {english_name} -> {chinese_name} (期望: {expected_chinese})")
    
    print("\n测试完成！")

if __name__ == "__main__":
    test_champion_name_mapping()
