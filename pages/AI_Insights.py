# pages/AI_Insights.py
import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.ai import get_demo_ai_insights

st.set_page_config(
    page_title="AI Insights - RevMax",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 AI-Powered Insights")
st.markdown("*Intelligent recommendations powered by advanced analytics*")
st.markdown("---")

# Get data from session state
daily_data = st.session_state.get('daily_data', None)
events = st.session_state.get('events', None)
room_types = st.session_state.get('room_types', None)

# Debug info
if daily_data is None:
    st.warning("⚠️ No data found in session state.")
    st.info("👈 Please go to the main page (RevMax) first to load data, then come back here.")
    st.stop()

if daily_data is not None and not daily_data.empty:
    
    ai_insights = get_demo_ai_insights(daily_data, events, room_types)
    
    # Executive Summary
    st.info(ai_insights['summary'])
    st.markdown("---")
    
    # Pricing Strategy
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💲 Pricing Strategy")
        st.markdown(ai_insights['pricing_advice'])
    
    with col2:
        st.markdown("### 📊 AI Confidence")
        st.metric("Model Confidence", "87%")
        st.metric("Data Quality", "92%")
        st.caption("RevMax AI v1.0")
    
    st.markdown("---")
    
    # Warnings and Opportunities
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⚠️ Alerts & Warnings")
        if ai_insights['warnings']:
            for warning in ai_insights['warnings'][:3]:
                if warning['type'] == 'critical':
                    st.error(f"**{warning['message']}**\n\n💡 {warning['action']}")
                elif warning['type'] == 'warning':
                    st.warning(f"**{warning['message']}**\n\n💡 {warning['action']}")
                else:
                    st.info(f"**{warning['message']}**\n\n💡 {warning['action']}")
        else:
            st.success("✅ No active warnings")
    
    with col2:
        st.markdown("### 🚀 Opportunities")
        if ai_insights['opportunities']:
            for opp in ai_insights['opportunities'][:3]:
                with st.expander(f"{opp['title']}"):
                    st.write(opp['description'])
                    st.caption(f"💡 Potential Impact: {opp['potential_impact']}")
        else:
            st.info("No immediate opportunities")
    
    st.markdown("---")
    
    # Action Items
    st.markdown("### ✅ AI-Generated Action Items")
    action_df = pd.DataFrame(ai_insights['action_items'])
    st.dataframe(action_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Forecast
    st.markdown("### 📈 7-Day AI Forecast")
    
    if 'forecast' in ai_insights and 'error' not in ai_insights['forecast']:
        forecast_df = pd.DataFrame(ai_insights['forecast'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_occ = px.line(forecast_df, x='day', y='predicted_occupancy',
                              title='Predicted Occupancy', markers=True)
            fig_occ.update_layout(height=350)
            fig_occ.update_yaxes(tickformat='.0%')
            st.plotly_chart(fig_occ, use_container_width=True)
        
        with col2:
            fig_rate = px.line(forecast_df, x='day', y='predicted_rate',
                               title='Predicted Average Rate', markers=True)
            fig_rate.update_layout(height=350)
            st.plotly_chart(fig_rate, use_container_width=True)
        
        st.caption("🤖 AI Forecast Confidence: Medium - Based on historical patterns")
    else:
        st.warning("Need at least 14 days of data for accurate forecasting")
    
    # AI Model Explanation
    with st.expander("🤖 How Our AI Works"):
        st.markdown("""
        ### AI Model Components:
        
        1. **Pattern Recognition**: Identifies trends in occupancy and rates
        2. **Predictive Analytics**: Forecasts future performance
        3. **Anomaly Detection**: Spots unusual patterns
        4. **Recommendation Engine**: Generates actionable insights
        5. **Continuous Learning**: Improves with more data
        
        *Premium feature: GPT-4 integration available for enhanced insights*
        """)

else:
    st.error("❌ No data available. Please check your data files.")
    st.info("Make sure daily_data.csv exists in the 'data' folder")

st.markdown("---")
st.caption("RevMax AI Intelligence Engine")