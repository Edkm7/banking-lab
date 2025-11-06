FROM python:3.10-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . . 
EXPOSE 8082
COPY wait-for-db.sh /wait-for-db.sh
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8082"]
