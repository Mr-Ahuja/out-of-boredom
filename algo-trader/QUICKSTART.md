# ⚡ Quick Start Guide

Get up and running in 5 minutes!

## Step 1: Get API Credentials (5 minutes)

Before running setup, get your Zerodha API access:

1. Visit: https://developers.kite.trade/
2. Sign up / Log in with your Zerodha account
3. Click "Create New App"
4. Fill in:
   - **App Name**: AlgoTrader (or anything)
   - **Redirect URL**: `http://127.0.0.1:5000`
   - **Description**: My algo trading platform
5. Submit and save:
   - **API Key** (e.g., `abc123xyz`)
   - **API Secret** (e.g., `secret456def`)

6. Generate access token:
   ```python
   # Run this in Python:
   from kiteconnect import KiteConnect
   
   kite = KiteConnect(api_key="your_api_key")
   print(kite.login_url())
   
   # Visit the URL, login, copy request_token from redirect URL
   data = kite.generate_session("request_token", api_secret="your_secret")
   print(f"Access Token: {data['access_token']}")
   ```

Keep these 3 values handy:
- ✅ API Key
- ✅ API Secret  
- ✅ Access Token

## Step 2: Run Setup (2 minutes)

```bash
cd algo-trader
./setup.sh
```

The script will ask you:

**Zerodha Credentials:**
- API Key: `[paste your key]`
- API Secret: `[paste your secret]`
- Access Token: `[paste your token]`

**Strategy Settings** (or press Enter for defaults):
- Target drop: `0.2%`
- Trailing stop: `0.1%`
- Max positions: `5`
- Capital per trade: `50000`

**Stock Filters** (or press Enter for defaults):
- Min price: `50`
- Max price: `5000`
- Min volume: `100000`

Setup will test your connection and confirm everything works.

## Step 3: Launch! (30 seconds)

```bash
./start.sh
```

You'll see this menu:

```
╔════════════════════════════════════════════════════════════╗
║           Algo Trading Platform - Launcher                 ║
╚════════════════════════════════════════════════════════════╝

✅ Setup verified
Setup completed on: [date]

🟢 Market is OPEN  (or 🔴 CLOSED)

Select an option:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  1) 🔍 Run Stock Screener
  2) 📊 Backtest a Stock
  3) 🎮 Start Paper Trading (Simulation)
  4) 📈 Launch Dashboard (Web UI)
  5) 🔴 Live Trading (Real Money) ⚠️
  6) 🧪 Run Examples
  7) ⚙️  Reconfigure (Re-run Setup)
  8) 📚 View Documentation
  9) 🚪 Exit
```

## Your First Actions

### Try the Screener (Option 1)

Finds today's top 5 short candidates:

```
Enter your choice: 1
```

You'll see stocks ranked by bearish sentiment + technicals.

### Backtest a Stock (Option 2)

Test the strategy on past data:

```
Enter your choice: 2
Enter stock symbol: RELIANCE
Number of days: 30
```

Shows win rate, P&L, and trade-by-trade results.

### Launch Dashboard (Option 4)

Visual web interface at http://localhost:8501:

```
Enter your choice: 4
```

Beautiful charts, interactive backtesting, and monitoring.

### Run Examples (Option 6)

See code in action:

```
Enter your choice: 6
```

Tests connection, runs screener, backtests, demos paper trading.

## Next: Paper Trading

During market hours (9:15 AM - 3:30 PM IST):

```
./start.sh → Option 3
```

This runs your strategy in **simulation mode**:
- ✅ Uses real market data
- ✅ Executes your logic
- ✅ No real money at risk

Watch it:
- Short stocks at market open
- Trail stop losses
- Hit targets or stops
- Close positions at EOD

Run this for **2+ weeks** before considering live trading.

## Troubleshooting

**"Token is invalid"**
→ Access tokens expire daily. Re-run setup or regenerate token.

**"Connection failed"**
→ Check your internet and API credentials.

**"Setup not completed"**
→ Run `./setup.sh` first.

**Need to change settings?**
→ `./start.sh` → Option 7 (Reconfigure)

## What's Next?

1. **Week 1**: Backtest multiple stocks, understand the strategy
2. **Week 2-3**: Paper trade daily, track results
3. **Week 4+**: If profitable → consider small live trades

Follow `CHECKLIST.md` for the full roadmap.

## Commands Reference

```bash
# Setup (one-time)
./setup.sh

# Launch application
./start.sh

# Or run directly:
python main.py screener
python main.py backtest --symbol RELIANCE --days 30
python main.py simulate
streamlit run dashboard.py
```

---

**⚠️ Important**: Always start with paper trading. Never risk money you can't afford to lose. Short selling has unlimited loss potential.

**Ready?** Run `./setup.sh` now! 🚀
