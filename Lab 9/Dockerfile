FROM python:3.11-slim

WORKDIR /app

ENV PRODUCTS="/app/database/products.csv"
ENV SUPPLIERS="/app/database/suppliers.csv"

COPY app/ app/
COPY data/ data/
COPY discounts/ discounts/
COPY managers/ managers/
COPY orders/ orders/
COPY products/ products/
COPY suppliers/ suppliers/
COPY tests/ tests/
COPY main.py .

RUN mkdir -p /app/database

CMD ["python", "main.py"]
