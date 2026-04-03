# utils/ai.py
import pandas as pd
import numpy as np
from datetime import datetime

def get_ai_insights(df, events_df=None, room_df=None, use_real_ai=False, api_key=None):
    """Generate AI-powered insights and recommendations"""
    
    if df is None or df.empty:
        return {
            'pricing_advice': "Insufficient data for AI analysis",
            'warnings': [],
            'opportunities': [],
            'summary': "Please provide more historical data",
            'action_items': [],
            'forecast': {}
        }
    
    # Get latest metrics
    latest = df.iloc[-1]
    current_occupancy = latest['Occupancy']
    current_rate = latest['Avg Rate']
    current_revenue = latest['Revenue']
    
    # Calculate trends
    last_7_days = df.tail(7)
    last_14_days = df.tail(14)
    
    avg_occ_7 = last_7_days['Occupancy'].mean()
    avg_occ_14 = last_14_days['Occupancy'].mean() if len(df) >= 14 else avg_occ_7
    occ_trend = avg_occ_7 - avg_occ_14
    
    avg_rate_7 = last_7_days['Avg Rate'].mean()
    avg_rate_14 = last_14_days['Avg Rate'].mean() if len(df) >= 14 else avg_rate_7
    rate_trend = avg_rate_7 - avg_rate_14
    
    # Find best and worst days
    df_copy = df.copy()
    df_copy['DayOfWeek'] = df_copy['Date'].dt.day_name()
    weekly_occ = df_copy.groupby('DayOfWeek')['Occupancy'].mean()
    
    best_day = weekly_occ.idxmax() if not weekly_occ.empty else "Unknown"
    worst_day = weekly_occ.idxmin() if not weekly_occ.empty else "Unknown"
    
    # Generate insights
    insights = {
        'pricing_advice': generate_pricing_advice(current_occupancy, current_rate, occ_trend, rate_trend),
        'warnings': generate_warnings(current_occupancy, occ_trend, df, events_df),
        'opportunities': generate_opportunities(current_occupancy, current_rate, best_day, worst_day, events_df, room_df, weekly_occ),
        'summary': generate_summary(current_occupancy, current_revenue, occ_trend, rate_trend),
        'action_items': generate_action_items(current_occupancy, occ_trend, events_df),
        'forecast': generate_forecast(df)
    }
    
    return insights


def generate_pricing_advice(occupancy, rate, occ_trend, rate_trend):
    """Generate pricing advice based on current metrics"""
    
    advice = []
    
    if occupancy > 0.85:
        advice.append(f"🏨 **Aggressive Pricing Opportunity**: With {occupancy:.0%} occupancy, you can increase rates by 10-15%.")
        advice.append(f"💰 **Rate Optimization**: Current rates ${rate:,.0f} could be raised to ${rate * 1.12:,.0f} based on demand.")
    
    elif occupancy > 0.70:
        advice.append(f"📊 **Strategic Pricing**: At {occupancy:.0%} occupancy, implement modest increases of 5-8%.")
    
    elif occupancy > 0.50:
        advice.append(f"⚖️ **Balanced Approach**: With {occupancy:.0%} occupancy, maintain current rates but add value.")
        
        if occ_trend > 0:
            advice.append(f"📈 **Momentum Building**: Occupancy rising ({occ_trend:+.1%} trend). Prepare for rate increases.")
        else:
            advice.append(f"📉 **Stimulate Demand**: Consider 5-8% discount for advance purchases.")
    
    else:
        advice.append(f"⚠️ **Aggressive Action Needed**: At {occupancy:.0%} occupancy, implement 10-15% discounts immediately.")
    
    return " ".join(advice)


def generate_warnings(occupancy, occ_trend, df, events_df):
    """Generate warning alerts"""
    
    warnings = []
    
    if occupancy < 0.40:
        warnings.append({
            'type': 'critical',
            'message': f'⚠️ CRITICAL: Occupancy at {occupancy:.0%} - 60%+ rooms empty',
            'action': 'Launch emergency promotion within 24 hours'
        })
    elif occupancy < 0.55:
        warnings.append({
            'type': 'warning',
            'message': f'⚠️ Warning: Occupancy below target at {occupancy:.0%}',
            'action': 'Review pricing and increase marketing spend'
        })
    
    if occ_trend < -0.05:
        warnings.append({
            'type': 'warning',
            'message': f'📉 Occupancy declining ({occ_trend:+.1%} trend week-over-week)',
            'action': 'Investigate cause - competitor actions? Seasonal factors?'
        })
    
    return warnings


def generate_opportunities(occupancy, rate, best_day, worst_day, events_df, room_df, weekly_occ):
    """Identify revenue opportunities"""
    
    opportunities = []
    
    if occupancy < 0.60:
        opportunities.append({
            'title': '💰 Dynamic Pricing Opportunity',
            'description': 'Implement yield management - increase rates on high-demand days, discount on low days',
            'potential_impact': '5-10% revenue increase'
        })
    
    if best_day != "Unknown" and worst_day != "Unknown":
        opportunities.append({
            'title': f'📅 Day Optimization',
            'description': f'{best_day} is your strongest day. {worst_day} needs attention.',
            'potential_impact': 'Focus marketing on filling mid-week gaps'
        })
    
    opportunities.append({
        'title': '🔄 Loyalty Program',
        'description': 'Implement discount for direct bookings to reduce OTA commissions',
        'potential_impact': 'Save 15-20% on distribution costs'
    })
    
    return opportunities


def generate_summary(occupancy, revenue, occ_trend, rate_trend):
    """Generate executive summary"""
    
    if occupancy > 0.75:
        performance = "strong"
        outlook = "bullish"
    elif occupancy > 0.55:
        performance = "stable"
        outlook = "neutral"
    else:
        performance = "challenging"
        outlook = "cautious"
    
    summary = f"📊 **Executive Summary**: Your hotel is showing {performance} performance with {occupancy:.0%} occupancy. "
    
    if occ_trend > 0:
        summary += f"Occupancy is trending upward (+{occ_trend:.1%}) which is positive. "
    else:
        summary += f"Occupancy is stable. "
    
    summary += f"Daily revenue is ${revenue:,.0f}. Market outlook is {outlook}."
    
    return summary


def generate_action_items(occupancy, occ_trend, events_df):
    """Generate specific action items"""
    
    actions = []
    
    if occupancy < 0.50:
        actions.append({
            'priority': 'HIGH',
            'action': 'Launch 48-hour flash sale with 15% discount',
            'deadline': 'Today'
        })
    
    if occ_trend < 0:
        actions.append({
            'priority': 'MEDIUM',
            'action': 'Review competitor rates and reposition',
            'deadline': 'This week'
        })
    
    actions.append({
        'priority': 'MEDIUM',
        'action': 'Analyze last 30 days of booking data for patterns',
        'deadline': 'This week'
    })
    
    actions.append({
        'priority': 'LOW',
        'action': 'Update rate parity across all OTAs',
        'deadline': 'Next week'
    })
    
    return actions


def generate_forecast(df):
    """Generate simple forecast for next 7 days"""
    
    if len(df) < 14:
        return {"error": "Need more data for forecast"}
    
    forecast = []
    last_week = df.iloc[-7:].copy()
    
    for i in range(7):
        historical_occ = last_week['Occupancy'].iloc[i]
        variation = np.random.uniform(-0.03, 0.03)
        predicted_occ = min(0.95, max(0.20, historical_occ + variation))
        predicted_rate = last_week['Avg Rate'].iloc[i] * (1 + np.random.uniform(-0.02, 0.02))
        
        forecast.append({
            'day': i + 1,
            'predicted_occupancy': predicted_occ,
            'predicted_rate': predicted_rate,
            'confidence': 'Medium'
        })
    
    return forecast


def get_demo_ai_insights(df, events_df=None, room_df=None):
    """Demo version that always works without API key"""
    return get_ai_insights(df, events_df, room_df, use_real_ai=False)
def calculate_revenue_impact(current_rate, new_rate, occupancy, total_rooms):
    current_rooms_sold = occupancy * total_rooms
    
    # Assume slight drop when price increases
    if new_rate > current_rate:
        new_rooms_sold = current_rooms_sold * 0.95
    else:
        new_rooms_sold = current_rooms_sold * 1.05

    current_revenue = current_rooms_sold * current_rate
    new_revenue = new_rooms_sold * new_rate

    return new_revenue - current_revenue