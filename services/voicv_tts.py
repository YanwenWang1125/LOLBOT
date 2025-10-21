#!/usr/bin/env python3
"""
VoicV TTS 服务模块
"""

import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

VOICV_BASE = "https://api.voicv.com"


def generate_tts_audio(text: str, output_path: str = None, voice_id: str = None) -> str:
    """
    使用VoicV TTS API生成音频文件
    
    Args:
        text: 要转换的文本
        output_path: 输出文件路径，如果为None则自动生成
        voice_id: 语音ID，如果为None则使用环境变量中的VOICV_VOICE_ID
        
    Returns:
        生成的音频文件路径，失败返回None
    """
    # 检查环境变量
    voicv_api_key = os.getenv("VOICV_API_KEY")
    if not voicv_api_key:
        print("[ERROR] 缺少环境变量 VOICV_API_KEY")
        return None
    
    # 使用传入的voice_id或默认的VOICV_VOICE_ID
    if voice_id is None:
        voice_id = os.getenv("VOICV_VOICE_ID")
        if not voice_id:
            # 使用默认语音ID
            voice_id = "cdf5f2a7604849e2a5ccd07ccf628ee6"
    
    # 生成输出路径
    if not output_path:
        # 确保audio目录存在
        os.makedirs("audio", exist_ok=True)
        # 生成时间戳
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f"audio/match_analysis_{timestamp}.mp3"
    
    headers = {"x-api-key": voicv_api_key, "Content-Type": "application/json"}
    payload = {"voiceId": voice_id, "text": text, "format": "mp3"}
    
    try:
        print("-> 调用 voicV TTS API...")
        response = requests.post(f"{VOICV_BASE}/v1/tts", headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        
        data = response.json().get("data", {})
        audio_url = data.get("audioUrl")
        
        if not audio_url:
            print(f"[ERROR] 未返回 audioUrl: {response.text}")
            return None
        
        print(f"🔗 音频地址: {audio_url}")
        print("-> 下载音频文件...")
        
        # 下载音频文件
        mp3_response = requests.get(audio_url, timeout=120)
        mp3_response.raise_for_status()
        
        # 确保目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 保存文件
        with open(output_path, "wb") as f:
            f.write(mp3_response.content)
        
        print(f"🎉 音频文件已保存: {output_path}")
        return output_path
        
    except requests.HTTPError as e:
        print(f"[ERROR] TTS API错误: {e}")
        print(f"请求: {payload}")
        print(f"响应: {response.text}")
        return None
    except Exception as e:
        print(f"[ERROR] TTS调用失败: {e}")
        return None


def main():
    """命令行入口"""
    import sys
    
    text = "你好，这是用我克隆的声音生成的语音测试。"
    if len(sys.argv) >= 2:
        text = " ".join(sys.argv[1:])
    
    print("🎵 VoicV TTS 测试")
    print("=" * 30)
    print(f"文本: {text}")
    
    output_path = generate_tts_audio(text, "output.mp3")
    if output_path:
        print(f"✅ 完成: {output_path}")
    else:
        print("❌ TTS生成失败")


if __name__ == "__main__":
    main()
