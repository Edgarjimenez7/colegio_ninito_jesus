# Dockerfile para desplegar en Render con dependencias de sistema necesarias
# Usa Python 3.11 para compatibilidad con tus paquetes actuales
FROM python:3.11-slim

# Evitar prompts de apt
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias del sistema necesarias para compilar ruedas
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       gcc \
       g++ \
       make \
       unixodbc-dev \
       default-libmysqlclient-dev \
       libpq-dev \
       libssl-dev \
       libxml2-dev \
       libxslt1-dev \
       zlib1g-dev \
       libjpeg-dev \
       libfreetype6-dev \
       pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de la aplicación
WORKDIR /app

# Copiar requirements primero para aprovechar cache
COPY requirements.txt /app/requirements.txt

# Actualizar pip y ruedas, luego instalar requerimientos
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . /app

# Crear usuario no root (opcional)
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Puerto que Render proveerá a través de la variable $PORT
ENV PORT=8000

# Start command - use shell form so environment variable $PORT is expanded at run time
CMD gunicorn colegio_ninito_jesus.wsgi --bind 0.0.0.0:$PORT --log-file -
