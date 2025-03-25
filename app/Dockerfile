FROM python:3.10-alpine

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /code

COPY requirements.txt /code/

#RUN apk add --no-cache mariadb-dev gcc musl-dev \
#    && pip install --no-cache-dir -r requirements.txt

RUN apk add --no-cache mariadb-dev gcc musl-dev \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del gcc musl-dev  # Elimina paquetes innecesarios para reducir el tamaño


COPY . /code/

EXPOSE 8000

# Comando para correr el servidor de Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]