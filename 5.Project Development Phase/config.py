import os

BASE_DIR = os.path.dirname(__file__)
DATASET_PATH = os.path.join(BASE_DIR, 'dataset', 'credit_card.csv')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
DB_PATH = os.path.join(BASE_DIR, 'predictions.db')
