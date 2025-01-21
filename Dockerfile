FROM python:3.10

WORKDIR /code

COPY requirements.txt /code/

# RUN pip install --no-cache-dir --no-dependencies -r requirements.txt
RUN pip install -r requirements.txt

COPY . /code/
