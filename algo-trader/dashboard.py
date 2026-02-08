#!/usr/bin/env python3
"""
Trading Dashboard - Streamlit UI for monitoring and backtesting
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from modules.screener import StockScreener
from modules.backtester import Backtester
from modules.live_executor import LiveExecutor
import plotly.graph_objects as go

st.set_page_config(page_title="Algo Trading Dashboard", layout="wide")

st.title("📈 Algo Trading Dashboard")

# Sidebar
st.sidebar.header("Controls")
mode = st.sidebar.selectbox("Mode", ["Screener", "Backtest", "Live Monitor"])

if mode == "Screener":
    st.header("🔍 Stock Screener")
    
    if st.button("Run Screener"):
        with st.spinner("Analyzing stocks..."):
            screener = StockScreener()
            results = screener.screen_stocks()
            
            if len(results) > 0:
                st.success(f"Found {len(results)} candidates!")
                
                # Display results
                st.dataframe(results, use_container_width=True)
                
                # Charts
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = go.Figure(data=[
                        go.Bar(x=results['symbol'], y=results['sentiment_score'], 
                               name='Sentiment Score')
                    ])
                    fig.update_layout(title="Sentiment Analysis")
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    fig = go.Figure(data=[
                        go.Bar(x=results['symbol'], y=results['combined_score'],
                               name='Combined Score')
                    ])
                    fig.update_layout(title="Combined Score")
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No stocks met the criteria")

elif mode == "Backtest":
    st.header("📊 Backtesting")
    
    col1, col2 = st.columns(2)
    
    with col1:
        symbol = st.text_input("Stock Symbol", value="RELIANCE")
    
    with col2:
        days = st.number_input("Days to Backtest", min_value=1, max_value=365, value=30)
    
    if st.button("Run Backtest"):
        with st.spinner(f"Backtesting {symbol}..."):
            backtester = Backtester()
            
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            results = backtester.backtest_symbol(symbol, start_date, end_date)
            
            if len(results) > 0:
                # Performance metrics
                metrics = backtester.calculate_metrics(results)
                
                col1, col2, col3, col4 = st.columns(4)
                
                col1.metric("Total Trades", metrics['total_trades'])
                col2.metric("Win Rate", f"{metrics['win_rate']:.1f}%")
                col3.metric("Total P&L", f"{metrics['total_pnl']:.2f}%")
                col4.metric("Profit Factor", f"{metrics['profit_factor']:.2f}")
                
                # Trade results
                st.subheader("Trade Results")
                st.dataframe(results[['date', 'entry_price', 'exit_price', 'exit_reason', 'pnl_percent']], 
                           use_container_width=True)
                
                # P&L chart
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=results['date'],
                    y=results['pnl_percent'].cumsum(),
                    mode='lines+markers',
                    name='Cumulative P&L'
                ))
                fig.update_layout(title="Cumulative P&L Over Time",
                                xaxis_title="Date",
                                yaxis_title="P&L %")
                st.plotly_chart(fig, use_container_width=True)
                
                # Win/Loss distribution
                fig = go.Figure(data=[
                    go.Histogram(x=results['pnl_percent'], nbinsx=20)
                ])
                fig.update_layout(title="P&L Distribution",
                                xaxis_title="P&L %",
                                yaxis_title="Frequency")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No trades found")

elif mode == "Live Monitor":
    st.header("🎮 Live Trading Monitor")
    
    simulation = st.sidebar.checkbox("Simulation Mode", value=True)
    
    st.info("📡 Real-time monitoring - Coming soon!")
    
    # Placeholder for live positions
    st.subheader("Active Positions")
    placeholder = st.empty()
    
    # This would be updated in real-time
    st.write("Connect to live trading executor to see real-time positions")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**⚠️ Risk Warning**")
st.sidebar.caption("Algo trading involves substantial risk. Never trade with money you can't afford to lose.")
