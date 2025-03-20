from aiogram import Bot, Dispatcher

from bot.routers.backtest import backtest_router
from bot.routers.basic_info import basic_router
from bot.routers.confirmation import confirmation_router
from bot.routers.portfolio import portfolio_router
from bot.routers.strategy import strategy_router
from bot.routers.symbols import symbols_router

from settings import TG_TOKEN

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

dp.include_router(basic_router)
dp.include_router(backtest_router)
dp.include_router(symbols_router)
dp.include_router(strategy_router)
dp.include_router(portfolio_router)
dp.include_router(confirmation_router)


async def start_bot():
    await dp.start_polling(bot)
