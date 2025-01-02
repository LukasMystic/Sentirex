import pandas as pd

df = pd.read_excel('Sa_Tapera_Label_NoEmoticon.xlsx', header=None)

missing_values = df[1].isna().sum() 

print(f"Number of missing values in 'sentimen' column: {missing_values}")
