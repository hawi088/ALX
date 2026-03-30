# revmax/app.py
import streamlit as st
import sys
import os
from datetime import datetime

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.data_loader import load_daily_data, load_room_types, load_events

# Page configuration
st.set_page_config(
    page_title="RevMax - Revenue Management System",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state with data
def init_session_state():
    """Load and store data in session state"""
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

# Call initialization
init_session_state()

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.3rem;
        font-weight: semi-bold;
        color: #2c3e50;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .feature-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">🏨 RevMax Revenue Management System</div>', unsafe_allow_html=True)
st.markdown(f"*Welcome back! Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
st.markdown("---")

# Show data status
if st.session_state.data_loaded:
    st.success("✅ Data loaded successfully!")
else:
    st.error("❌ No data found. Please check your data files in the 'data' folder.")

# Quick stats summary
if st.session_state.daily_data is not None and not st.session_state.daily_data.empty:
    from utils.kpi import calculate_kpis
    kpis = calculate_kpis(st.session_state.daily_data)
    
    st.markdown('<div class="sub-header">📊 Quick Snapshot</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Current Occupancy", kpis["current_occupancy_pct"])
    with col2:
        st.metric("Average Daily Rate", f"${kpis['avg_rate']:,.0f}")
    with col3:
        st.metric("Today's Revenue", f"${kpis['revenue']:,.0f}")
    with col4:
        st.metric("Rooms Available", f"{kpis['rooms_left']}/{kpis['total_rooms']}")
    
    st.markdown("---")

# Navigation Guide
st.markdown('<div class="sub-header">🚀 Navigate Your Dashboard</div>', unsafe_allow_html=True)
st.markdown("Use the sidebar to explore different features of RevMax:")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 📋 Main Features
    
    - **📊 Overview** - Real-time KPIs and performance metrics
    - **🚨 Alerts** - Live intelligence alerts and warnings
    - **📈 Analytics** - Charts, trends, and competitor analysis
    
    ### 💡 Smart Features
    
    - **🎮 What-If Simulator** - Test pricing strategies
    - **🧠 AI Insights** - Intelligent recommendations
    - **🎯 Recommendations** - Room-level pricing suggestions
    """)

with col2:
    st.markdown("""
    ### 🎯 Quick Actions
    
    """)
    
    # Use st.page_link for better navigation
    st.page_link("pages/Overview.py", label="📊 Go to Overview", icon="📊")
    st.page_link("pages/Alerts.py", label="🚨 Go to Alerts", icon="🚨")
    st.page_link("pages/AI_Insights.py", label="🧠 Get AI Insights", icon="🧠")

st.markdown("---")

# Data Status
with st.expander("📊 Data Status"):
    if st.session_state.daily_data is not None:
        st.success(f"✅ Daily Data: {len(st.session_state.daily_data)} records loaded")
        st.write(f"Date Range: {st.session_state.daily_data['Date'].min().date()} to {st.session_state.daily_data['Date'].max().date()}")
    else:
        st.error("❌ Daily Data: Not loaded")
    
    if st.session_state.room_types is not None:
        st.success(f"✅ Room Types: {len(st.session_state.room_types)} room categories loaded")
        st.write(st.session_state.room_types[['Room Type', 'Count']].head())
    else:
        st.error("❌ Room Types: Not loaded")
    
    if st.session_state.events is not None:
        st.success(f"✅ Events: {len(st.session_state.events)} upcoming events loaded")
    else:
        st.warning("⚠️ Events: No data")

# Footer
st.markdown("---")
st.caption("RevMax - Intelligent Hotel Revenue Management System | Multi-Page Dashboard")