import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import joblib
try:
    from xgboost import XGBClassifier
    XGB_AVAILABLE = True
except Exception:
    XGB_AVAILABLE = False
from preprocessing import load_dataset, basic_cleaning, build_preprocessor


PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
DATASET_PATH = os.path.join(PROJECT_DIR, 'dataset', 'credit_card.csv')
MODELS_DIR = os.path.join(PROJECT_DIR, 'models')


def evaluate_model(clf, X_test, y_test):
    y_pred = clf.predict(X_test)
    y_prob = clf.predict_proba(X_test)[:, 1] if hasattr(clf, 'predict_proba') else None
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, zero_division=0),
        'recall': recall_score(y_test, y_pred, zero_division=0),
        'f1': f1_score(y_test, y_pred, zero_division=0),
        'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
        'roc_auc': roc_auc_score(y_test, y_prob) if y_prob is not None else None
    }
    return metrics


def main():
    os.makedirs(MODELS_DIR, exist_ok=True)
    df = load_dataset(DATASET_PATH)
    df = basic_cleaning(df)

    # basic assumption about columns
    target = 'Approval_Status'
    if target not in df.columns:
        raise KeyError('Expected target column `Approval_Status` in dataset')

    # simple feature selection (user can expand)
    categorical_features = [c for c in df.select_dtypes(include=['object']).columns if c != target]
    numerical_features = [c for c in df.select_dtypes(include=['int64', 'float64']).columns if c != target]

    # drop rows with missing target
    df = df.dropna(subset=[target])

    X = df[categorical_features + numerical_features]
    y = (df[target].astype(str).str.lower() == 'approved').astype(int)

    preprocessor = build_preprocessor(categorical_features, numerical_features)
    X_proc = preprocessor.fit_transform(X)
    joblib.dump(preprocessor, os.path.join(MODELS_DIR, 'preprocessor.pkl'))

    X_train, X_test, y_train, y_test = train_test_split(X_proc, y, test_size=0.2, random_state=42)

    models = {
        'logistic': LogisticRegression(max_iter=200),
        'decision_tree': DecisionTreeClassifier(random_state=42),
        'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
    }
    if XGB_AVAILABLE:
        models['xgboost'] = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    

    results = {}
    best_model = None
    best_score = -1

    for name, model in models.items():
        try:
            model.fit(X_train, y_train)
            metrics = evaluate_model(model, X_test, y_test)
            results[name] = metrics
            score = metrics.get('f1', 0)
            if score > best_score:
                best_score = score
                best_model = (name, model)
            # save model artifact
            joblib.dump(model, os.path.join(MODELS_DIR, f'{name}.pkl'))
        except Exception as e:
            print(f'Error training {name}:', e)

    if best_model:
        joblib.dump(best_model[1], os.path.join(MODELS_DIR, 'best_model.pkl'))

    # write a summary CSV
    pd.DataFrame(results).T.to_csv(os.path.join(MODELS_DIR, 'model_summary.csv'))
    print('Training complete. Models saved to', MODELS_DIR)


if __name__ == '__main__':
    main()
