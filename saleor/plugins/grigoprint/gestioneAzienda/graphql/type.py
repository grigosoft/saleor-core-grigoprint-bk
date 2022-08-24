import graphene
from graphene_django import DjangoObjectType
from graphene_federation.entity import key

from .....graphql.core.connection import CountableDjangoObjectType
from .. import models

@key("id")
class Settore(CountableDjangoObjectType):
    class Meta:
        description = "descrive un settore nell'azienda"
        interfaces = [graphene.relay.Node,]
        model = models.Settore
        fields = "__all__"
@key("id")
class TempiPersonalizzazioneSettore(CountableDjangoObjectType):
    class Meta:
        description = "raccoglie i tempi di produzione di una certa personalizzazione, divisi per settore"
        interfaces = []
        model = models.TempiPersonalizzazioneSettore
        fields = "__all__"
@key("id")
class Notifica(CountableDjangoObjectType):
    class Meta:
        description = "rappresenta un Messaggio-Notifica inviato all'interno dell'azienda"
        interfaces = [graphene.relay.Node,]
        model = models.Notifica
        fields = "__all__"
@key("id")
class Ferie(CountableDjangoObjectType):
    class Meta:
        description = "descrive le ferie dei dipendenti"
        interfaces = [graphene.relay.Node,]
        model = models.Ferie
        fields = "__all__"