FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Certifique-se de que o diretório data exista se o CSV estiver lá
# RUN mkdir -p /app/data
CMD ["python", "app.py"]
