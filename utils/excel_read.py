import pandas as pd

def read_test_data(file_path):
    # Read the Excel file without skipping any rows
    try:
        data = pd.read_excel(file_path)
        print("Data read from Excel file:\n", data)  # Print the data to verify
        print("Column names in the data:", data.columns.tolist())  # Print the column names to verify
        return data
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error
