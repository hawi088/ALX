# utils/data_loader.py
import pandas as pd
import os

# Get the absolute path to the project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_daily_data():
    """
    Load daily performance data from CSV
    
    Returns:
        pd.DataFrame: Daily occupancy, revenue, and rate data
    """
    file_path = os.path.join(PROJECT_ROOT, 'data', 'daily_data.csv')
    try:
        df = pd.read_csv(file_path)
        # Convert Date column to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        # Clean up Occupancy column (remove % sign and convert to float)
        if df['Occupancy'].dtype == 'object':
            df['Occupancy'] = df['Occupancy'].str.rstrip('%').astype('float') / 100
        return df
    except FileNotFoundError:
        print(f"Error: Could not find {file_path}")
        return None
    except Exception as e:
        print(f"Error loading daily data: {e}")
        return None

def load_room_types():
    """
    Load room type configuration from CSV
    
    Returns:
        pd.DataFrame: Room type inventory and pricing data
    """
    file_path = os.path.join(PROJECT_ROOT, 'data', 'room_types.csv')
    try:
        df = pd.read_csv(file_path)
        # Clean up rate columns (remove commas and convert to numeric)
        rate_columns = ['Base Rate', 'High Season Rate', 'Low Season Rate']
        for col in rate_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace(',', '').astype(float)
        return df
    except FileNotFoundError:
        print(f"Error: Could not find {file_path}")
        return None
    except Exception as e:
        print(f"Error loading room types: {e}")
        return None

def load_events():
    """
    Load upcoming events data from CSV
    
    Returns:
        pd.DataFrame: Future events with dates and expected impact
    """
    file_path = os.path.join(PROJECT_ROOT, 'data', 'upcoming_events.csv')
    try:
        df = pd.read_csv(file_path)
        # Convert Date column to datetime
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
        return df
    except FileNotFoundError:
        print(f"Error: Could not find {file_path}")
        return None
    except Exception as e:
        print(f"Error loading events: {e}")
        return None