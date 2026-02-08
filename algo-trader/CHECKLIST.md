# 🚀 Getting Started Checklist

Work through this checklist to get your algo trading platform running.

## Phase 1: Setup (30 minutes)

### 1. Get Zerodha API Access
- [ ] Create account at https://developers.kite.trade/
- [ ] Create a new app
- [ ] Note down API Key
- [ ] Note down API Secret
- [ ] Generate access token (see SETUP_GUIDE.md)

### 2. Run Interactive Setup
- [ ] Navigate to project: `cd algo-trader`
- [ ] Run: `./setup.sh`
- [ ] Enter your Zerodha credentials when prompted
- [ ] Configure strategy parameters (or use defaults)
- [ ] Verify connection test passes
- [ ] Confirm setup complete message

### 3. Launch Application
- [ ] Run: `./start.sh`
- [ ] Select option 6 (Run Examples)
- [ ] Verify all examples work
- [ ] Familiarize yourself with the menu

## Phase 2: Understand the System (1 hour)

### 4. Run Stock Screener
- [ ] Run: `./start.sh` → Select option 1
- [ ] Review top 5 candidates in terminal
- [ ] Check output file in `data/`
- [ ] Understand scoring logic

### 5. Backtest on Historical Data
- [ ] Run: `./start.sh` → Select option 2
- [ ] Test RELIANCE for 30 days
- [ ] Analyze win rate and P&L
- [ ] Examine trade-by-trade results
- [ ] Try different symbols (INFY, TCS, HDFC)
- [ ] Adjust parameters: `./start.sh` → option 7 (Reconfigure)

### 6. Explore Dashboard
- [ ] Run: `./start.sh` → Select option 4
- [ ] Open browser to localhost:8501
- [ ] Run screener from UI
- [ ] Try backtesting different stocks
- [ ] Familiarize yourself with charts

## Phase 3: Paper Trading (Week 1)

### 7. Simulation Mode
- [ ] Read live_executor.py to understand logic
- [ ] Run: `./start.sh` → Select option 3 (during market hours)
- [ ] Monitor positions in terminal
- [ ] Watch trailing stop loss adjust
- [ ] Let it run for full trading day
- [ ] Review end-of-day results

### 8. Refine Strategy
- [ ] Run: `./start.sh` → option 7 (Reconfigure)
- [ ] Try different target_drop (0.15%, 0.25%, 0.3%)
- [ ] Try different trailing_delta (0.05%, 0.15%, 0.2%)
- [ ] Adjust capital per trade
- [ ] Backtest each configuration
- [ ] Find optimal parameters for your risk tolerance

### 9. Monitor & Log
- [ ] Check `logs/trading.log` daily
- [ ] Review all simulated trades
- [ ] Calculate overall P&L
- [ ] Track what worked and what didn't
- [ ] Document lessons learned

## Phase 4: Preparation for Live (Week 2+)

### 10. Risk Management
- [ ] Set maximum daily loss limit
- [ ] Decide capital allocation (never use full account)
- [ ] Plan position sizing
- [ ] Set max concurrent positions
- [ ] Define when to stop trading (drawdown limits)

### 11. System Checks
- [ ] Test internet stability
- [ ] Set up backup internet connection
- [ ] Verify API token refresh process
- [ ] Create monitoring dashboard
- [ ] Set up phone alerts (optional)

### 12. Paper Trade for 2+ Weeks
- [ ] Run simulation daily
- [ ] Track every metric
- [ ] Achieve consistent profitability
- [ ] Verify strategy edge
- [ ] Build confidence in system

## Phase 5: Going Live (Only When Ready!)

### 13. Pre-Live Checklist
- [ ] ✅ Profitable in simulation for 2+ weeks
- [ ] ✅ Understand every line of code
- [ ] ✅ Can explain strategy to someone else
- [ ] ✅ Have stop-loss rules
- [ ] ✅ Know when to pause trading
- [ ] ✅ Capital you can afford to lose
- [ ] ✅ Emotionally prepared for losses
- [ ] ✅ Broker account has sufficient margin

### 14. Start Small
- [ ] Allocate minimal capital (₹10-20k to start)
- [ ] Trade 1-2 positions max initially
- [ ] Monitor EVERY trade closely
- [ ] Keep detailed records
- [ ] Compare live vs simulation results

### 15. Scale Gradually
- [ ] If profitable for 1 week → increase capital slightly
- [ ] If losing → stop and analyze
- [ ] Never chase losses
- [ ] Stick to your plan
- [ ] Journal every decision

## 🎯 Success Criteria

**Before going live, you should:**
1. Understand the code completely
2. Have profitable backtest results
3. Profitable paper trading for 2+ weeks
4. Clear risk management rules
5. Emotional discipline
6. Capital you can lose without stress

## ⚠️ Warning Signs - STOP TRADING If:

- Multiple consecutive losses
- Daily loss exceeds limit
- Strategy stops working
- Can't focus / emotional
- System errors / bugs
- API connection issues
- Margin calls

## 📊 Metrics to Track

Create a spreadsheet to track:
- [ ] Daily P&L
- [ ] Win rate
- [ ] Average win/loss
- [ ] Max drawdown
- [ ] Number of trades
- [ ] Strategy adjustments made
- [ ] Market conditions

## 🎓 Continuous Learning

- [ ] Read trading psychology books
- [ ] Study successful algo traders
- [ ] Join trading communities
- [ ] Review trades weekly
- [ ] Keep improving strategy

## 📝 Notes Section

*Use this space for your own notes:*

**My Strategy Tweaks:**
- 

**Observations:**
- 

**Questions:**
- 

**Issues Encountered:**
- 

---

**Remember:** The goal isn't to get rich quick. It's to build a sustainable, profitable system through testing, learning, and discipline.

**Current Status:** [ ] Setup | [ ] Testing | [ ] Paper Trading | [ ] Live Trading

**Last Updated:** _______________
