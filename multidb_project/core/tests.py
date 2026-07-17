from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .db_router import CoreDatabaseRouter
from .models import Client, Contract
from .queries import clients_with_contract_count, raw_sql_clients, raw_sql_contracts, total_amount_by_client


class MultiDatabaseTests(TestCase):
    databases = {"default", "contracts"}

    def setUp(self):
        self.client_record = Client.objects.create(name="Ana", email="ana@example.com", country="Chile")
        Contract.objects.create(client_id=self.client_record.pk, title="Capacitación", amount="1500.00", signed_date=date.today())

    def test_router_separates_models(self):
        router = CoreDatabaseRouter()
        self.assertEqual(router.db_for_read(Client), "default")
        self.assertEqual(router.db_for_read(Contract), "contracts")

    def test_orm_aggregations_merge_both_databases(self):
        self.assertEqual(clients_with_contract_count()[0]["total_contracts"], 1)
        self.assertEqual(total_amount_by_client()[0]["total_amount"], Decimal("1500"))

    def test_raw_sql_examples(self):
        self.assertEqual(raw_sql_clients()[0][1], "Ana")
        self.assertEqual(raw_sql_contracts()[0][1], 1)

    def test_dashboard_and_api(self):
        self.assertContains(self.client.get(reverse("dashboard")), "Ana")
        response = self.client.get(reverse("api_client_stats"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["total_contracts"], 1)

    def test_contract_validation(self):
        invalid = Contract(client_id=9999, title="Inválido", amount=-1, signed_date=date.today())
        with self.assertRaises(ValidationError):
            invalid.full_clean()

    def test_forms_create_records(self):
        response = self.client.post(reverse("create_client"), {"name": "Luis", "email": "luis@example.com", "country": "Perú", "is_active": "on"})
        self.assertRedirects(response, reverse("dashboard"))
        self.assertTrue(Client.objects.filter(email="luis@example.com").exists())

    def test_admin_is_accessible(self):
        self.assertEqual(self.client.get("/admin/").status_code, 302)
