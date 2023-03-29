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
        # ボイスチャットチャンネルを作成する処理
        await guild.create_voice_channel(party_name, overwrites=overwrites, category=voice_category)
        # カテゴリー指定を行う テキストチャンネルのカテゴリーを指定
        text_category = discord.utils.get(
            guild.categories, id=1090650859328786594)
        # テキストチャンネルを作成する処理
        await guild.create_text_channel(party_name, overwrites=overwrites, category=text_category)

        # ギルドのチャンネルのコレクションを取得
        channels = guild.channels
        # チャンネルのコレクションからボイスチャンネル名の一致するボイスチャンネルのIDを取得する
        voice_channel = list(
            filter(lambda c: c.name == party_name, channels))[0]

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

            # 削除実行後にボイスチャンネルと同名のテキストチャンネルを削除
        for channel in member.guild.channels:
            if channel.name == before.channel.name:
                await channel.delete()

            # チャンネルを削除したことをテキストチャンネルに通知
        await member.guild.system_channel.send(f'あれれ、誰もいないみたい {before.channel.name} チャンネルを削除するよ。')


bot.run(discord_token)
