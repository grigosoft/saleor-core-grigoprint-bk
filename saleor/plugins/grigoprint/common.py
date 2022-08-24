from ...account.models import User
from .accountGrigo import models

from ...core.exceptions import PermissionDenied

def get_user_extra(user):
    if isinstance(models.UserExtra, user):
        return user
    elif isinstance(User, user):
        if hasattr(user, "extra"):
            return user.extra
        else:
            return models.UserExtra.objects.userExtrafromUser(user)
    raise PermissionDenied("Deve essere un istanza di un Utente")

def get_user_extra_or_error(user):
    userExtra = get_user_extra(user)
    if userExtra:
        return userExtra
    raise PermissionDenied("Deve essere un istanza di un Utente")