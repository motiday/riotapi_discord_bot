import requests

# Riot Games APIを使用するためのライブラリをインポートする
from riotwatcher import LolWatcher

# riotapiのキーを定義する変数を用意する
with open('D:/Work/discord_py_bot/ignores/riotapi_key.txt') as f:
    riotapi_key = f.read()

watcher = LolWatcher(riotapi_key)
region = 'jp1'
summoner_name = 'おおいそともや'
summoner = watcher.summoner.by_name(region, summoner_name)
matchlist = watcher.match.matchlist_by_puuid(region, summoner['puuid'])
print(matchlist)
# 取得したmatchlistは配列となっている
# そのため、配列の中の要素を指定する必要がある
# 今回は最新の試合の詳細を取得するため、配列の0番目を指定する

match = watcher.match.by_id(region, matchlist[0])
print(match)


# # レスポンスの中身を確認する
# print(response.json())

# 実行元にmatchを返す為に関数を定義する
def get_match():
    return match

