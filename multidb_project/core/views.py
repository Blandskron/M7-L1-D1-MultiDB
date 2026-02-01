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
    # ahora clients_with_contract_count() ya retorna lista de dicts
    return JsonResponse(clients_with_contract_count(), safe=False)


def client_amounts_view(request):
    # ahora total_amount_by_client() ya retorna lista de dicts
    return JsonResponse(total_amount_by_client(), safe=False)
