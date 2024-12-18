import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Excel file
file_path = 'preprocessed.xlsx'
data = pd.read_excel(file_path)

# Count the occurrences of 0, 1, and 2 in the 'sentimen' column (Column B)
sentiment_counts = data['sentimen'].value_counts()

# Map the values to their labels
sentiment_labels = {0: 'Negative', 1: 'Positive', 2: 'Neutral'}
sentiment_mapped = sentiment_counts.rename(index=sentiment_labels)

# Print the count of each sentiment
print(sentiment_mapped)

# Bar Chart
plt.figure(figsize=(8, 6))
sns.barplot(x=sentiment_mapped.index, y=sentiment_mapped.values, palette='Blues')
plt.title('Sentiment Distribution')
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.show()

# Pie Chart
plt.figure(figsize=(6, 6))
plt.pie(sentiment_mapped.values, labels=sentiment_mapped.index, autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99'])
plt.title('Sentiment Distribution')
plt.show()
