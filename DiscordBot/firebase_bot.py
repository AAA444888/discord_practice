#導入Discord.py
import discord
from discord.ext import commands
from firebase import firebase
import get_data
data=get_data.get_data()
url = data['url']
fdb = firebase.FirebaseApplication(url, None)
#client 是我們與 Discord 連結的橋樑，intents 是我們要求的權限
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
TOKEN = data['token']
intents = discord.Intents.all()
# command_prefix是前綴符號，可以自由選擇($, #, &...)
bot = commands.Bot(command_prefix = "%", intents = intents,case_insensitive=True)
@bot.event
# 當機器人完成啟動
async def on_ready():
    print(f"目前登入身份 --> {bot.user}")


    
@bot.command()
# 輸入%Hello呼叫指令
async def put(ctx):
    await ctx.send("點名成功")
    fdb.put('/',f'{ctx.author}',1)

@bot.command()
# 輸入%fat呼叫指令
async def query(ctx):

    x=fdb.get('/',f'{ctx.author}')
    if x==1:
        await ctx.send("點名成功")
    else:
        await ctx.send("未完成點名")
          

bot.run(TOKEN) #TOKEN在剛剛Discord Developer那邊「BOT」頁面裡面