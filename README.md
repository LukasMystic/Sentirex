# AI Model and Website Implementation Repository

This repository contains two main branches:

- **`main` branch**: Hosts the AI model implementation.
- **`master` branch**: Contains the website implementation that utilizes the AI model.

## AI Model Overview (Main Branch)
The AI model in the `main` branch performs text classification using machine learning techniques. The workflow includes preprocessing, feature extraction, oversampling for imbalanced data, hyperparameter tuning, and model evaluation.

### Libraries Used

Below is an explanation of the libraries used in this project:

- **`pandas`**:
  - Provides data manipulation and analysis capabilities, such as handling tabular data in DataFrames.

- **`numpy`**:
  - Offers support for high-performance mathematical operations and array handling.

- **`scikit-learn`**:
  - `GridSearchCV`: Performs hyperparameter tuning to find the best model configuration.
  - `TfidfVectorizer`: Converts text data into numerical features using Term Frequency-Inverse Document Frequency.
  - `SVC`: Support Vector Classifier for text classification.
  - `Pipeline`: Constructs a machine learning pipeline to streamline preprocessing and model training.
  - `classification_report`, `accuracy_score`, `confusion_matrix`: Tools for evaluating model performance.
  - `compute_class_weight`: Helps handle imbalanced datasets by calculating class weights.

- **`imbalanced-learn` (`imblearn`)**:
  - `SMOTE`: Synthetic Minority Oversampling Technique to balance the dataset.
  - `Pipeline`: Allows integration of oversampling and model training in a single pipeline.

- **`pickle`**:
  - Used for serializing and saving the trained model for later use.

- **`re`**:
  - Facilitates regular expression operations for text preprocessing.

- **`Sastrawi`**:
  - `StopWordRemoverFactory`: A library for Indonesian language text processing, specifically for removing stop words.

- **`spacy`**:
  - A powerful NLP library used for text preprocessing, tokenization, and lemmatization.

- **`string`**:
  - Provides utility functions to process and manipulate strings, such as removing punctuation.

- **`sklearn.preprocessing.LabelEncoder`**:
  - Encodes target labels into numeric format.

- **`matplotlib.pyplot`**:
  - Used for creating visualizations such as confusion matrices or performance plots.

### Usage Instructions
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Switch to the `main` branch:
   ```bash
   git checkout main
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the AI model script:
   ```bash
   python train_model.py
   ```
5. The trained model will be saved as a `.pkl` file for integration with the website.

## Website Overview (Master Branch)
The `master` branch contains the implementation of a website that utilizes the trained AI model from the `main` branch. The website provides an interface for users to input data and receive predictions.

### Website Features
- User-friendly interface for data input.
- Backend integration with the AI model for predictions.
- Visualizations of model results (optional).

### Usage Instructions
1. Switch to the `master` branch:
   ```bash
   git checkout master
   ```
2. Install necessary dependencies for the website (refer to the `requirements.txt` file).
3. Run the website locally:
   ```bash
   python app.py
   ```
4. Open the website in your browser at `http://localhost:5000`.

## Contributions
Feel free to contribute to the project by submitting issues or creating pull requests.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---
For any questions, please contact the repository maintainer.
