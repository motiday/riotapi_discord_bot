import discord
import asyncio


from discord.ext import commands

intents = discord.Intents.all()
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# ロールをまとめたオブジェクト
# TODO 今後ロールが増える場合ここに追記していく
server_roles_list = [{
    'emoji_type': '☠️',
    'role_name': 'ガンガンファイト',
}, {
    'emoji_type': '🥱',
    'role_name': '非戦闘',
}, {
    'emoji_type': '🕵️',
    'role_name': 'タスク一筋',
},
]

# riotapiのキーを定義する変数を用意する
with open('D:/Work/discord_py_bot/ignores/discord_token.txt') as f:
    discord_token = f.read()

# パーティ作成のコマンドから実行される処理


@bot.event
async def on_message(message):
    # テキストチャンネル「冒険者ギルド」のIDを指定
    CHANNEL_ID = 1090650082027786241
    # テキストチャンネル「冒険者ギルド」以外の場合は処理を終了する
    if message.channel.id != CHANNEL_ID:
        return

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

        # カテゴリー指定を行う ボイスチャンネルのカテゴリーを指定
        voice_category = discord.utils.get(
            guild.categories, id=1090650307517763604)
        # TODO ロールによるボイスチャンネルの入場制限を設ける
        


        # ボイスチャットチャンネルを作成する処理
        await guild.create_voice_channel(name=party_name.lower(), overwrites=overwrites, category=voice_category)
        # カテゴリー指定を行う テキストチャンネルのカテゴリーを指定　今回は「群れチャット」を指定する
        text_category = discord.utils.get(
            guild.categories, id=1090650859328786594)
        # テキストチャンネルを作成する処理
        await guild.create_text_channel(name=party_name.lower(), overwrites=overwrites, category=text_category)

        print(party_name.lower())
        # ギルドのチャンネルのコレクションを取得
        channels = guild.channels
        # チャンネルのコレクションからボイスチャンネル名の一致するボイスチャンネルのIDを取得する
        voice_channel = list(
            filter(lambda c: c.name == party_name.lower(), channels))[0]

        voice_channel_id = voice_channel.id
        # パーティ作成者にメンションを付けてメッセージを送信する
        await message.channel.send(f'{message.author.mention} パーティを作成しました★{party_name} 開かれたパーティはこっちだよ！。 https://discord.com/channels/{guild.id}/{voice_channel_id}')

    # ダイレクトメッセージの場合
    # 匿名チャットの処理
    # このボットにDMを送った場合、そのメッセージをテキストチャンネル「秘密の花園」へ送信する
    if isinstance(message.channel, discord.DMChannel):
        client = discord.Client(intents=intents)
        # 自分のメッセージは無視する
        if message.author == client.user:
            return

        # テキストチャンネル「秘密の花園」のIDを指定
        CHANNEL_ID = 1090642220958371840
        # テキストチャンネル「秘密の花園」を取得
        channel = bot.get_channel(CHANNEL_ID)

        # テキストチャンネル「秘密の花園」にメッセージを送信
        await channel.send(f'匿名さんからのメッセージです。 \n{message.content}')


@bot.event
async def on_voice_state_update(member, before, after):
    # 対象のボイスチャンネル名が「general」の場合は処理を終了する
    if before.channel is not None and before.channel.name == 'general':
        return

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

            # ボイスチャンネルの名前を取得
            channel_name = before.channel.name
            # 取得したボイスチャンネルと同名のサーバー内の同じ名前のテキストチャンネルとボイスチャンネルを取得する
            for guild in bot.guilds:
                text_channel = discord.utils.get(
                    guild.text_channels, name=channel_name)
                # 取得したテキストチャンネルを出力
                print(text_channel)
                voice_channel = discord.utils.get(
                    guild.voice_channels, name=channel_name)

                # チャンネルが存在する場合は削除する
                if text_channel is not None:
                    await text_channel.delete()
                if voice_channel is not None:
                    await voice_channel.delete()

            # 「冒険者ギルド」テキストチャンネルにメッセージを送信
            channel = bot.get_channel(1090650082027786241)
            await channel.send(f'あれれ、誰もいないみたい {before.channel.name} チャンネルを削除するよ。')


@bot.event
async def on_raw_reaction_add(payload):
    # リアクションをしたメッセージのID
    message_id = payload.message_id
    # リアクションをしたユーザーのID
    user_id = payload.user_id
    # リアクションをしたチャンネルのID
    channel_id = payload.channel_id
    # リアクションをしたユーザーのリアクション
    emoji = payload.emoji.name

    # リアクションをしたメッセージが特定のメッセージであるかどうかを確認する
    if message_id == 1091009091821908118:  # メッセージIDを指定

        # この処理で、リアクションをしたユーザーに特定のロールを付与する
        # ユーザーはロールを一つしか持てないので、リアクションをしたユーザーに特定のロールを付与する前に、
        # そのユーザーが持っているロールをすべて削除する
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)
        member = discord.utils.find(lambda m: m.id == user_id, guild.members)

        # リアクションをしたユーザーのリアクションが特定のリアクションであるかどうかを確認する
        # server_roles_list から一致する絵文字を持つロールを取得する
        for server_role in server_roles_list:
            if emoji == server_role['emoji_type']:
                # リアクションをしたユーザーのリアクションが特定のリアクションである場合、特定のロールを付与する
                role = discord.utils.get(
                    guild.roles, name=server_role['role_name'])
                if role is not None:
                    await member.add_roles(role)
                    print('ロールを付与しました。')


# リアクションを取り消したときに、そのユーザーの特定のロールを削除する処理
@bot.event
async def on_raw_reaction_remove(payload):
    # リアクションをしたメッセージのID
    message_id = payload.message_id
    # リアクションをしたユーザーのID
    user_id = payload.user_id
    # リアクションをしたチャンネルのID
    channel_id = payload.channel_id
    # リアクションをしたユーザーのリアクション
    emoji = payload.emoji.name

    # リアクションをしたメッセージが特定のメッセージであるかどうかを確認する
    if message_id == 1091009091821908118:  # メッセージIDを指定

        # この処理で、リアクションをしたユーザーの特定のロールを削除する
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)
        member = discord.utils.find(lambda m: m.id == user_id, guild.members)

        # リアクションをしたユーザーのリアクションが特定のリアクションであるかどうかを確認する
        # server_roles_list から一致する絵文字を持つロールを取得する
        for server_role in server_roles_list:
            if emoji == server_role['emoji_type']:
                # リアクションをしたユーザーのリアクションが特定のリアクションである場合、特定のロールを削除する
                role = discord.utils.get(
                    guild.roles, name=server_role['role_name'])
                if role is not None:
                    await member.remove_roles(role)
                    print('ロールを削除しました。')

# ボットの起動とDiscordサーバーへの接続
bot.run(discord_token)
