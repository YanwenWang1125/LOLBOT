#!/usr/bin/env python3
"""
Riot Games API 数据获取模块
获取英雄联盟游戏数据并保存为JSON文件
"""

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.utils import ensure_directory, get_analysis_filename, save_json_file

# 加载环境变量
load_dotenv()

# Riot API 配置
RIOT_API_KEY = os.getenv("RIOT_API_KEY")
GAME_NAME = os.getenv("GAME_NAME")
TAG_LINE = os.getenv("TAG_LINE")
REGION = os.getenv("REGION", "na1")
REGION_ROUTE = os.getenv("REGION_ROUTE", "americas")

# API 端点
ACCOUNT_BASE = f"https://{REGION_ROUTE}.api.riotgames.com/riot/account/v1"
SUMMONER_BASE = f"https://{REGION}.api.riotgames.com/lol/summoner/v4"
MATCH_BASE = f"https://{REGION_ROUTE}.api.riotgames.com/lol/match/v5"

HEADERS = {"X-Riot-Token": RIOT_API_KEY}


def get_summoner_info():
    """获取召唤师信息"""
    try:
        # 获取账户信息
        account_url = f"{ACCOUNT_BASE}/accounts/by-riot-id/{GAME_NAME}/{TAG_LINE}"
        account_response = requests.get(account_url, headers=HEADERS, timeout=10)
        account_response.raise_for_status()
        account_data = account_response.json()
        
        # 获取召唤师信息
        summoner_url = f"{SUMMONER_BASE}/summoners/by-puuid/{account_data['puuid']}"
        summoner_response = requests.get(summoner_url, headers=HEADERS, timeout=10)
        summoner_response.raise_for_status()
        summoner_data = summoner_response.json()
        
        return {
            'puuid': account_data['puuid'],
            'game_name': account_data['gameName'],
            'tag_line': account_data['tagLine'],
            'summoner_id': summoner_data.get('id', ''),
            'summoner_name': summoner_data.get('name', ''),
            'summoner_level': summoner_data.get('summonerLevel', 0)
        }
        
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] 获取召唤师信息失败: {e}")
        return None
    except KeyError as e:
        print(f"[ERROR] 召唤师数据缺少字段: {e}")
        print(f"[DEBUG] 召唤师数据: {summoner_data}")
        return None
    except Exception as e:
        print(f"[ERROR] 获取召唤师信息时发生未知错误: {e}")
        return None


def get_recent_matches(puuid, count=1):
    """获取最近的比赛ID"""
    try:
        matches_url = f"{MATCH_BASE}/matches/by-puuid/{puuid}/ids?start=0&count={count}"
        matches_response = requests.get(matches_url, headers=HEADERS, timeout=10)
        matches_response.raise_for_status()
        return matches_response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] 获取比赛列表失败: {e}")
        return []


def get_match_details(match_id):
    """获取比赛详细信息"""
    try:
        match_url = f"{MATCH_BASE}/matches/{match_id}"
        match_response = requests.get(match_url, headers=HEADERS, timeout=10)
        match_response.raise_for_status()
        return match_response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] 获取比赛详情失败: {e}")
        return None


def analyze_match_data(match_data, summoner_info):
    """分析比赛数据"""
    try:
        # 找到玩家在比赛中的信息
        player_puuid = summoner_info['puuid']
        player_info = None
        player_team_id = None
        
        # 遍历所有参与者找到玩家
        for participant in match_data['info']['participants']:
            if participant['puuid'] == player_puuid:
                player_info = participant
                player_team_id = participant['teamId']
                break
        
        if not player_info:
            raise ValueError("未找到玩家在比赛中的信息")
        
        # 获取团队信息
        team_info = None
        for team in match_data['info']['teams']:
            if team['teamId'] == player_team_id:
                team_info = team
                break
        
        # 找到MVP和LVP（团队内表现最好和最差的玩家）
        team_participants = [p for p in match_data['info']['participants'] if p['teamId'] == player_team_id]
        
        # 按KDA评分排序
        def calculate_kda_score(participant):
            kills = participant['kills']
            deaths = participant['deaths']
            assists = participant['assists']
            if deaths == 0:
                return kills + assists
            return (kills + assists) / deaths
        
        team_participants.sort(key=calculate_kda_score, reverse=True)
        mvp = team_participants[0]
        lvp = team_participants[-1]
        
        # 构建分析结果
        analysis = {
            'match_id': match_data['metadata']['matchId'],
            'game_creation': match_data['info']['gameCreation'],
            'game_duration': match_data['info']['gameDuration'],
            'game_mode': match_data['info']['gameMode'],
            'game_type': match_data['info']['gameType'],
            'map_id': match_data['info']['mapId'],
            'queue_id': match_data['info']['queueId'],
            'player_info': {
                'name': player_info['summonerName'],
                'champion': player_info['championName'],
                'kills': player_info['kills'],
                'deaths': player_info['deaths'],
                'assists': player_info['assists'],
                'kda': f"{player_info['kills']}/{player_info['deaths']}/{player_info['assists']}",
                'cs': player_info['totalMinionsKilled'],
                'gold_earned': player_info['goldEarned'],
                'damage_dealt': player_info['totalDamageDealtToChampions'],
                'result': '胜利' if team_info['win'] else '失败'
            },
            'team_mvp': {
                'name': mvp['summonerName'],
                'champion': mvp['championName'],
                'kills': mvp['kills'],
                'deaths': mvp['deaths'],
                'assists': mvp['assists'],
                'kda': f"{mvp['kills']}/{mvp['deaths']}/{mvp['assists']}"
            },
            'team_lvp': {
                'name': lvp['summonerName'],
                'champion': lvp['championName'],
                'kills': lvp['kills'],
                'deaths': lvp['deaths'],
                'assists': lvp['assists'],
                'kda': f"{lvp['kills']}/{lvp['deaths']}/{lvp['assists']}"
            },
            'team_result': '胜利' if team_info['win'] else '失败'
        }
        
        return analysis
        
    except Exception as e:
        print(f"[ERROR] 分析比赛数据失败: {e}")
        return None


def main():
    """主函数 - 获取并保存游戏数据"""
    print("英雄联盟游戏数据获取器")
    print("=" * 50)
    
    # 检查环境变量
    if not RIOT_API_KEY:
        print("错误: 请在.env文件中设置RIOT_API_KEY")
        return False
    
    if not GAME_NAME or not TAG_LINE:
        print("错误: 请在.env文件中设置GAME_NAME和TAG_LINE")
        return False
    
    try:
        print(f"正在获取玩家信息: {GAME_NAME}#{TAG_LINE}")
        
        # 获取召唤师信息
        summoner_info = get_summoner_info()
        if not summoner_info:
            print("获取召唤师信息失败")
            return False
        
        print(f"召唤师信息获取成功: {summoner_info['summoner_name']} (等级 {summoner_info['summoner_level']})")
        
        # 获取最近的比赛
        print("正在获取最近的比赛...")
        recent_matches = get_recent_matches(summoner_info['puuid'], 1)
        if not recent_matches:
            print("未找到最近的比赛")
            return False
        
        match_id = recent_matches[0]
        print(f"找到最近比赛: {match_id}")
        
        # 获取比赛详情
        print("正在获取比赛详情...")
        match_data = get_match_details(match_id)
        if not match_data:
            print("获取比赛详情失败")
            return False
        
        print("比赛详情获取成功")
        
        # 分析比赛数据
        print("正在分析比赛数据...")
        analysis = analyze_match_data(match_data, summoner_info)
        if not analysis:
            print("分析比赛数据失败")
            return False
        
        print("比赛数据分析完成")
        
        # 保存分析结果
        # 确保保存到根目录的analysis文件夹
        import os
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        analysis_dir = os.path.join(root_dir, "analysis")
        ensure_directory(analysis_dir)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join(analysis_dir, f"match_analysis_{timestamp}.json")
        
        if save_json_file(analysis, output_file):
            print(f"分析结果已保存: {output_file}")
            return True
        else:
            print("保存分析结果失败")
            return False
            
    except Exception as e:
        print(f"执行失败: {e}")
        return False


if __name__ == "__main__":
    main()
