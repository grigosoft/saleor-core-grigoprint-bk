import graphene
from django.db.models import Count, QuerySet

from .....graphql.account.sorters import UserSortField
from .....graphql.core.types.sort_input import SortInputObjectType


class UserGrigoSortField(graphene.Enum):
    DENOMINAZIONE = ["denominazione", "pk"]
    RAPPRESENTANTE = ["rappresentante", "denominazione", "pk"]
    LISTINO = ["listino", "denominazione", "pk"]
    SCONTO = ["sconto", "denominazione", "pk"]
    EMAIL = ["email"]
    ORDER_COUNT = ["order_count", "email"]

    @property
    def description(self):
        if self.name in UserGrigoSortField.__enum__._member_names_:
            sort_name = self.name.lower().replace("_", " ")
            return f"Sort users by {sort_name}."
        raise ValueError("Unsupported enum value: %s" % self.value)

    @staticmethod
    def qs_with_order_count(queryset: QuerySet, **_kwargs) -> QuerySet:
        return queryset.annotate(order_count=Count("orders__id"))

class UserGrigoSortingInput(SortInputObjectType):
    class Meta:
        sort_enum = UserGrigoSortField
        type_name = "userGrigos"