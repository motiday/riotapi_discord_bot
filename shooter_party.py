import discord
from discord.ext import commands

intents = discord.Intents.default()
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

    # パーティ募集文からパーティが作成された時の処理
    if message.content.startswith('!joinparty'):
        party_name = message.content.split(' ')[1]
        guild = message.guild
        # パーティに参加する処理

        # パーティのボイスチャンネルに参加する処理

        # パーティのテキストチャンネルに参加する処理

        # パーティ作成者にメンションを付けてメッセージを送信する
        await message.channel.send(f'{message.author.mention} パーティに参加しました。')


bot.run(discord_token)
# 「SERVER MEMBERS INTENT」と「PRESENCE INTENT」が有効化されていることを確認する
# TODO WARNING  discord.ext.commands.bot Privileged message content intent is missing, commands may not work as expected.
