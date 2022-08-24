import graphene
from graphene_django import DjangoObjectType
from graphene_federation.entity import key

from .....graphql.decorators import permission_required
from .....core.permissions import AccountPermissions



from .....graphql.core.connection import CountableDjangoObjectType
from .....graphql.account.types import Group, User, ObjectWithMetadata
from ...gestioneAzienda.graphql.type import Ferie, Notifica
from ...gestioneAzienda import models as gestioneAziendaModels
from .. import models
from django.contrib.auth import models as auth_models
@key("id")
class Contatto(CountableDjangoObjectType):
    class Meta:
        description = "Represents user contacts"
        interfaces = [graphene.relay.Node,]
        model = models.Contatto
        fields = "__all__"
@key("id")
class Listino(DjangoObjectType):
    class Meta:
        description = "Listino"
        interfaces = []
        model = models.Listino
        fields = "__all__"
@key("id")
@key("denominazione")
class Iva(DjangoObjectType):
    class Meta:
        description = "Listino"
        interfaces = []
        model = models.Iva
        fields = "__all__"

@key("id")
@key("email")
class UserExtra(User):
    contatti = graphene.List(Contatto, description="List of all user's contacts.")
    iva = graphene.Field(Iva, description="iva di default di questo cliente")
    listino = graphene.Field(Listino, description="listino di questo cliente")
    ferie = graphene.List(Ferie, description="ferie richieste di un cliente")
    notifiche = graphene.List(Notifica, description="notifiche inviate da un cliente")
    class Meta:
        description = "Represents user data."
        interfaces = [graphene.relay.Node, ObjectWithMetadata]
        model = models.UserExtra
        exclude = ["password"]
        convert_choices_to_enum = ["porto","vettore","tipo_cliente"]
        #fields = "__all__"
        #only_fields = [
        #    "date_joined",
        #]

    @staticmethod
    def resolve_contatti(root: models.UserExtra, _info, **_kwargs):
        return root.contatti.all()
    @staticmethod
    def resolve_iva(root: models.UserExtra, _info, **_kwargs):
        return root.iva
    @staticmethod
    def resolve_listino(root: models.UserExtra, _info, **_kwargs):
        return root.listino
    @staticmethod
    def resolve_ferie(root: models.UserExtra, _info, **_kwargs):
        if root.is_staff:
            # return root.ferie
            return gestioneAziendaModels.Ferie.objects.filter(utente=root.id)
        return None
    @staticmethod
    def resolve_notifiche(root: models.UserExtra, _info, **_kwargs):
        if root.is_staff:
            return gestioneAziendaModels.Notifica.objects.filter(mittente=root.id)
        return None

        
# @key(fields="id")
# class Gruppo(Group):
#     users = graphene.List(UserExtra, description="List of group users")

#     class Meta:
#         description = "Represents permission group data."
#         interfaces = [graphene.relay.Node]
#         model = auth_models.Group
#         only_fields = ["name", "permissions", "id"]

#     @staticmethod
#     @permission_required(AccountPermissions.MANAGE_STAFF)
#     def resolve_users(root: auth_models.Group, _info):
#         users = root.user_set.all()
#         usersExtra = []
#         for user in users:
#             if hasattr(user, 'extra'):
#                 usersExtra = user.extra
#         return usersExtra
