#!/usr/bin/env python3
"""
Example Usage - Quick examples of using each component
"""

import sys
from datetime import datetime, timedelta
from modules.screener import StockScreener
from modules.backtester import Backtester
from modules.live_executor import LiveExecutor
from modules.zerodha_client import ZerodhaClient

def example_test_connection():
    """Test Zerodha API connection"""
    print("\n=== Testing Zerodha Connection ===")
    
    client = ZerodhaClient()
    instruments = client.get_instruments('NSE')
    
    print(f"✅ Connected! Found {len(instruments)} NSE instruments")
    
    # Test quote
    quote = client.get_quote(['NSE:RELIANCE'])
    if quote:
        reliance = quote['NSE:RELIANCE']
        print(f"RELIANCE: ₹{reliance['last_price']}")

def example_screener():
    """Run stock screener"""
    print("\n=== Running Stock Screener ===")
    
    screener = StockScreener()
    results = screener.screen_stocks(top_n=5)
    
    if len(results) > 0:
        print("\n📊 Top 5 Short Candidates:")
        for idx, row in results.iterrows():
            print(f"  {idx+1}. {row['symbol']}: Score={row['combined_score']:.2f}, "
                  f"Price=₹{row['price']:.2f}, Sentiment={row['sentiment_score']:.2f}")
    else:
        print("No candidates found")
    
    return results

def example_backtest():
    """Backtest a stock"""
    print("\n=== Backtesting RELIANCE ===")
    
    backtester = Backtester()
    
    # Last 10 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=10)
    
    results = backtester.backtest_symbol('RELIANCE', start_date, end_date)
    
    if len(results) > 0:
        metrics = backtester.calculate_metrics(results)
        
        print(f"\n📈 Results:")
        print(f"  Total Trades: {metrics['total_trades']}")
        print(f"  Win Rate: {metrics['win_rate']:.1f}%")
        print(f"  Total P&L: {metrics['total_pnl']:.2f}%")
        print(f"  Profit Factor: {metrics['profit_factor']:.2f}")
        
        print("\nRecent trades:")
        print(results[['date', 'pnl_percent', 'exit_reason']].tail())

def example_paper_trading():
    """Demonstrate paper trading setup"""
    print("\n=== Paper Trading Example ===")
    
    # Initialize executor in simulation mode
    executor = LiveExecutor(simulation_mode=True)
    
    # Enter a few positions
    symbols = ['RELIANCE', 'INFY', 'TCS']
    
    print("Entering short positions:")
    for symbol in symbols:
        success = executor.enter_short_position(symbol)
        if success:
            print(f"  ✅ {symbol}")
    
    # Show portfolio
    summary = executor.get_portfolio_summary()
    print(f"\nPortfolio: {summary['open_positions']} positions open")
    
    print("\n💡 In real usage, this would stream live ticks and manage positions automatically")

def main():
    """Run all examples"""
    print("=" * 50)
    print("Algo Trading Platform - Usage Examples")
    print("=" * 50)
    
    try:
        # Test connection first
        example_test_connection()
        
        # Run screener
        example_screener()
        
        # Backtest
        example_backtest()
        
        # Paper trading demo
        example_paper_trading()
        
        print("\n✅ All examples completed!")
        print("\n📚 Next steps:")
        print("  - Adjust config.py parameters")
        print("  - Run: python main.py simulate")
        print("  - Launch dashboard: streamlit run dashboard.py")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you've:")
        print("  1. Created .env with valid Zerodha credentials")
        print("  2. Installed all dependencies (pip install -r requirements.txt)")
        sys.exit(1)

if __name__ == '__main__':
    main()
