import pandas as pd

# Load the Excel file
file_path = 'Sa_Tapera_Label_NoEmoticon.xlsx'
df = pd.read_excel(file_path)

print("Column names:", df.columns)

correct_column_name = 'text'  

df_no_duplicates = df[df.duplicated(subset=[correct_column_name], keep=False) == False]


df_no_duplicates.to_excel('no_duplicate.xlsx', index=False)

print("Rows with duplicates in the specified column have been removed, including the entire row.")
