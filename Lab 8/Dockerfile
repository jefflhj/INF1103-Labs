FROM python:3.11-slim

WORKDIR /app

ENV INVENTORY_FILE="/app/database/inventory.json"
ENV SUPPLIERS_FILE="/app/database/suppliers.json"

COPY can_be_shipped.py .
COPY inventory.py .
COPY product.py .
COPY physical_product.py .
COPY digital_product.py .
COPY inventory_manager.py .
COPY supplier.py .
COPY suppliers.py .
COPY order.py .
COPY orderline.py .
COPY test.py .

RUN mkdir -p /app/database

CMD ["python", "inventory_manager.py"]
