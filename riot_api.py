# riotapiをインポートする
from riotwatcher import RiotWatcher

# riotapiのキーを外部ファイルから読み込む
with open('riotapi_key.txt', 'r') as f:
    riotapi_key = f.read()

# riotapiのキーを取得する
riotapi = RiotWatcher(riotapi_key)

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

    # サモナーの情報から最も使用頻度の高いキャラクターを取得する。
    # 直近の100試合から抽出する
    # その際、キャラクターのIDを取得する。
    most_played_champion_id = riotapi.get_champion_mastery(
        summoner['id'], region='jp')[0]['championId']

    # キャラクターのIDから、キャラクターの名前を取得する。
    most_played_champion_name = riotapi.static_get_champion_list(
        region='jp')['data'][str(most_played_champion_id)]['name']

    # キャラクターの名前返す。
    return most_played_champion_name


print(is_in_game('おおいそ ともや'))
