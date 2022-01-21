from tokenize import String
import graphene

from .....checkout import AddressType

from .....graphql.account.types import AddressInput

from .....core.permissions import AccountPermissions

from .....graphql.core.enums import AccountErrorCode

from .....graphql.account.mutations.staff import CustomerCreate, CustomerUpdate
from .....graphql.account.mutations.account import AccountError
from .....graphql.account.mutations.base import (
    SHIPPING_ADDRESS_FIELD,
    UserCreateInput,
)
from django.core.exceptions import ValidationError

from .. import models
from . import type

ADDRESSES_FIELD = "addresses"

class rappresentanteInput(graphene.InputObjectType):
    id = graphene.String()

class CustomerCreateGrigoInput(UserCreateInput):
    denominazione = graphene.String()
    id_danea = graphene.String()

    #phone = graphene.String()
    
    #is_no_login = models.BooleanField(default=False) # sostituito per 
    #rappresentante
    is_rappresentante = graphene.Boolean()
    rappresentante = rappresentanteInput()
    commissione = graphene.Float()
    # dati azienda
    piva = graphene.String()
    cf = graphene.String()
    # ragione sociale nel nome
    pec = graphene.String()
    sdi = graphene.String()
    #Pubblica amministrazione
    rif_ammin = graphene.String()
    split_payment = graphene.String()

    addresses = graphene.List(AddressInput)

    iva = graphene.String()
    porto = graphene.String() # franco, assegnato, ecc
    pagamento = graphene.String()
    coordinate_bancarie = graphene.String()
    listino = graphene.String()
    sconto = graphene.Float()
    
    @classmethod
    def clean_input(cls, info, instance, data):
        addresses_data = data.pop(ADDRESSES_FIELD, None)
        cleaned_input = super().clean_input(info, instance, data)

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

    # @classmethod
    # @traced_atomic_transaction()
    # def save(cls, info, instance, cleaned_input):
    #     default_shipping_address = cleaned_input.get(SHIPPING_ADDRESS_FIELD)
    #     if default_shipping_address:
    #         default_shipping_address = info.context.plugins.change_user_address(
    #             default_shipping_address, "shipping", instance
    #         )
    #         default_shipping_address.save()
    #         instance.default_shipping_address = default_shipping_address
    #     default_billing_address = cleaned_input.get(BILLING_ADDRESS_FIELD)
    #     if default_billing_address:
    #         default_billing_address = info.context.plugins.change_user_address(
    #             default_billing_address, "billing", instance
    #         )
    #         default_billing_address.save()
    #         instance.default_billing_address = default_billing_address

    #     is_creation = instance.pk is None
    #     super().save(info, instance, cleaned_input)
    #     if default_billing_address:
    #         instance.addresses.add(default_billing_address)
    #     if default_shipping_address:
    #         instance.addresses.add(default_shipping_address)

    #     # The instance is a new object in db, create an event
    #     if is_creation:
    #         info.context.plugins.customer_created(customer=instance)
    #         account_events.customer_account_created_event(user=instance)
    #     else:
    #         info.context.plugins.customer_updated(instance)

    #     if cleaned_input.get("redirect_url"):
    #         channel_slug = cleaned_input.get("channel")
    #         if not instance.is_staff:
    #             channel_slug = clean_channel(
    #                 channel_slug, error_class=AccountErrorCode
    #             ).slug
    #         elif channel_slug is not None:
    #             channel_slug = validate_channel(
    #                 channel_slug, error_class=AccountErrorCode
    #             ).slug
    #         send_set_password_notification(
    #             cleaned_input.get("redirect_url"),
    #             instance,
    #             info.context.plugins,
    #             channel_slug,
    #         )
            
    
class CustomerCreateGrigo(CustomerCreate):
    class Arguments:
        input = CustomerCreateGrigoInput(
            description="Fields required to create a customer.", required=True
        )
    class Meta:
        description = "Creates a new customer."
        exclude = ["password"]
        permissions = (AccountPermissions.MANAGE_USERS,)
        error_type_class = AccountError
        error_type_field = "account_errors"
        model = models.UserGrigo

    # @classmethod
    # def get_type_for_model(cls):
    #     return type.UserGrigo

    # @classmethod
    # def perform_mutation(cls, root, info, **data):
    #     if "addresses" in data["input"]:
    #         adresses = data["input"]["addresses"]
    #         data["input"]["addreses"] = None
    #         print(adresses)
    #         response = super().perform_mutation(root, info, **data)
    #         #if response:
    #         print("test")
    #         print(response)
    #         return 
    #     else:
    #         super().perform_mutation( root, info, **data)



class CustomerUpdateGrigo(CustomerUpdate):
    class Arguments:
        id = graphene.ID(description="ID of a customer to update.", required=True)
        input = CustomerCreateGrigoInput(
            description="Fields required to update a customer.", required=True
        )
    class Meta:
        model = models.UserGrigo
        description = "Updates an existing customer."
        exclude = ["password"]
        permissions = (AccountPermissions.MANAGE_USERS,)
        error_type_class = AccountError
        error_type_field = "account_errors"

