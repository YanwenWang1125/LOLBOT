#!/usr/bin/env python3
"""
测试 voicV TTS 集成
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_voicv_tts():
    """测试 voicV TTS 功能"""
    print("🧪 测试 voicV TTS 集成")
    print("=" * 40)
    
    # 检查环境变量
    voicv_api_key = os.getenv("VOICV_API_KEY")
    voicv_voice_id = os.getenv("VOICV_VOICE_ID")
    
    if not voicv_api_key:
        print("❌ 缺少环境变量 VOICV_API_KEY")
        return False
    
    if not voicv_voice_id:
        print("❌ 缺少环境变量 VOICV_VOICE_ID")
        return False
    
    print("✅ 环境变量检查通过")
    
    # 测试文本
    test_text = "你好，这是voicV TTS的测试语音。"
    print(f"📝 测试文本: {test_text}")
    
    try:
        # 导入工作流程类
        from lol_workflow import LOLWorkflow
        
        # 创建实例并测试TTS
        workflow = LOLWorkflow()
        workflow.chinese_analysis = test_text
        
        print("🎤 开始生成TTS...")
        result = workflow._call_voicv_tts(test_text)
        
        if result:
            print(f"✅ TTS测试成功!")
            print(f"📁 音频文件: {result}")
            print(f"📊 文件大小: {os.path.getsize(result)} bytes")
            return True
        else:
            print("❌ TTS测试失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        return False

def main():
    """主函数"""
    print("🎮 voicV TTS 集成测试")
    print("=" * 50)
    
    success = test_voicv_tts()
    
    if success:
        print("\n🎉 所有测试通过！voicV TTS 集成成功！")
    else:
        print("\n❌ 测试失败，请检查配置")

if __name__ == "__main__":
    main()
