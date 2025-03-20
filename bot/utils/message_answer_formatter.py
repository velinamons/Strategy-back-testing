from typing import Dict

from settings import STRATEGIES_CONFIG, PORTFOLIO_CONFIG


def html_format_symbols(symbols_config: Dict) -> str:
    formatted_symbols = ""
    for symbol, intervals in symbols_config.items():
        formatted_symbols += f"📈 <b>{symbol}</b>:\n"
        for interval, date_range in intervals.items():
            formatted_symbols += f"    🔹<i>Interval</i>: {interval}\n"
            formatted_symbols += f"         <i>Start Date</i>: {date_range['start_date']}\n"
            formatted_symbols += f"         <i>End Date</i>: {date_range['end_date']}\n"

        formatted_symbols += "\n"
    return formatted_symbols if formatted_symbols else "No symbols available at the moment."


def html_format_portfolio(portfolio_config: Dict) -> str:
    formatted_portfolio = ""
    for param, param_details in portfolio_config["params"].items():
        formatted_portfolio += f"🔹 <b>{param.replace('_', ' ').capitalize()}</b>:\n"
        formatted_portfolio += f"      {param_details['description']}\n"
        formatted_portfolio += f"      Default: {param_details['default_value']}\n"
    return formatted_portfolio if formatted_portfolio else "No portfolio config available at the moment."


def html_format_strategies(strategies_config: Dict) -> str:
    formatted_strategies = ""
    for strategy_name, strategy_details in strategies_config.items():
        formatted_strategies += f"🎯 <b>{strategy_name.replace('_', '-').upper()} Strategy</b>:\n"
        formatted_strategies += f"       {strategy_details.get('description', 'No description available.')}\n"
        formatted_strategies += f"       <b>Assets</b>: {', '.join(strategy_details['asset_type'])}\n"

        formatted_strategies += "       <b>Parameters</b>:\n"
        for param_name, param_details in strategy_details['params'].items():
            formatted_strategies += f"       🔹 <b>{param_name.replace('_', ' ').capitalize()}</b>:\n"
            formatted_strategies += f"             {param_details['description']}\n"
            formatted_strategies += f"             Default: {param_details['default_value']}\n"

        formatted_strategies += "\n"

    return formatted_strategies if formatted_strategies else "No strategies available at the moment."


def html_format_strategy_params(strategy_name: str) -> str:
    """Formats strategy parameters for display."""
    strategy_details = STRATEGIES_CONFIG[strategy_name]
    formatted_text = f"<b>Strategy:</b> {strategy_name}\n\n"
    formatted_text += "📌 <b>Parameters:</b>\n"

    for param_name, param_details in strategy_details["params"].items():
        formatted_text += f"🔹 <b>{param_name.replace('_', ' ').capitalize()}</b>\n"
        formatted_text += f"   {param_details['description']}\n"
        formatted_text += f"   <i>Default:</i> {param_details['default_value']}\n\n"

    return formatted_text


def html_format_portfolio_params() -> str:
    """Formats portfolio parameters for display."""
    formatted_text = "<b>Portfolio Configuration Parameters:</b>\n\n"

    for param_name, param_details in PORTFOLIO_CONFIG["params"].items():
        formatted_text += f"🔹 <b>{param_name.replace('_', ' ').capitalize()}</b>\n"
        formatted_text += f"   {param_details['description']}\n"
        formatted_text += f"   <i>Default:</i> {param_details['default_value']}\n\n"

    return formatted_text


def html_format_params(params: dict) -> str:
    """Format the parameters into a nice string."""
    return "\n".join([f"<b>{key}:</b> {value}" for key, value in params.items()])
