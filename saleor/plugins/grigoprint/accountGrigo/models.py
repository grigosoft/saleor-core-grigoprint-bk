from django.db import models
from ....account.models import User

class UserGrigo(User):
    is_no_login = models.BooleanField(default=False)
    #rappresentante
    rappresentante = models.ForeignKey("UserGrigo", related_name="clienti", null=True,blank=True, on_delete=models.SET_NULL)
    commissione = models.FloatField(default=0,null=False, blank=True)
    # dati azienda
    piva = models.TextField(null=True, blank=True)
    cf = models.TextField(null=True, blank=True)
    # ragione sociale nel nome
    pec = models.TextField(null=True, blank=True)
    piva = models.TextField(null=True, blank=True)
    sdi = models.TextField(null=True, blank=True)
    split_payment = models.BooleanField(default=False)
    # listino = 
    sconto = models.FloatField(default=0,null=False, blank=True)
