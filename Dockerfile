FROM python:3.11-slim
WORKDIR taskflow
COPY app .
COPY static .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt