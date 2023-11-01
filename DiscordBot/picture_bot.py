#導入Discord.py
import discord
from discord import File
import aiohttp
import os
import get_data

data=get_data.get_data()
#client 是我們與 Discord 連結的橋樑，intents 是我們要求的權限
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
save_path = './saved_images/'  # 指定圖片保存的路徑
if not os.path.exists(save_path):
    os.makedirs(save_path)

#調用event函式庫
@client.event
#當機器人完成啟動時
async def on_ready():
    print('目前登入身份：',client.user)

@client.event
#當有訊息時
async def on_message(message):
    #排除自己的訊息，避免陷入無限循環
    if message.author == client.user:
        return
    #如果以「圖」開頭
    if message.content.startswith('圖'):
      #分割訊息成兩份
      pic = discord.File('1.png')
      await message.channel.send(file=pic)
      
      
    if message.attachments:
        for attachment in message.attachments:
            # 如果附件的 URL 是一個圖片
            if any(attachment.filename.endswith(image_ext) for image_ext in [".jpg", ".jpeg", ".png", ".gif", ".bmp"]):
                await save_image(attachment.url, attachment.filename)
                await message.channel.send(f"已經儲存了你的圖片： {attachment.filename}")
                
async def save_image(url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            with open(os.path.join(save_path, filename), 'wb') as f:
                f.write(await response.read())

client.run(data['token'])