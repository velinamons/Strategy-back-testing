from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from settings import SYMBOLS, SYMBOLS_CONFIG, STRATEGIES_CONFIG

kb_main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/symbols"), KeyboardButton(text="/portfolio")],
        [KeyboardButton(text="/strategies"), KeyboardButton(text="/start_single_asset_backtest")],
        [KeyboardButton(text="/start_multi_asset_backtest")],
    ],
    resize_keyboard=True,
)


def kb_symbols(multi: bool = False) -> ReplyKeyboardMarkup:
    """Creates a keyboard for selecting symbols.

    - If `multi=True`, allows multiple selections.
    - If `multi=False`, allows only one selection.
    """
    builder = ReplyKeyboardBuilder()

    for symbol in SYMBOLS:
        builder.button(text=symbol)

    if multi:
        builder.button(text="Done")

    return builder.as_markup(resize_keyboard=True)


def kb_intervals(symbols: list[str]) -> ReplyKeyboardMarkup:
    """Creates a keyboard for selecting intervals based on the selected symbol(s)."""
    builder = ReplyKeyboardBuilder()

    if len(symbols) == 1:
        available_intervals = SYMBOLS_CONFIG.get(symbols[0], {}).keys()
    else:
        all_intervals = [set(SYMBOLS_CONFIG.get(symbol, {}).keys()) for symbol in symbols]
        available_intervals = set.intersection(*all_intervals)

    for interval in sorted(available_intervals):
        builder.button(text=interval)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


kb_dates = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Default"), KeyboardButton(text="Custom")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


def kb_strategies(is_multi: bool) -> ReplyKeyboardMarkup:
    """Generate a keyboard with available strategies based on single or multi-asset mode."""
    asset_type = "multi-asset" if is_multi else "single-asset"

    strategy_buttons = [
        KeyboardButton(text=strategy_name)
        for strategy_name, strategy_details in STRATEGIES_CONFIG.items()
        if asset_type in strategy_details["asset_type"]
    ]

    return ReplyKeyboardMarkup(
        keyboard=[strategy_buttons],
        resize_keyboard=True
    )


def kb_param_choice() -> ReplyKeyboardMarkup:
    """Keyboard to choose between default parameters or custom input."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Use default parameters")], [KeyboardButton(text="Enter custom parameters")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )


from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def kb_backtest_confirm() -> ReplyKeyboardMarkup:
    """
    Creates a confirmation keyboard with 'Run Backtest' and 'Cancel' options.

    :param run_callback: Callback data for the "Run Backtest" button.
    :param cancel_callback: Callback data for the "Cancel" button.
    :return: InlineKeyboardMarkup instance
    """
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Run Backtest")], [KeyboardButton(text="Cancel")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
