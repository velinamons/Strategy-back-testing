from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.utils.states import SingleBacktestState, MultiBacktestState
from bot.utils.keyboards import kb_intervals, kb_dates, kb_strategies
from settings import SYMBOLS_CONFIG
from utils.validators import validate_date_range

symbols_router = Router()

# TODO: DRY, remove duplicated code fragments

@symbols_router.message(SingleBacktestState.choosing_symbol)
async def handle_single_symbol_selection(message: Message, state: FSMContext):
    """Stores the selected symbol and moves to interval selection."""
    selected_symbol = message.text

    if selected_symbol not in SYMBOLS_CONFIG:
        await message.answer("Invalid selection. Please choose a valid symbol.")
        return

    await state.update_data(selected_symbol=selected_symbol)

    await message.answer(
        f"Selected symbol: {selected_symbol}\n\nNow choose an interval:",
        reply_markup=kb_intervals([selected_symbol])
    )
    await state.set_state(SingleBacktestState.choosing_interval)


@symbols_router.message(MultiBacktestState.choosing_symbols)
async def handle_multi_symbol_selection(message: Message, state: FSMContext):
    """Stores multiple selected symbols and moves to interval selection when done."""
    data = await state.get_data()
    selected_symbols = data.get("selected_symbols", [])

    user_input = message.text

    if user_input == "Done":
        if not selected_symbols or len(selected_symbols) < 2:
            await message.answer("You must select at least two symbols before pressing 'Done'.")
            return

        await message.answer(
            f"Selected symbols: {', '.join(selected_symbols)}\n\nNow choose an interval:",
            reply_markup=kb_intervals(selected_symbols)
        )
        await state.set_state(MultiBacktestState.choosing_interval)
        return

    if user_input not in SYMBOLS_CONFIG:
        await message.answer("Invalid selection. Please choose a valid symbol.")
        return

    if user_input in selected_symbols:
        await message.answer(f"{user_input} is already selected.")
    else:
        selected_symbols.append(user_input)
        await state.update_data(selected_symbols=selected_symbols)
        await message.answer(f"Added {user_input}. Choose more or press 'Done'.")


@symbols_router.message(SingleBacktestState.choosing_interval)
async def handle_single_interval_selection(message: Message, state: FSMContext):
    """Handles interval selection for a single-symbol backtest."""
    data = await state.get_data()
    selected_symbol = data["selected_symbol"]

    available_intervals = SYMBOLS_CONFIG.get(selected_symbol, {}).keys()

    selected_interval = message.text
    if selected_interval not in available_intervals:
        await message.answer("Invalid interval selection. Please choose a valid interval.")
        return

    await state.update_data(selected_interval=selected_interval)
    await message.answer(f"Selected interval: {selected_interval}\n\nNow proceed with dates.")

    symbol_data = SYMBOLS_CONFIG.get(selected_symbol, {}).get(selected_interval)

    if symbol_data is None:
        await message.answer("No data found for the selected symbol and interval. Please /start again.")
        return

    available_start = symbol_data["start_date"]
    available_end = symbol_data["end_date"]

    await state.update_data(available_start=available_start, available_end=available_end)

    await message.answer(f"Available range for {selected_symbol} ({selected_interval}):\n"
                         f"Default range: {available_start} - {available_end}\n\n"
                         "Please choose an option:", reply_markup=kb_dates)

    await state.set_state(SingleBacktestState.waiting_for_date_choice)


@symbols_router.message(SingleBacktestState.waiting_for_date_choice)
async def handle_single_date_choice(message: Message, state: FSMContext):
    """Handles user's choice of default or custom date range."""
    user_input = message.text.strip().lower()
    data = await state.get_data()

    available_start = data["available_start"]
    available_end = data["available_end"]

    if user_input == "default":
        await state.update_data(start_date=available_start, end_date=available_end)
        await message.answer(
            f"Selected range: {available_start} - {available_end}\n\nNow proceed with strategy.",
            reply_markup=kb_strategies(is_multi=False)
        )
        await state.set_state(SingleBacktestState.choosing_strategy)
    elif user_input == "custom":
        await message.answer(
            f"Please input your custom date range in the format 'Y-m-d - Y-m-d' within the available range: {available_start} - {available_end}.")
        await state.set_state(SingleBacktestState.waiting_for_custom_range)
    else:
        await message.answer("Invalid option. Please choose either 'Default' or 'Custom'.")



@symbols_router.message(SingleBacktestState.waiting_for_custom_range)
async def handle_single_custom_date_input(message: Message, state: FSMContext):
    """Handles custom date range input and validates it."""
    user_input = message.text.strip()

    data = await state.get_data()

    available_start = data["available_start"]
    available_end = data["available_end"]

    if " - " not in user_input:
        await message.answer("Invalid format. Please enter the date range as 'Y-m-d - Y-m-d'.")
        return

    try:
        selected_start, selected_end = map(str.strip, user_input.split(" - "))
        selected_start, selected_end = validate_date_range(selected_start, selected_end, available_start, available_end)
    except ValueError:
        await message.answer(
            f"Invalid date range. Please ensure the date is in format 'Y-m-d - Y-m-d' and  within the available range: {available_start} - {available_end}.")
        return

    await state.update_data(start_date=selected_start, end_date=selected_end)
    await message.answer(
        f"Selected range: {selected_start} - {selected_end}\n\nNow proceed with strategy.",
        reply_markup=kb_strategies(is_multi=False)
    )
    await state.set_state(SingleBacktestState.choosing_strategy)


@symbols_router.message(MultiBacktestState.choosing_interval)
async def handle_multi_interval_selection(message: Message, state: FSMContext):
    """Handles interval selection for multi-symbol backtest."""
    data = await state.get_data()
    selected_symbols = data["selected_symbols"]

    all_intervals = [set(SYMBOLS_CONFIG.get(symbol, {}).keys()) for symbol in selected_symbols]

    available_intervals = set.intersection(*all_intervals)

    selected_interval = message.text
    if selected_interval not in available_intervals:
        await message.answer("Invalid interval selection. Please choose a valid interval.")
        return

    await state.update_data(selected_interval=selected_interval)
    await message.answer(f"Selected interval: {selected_interval}\n\nNow proceed with dates.")

    start_dates = []
    end_dates = []

    for symbol in selected_symbols:
        symbol_data = SYMBOLS_CONFIG.get(symbol, {}).get(selected_interval)

        if symbol_data is None:
            await message.answer(f"No data found for symbol {symbol} with interval {selected_interval}.")
            return

        start_dates.append(symbol_data["start_date"])
        end_dates.append(symbol_data["end_date"])

    available_start = max(start_dates)
    available_end = min(end_dates)

    await state.update_data(available_start=available_start, available_end=available_end)

    if available_start > available_end:
        await message.answer("No common date range found for selected symbols. Try again with /start.")
        return

    await message.answer(f"Available range for selected symbols ({selected_interval}):\n"
                         f"Default range: {available_start} - {available_end}\n\n"
                         "Please choose an option:", reply_markup=kb_dates)

    await state.set_state(MultiBacktestState.waiting_for_date_choice)


@symbols_router.message(MultiBacktestState.waiting_for_date_choice)
async def handle_multi_date_choice(message: Message, state: FSMContext):
    """Handles user's choice of default or custom date range."""
    user_input = message.text.strip().lower()
    data = await state.get_data()

    available_start = data["available_start"]
    available_end = data["available_end"]

    if user_input == "default":
        await state.update_data(start_date=available_start, end_date=available_end)
        await message.answer(
            f"Selected range: {available_start} - {available_end}\n\nNow proceed with strategy.",
            reply_markup=kb_strategies(is_multi=True)
        )
        await state.set_state(MultiBacktestState.choosing_strategy)
    elif user_input == "custom":
        await message.answer(
            f"Please input your custom date range in the format 'Y-m-d - Y-m-d' within the available range: {available_start} - {available_end}.")
        await state.set_state(MultiBacktestState.waiting_for_custom_range)
    else:
        await message.answer("Invalid option. Please choose either 'Default' or 'Custom'.")


@symbols_router.message(MultiBacktestState.waiting_for_custom_range)
async def handle_multi_custom_date_input(message: Message, state: FSMContext):
    """Handles custom date range input and validates it."""
    user_input = message.text.strip()

    data = await state.get_data()

    available_start = data["available_start"]
    available_end = data["available_end"]

    if " - " not in user_input:
        await message.answer("Invalid format. Please enter the date range as 'Y-m-d - Y-m-d'.")
        return

    try:
        selected_start, selected_end = map(str.strip, user_input.split(" - "))
        selected_start, selected_end = validate_date_range(selected_start, selected_end, available_start, available_end)
    except ValueError:
        await message.answer(
            f"Invalid date range. Please ensure the date is in format 'Y-m-d - Y-m-d' and  within the available range: {available_start} - {available_end}.")
        return

    await state.update_data(start_date=selected_start, end_date=selected_end)
    await message.answer(
        f"Selected range: {selected_start} - {selected_end}\n\nNow proceed with strategy.",
        reply_markup=kb_strategies(is_multi=True)
    )
    await state.set_state(MultiBacktestState.choosing_strategy)
