import graphene

from .....core.exceptions import PermissionDenied
from .....core.permissions import AccountPermissions
from .....core.tracing import traced_resolver
from .....graphql.core.utils import from_global_id_or_error
from .....graphql.utils import get_user_or_app_from_context

from .....graphql.core.validators import validate_one_of_args_is_in_query
from .sorters import UserGrigoSortingInput
from .filters import CustomerGrigoFilterInput

from .....graphql.core.fields import FilterInputConnectionField

from .....graphql.decorators import staff_member_or_app_required

from .. import models
from . import type

@traced_resolver
def resolve_user(info, id=None, email=None):
    requester = get_user_or_app_from_context(info.context)
    if requester:
        filter_kwargs = {}
        if id:
            _model, filter_kwargs["pk"] = from_global_id_or_error(id, type.UserGrigo)
        if email:
            filter_kwargs["email"] = email
        if requester.has_perms(
            [AccountPermissions.MANAGE_STAFF, AccountPermissions.MANAGE_USERS]
        ):
            return models.UserGrigo.objects.filter(**filter_kwargs).first()
        if requester.has_perm(AccountPermissions.MANAGE_STAFF):
            return models.UserGrigo.objects.staff().filter(**filter_kwargs).first()
        if requester.has_perm(AccountPermissions.MANAGE_USERS):
            return models.UserGrigo.objects.customers().filter(**filter_kwargs).first()
    return PermissionDenied()
    
class AccountQueries(graphene.ObjectType):
    
    customers_grigo = FilterInputConnectionField(
        type.UserGrigo,
        filter=CustomerGrigoFilterInput(description="Filtering options for customers."),
        sort_by=UserGrigoSortingInput(description="Sort customers."),
        description="Lista completa di utenti",
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
    rappresentanti = FilterInputConnectionField(
        type.UserGrigo,
        sort_by=UserGrigoSortingInput(description="Sort customers."),
        
        description="Listcompleta dei rappresentanti",
        name = "rappresentanti_grigo"
    )

    clienti_rappresentante = graphene.Field(
        type.UserGrigo,
        id=graphene.Argument(graphene.ID, description="ID of the user."),
        email=graphene.Argument(
            graphene.String, description="Email address of the user."
        ),
        
        description="Lista completa dei clienti di un rappresentante",
        name = "clienti_rappresentante"
    )
    

    @staff_member_or_app_required
    #@permission_required(AccountPermissions.MANAGE_USERS)
    def resolve_customers_grigo(self, _info, **kwargs):
        return models.UserGrigo.objects.all()

    def resolve_client_grigo(self, info, id=None, email=None):
        validate_one_of_args_is_in_query("id", id, "email", email)
        return resolve_user(info, id, email)

    @staff_member_or_app_required
    def resolve_rappresentanti(self, _info, **kwargs):
        return models.UserGrigo.objects.filter(is_rappresentante=True)

    def resolve_clienti_rappresentante(self, info, id=None, email=None):
        validate_one_of_args_is_in_query("id", id, "email", email)
        user = resolve_user(info, id, email)
        if user.isRappresentante:
            return user.clienti
        else:
            raise PermissionDenied("Questo utente non è un rappresentante")
   
    
