import pandas as pd
import re
import glob
import os
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier


def preprocess(pw):
    """
    Normalize the password: convert to string, lowercase, 
    and strip non-alphanumeric chars.
    """
    pw = str(pw)
    return re.sub(r'[^a-zA-Z0-9]', '', pw.lower())


# Map strength labels based on filename keywords
strength_map = {
    'very_weak': 0,
    'weak': 1,
    'average': 2,
    'strong': 3,
    'very_strong': 4
}


def load_and_prepare_data(dataset_path='dataset'):
    """
    Load all pwlds_*.csv files, assign strength labels from filename, preprocess passwords.
    """
    pattern = os.path.join(dataset_path, 'pwlds_*.csv')
    csv_files = glob.glob(pattern)
    dataframes = []

    for filepath in csv_files:
        fname = os.path.basename(filepath).lower()
        # Determine label from filename
        label = None
        for key, val in strength_map.items():
            if key in fname:
                label = val
                break
        if label is None:
            print(f"⚠️ Skipping {filepath}: cannot determine strength label.")
            continue

        # Read CSV assuming single-column of passwords
        df = pd.read_csv(filepath,
                         header=None,
                         names=['password'],
                         dtype=str,
                         low_memory=False)
        df['strength'] = label
        dataframes.append(df)

    if not dataframes:
        raise ValueError("❌ No valid password datasets found.")

    data = pd.concat(dataframes, ignore_index=True)
    # Preprocess
    data['password'] = data['password'].apply(preprocess)

    X = data['password']
    y = data['strength']
    return X, y


def train_and_save_model(X, y, dataset_path='dataset'):
    """
    Train a RandomForest on character n-grams and save model + vectorizer.
    """
    vectorizer = CountVectorizer(analyzer='char', ngram_range=(2, 3))
    X_vec = vectorizer.fit_transform(X)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_vec, y)

    os.makedirs(dataset_path, exist_ok=True)
    joblib.dump(model, os.path.join(dataset_path, 'model.pkl'))
    joblib.dump(vectorizer, os.path.join(dataset_path, 'vectorizer.pkl'))

    return model, vectorizer


# Execute training pipeline
X, y = load_and_prepare_data()
model, vectorizer = train_and_save_model(X, y)

# Reload to ensure consistency
model = joblib.load(os.path.join('dataset', 'model.pkl'))
vectorizer = joblib.load(os.path.join('dataset', 'vectorizer.pkl'))


def predict_strength(password):
    """
    Predict strength category (0-4) for a given password string.
    """
    pw = preprocess(password)
    vec = vectorizer.transform([pw])
    return int(model.predict(vec)[0])
