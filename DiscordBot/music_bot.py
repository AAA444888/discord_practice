import discord
from discord.ext import commands
import yt_dlp
import get_data

data=get_data.get_data()
TOKEN = data['token']
PREFIX = '!'
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX,intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command(name='play', help='To play song')
async def play(ctx, url):
    ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': '%(title)s.%(etx)s',
            'quiet': False
        }
    song_info = yt_dlp.YoutubeDL(ydl_opts).extract_info(url, download=False)
    voice_client = ctx.message.guild.voice_client
    if not voice_client.is_connected():
        await ctx.send("Bot is not connected to a voice channel.")
        return
    voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=song_info['url']))
@bot.command(name='pause', help='Pause the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.pause()
        await ctx.send("Music paused")
    else:
        await ctx.send("No music is playing right now.")
@bot.command(name='resume', help='Resume the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        voice_client.resume()
        await ctx.send("Music resumed")
    else:
        await ctx.send("Music is not paused.")

bot.run(TOKEN)