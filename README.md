# Intelligent Error Analyzer - Complete Working Project

## Fastest local run
1. Start MongoDB on `127.0.0.1:27017`.
2. Backend:
   `cd backend`
   `python -m venv .venv`
   `\.venv\Scripts\Activate.ps1`
   `pip install -r requirements.txt`
   `python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000`
3. New terminal:
   `cd frontend`
   `npm install`
   `npm run dev`
4. Open `http://localhost:5173`.

Swagger: `http://127.0.0.1:8000/docs`
Health: `http://127.0.0.1:8000/health`
Metrics: `http://127.0.0.1:8000/metrics`

## Easiest full-stack run
From project root:
`docker compose up --build`

Frontend `http://localhost:5173`
API `http://localhost:8000`
Prometheus `http://localhost:9090`
Grafana `http://localhost:3000` (admin/admin)

## DevOps coverage
Docker, Docker Compose, MongoDB, FastAPI, React/Vite, Prometheus, Grafana, Jenkins CI, Kubernetes starter manifests, Terraform starter, and Datadog-ready environment configuration.
