from __future__ import annotations
from ast import Try
from gc import collect
from http.client import HTTPException

from core.bot import Bot
from typing import Any, Optional , Callable , Literal , Union
from datetime import timedelta , datetime
from cogs.cog_config import Plugin
from discord.ext import commands , tasks 
from humanfriendly import parse_timespan , InvalidTimespan
from discord import app_commands , User , utils as Utils , CategoryChannel , ForumChannel , PartialMessageable , Object , TextChannel , Thread , Permissions , StageChannel , VoiceChannel , Role , Attachment , Forbidden , Color
from pytz import UTC
from aiohttp import ClientSession
import aiohttp
import discord
import config
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from easy_pil import Editor , Canvas, load_image_async , Font
from config import TOKEN
import requests
from typing import Union 
from datetime import timedelta , datetime
from core.embed import Embed
from core.models import Giveawaymodel
from views.giveaway import GiveawayView
import time
import humanfriendly
import asyncio
from discord import ui
from discord import Colour
import random


cluster = MongoClient("mongodb+srv://asj646464:8cdNz0UEamn8I6aV@cluster0.0ss9wqf.mongodb.net/?retryWrites=true&w=majority")
# Send a ping to confirm a successful connection
db = cluster["gif"]
collection = db["autogif"]
new_GUILD = db['guilds']

class AutoGifGen(ui.View):

    def __init__(self , bot:Bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
        self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
        self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)

    async def picgenerator(self , subject):
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



    @ui.button(label='Subject 1' , custom_id='Subject_1' , style=discord.ButtonStyle.primary)
    async def subject1(self, interaction:discord.Interaction,_):

        if interaction.guild.me.top_role.position > interaction.user.top_role.position and interaction.user.id != interaction.guild.owner_id:
            return await interaction.response.send_message('your role is not above me then you cant use this button' , ephemeral=True)


    
        async def on_sumbit(ctx):
            webhooker = ''
            try:
                await ctx.response.defer()
                self.subject_gif= str(self.subject_gif)
                self.channel_gif = str(self.channel_gif)
                self.count_gif =str(self.count_gif) 
                if " " not in self.subject_gif:
                    self.subject_gif = self.subject_gif + ' ' + self.subject_gif
                try:
                    self.channel_gif = int(self.channel_gif)
                    channel_checker = discord.utils.get(ctx.guild.text_channels , id=self.channel_gif)
                    if channel_checker is not None:
                        if (find_webhook:=collection.find_one({"server_id":ctx.guild_id})):
                            webhook_id = find_webhook['slot1_webhook']
                            if webhook_id is not None:
                                webhooker = discord.utils.get(await ctx.guild.webhooks() , id = webhook_id)
                                if webhooker is not None:
                                    pass
                                else:
                                    member1 = discord.utils.get(ctx.guild.members , id = ctx.guild.me.id)
                                    webhook_avatar =member1.display_avatar
                                    profile_webhook= await webhook_avatar.read()
                                    webhooker=await channel_checker.create_webhook(name='AutoGif' , avatar=profile_webhook)
                                    webhook_channel_set=discord.Object(self.channel_gif , type='abc.Snowflake')
                                    await webhooker.edit(channel=webhook_channel_set)
                                    collection.update_one({"server_id":ctx.guild_id} , {"$set":{"slot1_webhook":webhooker.id}}) 
                            else:
                                member1 = discord.utils.get(ctx.guild.members , id = ctx.guild.me.id)
                                webhook_avatar =member1.display_avatar
                                profile_webhook= await webhook_avatar.read()
                                webhooker=await channel_checker.create_webhook(name='AutoGif' , avatar=profile_webhook)
                                webhook_channel_set=discord.Object(self.channel_gif , type='abc.Snowflake')
                                await webhooker.edit(channel=webhook_channel_set)
                                collection.update_one({"server_id":ctx.guild_id} , {"$set":{"slot1_webhook":webhooker.id}}) 
                                   


                except:
                    await ctx.followup.send('enter your channel gif currectly')
                    self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                    self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                    self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)

                    return
                
                try :
                    self.count_gif = int(self.count_gif)
                    if self.count_gif > 5:
                        await ctx.followup.send('its more than 5!')
                        self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                        self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                        self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)

                        return
                except:
                    await ctx.followup.send('enter the number correctly')
                    self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                    self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                    self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)
                    return
                response , range_search = await self.picgenerator(self.subject_gif)
                if range_search -1 <=0:
                    await ctx.followup.send(f'there is no gif for this {self.subject_gif} subject')
                    self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                    self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                    self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)
                    return
                collection.update_one({"server_id":interaction.guild_id} , {"$set":{"slot1_subject":self.subject_gif, 'slot1_count':self.count_gif , "slot1_channel":self.channel_gif}})
                countgif = self.count_gif
                self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)

                try:
                    if range_search-1 > countgif:
                        list_temp = []
                        flag= True
                        counter = 1
                        while(flag):
                            selector = random.randint(0 , range_search-1)
                            if selector in list_temp:
                                continue

                            list_temp.append(selector)
                            if counter == 1:
                                await asyncio.sleep(2)
                            else:
                                await asyncio.sleep(5)
                            
                            try:
                                await webhooker.send(response['data'][selector]['url'])
                            except:
                                raise HTTPException(409 , 'exit webhook sending')
                            
                            if counter == countgif:
                                flag=False
                            counter +=1
                            
                except:
                    await interaction.followup.send('there is no gif for this item or there is a missing permission')
                

            except:
                self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)




        setting_form = discord.ui.Modal(title='GIF NUMBER 1 SETTINGS')
        setting_form.add_item(self.subject_gif)
        setting_form.add_item(self.channel_gif)
        setting_form.add_item(self.count_gif)
        setting_form.on_submit = on_sumbit
        await interaction.response.send_modal(setting_form)

    @ui.button(label='Subject 2' , custom_id='Subject_2' , style=discord.ButtonStyle.primary)
    async def subject2(self, interaction:discord.Interaction,_):

        if interaction.guild.me.top_role.position > interaction.user.top_role.position and interaction.user.id != interaction.guild.owner_id:
            return await interaction.response.send_message('your role is not above me then you cant use this button' , ephemeral=True)


        async def on_sumbit(ctx):
            webhooker = ''
            try:
                await ctx.response.defer()
                self.subject_gif= str(self.subject_gif)
                self.channel_gif = str(self.channel_gif)
                self.count_gif =str(self.count_gif) 
                if " " not in self.subject_gif:
                    self.subject_gif = self.subject_gif + ' ' + self.subject_gif

                try:
                    self.channel_gif = int(self.channel_gif)
                    channel_checker = discord.utils.get(ctx.guild.text_channels , id=self.channel_gif)
                    if channel_checker is not None:
                        if (find_webhook:=collection.find_one({"server_id":ctx.guild_id})):
                            webhook_id = find_webhook['slot2_webhook']
                            if webhook_id is not None:
                                webhooker = discord.utils.get(await ctx.guild.webhooks() , id = webhook_id)
                                if webhooker is not None:
                                    pass
                                else:
                                    member1 = discord.utils.get(ctx.guild.members , id = ctx.guild.me.id)
                                    webhook_avatar =member1.display_avatar
                                    profile_webhook= await webhook_avatar.read()
                                    webhooker=await channel_checker.create_webhook(name='AutoGif' , avatar=profile_webhook)
                                    webhook_channel_set=discord.Object(self.channel_gif , type='abc.Snowflake')
                                    await webhooker.edit(channel=webhook_channel_set)
                                    collection.update_one({"server_id":ctx.guild_id} , {"$set":{"slot2_webhook":webhooker.id}})  
                            else:
                                member1 = discord.utils.get(ctx.guild.members , id = ctx.guild.me.id)
                                webhook_avatar =member1.display_avatar
                                profile_webhook= await webhook_avatar.read()
                                webhooker=await channel_checker.create_webhook(name='AutoGif' , avatar=profile_webhook)
                                webhook_channel_set=discord.Object(self.channel_gif , type='abc.Snowflake')
                                await webhooker.edit(channel=webhook_channel_set)
                                collection.update_one({"server_id":ctx.guild_id} , {"$set":{"slot2_webhook":webhooker.id}}) 
                                  
                except:
                    await ctx.followup.send('enter your channel gif currectly')
                    self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                    self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                    self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)

                    return
                
                try :
                    self.count_gif = int(self.count_gif)
                    if self.count_gif > 5:
                        await ctx.followup.send('its more than 5!')
                        self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                        self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                        self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)
                        return
                except:
                    await ctx.followup.send('enter the number correctly')
                    self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                    self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                    self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)
                    return
                response , range_search = await self.picgenerator(self.subject_gif)
                if range_search -1 <=0:
                    await ctx.followup.send(f'there is no gif for this {self.subject_gif} subject')
                    self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                    self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                    self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)
                    return

                collection.update_one({"server_id":interaction.guild_id} , {"$set":{"slot2_subject":self.subject_gif, 'slot2_count':self.count_gif, "slot2_channel":self.channel_gif}})
                countgif = self.count_gif
                self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)

                try:
                    if range_search-1 > countgif:
                        list_temp = []
                        flag= True
                        counter = 1
                        while(flag):
                            selector = random.randint(0 , range_search-1)
                            if selector in list_temp:
                                continue

                            list_temp.append(selector)
                            if counter == 1:
                                await asyncio.sleep(2)
                            else:
                                await asyncio.sleep(5)
                            
                            try:
                                await webhooker.send(response['data'][selector]['url'])
                            except:
                                raise HTTPException(409 , 'exit webhook sending')
                            
                            if counter == countgif:
                                flag=False
                            counter +=1
                            
                except:
                    await interaction.followup.send('there is no gif for this item or there is a missing permission')


                
            except:
                self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)


        setting_form = discord.ui.Modal(title='GIF NUMBER 2 SETTINGS')
        setting_form.add_item(self.subject_gif)
        setting_form.add_item(self.channel_gif)
        setting_form.add_item(self.count_gif)
        setting_form.on_submit = on_sumbit
        await interaction.response.send_modal(setting_form)

    @ui.button(label='Subject 3' , custom_id='Subject_3' , style=discord.ButtonStyle.primary)
    async def subject3(self, interaction:discord.Interaction,_):

        if interaction.guild.me.top_role.position > interaction.user.top_role.position and interaction.user.id != interaction.guild.owner_id:
            return await interaction.response.send_message('your role is not above me then you cant use this button' , ephemeral=True)

        async def on_sumbit(ctx):
            webhooker = ''
            try:
                await ctx.response.defer()
                self.subject_gif= str(self.subject_gif)
                self.channel_gif = str(self.channel_gif)
                self.count_gif =str(self.count_gif) 
                if " " not in self.subject_gif:
                    self.subject_gif = self.subject_gif + ' ' + self.subject_gif

                try:
                    self.channel_gif = int(self.channel_gif)
                    channel_checker = discord.utils.get(ctx.guild.text_channels , id=self.channel_gif)
                    if channel_checker is not None:
                        if (find_webhook:=collection.find_one({"server_id":ctx.guild_id})):
                            webhook_id = find_webhook['slot3_webhook']
                            if webhook_id is not None:
                                webhooker = discord.utils.get(await ctx.guild.webhooks() , id = webhook_id)
                                if webhooker is not None:
                                    pass
                                else:
                                    member1 = discord.utils.get(ctx.guild.members , id = ctx.guild.me.id)
                                    webhook_avatar =member1.display_avatar
                                    profile_webhook= await webhook_avatar.read()
                                    webhooker=await channel_checker.create_webhook(name='AutoGif' , avatar=profile_webhook)
                                    webhook_channel_set=discord.Object(self.channel_gif , type='abc.Snowflake')
                                    await webhooker.edit(channel=webhook_channel_set)
                                    collection.update_one({"server_id":ctx.guild_id} , {"$set":{"slot3_webhook":webhooker.id}})  
                            else:
                                member1 = discord.utils.get(ctx.guild.members , id = ctx.guild.me.id)
                                webhook_avatar =member1.display_avatar
                                profile_webhook= await webhook_avatar.read()
                                webhooker=await channel_checker.create_webhook(name='AutoGif' , avatar=profile_webhook)
                                webhook_channel_set=discord.Object(self.channel_gif , type='abc.Snowflake')
                                await webhooker.edit(channel=webhook_channel_set)
                                collection.update_one({"server_id":ctx.guild_id} , {"$set":{"slot3_webhook":webhooker.id}}) 
                                  
                except:
                    await ctx.followup.send('enter your channel gif currectly')
                    self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                    self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                    self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)

                    return
                
                try :
                    self.count_gif = int(self.count_gif)
                    if self.count_gif > 5:
                        await ctx.followup.send('its more than 5!')
                        self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                        self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                        self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)

                        return
                except:
                    await ctx.followup.send('enter the number correctly')
                    self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                    self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                    self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)
                    return

                response , range_search = await self.picgenerator(self.subject_gif)
                if range_search -1 <=0:
                    await ctx.followup.send(f'there is no gif for this {self.subject_gif} subject')
                    self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                    self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                    self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)
                    return

                collection.update_one({"server_id":interaction.guild_id} , {"$set":{"slot3_subject":self.subject_gif, 'slot3_count':self.count_gif , "slot3_channel":self.channel_gif}})
                countgif = self.count_gif
                self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)

                try:
                    if range_search-1 > countgif:
                        list_temp = []
                        flag= True
                        counter = 1
                        while(flag):
                            selector = random.randint(0 , range_search-1)
                            if selector in list_temp:
                                continue

                            list_temp.append(selector)
                            if counter == 1:
                                await asyncio.sleep(2)
                            else:
                                await asyncio.sleep(5)
                            
                            try:
                                await webhooker.send(response['data'][selector]['url'])
                            except:
                                raise HTTPException(409 , 'exit webhook sending')
                            
                            if counter == countgif:
                                flag=False
                            counter +=1
                            
                except:
                    await interaction.followup.send('there is no gif for this item or there is a missing permission')

            except:
                self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)



        setting_form = discord.ui.Modal(title='GIF NUMBER 3 SETTINGS')
        setting_form.add_item(self.subject_gif)
        setting_form.add_item(self.channel_gif)
        setting_form.add_item(self.count_gif)
        setting_form.on_submit = on_sumbit
        await interaction.response.send_modal(setting_form)

    @ui.button(label='Subject 4' , custom_id='Subject_4' , style=discord.ButtonStyle.primary)
    async def subject4(self, interaction:discord.Interaction,_):

        if interaction.guild.me.top_role.position > interaction.user.top_role.position and interaction.user.id != interaction.guild.owner_id:
            return await interaction.response.send_message('your role is not above me then you cant use this button' , ephemeral=True)

    
        async def on_sumbit(ctx):
            webhooker = ''
            try:
                await ctx.response.defer()
                self.subject_gif= str(self.subject_gif)
                self.channel_gif = str(self.channel_gif)
                self.count_gif =str(self.count_gif) 
                if " " not in self.subject_gif:
                    self.subject_gif = self.subject_gif + ' ' + self.subject_gif

                try:
                    self.channel_gif = int(self.channel_gif)
                    channel_checker = discord.utils.get(ctx.guild.text_channels , id=self.channel_gif)
                    if channel_checker is not None:
                        if (find_webhook:=collection.find_one({"server_id":ctx.guild_id})):
                            webhook_id = find_webhook['slot4_webhook']
                            if webhook_id is not None:
                                webhooker = discord.utils.get(await ctx.guild.webhooks() , id = webhook_id)
                                if webhooker is not None:
                                    pass
                                else:
                                    member1 = discord.utils.get(ctx.guild.members , id = ctx.guild.me.id)
                                    webhook_avatar =member1.display_avatar
                                    profile_webhook= await webhook_avatar.read()
                                    webhooker=await channel_checker.create_webhook(name='AutoGif' , avatar=profile_webhook)
                                    webhook_channel_set=discord.Object(self.channel_gif , type='abc.Snowflake')
                                    await webhooker.edit(channel=webhook_channel_set)
                                    collection.update_one({"server_id":ctx.guild_id} , {"$set":{"slot4_webhook":webhooker.id}})  
                            else:
                                member1 = discord.utils.get(ctx.guild.members , id = ctx.guild.me.id)
                                webhook_avatar =member1.display_avatar
                                profile_webhook= await webhook_avatar.read()
                                webhooker=await channel_checker.create_webhook(name='AutoGif' , avatar=profile_webhook)
                                webhook_channel_set=discord.Object(self.channel_gif , type='abc.Snowflake')
                                await webhooker.edit(channel=webhook_channel_set)
                                collection.update_one({"server_id":ctx.guild_id} , {"$set":{"slot4_webhook":webhooker.id}}) 
                                  
                except:
                    await ctx.followup.send('enter your channel gif currectly')
                    self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                    self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                    self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)

                    return
                
                try :
                    self.count_gif = int(self.count_gif)
                    if self.count_gif > 5:
                        await ctx.followup.send('its more than 5!')
                        self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                        self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                        self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)

                        return
                except:
                    await ctx.followup.send('enter the number correctly')
                    self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                    self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                    self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)
                    return
                response , range_search = await self.picgenerator(self.subject_gif)
                if range_search -1 <=0:
                    await ctx.followup.send(f'there is no gif for this {self.subject_gif} subject')
                    self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                    self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                    self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)
                    return

                collection.update_one({"server_id":interaction.guild_id} , {"$set":{"slot4_subject":self.subject_gif, 'slot4_count':self.count_gif , "slot4_channel":self.channel_gif}})
                countgif = self.count_gif
                self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)

                try:
                    if range_search-1 > countgif:
                        list_temp = []
                        flag= True
                        counter = 1
                        while(flag):
                            selector = random.randint(0 , range_search-1)
                            if selector in list_temp:
                                continue

                            list_temp.append(selector)
                            if counter == 1:
                                await asyncio.sleep(2)
                            else:
                                await asyncio.sleep(5)
                            
                            try:
                                await webhooker.send(response['data'][selector]['url'])
                            except:
                                raise HTTPException(409 , 'exit webhook sending')
                            
                            if counter == countgif:
                                flag=False
                            counter +=1
                            
                except:
                    await interaction.followup.send('there is no gif for this item or there is a missing permission')

            except:
                self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)


        setting_form = discord.ui.Modal(title='GIF NUMBER 4 SETTINGS')
        setting_form.add_item(self.subject_gif)
        setting_form.add_item(self.channel_gif)
        setting_form.add_item(self.count_gif)
        setting_form.on_submit = on_sumbit
        await interaction.response.send_modal(setting_form)

    @ui.button(label='Subject 5' , custom_id='Subject_5' , style=discord.ButtonStyle.primary)
    async def subject5(self, interaction:discord.Interaction,_):

        if interaction.guild.me.top_role.position > interaction.user.top_role.position and interaction.user.id != interaction.guild.owner_id:
            return await interaction.response.send_message('your role is not above me then you cant use this button' , ephemeral=True)

        async def on_sumbit(ctx):
            webhooker = ''
            try:
                await ctx.response.defer()
                self.subject_gif= str(self.subject_gif)
                self.channel_gif = str(self.channel_gif)
                self.count_gif =str(self.count_gif) 
                if " " not in self.subject_gif:
                    self.subject_gif = self.subject_gif + ' ' + self.subject_gif

                try:
                    self.channel_gif = int(self.channel_gif)
                    channel_checker = discord.utils.get(ctx.guild.text_channels , id=self.channel_gif)
                    if channel_checker is not None:
                        if (find_webhook:=collection.find_one({"server_id":ctx.guild_id})):
                            webhook_id = find_webhook['slot5_webhook']
                            if webhook_id is not None:
                                webhooker = discord.utils.get(await ctx.guild.webhooks() , id = webhook_id)
                                if webhooker is not None:
                                    pass
                                else:
                                    member1 = discord.utils.get(ctx.guild.members , id = ctx.guild.me.id)
                                    webhook_avatar =member1.display_avatar
                                    profile_webhook= await webhook_avatar.read()
                                    webhooker=await channel_checker.create_webhook(name='AutoGif' , avatar=profile_webhook)
                                    webhook_channel_set=discord.Object(self.channel_gif , type='abc.Snowflake')
                                    await webhooker.edit(channel=webhook_channel_set)
                                    collection.update_one({"server_id":ctx.guild_id} , {"$set":{"slot5_webhook":webhooker.id}})   

                            else:
                                member1 = discord.utils.get(ctx.guild.members , id = ctx.guild.me.id)
                                webhook_avatar =member1.display_avatar
                                profile_webhook= await webhook_avatar.read()
                                webhooker=await channel_checker.create_webhook(name='AutoGif' , avatar=profile_webhook)
                                webhook_channel_set=discord.Object(self.channel_gif , type='abc.Snowflake')
                                await webhooker.edit(channel=webhook_channel_set)
                                collection.update_one({"server_id":ctx.guild_id} , {"$set":{"slot5_webhook":webhooker.id}}) 

                except:
                    await ctx.followup.send('enter your channel gif currectly')
                    self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                    self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                    self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)
                    return
                
                try :
                    self.count_gif = int(self.count_gif)
                    if self.count_gif > 5:
                        await ctx.followup.send('its more than 5!')
                        self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                        self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                        self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)

                        return
                except:
                    await ctx.followup.send('enter the number correctly')
                    self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                    self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                    self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)
                    return
                response , range_search = await self.picgenerator(self.subject_gif)
                if range_search -1 <=0:
                    await ctx.followup.send(f'there is no gif for this {self.subject_gif} subject')
                    self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                    self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                    self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)
                    return

                collection.update_one({"server_id":interaction.guild_id} , {"$set":{"slot5_subject":self.subject_gif, 'slot5_count':self.count_gif , "slot5_channel":self.channel_gif}})
                countgif = self.count_gif
                self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)


                try:
                    if range_search-1 > countgif:
                        list_temp = []
                        flag= True
                        counter = 1
                        while(flag):
                            selector = random.randint(0 , range_search-1)
                            if selector in list_temp:
                                continue

                            list_temp.append(selector)
                            if counter == 1:
                                await asyncio.sleep(2)
                            else:
                                await asyncio.sleep(5)
                            
                            try:
                                await webhooker.send(response['data'][selector]['url'])
                            except:
                                raise HTTPException(409 , 'exit webhook sending')
                            
                            if counter == countgif:
                                flag=False
                            counter +=1
                            
                except:
                    await interaction.followup.send('there is no gif for this item or there is a missing permission')


            except:
                self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)


        setting_form = discord.ui.Modal(title='GIF NUMBER 5 SETTINGS')
        setting_form.add_item(self.subject_gif)
        setting_form.add_item(self.channel_gif)
        setting_form.add_item(self.count_gif)
        setting_form.on_submit = on_sumbit
        await interaction.response.send_modal(setting_form)

    @ui.button(label='Subject 6' , custom_id='Subject_6' , style=discord.ButtonStyle.primary)
    async def subject6(self, interaction:discord.Interaction,_):

        if interaction.guild.me.top_role.position > interaction.user.top_role.position and interaction.user.id != interaction.guild.owner_id:
            return await interaction.response.send_message('your role is not above me then you cant use this button' , ephemeral=True)

        async def on_sumbit(ctx):
            webhooker = ''
            try:
                await ctx.response.defer()
                self.subject_gif= str(self.subject_gif)
                self.channel_gif = str(self.channel_gif)
                self.count_gif =str(self.count_gif) 
                if " " not in self.subject_gif:
                    self.subject_gif = self.subject_gif + ' ' + self.subject_gif

                try:
                    self.channel_gif = int(self.channel_gif)
                    channel_checker = discord.utils.get(ctx.guild.text_channels , id=self.channel_gif)
                    if channel_checker is not None:
                        if (find_webhook:=collection.find_one({"server_id":ctx.guild_id})):
                            webhook_id = find_webhook['slot6_webhook']
                            if webhook_id is not None:
                                webhooker = discord.utils.get(await ctx.guild.webhooks() , id = webhook_id)
                                if webhooker is not None:
                                    pass
                                else:
                                    member1 = discord.utils.get(ctx.guild.members , id = ctx.guild.me.id)
                                    webhook_avatar =member1.display_avatar
                                    profile_webhook= await webhook_avatar.read()
                                    webhooker=await channel_checker.create_webhook(name='AutoGif' , avatar=profile_webhook)
                                    webhook_channel_set=discord.Object(self.channel_gif , type='abc.Snowflake')
                                    await webhooker.edit(channel=webhook_channel_set)
                                    collection.update_one({"server_id":ctx.guild_id} , {"$set":{"slot6_webhook":webhooker.id}})
                            else:
                                member1 = discord.utils.get(ctx.guild.members , id = ctx.guild.me.id)
                                webhook_avatar =member1.display_avatar
                                profile_webhook= await webhook_avatar.read()
                                webhooker=await channel_checker.create_webhook(name='AutoGif' , avatar=profile_webhook)
                                webhook_channel_set=discord.Object(self.channel_gif , type='abc.Snowflake')
                                await webhooker.edit(channel=webhook_channel_set)
                                collection.update_one({"server_id":ctx.guild_id} , {"$set":{"slot6_webhook":webhooker.id}}) 
                                    
                except:
                    await ctx.followup.send('enter your channel gif currectly')
                    self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                    self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                    self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)

                    return
                
                try :
                    self.count_gif = int(self.count_gif)
                    if self.count_gif > 5:
                        await ctx.followup.send('its more than 5!')
                        self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                        self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                        self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)

                        return
                except:
                    await ctx.followup.send('enter the number correctly')
                    self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                    self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                    self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)
                    return
                response , range_search = await self.picgenerator(self.subject_gif)
                if range_search -1 <=0:
                    await ctx.followup.send(f'there is no gif for this {self.subject_gif} subject')
                    self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                    self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                    self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)
                    return

                collection.update_one({"server_id":interaction.guild_id} , {"$set":{"slot6_subject":self.subject_gif, 'slot6_count':self.count_gif , "slot6_channel":self.channel_gif}})
                countgif = self.count_gif
                self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)

                try:
                    if range_search-1 > countgif:
                        list_temp = []
                        flag= True
                        counter = 1
                        while(flag):
                            selector = random.randint(0 , range_search-1)
                            if selector in list_temp:
                                continue

                            list_temp.append(selector)
                            if counter == 1:
                                await asyncio.sleep(2)
                            else:
                                await asyncio.sleep(5)
                            
                            try:
                                await webhooker.send(response['data'][selector]['url'])
                            except:
                                raise HTTPException(409 , 'exit webhook sending')
                            
                            if counter == countgif:
                                flag=False
                            counter +=1
                            
                except:
                    await interaction.followup.send('there is no gif for this item or there is a missing permission')

            except:
                self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)


        setting_form = discord.ui.Modal(title='GIF NUMBER 6 SETTINGS')
        setting_form.add_item(self.subject_gif)
        setting_form.add_item(self.channel_gif)
        setting_form.add_item(self.count_gif)
        setting_form.on_submit = on_sumbit
        await interaction.response.send_modal(setting_form)


    @ui.button(label='Subject 7' , custom_id='Subject_7' , style=discord.ButtonStyle.primary)
    async def subject7(self, interaction:discord.Interaction,_):
        if interaction.guild.me.top_role.position > interaction.user.top_role.position and interaction.user.id != interaction.guild.owner_id:
            return await interaction.response.send_message('your role is not above me then you cant use this button' , ephemeral=True)
    

        async def on_sumbit(ctx):
            webhooker = ''
            try:
                await ctx.response.defer()
                self.subject_gif= str(self.subject_gif)
                self.channel_gif = str(self.channel_gif)
                self.count_gif =str(self.count_gif) 
                if " " not in self.subject_gif:
                    self.subject_gif = self.subject_gif + ' ' + self.subject_gif

                try:
                    self.channel_gif = int(self.channel_gif)
                    channel_checker = discord.utils.get(ctx.guild.text_channels , id=self.channel_gif)
                    if channel_checker is not None:
                        if (find_webhook:=collection.find_one({"server_id":ctx.guild_id})):
                            webhook_id = find_webhook['slot7_webhook']
                            if webhook_id is not None:
                                webhooker = discord.utils.get(await ctx.guild.webhooks() , id = webhook_id)
                                if webhooker is not None:
                                    pass
                                else:
                                    member1 = discord.utils.get(ctx.guild.members , id = ctx.guild.me.id)
                                    webhook_avatar =member1.display_avatar
                                    profile_webhook= await webhook_avatar.read()
                                    webhooker=await channel_checker.create_webhook(name='AutoGif' , avatar=profile_webhook)
                                    webhook_channel_set=discord.Object(self.channel_gif , type='abc.Snowflake')
                                    await webhooker.edit(channel=webhook_channel_set)
                                    collection.update_one({"server_id":ctx.guild_id} , {"$set":{"slot7_webhook":webhooker.id}}) 
                            else:
                                member1 = discord.utils.get(ctx.guild.members , id = ctx.guild.me.id)
                                webhook_avatar =member1.display_avatar
                                profile_webhook= await webhook_avatar.read()
                                webhooker=await channel_checker.create_webhook(name='AutoGif' , avatar=profile_webhook)
                                webhook_channel_set=discord.Object(self.channel_gif , type='abc.Snowflake')
                                await webhooker.edit(channel=webhook_channel_set)
                                collection.update_one({"server_id":ctx.guild_id} , {"$set":{"slot7_webhook":webhooker.id}}) 
                                   
                except:
                    await ctx.followup.send('enter your channel gif currectly')
                    self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                    self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                    self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)

                    return
                
                try :
                    self.count_gif = int(self.count_gif)
                    if self.count_gif > 5:
                        await ctx.followup.send('its more than 5!')
                        self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                        self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                        self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)

                        return
                except:
                    await ctx.followup.send('enter the number correctly')
                    self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                    self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                    self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)
                    return

                response , range_search = await self.picgenerator(self.subject_gif)
                if range_search -1 <=0:
                    await ctx.followup.send(f'there is no gif for this {self.subject_gif} subject')
                    self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                    self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                    self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)
                    return

                collection.update_one({"server_id":interaction.guild_id} , {"$set":{"slot7_subject":self.subject_gif, 'slot7_count':self.count_gif , "slot7_channel":self.channel_gif}})
                countgif = self.count_gif
                self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)
                
                try:
                    if range_search-1 > countgif:
                        list_temp = []
                        flag= True
                        counter = 1
                        while(flag):
                            selector = random.randint(0 , range_search-1)
                            if selector in list_temp:
                                continue

                            list_temp.append(selector)
                            if counter == 1:
                                await asyncio.sleep(2)
                            else:
                                await asyncio.sleep(5)
                            
                            try:
                                await webhooker.send(response['data'][selector]['url'])
                            except:
                                raise HTTPException(409 , 'exit webhook sending')
                            
                            if counter == countgif:
                                flag=False
                            counter +=1
                except:
                    await interaction.followup.send('there is no gif for this item or there is a missing permission')

            except:
                self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)


        setting_form = discord.ui.Modal(title='GIF NUMBER 7 SETTINGS')
        setting_form.add_item(self.subject_gif)
        setting_form.add_item(self.channel_gif)
        setting_form.add_item(self.count_gif)
        setting_form.on_submit = on_sumbit
        await interaction.response.send_modal(setting_form)

    @ui.button(label='Subject 8' , custom_id='Subject_8' , style=discord.ButtonStyle.primary)
    async def subject8(self, interaction:discord.Interaction,_):
        if interaction.guild.me.top_role.position > interaction.user.top_role.position and interaction.user.id != interaction.guild.owner_id:
            return await interaction.response.send_message('your role is not above me then you cant use this button' , ephemeral=True)

        async def on_sumbit(ctx):
            webhooker = ''
            try:
                await ctx.response.defer()
                self.subject_gif= str(self.subject_gif)
                self.channel_gif = str(self.channel_gif)
                self.count_gif =str(self.count_gif) 
                if " " not in self.subject_gif:
                    self.subject_gif = self.subject_gif + ' ' + self.subject_gif

                try:
                    self.channel_gif = int(self.channel_gif)
                    channel_checker = discord.utils.get(ctx.guild.text_channels , id=self.channel_gif)
                    if channel_checker is not None:
                        if (find_webhook:=collection.find_one({"server_id":ctx.guild_id})):
                            webhook_id = find_webhook['slot8_webhook']
                            if webhook_id is not None:
                                webhooker = discord.utils.get(await ctx.guild.webhooks() , id = webhook_id)
                                if webhooker is not None:
                                    pass
                                else:
                                    member1 = discord.utils.get(ctx.guild.members , id = ctx.guild.me.id)
                                    webhook_avatar =member1.display_avatar
                                    profile_webhook= await webhook_avatar.read()
                                    webhooker=await channel_checker.create_webhook(name='AutoGif' , avatar=profile_webhook)
                                    webhook_channel_set=discord.Object(self.channel_gif , type='abc.Snowflake')
                                    await webhooker.edit(channel=webhook_channel_set)
                                    collection.update_one({"server_id":ctx.guild_id} , {"$set":{"slot8_webhook":webhooker.id}})   

                            else:
                                member1 = discord.utils.get(ctx.guild.members , id = ctx.guild.me.id)
                                webhook_avatar =member1.display_avatar
                                profile_webhook= await webhook_avatar.read()
                                webhooker=await channel_checker.create_webhook(name='AutoGif' , avatar=profile_webhook)
                                webhook_channel_set=discord.Object(self.channel_gif , type='abc.Snowflake')
                                await webhooker.edit(channel=webhook_channel_set)
                                collection.update_one({"server_id":ctx.guild_id} , {"$set":{"slot8_webhook":webhooker.id}}) 

                except:
                    await ctx.followup.send('enter your channel gif currectly')
                    return
                
                try :
                    self.count_gif = int(self.count_gif)
                    if self.count_gif > 5:
                        await ctx.followup.send('its more than 5!')
                        self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                        self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                        self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)
                        return
                except:
                    await ctx.followup.send('enter the number correctly')
                    self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                    self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                    self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)
                    return
                response , range_search = await self.picgenerator(self.subject_gif)
                if range_search -1 <=0:
                    await ctx.followup.send(f'there is no gif for this {self.subject_gif} subject')
                    self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                    self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                    self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)
                    return

                collection.update_one({"server_id":interaction.guild_id} , {"$set":{"slot8_subject":self.subject_gif , 'slot8_count':self.count_gif, "slot8_channel":self.channel_gif}})
                countgif = self.count_gif
                self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)

                try:
                    if range_search-1 > countgif:
                        list_temp = []
                        flag= True
                        counter = 1
                        while(flag):
                            selector = random.randint(0 , range_search-1)
                            if selector in list_temp:
                                continue

                            list_temp.append(selector)
                            if counter == 1:
                                await asyncio.sleep(2)
                            else:
                                await asyncio.sleep(5)
                            
                            try:
                                await webhooker.send(response['data'][selector]['url'])
                            except:
                                raise HTTPException(409 , 'exit webhook sending')
                            
                            if counter == countgif:
                                flag=False
                            counter +=1
                except:
                    await interaction.followup.send('there is no gif for this item or there is a missing permission')


            except:
                self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)


        setting_form = discord.ui.Modal(title='GIF NUMBER 8 SETTINGS')
        setting_form.add_item(self.subject_gif)
        setting_form.add_item(self.channel_gif)
        setting_form.add_item(self.count_gif)
        setting_form.on_submit = on_sumbit
        await interaction.response.send_modal(setting_form)

    @ui.button(label='Subject 9' , custom_id='Subject_9' , style=discord.ButtonStyle.primary)
    async def subject9(self, interaction:discord.Interaction,_):
        
        if interaction.guild.me.top_role.position > interaction.user.top_role.position and interaction.user.id != interaction.guild.owner_id:
            return await interaction.response.send_message('your role is not above me then you cant use this button' , ephemeral=True)

        async def on_sumbit(ctx):
            webhooker = ''
            try:
                await ctx.response.defer()
                self.subject_gif= str(self.subject_gif)
                self.channel_gif = str(self.channel_gif)
                self.count_gif =str(self.count_gif) 
                if " " not in self.subject_gif:
                    self.subject_gif = self.subject_gif + ' ' + self.subject_gif

                try:
                    self.channel_gif = int(self.channel_gif)
                    channel_checker = discord.utils.get(ctx.guild.text_channels , id=self.channel_gif)
                    if channel_checker is not None:
                        if (find_webhook:=collection.find_one({"server_id":ctx.guild_id})):
                            webhook_id = find_webhook['slot9_webhook']
                            if webhook_id is not None:
                                webhooker = discord.utils.get(await ctx.guild.webhooks() , id = webhook_id)
                                if webhooker is not None:
                                    pass
                                else:
                                    member1 = discord.utils.get(ctx.guild.members , id = ctx.guild.me.id)
                                    webhook_avatar =member1.display_avatar
                                    profile_webhook= await webhook_avatar.read()
                                    webhooker=await channel_checker.create_webhook(name='AutoGif' , avatar=profile_webhook)
                                    webhook_channel_set=discord.Object(self.channel_gif , type='abc.Snowflake')
                                    await webhooker.edit(channel=webhook_channel_set)
                                    collection.update_one({"server_id":ctx.guild_id} , {"$set":{"slot9_webhook":webhooker.id}})
                            else:
                                member1 = discord.utils.get(ctx.guild.members , id = ctx.guild.me.id)
                                webhook_avatar =member1.display_avatar
                                profile_webhook= await webhook_avatar.read()
                                webhooker=await channel_checker.create_webhook(name='AutoGif' , avatar=profile_webhook)
                                webhook_channel_set=discord.Object(self.channel_gif , type='abc.Snowflake')
                                await webhooker.edit(channel=webhook_channel_set)
                                collection.update_one({"server_id":ctx.guild_id} , {"$set":{"slot9_webhook":webhooker.id}}) 
                                  
                except:
                    await ctx.followup.send('enter your channel gif currectly')
                    self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                    self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                    self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)

                    return
                
                try :
                    self.count_gif = int(self.count_gif)
                    if self.count_gif > 5:
                        await ctx.followup.send('its more than 5!')
                        self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                        self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                        self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)

                        return
                except:
                    await ctx.followup.send('enter the number correctly')
                    self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                    self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                    self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)
                    return
                response , range_search = await self.picgenerator(self.subject_gif)
                if range_search -1 <=0:
                    await ctx.followup.send(f'there is no gif for this {self.subject_gif} subject')
                    self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                    self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                    self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)
                    return

                collection.update_one({"server_id":interaction.guild_id} , {"$set":{"slot9_subject":self.subject_gif , 'slot9_count':self.count_gif, "slot9_channel":self.channel_gif}})
                countgif = self.count_gif
                self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)
                
                try:
                    if range_search-1 > countgif:
                        list_temp = []
                        flag= True
                        counter = 1
                        while(flag):
                            selector = random.randint(0 , range_search-1)
                            if selector in list_temp:
                                continue

                            list_temp.append(selector)
                            if counter == 1:
                                await asyncio.sleep(2)
                            else:
                                await asyncio.sleep(5)
                            
                            try:
                                await webhooker.send(response['data'][selector]['url'])
                            except:
                                raise HTTPException(409 , 'exit webhook sending')
                            
                            if counter == countgif:
                                flag=False
                            counter +=1
                except:
                    await interaction.followup.send('there is no gif for this item or there is a missing permission')


            except:
                self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)


        # self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
        # self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
        # self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)
        setting_form = discord.ui.Modal(title='GIF NUMBER 9 SETTINGS')
        setting_form.add_item(self.subject_gif)
        setting_form.add_item(self.channel_gif)
        setting_form.add_item(self.count_gif)
        setting_form.on_submit = on_sumbit
        await interaction.response.send_modal(setting_form)

    @ui.button(label='Subject 10' , custom_id='Subject_10' , style=discord.ButtonStyle.primary)
    async def subject10(self, interaction:discord.Interaction,_):
        if interaction.guild.me.top_role.position > interaction.user.top_role.position and interaction.user.id != interaction.guild.owner_id:
            return await interaction.response.send_message('your role is not above me then you cant use this button' , ephemeral=True)
        async def on_sumbit(ctx):
            webhooker = ''
            try:
                await ctx.response.defer()
                self.subject_gif= str(self.subject_gif)
                self.channel_gif = str(self.channel_gif)
                self.count_gif =str(self.count_gif) 
                if " " not in self.subject_gif:
                    self.subject_gif = self.subject_gif + ' ' + self.subject_gif
                try:
                    self.channel_gif = int(self.channel_gif)
                    channel_checker = discord.utils.get(ctx.guild.text_channels , id=self.channel_gif)
                    if channel_checker is not None:
                        if (find_webhook:=collection.find_one({"server_id":ctx.guild_id})):
                            webhook_id = find_webhook['slot10_webhook']
                            if webhook_id is not None:
                                webhooker = discord.utils.get(await ctx.guild.webhooks() , id = webhook_id)
                                if webhooker is not None:
                                    pass
                                else:
                                    member1 = discord.utils.get(ctx.guild.members , id = ctx.guild.me.id)
                                    webhook_avatar =member1.display_avatar
                                    profile_webhook= await webhook_avatar.read()
                                    webhooker=await channel_checker.create_webhook(name='AutoGif' , avatar=profile_webhook)
                                    webhook_channel_set=discord.Object(self.channel_gif , type='abc.Snowflake')
                                    await webhooker.edit(channel=webhook_channel_set)
                                    collection.update_one({"server_id":ctx.guild_id} , {"$set":{"slot10_webhook":webhooker.id}}) 
                            else:
                                member1 = discord.utils.get(ctx.guild.members , id = ctx.guild.me.id)
                                webhook_avatar =member1.display_avatar
                                profile_webhook= await webhook_avatar.read()
                                webhooker=await channel_checker.create_webhook(name='AutoGif' , avatar=profile_webhook)
                                webhook_channel_set=discord.Object(self.channel_gif , type='abc.Snowflake')
                                await webhooker.edit(channel=webhook_channel_set)
                                collection.update_one({"server_id":ctx.guild_id} , {"$set":{"slot10_webhook":webhooker.id}}) 
                            
                except:
                    await ctx.followup.send('enter your channel gif currectly')
                    self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                    self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                    self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)

                    return
                
                try :
                    self.count_gif = int(self.count_gif)
                    if self.count_gif > 5:
                        await ctx.followup.send('its more than 5!')
                        self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                        self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                        self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)

                        return
                except:
                    await ctx.followup.send('enter the number correctly')
                    self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                    self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                    self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)
                    return
                response , range_search = await self.picgenerator(self.subject_gif)
                if range_search -1 <=0:
                    await ctx.followup.send(f'there is no gif for this {self.subject_gif} subject')
                    self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                    self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                    self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)
                    return

                collection.update_one({"server_id":interaction.guild_id} , {"$set":{"slot10_subject":self.subject_gif, 'slot10_count':self.count_gif , "slot10_channel":self.channel_gif}})
                countgif = self.count_gif
                self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)

                try:
                    if range_search-1 > countgif:
                        list_temp = []
                        flag= True
                        counter = 1
                        while(flag):
                            selector = random.randint(0 , range_search-1)
                            if selector in list_temp:
                                continue

                            list_temp.append(selector)
                            if counter == 1:
                                await asyncio.sleep(2)
                            else:
                                await asyncio.sleep(5)
                            
                            try:
                                await webhooker.send(response['data'][selector]['url'])
                            except:
                                raise HTTPException(409 , 'exit webhook sending')
                            
                            if counter == countgif:
                                flag=False
                            counter +=1
                except:
                    await interaction.followup.send('there is no gif for this item or there is a missing permission')
                self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)

            except:
                self.subject_gif = discord.ui.TextInput(label='enter your gif subject:' , style=discord.TextStyle.short , required=True)
                self.channel_gif = discord.ui.TextInput(label='enter your channel id:' , style=discord.TextStyle.short, required=True)
                self.count_gif = discord.ui.TextInput(label='enter count of gifs (maximum 5):' , style=discord.TextStyle.short, required=True)

        setting_form = discord.ui.Modal(title='GIF NUMBER 10 SETTINGS')
        setting_form.add_item(self.subject_gif)
        setting_form.add_item(self.channel_gif)
        setting_form.add_item(self.count_gif)
        setting_form.on_submit = on_sumbit
        await interaction.response.send_modal(setting_form)

    @ui.button(label='Delete Settings' , custom_id='Subject_11' , style=discord.ButtonStyle.red)
    async def subject11(self, interaction:discord.Interaction,_):
        if interaction.guild.me.top_role.position > interaction.user.top_role.position and interaction.user.id != interaction.guild.owner_id:
            return await interaction.response.send_message('your role is not above me then you cant use this button' , ephemeral=True)
        
        async def submit1(ctx):
            collection.update_one({"server_id":ctx.guild_id} , {"$set":{"slot1_subject":None, 'slot1_count':None , "slot1_channel":None , 'slot1_webhook':None}})
            await ctx.response.send_message('subject 1 settings deleted' , ephemeral=True)
        async def submit2(ctx):
            collection.update_one({"server_id":ctx.guild_id} , {"$set":{"slot2_subject":None, 'slot2_count':None , "slot2_channel":None , 'slot2_webhook':None}})
            await ctx.response.send_message('subject 2 settings deleted' , ephemeral=True)
        async def submit3(ctx):
            collection.update_one({"server_id":ctx.guild_id} , {"$set":{"slot3_subject":None, 'slot3_count':None , "slot3_channel":None , 'slot3_webhook':None}})
            await ctx.response.send_message('subject 3 settings deleted' , ephemeral=True)
        async def submit4(ctx):
            collection.update_one({"server_id":ctx.guild_id} , {"$set":{"slot4_subject":None, 'slot4_count':None , "slot4_channel":None , 'slot4_webhook':None}})
            await ctx.response.send_message('subject 4 settings deleted' , ephemeral=True)
        async def submit5(ctx):
            collection.update_one({"server_id":ctx.guild_id} , {"$set":{"slot5_subject":None, 'slot5_count':None , "slot5_channel":None , 'slot5_webhook':None}})
            await ctx.response.send_message('subject 5 settings deleted' , ephemeral=True)
        async def submit6(ctx):
            collection.update_one({"server_id":ctx.guild_id} , {"$set":{"slot6_subject":None, 'slot6_count':None , "slot6_channel":None , 'slot6_webhook':None}})
            await ctx.response.send_message('subject 6 settings deleted' , ephemeral=True)
        async def submit7(ctx):
            collection.update_one({"server_id":ctx.guild_id} , {"$set":{"slot7_subject":None, 'slot7_count':None , "slot7_channel":None , 'slot7_webhook':None}})
            await ctx.response.send_message('subject 7 settings deleted' , ephemeral=True)
        async def submit8(ctx):
            collection.update_one({"server_id":ctx.guild_id} , {"$set":{"slot8_subject":None, 'slot8_count':None , "slot8_channel":None , 'slot8_webhook':None}})
            await ctx.response.send_message('subject 8 settings deleted' , ephemeral=True)
        async def submit9(ctx):
            collection.update_one({"server_id":ctx.guild_id} , {"$set":{"slot9_subject":None, 'slot9_count':None , "slot9_channel":None , 'slot9_webhook':None}})
            await ctx.response.send_message('subject 9 settings deleted' , ephemeral=True)
        async def submit10(ctx):
            collection.update_one({"server_id":ctx.guild_id} , {"$set":{"slot10_subject":None, 'slot10_count':None , "slot10_channel":None , 'slot10_webhook':None}})
            await ctx.response.send_message('subject 10 settings deleted' , ephemeral=True)

        but1=discord.ui.Button(label='Subject1' , style=discord.ButtonStyle.red , custom_id='subject1_delete')
        but2=discord.ui.Button(label='Subject2' , style=discord.ButtonStyle.red , custom_id='subject2_delete')
        but3=discord.ui.Button(label='Subject3' , style=discord.ButtonStyle.red , custom_id='subject3_delete')
        but4=discord.ui.Button(label='Subject4' , style=discord.ButtonStyle.red , custom_id='subject4_delete')
        but5=discord.ui.Button(label='Subject5' , style=discord.ButtonStyle.red , custom_id='subject5_delete')
        but6=discord.ui.Button(label='Subject6' , style=discord.ButtonStyle.red , custom_id='subject6_delete')
        but7=discord.ui.Button(label='Subject7' , style=discord.ButtonStyle.red , custom_id='subject7_delete')
        but8=discord.ui.Button(label='Subject8' , style=discord.ButtonStyle.red , custom_id='subject8_delete')
        but9=discord.ui.Button(label='Subject9' , style=discord.ButtonStyle.red , custom_id='subject9_delete')
        but10=discord.ui.Button(label='Subject10' , style=discord.ButtonStyle.red , custom_id='subject10_delete')

        but1.callback=submit1
        but2.callback=submit2
        but3.callback=submit3
        but4.callback=submit4
        but5.callback=submit5
        but6.callback=submit6
        but7.callback=submit7
        but8.callback=submit8
        but9.callback=submit9
        but10.callback=submit10


        butt_adder = discord.ui.View(timeout=None)
        butt_adder.add_item(but1)
        butt_adder.add_item(but2)
        butt_adder.add_item(but3)
        butt_adder.add_item(but4)
        butt_adder.add_item(but5)
        butt_adder.add_item(but6)
        butt_adder.add_item(but7)
        butt_adder.add_item(but8)
        butt_adder.add_item(but9)
        butt_adder.add_item(but10)

        embed=discord.Embed(
        title=f"DELETE SETTINGS",
        description= f"Select each subject you wants to delete the configuration",
        timestamp=datetime.now(),
        color= 0xF6F6F6
        )


        await interaction.response.send_message(view=butt_adder , ephemeral=True)



class Gif(Plugin):
    def __init__(self , bot:Bot):
        self.bot = bot
    
    async def cog_load(self):
        await super().cog_load()
        self.bot.add_view(AutoGifGen(self.bot))
        
    async def get_not_found_embed(self,interaction):
        embed=discord.Embed(title='ERROR',description =f'{interaction.user.mention},I COULDNT FIND ANYTHING')  
        return embed   

    async def userpic(self , subject , msg , interaction):
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
            elif response.status_code == 451:
                embeder = await self.get_not_found_embed(interaction)
                await msg.edit(embed=embeder)
                raise HTTPException(409 , "error happend")

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
            elif response.status_code == 459:
                embeder = await self.get_not_found_embed(interaction)
                await msg.edit(embed=embeder)
                raise HTTPException(409 , "error happend")
            else:
                raise HTTPException(409 , "error happend")
        filter1 = response.json()
        range_search = filter1['pagination']['count']


        return response.json() , range_search


    @commands.Cog.listener() #join to sv jadid
    async def on_guild_join(self,guild):
        try:
            flag=False
            if (find:= new_GUILD.find_one({"owner":guild.owner_id})):
                general = guild.text_channels
                if general is not None:
                    for i in general:
                        if i.permissions_for(guild.me).send_messages:
                            embed=discord.Embed(
                            title=f"AUTOGIF BOT",
                            description= f"🤖thanks for inviting me\n\n🌀 The Best Auto Gif Sender With Full Customization\n\n🟢 use </gifgenerate:1198772375299313868> To Receive Your Ideal Gif\n\n🛠 use </autogif:1198772375299313867> To Open Easy Setup\n\n📌make sure to join our support server:\n\nhttps://discord.gg/T7YAhZEDqz",
                            timestamp=datetime.now(),
                            color= 0xF6F6F6
                            )
                            embed.set_footer(text='Developed by APA team with ❤' , icon_url=None)
                            embed.set_image(url='https://media.discordapp.net/attachments/1198003052213448839/1198987152063725568/g0R9.gif?ex=65c0e6cd&is=65ae71cd&hm=8e178256e13db762528044c34c7e2178cb99c0cf4884eb521a31d96f1c45d553&=&width=575&height=575')
                            await i.send(embed=embed)
                            await guild.leave()
                            break
            else:
                new_GUILD.insert_one({'_id':guild.id ,'owner':guild.owner_id , 'server':guild.id ,'key':True})
                general = guild.text_channels
                if general is not None:
                    for i in general:
                        if i.permissions_for(guild.me).send_messages:
                            embed=discord.Embed(
                            title=f"AUTOGIF BOT",
                            description= f"🤖thanks for inviting me\n\n🌀 The Best Auto Gif Sender With Full Customization\n\n🟢 use </gifgenerate:1198772375299313868> To Receive Your Ideal Gif\n\n🛠 use </autogif:1198772375299313867> To Open Easy Setup\n\n📌make sure to join our support server:\n\nhttps://discord.gg/T7YAhZEDqz",
                            timestamp=datetime.now(),
                            color= 0xF6F6F6
                            )
                            embed.set_footer(text='Developed by APA team with ❤' , icon_url=None)
                            embed.set_image(url='https://media.discordapp.net/attachments/1198003052213448839/1198987152063725568/g0R9.gif?ex=65c0e6cd&is=65ae71cd&hm=8e178256e13db762528044c34c7e2178cb99c0cf4884eb521a31d96f1c45d553&=&width=575&height=575')
                            await i.send(embed=embed)
                            flag=True
                            break
            
            if flag==True:
                if (find1:= new_GUILD.find_one({"_id":1})):
                    counter = find1['count_guilds']
                    counter+=1
                    new_GUILD.update_one({'_id':1} ,{"$set":{'count_guilds':counter}})
                else:
                    new_GUILD.insert_one({'_id':1 ,'count_guilds':1})

        except:
            pass

      
        return

    @commands.Cog.listener() #join to sv jadid
    async def on_guild_remove(self,guild):
        try:
            if (find1:= new_GUILD.find_one({"_id":1})):
                counter = find1['count_guilds']
                counter-=1
                new_GUILD.update_one({'_id':1} ,{"$set":{'count_guilds':counter}})
                new_GUILD.delete_one({'_id':guild.id})
        except:
            pass


    @commands.Cog.listener()
    async def on_command_error(self,ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"{ctx.author.mention} command is cooldown wait for {round(error.retry_after)} seconds")

        elif isinstance(error,commands.MissingPermissions):
            await ctx.send(f'{ctx.author.mention} you dont have permission')
        elif isinstance(error,commands.CheckFailure):
            pass
        elif isinstance(error ,commands.ArgumentParsingError) :
            pass
        elif isinstance(error,commands.BadArgument):
            pass   
        # elif isinstance(error , commands.BadBoolArgument):
        #     pass
        # elif isinstance(error ,commands.BadInviteArgument ):
        #     pass
        elif isinstance(error ,commands.BadLiteralArgument ):
            pass
        elif isinstance(error , commands.BadUnionArgument):
            pass
        elif isinstance(error,commands.BotMissingRole):
            await ctx.send('bot missing role!')
        elif isinstance(error,commands.BotMissingPermissions ):
            await ctx.send('bot permission is not enough')
        elif isinstance(error, commands.ChannelNotFound):
            await ctx.send('channel not found')
        # elif isinstance(error,commands.ChannelNotFound):
        #     pass
        elif isinstance(error ,commands.CommandInvokeError ):
            pass
        elif isinstance(error ,commands.ChannelNotReadable ):
            pass
        elif isinstance(error , commands.CommandError):
            pass


        elif isinstance(error ,commands.MissingPermissions ):
            await ctx.send(f'you dont have permission , for using this bot you better have administrator')



#####################################
    @commands.hybrid_command(name='setgifchannel' , description='Enable Gif Request by users in specific channel')
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    @app_commands.choices(state=[
        app_commands.Choice(name='True' , value=1),
        app_commands.Choice(name='False' , value=1)
       
    ])#,channel_set=[app_commands.Choice(name='Enable' , value=1),app_commands.Choice(name='Disable' , value=2)])
    async def setgifchannel(self,ctx , state:app_commands.Choice[int] , channel_set:discord.TextChannel):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('your role is not above me then you cant use this command' , ephemeral=True)

        try:
            if(find:= collection.find_one({"_id":ctx.guild.id})):
                collection.update_one({"_id":ctx.guild.id} , {'$set':{"channel":channel_set.id , "state":state.value}})
                await ctx.send(f'the values updated',ephemeral=True)
            else:            
                collection.insert_one({'_id':ctx.guild.id ,'sv_name':ctx.guild.name , "channel":channel_set.id , "state" : state.value})
                await ctx.send("Gif Settings saved",ephemeral=True)

        except:

            return await ctx.send('something went wrong pls try again',ephemeral=True)


    async def get_error_embed(self,interaction):
        embed=discord.Embed(title='ERROR',description =f'{interaction.user.mention},PLS TRY AGAIN')  
        return embed   

    async def get_channel_embed(self,interaction ,tmp_id_channel):
        embed=discord.Embed(title='WRONG CHANNEL WARNING',description =f'you only can use this command in this <#{tmp_id_channel}> channel')  
        return embed   

    async def get_set_embed(self,interaction):
        embed=discord.Embed(title='SET CHANNEL',description =f'the fun channel is not set yet')  
        return embed   


    async def get_embed(self,interaction):
        embed=discord.Embed(title='Wait Process',description =f'{interaction.user.mention},generating ...')  
        return embed   

    





    @app_commands.command(
        name='autogif',
        description='setup auto gif'
    )
    @app_commands.default_permissions(use_application_commands=True)
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    async def autogif(self,interaction:discord.Interaction):
        if interaction.guild.me.top_role.position > interaction.user.top_role.position and interaction.user.id != interaction.guild.owner_id:
            return await interaction.response.send_message('your role is not above me then you cant use this command' , ephemeral=True)
        
        if (find:=collection.find_one({"server_id":interaction.guild_id})):
            pass
        else:
            collection.insert_one({"server_id":interaction.guild_id , "slot1_subject":None , 'slot1_channel':None,'slot1_webhook':None, 'slot1_count':None,  "slot2_subject":None,'slot2_webhook':None, 'slot2_channel':None, 'slot2_count':None , "slot3_subject":None,'slot3_webhook':None, 'slot3_channel':None , 'slot3_count':None, "slot4_subject":None ,'slot4_webhook':None, 'slot4_channel':None, 'slot4_count':None, "slot5_subject":None ,'slot5_webhook':None, 'slot5_channel':None, 'slot5_count':None, "slot6_subject":None,'slot6_webhook':None, 'slot6_channel':None, 'slot6_count':None , "slot7_subject":None,'slot7_webhook':None, 'slot7_channel':None, 'slot7_count':None , "slot8_subject":None,'slot8_webhook':None, 'slot8_channel':None , 'slot8_count':None, "slot9_subject":None,'slot9_webhook':None, 'slot9_channel':None, 'slot9_count':None , "slot10_subject":None,'slot10_webhook':None, 'slot10_channel':None, 'slot10_count':None})
        embed = discord.Embed(

            title=f"Auto Gif Easy Setup",
            description= f'🤖 AUTO GIF SENDER SETUP\n\n📌 Send Gif Every 6 hours\n\n🟢 The last modification will be saved\n\n🛠 Every time you change an specific subject its will send gif in that channel before the time comes',
            timestamp=datetime.now(),
            color= 0x0554FE
        )
        embed.set_image(url="https://media.discordapp.net/attachments/1198003052213448839/1198987152063725568/g0R9.gif?ex=65c0e6cd&is=65ae71cd&hm=8e178256e13db762528044c34c7e2178cb99c0cf4884eb521a31d96f1c45d553&=&width=575&height=575")
        await interaction.response.send_message(embed=embed , view=AutoGifGen(self.bot))
        
        



    @app_commands.command(
        name='gifgenerate',
        description='generate random fun gif'
    )
    @app_commands.default_permissions(use_application_commands=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    async def gifgenerate(self,interaction:discord.Interaction , subject:str):
        await interaction.response.defer()
        
        wait_embed = await self.get_embed(interaction)
        try:
            msg = await interaction.followup.send(embed=wait_embed)
        except:
            return
        if(find:= collection.find_one({"_id":interaction.guild.id})):
            tmp_guild = find['_id']
            tmp_id_channel= find['channel']
            name_embed = subject
            if " " not in subject:
                subject = subject + ' ' + subject

            if interaction.channel_id == tmp_id_channel:
                try:
                    main_guild=self.bot.get_guild(tmp_guild )
                    channel_send = discord.utils.get(main_guild.text_channels , id = tmp_id_channel)
                    response , range_search = await self.userpic(subject, msg , interaction)
                    if range_search-1 >0:
                        if response is not None:
                            embed = discord.Embed(

                                title=f"{find['sv_name']}",
                                description= f'{name_embed} GIF FOR {interaction.user.mention}\n',
                                timestamp=datetime.now(),
                                color= 0x0554FE
                            )
                            selector = random.randint(0 , range_search-1)
                            embed.set_image(url=response['data'][selector]['images']['original']['url'])
                            await msg.edit(embed=embed)

                            # await interaction.followup.send(response['data'][6]['url'])
                        else:
                            embeder = await self.get_error_embed(interaction)
                            await msg.edit(embed=embeder)
                    else:
                        embeder = await self.get_not_found_embed(interaction)
                        await msg.edit(embed=embeder)
                except:
                    try:
                        response , range_search = await self.userpic(subject , msg , interaction)
                        if range_search-1 >0:
                            if response is not None:
                                response=response.replace('<' , '')
                                response=response.replace('>' , '')
                                response=response.replace('img ' , '')
                                response=response.replace('src=' , '')
                                response=response.replace("'" , '')
                                embed = discord.Embed(

                                    title=f"{find['sv_name']}",
                                    description= f'{name_embed} gif for {interaction.user.mention}\n',
                                    timestamp=datetime.now(),
                                    color= 0x0554FE
                                )
                                selector = random.randint(0 , range_search-1)
                                embed.set_image(url=response['data'][selector]['images']['original']['url'])
                                await msg.edit(embed=embed)
                                # await interaction.followup.send(embed=embed)
                            else:
                                embeder = await self.get_error_embed(interaction)
                                await msg.edit(embed=embeder)
                        else:
                            embeder = await self.get_not_found_embed(interaction)
                            await msg.edit(embed=embeder)

                    except:
                        try:
                            embeder = await self.get_error_embed(interaction)
                            await msg.edit(embed=embeder)
                        except:
                            return
            else:
                try:
                    embeder = await self.get_channel_embed(interaction , tmp_id_channel)
                    await msg.edit(embed=embeder)
                except:
                    return
        else:
            try:
                embeder = await self.get_set_embed(interaction)
                await msg.edit(embed=embeder)
            except:
                return

    


        

async def setup(bot : Bot):
    await bot.add_cog(Gif(bot))
