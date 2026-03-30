# utils/kpi.py
import pandas as pd
import numpy as np

def calculate_kpis(df):
    """
    Calculate key performance metrics from daily data
    
    Args:
        df (pd.DataFrame): Daily data with columns: Date, Occupancy, Rooms Sold, 
                          Total Rooms, Avg Rate, Revenue
    
    Returns:
        dict: Dictionary containing all calculated KPIs
    """
    
    if df is None or df.empty:
        return {
            "current_occupancy": 0,
            "current_occupancy_pct": "0%",
            "avg_rate": 0,
            "revenue": 0,
            "rooms_left": 0,
            "rooms_sold": 0,
            "occupancy_trend": 0,
            "occupancy_trend_pct": "0%",
            "rate_trend": 0,
            "rate_trend_pct": "0%",
            "revenue_trend": 0,
            "revenue_trend_pct": "0%",
            "total_rooms": 0,
            "revpar": 0,
            "treasury_index": 100
        }
    
    # Get the latest data point
    latest = df.iloc[-1]
    
    # 1. Current Occupancy
    current_occupancy = latest['Occupancy'] if 'Occupancy' in latest else 0
    current_occupancy_pct = f"{current_occupancy * 100:.1f}%"
    
    # 2. Average Rate (ADR)
    avg_rate = latest['Avg Rate'] if 'Avg Rate' in latest else 0
    
    # 3. Revenue
    revenue = latest['Revenue'] if 'Revenue' in latest else 0
    
    # 4. Rooms Sold and Rooms Left
    rooms_sold = latest['Rooms Sold'] if 'Rooms Sold' in latest else 0
    total_rooms = latest['Total Rooms'] if 'Total Rooms' in latest else 50
    rooms_left = total_rooms - rooms_sold
    
    # 5. Occupancy Trend (compare last 7 days vs previous 7 days)
    if len(df) >= 14:
        last_7_days = df['Occupancy'].iloc[-7:].mean()
        previous_7_days = df['Occupancy'].iloc[-14:-7].mean()
        
        if previous_7_days > 0:
            occupancy_trend = ((last_7_days - previous_7_days) / previous_7_days) * 100
        else:
            occupancy_trend = 0
    else:
        occupancy_trend = 0
    
    occupancy_trend_pct = f"{occupancy_trend:+.1f}%"
    
    # 6. Rate Trend (ADR trend)
    if len(df) >= 14:
        last_7_days_rate = df['Avg Rate'].iloc[-7:].mean()
        previous_7_days_rate = df['Avg Rate'].iloc[-14:-7].mean()
        
        if previous_7_days_rate > 0:
            rate_trend = ((last_7_days_rate - previous_7_days_rate) / previous_7_days_rate) * 100
        else:
            rate_trend = 0
    else:
        rate_trend = 0
    
    rate_trend_pct = f"{rate_trend:+.1f}%"
    
    # 7. Revenue Trend
    if len(df) >= 14:
        last_7_days_rev = df['Revenue'].iloc[-7:].mean()
        previous_7_days_rev = df['Revenue'].iloc[-14:-7].mean()
        
        if previous_7_days_rev > 0:
            revenue_trend = ((last_7_days_rev - previous_7_days_rev) / previous_7_days_rev) * 100
        else:
            revenue_trend = 0
    else:
        revenue_trend = 0
    
    revenue_trend_pct = f"{revenue_trend:+.1f}%"
    
    # Calculate RevPAR (Revenue Per Available Room)
    revpar = revenue / total_rooms if total_rooms > 0 else 0
    
    # Calculate Treasury Index (rate vs competitor)
    competitor_rate = latest.get('Competitor Avg Rate', avg_rate)
    treasury_index = (avg_rate / competitor_rate) * 100 if competitor_rate > 0 else 100
    
    return {
        # Current metrics
        "current_occupancy": current_occupancy,
        "current_occupancy_pct": current_occupancy_pct,
        "avg_rate": avg_rate,
        "revenue": revenue,
        "rooms_left": rooms_left,
        "rooms_sold": rooms_sold,
        "total_rooms": total_rooms,
        
        # Trends
        "occupancy_trend": occupancy_trend,
        "occupancy_trend_pct": occupancy_trend_pct,
        "rate_trend": rate_trend,
        "rate_trend_pct": rate_trend_pct,
        "revenue_trend": revenue_trend,
        "revenue_trend_pct": revenue_trend_pct,
        
        # Additional useful metrics
        "revpar": revpar,
        "treasury_index": treasury_index
    }


def calculate_weekly_summary(df):
    """
    Calculate weekly aggregated metrics
    
    Args:
        df (pd.DataFrame): Daily data
    
    Returns:
        pd.DataFrame: Weekly summary of key metrics
    """
    if df is None or df.empty:
        return pd.DataFrame()
    
    # Create a copy and set date as index
    df_copy = df.copy()
    df_copy['Date'] = pd.to_datetime(df_copy['Date'])
    df_copy.set_index('Date', inplace=True)
    
    # Resample by week
    weekly = df_copy.resample('W').agg({
        'Occupancy': 'mean',
        'Rooms Sold': 'sum',
        'Avg Rate': 'mean',
        'Revenue': 'sum'
    }).round(2)
    
    weekly['Occupancy'] = weekly['Occupancy'] * 100  # Convert to percentage
    weekly['Week'] = weekly.index.strftime('%Y-W%W')
    
    return weekly


def calculate_monthly_summary(df):
    """
    Calculate monthly aggregated metrics
    
    Args:
        df (pd.DataFrame): Daily data
    
    Returns:
        pd.DataFrame: Monthly summary of key metrics
    """
    if df is None or df.empty:
        return pd.DataFrame()
    
    # Create a copy and set date as index
    df_copy = df.copy()
    df_copy['Date'] = pd.to_datetime(df_copy['Date'])
    df_copy.set_index('Date', inplace=True)
    
    # Resample by month
    monthly = df_copy.resample('M').agg({
        'Occupancy': 'mean',
        'Rooms Sold': 'sum',
        'Avg Rate': 'mean',
        'Revenue': 'sum'
    }).round(2)
    
    monthly['Occupancy'] = monthly['Occupancy'] * 100  # Convert to percentage
    monthly['Month'] = monthly.index.strftime('%B %Y')
    
    return monthly