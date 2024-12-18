import pandas as pd

# Load the Excel file
file_path = 'no_duplicate.xlsx'
df = pd.read_excel(file_path)


df['text'] = df['text'].str.lower()


df.to_excel('lowercase.xlsx', index=False)

print("All text in the 'text' column has been converted to lowercase.")
