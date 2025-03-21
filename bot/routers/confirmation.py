import csv

from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from bot.utils.keyboards import kb_main
from bot.utils.states import SingleBacktestState, MultiBacktestState

from backtester.app import run_backtest
from utils.bot_utils import format_csv

confirmation_router = Router()


@confirmation_router.message(MultiBacktestState.confirming_parameters)
async def handle_multi_backtest_confirmation(message: Message, state: FSMContext):
    """Handles backtest confirmation for multi-asset backtest."""
    user_choice = message.text.lower()

    if user_choice == "run backtest":
        data = await state.get_data()
        selected_symbols = data.get("selected_symbols", [])
        selected_interval = data.get("selected_interval")
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        selected_strategy = data.get("selected_strategy")
        strategy_params = data.get("strategy_params", {})
        portfolio_params = data.get("portfolio_params", {})

        result = await run_backtest(
            selected_symbols,
            selected_interval,
            start_date,
            end_date,
            selected_strategy,
            strategy_params,
            portfolio_params
        )

        if "error" in result:
            await message.answer(result["error"], reply_markup=kb_main)
        else:
            plot_path = result["plot_path"]
            plot_file = FSInputFile(plot_path)
            await message.answer_photo(plot_file, caption="Backtest Completed!")

            stats_path = result["result_path"]
            result_text = format_csv(stats_path)
            await message.answer(result_text)
            await message.answer("Backtest completed successfully!", reply_markup=kb_main)
        await state.clear()
    elif user_choice == "cancel":
        await state.clear()
        await message.answer("Backtest cancelled.", reply_markup=kb_main)


@confirmation_router.message(SingleBacktestState.confirming_parameters)
async def handle_single_backtest_confirmation(message: Message, state: FSMContext):
    """Handles backtest confirmation for single-asset backtest."""
    user_choice = message.text.lower()

    if user_choice == "run backtest":
        data = await state.get_data()
        selected_symbol = data.get("selected_symbol")
        selected_interval = data.get("selected_interval")
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        selected_strategy = data.get("selected_strategy")
        strategy_params = data.get("strategy_params", {})
        portfolio_params = data.get("portfolio_params", {})

        result = await run_backtest(
            selected_symbol,
            selected_interval,
            start_date,
            end_date,
            selected_strategy,
            strategy_params,
            portfolio_params
        )
        if "error" in result:
            await message.answer(result["error"], reply_markup=kb_main)
        else:
            plot_path = result["plot_path"]
            plot_file = FSInputFile(plot_path)
            await message.answer_photo(plot_file, caption="Backtest Completed!")

            stats_path = result["result_path"]
            with open(stats_path, 'r') as stats_file:
                stats_text = stats_file.read()
            await message.answer(f"Backtest Results {selected_symbol}:\n\n{stats_text}")
            await message.answer("Backtest completed successfully!", reply_markup=kb_main)
        await state.clear()

    elif user_choice == "cancel":
        await state.clear()
        await message.answer("Backtest cancelled.", reply_markup=kb_main)
