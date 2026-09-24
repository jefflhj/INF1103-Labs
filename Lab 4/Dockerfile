FROM python:3.11-slim

WORKDIR /app

COPY persistent_auditor.py .

RUN mkdir -p /app/database

CMD ["python", "persistent_auditor.py"]
