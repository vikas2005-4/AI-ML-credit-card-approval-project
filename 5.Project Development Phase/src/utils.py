import os
import sqlite3
from datetime import datetime


def init_db(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        input_json TEXT,
        prediction TEXT,
        probability REAL,
        model TEXT,
        created_at TEXT
    )
    ''')
    conn.commit()
    conn.close()


def save_prediction(db_path, name, input_json, prediction, probability, model_name):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('''INSERT INTO predictions (name, input_json, prediction, probability, model, created_at)
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (name, str(input_json), prediction, float(probability), model_name, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()


def get_recent_predictions(db_path, limit=10):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('SELECT id, name, prediction, probability, created_at FROM predictions ORDER BY id DESC LIMIT ?', (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows
