from graphene import relay
from graphene_federation.entity import key
from .....graphql.account.types import User, ObjectWithMetadata
from .. import models

@key("id")
@key("email")
class Personalizzazione(User):
    class Meta:
        description = "Represents user data."
        interfaces = [relay.Node, ObjectWithMetadata]
        model = models.UserGrigo
       