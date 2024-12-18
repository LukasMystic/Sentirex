import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.utils.class_weight import compute_class_weight
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping
from scikeras.wrappers import KerasClassifier
import tensorflow as tf
import pickle

# Load training data
train_file_path = 'train.xlsx'
train_data = pd.read_excel(train_file_path)

# Define features (Column A is 'text') and labels (Column B is 'sentimen')
X_train = train_data['text']
y_train = train_data['sentimen']

# Convert text data to TF-IDF features
tfidf = TfidfVectorizer(max_features=10000)
X_train_tfidf = tfidf.fit_transform(X_train).toarray()

# Encode labels
label_encoder = LabelEncoder()
y_train_encoded = label_encoder.fit_transform(y_train)
y_train_encoded = to_categorical(y_train_encoded)  # Convert to one-hot encoded format

# Compute class weights
class_weights = compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
class_weights_dict = dict(enumerate(class_weights))

# Define the model creation function for hyperparameter tuning
def create_model(learning_rate=0.001, dropout_rate=0.5):
    model = Sequential([
        Dense(512, activation='relu', input_dim=X_train_tfidf.shape[1]),
        Dropout(dropout_rate),
        Dense(256, activation='relu'),
        Dropout(dropout_rate),
        Dense(len(np.unique(y_train)), activation='softmax')  # Output layer with variable classes
    ])
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model

# Early stopping callback
early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

# Hyperparameter tuning using GridSearchCV
param_grid = {
    'model__learning_rate': [0.001, 0.01],
    'model__dropout_rate': [0.3, 0.5],
    'batch_size': [16, 32],
    'epochs': [10, 20]
}

keras_clf = KerasClassifier(model=create_model, verbose=0)

# GridSearchCV requires passing parameters that are recognized by KerasClassifier
grid_search = GridSearchCV(estimator=keras_clf, param_grid=param_grid, scoring='accuracy', cv=3, verbose=2)
grid_search.fit(X_train_tfidf, y_train_encoded, class_weight=class_weights_dict, callbacks=[early_stopping], validation_split=0.1)

# Save the best model using pickle
best_model = grid_search.best_estimator_
with open('best_model.pkl', 'wb') as f:
    pickle.dump(best_model, f)

# Load the test data
test_file_path = 'test.xlsx'
test_data = pd.read_excel(test_file_path)

# Extract text and true sentiment labels from the test data
X_test = test_data['text']
y_test = test_data['sentimen']

# Convert test data to TF-IDF features
X_test_tfidf = tfidf.transform(X_test).toarray()

# Encode true labels
y_test_encoded = label_encoder.transform(y_test)
y_test_encoded = to_categorical(y_test_encoded)  # Convert to one-hot encoded format

# Load the saved best model
with open('best_model.pkl', 'rb') as f:
    loaded_model = pickle.load(f)

# Predict sentiment using the trained model
y_pred_prob = loaded_model.predict(X_test_tfidf)
y_pred = np.argmax(y_pred_prob, axis=1)

# Convert predictions back to original labels
y_pred_labels = label_encoder.inverse_transform(y_pred)

# Add predictions to the third column in the test data
test_data['AI_prediction'] = y_pred_labels

# Save the test data with predictions to a new Excel file
test_data.to_excel('test_with_predictions.xlsx', index=False)

# Convert class labels to strings for the classification report
target_names = [str(class_label) for class_label in label_encoder.classes_]

# Calculate and print classification metrics
y_test_labels = np.argmax(y_test_encoded, axis=1)
print("Classification Report:")
print(classification_report(y_test_labels, y_pred, target_names=target_names))

# Print accuracy and confusion matrix
accuracy = accuracy_score(y_test_labels, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

conf_matrix = confusion_matrix(y_test_labels, y_pred)
print("Confusion Matrix:")
print(conf_matrix)

