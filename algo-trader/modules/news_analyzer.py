import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime, timedelta
from transformers import pipeline
import pandas as pd

logger = logging.getLogger(__name__)

class NewsAnalyzer:
    """Fetch and analyze news for sentiment"""
    
    def __init__(self):
        # Load FinBERT for financial sentiment analysis
        try:
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="ProsusAI/finbert",
                device=-1  # CPU, use 0 for GPU
            )
            logger.info("FinBERT model loaded successfully")
        except Exception as e:
            logger.warning(f"Could not load FinBERT: {e}. Using fallback.")
            self.sentiment_analyzer = None
    
    def fetch_nse_announcements(self):
        """Scrape NSE corporate announcements"""
        url = "https://www.nseindia.com/companies-listing/corporate-filings-announcements"
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            # Parse announcements (structure may vary)
            # This is a placeholder - actual parsing depends on NSE structure
            announcements = []
            return announcements
        except Exception as e:
            logger.error(f"Error fetching NSE announcements: {e}")
            return []
    
    def fetch_news_for_stock(self, symbol, days_back=7):
        """Fetch news articles for a specific stock"""
        # Using NewsAPI or similar service
        # This is a placeholder - implement with actual news API
        try:
            # Example: search for company name in news
            # You'd need to map stock symbols to company names
            news_items = []
            return news_items
        except Exception as e:
            logger.error(f"Error fetching news for {symbol}: {e}")
            return []
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of text"""
        if not self.sentiment_analyzer:
            return 0.0
        
        try:
            # Truncate text if too long
            text = text[:512]
            result = self.sentiment_analyzer(text)[0]
            
            # FinBERT returns: positive, negative, neutral
            label = result['label'].lower()
            score = result['score']
            
            if label == 'positive':
                return score
            elif label == 'negative':
                return -score
            else:
                return 0.0
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return 0.0
    
    def get_stock_sentiment(self, symbol):
        """Get overall sentiment score for a stock"""
        news_items = self.fetch_news_for_stock(symbol)
        
        if not news_items:
            return 0.0
        
        sentiments = []
        for item in news_items:
            text = f"{item.get('title', '')} {item.get('description', '')}"
            sentiment = self.analyze_sentiment(text)
            sentiments.append(sentiment)
        
        # Average sentiment
        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0.0
        return avg_sentiment
