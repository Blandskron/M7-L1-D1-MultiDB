
from django.db import models

class Client(models.Model):
    """
    Tabla en PostgreSQL (default): clients
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
    Tabla en MySQL (mysql): contracts

    Nota: no se define FK real a Client porque está en otra BD.
    Se mantiene integridad a nivel aplicación vía client_id.
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