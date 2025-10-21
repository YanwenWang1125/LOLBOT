#!/usr/bin/env python3
"""
Valorant API 数据获取模块
使用Henrik API获取用户最后一场Valorant比赛信息
"""

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from urllib.parse import quote
import sys

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.utils import ensure_directory, save_json_file

# 加载环境变量
load_dotenv()

# 配置
VAL_API_KEY = os.getenv("VAL_API_KEY")
GAME_NAME = os.getenv("GAME_NAME")
TAG_LINE = os.getenv("TAG_LINE")
REGION = os.getenv("REGION", "na1")

# Henrik API 端点
HENRIK_API_BASE = "https://api.henrikdev.xyz/valorant/v3"

# 设置API密钥到请求头
HEADERS = {"Authorization": VAL_API_KEY} if VAL_API_KEY else {}


def get_region_code(region_name):
    """将区域名称转换为Henrik API使用的代码"""
    region_mapping = {
        "na1": "na", "americas": "na",
        "euw1": "eu", "europe": "eu", 
        "kr": "ap", "asia": "ap",
        "br1": "br", "latam": "br"
    }
    return region_mapping.get(region_name.lower(), "na")


def get_last_match_henrik_api(game_name, tag_line, region="na"):
    """使用Henrik API获取最后一场比赛信息"""
    try:
        
        # 对用户名进行URL编码以处理特殊字符
        encoded_game_name = quote(game_name, safe='')
        encoded_tag_line = quote(tag_line, safe='')
        
        # 构建API URL
        url = f"{HENRIK_API_BASE}/matches/{region}/{encoded_game_name}/{encoded_tag_line}"
        
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        if response.status_code == 401:
            print("[ERROR] Henrik API需要认证，请检查VAL_API_KEY")
            return None
        elif response.status_code == 404:
            print("[WARNING] 未找到该用户的比赛数据")
            return None
        elif response.status_code == 429:
            print("[WARNING] Henrik API请求频率限制")
            return None
        
        response.raise_for_status()
        data = response.json()
        
        if not data.get("data") or len(data["data"]) == 0:
            print("[WARNING] 未找到比赛数据")
            return None
        
        # 获取最后一场比赛
        last_match = data["data"][0]
        meta = last_match["metadata"]
        teams = last_match["teams"]
        
        # 找到玩家信息
        player_info = None
        player_team = None
        for player in last_match["players"]["all_players"]:
            if player["name"].lower() == game_name.lower() and player["tag"].lower() == tag_line.lower():
                player_info = player
                player_team = player["team"]
                break
        
        if not player_info:
            # 如果没找到精确匹配，使用第一个玩家作为示例
            player_info = last_match["players"]["all_players"][0]
            player_team = player_info["team"]
            print(f"[WARNING] 未找到精确匹配的玩家，使用示例数据")
        
        # 分析队友表现
        teammates = [p for p in last_match["players"]["all_players"] if p["team"] == player_team and p != player_info]
        
        # 计算队友KDA评分并排序
        def calculate_kda_score(player):
            stats = player.get("stats", {})
            kills = stats.get("kills", 0)
            deaths = stats.get("deaths", 0)
            assists = stats.get("assists", 0)
            
            # 改进的KDA评分：击杀权重更高，助攻权重较低
            # 击杀权重: 1.0, 助攻权重: 0.3
            weighted_score = kills + (assists * 0.5)
            
            if deaths == 0:
                return weighted_score
            return weighted_score / deaths
        
        teammates.sort(key=calculate_kda_score, reverse=True)
        teammate_mvp = teammates[0] if teammates else None  # 最高分 = MVP
        teammate_lvp = teammates[-1] if teammates else None  # 最低分 = LVP
        
        # 调试输出：MVP和LVP详细信息
        if teammate_mvp:
            mvp_stats = teammate_mvp.get("stats", {})
            mvp_kills = mvp_stats.get("kills", 0)
            mvp_deaths = mvp_stats.get("deaths", 0)
            mvp_assists = mvp_stats.get("assists", 0)
            mvp_score = calculate_kda_score(teammate_mvp)
        
        if teammate_lvp:
            lvp_stats = teammate_lvp.get("stats", {})
            lvp_kills = lvp_stats.get("kills", 0)
            lvp_deaths = lvp_stats.get("deaths", 0)
            lvp_assists = lvp_stats.get("assists", 0)
            lvp_score = calculate_kda_score(teammate_lvp)
        
        # 判断胜负
        player_team_won = teams[player_team.lower()]["has_won"]
        match_result = "胜利" if player_team_won else "失败"
        
        # 构建简化的比赛信息
        match_info = {
            "map": meta.get("map", "Unknown"),
            "result": match_result,
            "strongest_player": {
                "name": teammate_mvp.get("name", "Unknown") if teammate_mvp else "N/A",
                "character": teammate_mvp.get("character", "Unknown") if teammate_mvp else "N/A"
            },
            "weakest_player": {
                "name": teammate_lvp.get("name", "Unknown") if teammate_lvp else "N/A", 
                "character": teammate_lvp.get("character", "Unknown") if teammate_lvp else "N/A"
            }
        }
        
        return match_info
        
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Henrik API请求失败: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] 处理Henrik API数据时发生错误: {e}")
        return None


def get_last_valorant_match(game_name=None, tag_line=None):
    """获取最后一场Valorant比赛信息"""
    print("Valorant 最后比赛信息获取器")
    print("=" * 50)
    
    # 使用传入的参数或环境变量
    target_game_name = game_name or GAME_NAME
    target_tag_line = tag_line or TAG_LINE
    
    if not target_game_name or not target_tag_line:
        print("[ERROR] 错误: 用户名和标签不能为空")
        return None
    
    try:
        # 使用Henrik API获取数据
        region_code = get_region_code(REGION)
        match_info = get_last_match_henrik_api(target_game_name, target_tag_line, region_code)
        
        if not match_info:
            print("[ERROR] 无法获取比赛信息")
            return None
        
        # 显示简化的比赛信息
        
        # 保存结果到analysis目录，并管理最多5个文件
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        analysis_dir = os.path.join(root_dir, "analysis")
        ensure_directory(analysis_dir)
        
        # 管理Valorant比赛文件，保持最多5个
        manage_valorant_match_files(analysis_dir)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join(analysis_dir, f"valorant_last_match_{timestamp}.json")
        
        if save_json_file(match_info, output_file):
            match_info['output_file'] = output_file
        
        return match_info
        
    except Exception as e:
        print(f"[ERROR] 执行失败: {e}")
        return None


def manage_valorant_match_files(analysis_dir, max_files=5):
    """
    管理Valorant比赛文件，保持最多指定数量的文件
    
    Args:
        analysis_dir (str): analysis目录路径
        max_files (int): 最大文件数量，默认5个
    """
    try:
        import glob
        import os
        
        # 查找所有valorant_last_match_*.json文件
        pattern = os.path.join(analysis_dir, "valorant_last_match_*.json")
        valorant_files = glob.glob(pattern)
        
        # 按修改时间排序（最新的在前）
        valorant_files.sort(key=os.path.getmtime, reverse=True)
        
        # 如果文件数量超过限制，删除最旧的文件
        if len(valorant_files) >= max_files:
            files_to_delete = valorant_files[max_files-1:]  # 保留最新的max_files-1个，删除其余的
            for file_path in files_to_delete:
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"[WARNING] 删除文件失败 {file_path}: {e}")
        
    except Exception as e:
        print(f"[ERROR] 管理Valorant比赛文件时发生错误: {e}")


def test_api_connection():
    """测试API连接"""
    
    if not VAL_API_KEY:
        print("[WARNING] 未设置VAL_API_KEY，将使用无认证模式")
        return True
    
    try:
        # 使用一个已知的公开玩家进行测试
        test_name = "TenZ"
        test_tag = "SEN"
        test_region = "na"
        
        url = f"{HENRIK_API_BASE}/matches/{test_region}/{test_name}/{test_tag}"
        
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("data") and len(data["data"]) > 0:
                return True
            else:
                print("[WARNING] API响应数据为空")
                return False
        elif response.status_code == 401:
            print("[ERROR] API密钥无效")
            return False
        else:
            print(f"[WARNING] API响应异常，状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"[ERROR] API连接测试失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 50)
    
    # 检查环境变量
    if not GAME_NAME or not TAG_LINE:
        print("[ERROR] 错误: 请在.env文件中设置GAME_NAME和TAG_LINE")
        return False
    
    # 测试API连接
    if not test_api_connection():
        print("[WARNING] API连接测试失败，但继续尝试获取用户数据...")
    
    print("\n" + "=" * 50)
    
    try:
        result = get_last_valorant_match()
        if result:
            return True
        else:
            print("\n[ERROR] 获取失败")
            return False
            
    except Exception as e:
        print(f"[ERROR] 执行失败: {e}")
        return False


if __name__ == "__main__":
    main()
