import pandas as pd
import math

def split_data_from_excel(file_path):
    # Read the data from Excel
    data = pd.read_excel(file_path)
    
    # Calculate the 70% split (round down)
    split_index = math.floor(0.7 * len(data))
    
    # Get the first 70% of the data
    data_70 = data.iloc[:split_index]
    
    # Get the remaining 30% of the data
    data_30 = data.iloc[split_index:]
    
    return data_70, data_30

# Example usage
file_path = 'preprocessed.xlsx'
data_70, data_30 = split_data_from_excel(file_path)

# Save the 70% split to 'train.xlsx'
data_70.to_excel('train.xlsx', index=False)

# Save the 30% split to 'test.xlsx'
data_30.to_excel('test.xlsx', index=False)

print("First 70% of the data saved to train.xlsx.")
print("Remaining 30% of the data saved to test.xlsx.")
