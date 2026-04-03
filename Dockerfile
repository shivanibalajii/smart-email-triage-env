FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir fastapi uvicorn

EXPOSE 7860

CMD ["uvicorn", "inference:app", "--host", "0.0.0.0", "--port", "7860"]