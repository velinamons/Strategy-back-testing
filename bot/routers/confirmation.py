from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.utils.keyboards import kb_main
from bot.utils.states import SingleBacktestState, MultiBacktestState

# Assuming your backtest functions
# from backtest import run_backtest_single_asset, run_backtest_multi_asset

confirmation_router = Router()


@confirmation_router.message(MultiBacktestState.confirming_parameters)
async def handle_multi_backtest_confirmation(message: Message, state: FSMContext):
    """Handles backtest confirmation for multi-asset backtest."""
    user_choice = message.text.lower()

    if user_choice == "run backtest":
        # Run the backtest here by calling your backtest function
        data = await state.get_data()  # Retrieve the parameters for the backtest
        selected_symbols = data.get("selected_symbols", [])
        selected_interval = data.get("selected_interval")
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        selected_strategy = data.get("selected_strategy")
        strategy_params = data.get("strategy_params", {})
        portfolio_params = data.get("portfolio_params", {})

        # Run the actual backtest
        # await run_backtest_multi_asset(
        #     selected_symbols,
        #     selected_interval,
        #     start_date,
        #     end_date,
        #     selected_strategy,
        #     strategy_params,
        #     portfolio_params
        # )

        await state.clear()
        await message.answer("Backtest completed successfully!", reply_markup=kb_main)

    elif user_choice == "cancel":
        await state.clear()
        await message.answer("Backtest cancelled.", reply_markup=kb_main)


@confirmation_router.message(SingleBacktestState.confirming_parameters)
async def handle_single_backtest_confirmation(message: Message, state: FSMContext):
    """Handles backtest confirmation for single-asset backtest."""
    user_choice = message.text.lower()

    if user_choice == "run backtest":
        # Run the backtest here by calling your backtest function
        data = await state.get_data()  # Retrieve the parameters for the backtest
        selected_symbol = data.get("selected_symbol")
        selected_interval = data.get("selected_interval")
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        selected_strategy = data.get("selected_strategy")
        strategy_params = data.get("strategy_params", {})
        portfolio_params = data.get("portfolio_params", {})

        # Run the actual backtest
        # await run_backtest_single_asset(
        #     selected_symbol,
        #     selected_interval,
        #     start_date,
        #     end_date,
        #     selected_strategy,
        #     strategy_params,
        #     portfolio_params
        # )

        await state.clear()
        await message.answer("Backtest completed successfully!", reply_markup=kb_main)

    elif user_choice == "cancel":
        await state.clear()
        await message.answer("Backtest cancelled.", reply_markup=kb_main)  # Replace with your main menu
