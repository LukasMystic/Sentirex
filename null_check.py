import pandas as pd

# Load your dataset from an Excel file
df = pd.read_excel('preprocessed.xlsx')

# Check for any null values in the 'sentimen' column
null_values = df[df['sentimen'].isnull()]

if not null_values.empty:
    print("Null values found in 'sentimen' column:")
    print(null_values)
else:
    print("No null values found in 'sentimen' column.")
