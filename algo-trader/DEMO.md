# 🎬 Demo - What You'll See

This shows exactly what happens when you run the scripts.

## Running ./setup.sh

```
╔════════════════════════════════════════════════════════════╗
║        Algo Trading Platform - Interactive Setup           ║
╚════════════════════════════════════════════════════════════╝

Step 1: Checking System Requirements
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Python 3.11.5 found
✅ pip found

Step 2: Setting Up Virtual Environment
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Creating virtual environment...
✅ Virtual environment created

Step 3: Installing Dependencies
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Installing Python packages (this may take a few minutes)...
✅ All dependencies installed

Step 4: Zerodha API Configuration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You need Zerodha Kite Connect API credentials.
If you don't have them yet, visit: https://developers.kite.trade/

Do you have Zerodha API credentials ready? (y/N): y

Enter your Zerodha API credentials:

API Key: abc123xyz456
API Secret: secretkey789
Access Token: longaccesstoken123456789

Step 5: Strategy Configuration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Configure your trading strategy parameters:
(Press Enter to use defaults shown in brackets)

Target drop percentage [0.2%]: ⏎
Trailing stop loss delta [0.1%]: ⏎
Maximum concurrent positions [5]: ⏎
Capital per trade (₹) [50000]: ⏎

Step 6: Screener Configuration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Minimum stock price (₹) [50]: ⏎
Maximum stock price (₹) [5000]: ⏎
Minimum daily volume [100000]: ⏎
Top N stocks to suggest [5]: ⏎

Step 7: Saving Configuration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ .env file created
✅ config.py updated

Step 8: Testing Connection
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Testing Zerodha API connection...
✅ Connection successful! Found 1847 NSE instruments

╔════════════════════════════════════════════════════════════╗
║              ✅ Setup Complete!                            ║
╚════════════════════════════════════════════════════════════╝

📋 Your Configuration:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Target drop: 0.2%
  Trailing SL: 0.1%
  Max positions: 5
  Capital per trade: ₹50000
  Stock price range: ₹50 - ₹5000
  Min volume: 100000

🚀 Ready to start!

Run: ./start.sh to launch the application

📚 Next Steps:
  1. Read README.md for usage guide
  2. Check CHECKLIST.md for launch plan
  3. Start with paper trading (simulation mode)
```

---

## Running ./start.sh

```
╔════════════════════════════════════════════════════════════╗
║           Algo Trading Platform - Launcher                 ║
╚════════════════════════════════════════════════════════════╝

✅ Setup verified

Setup completed on: Thu Feb 05 22:45:30 IST 2026

🟢 Market is OPEN

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

Enter your choice (1-9): _
```

---

## Option 1: Stock Screener

```
Enter your choice: 1

🔍 Running Stock Screener...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2026-02-05 10:30:15 - Starting stock screening...
2026-02-05 10:30:16 - Fetched 1847 NSE stocks
2026-02-05 10:30:45 - After basic filters: 342 stocks
2026-02-05 10:31:20 - Top 5 short candidates identified

📊 TOP SHORT CANDIDATES:

symbol      price   volume   technical_score  sentiment_score  combined_score
BAJFINANCE  6845.30  982340        2.0              -0.68            4.88
HDFCBANK    1589.75  5432100       1.5              -0.52            3.72
ICICIBANK    943.20  8765432       1.0              -0.45            3.10
AXISBANK     712.40  3210987       1.5              -0.38            2.88
SBIN         598.35  12345678      1.0              -0.35            2.50

Results saved to data/screener_results_20260205_103120.csv

Press Enter to return to menu...
```

---

## Option 2: Backtest

```
Enter your choice: 2

Enter stock symbol (e.g., RELIANCE): RELIANCE
Number of days to backtest [30]: 10

📊 Backtesting RELIANCE for 10 days...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2026-02-05 10:35:10 - Backtesting RELIANCE from 2026-01-26 to 2026-02-05

📈 BACKTEST RESULTS for RELIANCE:

date        entry_price  exit_price  exit_reason   pnl_percent
2026-01-27     2845.50     2839.81   TARGET_HIT         0.20
2026-01-28     2862.30     2864.16   STOP_LOSS         -0.06
2026-01-29     2858.75     2853.07   TARGET_HIT         0.20
2026-01-30     2871.20     2877.44   EOD_CLOSE         -0.22
2026-02-03     2889.40     2883.51   TARGET_HIT         0.20
2026-02-04     2895.65     2890.05   TARGET_HIT         0.19
2026-02-05     2903.80     2898.22   TARGET_HIT         0.19

📊 PERFORMANCE METRICS:
  total_trades: 7.00
  winning_trades: 5.00
  losing_trades: 2.00
  win_rate: 71.43
  avg_profit: 0.20
  avg_loss: -0.14
  total_pnl: 0.70
  max_profit: 0.20
  max_loss: -0.22
  profit_factor: 1.43

Results saved to data/backtest_RELIANCE_20260205_103542.csv

Press Enter to return to menu...
```

---

## Option 3: Paper Trading

```
Enter your choice: 3

🎮 Starting Paper Trading (Simulation Mode)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 This is SIMULATION mode - No real money involved
   Press Ctrl+C to stop trading

Press Enter to start...

2026-02-05 09:15:02 - [SIMULATION] Short BAJFINANCE: 7 @ 6845.30
2026-02-05 09:15:03 - [SIMULATION] Short HDFCBANK: 31 @ 1589.75
2026-02-05 09:15:04 - [SIMULATION] Short ICICIBANK: 53 @ 943.20
2026-02-05 09:15:05 - [SIMULATION] Short AXISBANK: 70 @ 712.40
2026-02-05 09:15:06 - [SIMULATION] Short SBIN: 83 @ 598.35
2026-02-05 09:15:07 - WebSocket connected. Subscribed to 5 instruments.

🎮 SIMULATION RUNNING...
Press Ctrl+C to stop

[09:15:45] Open: 5 | Closed: 0 | P&L: ₹0.00
[09:16:45] Open: 5 | Closed: 0 | P&L: ₹+234.50
[09:17:45] Open: 5 | Closed: 0 | P&L: ₹+567.80
[09:18:45] Open: 4 | Closed: 1 | P&L: ₹+945.60  ← ICICIBANK hit target
[09:19:45] Open: 4 | Closed: 1 | P&L: ₹+1234.20
...
[15:20:00] Closing all positions (EOD)
[15:20:01] [SIMULATION] Cover BAJFINANCE: 7 @ 6832.10 | TARGET_HIT | P&L: ₹92.40 (0.19%)
[15:20:02] [SIMULATION] Cover HDFCBANK: 31 @ 1583.65 | STOP_LOSS | P&L: ₹-34.10 (-0.07%)

📊 FINAL SUMMARY:
  Total P&L: ₹+1,456.80

Press Enter to return to menu...
```

---

## Option 4: Dashboard

```
Enter your choice: 4

📈 Launching Dashboard...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Opening browser at http://localhost:8501
Press Ctrl+C to stop the server

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.100:8501
```

**Browser opens showing:**
- Interactive screener with charts
- Backtesting interface with P&L graphs
- Live monitoring dashboard
- Beautiful Plotly visualizations

---

## Option 5: Live Trading

```
Enter your choice: 5

╔════════════════════════════════════════════════════════════╗
║                    ⚠️  WARNING ⚠️                           ║
║                                                            ║
║              LIVE TRADING MODE - REAL MONEY                ║
║                                                            ║
║  • Real trades will be executed                            ║
║  • Real money will be at risk                              ║
║  • Short selling = unlimited loss potential                ║
║                                                            ║
║  Only proceed if:                                          ║
║    ✓ You've tested thoroughly in simulation                ║
║    ✓ You understand the strategy completely               ║
║    ✓ You can afford to lose this capital                  ║
║    ✓ You have stop-loss discipline                        ║
╚════════════════════════════════════════════════════════════╝

Have you been profitable in paper trading for 2+ weeks? (y/N): n

⚠️  Not recommended to go live yet.
Continue paper trading until consistently profitable.
```

---

## File Structure After Setup

```
algo-trader/
├── ✅ .setup_complete          ← Setup flag file
├── ✅ .env                      ← Your API credentials
├── ✅ config.py                 ← Updated with your settings
├── ✅ venv/                     ← Virtual environment created
│
├── data/
│   ├── screener_results_*.csv  ← Screener outputs
│   └── backtest_*.csv          ← Backtest results
│
└── logs/
    └── trading.log             ← All activity logged
```

---

## What Each Script Does

### setup.sh
1. ✅ Checks Python/pip installed
2. ✅ Creates venv + installs packages
3. ✅ Prompts for Zerodha credentials
4. ✅ Prompts for strategy parameters
5. ✅ Creates .env file
6. ✅ Updates config.py
7. ✅ Tests API connection
8. ✅ Creates .setup_complete flag

### start.sh
1. ✅ Checks .setup_complete exists
2. ✅ Activates virtual environment
3. ✅ Shows market status (open/closed)
4. ✅ Presents interactive menu
5. ✅ Runs selected option
6. ✅ Returns to menu after completion

---

## Tips

- **First time?** Choose Option 6 (Run Examples) to see everything work
- **Learning?** Try Option 2 (Backtest) on different stocks
- **Testing?** Use Option 3 (Paper Trading) during market hours
- **Visual learner?** Launch Option 4 (Dashboard) for charts
- **Need to change settings?** Option 7 re-runs setup

**Ready to try it?** Run `./setup.sh` now! 🚀
