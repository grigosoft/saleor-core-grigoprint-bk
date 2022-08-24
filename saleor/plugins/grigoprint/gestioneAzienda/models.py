from django.utils import timezone
from django.db import models
from django.contrib.auth.models import Group

from ..accountGrigo.models import UserExtra
from ..prodottoPersonalizzato.models import Personalizzazione

# grafica, amministrazione ecc
class Settore(models.Model):
    gruppo = models.ForeignKey(Group, related_name="settori", null=True,blank=False, on_delete=models.SET_NULL)
    denominazione = models.CharField(max_length=256, null=False, blank=False, unique=True)
    info = models.TextField(null=True, blank=True, default="")
    #ore_lavorative = models.SmallIntegerField(default=0,null=False, blank=True)

#giorno per giorno quanto occupo in ogni settore
class TempiPersonalizzazioneSettore(models.Model):
    settore = models.ForeignKey(Settore, blank=False, null=False, related_name="tempi_personalizzazione", on_delete=models.CASCADE)
    data = models.DateField(blank=False, null=False)
    personalizzazione = models.ForeignKey(Personalizzazione, blank=False, null=False, related_name="tempi_settore", on_delete=models.CASCADE)
    ore_lavoro = models.FloatField(default=0,null=False, blank=False)


class Notifica(models.Model):
    settore = models.ForeignKey(Settore, blank=False, null=False, related_name="notifiche", on_delete=models.SET_NULL)
    data = models.DateTimeField(blank=False, null=False,default=timezone.now)
    scadenza = models.DateTimeField(blank=True, null=True)
    titolo = models.TextField(blank=False,null=False, default="Nuova notifica")
    testo = models.TextField(blank=False,null=False, default="testo default")
    mittente  = models.ForeignKey(UserExtra, related_name="notifiche", null=False,blank=False, on_delete=models.SET_NULL)
    completata = models.BooleanField(default=False)

class Ferie(models.Model):
    # utente richiede con date ora e motivazione
    #admin Approva con aggiunta di info per coprire il turno
    utente = models.ForeignKey(UserExtra,null=False,blank=False, on_delete=models.CASCADE, related_name="ferie")
    data_inizio = models.DateField(null=False,blank=False)
    data_fine = models.DateField(null=False,blank=False)
    ore = models.IntegerField(null=False, default = 0)
    motivazione = models.TextField(null=True, blank=True, default="")
    approvate = models.BooleanField(default=False)
    info_approvazione = models.TextField(null=True, blank=True, default="")