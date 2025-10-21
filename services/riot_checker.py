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

# 英雄名字映射表（英文到中文）
CHAMPION_NAME_MAPPING = {
    "Aatrox": "剑魔",
    "Ahri": "阿狸",
    "Akali": "阿卡丽",
    "Akshan": "阿克尚",
    "Alistar": "牛头",
    "Amumu": "阿木木",
    "Anivia": "冰鸟",
    "Annie": "安妮",
    "Aphelios": "厄斐琉斯",
    "Ashe": "艾希",
    "Azir": "沙皇",
    "Bard": "巴德",
    "Bel'Veth": "卑尔维斯",
    "Blitzcrank": "机器人",
    "Brand": "火男",
    "Braum": "布隆",
    "Caitlyn": "女警",
    "Camille": "卡蜜尔",
    "Cassiopeia": "蛇女",
    "Cho'Gath": "虫子",
    "Corki": "飞机",
    "Darius": "德莱文",
    "Diana": "黛安娜",
    "Draven": "德莱文",
    "DrMundo": "蒙多医生",
    "Ekko": "艾克",
    "Elise": "伊莉丝",
    "Evelynn": "伊芙琳",
    "Ezreal": "EZ",
    "Fiddlesticks": "费德提克",
    "Fiora": "菲奥娜",
    "Fizz": "小鱼人",
    "Galio": "加里奥",
    "Gangplank": "船长",
    "Garen": "盖伦",
    "Gnar": "纳尔",
    "Gragas": "酒桶",
    "Graves": "男枪",
    "Gwen": "格温",
    "Hecarim": "人马",
    "Heimerdinger": "大头",
    "Illaoi": "俄洛伊",
    "Irelia": "刀妹",
    "Ivern": "艾翁",
    "Janna": "风女",
    "Jarvan IV": "皇子",
    "Jax": "贾克斯",
    "Jayce": "杰斯",
    "Jhin": "烬",
    "Jinx": "金克丝",
    "Kai'Sa": "卡莎",
    "Kalista": "卡莉丝塔",
    "Karma": "卡尔玛",
    "Karthus": "死歌",
    "Kassadin": "卡萨丁",
    "Katarina": "卡特琳娜",
    "Kayle": "天使",
    "Kayn": "凯隐",
    "Kennen": "凯南",
    "Kha'Zix": "螳螂",
    "Kindred": "千珏",
    "Kled": "克烈",
    "Kog'Maw": "大嘴",
    "LeBlanc": "妖姬",
    "Lee Sin": "盲僧",
    "Leona": "日女",
    "Lillia": "莉莉娅",
    "Lissandra": "冰女",
    "Lucian": "卢锡安",
    "Lulu": "璐璐",
    "Lux": "拉克丝",
    "Malphite": "石头人",
    "Malzahar": "蚂蚱",
    "Maokai": "大树",
    "Master Yi": "剑圣",
    "Miss Fortune": "女枪",
    "Mordekaiser": "铁男",
    "Morgana": "莫甘娜",
    "Nami": "娜美",
    "Nasus": "狗头",
    "Nautilus": "泰坦",
    "Neeko": "妮蔻",
    "Nidalee": "豹女",
    "Nocturne": "梦魇",
    "Nunu & Willump": "努努",
    "Olaf": "奥拉夫",
    "Orianna": "奥莉安娜",
    "Ornn": "奥恩",
    "Pantheon": "潘森",
    "Poppy": "波比",
    "Pyke": "派克",
    "Qiyana": "奇亚娜",
    "Quinn": "奎因",
    "Rakan": "洛",
    "Rammus": "龙龟",
    "Rek'Sai": "挖掘机",
    "Rell": "芮尔",
    "Renekton": "鳄鱼",
    "Rengar": "狮子狗",
    "Riven": "瑞文",
    "Rumble": "兰博",
    "Ryze": "瑞兹",
    "Samira": "莎弥拉",
    "Sejuani": "猪妹",
    "Senna": "赛娜",
    "Seraphine": "萨勒芬妮",
    "Sett": "瑟提",
    "Shaco": "小丑",
    "Shen": "慎",
    "Shyvana": "龙女",
    "Singed": "炼金",
    "Sion": "赛恩",
    "Sivir": "希维尔",
    "Swain": "乌鸦",
    "Sylas": "塞拉斯",
    "Syndra": "辛德拉",
    "Tahm Kench": "塔姆",
    "Taliyah": "岩雀",
    "Talon": "男刀",
    "Taric": "宝石",
    "Teemo": "提莫",
    "Thresh": "锤石",
    "Tristana": "小炮",
    "Trundle": "巨魔",
    "Tryndamere": "蛮王",
    "Twisted Fate": "卡牌",
    "Twitch": "老鼠",
    "Udyr": "乌迪尔",
    "Urgot": "厄加特",
    "Varus": "韦鲁斯",
    "Vayne": "薇恩",
    "Veigar": "小法",
    "Vel'Koz": "大眼",
    "Vex": "薇古丝",
    "Vi": "蔚",
    "Viego": "佛耶戈",
    "Viktor": "维克托",
    "Vladimir": "吸血鬼",
    "Volibear": "狗熊",
    "Warwick": "狼人",
    "Wukong": "猴子",
    "Xayah": "霞",
    "Xerath": "泽拉斯",
    "Xin Zhao": "赵信",
    "Yasuo": "亚索",
    "Yone": "永恩",
    "Yorick": "掘墓",
    "Yuumi": "猫咪",
    "Zac": "扎克",
    "Zed": "劫",
    "Zeri": "泽丽",
    "Ziggs": "炸弹人",
    "Zilean": "老头",
    "Zoe": "佐伊",
    "Zyra": "婕拉"
}

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


def get_chinese_champion_name(english_name):
    """获取英雄的中文名字"""
    return CHAMPION_NAME_MAPPING.get(english_name, english_name)


def get_summoner_info(game_name=None, tag_line=None):
    """获取召唤师信息"""
    try:
        # 使用传入的参数或环境变量
        target_game_name = game_name or GAME_NAME
        target_tag_line = tag_line or TAG_LINE
        
        if not target_game_name or not target_tag_line:
            raise ValueError("游戏用户名和标签不能为空")
        
        # 获取账户信息
        account_url = f"{ACCOUNT_BASE}/accounts/by-riot-id/{target_game_name}/{target_tag_line}"
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
        
        # 获取玩家名字，尝试多个字段
        player_name = player_info.get('summonerName', '') or player_info.get('riotIdGameName', '') or summoner_info.get('summoner_name', '') or summoner_info.get('game_name', '')
        
        # 获取MVP和LVP的名字
        mvp_name = mvp.get('summonerName', '') or mvp.get('riotIdGameName', '')
        lvp_name = lvp.get('summonerName', '') or lvp.get('riotIdGameName', '')
        
        # 调试信息
        # print(f"[DEBUG] 玩家信息字段: {list(player_info.keys())}")
        print(f"[DEBUG] 玩家名字: summonerName='{player_info.get('summonerName', '')}', riotIdGameName='{player_info.get('riotIdGameName', '')}'")
        print(f"[DEBUG] 召唤师信息: {summoner_info}")
        
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
                'name': player_name,
                'champion': player_info['championName'],
                'champion_chinese': get_chinese_champion_name(player_info['championName']),
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
                'name': mvp_name,
                'champion': mvp['championName'],
                'champion_chinese': get_chinese_champion_name(mvp['championName']),
                'kills': mvp['kills'],
                'deaths': mvp['deaths'],
                'assists': mvp['assists'],
                'kda': f"{mvp['kills']}/{mvp['deaths']}/{mvp['assists']}"
            },
            'team_lvp': {
                'name': lvp_name,
                'champion': lvp['championName'],
                'champion_chinese': get_chinese_champion_name(lvp['championName']),
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


def get_match_data_for_user(game_name, tag_line):
    """为指定用户获取游戏数据"""
    print("英雄联盟游戏数据获取器（动态用户）")
    print("=" * 50)
    
    # 检查环境变量
    if not RIOT_API_KEY:
        print("错误: 请在.env文件中设置RIOT_API_KEY")
        return False
    
    if not game_name or not tag_line:
        print("错误: 用户名和标签不能为空")
        return False
    
    try:
        print(f"正在获取玩家信息: {game_name}#{tag_line}")
        
        # 获取召唤师信息
        summoner_info = get_summoner_info(game_name, tag_line)
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


def main():
    """主函数 - 获取并保存游戏数据（使用环境变量）"""
    print("英雄联盟游戏数据获取器")
    print("=" * 50)
    
    # 检查环境变量
    if not RIOT_API_KEY:
        print("错误: 请在.env文件中设置RIOT_API_KEY")
        return False
    
    # GAME_NAME 和 TAG_LINE 现在有默认值，不需要强制检查
    if not GAME_NAME:
        GAME_NAME = "exm233"  # 设置默认值
    if not TAG_LINE:
        TAG_LINE = "233"  # 设置默认值
    
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
