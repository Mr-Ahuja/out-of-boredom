# Algo Trading Platform

A complete algorithmic trading system for short-selling NSE stocks using Zerodha API.

## Features

✅ **Stock Screener** - Identifies top 5 short candidates based on:
- NSE news sentiment analysis (FinBERT)
- Technical indicators
- Volume and price filters

✅ **Backtesting Engine** - Test strategies on historical data with:
- Intraday minute-level data
- Trailing stop-loss simulation
- Performance metrics (win rate, P&L, profit factor)

✅ **Live Executor** - Execute trades in real-time:
- Simulation mode (paper trading)
- Live mode (real trades)
- WebSocket tick streaming
- Automatic trailing stop-loss

## Strategy

**Short Selling with Trailing Stop Loss:**

1. Enter short position at market open
2. Target: 0.2% drop from entry price
3. Trailing stop loss: 0.1% above the lowest price seen
4. Close all positions at end of day

Example:
- Short at ₹100
- Target: ₹99.80 (0.2% drop)
- Initial stop loss: ₹100.10
- If price drops to ₹99.50, new stop loss: ₹99.60 (0.1% trailing)

## Setup

### Quick Start (Recommended)

```bash
cd algo-trader

# Step 1: Run interactive setup
./setup.sh

# Step 2: Launch the application
./start.sh
```

The `setup.sh` script will:
- Check system requirements
- Install all dependencies
- Prompt for your Zerodha API credentials
- Configure strategy parameters
- Test the connection
- Set up the environment

### Manual Setup (Advanced)

If you prefer manual setup:

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Keys**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Create Required Directories**
   ```bash
   mkdir -p data logs
   ```

**Getting Zerodha Access Token:**
See `SETUP_GUIDE.md` for detailed instructions

## Usage

### Using the Launcher (Easiest)

```bash
./start.sh
```

This opens an interactive menu with all options:
- 🔍 Run Stock Screener
- 📊 Backtest a Stock
- 🎮 Start Paper Trading
- 📈 Launch Dashboard
- 🔴 Live Trading (with safety checks)

### Direct Commands (Advanced)

**Run Stock Screener:**
```bash
python main.py screener
```

**Backtest Strategy:**
```bash
python main.py backtest --symbol RELIANCE --days 30
```

**Paper Trading (Simulation):**
```bash
python main.py simulate
```

**Live Trading ⚠️:**
```bash
python main.py live
```

**Launch Dashboard:**
```bash
streamlit run dashboard.py
```

## Configuration

Edit `config.py` to adjust:

```python
STRATEGY_CONFIG = {
    'target_drop': 0.002,        # 0.2% target
    'trailing_delta': 0.001,     # 0.1% trailing SL
    'max_positions': 5,          # Max concurrent shorts
    'capital_per_trade': 50000,  # ₹50k per position
}

SCREENER_CONFIG = {
    'min_volume': 100000,
    'min_price': 50,
    'max_price': 5000,
    'bearish_sentiment_threshold': -0.3,
    'top_n_stocks': 5,
}
```

## Project Structure

```
algo-trader/
├── main.py                 # Entry point
├── config.py               # Configuration
├── requirements.txt        # Dependencies
├── .env                    # API credentials (create this)
│
├── modules/
│   ├── zerodha_client.py   # Zerodha API wrapper
│   ├── news_analyzer.py    # Sentiment analysis
│   ├── screener.py         # Stock screener
│   ├── backtester.py       # Backtesting engine
│   └── live_executor.py    # Live trading
│
├── data/                   # Results, historical data
├── logs/                   # Trading logs
└── strategies/             # Custom strategies (future)
```

## Next Steps

1. **Enhance News Fetching**: Integrate proper news APIs (NewsAPI, MoneyControl)
2. **More Technical Indicators**: Add RSI, MACD, Bollinger Bands
3. **Risk Management**: Position sizing, max drawdown limits
4. **Dashboard**: Build Streamlit UI for monitoring
5. **Alerts**: Telegram/WhatsApp notifications
6. **Database**: Store all trades in PostgreSQL
7. **Multi-timeframe**: Support different intervals

## Risks & Disclaimers

⚠️ **Important:**
- Short selling has **unlimited loss potential**
- Always use stop losses
- Start with paper trading
- Never risk more than you can afford to lose
- This is for educational purposes
- Consult a financial advisor
- Ensure SEBI compliance for algo trading

## License

MIT

---

**Questions?** Check logs in `logs/trading.log` for debugging.
