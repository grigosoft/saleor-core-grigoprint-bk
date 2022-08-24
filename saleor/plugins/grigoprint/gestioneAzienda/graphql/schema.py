import graphene
from graphql import GraphQLError

from .....core.exceptions import PermissionDenied
from .....graphql.utils import get_user_or_app_from_context

# from .sorters import UserGrigoSortingInput
from .filters import FerieFilterInput, NotificheFilterInput

from .....graphql.core.fields import FilterInputConnectionField

from .....graphql.decorators import staff_member_or_app_required

from .. import models
from . import type
from .....account.models import User

class GestioneAziendaQueries(graphene.ObjectType):
    
    settori = graphene.List(
        type.Settore,
        description="Lista completa dei settori dell'azienda",
        name = "settori"
    )
    ferie = FilterInputConnectionField(
        type.Ferie,
        filter=FerieFilterInput(description="Filtering options for Ferie."),
        description="Lista delle ferie dei dipendenti dell'azienda",
        name = "ferie"
    )
    notifiche = FilterInputConnectionField(
        type.Notifica,
        filter=NotificheFilterInput(description="Filtering options for Notfiche."),
        description="Lista delle notifiche interne dell'azienda",
        name = "notifiche"
    )
    ore_lavorative_per_giorno_e_settore = graphene.Field(
        graphene.Int,
        id=graphene.Argument(graphene.ID, description="ID del settore"),
        data=graphene.Argument(graphene.Date, description="giorno "),
        description="trova le ore lavorative disponibili in un certo settore in un tal giorno",
        name = "ore_lavorative_per_giorno_e_settore"
    )
    ore_lavorative_occupate_per_giorno_e_settore = graphene.Field(
        graphene.Int,
        id=graphene.Argument(graphene.ID, description="ID del settore"),
        data=graphene.Argument(graphene.Date, description="giorno "),
        description="trova le ore lavorative occupate in un certo settore in un tal giorno",
        name = "ore_lavorative_occupate_per_giorno_e_settore"
    )

    @staff_member_or_app_required
    #@permission_required(AccountPermissions.MANAGE_USERS)
    def resolve_settori(self, info, **kwargs):
        requester = get_user_or_app_from_context(info.context)
        if requester:
            return models.Settore.objects.all()
        return PermissionDenied()
    @staff_member_or_app_required
    #@permission_required(AccountPermissions.MANAGE_USERS)
    def resolve_ferie(self, info, **kwargs):
        requester = get_user_or_app_from_context(info.context)
        if requester:
            return models.Ferie.objects.all()
        return PermissionDenied()
    @staff_member_or_app_required
    #@permission_required(AccountPermissions.MANAGE_USERS)
    def resolve_notifiche(self, info, **kwargs):
        requester = get_user_or_app_from_context(info.context)
        if requester:
            return models.Notifica.objects.all()
        return PermissionDenied()
    @staff_member_or_app_required
    #@permission_required(AccountPermissions.MANAGE_USERS)
    def resolve_ore_lavorative_per_giorno_e_settore(self, info, id=None, data=None):
        requester = get_user_or_app_from_context(info.context)
        if requester:
            if id and data:
                user = User.objects.filter(email="02advitalia@gmail.com").first()
                print(user.piva)
                print(user.extra.email)
                # filter_kwargs = {}
                # settore = models.Settore.objects.filter(id=id).first()
                # if settore:
                #     lista_dipendenti = settore.gruppo.users
                #     print(lista_dipendenti)
                #     tot_ore = 0
                #     for dipendenti in lista_dipendenti:
                #         tot_ore += dipendenti.ore_lavoro
                #     return tot_ore
                # return GraphQLError("settore non trovato")
            return GraphQLError("i parametri ID settore e DATA vanno forniti")
        return PermissionDenied()
    @staff_member_or_app_required
    #@permission_required(AccountPermissions.MANAGE_USERS)
    def resolve_ore_lavorative_occupate_per_giorno_e_settore(self, info, id=None, data=None):
        requester = get_user_or_app_from_context(info.context)
        if requester:
            if id and data:
                filter_kwargs = {}
                settore = models.Settore.objects.filter(id=id).first()
                if settore:
                    filter_kwargs["settore"] = settore
                    filter_kwargs["data"] = data
                    lista_personalizzazioni = models.TempiPersonalizzazioneSettore.objects.filter(filter_kwargs)
                    tot_ore = 0
                    for personalizzazioni in lista_personalizzazioni:
                        tot_ore += personalizzazioni.ore_lavoro
                    return tot_ore
                return GraphQLError("settore non trovato")
            return GraphQLError("i parametri ID settore e DATA vanno forniti")
        return PermissionDenied()