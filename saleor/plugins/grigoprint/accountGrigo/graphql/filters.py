import django_filters
from django.db.models import Q, OuterRef, Exists

from .....graphql.core.types.filter_input import FilterInputObjectType
from .....account.models import Address
from .....graphql.account.filters import CustomerFilter
from ..models import UserExtra, Contatto


def filter_user_grigo_search(qs, _, value):
    if value:
        # preparo gli indirizzi
        UserAddress = UserExtra.addresses.through
        addresses = Address.objects.filter(
            Q(first_name__ilike=value)
            | Q(last_name__ilike=value)
            | Q(city__ilike=value)
            | Q(country__ilike=value)
            | Q(phone=value)
        ).values("id")
        user_addresses = UserAddress.objects.filter(
            Exists(addresses.filter(pk=OuterRef("address_id")))
        ).values("user_id")
        qs = qs.filter(
            Q(email__ilike=value)
            | Q(first_name__ilike=value)
            | Q(last_name__ilike=value)
            | Q(denominazione__ilike=value)
            | Q(id_danea__ilike=value)
            | Q(tel__ilike=value)
            | Q(cell__ilike=value)
            | Q(piva__ilike=value)
            | Q(cf__ilike=value)
            | Q(pec__ilike=value)
            | Q(Exists(user_addresses.filter(user_id=OuterRef("pk"))))
            | Q(contatti__denominazione__ilike=value)
            | Q(contatti__phone__ilike=value)
            | Q(contatti__email__ilike=value)
        ).distinct()
    return qs

def filter_user_rappresentante(qs, _, value):
    if value:
        qs = qs.filter(
            Q(rappresentante__ilike=value)
        )
    return qs
def filter_user_is_staff(qs, _, value):
    if value:
        qs = qs.filter(
            Q(is_staff=value)
        )
    return qs
def filter_user_is_rappresentante(qs, _, value):
    if value:
        qs = qs.filter(
            Q(is_rappresentante=value)
        )
    return qs

class CustomerExtraFilter(CustomerFilter):
    search = django_filters.CharFilter(method=filter_user_grigo_search)
    rappresentante = django_filters.CharFilter(method=filter_user_rappresentante)
    is_staff = django_filters.BooleanFilter(method=filter_user_is_staff)
    is_rappresentante = django_filters.BooleanFilter(method=filter_user_is_rappresentante)

    class Meta:
        model = UserExtra
        fields = [
            #"date_joined",
            "number_of_orders",
            "placed_orders",
            "search",
            "rappresentante",
            "is_staff",
            "is_rappresentante",
        ]

class CustomerExtraFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = CustomerExtraFilter