from django.db.models import Count, Sum
from django.db import connection
from .models import Client, Contract

# ORM: SELECT * FROM clients WHERE is_active = true;
def active_clients():
    return Client.objects.filter(is_active=True)


# ORM JOIN + AGGREGATE
def clients_with_contract_count():
    return Client.objects.annotate(
        total_contracts=Count("contracts")
    )


# ORM SUM equivalente a SQL GROUP BY
def total_amount_by_client():
    return Client.objects.annotate(
        total_amount=Sum("contracts__amount")
    )


# SQL crudo (RAW SQL)
def raw_sql_clients():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT c.id, c.name, COUNT(ct.id) as total_contracts
            FROM clients c
            LEFT JOIN contracts ct ON ct.client_id = c.id
            GROUP BY c.id, c.name
        """)
        return cursor.fetchall()
