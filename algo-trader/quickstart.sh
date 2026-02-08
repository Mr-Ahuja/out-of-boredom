#!/bin/bash

echo "🚀 Algo Trading Platform - Quick Start"
echo "======================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo ""
echo "1. Configure API keys:"
echo "   cp .env.example .env"
echo "   # Edit .env with your Zerodha credentials"
echo ""
echo "2. Run stock screener:"
echo "   python main.py screener"
echo ""
echo "3. Backtest a stock:"
echo "   python main.py backtest --symbol RELIANCE --days 30"
echo ""
echo "4. Start paper trading:"
echo "   python main.py simulate"
echo ""
echo "5. Launch dashboard:"
echo "   streamlit run dashboard.py"
echo ""
echo "⚠️  Before going live, test thoroughly in simulation mode!"
echo ""
