# pages/What_If_Simulator.py
import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.kpi import calculate_kpis

st.set_page_config(
    page_title="What-If Simulator - RevMax",
    page_icon="🎮",
    layout="wide"
)

st.title("🎮 What-If Price Simulator")
st.markdown("*Test pricing strategies before implementing them*")
st.markdown("---")

daily_data = st.session_state.get('daily_data', None)

if daily_data is not None and not daily_data.empty:
    
    kpis = calculate_kpis(daily_data)
    
    current_occupancy = kpis['current_occupancy']
    current_rate = kpis['avg_rate']
    current_revenue = kpis['revenue']
    total_rooms = kpis['total_rooms']
    
    # Simulator controls
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📊 Adjust Pricing Strategy")
        
        price_change = st.slider(
            "Price Change Percentage",
            min_value=-30,
            max_value=30,
            value=0,
            step=5,
            help="Increase or decrease your room rates"
        )
        
        demand_elasticity = st.select_slider(
            "Demand Elasticity",
            options=["Very Low", "Low", "Medium", "High", "Very High"],
            value="Medium"
        )
        
        elasticity_map = {"Very Low": 0.3, "Low": 0.5, "Medium": 1.0, "High": 1.5, "Very High": 2.0}
        elasticity = elasticity_map[demand_elasticity]
        
        month = datetime.now().month
        if month in [11, 12, 1]:
            season_factor = 1.2
            st.info("🎄 Peak season detected - demand is less sensitive")
        elif month in [6, 7, 8]:
            season_factor = 0.8
            st.info("☀️ Low season - customers more price sensitive")
        else:
            season_factor = 1.0
    
    # Calculate projections
    price_change_decimal = price_change / 100
    occupancy_impact = price_change_decimal * elasticity * season_factor
    
    if price_change > 0:
        occupancy_change = -occupancy_impact * 0.5
    elif price_change < 0:
        occupancy_change = -occupancy_impact * 0.5
    else:
        occupancy_change = 0
    
    new_occupancy = current_occupancy * (1 + occupancy_change)
    new_occupancy = max(0.1, min(0.98, new_occupancy))
    new_rate = current_rate * (1 + price_change_decimal)
    new_rooms_sold = int(new_occupancy * total_rooms)
    new_revenue = new_rooms_sold * new_rate
    
    revenue_change = new_revenue - current_revenue
    revenue_change_pct = (revenue_change / current_revenue) * 100 if current_revenue > 0 else 0
    
    with col2:
        st.subheader("📈 Projected Results")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Current Revenue", f"${current_revenue:,.0f}")
            st.metric("Current Occupancy", f"{current_occupancy:.1%}")
            st.metric("Current Rate", f"${current_rate:,.0f}")
        
        with col_b:
            st.metric("Projected Revenue", f"${new_revenue:,.0f}",
                     delta=f"{revenue_change:+,.0f} ({revenue_change_pct:+.1f}%)")
            st.metric("Projected Occupancy", f"{new_occupancy:.1%}",
                     delta=f"{(new_occupancy - current_occupancy)*100:+.1f}%")
            st.metric("New Rate", f"${new_rate:,.0f}",
                     delta=f"{price_change:+.0f}%")
    
    st.markdown("---")
    
    # Demand Curve
    st.subheader("📊 Demand Curve Analysis")
    
    price_range = range(-30, 35, 5)
    demand_data = []
    
    for pct in price_range:
        pct_decimal = pct / 100
        impact = pct_decimal * elasticity * season_factor
        occ_change = -impact * 0.5
        occ = current_occupancy * (1 + occ_change)
        occ = max(0.1, min(0.98, occ))
        rate = current_rate * (1 + pct_decimal)
        rooms = int(occ * total_rooms)
        revenue = rooms * rate
        
        demand_data.append({
            'Price Change %': pct,
            'Projected Occupancy': occ * 100,
            'Projected Revenue': revenue
        })
    
    demand_df = pd.DataFrame(demand_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_occ = px.line(demand_df, x='Price Change %', y='Projected Occupancy',
                          title='Price Impact on Occupancy', markers=True)
        fig_occ.add_vline(x=price_change, line_dash="dash", line_color="red")
        fig_occ.update_layout(height=400)
        st.plotly_chart(fig_occ, use_container_width=True)
    
    with col2:
        fig_rev = px.line(demand_df, x='Price Change %', y='Projected Revenue',
                          title='Price Impact on Revenue', markers=True)
        fig_rev.add_vline(x=price_change, line_dash="dash", line_color="red")
        fig_rev.add_hline(y=current_revenue, line_dash="dot", line_color="green")
        fig_rev.update_layout(height=400)
        st.plotly_chart(fig_rev, use_container_width=True)
    
    # Recommendation
    st.markdown("---")
    if revenue_change > 0:
        st.success(f"""
        ### ✅ Recommendation: IMPLEMENT {price_change:+.0f}% PRICE CHANGE
        
        **Expected Impact:** +${revenue_change:,.0f} daily revenue ({revenue_change_pct:.1f}% increase)
        
        **Action Items:**
        1. Update rates in your PMS system
        2. Monitor competitor response
        3. Review impact after 3-5 days
        """)
    elif price_change != 0:
        st.warning(f"""
        ### ⚠️ Recommendation: REVERT TO CURRENT PRICES
        
        A {price_change:+.0f}% price change would reduce revenue by ${abs(revenue_change):,.0f}
        
        **Alternative:** Try a smaller adjustment or add value instead of changing price
        """)
    else:
        st.info("💡 **Try adjusting the price slider** to see potential revenue impacts")

else:
    st.error("No data available. Please check your data files.")

st.markdown("---")
st.caption("RevMax What-If Simulator - Risk-Free Testing")