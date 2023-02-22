# Proyecto del Bootcamp de Backend con Python

## Uso sin docker

### Prerrequisitos

Para poder inicializar este proyecto es necesario tener instalado python 3.11.1, así como una conexión a una base de datos de Postgres y Redis.

Una vez instalado, hay que crear un archivo `.env` con al menos las siguientes claves:

```
SQLALCHEMY_DATABASE_URI = <cadena de conexión a la base de datos>
ENV= <dev | qas | prd>
```

### Instalación

Para poder usar el proyecto, se debe crear un ambiente virtual (recomiendo usar venv), activarlo e instalar las dependencias de python:

```
python -m  venv </ruta/al/entorno>
```

```
</ruta/al/entorno>/Scripts/activate
```

```
python -m pip install --upgrade pip
```

```
pip install -r .\requirements.txt
```

### Ejecutar

Una vez terminada la instalación, se pueden usar los comandos de flask:

```
flask --app main db upgrade
```

```
flask --app main run
```
