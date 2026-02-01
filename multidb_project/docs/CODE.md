## `multidb_project/settings.py` (solo lo que se agrega/modifica)

### `INSTALLED_APPS` (agregar `core`)

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
]
```

### `DATABASES` (PostgreSQL + MySQL)

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "clientdb",
        "USER": "postgres",
        "PASSWORD": "admin1234",
        "HOST": "localhost",
        "PORT": "5432",
    },
    "mysql": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "contractdb",
        "USER": "root",
        "PASSWORD": "admin1234",
        "HOST": "127.0.0.1",
        "PORT": "3306",
        "OPTIONS": {"charset": "utf8mb4"},
    },
}
```

### `DATABASE_ROUTERS`

```python
DATABASE_ROUTERS = ["core.db_router.CoreDatabaseRouter"]
```

---

## 2) `core/models.py` (completo)

```python
from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "clients"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Contract(models.Model):
    client_id = models.BigIntegerField(db_index=True)
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    signed_date = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "contracts"
        ordering = ["-signed_date"]

    def __str__(self):
        return f"{self.title} (client_id={self.client_id})"
```

---

## 3) `core/admin.py` (completo)

```python
from django.contrib import admin
from .models import Client, Contract

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "country", "is_active", "created_at")
    search_fields = ("name", "email")
    list_filter = ("country", "is_active")


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "client_id", "amount", "signed_date", "is_active")
    search_fields = ("title", "client_id")
    list_filter = ("is_active",)
```

---

## 4) `core/db_router.py` (completo)

```python
class CoreDatabaseRouter:
    postgres_models = {"client"}
    mysql_models = {"contract"}

    def db_for_read(self, model, **hints):
        if model._meta.model_name in self.postgres_models:
            return "default"
        if model._meta.model_name in self.mysql_models:
            return "mysql"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.model_name in self.postgres_models:
            return "default"
        if model._meta.model_name in self.mysql_models:
            return "mysql"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        db1 = self.db_for_read(obj1.__class__)
        db2 = self.db_for_read(obj2.__class__)
        if db1 and db2 and db1 != db2:
            return False
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label != "core":
            return None

        if model_name in self.postgres_models:
            return db == "default"

        if model_name in self.mysql_models:
            return db == "mysql"

        return None
```

---

## 5) `core/queries.py` (completo)

```python
from django.db.models import Count, Sum
from django.db import connections
from .models import Client, Contract

def active_clients():
    return Client.objects.using("default").filter(is_active=True)

def client_contract_counts():
    qs = (
        Contract.objects.using("mysql")
        .values("client_id")
        .annotate(total_contracts=Count("id"))
    )
    return {row["client_id"]: row["total_contracts"] for row in qs}

def client_amount_totals():
    qs = (
        Contract.objects.using("mysql")
        .values("client_id")
        .annotate(total_amount=Sum("amount"))
    )
    return {row["client_id"]: row["total_amount"] for row in qs}

def clients_with_contract_count():
    counts = client_contract_counts()
    clients = Client.objects.using("default").all().values("id", "name")
    return [
        {"id": c["id"], "name": c["name"], "total_contracts": counts.get(c["id"], 0)}
        for c in clients
    ]

def total_amount_by_client():
    totals = client_amount_totals()
    clients = Client.objects.using("default").all().values("id", "name")
    return [
        {"id": c["id"], "name": c["name"], "total_amount": totals.get(c["id"], 0)}
        for c in clients
    ]

def raw_sql_clients_postgres():
    with connections["default"].cursor() as cursor:
        cursor.execute("SELECT id, name, email, country, is_active, created_at FROM clients;")
        return cursor.fetchall()

def raw_sql_contracts_mysql():
    with connections["mysql"].cursor() as cursor:
        cursor.execute("""
            SELECT client_id, COUNT(id) AS total_contracts
            FROM contracts
            GROUP BY client_id
        """)
        return cursor.fetchall()
```

---

## 6) `core/views.py` (completo)

```python
from django.http import JsonResponse
from .queries import (
    active_clients,
    clients_with_contract_count,
    total_amount_by_client
)

def clients_view(request):
    data = list(active_clients().values())
    return JsonResponse(data, safe=False)

def client_stats_view(request):
    return JsonResponse(clients_with_contract_count(), safe=False)

def client_amounts_view(request):
    return JsonResponse(total_amount_by_client(), safe=False)
```

---

## 7) `core/urls.py` (completo)

```python
from django.urls import path
from .views import clients_view, client_stats_view, client_amounts_view

urlpatterns = [
    path("clients/", clients_view),
    path("clients/stats/", client_stats_view),
    path("clients/amounts/", client_amounts_view),
]
```

---

## 8) `multidb_project/urls.py` (completo)

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("core.urls")),
]
```
