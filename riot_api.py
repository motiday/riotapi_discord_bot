#riotapiをインポートする
from riotwatcher import RiotWatcher

# riotapiのキーを外部ファイルから読み込む
with open('riotapi_key.txt', 'r') as f:
    riotapi_key = f.read()

#riotapiのキーを取得する
riotapi = RiotWatcher('RGAPI-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx')

# ゲーム情報を取得する
# この時、SummonerNameを入力すると、そのゲーム情報を取得することができる。
# ただし、ゲーム中でないとエラーが出る。
# そのため、ゲーム中かどうかを判定する必要がある。
# そのため、ゲーム中かどうかを判定する関数を作成する。
def is_in_game(summoner_name):
    # サモナー名を入力すると、そのサモナーの情報を取得する。
    # その際、regionを指定する必要がある。
    # 今回は、日本のサーバーを指定する。
    summoner = riotapi.get_summoner(name=summoner_name, region='jp')
    # サモナーの情報から、ゲーム中かどうかを判定する。
    # ゲーム中であれば、Trueを返す。
    # ゲーム中でなければ、Falseを返す。
    return summoner['gameId'] != 0

# ゲーム中かどうかを判定する関数を呼び出す。
# 今回は、ゲーム中であると仮定する。
# そのため、Trueを返す。
print(is_in_game('cocords'))

