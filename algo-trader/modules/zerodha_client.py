from kiteconnect import KiteConnect, KiteTicker
import logging
from config import KITE_API_KEY, KITE_ACCESS_TOKEN

logger = logging.getLogger(__name__)

class ZerodhaClient:
    """Wrapper for Zerodha Kite Connect API"""
    
    def __init__(self):
        self.kite = KiteConnect(api_key=KITE_API_KEY)
        self.kite.set_access_token(KITE_ACCESS_TOKEN)
        self.ticker = None
        
    def get_instruments(self, exchange='NSE'):
        """Fetch all instruments for given exchange"""
        try:
            instruments = self.kite.instruments(exchange)
            return instruments
        except Exception as e:
            logger.error(f"Error fetching instruments: {e}")
            return []
    
    def get_quote(self, symbols):
        """Get live quotes for symbols"""
        try:
            quotes = self.kite.quote(symbols)
            return quotes
        except Exception as e:
            logger.error(f"Error fetching quotes: {e}")
            return {}
    
    def get_historical_data(self, instrument_token, from_date, to_date, interval='day'):
        """Fetch historical data"""
        try:
            data = self.kite.historical_data(
                instrument_token=instrument_token,
                from_date=from_date,
                to_date=to_date,
                interval=interval
            )
            return data
        except Exception as e:
            logger.error(f"Error fetching historical data: {e}")
            return []
    
    def place_order(self, tradingsymbol, transaction_type, quantity, order_type='MARKET', product='MIS'):
        """Place an order"""
        try:
            order_id = self.kite.place_order(
                variety=self.kite.VARIETY_REGULAR,
                exchange=self.kite.EXCHANGE_NSE,
                tradingsymbol=tradingsymbol,
                transaction_type=transaction_type,  # BUY or SELL
                quantity=quantity,
                product=product,  # MIS for intraday
                order_type=order_type
            )
            logger.info(f"Order placed: {order_id}")
            return order_id
        except Exception as e:
            logger.error(f"Error placing order: {e}")
            return None
    
    def get_positions(self):
        """Get current positions"""
        try:
            positions = self.kite.positions()
            return positions
        except Exception as e:
            logger.error(f"Error fetching positions: {e}")
            return {}
    
    def start_ticker(self, tokens, on_ticks_callback, on_connect_callback=None):
        """Start WebSocket ticker for live data"""
        self.ticker = KiteTicker(KITE_API_KEY, KITE_ACCESS_TOKEN)
        
        def on_ticks(ws, ticks):
            on_ticks_callback(ticks)
        
        def on_connect(ws, response):
            ws.subscribe(tokens)
            ws.set_mode(ws.MODE_FULL, tokens)
            if on_connect_callback:
                on_connect_callback(ws, response)
        
        self.ticker.on_ticks = on_ticks
        self.ticker.on_connect = on_connect
        self.ticker.connect()
    
    def stop_ticker(self):
        """Stop WebSocket ticker"""
        if self.ticker:
            self.ticker.close()
