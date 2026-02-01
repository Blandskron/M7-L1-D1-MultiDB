from django.db import models

class Client(models.Model):
    """
    Modelo persistido en PostgreSQL (alias: default)
    Tabla física: clients
    """
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "clients"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Contract(models.Model):
    """
    Modelo persistido en MySQL (alias: mysql)
    Tabla física: contracts

    Integridad entre DBs:
    - NO se define ForeignKey a Client (porque está en otra DB).
    - Se usa client_id y se resuelve la relación en consultas manuales / servicio.
    """
    client_id = models.BigIntegerField(db_index=True)
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    signed_date = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "contracts"
        ordering = ["-signed_date"]

    def __str__(self):
        return f"{self.title} (client_id={self.client_id})"
