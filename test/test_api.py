import requests
import os

RIOT_API_KEY = os.getenv("RIOT_API_KEY")
SUMMONER_NAME = "Loveù"
TAG_LINE = "NA1"
REGION = "na1"
MASS_REGION = "americas"

HEADERS = {"X-Riot-Token": RIOT_API_KEY}

def get_puuid(name, tag):
    url = f"https://{MASS_REGION}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()["puuid"]

def get_last_match_id(puuid):
    url = f"https://{MASS_REGION}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=1"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()[0]

def get_match_details(match_id):
    url = f"https://{MASS_REGION}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()

def get_last_game_status():
    puuid = get_puuid(SUMMONER_NAME, TAG_LINE)
    match_id = get_last_match_id(puuid)
    match = get_match_details(match_id)
    meta = match["metadata"]
    info = match["info"]
    idx = meta["participants"].index(puuid)
    p = info["participants"][idx]
    print(f"{SUMMONER_NAME}#{TAG_LINE}: {'WIN' if p['win'] else 'LOSS'}")
    print(f"{p['championName']}  KDA: {p['kills']}/{p['deaths']}/{p['assists']}")

if __name__ == "__main__":
    get_last_game_status()
