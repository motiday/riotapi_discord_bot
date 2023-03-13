# 色々作ったモジュールをここで呼び出す。

# match_log.pyにあるget_match()関数を呼び出す
# Path: cocords\riotapi_discord_bot\main.py
import match_log

match = match_log.get_match()
print(match)

# matchの結果から、試合の詳細を取得する
# 試合詳細には敵から最もダメージを受けたプレイヤーの情報が含まれている
# 最もダメージを受けたプレイヤーの情報を取得する
# Path: cocords\riotapi_discord_bot\main.py

print(match['participants'][0])