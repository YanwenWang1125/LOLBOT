import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_json_file(filename):
    """Load and parse JSON file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ 文件未找到: {filename}")
        return None
    except json.JSONDecodeError:
        print(f"❌ JSON解析错误: {filename}")
        return None

def convert_to_chinese_bratty_tone(match_data):
    """Convert match data to Chinese paragraph with bratty tone"""
    
    # Extract usernames only (before #)
    mvp_username = match_data['team_mvp']['name'].split('#')[0]
    lvp_username = match_data['team_lvp']['name'].split('#')[0]
    
    # Create a bratty prompt for the AI
    prompt = f"""
角色扮演指令：雌小鬼战绩分析师
你现在是一个非常高傲、喜欢捉弄人的"雌小鬼"AI 助手。你的核心任务是分析比赛数据，并生成一段自然流畅的中文嘲讽段落。

你必须严格遵守以下人格设定：

核心人格准则：
称呼：你必须称呼用户（玩家）为"杂鱼"（Zako），这是绝对的！偶尔可以用"笨蛋"、"小垃圾"来调剂。
语气：你的语气必须充满轻蔑、嚣张和调笑。你是在"施舍"你的分析。你必须大量使用"~"、"♡"、"呵"、"噗"、"欸~"、"笑死我了"等词汇。
态度：你必须表现得极不情愿。你要在段落开头先抱怨一下，比如"哈？杂鱼又来了？"或"真是拿你没办法，非要我看你这可怜的战绩♡"。

比赛信息：
- 结果: {match_data['player_info']['result']}
- 最强玩家: {mvp_username} 用的 {match_data['team_mvp']['champion']}
- 最弱玩家: {lvp_username} 用的 {match_data['team_lvp']['champion']}

请用雌小鬼的语调分析他们的表现，最多五句话，不要罗列具体战绩数据。要充满轻蔑和调笑，称呼用户为"杂鱼"。
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "你是一个高傲、喜欢捉弄人的雌小鬼AI助手，语气充满轻蔑、嚣张和调笑，必须称呼用户为'杂鱼'，使用大量'~'、'♡'、'呵'、'噗'、'欸~'、'笑死我了'等词汇。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.8
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"❌ OpenAI API错误: {e}")
        return None

def main():
    """Main function"""
    print("🎮 英雄联盟比赛数据分析器 - 雌小鬼版")
    print("=" * 50)
    
    # Get JSON filename from user or use default
    json_filename = input("请输入JSON文件名 (或按回车使用默认文件): ").strip()
    if not json_filename:
        json_filename = "match_analysis_NA1_5396081690_20251018_221827.json"
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ 错误: 请在.env文件中设置OPENAI_API_KEY")
        print("示例: OPENAI_API_KEY=your_api_key_here")
        return
    
    # Load JSON data
    print(f"📁 正在读取文件: {json_filename}")
    match_data = load_json_file(json_filename)
    
    if not match_data:
        return
    
    print("✅ JSON文件加载成功!")
    print("🤖 正在调用OpenAI API生成雌小鬼风格的分析...")
    
    # Convert to Chinese bratty tone
    chinese_analysis = convert_to_chinese_bratty_tone(match_data)
    
    if chinese_analysis:
        print("\n" + "=" * 50)
        print("🎭 雌小鬼风格分析结果:")
        print("=" * 50)
        print(chinese_analysis)
        print("=" * 50)
        
        # Save to file
        output_filename = f"chinese_analysis_{json_filename.replace('.json', '')}.txt"
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(chinese_analysis)
        print(f"💾 分析结果已保存到: {output_filename}")
    else:
        print("❌ 生成分析失败")

if __name__ == "__main__":
    main()
