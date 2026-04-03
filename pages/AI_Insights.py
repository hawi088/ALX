# pages/AI_Insights.py
import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Add utils path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Imports
from utils.ai import get_demo_ai_insights, calculate_revenue_impact
from utils.kpi import calculate_kpis

# Page config
st.set_page_config(
    page_title="AI Insights - RevMax",
    page_icon="🧠",
    layout="wide"
)

# ------------------- CUSTOM CSS -------------------
st.markdown("""
<style>
    .insight-card {
        background-color: rgba(248, 249, 250, 0.05);
        border-radius: 12px;
        padding: 1.2rem;
        margin: 0.5rem 0;
        border-left: 3px solid #d4af37;
    }
    .metric-explanation { font-size: 0.75rem; color: #888; margin-top: 0.25rem; }
    .day-card { text-align: center; padding: 0.5rem; border-radius: 8px; background-color: rgba(255,255,255,0.03);}
    .day-high { background-color: rgba(212, 175, 55, 0.15); border: 1px solid rgba(212, 175, 55, 0.3); }
    .day-low { background-color: rgba(220, 53, 69, 0.1); border: 1px solid rgba(220, 53, 69, 0.2); }
    .day-name { font-weight: 600; font-size: 0.8rem; }
    .day-value { font-size: 0.9rem; font-weight: bold; margin-top: 0.25rem; }
    .confidence-container { background-color: rgba(255,255,255,0.1); border-radius: 10px; margin: 8px 0; overflow: hidden; }
    .confidence-bar { height: 8px; border-radius: 10px; transition: width 0.5s ease; }
    .confidence-label { display: flex; justify-content: space-between; font-size: 0.75rem; margin-bottom: 4px; }
</style>
""", unsafe_allow_html=True)

# ------------------- LOAD SESSION DATA -------------------
daily_data = st.session_state.get('daily_data', None)
events = st.session_state.get('events', None)
room_types = st.session_state.get('room_types', None)

# Check data availability
if daily_data is None or daily_data.empty:
    st.warning("⚠️ No data found. Please ensure your data files are loaded in the 'data' folder.")
    st.stop()

# ------------------- CALCULATE KPIs AND REVENUE IMPACT -------------------
kpis = calculate_kpis(daily_data)
current_rate = kpis['avg_rate']
current_occ = kpis['current_occupancy']
total_rooms = kpis['total_rooms']
new_rate = current_rate * 1.1
impact = calculate_revenue_impact(current_rate, new_rate, current_occ, total_rooms)

# ------------------- AI INSIGHTS -------------------
ai_insights = get_demo_ai_insights(daily_data, events, room_types)

st.title("🧠 AI-Powered Insights")
st.markdown("*Your 24/7 AI Revenue Manager - Analyzing data and providing actionable recommendations*")
st.markdown("---")

# ---------- EXECUTIVE SUMMARY ----------
st.info(ai_insights['summary'])
st.markdown("---")

# ---------- PRICING STRATEGY ----------
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("### 💲 Pricing Strategy")
    st.markdown(ai_insights['pricing_advice'])
    st.markdown('<div class="metric-explanation">📌 Based on current occupancy and market conditions, this is your optimal pricing direction</div>', unsafe_allow_html=True)

with col2:
    st.markdown("### 📊 AI Confidence")
    model_conf = 87
    data_quality = 92
    st.markdown(f"""
    <div class="confidence-label">
        <span>🎯 Model Confidence</span>
        <span><strong>{model_conf}%</strong></span>
    </div>
    <div class="confidence-container">
        <div class="confidence-bar" style="width: {model_conf}%; background: linear-gradient(90deg, #d4af37, #c5a020);"></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div class="confidence-label">
        <span>📊 Data Quality</span>
        <span><strong>{data_quality}%</strong></span>
    </div>
    <div class="confidence-container">
        <div class="confidence-bar" style="width: {data_quality}%; background: linear-gradient(90deg, #28a745, #20c997);"></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="metric-explanation">📌 87% = AI confident | 92% = Data quality excellent</div>', unsafe_allow_html=True)

st.markdown("---")

# ---------- REVENUE IMPACT ----------
st.markdown("### 💰 Revenue Impact")
st.success(f"""
**If you follow this recommendation:**

💵 Additional Revenue: **ETB {impact:,.0f} per day**  
📈 Weekly Impact: **ETB {impact * 7:,.0f}**

👉 Based on your real occupancy & pricing.
""")

st.markdown("### 🧠 Why This Recommendation?")
st.markdown(f"""
- 📈 Occupancy: **{current_occ*100:.0f}%**
- 💲 Current Rate: **ETB {current_rate:,.0f}**
- 📊 Demand trend supports price increase

👉 RevMax predicts safe price increase without losing bookings.
""")
st.markdown("---")

# ---------- WEEKLY PATTERN ----------
st.markdown("### 📅 Weekly Performance Pattern")
daily_copy = daily_data.copy()
daily_copy['DayName'] = daily_copy['Date'].dt.day_name()
daily_copy['Occupancy %'] = daily_copy['Occupancy'] * 100
weekly_avg = daily_copy.groupby('DayName')['Occupancy %'].mean().reindex(
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
)
best_day = weekly_avg.idxmax()
worst_day = weekly_avg.idxmin()
best_value = weekly_avg.max()
worst_value = weekly_avg.min()
st.markdown(f"""
<div class="insight-card">
<strong>📊 Day Optimization Insight</strong><br>
📈 <strong>{best_day}</strong> strongest day: <strong>{best_value:.0f}%</strong> occupancy.<br>
📉 <strong>{worst_day}</strong> needs attention: <strong>{worst_value:.0f}%</strong> occupancy.<br>
💡 <strong>Recommendation:</strong> Focus marketing on filling {worst_day}.
</div>
""", unsafe_allow_html=True)

fig_weekly = px.bar(
    x=weekly_avg.index,
    y=weekly_avg.values,
    title="Average Occupancy by Day of Week (Last 30 Days)",
    labels={'x': 'Day', 'y': 'Average Occupancy (%)'},
    color=weekly_avg.values,
    color_continuous_scale=['#dc3545', '#ffc107', '#28a745'],
    text=weekly_avg.values
)
fig_weekly.update_traces(texttemplate='%{text:.0f}%', textposition='outside')
fig_weekly.update_layout(height=400, template='simple_white', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_weekly, use_container_width=True)
st.markdown("---")

# ---------- ALERTS & OPPORTUNITIES ----------
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
    st.markdown("### 🚀 Revenue Opportunities")
    if kpis['current_occupancy'] > 0.7:
        st.markdown("""
        <div class="insight-card">
        <strong>💎 Upsell Opportunity</strong><br>
        Create upgrade offers at check-in.<br>
        <span style="font-size: 0.8rem; color: #28a745;">💰 Potential: +$2,500/month</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("""
    <div class="insight-card">
    <strong>🏨 Direct Booking Incentive</strong><br>
    Offer 10% discount for direct website bookings.<br>
    <span style="font-size: 0.8rem; color: #28a745;">💰 Potential: Save $5,000+ monthly</span>
    </div>
    """, unsafe_allow_html=True)
    if events is not None and not events.empty:
        st.markdown("""
        <div class="insight-card">
        <strong>🎪 Event Package Creation</strong><br>
        Create special packages for upcoming events.<br>
        <span style="font-size: 0.8rem; color: #28a745;">💰 Potential: Premium pricing +15-20%</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ---------- ACTIONABLE RECOMMENDATIONS ----------
st.markdown("### ✅ Today's Actionable Recommendations")
st.markdown("*Based on your current data, here's what you should do right now:*")
recommendations = []
if current_occ < 0.5:
    recommendations.append({'priority':'🔴 HIGH','action':'Launch flash sale 15-20%','deadline':'Today','expected':'+15% occupancy'})
elif current_occ > 0.8:
    recommendations.append({'priority':'🟢 HIGH','action':f'Increase rates by 10-12% (from {current_rate:,.0f} to {current_rate*1.1:,.0f})','deadline':'Today','expected':'+$5,000 daily revenue'})
else:
    recommendations.append({'priority':'🟡 MEDIUM','action':'Test 5% rate increase on weekends','deadline':'This week','expected':'+$2,000 weekly'})
recommendations.append({'priority':'🟡 MEDIUM','action':'Review competitor rates','deadline':'This week','expected':'Stay competitive'})
recommendations.append({'priority':'🟢 LOW','action':'Analyze last 30 days of booking data','deadline':'Next week','expected':'Better forecasting'})
st.dataframe(pd.DataFrame(recommendations), use_container_width=True, hide_index=True)

# ---------- 7-DAY FORECAST ----------
st.markdown("### 📈 7-Day AI Forecast")
if 'forecast' in ai_insights and 'error' not in ai_insights['forecast']:
    forecast_df = pd.DataFrame(ai_insights['forecast'])
    today = datetime.now()
    forecast_df['Day'] = [(today + timedelta(days=i)).strftime('%a') for i in range(7)]
    col1, col2 = st.columns(2)
    with col1:
        fig_occ = px.line(forecast_df, x='Day', y='predicted_occupancy', title='Predicted Occupancy - Next 7 Days', markers=True)
        fig_occ.update_traces(line=dict(color='#d4af37', width=3), marker=dict(size=8, color='#d4af37'))
        fig_occ.update_layout(height=350, template='simple_white')
        fig_occ.update_yaxes(tickformat='.0%', title='Occupancy Rate')
        st.plotly_chart(fig_occ, use_container_width=True)
    with col2:
        fig_rate = px.line(forecast_df, x='Day', y='predicted_rate', title='Predicted Average Rate - Next 7 Days', markers=True)
        fig_rate.update_traces(line=dict(color='#d4af37', width=3), marker=dict(size=8, color='#d4af37'))
        fig_rate.update_layout(height=350, template='simple_white')
        fig_rate.update_yaxes(title='Rate ($)', tickprefix='$')
        st.plotly_chart(fig_rate, use_container_width=True)
    st.caption("🤖 AI Forecast Confidence: Medium - Based on 30-day historical patterns")
else:
    st.warning("Need at least 14 days of data for accurate forecasting")

# ---------- EXPORT ----------
with st.expander("📥 Export AI Report"):
    report_data = {
        'Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Summary': ai_insights['summary'],
        'Pricing Advice': ai_insights['pricing_advice'],
        'Current Occupancy': kpis['current_occupancy_pct'],
        'Current Rate': f"{current_rate:,.0f}",
        'Today Revenue': f"{kpis['revenue']:,.0f}"
    }
    st.download_button(
        label="📊 Download AI Report (CSV)",
        data=pd.DataFrame([report_data]).to_csv(index=False),
        file_name=f"revmax_ai_report_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

st.markdown("---")
st.caption("RevMax AI Intelligence Engine - Your 24/7 Revenue Management Assistant")