# Multi-stage Dockerfile for reduced image size and enhanced security
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-slim
WORKDIR /app

# Create a non-root user and group
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /bin/sh appuser

# Copy installed dependencies from builder stage
COPY --from=builder /install /usr/local
COPY main.py .

# Set proper ownership
RUN chown -R appuser:appgroup /app

EXPOSE 8000

# Run container with non-root security context
USER 10001
CMD ["uvicorn", "main.py:app", "--host", "0.0.0.0", "--port", "8000"]