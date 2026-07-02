# AI-ML-credit-card-approval-project
The Credit Card Approval Prediction project uses machine learning to predict whether a customer's credit card application will be approved based on personal and financial information such as income, employment status, credit history, and other factors.

## Run locally

1. Open PowerShell and go to the project root:
```powershell
Set-Location 'f:\AI-ML-credit-card-approval-project'
```

2. Build the Docker image:
```powershell
docker build -t credit-card-approval .
```

3. Run the app:
```powershell
docker run --rm -p 5000:5000 credit-card-approval
```

4. Open in browser:
```
http://127.0.0.1:5000
```

## Run with Docker Compose

```powershell
docker compose up --build
```

## Notes

- The app files are located under `5.Project Development Phase/`.
- The Flask app listens on port `5000`.
- If the project is already running locally, stop it before starting Docker.
