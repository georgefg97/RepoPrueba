# Usar la arquitectura correcta para evitar errores como 'exec format error'
FROM --platform=linux/amd64 python:3.11-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar paquetes de Python
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Hacer que Python reconozca 'app/' como raíz del proyecto para los imports
ENV PYTHONPATH=/app/app

# Comando por defecto para ejecutar el backend
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
