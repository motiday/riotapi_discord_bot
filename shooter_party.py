import discord
import asyncio


from discord.ext import commands

intents = discord.Intents.all()
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# riotapiのキーを定義する変数を用意する
with open('D:/Work/discord_py_bot/ignores/discord_token.txt') as f:
    discord_token = f.read()


@bot.event
async def on_message(message):
    # パーティ募集文からパーティが作成された時の処理
    if message.content.startswith('!createparty'):
        # 入力文字列のチェック
        if len(message.content.split(' ')) != 2:
            await message.channel.send('パーティ名を入力してください。　入力フォーマットは「!createparty パーティ名」です。')
            return

        # message の中を確認する
        party_name = message.content.split(' ')[1]
        guild = message.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        # ボイスチャットチャンネルを作成する処理
        await guild.create_voice_channel(party_name, overwrites=overwrites)

        # テキストチャンネルも作成する処理
        await guild.create_text_channel(party_name, overwrites=overwrites)

        # パーティ作成者にメンションを付けてメッセージを送信する
        await message.channel.send(f'{message.author.mention} パーティを作成しました。')

        # 作成されたボイスチャンネルが誰もいない場合が10分続いた場合　削除する
        # ボイスチャンネルの削除処理

        # テキストチャンネルの削除処理

    # パーティ募集文からパーティが作成された時の処理
    if message.content.startswith('!joinparty'):
        party_name = message.content.split(' ')[1]
        guild = message.guild
        # パーティに参加する処理 (ボイスチャンネルとテキストチャンネルに参加する処理)

        # パーティのボイスチャンネルに参加する処理

        # パーティのテキストチャンネルに参加する処理

        # パーティ作成者にメンションを付けてメッセージを送信する
        await message.channel.send(f'{message.author.mention} パーティに参加しました。')


@bot.event
async def on_voice_state_update(member, before, after):
    # ボイスチャンネルから退出したとき
    if before.channel is not None and after.channel is None:

        # ディレイの秒数を指定する変数を用意する
        # delay_seconds = 300
        delay_seconds = 3

        # ボイスチャンネルが空になったかどうかを確認
        if len(before.channel.members) == 0:
            # ボイスチャンネルを5分後に削除
            await asyncio.sleep(delay_seconds)  # 待機
            await before.channel.delete()

            # 削除実行後にボイスチャンネルと同名のテキストチャンネルを削除
        for channel in member.guild.channels:
            if channel.name == before.channel.name:
                await channel.delete()

            # チャンネルを削除したことをテキストチャンネルに通知
        await member.guild.system_channel.send(f'あれれ、誰もいないみたい {before.channel.name} チャンネルを削除するよ。')


bot.run(discord_token)
# 「SERVER MEMBERS INTENT」と「PRESENCE INTENT」が有効化されていることを確認する
# TODO WARNING  discord.ext.commands.bot Privileged message content intent is missing, commands may not work as expected.
