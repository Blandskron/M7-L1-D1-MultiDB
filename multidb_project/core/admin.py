# core/admin.py  (REEMPLAZAR COMPLETO)

from django.contrib import admin
from .models import Client, Contract

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "country", "is_active", "created_at")
    search_fields = ("name", "email")
    list_filter = ("country", "is_active")


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    # ya no existe "client" (ahora es client_id)
    list_display = ("id", "title", "client_id", "amount", "signed_date", "is_active")
    search_fields = ("title", "client_id")
    list_filter = ("is_active",)
