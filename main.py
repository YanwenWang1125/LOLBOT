#!/usr/bin/env python3
"""
英雄联盟游戏数据分析主入口
"""

import os
import sys
from dotenv import load_dotenv

# 添加bots目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'bots'))

def check_environment():
    """检查环境配置"""
    print("🔍 检查环境配置...")
    
    # 检查必要的环境变量
    required_vars = [
        "RIOT_API_KEY", "OPENAI_API_KEY", "DISCORD_TOKEN", "VOICV_API_KEY"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ 缺少必要的环境变量: {', '.join(missing_vars)}")
        print("请在.env文件中设置这些变量")
        return False
    
    print("✅ 所有配置检查通过")
    return True

def main():
    """主函数"""
    print("🎮 英雄联盟游戏分析工作流程")
    print("=" * 50)
    
    # 加载环境变量
    load_dotenv()
    
    # 检查环境
    if not check_environment():
        return
    
    # 自动选择模式1 - 启动Discord Bot
    print("\n🤖 启动Discord Bot...")
    print("在Discord中使用 !lol 命令来运行分析")
    
    # 导入并启动Discord Bot
    try:
        from bots.discord_bot import main as run_discord_bot
        run_discord_bot()
    except Exception as e:
        print(f"❌ 启动Discord Bot失败: {e}")

if __name__ == "__main__":
    main()
