
import django_filters
from django.db.models import Q, Exists, OuterRef

from .....graphql.core.filters import MetadataFilterBase

from .....graphql.core.types.filter_input import FilterInputObjectType
from .. import models


def filter_finitura(qs, _, value):
    if value:
        qs = qs.filter(
            Q(particolare_finitura__finitura__ilike=value)
        )
    return qs

class ParticolareFilter(MetadataFilterBase):
    finitura = django_filters.CharFilter(method=filter_finitura)
    
    class Meta:
        model = models.Particolare
        fields = [
            "finitura"
        ]

class ParticolareFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = ParticolareFilter