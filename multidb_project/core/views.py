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
    data = list(
        clients_with_contract_count().values(
            "id", "name", "total_contracts"
        )
    )
    return JsonResponse(data, safe=False)


def client_amounts_view(request):
    data = list(
        total_amount_by_client().values(
            "id", "name", "total_amount"
        )
    )
    return JsonResponse(data, safe=False)
