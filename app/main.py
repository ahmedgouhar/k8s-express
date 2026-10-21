import os
from fastapi import FastAPI, Response, status

app = FastAPI(title="k8s-express Production Microservice", version="1.0.0")

# Fetch environment configurations from ConfigMap and Secret
ENV = os.getenv("ENVIRONMENT", "development")
DB_HOST = os.getenv("DB_HOST", "localhost")
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")


@app.get("/")
def read_root():
    """Primary application route returning system metadata."""
    return {
        "service": "k8s-express API Service",
        "environment": ENV,
        "db_host": DB_HOST,
        "status": "online",
    }


@app.get("/healthz", status_code=status.HTTP_200_OK)
def health_check(response: Response):
    """Health check endpoint utilized by Kubernetes Probes."""
    return {"status": "healthy", "log_level": LOG_LEVEL}