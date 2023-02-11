# imagen base
FROM python:3.11-alpine

# establecer directorio de trabajo
WORKDIR /code

# instalar dependencias de linux
RUN apk add --no-cache gcc musl-dev linux-headers

# copiar archivo de dependencias e instalarlas
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copiar codigo fuente
COPY . .

# establecer variables de entorno
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

# exponer puerto default de flask
EXPOSE 5000

# correr comando
CMD ["flask", "run"]
