#!/bin/bash

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║        Algo Trading Platform - Interactive Setup           ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if setup already done
if [ -f ".setup_complete" ]; then
    echo -e "${YELLOW}⚠️  Setup already completed!${NC}"
    read -p "Do you want to reconfigure? (y/N): " reconfigure
    if [[ ! $reconfigure =~ ^[Yy]$ ]]; then
        echo -e "${GREEN}✅ Setup unchanged. Run ./start.sh to launch the application.${NC}"
        exit 0
    fi
    echo ""
fi

echo -e "${BLUE}Step 1: Checking System Requirements${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found!${NC}"
    echo "Please install Python 3.8+ from https://python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✅ Python $PYTHON_VERSION found${NC}"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip not found!${NC}"
    echo "Please install pip: python3 -m ensurepip"
    exit 1
fi
echo -e "${GREEN}✅ pip found${NC}"

echo ""
echo -e "${BLUE}Step 2: Setting Up Virtual Environment${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${YELLOW}Virtual environment already exists${NC}"
fi

# Activate virtual environment
source venv/bin/activate

echo ""
echo -e "${BLUE}Step 3: Installing Dependencies${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "Installing Python packages (this may take a few minutes)..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ All dependencies installed${NC}"
else
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}Step 4: Zerodha API Configuration${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo "You need Zerodha Kite Connect API credentials."
echo "If you don't have them yet, visit: https://developers.kite.trade/"
echo ""
read -p "Do you have Zerodha API credentials ready? (y/N): " has_creds

if [[ ! $has_creds =~ ^[Yy]$ ]]; then
    echo ""
    echo -e "${YELLOW}📚 Please complete these steps first:${NC}"
    echo "  1. Go to https://developers.kite.trade/"
    echo "  2. Create a new app"
    echo "  3. Note down your API Key and Secret"
    echo "  4. Generate an access token"
    echo ""
    echo "See SETUP_GUIDE.md for detailed instructions."
    echo ""
    echo "Run ./setup.sh again when you have your credentials."
    exit 0
fi

echo ""
echo "Enter your Zerodha API credentials:"
echo ""

read -p "API Key: " KITE_API_KEY
read -p "API Secret: " KITE_API_SECRET
read -p "Access Token: " KITE_ACCESS_TOKEN

if [ -z "$KITE_API_KEY" ] || [ -z "$KITE_API_SECRET" ] || [ -z "$KITE_ACCESS_TOKEN" ]; then
    echo -e "${RED}❌ All fields are required!${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}Step 5: Strategy Configuration${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo "Configure your trading strategy parameters:"
echo "(Press Enter to use defaults shown in brackets)"
echo ""

read -p "Target drop percentage [0.2%]: " target_drop
target_drop=${target_drop:-0.2}

read -p "Trailing stop loss delta [0.1%]: " trailing_delta
trailing_delta=${trailing_delta:-0.1}

read -p "Maximum concurrent positions [5]: " max_positions
max_positions=${max_positions:-5}

read -p "Capital per trade (₹) [50000]: " capital_per_trade
capital_per_trade=${capital_per_trade:-50000}

echo ""
echo -e "${BLUE}Step 6: Screener Configuration${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
read -p "Minimum stock price (₹) [50]: " min_price
min_price=${min_price:-50}

read -p "Maximum stock price (₹) [5000]: " max_price
max_price=${max_price:-5000}

read -p "Minimum daily volume [100000]: " min_volume
min_volume=${min_volume:-100000}

read -p "Top N stocks to suggest [5]: " top_n_stocks
top_n_stocks=${top_n_stocks:-5}

echo ""
echo -e "${BLUE}Step 7: Saving Configuration${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Create .env file
cat > .env << EOF
# Zerodha API Credentials
KITE_API_KEY=$KITE_API_KEY
KITE_API_SECRET=$KITE_API_SECRET
KITE_ACCESS_TOKEN=$KITE_ACCESS_TOKEN

# News API (optional - add later if needed)
NEWS_API_KEY=

# Database
DATABASE_URL=sqlite:///data/trades.db
EOF

echo -e "${GREEN}✅ .env file created${NC}"

# Update config.py with user preferences
cat > config.py << EOF
import os
from dotenv import load_dotenv

load_dotenv()

# Zerodha API
KITE_API_KEY = os.getenv('KITE_API_KEY')
KITE_API_SECRET = os.getenv('KITE_API_SECRET')
KITE_ACCESS_TOKEN = os.getenv('KITE_ACCESS_TOKEN')

# Trading Parameters
STRATEGY_CONFIG = {
    'target_drop': ${target_drop} / 100,  # ${target_drop}% drop target
    'trailing_delta': ${trailing_delta} / 100,  # ${trailing_delta}% trailing stop loss
    'max_positions': ${max_positions},  # Max concurrent shorts
    'capital_per_trade': ${capital_per_trade},  # Capital per position
}

# Screener Parameters
SCREENER_CONFIG = {
    'min_volume': ${min_volume},  # Minimum daily volume
    'min_price': ${min_price},  # Minimum stock price
    'max_price': ${max_price},  # Maximum stock price
    'bearish_sentiment_threshold': -0.3,  # Negative sentiment score
    'top_n_stocks': ${top_n_stocks},  # Number of stocks to suggest
}

# Database
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/trades.db')

# Logging
LOG_FILE = 'logs/trading.log'
EOF

echo -e "${GREEN}✅ config.py updated${NC}"

echo ""
echo -e "${BLUE}Step 8: Testing Connection${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo "Testing Zerodha API connection..."

# Create a simple test script
cat > test_connection.py << 'EOF'
import sys
from modules.zerodha_client import ZerodhaClient

try:
    client = ZerodhaClient()
    instruments = client.get_instruments('NSE')
    print(f"✅ Connection successful! Found {len(instruments)} NSE instruments")
    sys.exit(0)
except Exception as e:
    print(f"❌ Connection failed: {e}")
    sys.exit(1)
EOF

python test_connection.py
connection_status=$?

rm test_connection.py

if [ $connection_status -ne 0 ]; then
    echo ""
    echo -e "${RED}❌ Failed to connect to Zerodha API${NC}"
    echo ""
    echo "Please check:"
    echo "  1. Your API credentials are correct"
    echo "  2. Access token is valid (they expire daily)"
    echo "  3. Your internet connection is working"
    echo ""
    echo "See SETUP_GUIDE.md for troubleshooting."
    exit 1
fi

# Create setup complete flag
cat > .setup_complete << EOF
Setup completed on: $(date)
API Key: $KITE_API_KEY
Strategy: ${target_drop}% target, ${trailing_delta}% trailing SL
Max positions: ${max_positions}
Capital per trade: ₹${capital_per_trade}
EOF

echo ""
echo -e "${GREEN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║              ✅ Setup Complete!                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo ""
echo -e "${BLUE}📋 Your Configuration:${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Target drop: ${target_drop}%"
echo "  Trailing SL: ${trailing_delta}%"
echo "  Max positions: ${max_positions}"
echo "  Capital per trade: ₹${capital_per_trade}"
echo "  Stock price range: ₹${min_price} - ₹${max_price}"
echo "  Min volume: ${min_volume}"
echo ""

echo -e "${GREEN}🚀 Ready to start!${NC}"
echo ""
echo "Run: ${BLUE}./start.sh${NC} to launch the application"
echo ""

echo -e "${YELLOW}📚 Next Steps:${NC}"
echo "  1. Read README.md for usage guide"
echo "  2. Check CHECKLIST.md for launch plan"
echo "  3. Start with paper trading (simulation mode)"
echo ""
