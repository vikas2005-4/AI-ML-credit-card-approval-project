import os
from flask import Flask, render_template, request, redirect, url_for, flash
from src.predict import predict_from_input
from src.utils import init_db, save_prediction, get_recent_predictions
import json

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, 'predictions.db')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-me-in-production'

init_db(DB_PATH)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        data = request.form.to_dict()
        name = data.get('applicant_name', 'Anonymous')
        # map to expected features - relies on preprocessing pipeline
        # here we assume form keys match expected columns
        try:
            pred, prob, model_name = predict_from_input(data)
            label = 'Approved' if pred == 1 else 'Rejected'
            confidence = f"{prob*100:.2f}%" if prob is not None else 'N/A'
            save_prediction(DB_PATH, name, json.dumps(data), label, prob or 0.0, model_name)
            return render_template('result.html', name=name, prediction=label, probability=confidence, model=model_name)
        except Exception as e:
            flash('Prediction failed: ' + str(e), 'danger')
            return redirect(url_for('predict'))
    return render_template('predict.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/dashboard')
def dashboard():
    rows = get_recent_predictions(DB_PATH, limit=20)
    total = len(rows)
    approved = sum(1 for r in rows if r[2] == 'Approved')
    rejected = sum(1 for r in rows if r[2] == 'Rejected')
    return render_template('dashboard.html', total=total, approved=approved, rejected=rejected, recent=rows)


if __name__ == '__main__':
    app.run(debug=True)
