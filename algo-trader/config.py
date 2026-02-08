import os
from dotenv import load_dotenv

load_dotenv()

# Zerodha API
KITE_API_KEY = os.getenv('KITE_API_KEY')
KITE_API_SECRET = os.getenv('KITE_API_SECRET')
KITE_ACCESS_TOKEN = os.getenv('KITE_ACCESS_TOKEN')

# Trading Parameters
STRATEGY_CONFIG = {
    'target_drop': 0.2 / 100,  # 0.2% drop target
    'trailing_delta': 0.1 / 100,  # 0.1% trailing stop loss
    'max_positions': 5,  # Max concurrent shorts
    'capital_per_trade': 500000,  # Capital per position
}

# Screener Parameters
SCREENER_CONFIG = {
    'min_volume': 100000,  # Minimum daily volume
    'min_price': 50,  # Minimum stock price
    'max_price': 5000,  # Maximum stock price
    'bearish_sentiment_threshold': -0.3,  # Negative sentiment score
    'top_n_stocks': 5,  # Number of stocks to suggest
}

# Database
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/trades.db')

# Logging
LOG_FILE = 'logs/trading.log'
