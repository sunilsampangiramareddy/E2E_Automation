import pandas as pd


def is_valid_data(value):
    if pd.notna(value):  # Check if it's not NaN or None
        value_str = str(value).strip()  # Convert to string and remove spaces
        return bool(value_str)  # True if not empty
    return False  # If NaN, return False
