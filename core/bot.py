from __future__ import annotations

import os
import sys
from typing import Optional
from discord.ext import commands , tasks
from logging import getLogger; log  = getLogger("Bot")
import discord
from discord import app_commands 
from embed import Embed
from tortoise import Tortoise
import config
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import asyncio
import random
import requests
from http.client import HTTPException

cluster = MongoClient("mongodb+srv://asj646464:8cdNz0UEamn8I6aV@cluster0.0ss9wqf.mongodb.net/?retryWrites=true&w=majority")
# Send a ping to confirm a successful connection
db = cluster["gif"]
collection = db["autogif"]
new_GUILD = db['guilds']


__all__ = (

    "Bot",
)

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or('au!'),
            intents=discord.Intents.all(),
            chunk_guild_at_startup=False,
            help_command=None,
        )

    async def on_tree_error(self ,interaction:discord.Interaction , error:app_commands.AppCommandError):
        if isinstance(error , app_commands.CommandOnCooldown):
            return await interaction.response.send_message(f'command cooldown try after {round(error.retry_after)}Seconds' , ephemeral=True)
        if isinstance(error,app_commands.MissingPermissions):
            return await interaction.response.send_message(f'your permission is not enough',ephemeral=True)
        if isinstance(error , app_commands.BotMissingPermissions):
            return await interaction.response.send_message(f'bot permission is not enough' , ephemeral=True)
        if isinstance(error , app_commands.MissingRole):
            return await interaction.response.send_message(f'Bot Missing Role' , ephemeral=True)
        if isinstance(error , app_commands.CheckFailure):
            return await interaction.response.send_message(f'something went wrong try again' , ephemeral=True)


    async def setup_hook(self):
        for filename in os.listdir('Bot4/cogs'):
            if not filename.startswith("_") and not filename.startswith("c"):
                await self.load_extension(f'cogs.{filename}.plugin')
                
    async def on_ready(self):
        log.info(f'logged in as {self.user} , ID: {self.user.id}')
        self.auto_gif_sender.start()
        await self.change_presence(status=discord.Status.online , activity=discord.Activity(type=discord.ActivityType.watching, name="Nice Gifs"))    

    async def userpic(self , subject):
        url = "https://giphy.p.rapidapi.com/v1/gifs/search"
        random_num = random.randint(0,4899)

        querystring = {"api_key":"c7WCw3Xyde3F3VCNEemRzkK9ZdC5mkL6","q":subject,"limit":"50" ,'offset':0}

        headers = {
            "X-RapidAPI-Key": "21eb3ac3b1msh4b51216a0cdeb6bp19d362jsn78f7b5fa6e25",
            "X-RapidAPI-Host": "giphy.p.rapidapi.com"
        }
        flag = True
        while (flag):
            response = requests.get(url, headers=headers, params=querystring)
            if response.status_code == 429:
                await asyncio.sleep(60, loop=self.loop)
                continue

            elif response.status_code >=200 and response.status_code <300:
                break
            else:
                raise HTTPException(409 , "error happend")

        filter1 = response.json()
        
        offset_total=filter1['pagination']['total_count']
        new_offset = offset_total - 5
        if new_offset <= 0:
            new_offset = 0
        else:
            new_offset = random.randint(0 , offset_total)

        querystring = {"api_key":"c7WCw3Xyde3F3VCNEemRzkK9ZdC5mkL6","q":subject,"limit":"50" ,'offset':new_offset}
        while (flag):
            response = requests.get(url, headers=headers, params=querystring)
            if response.status_code == 429:
                await asyncio.sleep(60, loop=self.loop)
                continue

            elif response.status_code >=200 and response.status_code <300:
                break
            else:
                raise HTTPException(409 , "error happend")
    
        filter1 = response.json()
        range_search = filter1['pagination']['count']



        return response.json() , range_search

    @tasks.loop(hours=6)
    async def auto_gif_sender(self):
        # delta = discord.utils._parse_ratelimit_header(r)
        webhooker = ''
        
        if (find1:=new_GUILD.find({"key":True})):
            for jj in find1:
                if (find:= collection.find_one({"server_id":jj['server']})):
                    guild = self.get_guild(jj['server'])
                    if guild is not None:
                        count= 1
                        for i in range(10):
                            name_slot =f'slot{count}_subject'
                            name_channel = f'slot{count}_channel'
                            name_gif = f'slot{count}_count'
                            name_webhook = f'slot{count}_webhook'
                            subject_gif = find[f'{name_slot}']
                            channel_id = find[f'{name_channel}']
                            gif_count = find[f'{name_gif}']
                            gif_webhook = find[f'{name_webhook}']
                            if subject_gif is not None and channel_id is not None and gif_count is not None:
                                channel_checker = guild.get_channel(channel_id)
                                if channel_checker is not None and gif_webhook is not None:
                                    webhooker = discord.utils.get(await guild.webhooks() , id = gif_webhook)
                                    if webhooker is not None:
                                        pass
                                    else:
                                        member1 = discord.utils.get(guild.members , id = guild.me.id)
                                        webhook_avatar =member1.display_avatar
                                        profile_webhook= await webhook_avatar.read()
                                        webhooker=await channel_checker.create_webhook(name='AutoGif' , avatar=profile_webhook)
                                        webhook_channel_set=discord.Object( channel_id, type='abc.Snowflake')
                                        await webhooker.edit(channel=webhook_channel_set)
                                        collection.update_one({"server_id":guild.id} , {"$set":{f'{name_webhook}':webhooker.id}})                                    

                                    response , range_search = await self.userpic(subject_gif)
                                    list_temp = []
                                    selector :int=None
                                    loop_counter = 0
                                    flag = True
                                    if range_search-1 > gif_count:
                                        while (flag):
                                            selector = random.randint(0 , range_search-1)
                                            if selector in list_temp:
                                                continue
                                            list_temp.append(selector)
                                            try:
                                                await asyncio.sleep(3)
                                                await webhooker.send(response['data'][selector]['url'])
                                            except:
                                                raise HTTPException(409 , 'nothing there')
                                            if loop_counter == 2:
                                                await asyncio.sleep(10)
                                            loop_counter+=1
                                            if loop_counter >=gif_count:
                                                flag=False
                            count +=1

    async def on_connect(self):
        log.info(f'succesfully connected')
        self.tree.on_error = self.on_tree_error
        # if '-sync' in sys.argv:
        synced_command = await self.tree.sync()
        log.info(f'synced {len(synced_command)} commands')

    async def success(self , message:str, interaction:discord.Interaction,*,ephemeral:bool=False , embed:Optional[bool] = True)->Optional[discord.WebhookMessage]:
        if embed:
            if interaction.response.is_done():
                return await interaction.followup.send(
                    embed = Embed(description=message , color =discord.Colour.green()),
                    ephemeral=ephemeral
                )
            return await interaction.response.send_message(
                embed = Embed(description=message , color=discord.Colour.green()),
                ephemeral=ephemeral
            )
        else:
            if interaction.response.is_done():
                return await interaction.followup.send(content=message , ephemeral=ephemeral)
            return await interaction.response.send_message(content=message , ephemeral=ephemeral)

    async def error(self , message:str, interaction:discord.Interaction,*,ephemeral:bool=True , embed:Optional[bool] = True)->Optional[discord.WebhookMessage]:
        if embed:
            if interaction.response.is_done():
                return await interaction.followup.send(
                    embed = Embed(description=message , color =discord.Colour.red()),
                    ephemeral=ephemeral
                )
            return await interaction.response.send_message(
                embed = Embed(description=message , color=discord.Colour.red()),
                ephemeral=ephemeral
            )
        else:
            if interaction.response.is_done():
                return await interaction.followup.send(content=message , ephemeral=ephemeral)
            return await interaction.response.send_message(content=message , ephemeral=ephemeral)
    


    async def get_or_fetch_guild(self,guild_id:int)-> discord.Guild | None:
        return self.get_guild(guild_id) or await self.fetch_guild(guild_id)

    
    def get_message(
        self,
        message_id:int,
        channel_id:int,
        guild_id:int,
    )->discord.PartialMessage:
        return self.get_partial_messageable(channel_id , guild_id=guild_id).get_partial_message(message_id)

