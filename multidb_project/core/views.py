from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .forms import ClientForm, ContractForm
from .models import Client, Contract
from .queries import active_clients, clients_with_contract_count, total_amount_by_client


def dashboard(request):
    return render(request, "core/dashboard.html", {
        "clients": Client.objects.using("default").all(),
        "contracts": Contract.objects.using("contracts").all(),
        "stats": clients_with_contract_count(),
        "client_form": ClientForm(),
        "contract_form": ContractForm(),
    })


@require_http_methods(["POST"])
def create_client(request):
    form = ClientForm(request.POST)
    if form.is_valid():
        client = form.save(commit=False)
        client.save(using="default")
        messages.success(request, "Cliente creado en la base principal.")
    else:
        messages.error(request, "No se pudo crear el cliente: " + form.errors.as_text())
    return redirect("dashboard")


@require_http_methods(["POST"])
def create_contract(request):
    form = ContractForm(request.POST)
    if form.is_valid():
        contract = form.save(commit=False)
        contract.full_clean()
        contract.save(using="contracts")
        messages.success(request, "Contrato creado en la segunda base.")
    else:
        messages.error(request, "No se pudo crear el contrato: " + form.errors.as_text())
    return redirect("dashboard")


def clients_view(request):
    return JsonResponse(list(active_clients().values()), safe=False)


def client_stats_view(request):
    return JsonResponse(clients_with_contract_count(), safe=False)


def client_amounts_view(request):
    return JsonResponse(total_amount_by_client(), safe=False)
