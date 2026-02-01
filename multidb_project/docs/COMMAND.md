# command.md

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

```bash
python -m pip install --upgrade pip
```

```bash
pip install django psycopg2-binary mysqlclient
```

```bash
django-admin startproject multidb_project
```

```bash
cd multidb_project
```

```bash
python manage.py startapp core
```

```bash
python manage.py makemigrations core
```

```bash
python manage.py migrate --database=default
```

```bash
python manage.py migrate --database=mysql
```

```bash
python manage.py createsuperuser --database=default
```

```bash
python manage.py runserver
```

```bash
pip freeze > requirements.txt
```
