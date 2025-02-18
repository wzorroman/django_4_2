FROM python:3.10
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /code

COPY requirements.txt /code/

# RUN pip install --no-cache-dir --no-dependencies -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

EXPOSE 8000

# Comando para correr el servidor de Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]