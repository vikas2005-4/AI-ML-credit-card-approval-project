# Deployment Guide for Credit Card Approval Flask App

## GitHub push

```bash
git add .
git commit -m "Prepare app for Render deployment: requirements, config, ignore, render.yaml"
git push origin main
```

## Render deployment

1. Log in to Render and create a new Web Service.
2. Connect your GitHub repository and select the `main` branch.
3. Use the following build and start commands:

- Build Command:

```
pip install -r requirements.txt
```

- Start Command:

```
gunicorn app:app
```

No environment variables are required, but you may optionally set `SECRET_KEY` in Render's environment settings.
