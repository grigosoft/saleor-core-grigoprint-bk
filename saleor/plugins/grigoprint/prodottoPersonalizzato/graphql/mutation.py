import graphene

from saleor.saleor.graphql.order.mutations.draft_orders import OrderLineInput

from .....graphql.core.types.common import StaffError

from .....core.permissions import AccountPermissions

from .....graphql.core.mutations import BaseMutation, ModelDeleteMutation, ModelMutation

from .....graphql.core.enums import AccountErrorCode

from .....graphql.account.mutations.staff import CustomerCreate, CustomerUpdate
from .....graphql.account.mutations.account import AccountError
from .....graphql.order.mutations.discount_order import OrderLineInput


from django.core.exceptions import ValidationError

from .. import models
from . import type
class LineaOrdineInput(OrderLineInput):
    padre = graphene.Field(type.LineaOrdine, description="linea ordine padre")
class OrdineInput(ModelMutation):
    
class OrdineCrea(ModelMutation):
    class Arguments:
        input = ParticolareInput(
            description="Fields required to create a Particolare.", required=True
        )
    class Meta:
        description = "Creates a new Settore."
        permissions = (AccountPermissions.MANAGE_STAFF,)
        error_type_class = StaffError
        error_type_field = "staff_errors"
        model = models.Particolare

class ParticolareAggiorna(ModelMutation):
    class Arguments:
        id = graphene.ID(description="ID of a Particolare to update.", required=True)
        input = ParticolareInput(
            description="Fields required to update a Particolare.", required=True
        )
    class Meta:
        description = "Updates an existing settore"
        permissions = (AccountPermissions.MANAGE_STAFF,)
        error_type_class = StaffError
        error_type_field = "staff_errors"
        model = models.Particolare


class ParticolareElimina(ModelDeleteMutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a settore to delete.")
    class Meta:
        description = "Deletes a Particolare."
        model = models.Particolare
        permissions = (AccountPermissions.MANAGE_STAFF,)
        error_type_class = StaffError
        error_type_field = "staff_errors"
