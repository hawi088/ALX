# pages/Analytics.py
import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="Analytics - RevMax",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Advanced Analytics")
st.markdown("*Deep dive into your hotel's performance data*")
st.markdown("---")

daily_data = st.session_state.get('daily_data', None)

if daily_data is not None and not daily_data.empty:
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        min_date = daily_data['Date'].min().date()
        max_date = daily_data['Date'].max().date()
        date_range = st.date_input("Select Date Range", value=(min_date, max_date))
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_data = daily_data[
            (daily_data['Date'].dt.date >= start_date) & 
            (daily_data['Date'].dt.date <= end_date)
        ]
    else:
        filtered_data = daily_data
    
    st.markdown("---")
    
    # Correlation Analysis
    st.subheader("🔍 Correlation Analysis")
    
    corr_matrix = filtered_data[['Occupancy', 'Avg Rate', 'Revenue', 'Rooms Sold']].corr()
    
    fig_corr = px.imshow(corr_matrix, text_auto=True, aspect="auto",
                         title="Metric Correlations",
                         color_continuous_scale='RdBu')
    fig_corr.update_layout(height=500)
    st.plotly_chart(fig_corr, use_container_width=True)
    
    st.markdown("---")
    
    # Distribution Analysis
    st.subheader("📊 Distribution Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_hist_occ = px.histogram(filtered_data, x='Occupancy', nbins=20,
                                     title='Occupancy Distribution',
                                     labels={'Occupancy': 'Occupancy Rate'},
                                     color_discrete_sequence=['blue'])
        fig_hist_occ.update_layout(height=400)
        fig_hist_occ.update_xaxes(tickformat='.0%')
        st.plotly_chart(fig_hist_occ, use_container_width=True)
    
    with col2:
        fig_hist_rate = px.histogram(filtered_data, x='Avg Rate', nbins=20,
                                     title='Rate Distribution',
                                     labels={'Avg Rate': 'Average Rate ($)'},
                                     color_discrete_sequence=['green'])
        fig_hist_rate.update_layout(height=400)
        st.plotly_chart(fig_hist_rate, use_container_width=True)
    
    st.markdown("---")
    
    # Scatter Plot Matrix
    st.subheader("📉 Multi-Dimensional Analysis")
    
    scatter_vars = st.multiselect(
        "Select variables to analyze",
        ['Occupancy', 'Avg Rate', 'Revenue', 'Rooms Sold'],
        default=['Occupancy', 'Avg Rate', 'Revenue']
    )
    
    if len(scatter_vars) >= 2:
        fig_scatter = px.scatter_matrix(
            filtered_data[scatter_vars],
            dimensions=scatter_vars,
            title="Variable Relationships",
            height=600
        )
        fig_scatter.update_layout(template='simple_white')
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.markdown("---")
    
    # Summary Statistics
    st.subheader("📋 Summary Statistics")
    
    stats = filtered_data[['Occupancy', 'Avg Rate', 'Revenue', 'Rooms Sold']].describe()
    st.dataframe(stats, use_container_width=True)

else:
    st.error("No data available. Please check your data files.")

st.markdown("---")
st.caption("RevMax Advanced Analytics")