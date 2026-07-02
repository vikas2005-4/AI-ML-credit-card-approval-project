import os
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib


def load_dataset(path):
    if not os.path.exists(path):
        # attempt to copy from repository root dataset
        root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'dataset', 'credit_card.csv'))
        if os.path.exists(root_path):
            path = root_path
        else:
            raise FileNotFoundError(f"Dataset not found at {path} or {root_path}")
    return pd.read_csv(path)


def basic_cleaning(df):
    df = df.copy()
    # strip column names
    df.columns = [c.strip() for c in df.columns]
    return df


def build_preprocessor(categorical_features, numerical_features):
    # Use `sparse_output` for newer scikit-learn, fallback to `sparse` if needed
    try:
        encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    except TypeError:
        encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
    cat_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', encoder)
    ])

    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    preprocessor = ColumnTransformer([
        ('num', num_pipeline, numerical_features),
        ('cat', cat_pipeline, categorical_features)
    ])
    return preprocessor


def fit_and_save_preprocessor(df, categorical_features, numerical_features, out_dir):
    preprocessor = build_preprocessor(categorical_features, numerical_features)
    preprocessor.fit(df[categorical_features + numerical_features])
    os.makedirs(out_dir, exist_ok=True)
    joblib.dump(preprocessor, os.path.join(out_dir, 'preprocessor.pkl'))
    return preprocessor
