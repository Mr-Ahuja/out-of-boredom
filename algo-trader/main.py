#!/usr/bin/env python3
"""
Algo Trading Platform - Main Entry Point

Modes:
1. screener - Run stock screener
2. backtest - Backtest strategy on historical data
3. simulate - Run live simulation (paper trading)
4. live - Execute real trades (⚠️ USE WITH CAUTION)
"""

import argparse
import logging
from datetime import datetime, timedelta
from modules.screener import StockScreener
from modules.backtester import Backtester
from modules.live_executor import LiveExecutor
import sys

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/trading.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def run_screener():
    """Run stock screener and display top candidates"""
    logger.info("=" * 50)
    logger.info("RUNNING STOCK SCREENER")
    logger.info("=" * 50)
    
    screener = StockScreener()
    top_stocks = screener.screen_stocks()
    
    if len(top_stocks) > 0:
        print("\n📊 TOP SHORT CANDIDATES:")
        print(top_stocks.to_string(index=False))
        
        # Save to CSV
        filename = f"data/screener_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        top_stocks.to_csv(filename, index=False)
        logger.info(f"Results saved to {filename}")
    else:
        print("\n⚠️ No stocks met the criteria today")

def run_backtest(symbol, days=30):
    """Backtest strategy on a symbol"""
    logger.info("=" * 50)
    logger.info(f"BACKTESTING {symbol}")
    logger.info("=" * 50)
    
    backtester = Backtester()
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    results = backtester.backtest_symbol(symbol, start_date, end_date)
    
    if len(results) > 0:
        print(f"\n📈 BACKTEST RESULTS for {symbol}:")
        print(results[['date', 'entry_price', 'exit_price', 'exit_reason', 'pnl_percent']].to_string(index=False))
        
        metrics = backtester.calculate_metrics(results)
        print("\n📊 PERFORMANCE METRICS:")
        for key, value in metrics.items():
            print(f"  {key}: {value:.2f}")
        
        # Save results
        filename = f"data/backtest_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        results.to_csv(filename, index=False)
        logger.info(f"Results saved to {filename}")
    else:
        print(f"\n⚠️ No trades executed for {symbol}")

def run_simulation(symbols=None):
    """Run live simulation (paper trading)"""
    logger.info("=" * 50)
    logger.info("STARTING SIMULATION MODE")
    logger.info("=" * 50)
    
    if not symbols:
        # Run screener first
        screener = StockScreener()
        top_stocks = screener.screen_stocks()
        symbols = top_stocks['symbol'].tolist()
    
    if not symbols:
        logger.error("No symbols to trade")
        return
    
    executor = LiveExecutor(simulation_mode=True)
    
    # Enter short positions for all symbols
    for symbol in symbols:
        executor.enter_short_position(symbol)
    
    # Start tick streaming
    logger.info(f"Starting tick stream for {len(symbols)} symbols...")
    executor.start_tick_stream(symbols)
    
    print("\n🎮 SIMULATION RUNNING...")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            import time
            time.sleep(10)
            
            # Show portfolio summary every 10 seconds
            summary = executor.get_portfolio_summary()
            print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                  f"Open: {summary['open_positions']} | "
                  f"Closed: {summary['closed_positions']} | "
                  f"P&L: ₹{summary['total_pnl']:.2f}")
    
    except KeyboardInterrupt:
        logger.info("Stopping simulation...")
        executor.close_all_positions_eod()
        
        final_summary = executor.get_portfolio_summary()
        print("\n📊 FINAL SUMMARY:")
        print(f"  Total P&L: ₹{final_summary['total_pnl']:.2f}")

def run_live(symbols=None):
    """⚠️ Execute REAL trades - USE WITH EXTREME CAUTION"""
    print("\n" + "=" * 50)
    print("⚠️  LIVE TRADING MODE ⚠️")
    print("=" * 50)
    print("\nThis will execute REAL trades with REAL money!")
    confirm = input("Type 'YES I UNDERSTAND THE RISKS' to proceed: ")
    
    if confirm != "YES I UNDERSTAND THE RISKS":
        print("Live trading cancelled.")
        return
    
    logger.warning("LIVE TRADING MODE ACTIVATED")
    
    # Same as simulation but with simulation_mode=False
    executor = LiveExecutor(simulation_mode=False)
    
    # ... rest of the logic similar to run_simulation()
    print("\n🔴 LIVE TRADING - Not fully implemented yet")
    print("Complete the integration and add safety checks before using!")

def main():
    parser = argparse.ArgumentParser(description='Algo Trading Platform')
    parser.add_argument('mode', choices=['screener', 'backtest', 'simulate', 'live'],
                       help='Mode to run')
    parser.add_argument('--symbol', help='Stock symbol (for backtest)')
    parser.add_argument('--symbols', nargs='+', help='List of symbols (for simulate/live)')
    parser.add_argument('--days', type=int, default=30, help='Days to backtest (default: 30)')
    
    args = parser.parse_args()
    
    if args.mode == 'screener':
        run_screener()
    
    elif args.mode == 'backtest':
        if not args.symbol:
            print("Error: --symbol required for backtest mode")
            sys.exit(1)
        run_backtest(args.symbol, args.days)
    
    elif args.mode == 'simulate':
        run_simulation(args.symbols)
    
    elif args.mode == 'live':
        run_live(args.symbols)

if __name__ == '__main__':
    main()
