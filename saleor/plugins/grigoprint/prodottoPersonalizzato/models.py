
from ....account.models import User
from ....product.models import Product
from django.db import models
from django.core.validators import MinValueValidator
from ....order.models import Order, OrderLine
from ....checkout.models import CheckoutLine
from versatileimagefield.fields import VersatileImageField


#class TipoPrezzo(models.TextChoices):
#    LINIEARE = 'L', _('Lineare')
#    AREA = 'A', _('Area')
#    CAD = 'C', _('Cad')
#    PERCENTUALE = '%', _('Percentuale')

class TipoProdottoPersonalizzato(models.Model):
    nome = models.TextField(null=False, blank=False)


class Particolare(models.Model):
    nome = models.TextField(null=False, blank=False)
    descrizione = models.TextField()
    costo_cad = models.FloatField()
    tempo_realizzazione = models.PositiveSmallIntegerField()
    tempo_avvio = models.PositiveSmallIntegerField()
    foto = VersatileImageField(upload_to="foto-particolari", blank=True, null=True)

class Finitura (models.Model):
    nome = models.TextField(null=False, blank=False)
    descrizione = models.TextField()
    tipo_prezzo = models.CharField(max_length=1)
    prezzo_ml = models.FloatField()
    tempo_realizzazione = models.PositiveSmallIntegerField()
    tempo_avvio = models.PositiveSmallIntegerField()
    foto = VersatileImageField(upload_to="foto-finiture", blank=True, null=True)

### solo per compialre i combo box in frontend e calcolare il prezzo,
# poi nel prodotto verrà memorizzato in json
class ParticolareFinitura(models.Model):
    finitura = models.ForeignKey(Finitura, blank=False, null=False, related_name="particolare", on_delete=models.CASCADE)
    particolare = models.ForeignKey(Particolare, blank=False, null=False, related_name="finitura", on_delete=models.CASCADE)
    descrizione = models.TextField(blank=True, null=True)

###
#tabella per momorizzare le finiture di default dei vari prodotti
class FinituraDefault(models.Model):
    nome = models.TextField(null=False, blank=False)
    descrizione = models.TextField(null=False, blank=False)
    prodotto = models.ForeignKey(Product, blank=False, null=False, related_name="finiture_default", on_delete=models.CASCADE)
    finiture = models.JSONField()#scelte utente in frontend
    foto = VersatileImageField(upload_to="foto-finiture", blank=True, null=True)

class Tessuto(models.Model):
    nome = models.TextField(null=False, blank=False)
    composizione = models.TextField(null=False, blank=False)
    grammatura = models.PositiveIntegerField(null=False, blank=False)
    descrizione = models.TextField(null=True, blank=True)
    altezza = models.PositiveIntegerField(null=False, blank=False)
    costo_ml = models.FloatField(null=False, blank=False)
    spreco_ml = models.FloatField(null=False, blank=False)
    # ml ora
    velocita_stampa = models.PositiveSmallIntegerField(null=False, blank=False)
    velocita_calandra = models.PositiveSmallIntegerField(null=False, blank=False)
    velocita_cucitura = models.PositiveSmallIntegerField(null=False, blank=False) # pecentuale di difficoltà



class LineaCarrello(CheckoutLine):
    padre = models.ForeignKey(CheckoutLine, blank=True, null=True, related_name="checkout_line_figlio", on_delete=models.CASCADE)
    
class LineaOrdine(OrderLine):
    padre = models.ForeignKey(OrderLine, blank=True, null=True, related_name="order_line_figlio", on_delete=models.CASCADE)

class Personalizzazione(models.Model):
    # per riordini delle stesse personalizzazioni
    personalizzazione_precedente = models.ForeignKey("Personalizzazione", blank=True, null=True, related_name="personalizzazione_sucessiva",on_delete=models.SET_NULL)
    
    # quando elimino una linea di checout elimino la personalizzazione
    # quando elimino ilcheckout di proposito elimino la personalizzazione
    # quando elimino la linea d'ordine elimino la personalizzazione
    # QUANDO COMPLETO IL CHECKOUT NON ELIMINO, passo la personalizzazione da checkout_linea a ordine_linea
    
    # Se entrambi null è una bozza
    # Mai entrambi COLLEGATI
    # se uno valorizzato NON è una bozza
    checkout_line = models.ForeignKey(CheckoutLine, blank=True, null=True, related_name="personalizzazione_checkout_line", on_delete=models.CASCADE) # bisogna capiarla e ributtarla dentro l'ordine nuovo
    order_line = models.ForeignKey(OrderLine, blank=True, null=True, related_name="personalizzazione_order_line", on_delete=models.CASCADE)
    # per bozze (no)
    titolo = models.TextField(default="")
    #utente = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE)
    prodotto = models.ForeignKey(Product, blank=False, null=True, on_delete=models.SET_NULL)
    # personalizzazione
    data_scadenza = models.DateField()

    tessuto = models.ForeignKey(Tessuto, blank=True, null=True, on_delete=models.SET_NULL)
    misure = models.JSONField()

    finiture = models.JSONField()#scelte utente in frontend
    #lavorazioni = models.JSONField()#copia della struttura delle tabelle
    # lato_superiore = models.ForeignKey(ParticolareFinitura, related_name="files",on_delete=models.SET_NULL)
    # lato_inferiore = models.ForeignKey(ParticolareFinitura, related_name="files",on_delete=models.SET_NULL)
    # lato_sinistro = models.ForeignKey(ParticolareFinitura, related_name="files",on_delete=models.SET_NULL)
    # lato_destro = models.ForeignKey(ParticolareFinitura, related_name="files",on_delete=models.SET_NULL)
    # angolo_superiore_sinsitro = models.ForeignKey(ParticolareFinitura, related_name="files",on_delete=models.SET_NULL)
    # angolo_superiore_destro = models.ForeignKey(ParticolareFinitura, related_name="files",on_delete=models.SET_NULL)
    # angolo_inferiore_sinsitro = models.ForeignKey(ParticolareFinitura, related_name="files",on_delete=models.SET_NULL)
    # angolo_inferiore_destro = models.ForeignKey(ParticolareFinitura, related_name="files",on_delete=models.SET_NULL)
    

def user_appena_arrivati_path(instance, filename):
    #if instance.personalizzazione.
    return 'appena_arrivati/{0}/{2}'.format(instance.personalizzazione.utente, filename)
def user_appena_arrivati_tmb_path(instance, filename):
    return 'appena_arrivati/{0}/tmb_{2}'.format(instance.personalizzazione.utente, filename)
class FileGrafico(models.Model):
    personalizzazione = models.ForeignKey(Personalizzazione, related_name="files",on_delete=models.CASCADE)
    #nome = models.TextField(null=True, blank=True) #titolo aggiuntivo
    file = models.FileField(upload_to=user_appena_arrivati_path, null=True, blank=True)
    anteprima = models.FileField(upload_to="appena_arrivati", null=True, blank=True)
    quantita = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
