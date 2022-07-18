from django.utils.translation import gettext_lazy as _
from django.db import models


class Porto(models.TextChoices):
    FRESHMAN = 'FR', _('Freshman')
