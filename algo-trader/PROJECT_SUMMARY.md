# Project Summary - Algo Trading Platform

## ✅ What's Been Built

A complete algorithmic trading system for short-selling NSE stocks with:

### 1. **Stock Screener** (`modules/screener.py`)
- Fetches all NSE equity stocks via Zerodha API
- Applies volume & price filters
- Analyzes news sentiment using FinBERT (AI model for financial text)
- Calculates technical indicators
- Returns top 5 short candidates

### 2. **Backtesting Engine** (`modules/backtester.py`)
- Fetches historical intraday (minute-level) data
- Simulates your exact strategy:
  - Short at market open
  - Target: 0.2% drop
  - Trailing stop loss: 0.1%
- Calculates performance metrics (win rate, P&L, profit factor)
- Identifies what worked and what didn't

### 3. **Live Trading Executor** (`modules/live_executor.py`)
- **Simulation mode**: Paper trading with virtual money
- **Live mode**: Real trades (with safety confirmations)
- WebSocket tick streaming for real-time price updates
- Automatic trailing stop loss management
- Position tracking and P&L monitoring

### 4. **Dashboard** (`dashboard.py`)
- Streamlit-based web interface
- Visual charts for screening results
- Interactive backtesting with P&L graphs
- Live monitoring (ready for integration)

### 5. **Supporting Infrastructure**
- Zerodha API wrapper (`modules/zerodha_client.py`)
- News & sentiment analyzer (`modules/news_analyzer.py`)
- Configuration management (`config.py`)
- Logging system
- Example scripts

## 📁 Project Structure

```
algo-trader/
├── main.py                    # Main CLI entry point
├── dashboard.py               # Streamlit web dashboard
├── config.py                  # All configuration settings
├── requirements.txt           # Python dependencies
├── .env.example               # Template for API keys
├── .gitignore                 # Git ignore rules
│
├── README.md                  # User documentation
├── SETUP_GUIDE.md            # Zerodha API setup steps
├── PROJECT_SUMMARY.md        # This file
│
├── quickstart.sh             # Automated setup script
├── example_usage.py          # Code examples
│
├── modules/
│   ├── __init__.py
│   ├── zerodha_client.py     # Zerodha API wrapper
│   ├── news_analyzer.py      # FinBERT sentiment analysis
│   ├── screener.py           # Stock screening logic
│   ├── backtester.py         # Historical simulation
│   └── live_executor.py      # Real-time trading engine
│
├── data/                     # Output: CSVs, databases
├── logs/                     # Trading logs
└── strategies/               # Future: custom strategies
```

## 🚀 Quick Start

### Two-Step Launch

```bash
cd algo-trader

# Step 1: Interactive setup (one-time)
./setup.sh

# Step 2: Launch application
./start.sh
```

That's it! The scripts will handle everything.

### What setup.sh Does

- ✅ Checks Python & dependencies
- ✅ Creates virtual environment
- ✅ Installs packages
- ✅ Prompts for Zerodha API credentials
- ✅ Configures strategy parameters
- ✅ Tests connection
- ✅ Creates `.setup_complete` flag

### What start.sh Does

- ✅ Verifies setup complete
- ✅ Shows interactive menu:
  1. Run Stock Screener
  2. Backtest a Stock
  3. Start Paper Trading
  4. Launch Dashboard
  5. Live Trading (with warnings)
  6. Run Examples
  7. Reconfigure
  8. View Documentation
  9. Exit

### Manual Commands (Optional)

You can also run commands directly:

```bash
python main.py screener
python main.py backtest --symbol RELIANCE --days 30
python main.py simulate
streamlit run dashboard.py
```

## 🎯 Your Strategy (Implemented)

**Entry:**
- Screen NSE stocks for bearish signals (news + technicals)
- Short at market open (9:15 AM IST)

**Exit:**
- **Target**: Buy back when price drops 0.2% (profit)
- **Stop Loss**: Buy back if price rises (trailing)
  - Initially: 0.1% above entry
  - Trails down: Always 0.1% above lowest price seen
- **End of Day**: Close all positions at 3:20 PM

**Example Trade:**
```
09:15 AM - Short RELIANCE @ ₹1000
         - Target: ₹998 (0.2% drop)
         - Stop loss: ₹1001 (0.1% rise)

09:30 AM - Price drops to ₹996
         - New stop loss: ₹996.96 (0.1% above ₹996)

09:45 AM - Price hits ₹998
         - Exit! Profit = ₹2 per share (0.2%)
```

## 🔧 Configuration

All settings in `config.py`:

```python
STRATEGY_CONFIG = {
    'target_drop': 0.002,         # 0.2% profit target
    'trailing_delta': 0.001,      # 0.1% trailing stop
    'max_positions': 5,           # Max 5 shorts at once
    'capital_per_trade': 50000,   # ₹50k per position
}
```

Adjust these based on your:
- Risk tolerance
- Capital availability
- Market conditions

## 📊 What Each Mode Does

### `screener`
- Analyzes all NSE stocks
- Outputs: `data/screener_results_YYYYMMDD.csv`
- Use: Find today's best short candidates

### `backtest --symbol XYZ`
- Tests strategy on past data
- Shows: win rate, P&L, trade-by-trade results
- Use: See if strategy would've worked on a stock

### `simulate`
- Runs strategy in real-time with fake money
- Uses: Live market data
- Safe: No real trades executed
- Use: Test before going live

### `live`
- **⚠️ REAL MONEY MODE**
- Executes actual trades
- Use: Only after thorough testing!

## 🛡️ Safety Features

1. **Simulation mode default**: Can't accidentally trade real money
2. **Explicit confirmation**: Live mode requires typing a warning
3. **Trailing stop loss**: Limits losses automatically
4. **Position limits**: Max 5 concurrent shorts
5. **End-of-day close**: All positions auto-closed
6. **Logging**: Every action logged to `logs/trading.log`

## 📈 Next Enhancements

**Phase 2 (Your Next Steps):**
1. Integrate real news APIs (currently placeholder)
2. Add more technical indicators (RSI, MACD, Bollinger Bands)
3. Build database to track all trades
4. Add Telegram alerts for trade notifications
5. Implement risk management (max drawdown, daily loss limits)

**Phase 3 (Advanced):**
1. Multiple strategies (not just shorting)
2. Machine learning for stock selection
3. Options trading support
4. Multi-timeframe analysis
5. Auto-rebalancing

## 📚 Documentation

- **README.md**: User guide for running the system
- **SETUP_GUIDE.md**: Step-by-step API setup
- **config.py**: All tunable parameters explained
- **Code comments**: Each module is documented

## ⚠️ Important Reminders

### Regulatory
- Ensure SEBI compliance for algo trading
- Some brokers require approval for algo trading
- Keep records of all trades

### Risk Management
- **Short selling = unlimited loss potential**
- Always use stop losses (already implemented)
- Start with small capital
- Don't risk more than 2% per trade
- Test thoroughly before going live

### Technical
- Zerodha access tokens expire daily (need refresh)
- Market hours: 9:15 AM - 3:30 PM IST
- Rate limits: Don't spam API (delays added)
- MIS positions auto-square at 3:20 PM

## 🎓 Learning Resources

- Zerodha Kite Connect Docs: https://kite.trade/docs/
- Algorithmic Trading: Read books on quant trading
- Technical Analysis: Understanding indicators
- Risk Management: Position sizing, Kelly Criterion

## 🐛 Troubleshooting

**"Token invalid"**
→ Regenerate access token (see SETUP_GUIDE.md)

**"No stocks found"**
→ Adjust screener filters in config.py

**"Connection timeout"**
→ Check internet, Zerodha API status

**Need help?**
→ Check `logs/trading.log` for detailed errors

## 📞 Support

- Zerodha Support: https://support.zerodha.com
- Kite Connect: https://kite.trade

---

**Built with:** Python, Zerodha API, FinBERT, Streamlit  
**License:** MIT  
**Use at your own risk** - This is for educational purposes

**Ready to start?** Run `./quickstart.sh` and follow the prompts!
