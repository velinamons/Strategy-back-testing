from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.utils.keyboards import kb_backtest_confirm
from bot.utils.message_answer_formatter import html_format_params
from bot.utils.states import SingleBacktestState, MultiBacktestState
from settings import PORTFOLIO_CONFIG

portfolio_router = Router()


def get_portfolio_params() -> dict:
    """Returns the portfolio parameters from the config dictionary."""
    return {
        param_name: param_info["default_value"]
        for param_name, param_info in PORTFOLIO_CONFIG["params"].items()
    }

# TODO: DRY, remove duplicated code fragments

@portfolio_router.message(SingleBacktestState.choosing_portfolio_params)
async def handle_single_portfolio_choice(message: Message, state: FSMContext):
    """Handles portfolio parameter selection for single-asset backtest."""
    user_choice = message.text.lower()

    if user_choice == "use default parameters":
        default_params = get_portfolio_params()
        await state.update_data(portfolio_params=default_params)

        await message.answer(
            f"Using default parameters:\n\n" +
            "\n".join([f"{k}: {v}" for k, v in default_params.items()])
        )

        data = await state.get_data()  # Retrieve the data to show in confirmation
        selected_symbol = data.get("selected_symbol", [])
        selected_interval = data.get("selected_interval")
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        selected_strategy = data.get("selected_strategy")
        strategy_params = data.get("strategy_params", {})
        portfolio_params = data.get("portfolio_params", {})

        confirmation_message = (
            f"Confirming the following parameters:\n\n"
            f"Symbol: {selected_symbol}\n"
            f"Interval: {selected_interval}\n"
            f"Start Date: {start_date}\n"
            f"End Date: {end_date}\n\n"
            f"Strategy: {selected_strategy}\n\n"
            f"Strategy Params:\n{html_format_params(strategy_params)}\n\n"
            f"Portfolio Params:\n{html_format_params(portfolio_params)}"
        )

        await message.answer(confirmation_message, reply_markup=kb_backtest_confirm(), parse_mode="HTML")

        await state.set_state(SingleBacktestState.confirming_parameters)

    elif user_choice == "enter custom parameters":
        await state.update_data(custom_portfolio_params={})
        param_list = list(PORTFOLIO_CONFIG["params"].keys())

        await state.update_data(portfolio_param_list=param_list, current_portfolio_param_idx=0)

        first_param = param_list[0]

        await message.answer(
            f"Enter value for {first_param} ({PORTFOLIO_CONFIG['params'][first_param]['description']}):"
        )

        await state.set_state(SingleBacktestState.entering_portfolio_params)


@portfolio_router.message(MultiBacktestState.choosing_portfolio_params)
async def handle_multi_portfolio_choice(message: Message, state: FSMContext):
    """Handles portfolio parameter selection for multi-asset backtest."""
    user_choice = message.text.lower()

    if user_choice == "use default parameters":
        default_params = get_portfolio_params()
        await state.update_data(portfolio_params=default_params)

        await message.answer(
            f"Using default parameters:\n\n" +
            "\n".join([f"{k}: {v}" for k, v in default_params.items()])
        )

        data = await state.get_data()  # Retrieve the data to show in confirmation
        selected_symbols = data.get("selected_symbols", [])
        selected_interval = data.get("selected_interval")
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        selected_strategy = data.get("selected_strategy")
        strategy_params = data.get("strategy_params", {})
        portfolio_params = data.get("portfolio_params", {})

        confirmation_message = (
            f"Confirming the following parameters:\n\n"
            f"Symbols: {', '.join(selected_symbols)}\n"
            f"Interval: {selected_interval}\n"
            f"Start Date: {start_date}\n"
            f"End Date: {end_date}\n\n"
            f"Strategy: {selected_strategy}\n\n"
            f"Strategy Params:\n{html_format_params(strategy_params)}\n\n"
            f"Portfolio Params:\n{html_format_params(portfolio_params)}"
        )

        await message.answer(confirmation_message, reply_markup=kb_backtest_confirm(), parse_mode="HTML")

        await state.set_state(MultiBacktestState.confirming_parameters)

    elif user_choice == "enter custom parameters":
        await state.update_data(custom_portfolio_params={})
        param_list = list(PORTFOLIO_CONFIG["params"].keys())

        await state.update_data(portfolio_param_list=param_list, current_portfolio_param_idx=0)

        first_param = param_list[0]

        await message.answer(
            f"Enter value for {first_param} ({PORTFOLIO_CONFIG['params'][first_param]['description']}):"
        )

        await state.set_state(MultiBacktestState.entering_portfolio_params)


@portfolio_router.message(SingleBacktestState.entering_portfolio_params)
async def handle_single_custom_portfolio_param(message: Message, state: FSMContext):
    """Handles user input for custom portfolio parameters (single-asset)."""
    data = await state.get_data()
    portfolio_param_list = data.get("portfolio_param_list")
    current_portfolio_param_idx = data.get("current_portfolio_param_idx")

    param_name = portfolio_param_list[current_portfolio_param_idx]

    try:
        param_value = float(message.text)
    except ValueError:
        await message.answer("Invalid input. Please enter a valid number.")
        return

    custom_portfolio_params = data.get("custom_portfolio_params", {})
    custom_portfolio_params[param_name] = param_value
    await state.update_data(custom_portfolio_params=custom_portfolio_params)

    current_portfolio_param_idx += 1

    if current_portfolio_param_idx < len(portfolio_param_list):
        next_param = portfolio_param_list[current_portfolio_param_idx]
        await state.update_data(current_portfolio_param_idx=current_portfolio_param_idx)
        await message.answer(
            f"Enter value for {next_param} ({PORTFOLIO_CONFIG['params'][next_param]['description']}):"
        )
    else:
        await state.update_data(portfolio_params=custom_portfolio_params)
        await message.answer(
            f"Custom parameters saved:\n\n" +
            "\n".join([f"{k}: {v}" for k, v in custom_portfolio_params.items()])
        )

        data = await state.get_data()  # Retrieve the data to show in confirmation
        selected_symbol = data.get("selected_symbol", [])
        selected_interval = data.get("selected_interval")
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        selected_strategy = data.get("selected_strategy")
        strategy_params = data.get("strategy_params", {})
        portfolio_params = data.get("portfolio_params", {})

        confirmation_message = (
            f"Confirming the following parameters:\n\n"
            f"Symbol: {selected_symbol}\n"
            f"Interval: {selected_interval}\n"
            f"Start Date: {start_date}\n"
            f"End Date: {end_date}\n\n"
            f"Strategy: {selected_strategy}\n\n"
            f"Strategy Params:\n{html_format_params(strategy_params)}\n\n"
            f"Portfolio Params:\n{html_format_params(portfolio_params)}"
        )

        await message.answer(confirmation_message, reply_markup=kb_backtest_confirm(), parse_mode="HTML")

        await state.set_state(SingleBacktestState.confirming_parameters)


@portfolio_router.message(MultiBacktestState.entering_portfolio_params)
async def handle_multi_custom_portfolio_param(message: Message, state: FSMContext):
    """Handles user input for custom portfolio parameters (multi-asset)."""
    data = await state.get_data()
    portfolio_param_list = data.get("portfolio_param_list")
    current_portfolio_param_idx = data.get("current_portfolio_param_idx")

    param_name = portfolio_param_list[current_portfolio_param_idx]

    try:
        param_value = float(message.text)
    except ValueError:
        await message.answer("Invalid input. Please enter a valid number.")
        return

    custom_portfolio_params = data.get("custom_portfolio_params", {})
    custom_portfolio_params[param_name] = param_value
    await state.update_data(custom_portfolio_params=custom_portfolio_params)

    current_portfolio_param_idx += 1

    if current_portfolio_param_idx < len(portfolio_param_list):
        next_param = portfolio_param_list[current_portfolio_param_idx]
        await state.update_data(current_portfolio_param_idx=current_portfolio_param_idx)
        await message.answer(
            f"Enter value for {next_param} ({PORTFOLIO_CONFIG['params'][next_param]['description']}):"
        )
    else:
        await state.update_data(portfolio_params=custom_portfolio_params)
        await message.answer(
            f"Custom parameters saved:\n\n" +
            "\n".join([f"{k}: {v}" for k, v in custom_portfolio_params.items()])
        )

        data = await state.get_data()  # Retrieve the data to show in confirmation
        selected_symbols = data.get("selected_symbols", [])
        selected_interval = data.get("selected_interval")
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        selected_strategy = data.get("selected_strategy")
        strategy_params = data.get("strategy_params", {})
        portfolio_params = data.get("portfolio_params", {})

        confirmation_message = (
            f"Confirming the following parameters:\n\n"
            f"Symbols: {', '.join(selected_symbols)}\n"
            f"Interval: {selected_interval}\n"
            f"Start Date: {start_date}\n"
            f"End Date: {end_date}\n\n"
            f"Strategy: {selected_strategy}\n\n"
            f"Strategy Params:\n{html_format_params(strategy_params)}\n\n"
            f"Portfolio Params:\n{html_format_params(portfolio_params)}"
        )

        await message.answer(confirmation_message, reply_markup=kb_backtest_confirm(), parse_mode="HTML")

        await state.set_state(MultiBacktestState.confirming_parameters)
