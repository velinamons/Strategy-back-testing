import asyncio
from fetcher.app import fetch_klines_batch
from bot.app import start_bot
from logger.config import logger


async def main():
    logger.info("Starting app")
    await fetch_klines_batch()
    logger.info("Starting bot")
    await start_bot()


if __name__ == "__main__":
    asyncio.run(main())
