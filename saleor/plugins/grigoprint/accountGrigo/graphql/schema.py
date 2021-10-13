import graphene
from .....graphql.account.schema import CustomerFilterInput
from .....graphql.account.sorters import UserSortingInput

from .....graphql.core.fields import FilterInputConnectionField

from .....graphql.decorators import staff_member_or_app_required

from .. import models
from . import type

class AccountQueries(graphene.ObjectType):
    
    customers_grigo = FilterInputConnectionField(
        type.UserGrigo,
        filter=CustomerFilterInput(description="Filtering options for customers."),
        sort_by=UserSortingInput(description="Sort customers."),
        description="Look up a user by ID or email address.",
        name = "customers_grigo"
    )
    client_grigo = graphene.Field(
        type.UserGrigo,
        id=graphene.Argument(graphene.ID, description="ID of the user."),
        email=graphene.Argument(
            graphene.String, description="Email address of the user."
        ),
        
        description="Look up a user by ID or email address.",
        name = "client_grigo"
    )

    @staff_member_or_app_required
    #@permission_required(AccountPermissions.MANAGE_USERS)
    def resolve_customers_grigo(self, _info, **kwargs):
        return models.UserGrigo.objects.all()