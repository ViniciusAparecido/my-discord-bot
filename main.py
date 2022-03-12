#libraries
import discord
from discord.ext import commands
import random
import os
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from discord.utils import get
from time import sleep
from random import randint
from discord.ext import commands, tasks
from discord.ext.commands.errors import MissingRequiredArgument, CommandNotFound
import youtube_dl
import asyncio

intents = discord.Intents.default()
intents.members = True

#bot prefix
client = commands.Bot(command_prefix=">",
                      case_insensitive=True,
                      intents=intents)

#when the bot starts sent an activation message
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle,
                                 activity=discord.Game('>help'))
    print('we entered as {0.user}'.format(client))

#the bot enters a voice channel
@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await ctx.send('the bot joined the voice channel')
  
#the bot leaves the voice channel
@client.command()
async def leave(ctx):
  voice_client = ctx.message.guild.voice_client
  await voice_client.disconnect()
  
  await ctx.send('the bot came out of the voice channel')

#the bot plays the chosen song
@client.command()
async def play(ctx, url):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
        await ctx.send('the bot is playing')


    else:
        await ctx.send("the bot is ready to play")
        return

#the bot returns to play the song chose
@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        voice.resume()
        await ctx.send('depaused music')

#the bot pauses the music that is playing
@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
        await ctx.send('paused music')

#the bot stop playing the song that was playing
@client.command()
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.stop()
        await ctx.send('the music stopped')

#o bot show at latency
@client.command()
async def ping(ctx):
    await ctx.send(f'pong! {round(client.latency * 1000)}ms')

#the bot clears the channel where the command was given
@client.command()
async def clear(ctx, amount=20):
    await ctx.channel.purge(limit=amount)

#the bot expels a member
@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'the member:{member.mention},was kicked!')

#the bot bans a member
@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'the member:{member.mention},was banned!')

#the bot removes the member ban
@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name,
                                               member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'unbanned {user.mention}#{user.discriminator}')
            return

#the bot plays a dice
@client.command()
async def dice(ctx, Number):
    Variable = random.randint(1, int(Number))
    await ctx.send(f'the dice fell on {Variable}')

#the bot shows the user's avatar
@client.command()
async def avatar(ctx, *, avamember: discord.Member = None):
    userAvatarUrl = avamember.avatar_url
    await ctx.send(userAvatarUrl)

#the bot sends an embed with the gif
@client.command(brief=":sad")
async def sad(ctx):
    embed = discord.Embed(title='', description='', colour=0)

    embed.set_author(name=client.user.name, icon_url='')

    embed.set_thumbnail(url='')

    embed.set_image(
        url= 'https://c.tenor.com/_kGSWq3wq4IAAAAj/sad-pepe.gif')

    embed.set_footer(text='')

    await ctx.send(embed=embed)
  
#the bot warns about possible typos in typing
@client.event
async def on_command_error(ctx, error):
  if isinstance(error,MissingRequiredArgument):
    await ctx.send("send all arguments")
  elif isinstance(error,CommandNotFound):
      await ctx.send("the command does not exist")
  else:
    raise error

#token of your bot
client.run('')
