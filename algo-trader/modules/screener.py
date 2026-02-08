import pandas as pd
import logging
from datetime import datetime, timedelta
from modules.zerodha_client import ZerodhaClient
from modules.news_analyzer import NewsAnalyzer
from config import SCREENER_CONFIG

logger = logging.getLogger(__name__)

class StockScreener:
    """Screen stocks for short opportunities"""
    
    def __init__(self):
        self.zerodha = ZerodhaClient()
        self.news_analyzer = NewsAnalyzer()
    
    def get_nse_stocks(self):
        """Fetch all NSE equity stocks"""
        instruments = self.zerodha.get_instruments('NSE')
        
        # Filter for equity stocks
        stocks = [
            inst for inst in instruments 
            if inst['segment'] == 'NSE' and inst['instrument_type'] == 'EQ'
        ]
        
        return pd.DataFrame(stocks)
    
    def apply_basic_filters(self, df):
        """Apply volume and price filters"""
        # Get quotes for all symbols (in batches to avoid API limits)
        symbols = [f"NSE:{symbol}" for symbol in df['tradingsymbol'].tolist()]
        
        filtered_stocks = []
        
        # Process in batches of 500
        batch_size = 500
        for i in range(0, len(symbols), batch_size):
            batch = symbols[i:i+batch_size]
            quotes = self.zerodha.get_quote(batch)
            
            for symbol, data in quotes.items():
                ltp = data.get('last_price', 0)
                volume = data.get('volume', 0)
                
                # Apply filters
                if (SCREENER_CONFIG['min_price'] <= ltp <= SCREENER_CONFIG['max_price'] and
                    volume >= SCREENER_CONFIG['min_volume']):
                    
                    filtered_stocks.append({
                        'symbol': symbol.replace('NSE:', ''),
                        'price': ltp,
                        'volume': volume,
                        'ohlc': data.get('ohlc', {})
                    })
        
        return pd.DataFrame(filtered_stocks)
    
    def calculate_technical_indicators(self, stock_data):
        """Calculate bearish technical indicators"""
        score = 0
        
        # Price vs Open (bearish if trading below open)
        ohlc = stock_data.get('ohlc', {})
        open_price = ohlc.get('open', 0)
        current_price = stock_data.get('price', 0)
        
        if current_price < open_price:
            score += 1
        
        # You can add more indicators:
        # - RSI (overbought)
        # - MACD bearish crossover
        # - Volume spike with price drop
        # - Moving average crossovers
        
        return score
    
    def screen_stocks(self, top_n=None):
        """Main screening function"""
        if top_n is None:
            top_n = SCREENER_CONFIG['top_n_stocks']
        
        logger.info("Starting stock screening...")
        
        # Step 1: Get all NSE stocks
        all_stocks = self.get_nse_stocks()
        logger.info(f"Fetched {len(all_stocks)} NSE stocks")
        
        # Step 2: Apply basic filters (price, volume)
        filtered = self.apply_basic_filters(all_stocks)
        logger.info(f"After basic filters: {len(filtered)} stocks")
        
        # Step 3: Score each stock
        scored_stocks = []
        
        for idx, stock in filtered.iterrows():
            symbol = stock['symbol']
            
            # Technical score
            tech_score = self.calculate_technical_indicators(stock)
            
            # Sentiment score
            sentiment_score = self.news_analyzer.get_stock_sentiment(symbol)
            
            # Combined score (weighted)
            # Higher negative sentiment + bearish technicals = better short candidate
            combined_score = (tech_score * 0.4) + (abs(sentiment_score) * 0.6)
            
            # Only consider stocks with negative sentiment
            if sentiment_score < SCREENER_CONFIG['bearish_sentiment_threshold']:
                scored_stocks.append({
                    'symbol': symbol,
                    'price': stock['price'],
                    'volume': stock['volume'],
                    'technical_score': tech_score,
                    'sentiment_score': sentiment_score,
                    'combined_score': combined_score
                })
        
        # Sort by combined score (descending)
        scored_df = pd.DataFrame(scored_stocks)
        if len(scored_df) > 0:
            scored_df = scored_df.sort_values('combined_score', ascending=False)
            top_stocks = scored_df.head(top_n)
            
            logger.info(f"Top {top_n} short candidates identified")
            return top_stocks
        else:
            logger.warning("No stocks met the criteria")
            return pd.DataFrame()
