from __future__ import annotations

from core.bot import Bot
import asyncio , discord
from config import TOKEN
from tortoise.models import Model
from tortoise.contrib.postgres.fields import ArrayField
async def main():
    discord.utils.setup_logging()
    async with Bot() as bot:
        await bot.start(TOKEN , reconnect=True)


if __name__ == '__main__':
    asyncio.run(main())