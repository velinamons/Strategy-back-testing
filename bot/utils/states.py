from aiogram.fsm.state import State, StatesGroup


# TODO: Remove code duplication
class SingleBacktestState(StatesGroup):
    choosing_symbol = State()
    choosing_interval = State()
    waiting_for_date_choice = State()
    waiting_for_custom_range = State()
    choosing_strategy = State()
    choosing_strategy_params = State()
    entering_strategy_params = State()
    choosing_portfolio_params = State()
    entering_portfolio_params = State()
    confirming_parameters = State()


class MultiBacktestState(StatesGroup):
    choosing_symbols = State()
    choosing_interval = State()
    waiting_for_date_choice = State()
    waiting_for_custom_range = State()
    choosing_strategy = State()
    choosing_strategy_params = State()
    entering_strategy_params = State()
    choosing_portfolio_params = State()
    entering_portfolio_params = State()
    confirming_parameters = State()
