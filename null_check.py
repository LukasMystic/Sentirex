import pandas as pd


df = pd.read_excel('preprocessed.xlsx')


null_values = df[df['sentimen'].isnull()]

if not null_values.empty:
    print("Null values found in 'sentimen' column:")
    print(null_values)
else:
    print("No null values found in 'sentimen' column.")
