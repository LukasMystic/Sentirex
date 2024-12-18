import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.utils.class_weight import compute_class_weight
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as imPipeline
import pickle
import re

def preprocess_text(text):
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^A-Za-z\s]', '', text)
    return text

train_file_path = 'train.xlsx'
train_data = pd.read_excel(train_file_path)

X_train = train_data['text'].apply(preprocess_text)
y_train = train_data['sentimen']

X_train = X_train[X_train.str.split().apply(len).between(3, 200)]
y_train = y_train[X_train.index]

classes = np.array([0, 1, 2])
class_weights = compute_class_weight('balanced', classes=classes, y=y_train)
class_weight_dict = {i: weight for i, weight in zip(classes, class_weights)}

pipeline = imPipeline([
    ('tfidf', TfidfVectorizer(max_df=0.95, min_df=0.01)),
    ('smote', SMOTE()),
    ('svm', SVC(class_weight=class_weight_dict, probability=True))
])

param_grid = {
    'svm__C': [0.1, 1, 10],
    'svm__kernel': ['linear', 'rbf'],
    'svm__gamma': ['scale', 'auto']
}

grid_search = GridSearchCV(pipeline, param_grid, cv=5, n_jobs=-1, verbose=1)
grid_search.fit(X_train, y_train)

best_model = grid_search.best_estimator_

with open('model.pkl', 'wb') as f:
    pickle.dump(best_model, f)

test_file_path = 'test.xlsx'
test_data = pd.read_excel(test_file_path)

X_test = test_data['text'].apply(preprocess_text)
y_test = test_data['sentimen']

X_test_filtered = X_test[X_test.str.split().apply(len).between(3, 200)]
y_test_filtered = y_test[X_test_filtered.index]

y_pred_proba = best_model.predict_proba(X_test_filtered)

sentiment_percentages = []
for prob in y_pred_proba:
    total = sum(prob)
    percentages = {0: (prob[0] / total) * 100, 1: (prob[1] / total) * 100, 2: (prob[2] / total) * 100}
    sentiment_percentages.append(percentages)

test_data['sentiment_percentages'] = None
test_data.loc[X_test_filtered.index, 'sentiment_percentages'] = sentiment_percentages

y_pred_filtered = best_model.predict(X_test_filtered)

test_data['AI_prediction'] = None
test_data.loc[X_test_filtered.index, 'AI_prediction'] = y_pred_filtered

most_frequent_class = y_train.mode()[0]  
test_data['AI_prediction'].fillna(most_frequent_class, inplace=True)

test_data.to_excel('test_with_predictions_and_percentages.xlsx', index=False)

print("Classification Report:")
print(classification_report(y_test_filtered, y_pred_filtered, target_names=['Negative', 'Positive', 'Neutral']))

accuracy = accuracy_score(y_test_filtered, y_pred_filtered)
print(f"Accuracy: {accuracy * 100:.2f}%")

conf_matrix = confusion_matrix(y_test_filtered, y_pred_filtered)
print("Confusion Matrix:")
print(conf_matrix)
