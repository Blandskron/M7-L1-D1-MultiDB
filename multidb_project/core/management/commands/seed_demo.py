from datetime import date

from django.core.management.base import BaseCommand

from core.models import Client, Contract


class Command(BaseCommand):
    help = "Crea datos educativos idempotentes en las dos bases"

    def handle(self, *args, **options):
        client, _ = Client.objects.using("default").get_or_create(
            email="demo@example.com",
            defaults={"name": "Cliente Demostración", "country": "Chile", "is_active": True},
        )
        Contract.objects.using("contracts").get_or_create(
            client_id=client.pk,
            title="Contrato de ejemplo",
            defaults={"amount": "125000.00", "signed_date": date(2026, 1, 15), "is_active": True},
        )
        self.stdout.write(self.style.SUCCESS("Datos de demostración disponibles."))
