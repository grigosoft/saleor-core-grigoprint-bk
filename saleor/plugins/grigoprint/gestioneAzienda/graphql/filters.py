import django_filters
from django.db.models import Q

from .....graphql.core.filters import MetadataFilterBase

from .....graphql.core.types.filter_input import FilterInputObjectType
from .. import models
from .....graphql.utils.filters import filter_range_field

def filter_date(qs, _, value):
    qs = filter_range_field(qs, "data_inizio__date", value)
    qs = filter_range_field(qs, "data_fine__date", value)
    return qs
def filter_user_rappresentante(qs, _, value):
    if value:
        qs = qs.filter(
            Q(rappresentante__ilike=value)
        )
    return qs
def filter_search_dipendente(qs, _, value):
    if value:
        qs = qs.filter(
            Q(utente__denominazione__ilike=value)
            | Q(utente__first_name__ilike=value)
            | Q(utente__last_name__ilike=value)
            | Q(utente__email__ilike=value)
        )
    return qs
def filter_approvate(qs, _, value):
    if value:
        qs = qs.filter(
            Q(approvate=value)
        )
    return qs

class FerieFilter(MetadataFilterBase):
    data = django_filters.DateRangeFilter(method=filter_date)
    search_dipendente = django_filters.CharFilter(method=filter_search_dipendente)
    approvate = django_filters.BooleanFilter(method=filter_approvate)
    
    class Meta:
        model = models.Ferie
        fields = [
            "data",
            "search_dipendente",
            "approvate"
        ]

class FerieFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = FerieFilter


def filter_creazione(qs, _, value):
    return filter_range_field(qs, "data__date", value)
def filter_scadenza(qs, _, value):
    return filter_range_field(qs, "scadenza__date", value)
def filter_completate(qs, _, value):
    if value:
        qs = qs.filter(
            Q(completa=value)
        )
    return qs
def filter_search_mittente(qs, _, value):
    if value:
        qs = qs.filter(
            Q(mittente__denominazione__ilike=value)
            | Q(mittente__first_name__ilike=value)
            | Q(mittente__last_name__ilike=value)
            | Q(mittente__email__ilike=value)
        )
    return qs
class NotificheFilter(MetadataFilterBase):
    data_creazione = django_filters.DateRangeFilter(method=filter_creazione)
    data_scadenza = django_filters.DateRangeFilter(method=filter_scadenza)
    search_mittente = django_filters.CharFilter(method=filter_search_mittente)
    completate = django_filters.BooleanFilter(method=filter_completate)
    
    class Meta:
        model = models.Notifica
        fields = [
            "data_creazione",
            "data_scadenza",
            "search_mittente",
            "completate"
        ]

class NotificheFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = NotificheFilter