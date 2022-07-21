from tkinter import CASCADE
from django.db import models
from django.contrib.postgres.indexes import GinIndex
from django.db.models import Q

from django.contrib.auth import models as auth_models

from ....core.models import ModelWithMetadata
from ....core.permissions import AccountPermissions
from ....account.models import PossiblePhoneNumberField, User, UserManager


PORTO_DEFAULT = "FAF"
PORTO_CHOICES = (
    ("A", "Assegnato"),
    ("F", "Franco"),
    (PORTO_DEFAULT, "Franco con addebito in fattura"),
    #("Ritiro in azienda", ""),
)
VETTORE_DEFAULT = "VG"
VETTORE_CHOICES = (
    ("D", "Destinatario"),
    ("M", "Mittente"),
    ("V", "Vettore"),
    (VETTORE_DEFAULT, "Vettore GLS"),
    ("VD", "Vettore DHL"),
    ("VB", "Vettore BRT"),
)
TIPO_CLIENTE_DEFAULT = "A"
TIPO_CLIENTE_CHOICES = (
    (TIPO_CLIENTE_DEFAULT, "Azienda"),
    ("P", "Privato"),
    ("PA", "Pubblica Amministrazione"),
    ("R", "Agenzia Pubblicitaria"),
    ("D", "Dipendente"),
)

###
# tabella contatti aggiuntivi di un azienda
###
class Iva(models.Model):
    denominazione = models.CharField(max_length=256, blank=False,null=True, unique=True)
    valore = models.FloatField()
    info = models.TextField(blank=True, default="")
class Listino(models.Model):
    denominazione = models.CharField(max_length=256, blank=False,null=False, unique=True)
    ricarico = models.FloatField(default=0)
    info = models.TextField(blank=True, default="")

class UserExtraManager(UserManager):
    def rappresentanti(self):
        return self.get_queryset().filter(
            Q(is_staff=True) & Q(is_rappresentante=True)
        )
    
    def userExtrafromUser(self, user):
        return self.get_queryset().filter(email=user.email).first()

    def clienti(self):
        return self().customers(self)

# class UserExtraInfo(User):
#     user = models.ForeignKey(User,related_name="extra_info", on_delete=models.CASCADE)

#     denominazione = models.TextField(null=True, blank=True)
#     id_danea = models.TextField(null=True, blank=True)

class UserExtra(User):
    user_ptr = models.OneToOneField(User, on_delete=models.CASCADE, related_name="extra", parent_link=True, primary_key=True, serialize=False)
    objects = UserExtraManager() # override del "userManager"
    
    denominazione = models.TextField(null=True, blank=True)
    id_danea = models.TextField(null=True, blank=True, unique=True)
    tipo_cliente = models.CharField(max_length=9,
                  choices=TIPO_CLIENTE_CHOICES,
                  default=TIPO_CLIENTE_DEFAULT)

    tel = PossiblePhoneNumberField(null=True,blank=True, default="", db_index=True)
    cell = PossiblePhoneNumberField(null=True,blank=True, default="", db_index=True)
    
    #is_no_login = models.BooleanField(default=False) # sostituito per 
    #rappresentante
    is_rappresentante = models.BooleanField(default=False)
    rappresentante = models.ForeignKey("self", related_name="clienti", null=True,blank=True, on_delete=models.SET_NULL)
    #nome_rappresentante = models.CharField(max_length=256, blank=True) # nel caso si cancellasse il riferimento esterno al rappresentante
    commissione = models.FloatField(default=0,null=False, blank=True)
    # dati azienda
    piva = models.TextField(null=True, blank=True, unique=True)
    cf = models.TextField(null=True, blank=True, unique=True)
    pec = models.EmailField(null=True, blank=True)
    sdi = models.TextField(null=True, blank=True)
    #Pubblica amministrazione
    rif_ammin = models.TextField(null=True, blank=True)
    split_payment = models.BooleanField(null=True,default=False)

    iva = models.ForeignKey(Iva, null=True,blank=True, on_delete=models.SET_NULL)
    porto = models.CharField(null=True, blank=True, max_length=3,
                  choices=PORTO_CHOICES,
                  default=PORTO_DEFAULT)
    vettore = models.CharField(null=True, blank=True, max_length=2,
                  choices=VETTORE_CHOICES,
                  default=VETTORE_DEFAULT)
    pagamento = models.TextField(null=True, blank=True, default = "Bonifico anticipato")
    coordinate_bancarie = models.TextField(null=True, blank=True)
    listino = models.ForeignKey(Listino, null=True,blank=True, on_delete=models.SET_NULL)
    sconto = models.FloatField(default=0,null=False, blank=True)


###
# tabella contatti aggiuntivi di un cliente
###
class Contatto(models.Model):
    utente = models.ForeignKey(UserExtra, related_name="contatti", null=True,blank=True, on_delete=models.CASCADE)
    email = models.EmailField(unique=False, db_index=True)
    denominazione = models.CharField(max_length=256, blank=True)
    phone = PossiblePhoneNumberField(blank=True, default="", db_index=True)


