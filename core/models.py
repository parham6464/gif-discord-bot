from __future__ import annotations

import discord
import random
from tortoise.models import Model
from tortoise.contrib.postgres.fields import ArrayField
from tortoise import fields
from .embed import Embed
from datetime import datetime
from contextlib import suppress

class Giveawaymodel(Model):
    guild_id :int  = fields.BigIntField()
    message_id :int  = fields.BigIntField()
    channel_id :int  = fields.BigIntField()
    host_id :int  = fields.BigIntField()
    required_role_id :int  = fields.BigIntField(null=True)
    prize: fields.Field[str] = fields.CharField(max_length=200)
    duration:float = fields.FloatField()
    winners:int = fields.IntField()
    participants:fields.Field[list] = ArrayField(element_type="bigint")
    max_entries:int = fields.IntField(null=True)
    is_active:bool = fields.BooleanField(default=True)

    async def check_for_requirements(self,interaction:discord.Interaction) ->bool or str:
        assert interaction.guild is not None and isinstance(interaction.user , discord.Member)
        if self.required_role_id is not None and (role:=interaction.guild.get_role(self.required_role_id)):
            if role in interaction.user.roles:
                return True
            return f"only users with the {role.mention} role can join this giveaway."
            # can add more requirements like invite count and message count
        return True
    
    def get_winner(self, guild:discord.Guild)-> list[discord.Member] or None:
        participants = [m for m in (guild.get_member(i) for i in self.participants) if m]
        if not participants:return None
        winners:list[discord.Member] = list()
        num_winners = min(self.winners,len (participants))
        while len(winners) < num_winners:
            participant = random.choice(participants)
            if participant in winners:
                continue
            else:
                winners.append(participant)
        return winners

    def get_winner_mention(self , guild:discord.Guild)-> list(str) or None :
        winners = self.get_winner(guild)
        if not winners:
            return None
        return [m.mention for m in winners]

    def create_giveaway_embed(self ,title,description ,required_role:discord.Role or None , host:discord.Member or discord.User )->Embed:
        embed = Embed()
        embed.set_author(name=title)
        embed.description=f'{description}'
        embed.add_field(name='Prize:' , value=f'{self.prize}' , inline=False)
        embed.add_field(name='Winners:' , value=f'{self.winners}' , inline=False)
        embed.add_field(name='Ends at :' , value=f"{discord.utils.format_dt(datetime.fromtimestamp(self.duration),'R')}" , inline=False)
        embed.add_field(name='Hosted by:' , value=f'{host.mention}' , inline=False)
        embed.add_field(name='Maximum Entries:' , value=f"{self.max_entries if self.max_entries else 'Unlimited'}" , inline=False)

        if required_role:
            embed.add_field(name='Requirements' , value=f"Required role: {required_role.mention}" ,inline=False)
        return embed
    
    @property
    def get_end_embed(self)->Embed:
        return Embed(title='Giveaway Ended' , description=f"Winners: {self.winners}\n total users that joined: {len(self.participants)}\n Hosted by: <@{self.host_id}>\nMaximum Entries: {self.max_entries if self.max_entries else 'Unlimited'}")

    
    async def end_giveaway(self,guild:discord.Guild , message:discord.PartialMessage ):
        embed = self.get_end_embed
        checker_channel=self.channel_id
        checker_channel = discord.utils.get(guild.channels , id = checker_channel)
        flag=False
        if checker_channel is not None:
            async for messager in checker_channel.history(limit=200):
                if messager.id == self.message_id:
                    flag=True
        if flag == False:
            await self.delete()
            return
        if len(self.participants) >0:
            if (winner_mentions:= self.get_winner_mention(guild)):
                embed.add_field(name="Winners" , value=', '.join(winner_mentions))
                await message.reply(f"{', '.join(winner_mentions)} you have won the {self.prize}.")
            self.is_active = False
            await self.save()
        elif len(self.participants) == 0:
            await message.reply(f"no one joined the giveaway")
            self.is_active = False
            await self.save()

        else:
            await self.delete()
        with suppress(Exception):
            await message.edit(embed=embed , view=None)