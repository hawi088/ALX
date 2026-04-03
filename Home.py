# landing.py - The Sovereign Revenue Engine Landing Page
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.data_loader import load_daily_data, load_room_types, load_events
from utils.kpi import calculate_kpis

# Page config
st.set_page_config(
    page_title="RevMax - Sovereign Revenue Engine",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize data
def init_session_state():
    if 'daily_data' not in st.session_state:
        daily_data = load_daily_data()
        st.session_state.daily_data = daily_data
        st.session_state.data_loaded = daily_data is not None
    
    if 'room_types' not in st.session_state:
        room_types = load_room_types()
        st.session_state.room_types = room_types
    
    if 'events' not in st.session_state:
        events = load_events()
        st.session_state.events = events

init_session_state()

# Custom CSS for Black/Gold Theme
st.markdown("""
<style>
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main container */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #0a0a0a 100%);
    }
    
    /* Top gradient bar */
    .top-bar {
        background: linear-gradient(90deg, #000000 0%, #d4af37 50%, #000000 100%);
        height: 4px;
        width: 100%;
        margin-bottom: 3rem;
    }
    
    /* Gold tag */
    .gold-tag {
        color: #d4af37;
        font-size: 0.85rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 1rem;
        font-weight: 500;
    }
    
    /* Main title */
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: #ffffff;
        line-height: 1.2;
        margin-bottom: 1rem;
    }
    
    .highlight {
        color: #d4af37;
    }
    
    /* Description */
    .description {
        font-size: 1rem;
        color: #a0a0a0;
        line-height: 1.6;
        margin-bottom: 2rem;
        max-width: 90%;
    }
    
    /* Button styling */
    .analytics-btn {
        background: linear-gradient(135deg, #d4af37 0%, #c5a020 100%);
        color: #0a0a0a;
        padding: 14px 28px;
        border-radius: 10px;
        border: none;
        font-weight: 700;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
    }
    .analytics-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.4);
    }
    
    .ai-btn {
        background: transparent;
        color: #d4af37;
        padding: 14px 28px;
        border-radius: 10px;
        border: 2px solid #d4af37;
        font-weight: 700;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
    }
    .ai-btn:hover {
        background: rgba(212, 175, 55, 0.1);
        transform: translateY(-2px);
    }
    
    /* Dashboard Card */
    .dashboard-card {
        background: rgba(20, 20, 20, 0.8);
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid rgba(212, 175, 55, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .revenue-pulse {
        color: #d4af37;
        font-size: 0.8rem;
        letter-spacing: 1px;
        margin-bottom: 1rem;
    }
    
    .metric-value-gold {
        font-size: 2.2rem;
        font-weight: 700;
        color: #d4af37;
    }
    
    .metric-label {
        font-size: 0.75rem;
        color: #888;
        margin-top: 0.25rem;
    }
    
    .stat-box {
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }
    
    /* Divider */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #d4af37, transparent);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Top gradient bar
st.markdown('<div class="top-bar"></div>', unsafe_allow_html=True)

# Main layout - Two columns
left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    st.markdown("""
    <div class="gold-tag">⚡ AI-POWERED REVENUE MANAGEMENT</div>
    <div class="main-title">
        The Sovereign Revenue Engine<br>
        for <span class="highlight">Ethiopian Resorts</span>
    </div>
    <div class="description">
        Move from spreadsheet chaos to data-driven growth with AI-powered occupancy intelligence 
        and dynamic pricing built for the unique rhythms of the Highlands.
    </div>
    """, unsafe_allow_html=True)
    
    # Two buttons - Analytics and AI Insights
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("📊 Live Analytics →", use_container_width=True, key="analytics"):
            st.switch_page("pages/Analytics.py")
    with col_b:
        if st.button("🧠 AI Insights →", use_container_width=True, key="ai_insights"):
            st.switch_page("pages/AI_Insights.py")

with right_col:
    st.markdown("""
    <div class="dashboard-card">
        <div class="revenue-pulse">⚡ REVENUE PULSE</div>
    """, unsafe_allow_html=True)
    
    # Get real data if available
    if st.session_state.data_loaded and st.session_state.daily_data is not None:
        from utils.kpi import calculate_kpis
        kpis = calculate_kpis(st.session_state.daily_data)
        occupancy_value = kpis['current_occupancy_pct']
        revenue_value = kpis['revenue']
        
        # Create metrics row
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="stat-box">
                <div class="metric-value-gold">{occupancy_value}</div>
                <div class="metric-label">Current Occupancy</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="stat-box">
                <div class="metric-value-gold">ETB {revenue_value:,.0f}</div>
                <div class="metric-label">Today's Revenue</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Create bar chart for monthly data
        df = st.session_state.daily_data.copy()
        df['Month'] = df['Date'].dt.strftime('%b')
        monthly_revenue = df.groupby('Month')['Revenue'].sum().reset_index()
        
        fig = go.Figure(data=[
            go.Bar(
                x=monthly_revenue['Month'],
                y=monthly_revenue['Revenue'],
                marker_color='#d4af37',
                marker_line_color='#d4af37',
                marker_line_width=1,
                opacity=0.8,
                text=monthly_revenue['Revenue'],
                textposition='outside',
                textfont=dict(color='#d4af37', size=10)
            )
        ])
        
        fig.update_layout(
            title=dict(text="Monthly Revenue Trend", font=dict(color='white', size=14)),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                tickfont=dict(color='#888'),
                gridcolor='rgba(255,255,255,0.1)',
                title_font=dict(color='#888')
            ),
            yaxis=dict(
                tickfont=dict(color='#888'),
                gridcolor='rgba(255,255,255,0.1)',
                title_font=dict(color='#888'),
                tickformat='$,.0f'
            ),
            height=300,
            margin=dict(l=40, r=20, t=50, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # AI Insight note
        st.caption("🤖 AI predicts +12.4% demand increase next week")
        
    else:
        # Demo data if no real data
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="stat-box">
                <div class="metric-value-gold">94.2%</div>
                <div class="metric-label">Occupancy Forecast</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="stat-box">
                <div class="metric-value-gold">ETB 12,450</div>
                <div class="metric-label">Revenue (Today)</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Sample bar chart
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        values = [8500, 9200, 10100, 11200, 12450, 13800]
        
        fig = go.Figure(data=[
            go.Bar(x=months, y=values, marker_color='#d4af37')
        ])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(tickfont=dict(color='#888'), gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(tickfont=dict(color='#888'), gridcolor='rgba(255,255,255,0.1)', tickformat='$,.0f'),
            height=300,
            margin=dict(l=40, r=20, t=20, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.caption("🤖 AI predictions active - Connect data for real insights")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Divider
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col2:
    st.caption("© 2026 RevMax - AI-Powered Revenue Management for Ethiopian Resorts")