import pandas as pd
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import spacy
import string
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

nlp = spacy.load('xx_ent_wiki_sm')

def preprocess_text(text):
    if not isinstance(text, str):  
        return ""  
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    doc = nlp(text)
    tokens = [token.text for token in doc]
    factory = StopWordRemoverFactory()
    stopword_list = factory.get_stop_words()
    filtered_tokens = [word for word in tokens if word not in stopword_list]
    return ' '.join(filtered_tokens)

df = pd.read_excel('lowercase.xlsx')
df['text'] = df['text'].apply(preprocess_text)

def encode_sentiment(sentiment):
    if sentiment == 'negative':
        return 0
    elif sentiment == 'positive':
        return 1
    elif sentiment == 'neutral':
        return 2
    else:
        return None

df['sentimen'] = df['sentimen'].apply(encode_sentiment)

# Tokenizing visualization
df['token_count'] = df['text'].apply(lambda x: len(x.split()))

# Plotting token count distribution
plt.figure(figsize=(8, 6))
plt.hist(df['token_count'], bins=30, color='purple', edgecolor='black')
plt.title('Token Count Distribution After Preprocessing')
plt.xlabel('Number of Tokens')
plt.ylabel('Frequency')
plt.show()

df.to_excel('preprocessed.xlsx', index=False)

# Visualizing the distribution of sentiments
sentiment_counts = df['sentimen'].value_counts()
sentiment_labels = ['Positive', 'Negative', 'Neutral']

plt.figure(figsize=(8, 6))
plt.bar(sentiment_labels, sentiment_counts, color=['green', 'red', 'blue'])
plt.title('Sentiment Distribution')
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.show()

print("Text preprocessing, token count visualization, label encoding, and sentiment visualization complete. File saved as 'preprocessed.xlsx'.")
