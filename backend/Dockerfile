# Dockerfile for API service

FROM python:3.10-slim

WORKDIR /backend

COPY api/requirements.txt /backend/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt

RUN touch /backend/__init__.py
COPY api/ /backend/api
COPY db/ /backend/db

EXPOSE 80

CMD ["uvicorn", "--proxy-headers", "api.main:app", "--host", "0.0.0.0", "--port", "80"]
