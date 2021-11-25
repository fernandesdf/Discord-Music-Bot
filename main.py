import os
import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

TOKEN = os.environ['discordToken']
#TOKEN_YOUTUBE = os.environ['youtubeToken']



queue = []

class YTDLSource:

  def __init__(self, ctx: commands.context, url: str):
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

    ytdl = YoutubeDL(YDL_OPTIONS)

    self.FFMPEG_OPTIONS = {
      'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'
    }

    info = ytdl.extract_info(url, download=False)
    self.requester = ctx.author
    self.channel = ctx.channel
    self.info = info
    
    self.url = info['url']
    self.uploader = info['uploader']
    self.uploader_url = info['uploader_url']
    date = info['upload_date']
    self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
    self.title = info['title']
    self.thumbnail = info['thumbnail']
    self.description = info['description']
    self.duration = self.parse_duration(int(info['duration']))
    self.tags = info['tags']
    self.webpage_url = info['webpage_url']
    self.views = info['view_count']
    self.likes = info['like_count']
    self.dislikes = info['dislike_count']  


class Music(commands.cog):
"""
  @commands.command() #ctx = context
  async def play(ctx, url : str):

    if not ctx.guild.voice_client in client.voice_clients:
      # Join
      voice = await ctx.author.voice.channel.connect()
      #print('Connected to the channel: {0}'.format(ctx.author.voice.channel))

      # Play
      with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        queue.append(info)
        URL = info['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
        title = str(info['title'])
        
        embed = discord.Embed(
                    description="Started playing **{0}**".format(title),
                    color=discord.Color.green())
        
        await ctx.send(embed=embed)
    else:
      # Play
      voice = ctx.guild.voice_client
      if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
          info = ydl.extract_info(url, download=False)
          queue.append(info)
          URL = info['url']
          voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
          voice.is_playing()
          title = str(info['title'])
          
          embed = discord.Embed(
                      description="Started playing **{0}**".format(title),
                      color=discord.Color.green())
          
          await ctx.send(embed=embed)
      else:
        with YoutubeDL(YDL_OPTIONS) as ydl:
          info = ydl.extract_info(url, download=False)
          queue.append(info)

        embed = discord.Embed(
                    description="**{0}** is already being played".format("A track"),
                    color=discord.Color.orange())
        
        await ctx.send(embed=embed)
"""

  @commands.command()
  async def pause(ctx):
    ctx.voice_client.pause()
    embed = discord.Embed(
                  description="Track has been paused :pause_button:",
                  color=discord.Color.green())
      
    await ctx.send(embed=embed)

  @commands.command()
  async def resume(ctx):
    ctx.voice_client.resume()
    embed = discord.Embed(
                  description="Track has been resumed :arrow_forward:",
                  color=discord.Color.green())
      
    await ctx.send(embed=embed)

  @commands.command()
  async def skip(ctx):
    ctx.voice_client.stop()
    embed = discord.Embed(
                  description="Track has been skipped",
                  color=discord.Color.green())
      
    await ctx.send(embed=embed)

  @commands.command()
  async def leave(ctx):  
    
    embed = discord.Embed(
                  description="Leaving... :wave:",
                  color=discord.Color.red())
      
    await ctx.send(embed=embed)
    await ctx.voice_client.disconnect()


client = commands.Bot(command_prefix="!")

client.add_cog(Music(client))

@commands.event  # Check if bot is ready
async def on_ready():
  print('Music Roi is ready!')

client.run(TOKEN)