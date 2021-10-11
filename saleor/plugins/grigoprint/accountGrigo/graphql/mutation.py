import graphene

from .....core.permissions import AccountPermissions

from .....graphql.core.enums import AccountErrorCode

from .....graphql.account.mutations.staff import CustomerCreate, CustomerUpdate
from .....graphql.account.mutations.account import AccountError
from .....graphql.account.mutations.base import (
    UserCreateInput,
)

from .. import models
from . import type

class CustomerCreateGrigoInput(UserCreateInput):
    #rappresentante = models.UserGrigo
    commissione = graphene.Float()
    # dati azienda
    piva = graphene.String()
    cf = graphene.String()
    # ragione sociale nel nome
    pec = graphene.String()
    piva = graphene.String()
    sdi = graphene.String()
    split_payment = graphene.Boolean()
    # listino = 
    sconto = graphene.Float()
    is_no_login = graphene.Boolean()
    
class CustomerCreateGrigo(CustomerCreate):
    class Arguments:
        input = CustomerCreateGrigoInput(
            description="Fields required to create a customer.", required=True
        )
    class Meta:
        description = "Creates a new customer."
        exclude = ["password"]
        permissions = (AccountPermissions.MANAGE_USERS,)
        error_type_class = AccountErrorCode
        error_type_field = "account_errors"
        model = models.UserGrigo

    @classmethod
    def get_type_for_model(cls):
        return type.UserGrigo


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

    @classmethod
    def get_type_for_model(cls):
        return type.UserGrigo
