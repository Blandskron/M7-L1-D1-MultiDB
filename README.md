# Laboratorio educativo Django ORM y múltiples bases de datos

Aplicación sencilla para aprender cómo Django integra modelos Python con bases de datos. Separa `Client` y `Contract` en dos bases SQLite mediante un `DatabaseRouter`, expone una interfaz web, administración y API, e incluye consultas ORM y SQL crudo.

## Ejecución completa con Docker

```bash
docker compose up --build
```

Abra <http://localhost:8000/>. El panel está en <http://localhost:8000/admin/> con usuario `admin` y contraseña `admin1234`. El contenedor ejecuta las migraciones de ambas bases, recopila estáticos y crea de forma idempotente el usuario y los datos de demostración.

## Qué demuestra

- **Integración Django/BD:** un modelo declara campos, tipos, restricciones y orden; las migraciones versionan el esquema; el ORM traduce expresiones Python a SQL.
- **Multi-DB:** `core/db_router.py` dirige `Client`, autenticación y administración a `default`, y `Contract` a `contracts`. No se utiliza una `ForeignKey` entre conexiones: la asociación se representa con `client_id` y se combina en Python.
- **Consultas ORM:** `filter()`, `values()`, `annotate()`, `Count()` y `Sum()` están en `core/queries.py`. `.using(alias)` hace explícita la conexión.
- **SQL en Django:** el mismo archivo muestra consultas con `connections[alias].cursor()`. Los valores externos siempre deben enviarse como parámetros, nunca concatenarse.
- **Migraciones:** `core/migrations/0001_initial.py` define el esquema; el router decide qué modelo se crea en cada conexión.
- **Validación:** formularios `ModelForm`, unicidad del email, monto positivo y existencia del cliente.
- **Interfaces:** página principal, formularios, panel admin y endpoints `/api/clients/`, `/api/clients/stats/` y `/api/clients/amounts/`.

## Motores soportados y paquetes

Django incluye backends oficiales para los motores relacionales solicitados. SQLite usa la biblioteca estándar de Python y no requiere driver adicional.

| Motor | `ENGINE` | Driver habitual |
|---|---|---|
| SQLite | `django.db.backends.sqlite3` | incluido en Python |
| PostgreSQL | `django.db.backends.postgresql` | `psycopg` |
| MySQL | `django.db.backends.mysql` | `mysqlclient` |
| Oracle | `django.db.backends.oracle` | `oracledb` |

Los drivers alternativos se instalan solo si se cambia el motor, por ejemplo `pip install psycopg[binary]`, `pip install mysqlclient` o `pip install oracledb`. Este proyecto usa SQLite por defecto para que el evaluador no necesite servicios o instalaciones adicionales.

### Bases NoSQL

El ORM oficial está diseñado para bases relacionales. MongoDB y otros motores NoSQL requieren un backend o cliente de terceros, cuyas compatibilidad, migraciones y limitaciones deben evaluarse por separado. No se añadió uno porque no es necesario para este ejercicio y ocultaría los conceptos esenciales.

## Ejecución local opcional

Requiere Python 3.12 o superior:

```bash
cd multidb_project
python -m venv .venv
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py migrate --database=contracts
python manage.py seed_demo
python manage.py runserver
```

Pruebas:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

## Estructura relevante

- `models.py`: mapeo objeto-relacional y validación.
- `db_router.py`: lectura, escritura, relaciones y migraciones multi-DB.
- `queries.py`: consultas ORM, agregaciones, combinación y SQL crudo.
- `forms.py`, `views.py`, `urls.py`: ingreso validado y presentación.
- `admin.py`: gestión de ambos modelos.
- `management/commands/seed_demo.py`: catálogo inicial idempotente.
- `tests.py`: pruebas básicas sobre ambas conexiones.

Las bases se guardan en el volumen Docker `django_data`, por lo que reiniciar el contenedor no duplica datos ni pierde el estado.
