import pandas as pd
import logging
from datetime import datetime, timedelta
from modules.zerodha_client import ZerodhaClient
from config import STRATEGY_CONFIG

logger = logging.getLogger(__name__)

class Backtester:
    """Backtest the short strategy on historical data"""
    
    def __init__(self):
        self.zerodha = ZerodhaClient()
        self.target_drop = STRATEGY_CONFIG['target_drop']
        self.trailing_delta = STRATEGY_CONFIG['trailing_delta']
    
    def fetch_intraday_data(self, symbol, date, interval='minute'):
        """Fetch minute-level data for a specific date"""
        try:
            # Get instrument token
            instruments = self.zerodha.get_instruments('NSE')
            instrument = next((i for i in instruments if i['tradingsymbol'] == symbol), None)
            
            if not instrument:
                logger.error(f"Instrument {symbol} not found")
                return None
            
            token = instrument['instrument_token']
            
            # Fetch historical data
            from_date = datetime.combine(date, datetime.min.time())
            to_date = datetime.combine(date, datetime.max.time())
            
            data = self.zerodha.get_historical_data(
                instrument_token=token,
                from_date=from_date,
                to_date=to_date,
                interval=interval
            )
            
            df = pd.DataFrame(data)
            return df
        
        except Exception as e:
            logger.error(f"Error fetching intraday data for {symbol}: {e}")
            return None
    
    def simulate_trade(self, df, entry_price):
        """
        Simulate a single trade with trailing stop loss
        
        Strategy:
        - Short at entry_price (market open)
        - Target: 0.2% drop from entry
        - Trailing stop loss: 0.1% above current low
        """
        if df is None or len(df) == 0:
            return None
        
        target_price = entry_price * (1 - self.target_drop)
        current_stop_loss = entry_price * (1 + self.trailing_delta)
        lowest_price_seen = entry_price
        
        trade_result = {
            'entry_price': entry_price,
            'exit_price': None,
            'exit_time': None,
            'exit_reason': None,
            'pnl_percent': 0,
            'max_profit_percent': 0
        }
        
        for idx, row in df.iterrows():
            current_price = row['close']
            current_low = row['low']
            current_high = row['high']
            current_time = row['date']
            
            # Update lowest price seen
            if current_low < lowest_price_seen:
                lowest_price_seen = current_low
                # Update trailing stop loss
                current_stop_loss = lowest_price_seen * (1 + self.trailing_delta)
            
            # Check if target hit
            if current_low <= target_price:
                trade_result['exit_price'] = target_price
                trade_result['exit_time'] = current_time
                trade_result['exit_reason'] = 'TARGET_HIT'
                trade_result['pnl_percent'] = ((entry_price - target_price) / entry_price) * 100
                break
            
            # Check if stop loss hit
            if current_high >= current_stop_loss:
                trade_result['exit_price'] = current_stop_loss
                trade_result['exit_time'] = current_time
                trade_result['exit_reason'] = 'STOP_LOSS'
                trade_result['pnl_percent'] = ((entry_price - current_stop_loss) / entry_price) * 100
                break
            
            # Track max profit
            max_profit = ((entry_price - current_low) / entry_price) * 100
            if max_profit > trade_result['max_profit_percent']:
                trade_result['max_profit_percent'] = max_profit
        
        # If no exit, close at end of day
        if trade_result['exit_price'] is None:
            last_row = df.iloc[-1]
            trade_result['exit_price'] = last_row['close']
            trade_result['exit_time'] = last_row['date']
            trade_result['exit_reason'] = 'EOD_CLOSE'
            trade_result['pnl_percent'] = ((entry_price - last_row['close']) / entry_price) * 100
        
        return trade_result
    
    def backtest_symbol(self, symbol, start_date, end_date):
        """Backtest strategy on a symbol over a date range"""
        logger.info(f"Backtesting {symbol} from {start_date} to {end_date}")
        
        results = []
        current_date = start_date
        
        while current_date <= end_date:
            # Skip weekends
            if current_date.weekday() >= 5:
                current_date += timedelta(days=1)
                continue
            
            # Fetch intraday data
            df = self.fetch_intraday_data(symbol, current_date)
            
            if df is not None and len(df) > 0:
                # Entry price is the open of the day
                entry_price = df.iloc[0]['open']
                
                # Simulate trade
                trade = self.simulate_trade(df, entry_price)
                
                if trade:
                    trade['date'] = current_date
                    trade['symbol'] = symbol
                    results.append(trade)
            
            current_date += timedelta(days=1)
        
        return pd.DataFrame(results)
    
    def calculate_metrics(self, results_df):
        """Calculate performance metrics"""
        if len(results_df) == 0:
            return {}
        
        total_trades = len(results_df)
        winning_trades = len(results_df[results_df['pnl_percent'] > 0])
        losing_trades = len(results_df[results_df['pnl_percent'] < 0])
        
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        
        avg_profit = results_df[results_df['pnl_percent'] > 0]['pnl_percent'].mean() if winning_trades > 0 else 0
        avg_loss = results_df[results_df['pnl_percent'] < 0]['pnl_percent'].mean() if losing_trades > 0 else 0
        
        total_pnl = results_df['pnl_percent'].sum()
        max_profit = results_df['pnl_percent'].max()
        max_loss = results_df['pnl_percent'].min()
        
        metrics = {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'avg_profit': avg_profit,
            'avg_loss': avg_loss,
            'total_pnl': total_pnl,
            'max_profit': max_profit,
            'max_loss': max_loss,
            'profit_factor': abs(avg_profit / avg_loss) if avg_loss != 0 else 0
        }
        
        return metrics
