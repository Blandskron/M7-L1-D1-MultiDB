# Comandos de evaluación

Desde la raíz del repositorio:

```bash
docker compose config
docker compose build
docker compose up
```

El `entrypoint.sh` ejecuta automáticamente:

```bash
python manage.py migrate --database=default --noinput
python manage.py migrate --database=contracts --noinput
python manage.py collectstatic --noinput
python manage.py seed_demo
python manage.py runserver 0.0.0.0:8000
```

Para ejecutar pruebas dentro de la imagen:

```bash
docker compose run --rm --no-deps --entrypoint python web manage.py check
docker compose run --rm --no-deps --entrypoint python web manage.py test
```
