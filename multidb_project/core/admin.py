from django.contrib import admin
from .models import Client, Contract

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """
    Admin para Client (PostgreSQL).
    """
    list_display = ("id", "name", "email", "country", "is_active", "created_at")
    search_fields = ("name", "email")
    list_filter = ("country", "is_active")


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    """
    Admin para Contract (MySQL).

    Importante:
    - No existe ForeignKey real a Client, porque Client vive en otra base de datos.
    - Usamos client_id (integer) para enlazar a nivel aplicación.
    """
    list_display = ("id", "title", "client_id", "amount", "signed_date", "is_active")
    search_fields = ("title", "client_id")
    list_filter = ("is_active",)
