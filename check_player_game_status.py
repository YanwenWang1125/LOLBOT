# requirements: aiohttp
# pip install aiohttp

import asyncio
import aiohttp
import time
import os
import json
import subprocess
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

RIOT_API_KEY = os.getenv("RIOT_API_KEY")         # 你的 Riot API Key
REGION = os.getenv("REGION", "na1")                     # platform routing (spectator uses platform)
REGION_ROUTE = os.getenv("REGION_ROUTE", "americas")    # regional routing (americas/europe/asia)
GAME_NAME      = os.getenv("GAME_NAME")      # before the '#'
TAG_LINE       = os.getenv("TAG_LINE") 
SUMMONER_NAME = GAME_NAME+'#'+TAG_LINE
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Optional: external notification endpoint

# 验证必需的环境变量
if not RIOT_API_KEY:
    raise ValueError("RIOT_API_KEY environment variable is required")
if not GAME_NAME:
    raise ValueError("GAME_NAME environment variable is required")
if not TAG_LINE:
    raise ValueError("TAG_LINE environment variable is required")

# 检查 API 密钥格式
if not RIOT_API_KEY.startswith("RGAPI-"):
    print("⚠️ 警告：API 密钥格式可能不正确")
    print("   正确的格式应该以 'RGAPI-' 开头")
    print(f"   当前密钥: {RIOT_API_KEY[:10]}...")
else:
    print(f"✅ API 密钥格式正确: {RIOT_API_KEY[:10]}...")

HEADERS = {"X-Riot-Token": RIOT_API_KEY}
SPECTATOR_BASE = f"https://{REGION}.api.riotgames.com/lol/spectator/v4"
ACCOUNT_BASE = f"https://{REGION_ROUTE}.api.riotgames.com/riot/account/v1"
SUMMONER_BASE = f"https://{REGION}.api.riotgames.com/lol/summoner/v4"
MATCH_BASE = f"https://{REGION_ROUTE}.api.riotgames.com/lol/match/v5"

POLL_SECONDS_WHEN_IDLE = 10    # 推荐：10 秒轮询一次 Spectator（单玩家可接受）
POLL_SECONDS_IN_GAME = 5      # 对局中更频繁一些（或看需要）
BACKOFF_MAX = 60              # 出错时最大退避

# 已处理对局记录文件
PROCESSED_MATCHES_FILE = "processed_matches.json"

def load_processed_matches():
    """加载已处理的对局记录"""
    try:
        if os.path.exists(PROCESSED_MATCHES_FILE):
            with open(PROCESSED_MATCHES_FILE, 'r', encoding='utf-8') as f:
                return set(json.load(f))
        return set()
    except Exception as e:
        print(f"加载已处理对局记录失败: {e}")
        return set()

def save_processed_matches(processed_matches):
    """保存已处理的对局记录"""
    try:
        with open(PROCESSED_MATCHES_FILE, 'w', encoding='utf-8') as f:
            json.dump(list(processed_matches), f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存已处理对局记录失败: {e}")

def is_match_processed(match_id, processed_matches):
    """检查对局是否已经处理过"""
    return match_id in processed_matches

def mark_match_processed(match_id, processed_matches):
    """标记对局为已处理"""
    processed_matches.add(match_id)
    save_processed_matches(processed_matches)

async def check_api_permissions(session):
    """检查 API 密钥权限"""
    print("🔍 检查 API 密钥权限...")
    
    # 测试不同的 API 端点
    test_endpoints = [
        ("Account API", f"{ACCOUNT_BASE}/accounts/by-riot-id/{GAME_NAME}/{TAG_LINE}"),
        ("Summoner API", f"{SUMMONER_BASE}/summoners/by-name/{GAME_NAME}"),
        ("Match API", f"{MATCH_BASE}/matches/by-puuid/test/ids?start=0&count=1")
    ]
    
    for api_name, url in test_endpoints:
        try:
            status, text, headers = await fetch_json(session, url)
            if status == 200:
                print(f"✅ {api_name}: 权限正常")
            elif status == 403:
                print(f"❌ {api_name}: 权限被拒绝 (403)")
            elif status == 401:
                print(f"❌ {api_name}: 认证失败 (401)")
            else:
                print(f"⚠️ {api_name}: 状态码 {status}")
        except Exception as e:
            print(f"❌ {api_name}: 请求失败 - {e}")
    
    print("💡 如果看到权限被拒绝，请检查：")
    print("   1. API 密钥是否正确")
    print("   2. API 密钥是否已激活")
    print("   3. API 密钥是否有足够的权限")
    print("   4. 是否在正确的区域使用 API")

async def fetch_json(session, url, headers=HEADERS):
    async with session.get(url, headers=headers) as resp:
        text = await resp.text()
        return resp.status, text, resp.headers

async def notify_webhook(session, payload):
    # 简单 POST 通知
    async with session.post(WEBHOOK_URL, json=payload) as resp:
        return resp.status

async def get_account(session, game_name, tag_line):
    """使用 Account API v1 获取玩家账户信息"""
    url = f"{ACCOUNT_BASE}/accounts/by-riot-id/{game_name}/{tag_line}"
    status, text, headers = await fetch_json(session, url)
    if status == 200:
        return __import__('json').loads(text)
    else:
        raise RuntimeError(f"account lookup failed {status}: {text}")

async def get_summoner_by_puuid(session, puuid):
    """通过 puuid 获取召唤师信息"""
    url = f"{SUMMONER_BASE}/summoners/by-puuid/{puuid}"
    print(f"🔍 正在请求召唤师信息: {url}")
    status, text, headers = await fetch_json(session, url)
    print(f"   响应状态: {status}")
    
    if status == 200:
        data = __import__('json').loads(text)
        print(f"   返回数据: {data}")
        return data
    elif status == 404:
        raise RuntimeError(f"召唤师不存在 (404): 可能该玩家从未玩过召唤师峡谷")
    elif status == 403:
        raise RuntimeError(f"API访问被拒绝 (403): 检查API密钥权限")
    else:
        raise RuntimeError(f"召唤师查找失败 {status}: {text}")

async def get_summoner_by_name(session, summoner_name):
    """通过召唤师名称获取召唤师信息（备用方法）"""
    url = f"{SUMMONER_BASE}/summoners/by-name/{summoner_name}"
    print(f"🔍 正在通过名称请求召唤师信息: {url}")
    status, text, headers = await fetch_json(session, url)
    print(f"   响应状态: {status}")
    
    if status == 200:
        data = __import__('json').loads(text)
        print(f"   返回数据: {data}")
        return data
    elif status == 404:
        raise RuntimeError(f"召唤师不存在 (404): 找不到召唤师 {summoner_name}")
    elif status == 403:
        raise RuntimeError(f"API访问被拒绝 (403): 检查API密钥权限")
    else:
        raise RuntimeError(f"召唤师查找失败 {status}: {text}")

async def monitor_player():
    # 加载已处理的对局记录
    processed_matches = load_processed_matches()
    print(f"已加载 {len(processed_matches)} 个已处理的对局记录")
    
    async with aiohttp.ClientSession() as session:
        # 0) 检查 API 权限
        await check_api_permissions(session)
        
        # 1) 使用 Account API 获取玩家信息
        try:
            account = await get_account(session, GAME_NAME, TAG_LINE)
            puuid = account["puuid"]
            print(f"✅ 成功获取玩家账户信息: {GAME_NAME}#{TAG_LINE}")
            print(f"   PUUID: {puuid}")
        except Exception as e:
            print(f"❌ Account API 也失败了: {e}")
            print("🔍 这可能是 API 密钥权限问题")
            print("   请检查你的 Riot API 密钥是否有以下权限：")
            print("   - Account API v1")
            print("   - Summoner API v4") 
            print("   - Spectator API v4")
            print("   - Match API v5")
            raise SystemExit(f"获取玩家账户信息失败: {e}")
        
        # 2) 由于 Summoner API 权限被拒绝，我们跳过召唤师信息获取
        print("⚠️ 检测到 Summoner API 权限被拒绝")
        print("   将使用 puuid 直接进行 spectator 查询")
        print("   如果失败，将使用替代方案")
        
        # 使用 puuid 作为 summonerId
        summonerId = puuid
        print(f"🔄 使用 puuid 作为 summonerId: {summonerId}")
        
        # 由于无法获取传统的 summonerId，我们将尝试其他方法
        print("ℹ️ 由于权限限制，将使用 puuid 进行所有操作")

        last_seen_match = None
        in_game = False
        backoff = 1

        print("🚀 开始监控循环...")
        print("   使用 Match API 直接监控比赛历史")
        print("   每 10 秒检查一次新比赛")
        print("")
        
        while True:
            try:
                # 由于 Spectator API 权限问题，直接使用 Match API 监控
                print("🔍 检查最新比赛...")
                ids_url = f"{MATCH_BASE}/matches/by-puuid/{puuid}/ids?start=0&count=1"
                m_status, m_text, m_headers = await fetch_json(session, ids_url)
                
                if m_status == 200:
                    ids = __import__('json').loads(m_text)
                    if ids:
                        latest = ids[0]
                        if latest != last_seen_match:
                            print(f"🎮 发现新比赛: {latest}")
                            
                            # 检查是否已经处理过
                            if is_match_processed(latest, processed_matches):
                                print(f"对局 {latest} 已经处理过，跳过播报")
                                last_seen_match = latest
                            else:
                                # 获取比赛详情并处理
                                match_url = f"{MATCH_BASE}/matches/{latest}"
                                mm_status, mm_text, mm_headers = await fetch_json(session, match_url)
                                if mm_status == 200:
                                    match_detail = __import__('json').loads(mm_text)
                                    
                                    # 标记为已处理
                                    mark_match_processed(latest, processed_matches)
                                    print(f"对局 {latest} 已标记为已处理")
                                    
                                    # 调用 LOL 工作流程
                                    print("🎮 开始调用 LOL 工作流程进行播报...")
                                    try:
                                        # 使用 subprocess 调用 LOL 工作流程，避免事件循环冲突
                                        print("🔄 启动 LOL 工作流程子进程...")
                                        # 设置环境变量以支持UTF-8编码
                                        env = os.environ.copy()
                                        env['PYTHONIOENCODING'] = 'utf-8'
                                        
                                        result = subprocess.run([
                                            sys.executable, 
                                            "lol_workflow.py"
                                        ], capture_output=True, text=True, timeout=300, 
                                        encoding='utf-8', errors='replace', env=env)  # 5分钟超时，处理编码问题
                                        
                                        if result.returncode == 0:
                                            print("✅ LOL 工作流程播报完成")
                                            if result.stdout:
                                                print(f"   输出: {result.stdout}")
                                        else:
                                            print(f"❌ LOL 工作流程播报失败: {result.stderr}")
                                    except subprocess.TimeoutExpired:
                                        print("❌ LOL 工作流程超时")
                                    except Exception as e:
                                        print(f"❌ LOL 工作流程播报失败: {e}")
                                    
                                    last_seen_match = latest
                                else:
                                    print(f"获取比赛详情失败: {mm_status}")
                        else:
                            print("ℹ️ 没有新比赛，继续监控...")
                    else:
                        print("ℹ️ 没有找到比赛记录，继续监控...")
                else:
                    print(f"❌ 获取比赛列表失败: {m_status}")
                
                # 等待后继续
                print(f"⏰ 等待 {POLL_SECONDS_WHEN_IDLE} 秒后继续监控...")
                await asyncio.sleep(POLL_SECONDS_WHEN_IDLE)
                continue

            except Exception as e:
                print("异常：", e)
                backoff = min(BACKOFF_MAX, backoff * 2)
                await asyncio.sleep(backoff)

if __name__ == "__main__":
    asyncio.run(monitor_player())
