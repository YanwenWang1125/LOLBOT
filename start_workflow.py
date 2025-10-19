#!/usr/bin/env python3
"""
简化版启动脚本 - 快速测试工作流程
"""

import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def check_environment():
    """检查环境配置"""
    print("🔍 检查环境配置...")
    
    required_vars = {
        "RIOT_API_KEY": "Riot API密钥",
        "GAME_NAME": "游戏名",
        "TAG_LINE": "游戏标签", 
        "OPENAI_API_KEY": "OpenAI API密钥",
        "DISCORD_TOKEN": "Discord Bot Token",
        "VOICV_API_KEY": "voicV API密钥",
        "VOICV_VOICE_ID": "voicV Voice ID"
    }
    
    missing_vars = []
    for var, desc in required_vars.items():
        if not os.getenv(var):
            missing_vars.append(f"{var} ({desc})")
    
    if missing_vars:
        print("❌ 缺少必要的环境变量:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n请在.env文件中设置这些变量")
        return False
    
    print("✅ 环境配置检查通过")
    return True

def run_workflow():
    """运行工作流程"""
    print("\n🚀 启动英雄联盟游戏分析工作流程")
    print("=" * 50)
    
    try:
        # 导入并运行主工作流程
        from lol_workflow import main
        main()
    except KeyboardInterrupt:
        print("\n👋 用户中断，程序退出")
    except Exception as e:
        print(f"❌ 运行失败: {e}")
        return False
    
    return True

def main():
    """主函数"""
    print("🎮 英雄联盟游戏分析工作流程启动器")
    print("=" * 50)
    
    # 检查环境
    if not check_environment():
        return
    
    # 询问用户选择
    print("\n请选择运行模式:")
    print("1. 启动Discord Bot (推荐)")
    print("2. 测试文件结构")
    print("3. 仅测试工作流程")
    print("4. 退出")
    
    choice = input("\n请输入选择 (1-4): ").strip()
    
    if choice == "1":
        print("\n🤖 启动Discord Bot...")
        print("在Discord中使用 !lol 命令来运行分析")
        run_workflow()
    elif choice == "2":
        print("\n🧪 测试文件结构...")
        try:
            from test_file_structure import main as test_structure
            test_structure()
        except Exception as e:
            print(f"❌ 测试失败: {e}")
    elif choice == "3":
        print("\n🧪 测试模式...")
        print("测试功能开发中...")
    elif choice == "4":
        print("👋 再见!")
    else:
        print("❌ 无效选择")

if __name__ == "__main__":
    main()
