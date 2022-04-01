
from ....account.models import User
from ....product.models import Product
from django.db import models
from django.db.models.fields.related import ForeignKey
from ....order.models import Order, OrderLine
from ....checkout.models import CheckoutLine


#class TipoPrezzo(models.TextChoices):
#    LINIEARE = 'L', _('Lineare')
#    AREA = 'A', _('Area')
#    CAD = 'C', _('Cad')
#    PERCENTUALE = '%', _('Percentuale')

class TipoProdottoPersonalizzato(models.Model):
    nome = models.TextField(null=False, blank=False)

class Stato(models.Model):
    nome = models.TextField(null=False, blank=False)

class Lavorazione(models.Model):
    nome = models.TextField(null=False, blank=False)
    descrizione = models.TextField()
    ordine = models.PositiveBigIntegerField()

class Azione (models.Model):
    #class Locazione_CHOICES(models.TextChoices):
    #    LATO_SUPERIORE = 'N', _('Lato sopra')
    #    LATO_INSEFIORE = 'S', _('Lato sotto')
    #    LATO_SINISTRO = 'O', _('Lato sinistro')
    #    LATO_DESTRO = 'E', _('Lato DESTRO')
    #    ANGOLO = 'A', _('Angolo')
    nome = models.TextField(null=False, blank=False)
    descrizione = models.TextField()
    locazione = models.CharField(max_length=1)
    tipo_prezzo = models.CharField(max_length=1)
    prezzo = models.FloatField()

class AzioneLavorazione(models.Model):
    azione = ForeignKey(Azione, blank=False, null=False, related_name="lavorazioni", on_delete=models.CASCADE)
    lavorazione = ForeignKey(Lavorazione, blank=False, null=False, related_name="azioni", on_delete=models.CASCADE)

class statoLavorazione(models.Model):
    stato = ForeignKey(Stato, blank=False, null=False, related_name="lavorazioni", on_delete=models.CASCADE)
    lavorazione = ForeignKey(Lavorazione, blank=False, null=False, related_name="stati", on_delete=models.CASCADE)

class Tessuto(models.Model):
    nome = models.TextField(null=False, blank=False)
    composizione = models.TextField(null=False, blank=False)
    grammatura = models.PositiveIntegerField(null=False, blank=False)
    descrizione = models.TextField(null=True, blank=True)
    altezza = models.PositiveIntegerField(null=False, blank=False)
    costo_ml = models.FloatField(null=False, blank=False)
    spreco_ml = models.FloatField(null=False, blank=False)



class CheckoutLinePadreFiglio(CheckoutLine):
    padre = ForeignKey(CheckoutLine, blank=True, null=True, related_name="checkout_line_figlio", on_delete=models.CASCADE)
    
class OrderLinePadreFiglio(OrderLine):
    padre = ForeignKey(OrderLine, blank=True, null=True, related_name="order_line_figlio", on_delete=models.SET_NULL)
    padre_name = models.TextField(blank=True, null=True)

class Personalizzazione(models.Model):
    # per riordini delle stesse personalizzazioni
    personalizzazione_precedente = ForeignKey("Personalizzazione", blank=True, null=True, related_name="personalizzazione_sucessiva",on_delete=models.SET_NULL)
    
    # quando elimino una linea di checout elimino la personalizzazione
    # quando elimino ilcheckout di proposito elimino la personalizzazione
    # quando elimino la linea d'ordine elimino la personalizzazione
    # QUANDO COMPLETO IL CHECKOUT NON ELIMINO, passo lapersonalizzazione da checkout_linea a ordine_linea
    
    # Se entrambi null è una bozza
    # Mai entrambi NON NULL
    # se uno valorizzato NON è una bozza
    checkout_line = ForeignKey(CheckoutLine, blank=True, null=True, related_name="personalizzazione_checkout_line", on_delete=models.CASCADE)
    order_line = ForeignKey(OrderLine, blank=True, null=True, related_name="personalizzazione_order_line", on_delete=models.CASCADE)
    # per bozze (no)
    nome = models.TextField(default="bozza")
    utente = ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE)
    prodotto = ForeignKey(Product, blank=False, null=True, on_delete=models.SET_NULL)
    # personalizzazione
    data_scadenza = models.DateField()

    tessuto = ForeignKey(Tessuto, blank=True, null=True, on_delete=models.SET_NULL)
    misure = models.JSONField()
    finiture_frontend = models.JSONField()#scelte utente in frontend
    lavorazioni = models.JSONField()#copia della struttura delle tabelle


def user_appena_arrivati_path(instance, filename):
    return 'appena_arrivati/{0}/{2}'.format(instance.personalizzazione.utente, filename)
def user_appena_arrivati_tmb_path(instance, filename):
    return 'appena_arrivati/{0}/tmb_{2}'.format(instance.personalizzazione.utente, filename)
class FileGrafico(models.Model):
    personalizzazione = ForeignKey(Personalizzazione, related_name="file",on_delete=models.CASCADE)
    nome = models.TextField(null=True, blank=True) #titolo aggiuntivo
    file = models.FileField(upload_to=user_appena_arrivati_path, null=True, blank=True)
    anteprima = models.FileField(upload_to="appena_arrivati", null=True, blank=True)
    quantita = models.PositiveIntegerField(default=1, null=False, blank=False)
