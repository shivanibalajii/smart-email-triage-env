FROM python:3.10-slim

WORKDIR /app

COPY inference.py /app/

RUN pip install fastapi uvicorn pydantic

EXPOSE 8000

CMD ["uvicorn", "inference:app", "--host", "0.0.0.0", "--port", "8000"]