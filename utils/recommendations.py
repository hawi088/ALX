# utils/recommendations.py
import pandas as pd
import numpy as np

def get_room_recommendations(room_df, daily_df):
    """
    Generate smart pricing recommendations based on occupancy and performance
    
    Args:
        room_df (pd.DataFrame): Room types data with counts and rates
        daily_df (pd.DataFrame): Daily performance data
    
    Returns:
        pd.DataFrame: Recommendations for each room type
    """
    
    if room_df is None or room_df.empty:
        return pd.DataFrame()
    
    if daily_df is None or daily_df.empty:
        return pd.DataFrame()
    
    # Get current occupancy from latest day
    current_occupancy = daily_df['Occupancy'].iloc[-1]
    
    # Get competitor rate
    competitor_rate = daily_df['Competitor Avg Rate'].iloc[-1] if 'Competitor Avg Rate' in daily_df.columns else None
    
    recommendations = []
    
    for idx, room in room_df.iterrows():
        room_type = room['Room Type']
        
        # Skip if it's a total row
        if room_type == 'Total' or pd.isna(room_type):
            continue
        
        # Get room counts and rates
        room_count = room['Count'] if 'Count' in room else 0
        base_rate = room['Base Rate'] if 'Base Rate' in room else 0
        high_season_rate = room['High Season Rate'] if 'High Season Rate' in room else 0
        low_season_rate = room['Low Season Rate'] if 'Low Season Rate' in room else 0
        
        # Determine current rate
        current_rate = high_season_rate if current_occupancy > 0.8 else (low_season_rate if current_occupancy < 0.5 else base_rate)
        
        # Initialize recommendation variables
        recommended_rate = current_rate
        change_percentage = 0
        action = "Maintain"
        reason = ""
        expected_impact = 0
        
        # Pricing Logic
        
        # Rule 1: High occupancy (>80%) - Increase prices
        if current_occupancy > 0.8:
            if room_type == "Standard":
                recommended_rate = current_rate * 1.12
                action = "Increase Price"
                reason = f"High occupancy ({current_occupancy:.1%}) - strong demand"
                change_percentage = 12
                expected_impact = (recommended_rate - current_rate) * room_count * current_occupancy
                
            elif room_type == "Deluxe":
                recommended_rate = current_rate * 1.10
                action = "Increase Price"
                reason = f"High occupancy ({current_occupancy:.1%}) - premium demand"
                change_percentage = 10
                expected_impact = (recommended_rate - current_rate) * room_count * current_occupancy
                
            elif room_type == "Suite":
                recommended_rate = current_rate * 1.08
                action = "Increase Price"
                reason = f"High occupancy ({current_occupancy:.1%}) - luxury demand strong"
                change_percentage = 8
                expected_impact = (recommended_rate - current_rate) * room_count * current_occupancy
        
        # Rule 2: Low occupancy (<50%) - Decrease prices
        elif current_occupancy < 0.5:
            if room_type == "Standard":
                recommended_rate = current_rate * 0.88
                action = "Decrease Price"
                reason = f"Low occupancy ({current_occupancy:.1%}) - need to stimulate demand"
                change_percentage = -12
                expected_impact = (recommended_rate - current_rate) * room_count * current_occupancy
                
            elif room_type == "Deluxe":
                recommended_rate = current_rate * 0.90
                action = "Decrease Price"
                reason = f"Low occupancy ({current_occupancy:.1%}) - improve competitiveness"
                change_percentage = -10
                expected_impact = (recommended_rate - current_rate) * room_count * current_occupancy
                
            elif room_type == "Suite":
                recommended_rate = current_rate * 0.85
                action = "Discount - Fill Suites"
                reason = f"Very low occupancy ({current_occupancy:.1%}) - fill high-value inventory"
                change_percentage = -15
                expected_impact = (recommended_rate - current_rate) * room_count * current_occupancy
        
        # Rule 3: Medium occupancy (50-80%) - Strategic adjustments
        elif 0.5 <= current_occupancy <= 0.8:
            if competitor_rate:
                rate_gap_percentage = ((current_rate - competitor_rate) / competitor_rate) * 100
                
                if rate_gap_percentage > 15:
                    recommended_rate = current_rate * 0.95
                    action = "Slight Decrease"
                    reason = f"Price {rate_gap_percentage:.0f}% above competitor"
                    change_percentage = -5
                    expected_impact = (recommended_rate - current_rate) * room_count * current_occupancy
                    
                elif rate_gap_percentage < -10:
                    recommended_rate = current_rate * 1.05
                    action = "Slight Increase"
                    reason = f"Price {abs(rate_gap_percentage):.0f}% below competitor"
                    change_percentage = 5
                    expected_impact = (recommended_rate - current_rate) * room_count * current_occupancy
                else:
                    action = "Maintain"
                    reason = "Price competitive with market"
            else:
                action = "Maintain"
                reason = "Stable occupancy - monitor trends"
        
        # Round recommended rate
        recommended_rate = round(recommended_rate / 10) * 10
        
        # Add recommendation
        recommendations.append({
            'Room Type': room_type,
            'Current Rate': f"${current_rate:,.0f}",
            'Recommended Rate': f"${recommended_rate:,.0f}",
            'Change': f"{change_percentage:+.0f}%",
            'Action': action,
            'Reason': reason,
            'Expected Daily Impact': f"${expected_impact:,.0f}" if expected_impact != 0 else "Monitor",
            'Priority': get_priority(change_percentage, current_occupancy, room_type)
        })
    
    return pd.DataFrame(recommendations)


def get_priority(change_percentage, occupancy, room_type):
    """Determine priority level for recommendation"""
    if abs(change_percentage) >= 10:
        return "🔴 High"
    elif abs(change_percentage) >= 5:
        return "🟡 Medium"
    else:
        return "🟢 Low"


def get_urgent_recommendations(room_df, daily_df):
    """Get only high-priority recommendations"""
    all_recs = get_room_recommendations(room_df, daily_df)
    if not all_recs.empty:
        high_priority = all_recs[all_recs['Priority'].str.contains('High')]
        return high_priority
    return pd.DataFrame()


def calculate_savings_opportunity(room_df, daily_df):
    """Calculate total revenue opportunity from recommendations"""
    recs = get_room_recommendations(room_df, daily_df)
    
    if recs.empty:
        return {
            'total_opportunity': 0,
            'high_priority_count': 0,
            'avg_change': 0
        }
    
    total_opportunity = 0
    for impact in recs['Expected Daily Impact']:
        if impact != 'Monitor':
            try:
                value = int(impact.replace('$', '').replace(',', ''))
                total_opportunity += value
            except:
                pass
    
    high_priority_count = len(recs[recs['Priority'].str.contains('High')])
    
    changes = []
    for change in recs['Change']:
        if change != 'Monitor':
            try:
                num = float(change.replace('%', '').replace('+', ''))
                changes.append(abs(num))
            except:
                pass
    
    avg_change = sum(changes) / len(changes) if changes else 0
    
    return {
        'total_opportunity': total_opportunity,
        'high_priority_count': high_priority_count,
        'avg_change': avg_change
    }