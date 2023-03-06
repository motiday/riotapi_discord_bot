# discordbotを作成します

import discord
from discord.ext import commands
import os
import traceback


import configparser

# 設定ファイルからトークンを読み込む
config = configparser.ConfigParser()
config.read('config.ini')
TOKEN = config.get('discord', 'token')

# botのコマンドの接頭辞を設定
bot = commands.Bot(command_prefix='/')
# tokenを環境変数から取得
token = os.environ['DISCORD_BOT_TOKEN']

# 起動時に動作する処理
@bot.event
async def on_ready():
    print('ログインしました')

# メッセージ受信時に動作する処理
@bot.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('にゃーん')

    # その他のメッセージ
    await bot.process_commands(message)

# Botの起動とDiscordサーバーへの接続
bot.run(token)
