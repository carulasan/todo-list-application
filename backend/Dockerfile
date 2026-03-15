FROM python:3.10

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Run prestart script before the app starts
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]