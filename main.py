import os
import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

TOKEN = os.environ['discordToken']
#TOKEN_YOUTUBE = os.environ['youtubeToken']

client = commands.Bot(command_prefix="!")

@client.event  # Check if bot is ready
async def on_ready():
  print('Music Roi is ready!')

#@client.command()
#async def test(ctx, arg):
#  print(ctx.message)
#  print(ctx.message.channel)
#  print(ctx.author.voice.channel)
#  print(ctx.guild.voice_client)
#  await ctx.send(arg)

@client.command() #ctx = context
async def play(ctx, url : str):

  # Join  
  if not ctx.guild.voice_client in client.voice_clients:
    voice = await ctx.author.voice.channel.connect()
    print('Connected to the channel: {0}'.format(ctx.author.voice.channel))


  # Play
  FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

  YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
  }

  if not voice.is_playing():
    with YoutubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(url, download=False)
      URL = info['url']
      voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
      voice.is_playing()
      title = str(info['title'])
      
      embed = discord.Embed(
                  description="Started playing **{0}**".format(title),
                  color=discord.Color.green())
      
      await ctx.send(embed=embed)
  else:
    voice = get(client.voice_clients, guild=ctx.guild)
    print(voice.source)
    embed = discord.Embed(
                description="**{0}** is already being played".format("A track"),
                color=discord.Color.orange())
    
    await ctx.send(embed=embed)

@client.command()
async def pause(ctx):
  ctx.voice_client.pause()
  embed = discord.Embed(
                description="Track has been paused :pause_button:",
                color=discord.Color.green())
    
  await ctx.send(embed=embed)

@client.command()
async def resume(ctx):
  ctx.voice_client.resume()
  embed = discord.Embed(
                description="Track has been resumed :arrow_forward:",
                color=discord.Color.green())
    
  await ctx.send(embed=embed)

@client.command()
async def skip(ctx):
  ctx.voice_client.stop()
  embed = discord.Embed(
                description="Track has been skipped",
                color=discord.Color.green())
    
  await ctx.send(embed=embed)

@client.command()
async def leave(ctx):  
  
  embed = discord.Embed(
                description="Leaving... :wave:",
                color=discord.Color.red())
    
  await ctx.send(embed=embed)
  await ctx.voice_client.disconnect()


client.run(TOKEN)