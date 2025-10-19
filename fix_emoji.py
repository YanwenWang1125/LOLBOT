#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

def fix_emoji_in_file(filename):
    """移除文件中的 emoji 字符"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换常见的 emoji
    emoji_replacements = {
        '🎮': '',
        '✅': '[OK]',
        '❌': '[ERROR]',
        '⚠️': '[WARNING]',
        '🔍': '',
        '🔄': '',
        '📤': '',
        'ℹ️': '[INFO]',
        '⏰': '',
        '🚀': '',
        '🤖': '',
        '➡️': '->',
    }
    
    for emoji, replacement in emoji_replacements.items():
        content = content.replace(emoji, replacement)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"已修复 {filename} 中的 emoji 字符")

if __name__ == "__main__":
    fix_emoji_in_file("lol_workflow.py")
    print("修复完成！")
