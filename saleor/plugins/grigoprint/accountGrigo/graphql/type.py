import graphene
from graphene_django import DjangoObjectType
from graphene_federation.entity import key

from .....graphql.core.connection import CountableDjangoObjectType
from .....graphql.account.types import User, ObjectWithMetadata
from .. import models

@key("id")
class Contatto(CountableDjangoObjectType):
    class Meta:
        description = "Represents user contacts"
        interfaces = [graphene.relay.Node,]
        model = models.Contatto
        fields = "__all__"
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