# pages/Recommendations.py
import streamlit as st
import sys
import os
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.recommendations import get_room_recommendations, get_urgent_recommendations, calculate_savings_opportunity

st.set_page_config(
    page_title="Recommendations - RevMax",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Smart Pricing Recommendations")
st.markdown("*AI-driven room-level pricing optimization*")
st.markdown("---")

daily_data = st.session_state.get('daily_data', None)
room_types = st.session_state.get('room_types', None)

if daily_data is not None and not daily_data.empty and room_types is not None:
    
    # Opportunity Summary
    opportunity = calculate_savings_opportunity(room_types, daily_data)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 Total Revenue Opportunity", f"${opportunity['total_opportunity']:,.0f}", delta="per day")
    with col2:
        st.metric("🎯 High Priority Actions", opportunity['high_priority_count'])
    with col3:
        st.metric("📊 Average Price Change", f"{opportunity['avg_change']:.0f}%")
    
    st.markdown("---")
    
    # Urgent Recommendations
    urgent_recs = get_urgent_recommendations(room_types, daily_data)
    
    if not urgent_recs.empty:
        st.warning("⚠️ **Urgent Recommendations - Take Action Today**")
        st.dataframe(
            urgent_recs[['Room Type', 'Current Rate', 'Recommended Rate', 'Change', 'Action', 'Reason', 'Expected Daily Impact']],
            use_container_width=True,
            hide_index=True
        )
        st.markdown("---")
    
    # All Recommendations
    recommendations_df = get_room_recommendations(room_types, daily_data)
    
    if not recommendations_df.empty:
        st.info("📋 **Complete Room-by-Room Analysis**")
        st.dataframe(
            recommendations_df[['Room Type', 'Current Rate', 'Recommended Rate', 'Change', 'Action', 'Reason', 'Expected Daily Impact', 'Priority']],
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown("---")
        
        # Action Buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("✅ Apply All Recommendations", use_container_width=True):
                st.success("Recommendations logged for review!")
                st.balloons()
        
        with col2:
            if st.button("📧 Generate Report", use_container_width=True):
                st.info("Report generated! (Would email revenue team in production)")
        
        with col3:
            if st.button("🔄 Refresh Analysis", use_container_width=True):
                st.rerun()
        
        # Explanation
        with st.expander("📖 How Recommendations Are Calculated"):
            st.markdown("""
            ### Pricing Strategy Logic:
            
            1. **High Occupancy (>80%)** → Increase prices (8-12%)
            2. **Low Occupancy (<50%)** → Decrease prices (10-15%)
            3. **Medium Occupancy (50-80%)** → Strategic adjustments
            4. **Weekend Premium** → +5% on high-demand days
            5. **Suite Strategy** → Special focus on luxury inventory
            
            ### Priority Levels:
            - 🔴 **High**: Urgent action needed (10%+ price change)
            - 🟠/🟡 **Medium**: Consider this week
            - 🟢 **Low**: Monitor and review
            """)
    else:
        st.info("No recommendations available. Current pricing appears optimal!")

else:
    st.error("Insufficient data. Please check daily_data.csv and room_types.csv")

st.markdown("---")
st.caption("RevMax Recommendation Engine")