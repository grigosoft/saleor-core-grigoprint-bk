from graphene import relay
import graphene
from graphene_federation.entity import key

from .....graphql.core.connection import CountableDjangoObjectType
from .. import models
from .....checkout import models as sal_ck_models
from .....order import models as sal_o_models
from .....graphql.order import types as sal_o_types


@key("id")
class Particolare(CountableDjangoObjectType):
    class Meta:
        description = "Rappresenta un particolare"
        interfaces = [relay.Node]
        model = models.Particolare
        fields = "__all__"
@key("id")
class Finitura(CountableDjangoObjectType):
    class Meta:
        description = "Rappresenta una finitura"
        interfaces = [relay.Node]
        model = models.Finitura
        fields = "__all__"
@key("id")
class ParticolareFinitura(CountableDjangoObjectType):
    class Meta:
        description = "Rappresenta come sono collegati i particolari e le finiture"
        interfaces = [relay.Node]
        model = models.ParticolareFinitura
        fields = "__all__"

@key("id")
class Tessuto(CountableDjangoObjectType):
    class Meta:
        description = "Rappresenta un tessuto"
        interfaces = [relay.Node]
        model = models.Tessuto
        fields = "__all__"

@key("id")
class LineaCarrello(CountableDjangoObjectType):
    class Meta:
        description = "Rappresenta una linea Carrello"
        interfaces = [relay.Node]
        model = models.LineaCarrello
        fields = "__all__"
@key("id")
class LineaOrdine(CountableDjangoObjectType):
    class Meta:
        description = "Rappresenta una linea ordine"
        interfaces = [relay.Node]
        model = models.LineaOrdine
        fields = "__all__"
@key("id")
class Personalizzazione(CountableDjangoObjectType):
    # personalizzazione_precedente = graphene.Field("Personalizzazione", description="personalizzazione precedente")
    linea_carrello = graphene.Field(LineaCarrello, description="linea checkout legata a questa personalizzazione")
    linea_ordine = graphene.Field(LineaOrdine, description="linea ordine legata a questa personalizzazione")
    tessuto = graphene.Field(Tessuto, description="tessuto da utilizzare in questa personalizzazione")
    class Meta:
        description = "Rappresenta una personalizzazione di un prodotto"
        interfaces = [relay.Node]
        model = models.Personalizzazione
        fields = "__all__"

class Ordine(sal_o_types.Order):
    lines = graphene.List(
        lambda: LineaOrdine, required=True, description="List of order lines."
    )
    @staticmethod
    def resolve_lines(root: sal_o_models.Order, info):
        #return OrderLinesByOrderIdLoader(info.context).load(root.id) TODO
        return sal_o_models.OrderLine.objects.filter(order_id__in=root.id)