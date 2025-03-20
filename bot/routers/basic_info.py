from aiogram import Router
from aiogram.filters import Command
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import Message
from settings import SYMBOLS_CONFIG, PORTFOLIO_CONFIG, STRATEGIES_CONFIG
from bot.utils.message_answer_formatter import html_format_strategies, html_format_symbols, html_format_portfolio
from bot.utils.keyboards import kb_main

basic_router = Router()


@basic_router.message(Command("start"))
async def start(message: Message):
    await message.answer("Welcome to the Backtest Bot! Use the commands to interact.", reply_markup=kb_main)


@basic_router.message(Command("symbols"))
async def symbols(message: Message):
    formatted_symbols = html_format_symbols(SYMBOLS_CONFIG)
    await message.answer(f"📊 Available symbols:\n\n{formatted_symbols}", parse_mode=ParseMode.HTML)


@basic_router.message(Command("portfolio"))
async def portfolio(message: Message):
    formatted_portfolio = html_format_portfolio(PORTFOLIO_CONFIG)
    await message.answer(f"💼 Portfolio Configuration:\n\n{formatted_portfolio}", parse_mode=ParseMode.HTML)


@basic_router.message(Command("strategies"))
async def strategies(message: Message):
    formatted_strategies = html_format_strategies(STRATEGIES_CONFIG)
    await message.answer(f"📈 Available Strategies:\n\n{formatted_strategies}", parse_mode=ParseMode.HTML)
