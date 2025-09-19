# Colegio_Ninito_Jesus — Despliegue en Render (Docker)

Este repositorio contiene una aplicación Django preparada para desplegar en Render.
He agregado un `Dockerfile` para facilitar builds en Render cuando hay dependencias nativas (pandas, pyodbc, etc.).

## Qué hace el `Dockerfile`
- Usa `python:3.11-slim`.
- Instala dependencias de sistema necesarias para compilar paquetes nativos (`build-essential`, `unixodbc-dev`, `libpq-dev`, etc.).
- Actualiza `pip` y luego instala las dependencias desde `requirements.txt`.
- Usa `gunicorn` para arrancar la app: `gunicorn colegio_ninito_jesus.wsgi --bind 0.0.0.0:$PORT`.

## Pasos para desplegar en Render (modo Docker) — recomendado
1. Ve a https://dashboard.render.com y selecciona tu servicio o crea uno nuevo.
2. Elige "Docker" como método de despliegue (Render detectará el `Dockerfile` en la raíz del repo).
3. Asegúrate de que la rama sea `main` (o la rama que uses).
4. En las Environment Variables de tu servicio, añade al menos:
   - `DJANGO_SECRET_KEY` = (tu secret)
   - `DJANGO_DEBUG` = `False`
   - `ALLOWED_HOSTS` = (tu dominio Render o `*` temporalmente)
   - Si usas Postgres: crea y enlaza el servicio Postgres en Render; se añadirá `DATABASE_URL` automáticamente.
5. Lanza el deploy (Build). Observa los logs: el build debe ejecutar `apt-get` y luego `pip install -r requirements.txt`.
6. Tras un deploy exitoso, abre la **Shell** del servicio en Render y corre:
```bash
python manage.py migrate --noinput
python manage.py collectstatic --noinput
```
7. Abre la URL asignada por Render y verifica la app.

## Si prefieres no usar Docker (builder estándar)
- Asegúrate de que `runtime.txt` tiene la versión que quieres (ya hay `python-3.11.6`).
- En Render, en Build Command usa:
```bash
python -m pip install --upgrade pip && pip install -r requirements.txt
```
- Si el builder falla por paquetes nativos (por ejemplo `pyodbc`, `pandas`, `mysqlclient`), considera:
  - Cambiar a Docker (recomendado), o
  - Reemplazar paquetes por alternativas binarias (por ejemplo `mysql-connector-python` en vez de `mysqlclient`) o usar `psycopg2-binary` para Postgres.

## Troubleshooting rápido
- Si ves errores de `Failed building wheel for ...` o `command 'g++' failed`: usa Docker o instala las dependencias del sistema.
- Si el servicio da `502 Bad Gateway` en Render: revisa los logs del proceso (no solo build). Puede ser que la app no esté escuchando en `0.0.0.0:$PORT` (el `Dockerfile` y `Procfile` ya usan este bind).
- Si ves `ModuleNotFoundError` para paquetes: asegúrate de que estén en `requirements.txt` y que el build haya instalado todo (usa Clear Cache y Deploy latest commit).

## Comandos locales útiles
```powershell
# activar entorno
.\venv\Scripts\Activate.ps1
# instalar deps
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
# comprobar Django
python manage.py check
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py runserver
```

Si quieres, yo puedo:
- Preparar un `render.yaml` (deployment spec) si prefieres infra-as-code; o
- Modificar `requirements.txt` para sustituir paquetes problemáticos por alternativas binarias.

Dime qué prefieres y te preparo los siguientes pasos.
