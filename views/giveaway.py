from __future__ import annotations

import discord
from core.models import Giveawaymodel
from core.bot import Bot
from discord import ui 

__all__ = (
    "GiveawayView",
)

class GiveawayView(ui.View):
    def __init__(self , bot:Bot):
        super().__init__(timeout=None)
        self.bot = bot

    
    @ui.button(label='join' , custom_id='gw_join' , style=discord.ButtonStyle.primary)
    async def gw_join(self, interaction:discord.Interaction,_):
        assert interaction.message and interaction.guild and isinstance(interaction.channel , discord.TextChannel)
        await interaction.response.defer(ephemeral=True , thinking=True)
        giveaway = await Giveawaymodel.get_or_none(
            guild_id = interaction.guild_id,
            channel_id = interaction.channel.id,
            message_id = interaction.message.id
        )
        if not giveaway:
            return await self.bot.error(
                f'the giveaway does not exist', interaction
            )
        check =await giveaway.check_for_requirements(interaction)
        if not isinstance(check, bool):
            return await self.bot.error(check , interaction)
        if interaction.user.id in giveaway.participants:
            return await self.bot.error(
                f'you have already joined the giveaway',interaction
            )
        giveaway.participants.append(interaction.user.id)
        self.gw_count.label = str(len(giveaway.participants))
        if giveaway.max_entries:
            if len(giveaway.participants)== giveaway.max_entries:
                self.gw_join.disabled = True
        await interaction.message.edit(view=self)
        await self.bot.success(
            f'you have been successfully joined this giveaway.' , interaction
        )
        return await giveaway.save()
    @ui.button(label='leave' , custom_id='gw_cancel' , style=discord.ButtonStyle.red)
    async def gw_leave(self, interaction:discord.Interaction,_):
        assert interaction.message and interaction.guild and isinstance(interaction.channel , discord.TextChannel)
        await interaction.response.defer(ephemeral=True , thinking=True)
        giveaway = await Giveawaymodel.get_or_none(
            guild_id = interaction.guild_id,
            channel_id = interaction.channel.id,
            message_id = interaction.message.id
        )
        if not giveaway:
            return await self.bot.error(
                f'the giveaway does not exist', interaction
            )
        check =await giveaway.check_for_requirements(interaction)
        if not isinstance(check, bool):
            return await self.bot.error(check , interaction)
        if interaction.user.id in giveaway.participants:
            giveaway.participants.remove(interaction.user.id)
            await self.bot.success(
                f'you leaved giveaway successfully',interaction
            )
        else:
            await self.bot.error(
                f'you didnt join this giveaway!' , interaction
            )

        self.gw_count.label = str(len(giveaway.participants))
        if giveaway.max_entries:
            if len(giveaway.participants)< giveaway.max_entries:
                if self.gw_join.disabled == True:
                    self.gw_join.disabled = False
                

        await interaction.message.edit(view=self)

        return await giveaway.save()

    @ui.button(label='0' , custom_id='gw_count' , disabled=True)
    async def gw_count(self, interaction:discord.Interaction,_):
        ...
    
    @ui.button(label='CANCEL' , custom_id='END' , style=discord.ButtonStyle.danger)
    async def gw_cancel(self, interaction:discord.Interaction,_):
        await interaction.response.defer(ephemeral=True , thinking=True)
        giveaway = await Giveawaymodel.get_or_none(
            guild_id = interaction.guild_id,
            channel_id = interaction.channel.id,
            message_id = interaction.message.id
        )
        if not giveaway:
            return await self.bot.error(
                f'the giveaway does not exist', interaction
            )
        perm_checker= interaction.user.guild_permissions.administrator
        ownership_checker = interaction.guild.owner_id
        if interaction.user.id != giveaway.host_id and perm_checker !=True and interaction.user.id !=ownership_checker :
            await self.bot.error(
            f'you dont have permission', interaction
        )
            

        else:
            checker_channel = discord.utils.get(interaction.guild.channels , id = giveaway.channel_id)
            if checker_channel is not None:
                async for messager in checker_channel.history(limit=200):
                    if messager.id == giveaway.message_id:
                        await messager.delete()
                        await interaction.followup.send(f'giveaway canceld')
                        giveaway.is_active=False
                        await giveaway.delete()
                
