from graphene import relay, List
from graphene_federation.entity import key

from .....graphql.core.connection import CountableDjangoObjectType
from .....graphql.account.types import User, ObjectWithMetadata
from .. import models

@key("id")
class Contatto(CountableDjangoObjectType):
    class Meta:
        description = "Represents user contacts"
        interfaces = [relay.Node,]
        model = models.Contatto
        fields = "__all__"
@key("id")
@key("email")
class UserExtra(User):
    contatti = List(Contatto, description="List of all user's contacts.")
    class Meta:
        description = "Represents user data."
        interfaces = [relay.Node, ObjectWithMetadata]
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