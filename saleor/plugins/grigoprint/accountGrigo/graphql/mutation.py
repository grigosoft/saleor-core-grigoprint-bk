from email.policy import default
from secrets import choice
import graphene

from .....graphql.core.mutations import BaseMutation, ModelMutation
from ..danea_firebird import import_anagrafica

from .....checkout import AddressType

from .....graphql.account.types import AddressInput

from .....core.permissions import AccountPermissions

from .....graphql.core.enums import AccountErrorCode

from .....graphql.account.mutations.staff import AddressCreate, AddressUpdate, CustomerCreate, CustomerUpdate, StaffCreate, StaffUpdate
from .....graphql.account.mutations.account import AccountError
from .....graphql.account.mutations.base import (
    SHIPPING_ADDRESS_FIELD,
    BILLING_ADDRESS_FIELD,
    UserCreateInput,
)
from django.core.exceptions import ValidationError

from .. import models
from .....account import models as models_saleor
from . import type

ADDRESSES_FIELD = "addresses"
RAPPRESENTANTE_FIELD = "rappresentante"
PIVA_FIELD = "piva"
CF_FIELD = "cf"
IDDANEA_FIELD = "id_danea"
ISSTAFF_FIELD = "is_staff"
ISRAPPRESENTANTE_FIELD = "is_rappresentante"


def clean_account_extra_input(cls, info, instance, data, cleaned_input):
    addresses_data = data.pop(ADDRESSES_FIELD, None)
    rappresentate_data = data.pop(RAPPRESENTANTE_FIELD, None)
    piva = data.pop(PIVA_FIELD, None)
    cleaned_input[PIVA_FIELD] = piva if piva else None
    cf = data.pop(CF_FIELD, None)
    cleaned_input[CF_FIELD] = cf if cf else None
    idanea = data.pop(IDDANEA_FIELD, None)
    cleaned_input[IDDANEA_FIELD] = idanea if idanea else None
    idanea = data.pop(IDDANEA_FIELD, None)
    cleaned_input[IDDANEA_FIELD] = idanea if idanea else None

    # rappresentante
    if rappresentate_data:
        rapp = models.UserExtra.objects.filter(email=rappresentate_data).first()
        if rapp and rapp.is_rappresentante:
            cleaned_input[RAPPRESENTANTE_FIELD] = rapp
        else:
            raise ValidationError(
                {
                    "rappresentante": ValidationError(
                        "rappresentante non valido %s"%rappresentate_data, code="value", params={"rappresentante":rappresentate_data}
                    )
                })
    is_staff = data.pop(ISSTAFF_FIELD, None)
    is_rappresentante = data.pop(ISRAPPRESENTANTE_FIELD, None)
    cleaned_input[ISRAPPRESENTANTE_FIELD] = is_staff and is_rappresentante # se non è anche staff non può diventare rappresentante

    # indirizzi
    if addresses_data:
        cleaned_addresses = []
        for address_data in addresses_data:
            address_data_cleaned = cls.validate_address(
                address_data,
                address_type=AddressType.SHIPPING,
                instance=getattr(instance, SHIPPING_ADDRESS_FIELD),
                info=info,
            )
            cleaned_addresses.append(address_data_cleaned)
        cleaned_input[ADDRESSES_FIELD] = cleaned_addresses

    if cleaned_input.get("sconto"):
        if cleaned_input.get("sconto") not in range(0, 0.50):
            raise ValidationError(
                {
                    "sconto": ValidationError(
                        "Sconto da 0% e 50%", code="value", params={"sconto":cleaned_input.get("sconto")}
                    )
                })

    return cleaned_input

# class rappresentanteInput(graphene.InputObjectType):
#     UserGrigo_id = graphene.String()

class ContattoInput(graphene.InputObjectType):
    denominazione = graphene.String(description="nome completo")
    email = graphene.String(description="The email address of the user.")
    phone = graphene.String(description="telefono dell'utente")
class ClienteInput(UserCreateInput):
    denominazione = graphene.String(description="nome completo")
    id_danea = graphene.String(description="id cliene nel programma DaneaEsayfatt")
    tipo_cliente = graphene.String(choice = models.TIPO_CLIENTE_CHOICES, default = models.TIPO_CLIENTE_DEFAULT)

    tel = graphene.String(description="telefono dell'utente")
    cell = graphene.String(description="cellulare dell'utente")
    
    #is_no_login = models.BooleanField(default=False) # sostituito per 
    rappresentante = graphene.String(description="email del rappresentate")
    # dati azienda
    piva = graphene.String()
    cf = graphene.String()
    # ragione sociale nel nome
    pec = graphene.String()
    sdi = graphene.String()
    #Pubblica amministrazione
    rif_ammin = graphene.String()
    split_payment = graphene.Boolean(default=False)

    addresses = graphene.List(AddressInput)

    iva = graphene.String()
    porto = graphene.String(choice = models.PORTO_CHOICES, default = models.PORTO_DEFAULT) # franco, assegnato, ecc
    vettore = graphene.String(choice = models.VETTORE_CHOICES, default = models.VETTORE_DEFAULT) # franco, assegnato, ecc
    pagamento = graphene.String()
    coordinate_bancarie = graphene.String()
    listino = graphene.String()
    sconto = graphene.Float()
class StaffInput(ClienteInput):
    #rappresentante
    is_staff = graphene.Boolean(defult = False, description="se questo utente è uno staff.")
    is_rappresentante = graphene.Boolean(defult = False, description="se questo staff è un rappresentante. DEVE essere anche STAFF!")
    commissione = graphene.Float(default = 0, description="compenso che ha il prappresentante con i suoi clienti")
           
    
class ClienteCrea(CustomerCreate):
    class Arguments:
        input = ClienteInput(
            description="Fields required to create a customer.", required=True
        )
    class Meta:
        description = "Creates a new customer."
        exclude = ["password"]
        permissions = (AccountPermissions.MANAGE_USERS,)
        error_type_class = AccountError
        error_type_field = "account_errors"
        model = models.UserExtra

    @classmethod
    def clean_input(cls, info, instance, data):
        billing = data.get(BILLING_ADDRESS_FIELD, None)
        billing_vuoto = True
        if billing:
            for c in billing:
                if billing[c]:
                    billing_vuoto = False
        if billing_vuoto:
            data.pop(BILLING_ADDRESS_FIELD, None)
        cleaned_input = super().clean_input(info, instance, data)

        return clean_account_extra_input(cls, info, instance, data, cleaned_input)



class ClienteAggiorna(CustomerUpdate):
    class Arguments:
        id = graphene.ID(description="ID of a customer to update.", required=True)
        input = ClienteInput(
            description="Fields required to update a customer.", required=True
        )
    class Meta:
        model = models.UserExtra
        description = "Updates an existing customer."
        exclude = ["password"]
        permissions = (AccountPermissions.MANAGE_USERS,)
        error_type_class = AccountError
        error_type_field = "account_errors"

    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = super().clean_input(info, instance, data)
        return clean_account_extra_input(cls, info, instance, data, cleaned_input)

class StaffCrea(StaffCreate):
    class Arguments:
        input = StaffInput(
            description="Fields required to create un utente staff.", required=True
        )
    class Meta:
        description = "Creates a new staff."
        exclude = ["password"]
        permissions = (AccountPermissions.MANAGE_STAFF,)
        error_type_class = AccountError
        error_type_field = "account_errors"
        model = models.UserExtra

    @classmethod
    def clean_input(cls, info, instance, data):
        billing = data.get(BILLING_ADDRESS_FIELD, None)
        billing_vuoto = True
        if billing:
            for c in billing:
                if billing[c]:
                    billing_vuoto = False
        if billing_vuoto:
            data.pop(BILLING_ADDRESS_FIELD, None)
        cleaned_input = super().clean_input(info, instance, data)
        cleaned_input["is_staff"] = True
        cleaned_input["tipo_cliente"] = models.TIPO_CLIENTE_DEFAULT
        return cleaned_input
class StaffAggiorna(StaffUpdate):
    class Arguments:
        id = graphene.ID(description="ID of a staff to update.", required=True)
        input = StaffInput(
            description="Fields required to update a staff.", required=True
        )
    class Meta:
        model = models.UserExtra
        description = "Updates an existing Staff."
        exclude = ["password"]
        permissions = (AccountPermissions.MANAGE_STAFF,)
        error_type_class = AccountError
        error_type_field = "account_errors"

    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = super().clean_input(info, instance, data)
        return clean_account_extra_input(cls, info, instance, data, cleaned_input)

class ContattoCrea(ModelMutation):
    user = graphene.Field(
        type.UserExtra, description="A user instance for which the contacts was created."
    )
    class Arguments:
        user_id = graphene.ID(description="id dell'utente", required=True)
        input = ContattoInput(
            description="Fields required to create un contatto.", required=True
        )
    class Meta:
        description = "Creates a new contatto."
        permissions = (AccountPermissions.MANAGE_USERS,)
        error_type_class = AccountError
        error_type_field = "account_errors"
        model = models.Contatto

    @classmethod
    def perform_mutation(cls, root, info, **data):
        user_id = data["user_id"]
        user = cls.get_node_or_error(info, user_id, field="user_id", only_type=type.UserExtra)
        response = super().perform_mutation(root, info, **data)
        if not response.errors:
            user.contatti.add(response.contatto)
            response.user = user
        return response
    # @classmethod
    # def clean_input(cls, info, instance, data):
    #     cleaned_input = super().clean_input(info, instance, data)
    #     utente_input = getattr(cls.Arguments, "utente")
    #     if utente_input:
    #         utente_da_modificare = models.UserExtra.objects.filter(id=utente_input)
    #         if utente_da_modificare:
    #             cleaned_input["utente"] = utente_da_modificare
    #             return clean_account_extra_input(cls, info, instance, data, cleaned_input)
    #     raise ValidationError("fornisci un id utenteExtra valido")
class ContattoAggiorna(ModelMutation):
    class Arguments:
        id = graphene.ID(description="ID of a contatto to update.", required=True)
        input = ContattoInput(
            description="Fields required to update a contatto.", required=True
        )
    class Meta:
        model = models.Contatto
        description = "Updates an existing Contatto."
        permissions = (AccountPermissions.MANAGE_USERS,)
        error_type_class = AccountError
        error_type_field = "account_errors"

class IndirizzoCrea(ModelMutation):
    user = graphene.Field(
        type.UserExtra, description="A user instance for which the address was created."
    )
    class Arguments:
        user_id = graphene.ID(
            description="ID of a user to create address for.", required=True
        )
        input = AddressInput(
            description="Fields required to create address.", required=True
        )

    class Meta:
        description = "Creates user address."
        model = models_saleor.Address
        permissions = (AccountPermissions.MANAGE_USERS,)
        error_type_class = AccountError
        error_type_field = "account_errors"

    @classmethod
    def perform_mutation(cls, root, info, **data):
        user_id = data["user_id"]
        user = cls.get_node_or_error(info, user_id, field="user_id", only_type=type.UserExtra)
        response = super().perform_mutation(root, info, **data)
        if not response.errors:
            address = info.context.plugins.change_user_address(
                response.address, None, user
            )
            user.addresses.add(address)
            response.user = user
        return response
class IndirizzoAggiorna(AddressUpdate):
    class Meta:
        description = "Updates an address."
        model = models_saleor.Address
        permissions = (AccountPermissions.MANAGE_USERS,)
        error_type_class = AccountError
        error_type_field = "account_errors"

class LoadDataFromDanea(ModelMutation):
    class Arguments:
        id_danea = graphene.String(required= False)
    class Meta:
        description = "Load anagrafica form danea"
        model = models.UserExtra
        exclude = ["password", "email"]
        #permissions = (AccountPermissions.MANAGE_STAFF,)
        error_type_class = AccountError
        error_type_field = "account_errors"

    @classmethod
    def perform_mutation(cls, _root, info, **data):
        id = data["id_danea"]
        instance = cls.get_instance(info, **data)
        cls.clean_instance(info, instance)
        import_anagrafica(id) ## mia
        return cls.success_response(instance)
