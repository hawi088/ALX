# pages/Alerts.py
import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.alerts import get_alerts, get_alert_summary

st.set_page_config(
    page_title="Alerts - RevMax",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 Live Intelligence Alerts")
st.markdown("*Real-time monitoring and proactive notifications*")
st.markdown("---")

# Get data from session state
daily_data = st.session_state.get('daily_data', None)
events = st.session_state.get('events', None)
room_types = st.session_state.get('room_types', None)

if daily_data is not None and not daily_data.empty:
    
    alerts = get_alerts(daily_data, events, room_types)
    alert_summary = get_alert_summary(daily_data, events, room_types)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Alerts", alert_summary['total'])
    with col2:
        st.metric("Critical", alert_summary['critical'], delta="Action needed")
    with col3:
        st.metric("Warnings", alert_summary['warning'])
    with col4:
        st.metric("Opportunities", alert_summary['success'])
    
    st.markdown("---")
    
    # Filter alerts
    alert_filter = st.selectbox(
        "Filter Alerts",
        ["All Alerts", "Critical Only", "Warnings Only", "Opportunities Only"]
    )
    
    # Display filtered alerts
    if alerts:
        filtered_alerts = alerts
        if alert_filter == "Critical Only":
            filtered_alerts = [a for a in alerts if a['type'] == 'critical']
        elif alert_filter == "Warnings Only":
            filtered_alerts = [a for a in alerts if a['type'] == 'warning']
        elif alert_filter == "Opportunities Only":
            filtered_alerts = [a for a in alerts if a['type'] == 'success']
        
        for alert in filtered_alerts:
            if alert['type'] == 'critical':
                st.error(f"""
                **{alert['title']}**
                
                📝 {alert['message']}
                
                💡 **Recommended Action:** {alert['action']}
                
                📊 **Metric:** {alert['metric']} | **Value:** {alert['value']}
                """)
            elif alert['type'] == 'warning':
                st.warning(f"""
                **{alert['title']}**
                
                📝 {alert['message']}
                
                💡 **Recommended Action:** {alert['action']}
                """)
            elif alert['type'] == 'success':
                st.success(f"""
                **{alert['title']}**
                
                📝 {alert['message']}
                
                💡 **Recommended Action:** {alert['action']}
                """)
            else:
                st.info(f"""
                **{alert['title']}**
                
                📝 {alert['message']}
                """)
        
        # Auto-refresh option
        st.markdown("---")
        if st.button("🔄 Refresh Alerts", use_container_width=True):
            st.rerun()
    
    else:
        st.success("✅ No alerts at this time. All systems optimal!")
        # REMOVED: st.balloons()

else:
    st.error("❌ No data available. Please check your data files.")
    st.info("Make sure daily_data.csv exists in the 'data' folder")

st.markdown("---")
st.caption("RevMax Alert System - 24/7 Monitoring")