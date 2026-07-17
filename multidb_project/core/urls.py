from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("clients/new/", views.create_client, name="create_client"),
    path("contracts/new/", views.create_contract, name="create_contract"),
    path("clients/", views.clients_view, name="api_clients"),
    path("clients/stats/", views.client_stats_view, name="api_client_stats"),
    path("clients/amounts/", views.client_amounts_view, name="api_client_amounts"),
]
