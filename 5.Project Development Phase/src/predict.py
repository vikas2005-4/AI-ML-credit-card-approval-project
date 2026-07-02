import os
import joblib
import numpy as np
import pandas as pd

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
MODELS_DIR = os.path.join(PROJECT_DIR, 'models')

DATASET_PATH = os.path.join(PROJECT_DIR, 'dataset', 'credit_card.csv')


def load_artifacts():
    preprocessor = joblib.load(os.path.join(MODELS_DIR, 'preprocessor.pkl'))
    model = joblib.load(os.path.join(MODELS_DIR, 'best_model.pkl'))
    return preprocessor, model


def predict_from_input(input_dict):
    preprocessor, model = load_artifacts()

    # load training dataset to infer expected columns and sensible defaults
    if os.path.exists(DATASET_PATH):
        train_df = pd.read_csv(DATASET_PATH)
    else:
        train_df = None

    target = 'Approval_Status'
    if train_df is not None:
        expected_cats = [c for c in train_df.select_dtypes(include=['object']).columns if c != target]
        expected_nums = [c for c in train_df.select_dtypes(include=['int64', 'float64']).columns if c != target]
        expected_cols = expected_cats + expected_nums
    else:
        # fallback: use keys from input
        expected_cols = list(input_dict.keys())

    # build input row filling missing values with median/mode from training data
    row = {}
    for col in expected_cols:
        if col in input_dict and input_dict[col] != '':
            row[col] = input_dict[col]
        else:
            if train_df is not None and col in train_df.columns:
                if col in expected_nums:
                    row[col] = float(train_df[col].median())
                else:
                    modes = train_df[col].mode()
                    row[col] = modes.iloc[0] if not modes.empty else ''
            else:
                row[col] = np.nan

    df = pd.DataFrame([row], columns=expected_cols)

    # ensure numeric columns are numeric
    for col in expected_nums if train_df is not None else []:
        try:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        except Exception:
            pass

    X = preprocessor.transform(df)
    prob = model.predict_proba(X)[0, 1] if hasattr(model, 'predict_proba') else None
    pred = model.predict(X)[0]
    return int(pred), float(prob) if prob is not None else None, model.__class__.__name__
