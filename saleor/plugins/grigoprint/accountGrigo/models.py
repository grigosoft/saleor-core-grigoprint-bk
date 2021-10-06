from django.db import models
from ....account.models import User

class UserGrigo(User):
    #rappresentante
    rappresentante = models.ForeignKey("UserGrigo", related_name="clienti", null=True,blank=True, on_delete=models.SET_NULL)
    commissione = models.FloatField(default=0,null=False, blank=True)
    # dati azienda
    piva = models.TextField(null=False, blank=False)
    cf = models.TextField(null=False, blank=False)
    # ragione sociale nel nome
    pec = models.TextField(null=False, blank=False)
    piva = models.TextField(null=False, blank=False)
    sdi = models.TextField(null=False, blank=False)
    split_payment = models.BooleanField(default=False)
    # listino = 
    sconto = models.FloatField(default=0,null=False, blank=True)
