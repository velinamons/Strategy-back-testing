# Strategy Backtesting Bot

## Overview
Strategy Backtesting Bot is a trading strategy testing framework that allows you to backtest various trading strategies using historical market data. It supports multiple asset types, configurable parameters, and Telegram bot integration for interactive backtesting.

## Features
- Supports multiple strategies (SMA-RSI, MACD, Bollinger Bands, Stochastic, ATR Breakout)
- Multi-asset and single-asset trading
- Configurable portfolio settings (initial cash, fees, slippage, stop-loss, take-profit)
- Historical data fetching and storage in Parquet format
- Backtest result visualization and CSV export
- Telegram bot integration for remote testing and monitoring

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/velinamons/Strategy-back-testing.git
   cd Strategy-back-testing
   ```
2. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Create a `.env` file based on the `.env.sample` provided (get tg token using @BotFather):
   ```sh
   cp .env.sample .env
   ```
4. Modify `config.json` to specify symbols and timeframes to preload:
   ```sh
   {
       "symbols": {
           "BTCUSDT": {
               "30m": {"start_date": "2024-01-01", "end_date": "2025-01-01"},
               "1h": {"start_date": "2024-01-01", "end_date": "2025-01-01"}
           }
       },
       ...
   }
   ```

## Running the Project

1. Start the backtesting system:
   ```sh
   python main.py
   ```
2. Wait for historical data to load.
3. Interact with the Telegram bot to trigger backtests and retrieve results using commands and by following instructions:


## General Commands

### `/start`
- **Description:** Starts the bot and shows the main menu.

### `/symbols`
- **Description:** Lists available trading symbols.

### `/portfolio`
- **Description:** Displays portfolio configuration.

### `/strategies`
- **Description:** Shows available backtesting strategies.

## Backtest Commands

### `/start_single_asset_backtest`
- **Description:** Starts a single asset backtest by selecting a symbol.

### `/start_multi_asset_backtest`
- **Description:** Starts a multi-asset backtest by selecting multiple symbols.


## Strategies Implemented

### 1. SMA-RSI Strategy
- Combines Simple Moving Average (SMA) and Relative Strength Index (RSI) for trade signals.
- Parameters: `short_window`, `long_window`, `rsi_window`, `rsi_buy`, `rsi_sell`

### 2. MACD Strategy
- Uses Moving Average Convergence Divergence (MACD) crossovers to generate trade signals.
- Parameters: `short_window`, `long_window`, `signal_window`

### 3. Bollinger Bands Strategy
- Generates buy/sell signals based on price crossing Bollinger Bands.
- Parameters: `window`, `num_std`

### 4. Stochastic Strategy
- Uses the Stochastic Oscillator to identify overbought and oversold conditions.
- Parameters: `k_window`, `d_window`, `stoch_buy`, `stoch_sell`

### 5. ATR Breakout Strategy
- Identifies breakouts and trends using the Average True Range (ATR).
- Parameters: `atr_window`, `atr_multiplier`

## Configuration

Modify `config.json` to:
- Define symbols and timeframes for data fetching.
- Adjust portfolio parameters (fees, slippage, stop-loss, take-profit).
- Enable or disable specific strategies.

Modify `.env` to:
- Set environment variables (log level, data storage paths, Telegram token, etc.).

## Results
Backtest results are stored in the `backtest_results/` directory:
- **CSV files**: Detailed trade history and performance metrics.
- **PNG files**: Visual representations of backtest performance.

