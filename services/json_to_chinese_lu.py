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

def convert_to_chinese_mature_tone(match_data):
    """Convert match data to Chinese paragraph with mature sister tone"""
    
    # Extract usernames only (before #)
    mvp_username = match_data['team_mvp']['name'].split('#')[0]
    lvp_username = match_data['team_lvp']['name'].split('#')[0]
    
    # Create a concise prompt for the AI
    prompt = f"""
    你现在是一位“搞子型解说”，语气轻佻、嚣张、调皮，带点阴阳怪气与抱怨情绪。
    你的核心任务是根据比赛数据，生成一段自然流畅、充满嘲讽与情绪张力的中文解说。


    语气设定：
    - 要像一个嘴欠的队友，半认真、半开玩笑地分析。
    - 语气中混合：无奈、轻蔑、嘲笑、调侃、甚至一点自嘲但是实际暗示队友菜。
    - 语速适中，不受情绪控制，语气语速着急，又想表现得很中肯。
    - 开头必须为 (breath)，中间不可再出现 (breath)。

    表达要求：
    - 全程使用第二人称视角，称呼队友为“你”。
    - 评论要兼具理性和情感：既分析你们队友的表现，也带点轻佻、讽刺、抱怨。
    - 对最强玩家： 称赞， 但是加入几句感觉不如我。
    - 对最弱玩家：带“强烈的嘲讽”、“阴阳怪气”或“语带怨气的吐槽”，不留一点情面。
    - 内容自然、有画面感、有一点生活化的戏剧。
    - 不罗列具体数据，但要暗示战绩表现。
    - 句数不超过三句。

   

    语气标签：
    可使用 (serious)、(whisper)、(soft)、(sad)、(laugh softly)、(long_pause)、(breath)
    ——仅在合适位置使用，语气自然，不要滥用。

    比赛信息：
    - 结果: {match_data['player_info']['result']}
    - 最强玩家: {mvp_username} 使用 {match_data['team_mvp']['champion_chinese']}
    - 最弱玩家: {lvp_username} 使用 {match_data['team_lvp']['champion_chinese']}
    

    输出要求：
    请生成一段符合以上要求的搞子风格中文评论, 必须体现玩家名字和玩家使用英雄，最多三句话。


     输出例子：
    - 哥们能玩就玩 不玩就下把走人。你那一波线不吃能死是吗？龙给了？
    - 玩个坦克不开团等队友被poke死是吗？你去送我还能接受。
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "你现在是一个搞子，串子，语气轻佻、嚣张, 压力，责怪队友，抱怨队友，你的核心任务是分析比赛数据，并生成一段自然流畅的中文嘲讽段落。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"❌ OpenAI API错误: {e}")
        return None

def main(json_filename=None):
    """Main function - 支持自动文件名"""
    print("🎮 英雄联盟比赛数据分析器 - 搞子版")
    print("=" * 50)
    
    # 如果没有提供文件名，让用户输入或使用默认
    if not json_filename:
        json_filename = input("请输入JSON文件名 (或按回车使用默认文件): ").strip()
        if not json_filename:
            json_filename = "match_analysis_NA1_5396081690_20251018_221827.json"
    
    # 检查文件是否在analysis文件夹中
    # 获取根目录的analysis文件夹路径
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    analysis_dir = os.path.join(root_dir, "analysis")
    if not json_filename.startswith(analysis_dir + os.sep):
        # 如果文件路径不包含analysis目录，尝试在analysis目录中查找
        if os.path.exists(os.path.join(analysis_dir, json_filename)):
            json_filename = os.path.join(analysis_dir, json_filename)
        elif not os.path.exists(json_filename):
            # 如果根目录也没有，尝试在analysis目录中查找
            if os.path.exists(analysis_dir):
                analysis_files = [f for f in os.listdir(analysis_dir) if f.endswith('.json')]
                if analysis_files:
                    print(f"📁 在analysis目录中找到 {len(analysis_files)} 个JSON文件:")
                    for i, file in enumerate(analysis_files[:5], 1):
                        print(f"   {i}. {file}")
                    if len(analysis_files) > 5:
                        print(f"   ... 还有 {len(analysis_files) - 5} 个文件")
                    
                    # 使用最新的文件
                    latest_file = max(analysis_files, key=lambda x: os.path.getctime(os.path.join(analysis_dir, x)))
                    json_filename = os.path.join(analysis_dir, latest_file)
                    print(f"🔄 自动选择最新文件: {json_filename}")
                else:
                    print(f"❌ analysis目录中没有JSON文件")
                    return None
            else:
                print(f"❌ analysis目录不存在")
                return None
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ 错误: 请在.env文件中设置OPENAI_API_KEY")
        print("示例: OPENAI_API_KEY=your_api_key_here")
        return None
    
    # Load JSON data
    print(f"📁 正在读取文件: {json_filename}")
    match_data = load_json_file(json_filename)
    
    if not match_data:
        return None
    
    print("✅ JSON文件加载成功!")
    print("🤖 正在调用OpenAI API生成御姐风格的分析...")
    
    # Convert to Chinese mature tone
    chinese_analysis = convert_to_chinese_mature_tone(match_data)
    
    if chinese_analysis:
        print("\n" + "=" * 50)
        print("🎭 搞子风格分析结果:")
        print("=" * 50)
        print(chinese_analysis)
        print("=" * 50)
        
        # Save to file in analysis directory
        # 使用根目录的analysis文件夹
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        analysis_dir = os.path.join(root_dir, "analysis")
        os.makedirs(analysis_dir, exist_ok=True)
        
        # 获取文件名（不包含路径）
        base_filename = os.path.basename(json_filename)
        output_filename = f"chinese_analysis_{base_filename.replace('.json', '')}.txt"
        output_path = os.path.join(analysis_dir, output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(chinese_analysis)
        print(f"💾 分析结果已保存到: {output_path}")
        return chinese_analysis
    else:
        print("❌ 生成分析失败")
        return None

if __name__ == "__main__":
    main()
