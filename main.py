# 色々作ったモジュールをここで呼び出す。

# match_log.pyにあるget_match()関数を呼び出す
# Path: cocords\riotapi_discord_bot\main.py
import match_log
import json

match = match_log.get_match()

# matchをjson形式に変換する
match_json = json.dumps(match)
# print(match_json)

# match_jsonからmetadataを取得する
# metadataには試合の詳細が含まれている
# metadataを取得する
metadata = match['metadata']
# print(metadata)

# metadataからinfoを取得する
# infoには試合の詳細が含まれている
# infoを取得する
info = match['info']
print(info)

participants = match['info']['participants']

# 参加者の名前を取得する
for participant in participants:
    print(participant['summonerName'])
