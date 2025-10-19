# clone_voice.py
import os, sys, requests, json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("VOICV_API_KEY")
AUDIO_PATH = r"C:\Users\Leo\AI projects\LOLBOT\audio_source\taffy.mp3"
if not API_KEY:
    print("缺少环境变量 VOICV_API_KEY"); sys.exit(1)
if not AUDIO_PATH or not os.path.exists(AUDIO_PATH):
    print("用法: python clone_voice.py /path/to/voice.mp3"); sys.exit(1)

url = "https://api.voicv.com/v1/voice-clone"
headers = {"x-api-key": API_KEY}
with open(AUDIO_PATH, "rb") as f:
    files = {"voice": (os.path.basename(AUDIO_PATH), f, "audio/mpeg")}
    r = requests.post(url, headers=headers, files=files, timeout=300)

try:
    r.raise_for_status()
except requests.HTTPError as e:
    print("克隆失败:", e, "\n响应:", r.text); sys.exit(1)

data = r.json()
print("返回：", json.dumps(data, ensure_ascii=False, indent=2))
voice_id = data.get("data", {}).get("voiceId")
if not voice_id:
    print("未拿到 voiceId"); sys.exit(1)

print("✅ 克隆完成，voiceId =", voice_id)
