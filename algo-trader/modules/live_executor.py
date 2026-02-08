import logging
from datetime import datetime
from modules.zerodha_client import ZerodhaClient
from config import STRATEGY_CONFIG
import time
import threading

logger = logging.getLogger(__name__)

class LiveExecutor:
    """Execute trades in real-time or simulation mode"""
    
    def __init__(self, simulation_mode=True):
        self.zerodha = ZerodhaClient()
        self.simulation_mode = simulation_mode
        self.active_positions = {}  # symbol -> position_data
        self.target_drop = STRATEGY_CONFIG['target_drop']
        self.trailing_delta = STRATEGY_CONFIG['trailing_delta']
        self.capital_per_trade = STRATEGY_CONFIG['capital_per_trade']
        
        logger.info(f"LiveExecutor initialized (simulation={simulation_mode})")
    
    def enter_short_position(self, symbol, price=None):
        """
        Enter a short position at market open
        
        In simulation: track virtually
        In live mode: place actual SELL order
        """
        if symbol in self.active_positions:
            logger.warning(f"{symbol} already has an active position")
            return False
        
        # Get current quote
        quote = self.zerodha.get_quote([f"NSE:{symbol}"])
        if not quote:
            logger.error(f"Could not get quote for {symbol}")
            return False
        
        entry_price = price if price else quote[f"NSE:{symbol}"]['last_price']
        quantity = int(self.capital_per_trade / entry_price)
        
        if self.simulation_mode:
            # Simulated trade
            order_id = f"SIM_{symbol}_{int(time.time())}"
            logger.info(f"[SIMULATION] Short {symbol}: {quantity} @ {entry_price}")
        else:
            # Real trade
            order_id = self.zerodha.place_order(
                tradingsymbol=symbol,
                transaction_type='SELL',
                quantity=quantity,
                order_type='MARKET',
                product='MIS'
            )
            
            if not order_id:
                logger.error(f"Failed to place order for {symbol}")
                return False
            
            logger.info(f"[LIVE] Short {symbol}: {quantity} @ {entry_price}, Order: {order_id}")
        
        # Track position
        target_price = entry_price * (1 - self.target_drop)
        stop_loss = entry_price * (1 + self.trailing_delta)
        
        self.active_positions[symbol] = {
            'entry_price': entry_price,
            'entry_time': datetime.now(),
            'quantity': quantity,
            'target_price': target_price,
            'stop_loss': stop_loss,
            'lowest_price_seen': entry_price,
            'order_id': order_id,
            'status': 'OPEN'
        }
        
        return True
    
    def update_position(self, symbol, current_price):
        """Update position based on current tick price"""
        if symbol not in self.active_positions:
            return
        
        position = self.active_positions[symbol]
        
        if position['status'] != 'OPEN':
            return
        
        # Update trailing stop loss
        if current_price < position['lowest_price_seen']:
            position['lowest_price_seen'] = current_price
            new_stop_loss = current_price * (1 + self.trailing_delta)
            position['stop_loss'] = new_stop_loss
            logger.debug(f"{symbol}: New trailing stop loss @ {new_stop_loss:.2f}")
        
        # Check if target hit
        if current_price <= position['target_price']:
            self.exit_position(symbol, position['target_price'], 'TARGET_HIT')
            return
        
        # Check if stop loss hit
        if current_price >= position['stop_loss']:
            self.exit_position(symbol, position['stop_loss'], 'STOP_LOSS')
            return
    
    def exit_position(self, symbol, exit_price, reason):
        """
        Exit a position
        
        In simulation: log the exit
        In live mode: place BUY order to cover short
        """
        if symbol not in self.active_positions:
            logger.warning(f"No active position for {symbol}")
            return
        
        position = self.active_positions[symbol]
        quantity = position['quantity']
        entry_price = position['entry_price']
        
        pnl_percent = ((entry_price - exit_price) / entry_price) * 100
        pnl_amount = (entry_price - exit_price) * quantity
        
        if self.simulation_mode:
            logger.info(
                f"[SIMULATION] Cover {symbol}: {quantity} @ {exit_price} | "
                f"Reason: {reason} | P&L: ₹{pnl_amount:.2f} ({pnl_percent:.2f}%)"
            )
        else:
            # Place BUY order to cover
            order_id = self.zerodha.place_order(
                tradingsymbol=symbol,
                transaction_type='BUY',
                quantity=quantity,
                order_type='MARKET',
                product='MIS'
            )
            
            logger.info(
                f"[LIVE] Cover {symbol}: {quantity} @ {exit_price} | "
                f"Reason: {reason} | P&L: ₹{pnl_amount:.2f} ({pnl_percent:.2f}%) | "
                f"Order: {order_id}"
            )
        
        # Mark position as closed
        position['status'] = 'CLOSED'
        position['exit_price'] = exit_price
        position['exit_time'] = datetime.now()
        position['exit_reason'] = reason
        position['pnl_percent'] = pnl_percent
        position['pnl_amount'] = pnl_amount
    
    def start_tick_stream(self, symbols):
        """Start live tick streaming for active positions"""
        instruments = self.zerodha.get_instruments('NSE')
        tokens = []
        
        for symbol in symbols:
            inst = next((i for i in instruments if i['tradingsymbol'] == symbol), None)
            if inst:
                tokens.append(inst['instrument_token'])
        
        def on_ticks(ticks):
            for tick in ticks:
                # Find symbol from token
                inst = next((i for i in instruments if i['instrument_token'] == tick['instrument_token']), None)
                if inst:
                    symbol = inst['tradingsymbol']
                    current_price = tick['last_price']
                    self.update_position(symbol, current_price)
        
        def on_connect(ws, response):
            logger.info(f"WebSocket connected. Subscribed to {len(tokens)} instruments.")
        
        # Start ticker in separate thread
        ticker_thread = threading.Thread(
            target=self.zerodha.start_ticker,
            args=(tokens, on_ticks, on_connect)
        )
        ticker_thread.daemon = True
        ticker_thread.start()
    
    def close_all_positions_eod(self):
        """Close all open positions at end of day"""
        for symbol, position in self.active_positions.items():
            if position['status'] == 'OPEN':
                # Get current quote
                quote = self.zerodha.get_quote([f"NSE:{symbol}"])
                if quote:
                    current_price = quote[f"NSE:{symbol}"]['last_price']
                    self.exit_position(symbol, current_price, 'EOD_CLOSE')
    
    def get_portfolio_summary(self):
        """Get summary of all positions"""
        summary = {
            'total_positions': len(self.active_positions),
            'open_positions': sum(1 for p in self.active_positions.values() if p['status'] == 'OPEN'),
            'closed_positions': sum(1 for p in self.active_positions.values() if p['status'] == 'CLOSED'),
            'total_pnl': sum(p.get('pnl_amount', 0) for p in self.active_positions.values() if 'pnl_amount' in p)
        }
        return summary
