import pandas as pd

# Load your dataset from an Excel file, skipping the header
df = pd.read_excel('Sa_Tapera_Label_NoEmoticon.xlsx', header=None)

# Check for missing values in the 'sentimen' column (adjust column index accordingly, e.g., column 1)
missing_values = df[1].isna().sum()  # Assuming 'sentimen' is in the second column (index 1)

print(f"Number of missing values in 'sentimen' column: {missing_values}")
