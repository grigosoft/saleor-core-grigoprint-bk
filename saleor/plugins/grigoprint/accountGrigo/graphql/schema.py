import graphene

from .....core.exceptions import PermissionDenied
from .....core.permissions import AccountPermissions
from .....core.tracing import traced_resolver
from .....graphql.core.utils import from_global_id_or_error
from .....graphql.utils import get_user_or_app_from_context

from .....graphql.core.validators import validate_one_of_args_is_in_query
from .sorters import UserGrigoSortingInput
from .filters import CustomerExtraFilterInput

from .....graphql.core.fields import FilterInputConnectionField

from .....graphql.decorators import staff_member_or_app_required

from .. import models
from . import type

@traced_resolver
def resolve_user(info, id=None, email=None):
    requester = get_user_or_app_from_context(info.context)
    if requester:
        filter_kwargs = {}
        requesterExtra = models.UserExtra.objects.userExtrafromUser(requester)
        if requesterExtra:
            print("requester è un oggetto UserExtra")
            if requesterExtra.is_rappresentante:############################
                print("requester è un rappresentante")
                filter_kwargs["rappresentante"] = requesterExtra
        if id:
            _model, filter_kwargs["pk"] = from_global_id_or_error(id, type.UserExtra)
        if email:
            filter_kwargs["email"] = email
        if requester.has_perms(
            [AccountPermissions.MANAGE_STAFF, AccountPermissions.MANAGE_USERS]
        ):
            return models.UserExtra.objects.filter(**filter_kwargs).first() # tutti
        if requester.has_perm(AccountPermissions.MANAGE_STAFF):
            return models.UserExtra.objects.staff().filter(**filter_kwargs).first()
        if requester.has_perm(AccountPermissions.MANAGE_USERS):
            return models.UserExtra.objects.customers().filter(**filter_kwargs).first()
    return PermissionDenied()
    
class AccountQueries(graphene.ObjectType):
    
    clienti = FilterInputConnectionField(
        type.UserExtra,
        filter=CustomerExtraFilterInput(description="Filtering options for customers."),
        sort_by=UserGrigoSortingInput(description="Sort customers."),
        description="Lista completa di utenti, in base a chi è loggato",
        name = "clienti"
    )
    cliente = graphene.Field(
        type.UserExtra,
        id=graphene.Argument(graphene.ID, description="ID dell'utente"),
        email=graphene.Argument(
            graphene.String, description="Email dell'utente"
        ),
        
        description="Look up a user by ID or email address.",
        name = "cliente"
    )

    # clienti_rappresentante = graphene.Field(
    #     type.UserGrigo,
    #     id=graphene.Argument(graphene.ID, description="ID of the user."),
    #     email=graphene.Argument(
    #         graphene.String, description="Email address of the user."
    #     ),
        
    #     description="Lista completa dei clienti di un rappresentante",
    #     name = "clienti_rappresentante"
    # )
    aliquote_iva = graphene.Field(
        type.Iva,
        description="lista delle aliquote iva disponibili",
        name = "aliquoteIva"
    )
    listini = graphene.Field(
        type.Iva,
        description="listini disponibili",
        name = "listini"
    )

    @staff_member_or_app_required
    #@permission_required(AccountPermissions.MANAGE_USERS)
    def resolve_clienti(self, info, **kwargs):
        requester = get_user_or_app_from_context(info.context)
        if requester:
            print(requester)
            #requesterExtra = models.UserExtra.objects.filter(email="corbella@bandieregrigolini.it").first() # per testare i rappresentanti
            requesterExtra = models.UserExtra.objects.userExtrafromUser(requester)
            print("to user extra --> ",requesterExtra)
            # se rappresentante
            if requesterExtra:
                print("requester è un oggetto UserExtra")
                if requesterExtra.is_rappresentante:
                    print("requester è un rappresentante")
                    return requesterExtra.clienti
            else:
                return models.UserExtra.objects.all()
        return PermissionDenied()

    @staff_member_or_app_required
    def resolve_cliente(self, info, id=None, email=None):
        validate_one_of_args_is_in_query("id", id, "email", email)
        return resolve_user(info, id, email)

    # def resolve_clienti_rappresentante(self, info, id=None, email=None):
    #     validate_one_of_args_is_in_query("id", id, "email", email)
    #     user = resolve_user(info, id, email)
    #     if user.isRappresentante:
    #         return user.clienti
    #     else:
    #         return PermissionDenied("Questo utente non è un rappresentante")
   
    @staff_member_or_app_required
    def resolve_aliquote_iva(self, info, **kwargs):
        return models.Iva.objects.all()
        
    @staff_member_or_app_required
    def resolve_listini(self, info, **kwargs):
        return models.Listino.objects.all()

