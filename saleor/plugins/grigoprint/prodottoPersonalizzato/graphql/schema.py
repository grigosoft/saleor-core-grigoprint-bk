import graphene

from .filters import ParticolareFilterInput

from .....graphql.core.fields import FilterInputConnectionField

from .....graphql.decorators import staff_member_or_app_required

from .. import models
from . import type

    
class ProdottoPersonalizzatoQueries(graphene.ObjectType):
    
    particolari = FilterInputConnectionField(
        type.Particolare,
        filter=ParticolareFilterInput(description="Filtering options for customers."),
        description="Lista dei particolari",
        name = "customers_grigo"
    )
    finiture = graphene.List(
        type.Finitura,
        description="Lista finiture",
        name = "client_grigo"
    )
    particolari_finiture = graphene.List(
        type.ParticolareFinitura,
        description="Lista particolari legati alle finiture",
        name = "client_grigo"
    )
    

    @staff_member_or_app_required
    #@permission_required(AccountPermissions.MANAGE_USERS)
    def resolve_particolari(self, _info, **kwargs):
        return models.Particolare.objects.all()
    @staff_member_or_app_required
    def resolve_particolari_finiture(self, _info, **kwargs):
        return models.ParticolareFinitura.objects.all()

    @staff_member_or_app_required
    #@permission_required(AccountPermissions.MANAGE_USERS)
    def resolve_finiture(self, _info, **kwargs):
        return models.Finitura.objects.all()

