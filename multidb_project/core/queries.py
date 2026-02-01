from django.db.models import Count, Sum
from django.db import connections
from .models import Client, Contract

# -----------------------------------------------------------------------------
# ORM (PostgreSQL): SELECT * FROM clients WHERE is_active = true;
# -----------------------------------------------------------------------------
def active_clients():
    return Client.objects.using("default").filter(is_active=True)

# -----------------------------------------------------------------------------
# Multi-DB: no existe relación ORM entre Client y Contract.
# Por lo tanto NO se puede usar annotate(Count("contracts")) porque no hay related_name.
# Se resuelve con:
# - query en MySQL para agrupar por client_id
# - merge en memoria con clients desde PostgreSQL
# -----------------------------------------------------------------------------
def client_contract_counts():
    """
    Retorna dict: {client_id: total_contracts} desde MySQL.
    """
    qs = (
        Contract.objects.using("mysql")
        .values("client_id")
        .annotate(total_contracts=Count("id"))
    )
    return {row["client_id"]: row["total_contracts"] for row in qs}


def client_amount_totals():
    """
    Retorna dict: {client_id: total_amount} desde MySQL.
    """
    qs = (
        Contract.objects.using("mysql")
        .values("client_id")
        .annotate(total_amount=Sum("amount"))
    )
    return {row["client_id"]: row["total_amount"] for row in qs}


def clients_with_contract_count():
    """
    Retorna lista de dicts combinando:
    - Clients desde PostgreSQL
    - Conteos desde MySQL
    """
    counts = client_contract_counts()
    clients = Client.objects.using("default").all().values("id", "name")
    return [
        {"id": c["id"], "name": c["name"], "total_contracts": counts.get(c["id"], 0)}
        for c in clients
    ]


def total_amount_by_client():
    """
    Retorna lista de dicts combinando:
    - Clients desde PostgreSQL
    - Sumas desde MySQL
    """
    totals = client_amount_totals()
    clients = Client.objects.using("default").all().values("id", "name")
    return [
        {"id": c["id"], "name": c["name"], "total_amount": totals.get(c["id"], 0)}
        for c in clients
    ]

# -----------------------------------------------------------------------------
# SQL crudo (RAW SQL) - EJEMPLO SEPARADO POR DB (NO JOIN CROSS-DB)
# -----------------------------------------------------------------------------
def raw_sql_clients_postgres():
    """
    SQL crudo en PostgreSQL: lista de clients.
    """
    with connections["default"].cursor() as cursor:
        cursor.execute("SELECT id, name, email, country, is_active, created_at FROM clients;")
        return cursor.fetchall()


def raw_sql_contracts_mysql():
    """
    SQL crudo en MySQL: conteo por client_id.
    """
    with connections["mysql"].cursor() as cursor:
        cursor.execute("""
            SELECT client_id, COUNT(id) AS total_contracts
            FROM contracts
            GROUP BY client_id
        """)
        return cursor.fetchall()
