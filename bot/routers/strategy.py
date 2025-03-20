from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.utils.keyboards import kb_param_choice
from bot.utils.message_answer_formatter import html_format_strategy_params, html_format_portfolio_params
from bot.utils.states import SingleBacktestState, MultiBacktestState
from settings import STRATEGIES_CONFIG

strategy_router = Router()


def get_strategy_params(strategy_name: str) -> dict:
    """Retrieve default parameters for the selected strategy."""
    return {
        param_name: param_info["default_value"]
        for param_name, param_info in STRATEGIES_CONFIG[strategy_name]["params"].items()
    }

# TODO: DRY, remove duplicated code fragments

@strategy_router.message(SingleBacktestState.choosing_strategy)
async def handle_single_strategy_selection(message: Message, state: FSMContext):
    """Handles strategy selection for single-asset backtest."""
    selected_strategy = message.text

    if selected_strategy not in STRATEGIES_CONFIG or "single-asset" not in STRATEGIES_CONFIG[selected_strategy]["asset_type"]:
        await message.answer("Invalid strategy selection. Please choose a valid strategy.")
        return

    await state.update_data(selected_strategy=selected_strategy)

    formatted_params = html_format_strategy_params(selected_strategy)

    await message.answer(
        f"Selected strategy: {selected_strategy}\n\n"
        f"Now configure strategy parameters.\n\n"
        f"{formatted_params}"
        f"Would you like to use default parameters or enter custom values?",
        reply_markup=kb_param_choice(),
        parse_mode="HTML"
    )

    await state.set_state(SingleBacktestState.choosing_strategy_params)


@strategy_router.message(MultiBacktestState.choosing_strategy)
async def handle_multi_strategy_selection(message: Message, state: FSMContext):
    """Handles strategy selection for multi-asset backtest."""
    selected_strategy = message.text

    if selected_strategy not in STRATEGIES_CONFIG or "multi-asset" not in STRATEGIES_CONFIG[selected_strategy]["asset_type"]:
        await message.answer("Invalid strategy selection. Please choose a valid strategy.")
        return

    await state.update_data(selected_strategy=selected_strategy)

    formatted_params = html_format_strategy_params(selected_strategy)

    await message.answer(
        f"Selected strategy: {selected_strategy}\n\n"
        f"Now configure strategy parameters.\n\n"
        f"{formatted_params}"
        f"Would you like to use default parameters or enter custom values?",
        reply_markup=kb_param_choice(),
        parse_mode="HTML"
    )

    await state.set_state(MultiBacktestState.choosing_strategy_params)


@strategy_router.message(SingleBacktestState.choosing_strategy_params)
async def handle_single_strategy_params(message: Message, state: FSMContext):
    """Handles parameter selection for single-asset strategy."""
    user_choice = message.text.lower()
    data = await state.get_data()
    strategy_name = data["selected_strategy"]

    if user_choice == "use default parameters":
        default_params = get_strategy_params(strategy_name)
        await state.update_data(strategy_params=default_params)

        await message.answer(
            f"Using default parameters:\n\n" +
            "\n".join([f"{k}: {v}" for k, v in default_params.items()])
        )

        formatted_params = html_format_portfolio_params()

        await message.answer(
            f"{formatted_params}\n"
            "Would you like to use default parameters or enter custom values?\n",
            reply_markup=kb_param_choice(),
            parse_mode="HTML"
        )

        await state.set_state(SingleBacktestState.choosing_portfolio_params)

    elif user_choice == "enter custom parameters":
        await state.update_data(custom_params={})
        param_list = list(STRATEGIES_CONFIG[strategy_name]["params"].keys())

        await state.update_data(param_list=param_list, current_param_idx=0)

        first_param = param_list[0]
        await message.answer(
            f"Enter value for {first_param} ({STRATEGIES_CONFIG[strategy_name]['params'][first_param]['description']}):"
        )

        await state.set_state(SingleBacktestState.entering_strategy_params)


@strategy_router.message(MultiBacktestState.choosing_strategy_params)
async def handle_multi_strategy_params(message: Message, state: FSMContext):
    """Handles parameter selection for multi-asset strategy."""
    user_choice = message.text.lower()
    data = await state.get_data()
    strategy_name = data["selected_strategy"]

    if user_choice == "use default parameters":
        default_params = get_strategy_params(strategy_name)
        await state.update_data(strategy_params=default_params)

        await message.answer(
            f"Using default parameters:\n\n" +
            "\n".join([f"{k}: {v}" for k, v in default_params.items()])
        )

        formatted_params = html_format_portfolio_params()

        await message.answer(
            f"{formatted_params}\n"
            "Would you like to use default parameters or enter custom values?\n",
            reply_markup=kb_param_choice(),
            parse_mode="HTML"
        )

        await state.set_state(MultiBacktestState.choosing_portfolio_params)

    elif user_choice == "enter custom parameters":
        await state.update_data(custom_params={})
        param_list = list(STRATEGIES_CONFIG[strategy_name]["params"].keys())

        await state.update_data(param_list=param_list, current_param_idx=0)

        first_param = param_list[0]
        await message.answer(
            f"Enter value for {first_param} ({STRATEGIES_CONFIG[strategy_name]['params'][first_param]['description']}):"
        )

        await state.set_state(MultiBacktestState.entering_strategy_params)


@strategy_router.message(SingleBacktestState.entering_strategy_params)
async def handle_single_custom_param(message: Message, state: FSMContext):
    """Handles user input for custom strategy parameters (single-asset)."""
    data = await state.get_data()
    param_list = data["param_list"]
    current_idx = data["current_param_idx"]
    strategy_name = data["selected_strategy"]

    param_name = param_list[current_idx]

    try:
        param_value = int(message.text)
    except ValueError:
        await message.answer("Invalid input. Please enter a valid number.")
        return

    custom_params = data.get("custom_params", {})
    custom_params[param_name] = param_value
    await state.update_data(custom_params=custom_params)

    current_idx += 1
    if current_idx < len(param_list):
        next_param = param_list[current_idx]
        await state.update_data(current_param_idx=current_idx)
        await message.answer(
            f"Enter value for {next_param} ({STRATEGIES_CONFIG[strategy_name]['params'][next_param]['description']}):"
        )
    else:
        await state.update_data(strategy_params=custom_params)

        await message.answer(
            f"Custom parameters saved:\n\n" +
            "\n".join([f"{k}: {v}" for k, v in custom_params.items()])
        )

        formatted_params = html_format_portfolio_params()

        await message.answer(
            f"{formatted_params}\n"
            "Would you like to use default parameters or enter custom values?\n",
            reply_markup=kb_param_choice(),
            parse_mode="HTML"
        )

        await state.set_state(SingleBacktestState.choosing_portfolio_params)


@strategy_router.message(MultiBacktestState.entering_strategy_params)
async def handle_multi_custom_param(message: Message, state: FSMContext):
    """Handles user input for custom strategy parameters (multi-asset)."""
    data = await state.get_data()
    param_list = data["param_list"]
    current_idx = data["current_param_idx"]
    strategy_name = data["selected_strategy"]

    param_name = param_list[current_idx]

    try:
        param_value = int(message.text)
    except ValueError:
        await message.answer("Invalid input. Please enter a valid number.")
        return

    custom_params = data.get("custom_params", {})
    custom_params[param_name] = param_value
    await state.update_data(custom_params=custom_params)

    current_idx += 1
    if current_idx < len(param_list):
        next_param = param_list[current_idx]
        await state.update_data(current_param_idx=current_idx)
        await message.answer(
            f"Enter value for {next_param} ({STRATEGIES_CONFIG[strategy_name]['params'][next_param]['description']}):"
        )
    else:
        await state.update_data(strategy_params=custom_params)

        await message.answer(
            f"Custom parameters saved:\n\n" +
            "\n".join([f"{k}: {v}" for k, v in custom_params.items()])
        )

        formatted_params = html_format_portfolio_params()

        await message.answer(
            f"{formatted_params}\n"
            "Would you like to use default parameters or enter custom values?\n",
            reply_markup=kb_param_choice(),
            parse_mode="HTML"
        )

        await state.set_state(MultiBacktestState.choosing_portfolio_params)
