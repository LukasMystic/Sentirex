import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = 'preprocessed.xlsx'
data = pd.read_excel(file_path)
sentiment_counts = data['sentimen'].value_counts()

sentiment_labels = {0: 'Negative', 1: 'Positive', 2: 'Neutral'}
sentiment_mapped = sentiment_counts.rename(index=sentiment_labels)
print(sentiment_mapped)

plt.figure(figsize=(8, 6))
sns.barplot(x=sentiment_mapped.index, y=sentiment_mapped.values, palette='Blues')
plt.title('Sentiment Distribution')
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.show()

plt.figure(figsize=(6, 6))
plt.pie(sentiment_mapped.values, labels=sentiment_mapped.index, autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99'])
plt.title('Sentiment Distribution')
plt.show()
