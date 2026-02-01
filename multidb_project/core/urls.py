from django.urls import path
from .views import clients_view, client_stats_view, client_amounts_view

urlpatterns = [
    path("clients/", clients_view),
    path("clients/stats/", client_stats_view),
    path("clients/amounts/", client_amounts_view),
]
