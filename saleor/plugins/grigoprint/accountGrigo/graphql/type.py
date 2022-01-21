from graphene import relay
from graphene_federation.entity import key
from .....graphql.account.types import User, ObjectWithMetadata
from .. import models

@key("id")
@key("email")
class UserGrigo(User):
    class Meta:
        description = "Represents user data."
        interfaces = [relay.Node, ObjectWithMetadata]
        model = models.UserGrigo
        exclude = ["password"]
        #fields = "__all__"
        #only_fields = [
        #    "date_joined",
        #    "default_billing_address",
        #    "default_shipping_address",
        #    "email",
        #    "first_name",
        #    "id",
        #    "is_active",
        #    "is_staff",
        #    "last_login",
        #    "last_name",
        #    "note",
        #    "rappresentante",
        #    "commissione",
        #    "piva",
        #    "cf",
        #    "sdi",
        #    "split_payment",
        #    "sconto",
        #    "rappresentante"
        #]