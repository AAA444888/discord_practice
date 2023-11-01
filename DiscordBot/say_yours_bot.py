import get_data

data=get_data.get_data()
token=data['token']
#導入Discord.py
import discord
import asyncio
import time
from firebase import firebase

#client 是我們與 Discord 連結的橋樑，intents 是我們要求的權限
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
url = data['url']
fdb = firebase.FirebaseApplication(url, None)

#調用event函式庫
@client.event
#當機器人完成啟動時
async def on_ready():
    print('目前登入身份：',client.user)
    game = discord.Game('努力學習py中')
    #discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
    await client.change_presence(status=discord.Status.idle, activity=game)
    
@client.event
#當有訊息時
async def on_message(message):
    if message.content.startswith('跟我打聲招呼吧'):
        channel = message.channel
        #機器人叫你先跟他說你好
        await channel.send('那你先跟我說你好')
		#檢查函式，確認使用者是否在相同頻道打上「你好」
        def checkmessage(m):
            return m.content == '你好' and m.channel == channel
		#獲取傳訊息的資訊(message是類型，也可以用reaction_add等等動作)
        msg = await client.wait_for('message', check=checkmessage)
        await channel.send('嗨, {.author}!'.format(msg))
    if message.content == '我好帥喔':
        #刪除傳送者的訊息
        await message.delete()
        #然後回傳訊息
        await message.channel.send('不好意思，不要騙人啦')
    if message.content == '群組':
        #獲取當前所在群組(極限150個，預設為100個)，並用flatten將它全部移到guilds這個list裡面
        guilds = await client.fetch_guilds(limit=150).flatten()
        #遍尋 guilds
        for i in guilds:
            #由於我們只要 guilds 的name 就好，當然也可以獲取 id~
            await message.channel.send(i.name)
        
client.run(token) #TOKEN 在剛剛 Discord Developer 那邊「BOT」頁面裡面