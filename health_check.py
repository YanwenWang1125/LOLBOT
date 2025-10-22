#!/usr/bin/env python3
"""
健康检查脚本
用于监控LOLBOT服务的状态
"""

import os
import sys
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def check_environment():
    """检查环境变量配置"""
    print("🔍 检查环境变量...")
    
    required_vars = [
        "RIOT_API_KEY", "VAL_API_KEY", "OPENAI_API_KEY", "DISCORD_TOKEN", "VOICV_API_KEY"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ 缺少环境变量: {', '.join(missing_vars)}")
        return False
    
    print("✅ 环境变量检查通过")
    return True

def check_riot_api():
    """检查Riot API连接"""
    print("🔍 检查Riot API连接...")
    
    try:
        api_key = os.getenv("RIOT_API_KEY")
        game_name = os.getenv("GAME_NAME")
        tag_line = os.getenv("TAG_LINE")
        region_route = os.getenv("REGION_ROUTE", "americas")
        
        # 测试API连接
        headers = {"X-Riot-Token": api_key}
        url = f"https://{region_route}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        print("✅ Riot API连接正常")
        return True
        
    except Exception as e:
        print(f"❌ Riot API连接失败: {e}")
        return False

def check_openai_api():
    """检查OpenAI API连接"""
    print("🔍 检查OpenAI API连接...")
    
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # 发送测试请求
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        
        print("✅ OpenAI API连接正常")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI API连接失败: {e}")
        return False

def check_voicv_api():
    """检查VoicV API连接"""
    print("🔍 检查VoicV API连接...")
    
    try:
        api_key = os.getenv("VOICV_API_KEY")
        voice_id = os.getenv("VOICV_VOICE_ID", "cdf5f2a7604849e2a5ccd07ccf628ee6")  # 使用默认语音ID
        
        headers = {"x-api-key": api_key, "Content-Type": "application/json"}
        payload = {"voiceId": voice_id, "text": "测试", "format": "mp3"}
        
        response = requests.post(
            "https://api.voicv.com/v1/tts", 
            headers=headers, 
            json=payload, 
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ VoicV API连接正常")
            return True
        else:
            print(f"❌ VoicV API响应错误: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ VoicV API连接失败: {e}")
        return False

def check_discord_bot():
    """检查Discord Bot配置"""
    print("🔍 检查Discord Bot配置...")
    
    try:
        import discord
        from discord.ext import commands
        
        # 创建Bot实例进行测试
        intents = discord.Intents.default()
        intents.message_content = True
        bot = commands.Bot(command_prefix="!", intents=intents)
        
        token = os.getenv("DISCORD_TOKEN")
        if not token:
            print("❌ Discord Token未设置")
            return False
        
        print("✅ Discord Bot配置正常")
        return True
        
    except Exception as e:
        print(f"❌ Discord Bot检查失败: {e}")
        return False

def check_file_permissions():
    """检查文件权限"""
    print("🔍 检查文件权限...")
    
    try:
        # 检查必要目录
        directories = ["analysis", "audio", "audio_source"]
        
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
                print(f"📁 创建目录: {directory}")
            
            # 检查写权限
            test_file = os.path.join(directory, "test.txt")
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)
        
        print("✅ 文件权限检查通过")
        return True
        
    except Exception as e:
        print(f"❌ 文件权限检查失败: {e}")
        return False

def check_dependencies():
    """检查Python依赖"""
    print("🔍 检查Python依赖...")
    
    try:
        import requests
        import discord
        from openai import OpenAI
        import ffmpeg
        
        print("✅ Python依赖检查通过")
        return True
        
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        return False

def generate_health_report():
    """生成健康检查报告"""
    print("\n" + "="*50)
    print("🏥 LOLBOT健康检查报告")
    print("="*50)
    print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    checks = [
        ("环境变量", check_environment),
        ("Python依赖", check_dependencies),
        ("文件权限", check_file_permissions),
        ("Riot API", check_riot_api),
        ("OpenAI API", check_openai_api),
        ("VoicV API", check_voicv_api),
        ("Discord Bot", check_discord_bot)
    ]
    
    results = {}
    all_passed = True
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results[check_name] = result
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ {check_name}检查异常: {e}")
            results[check_name] = False
            all_passed = False
    
    print("\n" + "="*50)
    print("📊 检查结果汇总")
    print("="*50)
    
    for check_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{check_name}: {status}")
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 所有检查通过！LOLBOT服务状态正常")
        return 0
    else:
        print("⚠️  部分检查失败，请检查配置")
        return 1

def main():
    """主函数"""
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        # JSON输出模式，用于监控系统
        results = {}
        checks = [
            ("environment", check_environment),
            ("dependencies", check_dependencies),
            ("file_permissions", check_file_permissions),
            ("riot_api", check_riot_api),
            ("openai_api", check_openai_api),
            ("voicv_api", check_voicv_api),
            ("discord_bot", check_discord_bot)
        ]
        
        for check_name, check_func in checks:
            try:
                results[check_name] = check_func()
            except:
                results[check_name] = False
        
        print(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "status": "healthy" if all(results.values()) else "unhealthy",
            "checks": results
        }))
    else:
        # 交互式输出模式
        return generate_health_report()

if __name__ == "__main__":
    sys.exit(main())
