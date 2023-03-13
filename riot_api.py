
# サモナーネームを定義する変数を用意する
summoner_name = 'おおいそともや'

# riotapiのキーを定義する変数を用意する
with open('D:/Work/discord_py_bot/ignores/riotapi_key.txt') as f:
    riotapi_key = f.read()

# urlを指定する変数を用意する
# url + サモナーネーム + riotapiのキー となる形で連結する
url = 'https://jp1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summoner_name + '?api_key=' + riotapi_key

# リクエストを送信する
# その際、requestsをインポートする
import requests
response = requests.get(url)

# レスポンスを確認する
# print(response)

# レスポンスの中身を確認する
# print(response.json())

