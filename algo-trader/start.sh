#!/bin/bash

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

clear

echo -e "${CYAN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║           Algo Trading Platform - Launcher                 ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if setup is complete
if [ ! -f ".setup_complete" ]; then
    echo -e "${RED}❌ Setup not completed!${NC}"
    echo ""
    echo "Please run ./setup.sh first to configure the application."
    echo ""
    exit 1
fi

# Display setup info
echo -e "${GREEN}✅ Setup verified${NC}"
echo ""
cat .setup_complete | head -n 1
echo ""

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Virtual environment not found!${NC}"
    echo "Please run ./setup.sh again"
    exit 1
fi

source venv/bin/activate

# Check if we're in trading hours (9:00 AM - 3:30 PM IST)
current_hour=$(date +%H)
current_min=$(date +%M)
current_time=$((10#$current_hour * 60 + 10#$current_min))
market_open=$((9 * 60))      # 9:00 AM
market_close=$((15 * 60 + 30))  # 3:30 PM

if [ $current_time -ge $market_open ] && [ $current_time -le $market_close ]; then
    echo -e "${GREEN}🟢 Market is OPEN${NC}"
else
    echo -e "${YELLOW}🔴 Market is CLOSED${NC}"
    echo "   Trading hours: 9:15 AM - 3:30 PM IST"
fi

echo ""
echo -e "${BLUE}Select an option:${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  ${CYAN}1)${NC} 🔍 Run Stock Screener"
echo "  ${CYAN}2)${NC} 📊 Backtest a Stock"
echo "  ${CYAN}3)${NC} 🎮 Start Paper Trading (Simulation)"
echo "  ${CYAN}4)${NC} 📈 Launch Dashboard (Web UI)"
echo "  ${CYAN}5)${NC} 🔴 Live Trading (Real Money) ⚠️"
echo "  ${CYAN}6)${NC} 🧪 Run Examples"
echo "  ${CYAN}7)${NC} ⚙️  Reconfigure (Re-run Setup)"
echo "  ${CYAN}8)${NC} 📚 View Documentation"
echo "  ${CYAN}9)${NC} 🚪 Exit"
echo ""

read -p "Enter your choice (1-9): " choice

case $choice in
    1)
        echo ""
        echo -e "${BLUE}🔍 Running Stock Screener...${NC}"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        python main.py screener
        ;;
    
    2)
        echo ""
        read -p "Enter stock symbol (e.g., RELIANCE): " symbol
        read -p "Number of days to backtest [30]: " days
        days=${days:-30}
        
        echo ""
        echo -e "${BLUE}📊 Backtesting $symbol for $days days...${NC}"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        python main.py backtest --symbol "$symbol" --days "$days"
        ;;
    
    3)
        echo ""
        echo -e "${BLUE}🎮 Starting Paper Trading (Simulation Mode)${NC}"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo -e "${YELLOW}💡 This is SIMULATION mode - No real money involved${NC}"
        echo "   Press Ctrl+C to stop trading"
        echo ""
        read -p "Press Enter to start..."
        
        python main.py simulate
        ;;
    
    4)
        echo ""
        echo -e "${BLUE}📈 Launching Dashboard...${NC}"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "Opening browser at http://localhost:8501"
        echo "Press Ctrl+C to stop the server"
        echo ""
        streamlit run dashboard.py
        ;;
    
    5)
        echo ""
        echo -e "${RED}"
        echo "╔════════════════════════════════════════════════════════════╗"
        echo "║                    ⚠️  WARNING ⚠️                           ║"
        echo "║                                                            ║"
        echo "║              LIVE TRADING MODE - REAL MONEY                ║"
        echo "║                                                            ║"
        echo "║  • Real trades will be executed                            ║"
        echo "║  • Real money will be at risk                              ║"
        echo "║  • Short selling = unlimited loss potential                ║"
        echo "║                                                            ║"
        echo "║  Only proceed if:                                          ║"
        echo "║    ✓ You've tested thoroughly in simulation                ║"
        echo "║    ✓ You understand the strategy completely               ║"
        echo "║    ✓ You can afford to lose this capital                  ║"
        echo "║    ✓ You have stop-loss discipline                        ║"
        echo "╚════════════════════════════════════════════════════════════╝"
        echo -e "${NC}"
        echo ""
        
        read -p "Have you been profitable in paper trading for 2+ weeks? (y/N): " profitable
        
        if [[ ! $profitable =~ ^[Yy]$ ]]; then
            echo ""
            echo -e "${YELLOW}⚠️  Not recommended to go live yet.${NC}"
            echo "Continue paper trading until consistently profitable."
            echo ""
            exit 0
        fi
        
        echo ""
        read -p "Enter capital to allocate (₹): " capital
        
        if [ -z "$capital" ]; then
            echo -e "${RED}Capital is required${NC}"
            exit 1
        fi
        
        echo ""
        echo -e "${YELLOW}Type 'START LIVE TRADING' to confirm:${NC}"
        read confirmation
        
        if [ "$confirmation" != "START LIVE TRADING" ]; then
            echo ""
            echo "Live trading cancelled."
            exit 0
        fi
        
        echo ""
        echo -e "${RED}🔴 Starting Live Trading...${NC}"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        
        python main.py live
        ;;
    
    6)
        echo ""
        echo -e "${BLUE}🧪 Running Examples...${NC}"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        python example_usage.py
        ;;
    
    7)
        echo ""
        echo -e "${BLUE}⚙️  Re-running Setup...${NC}"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ./setup.sh
        ;;
    
    8)
        echo ""
        echo -e "${BLUE}📚 Documentation${NC}"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "  1) README.md         - User guide"
        echo "  2) PROJECT_SUMMARY.md - What was built"
        echo "  3) SETUP_GUIDE.md     - API setup details"
        echo "  4) CHECKLIST.md       - Launch checklist"
        echo ""
        read -p "Enter number to view (or press Enter to skip): " doc_choice
        
        case $doc_choice in
            1) less README.md ;;
            2) less PROJECT_SUMMARY.md ;;
            3) less SETUP_GUIDE.md ;;
            4) less CHECKLIST.md ;;
            *) echo "Skipping..." ;;
        esac
        ;;
    
    9)
        echo ""
        echo -e "${GREEN}👋 Goodbye!${NC}"
        echo ""
        exit 0
        ;;
    
    *)
        echo ""
        echo -e "${RED}Invalid choice. Please run ./start.sh again.${NC}"
        exit 1
        ;;
esac

echo ""
echo ""
read -p "Press Enter to return to menu or Ctrl+C to exit..."
exec ./start.sh
