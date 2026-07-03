import os
from flask import Flask, render_template, request, redirect, url_for, flash
from src.predict import predict_from_input
from src.utils import init_db, save_prediction, get_recent_predictions
import json

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, 'predictions.db')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "change-me-in-production")

init_db(DB_PATH)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    def build_suggestions(data):
        tips = []
        try:
            credit_score = float(data.get('Credit_Score', 0))
        except ValueError:
            credit_score = None
        if credit_score is not None and credit_score < 650:
            tips.append('Improve your credit score by paying bills on time and reducing outstanding debt.')

        try:
            existing_loans = float(data.get('Existing_Loans', 0))
        except ValueError:
            existing_loans = None
        if existing_loans is not None and existing_loans > 0:
            tips.append('Reduce outstanding loans before applying for new credit to improve your offer.')

        if data.get('Payment_History', '').strip().lower() != 'good':
            tips.append('Maintain a good payment history by paying all bills on time.')

        try:
            employment_duration = float(data.get('Employment_Duration', 0))
        except ValueError:
            employment_duration = None
        if employment_duration is not None and employment_duration < 2:
            tips.append('Keep a stable job for longer to increase lender confidence.')

        try:
            annual_income = float(data.get('Annual_Income', 0))
        except ValueError:
            annual_income = None
        try:
            loan_amount = float(data.get('Loan_Amount', 0))
        except ValueError:
            loan_amount = None
        if annual_income and loan_amount and loan_amount / annual_income > 0.4:
            tips.append('Request a lower loan amount or increase your income-to-loan ratio.')

        if data.get('Housing_Type', '').strip().lower() == 'rented':
            tips.append('Reducing housing expenses or moving to owned housing can improve your credit profile.')

        if not tips:
            tips.append('Review your financial profile and focus on stable income, good payment history, and manageable loan amounts.')
        return tips

    if request.method == 'POST':
        data = request.form.to_dict()
        name = data.get('applicant_name', 'Anonymous')
        try:
            pred, prob, model_name = predict_from_input(data)
            label = 'Approved' if pred == 1 else 'Rejected'
            confidence = f"{prob*100:.2f}%" if prob is not None else 'N/A'
            save_prediction(DB_PATH, name, json.dumps(data), label, prob or 0.0, model_name)
            suggestions = build_suggestions(data)
            return render_template('result.html', name=name, prediction=label, probability=confidence, suggestions=suggestions)
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
