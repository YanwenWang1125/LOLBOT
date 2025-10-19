import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from .prompts import get_style_config, format_prompt

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

def convert_to_chinese_mature_tone(match_data, prompt=None, system_role=None, style="default"):
    """Convert match data to Chinese paragraph with specified style
    
    Args:
        match_data (dict): The match data containing player information
        prompt (str, optional): Custom prompt for the AI. If None, uses style-based prompt
        system_role (str, optional): Custom system role for the AI. If None, uses style-based system role
        style (str, optional): Style name (default, professional, humorous). Defaults to "default"
    
    Returns:
        tuple: (Generated Chinese analysis text, voice_id) or (None, None) if failed
    """
    
    # Get style configuration if custom prompt/role not provided
    if prompt is None or system_role is None:
        # print(f"DEBUG: 获取风格配置，风格: {style}")
        style_config = get_style_config(style)
        print(f"DEBUG: 风格配置: {style_config}")
        if prompt is None:
            prompt = style_config["prompt"]
            print(f"DEBUG: 使用风格提示词，长度: {len(prompt)}")
        if system_role is None:
            system_role = style_config["system_role"]
            print(f"DEBUG: 使用风格系统角色，长度: {len(system_role)}")
        
        # Get voice_id from style config
        voice_id = style_config.get("voice_id")
        print(f"DEBUG: 获取到voice_id: {voice_id}")
    else:
        voice_id = None
        print("DEBUG: 使用自定义提示词和系统角色")
    
    # Format the prompt with match data
    formatted_prompt = format_prompt(prompt, match_data)

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": system_role},
                {"role": "user", "content": formatted_prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip(), voice_id
    
    except Exception as e:
        print(f"❌ OpenAI API错误: {e}")
        return None, None

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
    result = convert_to_chinese_mature_tone(match_data)
    if result and result[0]:
        chinese_analysis = result[0]
    else:
        chinese_analysis = None
    
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
