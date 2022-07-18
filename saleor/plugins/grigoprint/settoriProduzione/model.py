
from django.db import models
from django.contrib.auth.models import Group

from ..accountGrigo.models import UserExtra
from ..prodottoPersonalizzato.models import Personalizzazione

# grafica, amministrazione ecc
class Settore(models.Model):
    gruppo = models.ForeignKey(Group, related_name="settori", null=True,blank=True, on_delete=models.SET_NULL)
    denominazione = models.CharField(max_length=256, blank=False, unique=True)
    info = models.TextField(blank=True, default="")
    ore_lavorative = models.SmallIntegerField(default=0,null=False, blank=True)

#giorno per giorno quanto occupo in ogni settore
class TempiSettore(models.Model):
    settore = models.ForeignKey(Settore, blank=False, null=False, related_name="notifiche", on_delete=models.CASCADE)
    data = models.DateField(blank=False, null=False,)
    personalizzazione = models.ForeignKey(Personalizzazione, blank=False, null=False, related_name="tempi_settore", on_delete=models.CASCADE)
    ore_lavoro = models.FloatField(default=0,null=False, blank=False)


class Notifica(models.Model):
    settore = models.ForeignKey(Settore, blank=False, null=False, related_name="notifiche", on_delete=models.SET_NULL)
    data = models.DateTimeField(blank=False, null=False,)
    scadenza = models.DateTimeField(blank=False, null=False,)
    titolo = models.TextField()
    testo = models.TextField()
    mittente  = models.ForeignKey(UserExtra, related_name="contatti", null=True,blank=True, on_delete=models.CASCADE)