from django import forms

from .models import Client, Contract


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ("name", "email", "country", "is_active")
        labels = {"name": "Nombre", "country": "País", "is_active": "Activo"}


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ("client_id", "title", "amount", "signed_date", "is_active")
        labels = {"client_id": "ID del cliente", "title": "Título", "amount": "Monto", "signed_date": "Fecha de firma", "is_active": "Activo"}
        widgets = {"signed_date": forms.DateInput(attrs={"type": "date"})}
