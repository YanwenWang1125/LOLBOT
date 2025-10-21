#!/usr/bin/env python3
"""
Valorant 比赛数据分析器
将Valorant比赛数据转换为中文成熟风格分析
"""

import json
import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.prompts import prompt_manager

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
    """Convert Valorant match data to Chinese paragraph with specified style
    
    Args:
        match_data (dict): The Valorant match data containing game information
        prompt (str, optional): Custom prompt for the AI. If None, uses style-based prompt
        system_role (str, optional): Custom system role for the AI. If None, uses style-based system role
        style (str, optional): Style name (default, professional, humorous). Defaults to "default"
    
    Returns:
        tuple: (Generated Chinese analysis text, voice_id) or (None, None) if failed
    """
    
    # Get style configuration if custom prompt/role not provided
    if prompt is None or system_role is None:
        style_config = prompt_manager.get_style_config(style)
        if prompt is None:
            prompt = style_config["prompt"]
        if system_role is None:
            system_role = style_config["system_role"]
        
        # Get voice_id from style config
        voice_id = style_config.get("voice_id")
    else:
        voice_id = None
    
    
    # For Valorant, use custom prompt formatting
    if prompt is None:
        # Use the custom Valorant prompt
        formatted_prompt = create_valorant_prompt(match_data)
    else:
        # Use the provided custom prompt with Valorant formatting
        formatted_prompt = format_valorant_prompt(prompt, match_data)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
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

def create_valorant_prompt(match_data):
    """Create a specialized prompt for Valorant match analysis"""
    prompt = f"""
请分析这场Valorant比赛的数据，用成熟御姐的语气进行评价：

比赛信息：
- 地图：{match_data.get('map', 'Unknown')}
- 结果：{match_data.get('result', 'Unknown')}
- 最强玩家：{match_data.get('strongest_player', {}).get('name', 'Unknown')} (使用 {match_data.get('strongest_player', {}).get('character', 'Unknown')})
- 最弱玩家：{match_data.get('weakest_player', {}).get('name', 'Unknown')} (使用 {match_data.get('weakest_player', {}).get('character', 'Unknown')})

请用成熟御姐的语气，分析这场比赛的胜负情况，评价最强和最弱玩家的表现，并给出一些游戏建议。语言要优雅、专业，带有一定的威严感。
"""
    return prompt

def create_valorant_system_role():
    """Create a specialized system role for Valorant analysis"""
    return """你是一位成熟的御姐型游戏分析师，专门分析Valorant比赛。你的语言风格优雅、专业，带有一定的威严感。你会用成熟女性的视角来分析游戏数据，给出专业的评价和建议。"""

def format_valorant_prompt(prompt_template, match_data):
    """
    格式化Valorant提示词模板
    
    Args:
        prompt_template (str): 提示词模板
        match_data (dict): Valorant比赛数据
    
    Returns:
        str: 格式化后的提示词
    """
    # 提取Valorant数据字段
    # 注意：strongest_player 实际上是MVP，weakest_player 实际上是LVP
    mvp_username = match_data.get('strongest_player', {}).get('name', 'Unknown')
    lvp_username = match_data.get('weakest_player', {}).get('name', 'Unknown')
    player_result = match_data.get('result', 'Unknown')
    mvp_champion = match_data.get('strongest_player', {}).get('character', 'Unknown')
    lvp_champion = match_data.get('weakest_player', {}).get('character', 'Unknown')
    
    # 调试输出：显示映射到提示词的数据
    print(f"  MVP (最强玩家): {mvp_username} - 角色: {mvp_champion}")
    print(f"  LVP (最弱玩家): {lvp_username} - 角色: {lvp_champion}")
    print(f"  比赛结果: {player_result}")
    
    return prompt_template.format(
        match_data=match_data,
        mvp_username=mvp_username,
        lvp_username=lvp_username,
        player_result=player_result,
        mvp_champion=mvp_champion,
        lvp_champion=lvp_champion
    )

def main(json_filename=None):
    """Main function - 支持自动文件名"""
    print("🔫 Valorant比赛数据分析器 - 御姐版")
    print("=" * 50)
    
    # 如果没有提供文件名，让用户输入或使用默认
    if not json_filename:
        json_filename = input("请输入JSON文件名 (或按回车使用默认文件): ").strip()
        if not json_filename:
            # 查找最新的valorant分析文件
            root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            analysis_dir = os.path.join(root_dir, "analysis")
            if os.path.exists(analysis_dir):
                valorant_files = [f for f in os.listdir(analysis_dir) if f.startswith('valorant_last_match_') and f.endswith('.json')]
                if valorant_files:
                    latest_file = max(valorant_files, key=lambda x: os.path.getctime(os.path.join(analysis_dir, x)))
                    json_filename = os.path.join(analysis_dir, latest_file)
                    print(f"🔄 自动选择最新Valorant文件: {json_filename}")
                else:
                    print("❌ 未找到Valorant分析文件")
                    return None
            else:
                print("❌ analysis目录不存在")
                return None
    
    # 检查文件是否在analysis文件夹中
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    analysis_dir = os.path.join(root_dir, "analysis")
    if not json_filename.startswith(analysis_dir + os.sep):
        # 如果文件路径不包含analysis目录，尝试在analysis目录中查找
        if os.path.exists(os.path.join(analysis_dir, json_filename)):
            json_filename = os.path.join(analysis_dir, json_filename)
        elif not os.path.exists(json_filename):
            # 如果根目录也没有，尝试在analysis目录中查找
            if os.path.exists(analysis_dir):
                valorant_files = [f for f in os.listdir(analysis_dir) if f.startswith('valorant_') and f.endswith('.json')]
                if valorant_files:
                    print(f"📁 在analysis目录中找到 {len(valorant_files)} 个Valorant文件:")
                    for i, file in enumerate(valorant_files[:5], 1):
                        print(f"   {i}. {file}")
                    if len(valorant_files) > 5:
                        print(f"   ... 还有 {len(valorant_files) - 5} 个文件")
                    
                    # 使用最新的文件
                    latest_file = max(valorant_files, key=lambda x: os.path.getctime(os.path.join(analysis_dir, x)))
                    json_filename = os.path.join(analysis_dir, latest_file)
                    print(f"🔄 自动选择最新文件: {json_filename}")
                else:
                    print(f"❌ analysis目录中没有Valorant文件")
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
    print("🤖 正在调用OpenAI API生成御姐风格的Valorant分析...")
    
    # Use specialized Valorant prompt and system role
    custom_prompt = create_valorant_prompt(match_data)
    custom_system_role = create_valorant_system_role()
    
    # Convert to Chinese mature tone
    result = convert_to_chinese_mature_tone(match_data, prompt=custom_prompt, system_role=custom_system_role)
    if result and result[0]:
        chinese_analysis = result[0]
    else:
        chinese_analysis = None
    
    if chinese_analysis:
        print("\n" + "=" * 50)
        print("🎭 御姐风格Valorant分析结果:")
        print("=" * 50)
        print(chinese_analysis)
        print("=" * 50)
        
        # Save to file in analysis directory
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        analysis_dir = os.path.join(root_dir, "analysis")
        os.makedirs(analysis_dir, exist_ok=True)
        
        # 获取文件名（不包含路径）
        base_filename = os.path.basename(json_filename)
        output_filename = f"valorant_chinese_analysis_{base_filename.replace('.json', '')}.txt"
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
