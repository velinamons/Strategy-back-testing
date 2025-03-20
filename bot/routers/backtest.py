from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.utils.keyboards import kb_symbols
from bot.utils.states import SingleBacktestState, MultiBacktestState

backtest_router = Router()


@backtest_router.message(Command("start_single_asset_backtest"))
async def start_single_asset_backtest(message: Message, state: FSMContext):
    """Handles symbol selection for a single asset backtest."""
    await message.answer("Choose a symbol:", reply_markup=kb_symbols(multi=False))
    await state.set_state(SingleBacktestState.choosing_symbol)


@backtest_router.message(Command("start_multi_asset_backtest"))
async def start_multi_asset_backtest(message: Message, state: FSMContext):
    """Handles symbol selection for a multi-asset backtest."""
    await message.answer("Choose at least 2 symbols (press 'Done' when finished):", reply_markup=kb_symbols(multi=True))
    await state.set_state(MultiBacktestState.choosing_symbols)
