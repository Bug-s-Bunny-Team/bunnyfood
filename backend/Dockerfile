# Dockerfile for API service

FROM python:3.9

WORKDIR /api

COPY api/requirements.txt /api/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt

COPY api/ /api

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]