# pages/Overview.py
import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.kpi import calculate_kpis

st.set_page_config(
    page_title="Overview - RevMax",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Performance Overview")
st.markdown("---")

# Get data from session state
daily_data = st.session_state.get('daily_data', None)
room_types = st.session_state.get('room_types', None)

# Debug info (remove in production)
if daily_data is None:
    st.warning("No data in session state. Please go back to the main page to load data.")
    st.info("👈 Click on 'RevMax' in the sidebar to go to the main page")

if daily_data is not None and not daily_data.empty:
    
    # KPI Row
    kpis = calculate_kpis(daily_data)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Occupancy Rate", kpis["current_occupancy_pct"], delta=kpis["occupancy_trend_pct"])
    with col2:
        st.metric("Average Daily Rate", f"${kpis['avg_rate']:,.0f}", delta=kpis["rate_trend_pct"])
    with col3:
        st.metric("Today's Revenue", f"${kpis['revenue']:,.0f}")
    with col4:
        st.metric("RevPAR", f"${kpis['revpar']:,.0f}")
    
    st.markdown("---")
    
    # Trend Chart
    st.subheader("📈 Performance Trends")
    
    chart_option = st.selectbox(
        "Select metric to view:",
        ["Occupancy Rate", "Average Rate", "Revenue"]
    )
    
    last_30_days = daily_data.tail(30).copy()
    
    if chart_option == "Occupancy Rate":
        last_30_days['Occupancy %'] = last_30_days['Occupancy'] * 100
        fig = px.line(last_30_days, x='Date', y='Occupancy %', title='Occupancy Trend', markers=True)
        fig.update_layout(height=400, template='simple_white')
        st.plotly_chart(fig, use_container_width=True)
        
    elif chart_option == "Average Rate":
        fig = px.line(last_30_days, x='Date', y='Avg Rate', title='Rate Trend', markers=True)
        fig.update_layout(height=400, template='simple_white')
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        fig = px.line(last_30_days, x='Date', y='Revenue', title='Revenue Trend', markers=True)
        fig.update_layout(height=400, template='simple_white')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Weekly Patterns
    st.subheader("📅 Weekly Patterns")
    
    daily_copy = daily_data.copy()
    daily_copy['DayOfWeek'] = daily_copy['Date'].dt.day_name()
    daily_copy['Occupancy %'] = daily_copy['Occupancy'] * 100
    
    weekly_avg = daily_copy.groupby('DayOfWeek').agg({
        'Occupancy %': 'mean',
        'Avg Rate': 'mean'
    }).reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_bar = px.bar(weekly_avg, x=weekly_avg.index, y='Occupancy %', 
                         title='Occupancy by Day', color='Occupancy %',
                         color_continuous_scale='Blues', text='Occupancy %')
        fig_bar.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_bar.update_layout(height=350)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        fig_bar2 = px.bar(weekly_avg, x=weekly_avg.index, y='Avg Rate',
                          title='Rate by Day', color='Avg Rate',
                          color_continuous_scale='Reds', text='Avg Rate')
        fig_bar2.update_traces(texttemplate='$%{text:.0f}', textposition='outside')
        fig_bar2.update_layout(height=350)
        st.plotly_chart(fig_bar2, use_container_width=True)
    
    # Competitor Comparison
    if 'Competitor Avg Rate' in daily_data.columns:
        st.markdown("---")
        st.subheader("🏆 Competitor Benchmarking")
        
        comparison = daily_data.tail(30)[['Date', 'Avg Rate', 'Competitor Avg Rate']].copy()
        comparison.columns = ['Date', 'Your Hotel', 'Competitors']
        
        fig_comp = px.line(comparison, x='Date', y=['Your Hotel', 'Competitors'],
                           title='Rate Comparison', markers=True)
        fig_comp.update_layout(height=400)
        st.plotly_chart(fig_comp, use_container_width=True)

else:
    st.error("No data available. Please check your data files.")
    st.info("Make sure daily_data.csv exists in the 'data' folder")

st.markdown("---")
st.caption("RevMax Overview Dashboard")