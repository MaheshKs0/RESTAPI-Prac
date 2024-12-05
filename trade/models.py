from django.db import models

# Create your models here.

class Trade(models.Model):
    tradeid = models.IntegerField(primary_key=True)
    notional = models.IntegerField()
    counterparty = models.CharField(max_length=255)


