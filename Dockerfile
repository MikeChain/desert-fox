# imagen base
FROM python:3.11-alpine

# establecer directorio de trabajo
WORKDIR /code

# instalar dependencias de linux
RUN apk add --no-cache gcc musl-dev linux-headers libpq-dev

RUN pip install --upgrade pip
# copiar archivo de dependencias e instalarlas
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

# copiar codigo fuente
COPY . .

COPY .env.container .env

# establecer variables de entorno
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN flask --app main db upgrade

# exponer puerto default de flask
EXPOSE 5000

# correr comando
# CMD ["flask", "run"]
CMD ["gunicorn", "main:app", "-w", "4", "-b", "0.0.0.0:5000"]
