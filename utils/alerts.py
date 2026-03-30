# utils/alerts.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_alerts(df, events_df, room_df=None):
    """Generate intelligent alerts based on data patterns"""
    
    alerts = []
    
    if df is None or df.empty:
        return alerts
    
    # Get latest data
    latest = df.iloc[-1]
    current_occupancy = latest['Occupancy']
    current_rate = latest['Avg Rate']
    
    # Get recent trends
    last_7_days = df.tail(7)
    last_14_days = df.tail(14)
    
    avg_occupancy_7 = last_7_days['Occupancy'].mean()
    avg_occupancy_14 = last_14_days['Occupancy'].mean() if len(df) >= 14 else avg_occupancy_7
    
    # Occupancy Alerts
    if current_occupancy < 0.3:
        alerts.append({
            'title': '🔴 CRITICAL: Very Low Occupancy',
            'message': f'Current occupancy is only {current_occupancy:.1%}. Immediate action needed!',
            'type': 'critical',
            'priority': 1,
            'action': 'Consider aggressive discounts or marketing push',
            'metric': 'Occupancy',
            'value': f'{current_occupancy:.1%}'
        })
    elif current_occupancy < 0.5:
        alerts.append({
            'title': '🟠 WARNING: Low Occupancy',
            'message': f'Occupancy at {current_occupancy:.1%} is below target.',
            'type': 'warning',
            'priority': 2,
            'action': 'Review pricing strategy and increase marketing',
            'metric': 'Occupancy',
            'value': f'{current_occupancy:.1%}'
        })
    
    # Occupancy drop alert
    if len(df) >= 7:
        occupancy_drop = avg_occupancy_7 - avg_occupancy_14
        if occupancy_drop > 0.15:
            alerts.append({
                'title': '📉 SIGNIFICANT DROP: Occupancy Declining',
                'message': f'Occupancy dropped {occupancy_drop:.1%} compared to last week.',
                'type': 'warning',
                'priority': 2,
                'action': 'Investigate cause - competitor actions? Market changes?',
                'metric': 'Occupancy Trend',
                'value': f'{occupancy_drop:.1%} drop'
            })
    
    # Rate vs Competitor
    if 'Competitor Avg Rate' in df.columns:
        competitor_rate = latest['Competitor Avg Rate']
        rate_gap = current_rate - competitor_rate
        
        if rate_gap > competitor_rate * 0.15:
            alerts.append({
                'title': '⚠️ PRICE GAP: Above Competitors',
                'message': f'Your rate (${current_rate:,.0f}) is {rate_gap/competitor_rate:.0%} above competitors.',
                'type': 'warning',
                'priority': 2,
                'action': 'Review value proposition or consider slight reduction',
                'metric': 'Rate Gap',
                'value': f'+{rate_gap/competitor_rate:.0%}'
            })
    
    # Event-based alerts
    if events_df is not None and not events_df.empty:
        date_column = None
        for col in events_df.columns:
            if col.lower() in ['date', 'event date']:
                date_column = col
                break
        
        if date_column:
            today = pd.Timestamp.now().normalize()
            
            for idx, event in events_df.iterrows():
                try:
                    event_date = pd.to_datetime(event[date_column]).normalize()
                    days_until = (event_date - today).days
                    event_name = event['Event Name'] if 'Event Name' in event.columns else str(event[date_column])
                    
                    if 0 <= days_until <= 7:
                        alerts.append({
                            'title': '🎉 EVENT APPROACHING: Price Opportunity!',
                            'message': f'{event_name} in {days_until} days. Expect high demand!',
                            'type': 'success',
                            'priority': 1,
                            'action': 'INCREASE RATES NOW - Strong demand expected',
                            'metric': 'Event',
                            'value': event_name
                        })
                except:
                    pass
    
    return alerts


def get_alert_summary(df, events_df, room_df=None):
    """Get summary statistics about current alerts"""
    all_alerts = get_alerts(df, events_df, room_df)
    
    summary = {
        'total': len(all_alerts),
        'critical': len([a for a in all_alerts if a['type'] == 'critical']),
        'warning': len([a for a in all_alerts if a['type'] == 'warning']),
        'success': len([a for a in all_alerts if a['type'] == 'success']),
        'info': len([a for a in all_alerts if a['type'] == 'info']),
        'high_priority': len([a for a in all_alerts if a['priority'] == 1]),
        'urgent_actions': [a['title'] for a in all_alerts if a['priority'] == 1]
    }
    
    return summary


def get_critical_alerts(df, events_df, room_df=None):
    """Get only critical and high-priority alerts"""
    all_alerts = get_alerts(df, events_df, room_df)
    critical = [alert for alert in all_alerts if alert['priority'] <= 2]
    return critical