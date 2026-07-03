# AI-ML-credit-card-approval-project
The Credit Card Approval Prediction project uses machine learning to predict whether a customer's credit card application will be approved based on personal and financial information such as income, employment status, credit history, and other factors.

## Live Demo

https://ai-ml-credit-card-approval-project-1.onrender.com

## Run locally

1. Open PowerShell and go to the project root:
```powershell
Set-Location 'f:\AI-ML-credit-card-approval-project\5.Project Development Phase'
```

2. Create and activate a virtual environment:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

3. Install dependencies:
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

4. Run the Flask app:
```powershell
python app.py
```

5. Open in browser:
```
http://127.0.0.1:5000
```

## Notes

- The app files are located under `5.Project Development Phase/`.
- The Flask app listens on port `5000`.
- If the project is already running locally, stop it before starting the app.
