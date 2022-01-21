from django.db import models
from ....account.models import PossiblePhoneNumberField, User

# class UserExtraInfo(User):
#     user = models.ForeignKey(User,related_name="extra_info", on_delete=models.CASCADE)

#     denominazione = models.TextField(null=True, blank=True)
#     id_danea = models.TextField(null=True, blank=True)

class UserGrigo(User):
    denominazione = models.TextField(null=True, blank=True)
    id_danea = models.TextField(null=True, blank=True)

    phone = PossiblePhoneNumberField(blank=True, default="", db_index=True)
    
    #is_no_login = models.BooleanField(default=False) # sostituito per 
    #rappresentante
    is_rappresentante = models.BooleanField(default=False)
    rappresentante = models.ForeignKey("UserGrigo", related_name="clienti", null=True,blank=True, on_delete=models.SET_NULL)
    commissione = models.FloatField(default=0,null=False, blank=True)
    # dati azienda
    piva = models.TextField(null=True, blank=True, unique=True)
    cf = models.TextField(null=True, blank=True, unique=True)
    pec = models.EmailField(null=True, blank=True)
    sdi = models.TextField(null=True, blank=True)
    #Pubblica amministrazione
    rif_ammin = models.TextField(null=True, blank=True)
    split_payment = models.BooleanField(default=False)



    iva = models.TextField(null=True, blank=True)
    porto = models.TextField(null=True, blank=True) # franco, assegnato, ecc
    pagamento = models.TextField(null=True, blank=True)
    coordinate_bancarie = models.TextField(null=True, blank=True)
    listino = models.TextField(null=True, blank=True)
    sconto = models.FloatField(default=0,null=False, blank=True)
