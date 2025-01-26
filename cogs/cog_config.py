from __future__ import annotations

from discord.ext.commands import Cog
from core.bot import Bot
from logging import getLogger ; log = getLogger()

class Plugin(Cog):
    def __init__(self , bot:Bot):
        super().__init__()
    
    async def cog_load(self) -> None:
        log.info(f'succesfully cog loaded')

async def setup(bot : Bot):
    await bot.add_cog(Plugin(bot))