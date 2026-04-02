FROM python:3.10-slim

WORKDIR /app

COPY inference.py .

RUN pip install fastapi uvicorn pydantic

CMD ["uvicorn", "inference:app", "--host", "0.0.0.0", "--port", "8000"]