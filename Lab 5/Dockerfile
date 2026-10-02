FROM python:3.11-slim

WORKDIR /app

ENV INVENTORY_FILE="/app/database/inventory.json"

COPY inventory_manager.py .

RUN mkdir -p /app/database

CMD ["python", "inventory_manager.py"]
