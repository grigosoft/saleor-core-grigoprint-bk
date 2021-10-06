from .....core.permissions import AccountPermissions

from .....graphql.core.enums import AccountErrorCode

from .....graphql.account.mutations.staff import CustomerCreate, CustomerUpdate
from .....graphql.account.mutations.account import AccountInput, AccountError
from .....graphql.account.mutations.base import (
    CustomerInput,
)

from .. import models
from . import type


class CustomerCreateGrigo(CustomerCreate):
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
