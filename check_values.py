import pandas as pd

# Load your dataset from an Excel file
df = pd.read_excel('preprocessed.xlsx')


valid_values = [0 , 1, 2]


invalid_values = df[~df['sentimen'].isin(valid_values)]

if not invalid_values.empty:
    print("Invalid values found in 'sentimen' column:")
    print(invalid_values['sentimen'].unique())
else:
    print("No invalid values found in 'sentimen' column.")
