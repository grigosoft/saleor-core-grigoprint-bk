import graphene

from .....core.exceptions import PermissionDenied

from .....graphql.core.types.common import StaffError

from .....graphql.core.mutations import BaseMutation, ModelDeleteMutation, ModelMutation

from .....core.permissions import AccountPermissions

from .....graphql.utils import get_user_or_app_from_context


from .. import models
from ...accountGrigo import models as models_account
from .....account import models as models_saleor
from . import type
from ...accountGrigo.graphql import type as type_account

USER_FIELD = "utente"


class SettoreInput(graphene.InputObjectType):
    gruppo = graphene.ID(description="gruppo di appartenenza")
    denominazione = graphene.String(description="nome Settore")
    info = graphene.String(description="informazioni sul settore")

class NotificaCreaInput(graphene.InputObjectType):
    mittente  = graphene.ID(description="utente che ha creato la notifica")
    settore = graphene.ID(description="Settore di destinazione")
    scadenza = graphene.DateTime(description="data scadenza")
    titolo = graphene.String(description="titolo notifica")
    testo = graphene.String(description="testo notifica")
class NotificaInput(NotificaCreaInput):
    data = graphene.DateTime(description="data creazione")
    completata = graphene.Boolean(description="notifica completata")

class RichiediFerieInput(graphene.InputObjectType):
    data_inizio = graphene.Date(description="primo giorno a casa")
    data_fine = graphene.Date(description="ultimo giorno a casa")
    ore = graphene.Int(description="ore di permesso")
    motivazione = graphene.String(description="motivo richiesta ferie")
class FerieConfermaInput(graphene.InputObjectType):
    info_approvazione = graphene.String(description="info aupprovazione ferie")
class FerieInput(RichiediFerieInput, FerieConfermaInput):
    utente = graphene.ID(description="utente che ha richiesto le ferie")
    approvate = graphene.Boolean(description="ferie autorizzate")
    
class SettoreCrea(ModelMutation):
    class Arguments:
        input = SettoreInput(
            description="Fields required to create a customer.", required=True
        )
    class Meta:
        description = "Creates a new Settore."
        permissions = (AccountPermissions.MANAGE_STAFF,)
        error_type_class = StaffError
        error_type_field = "staff_errors"
        model = models.Settore

class SettoreAggiorna(ModelMutation):
    class Arguments:
        id = graphene.ID(description="ID of a settore to update.", required=True)
        input = SettoreInput(
            description="Fields required to update a settore.", required=True
        )
    class Meta:
        description = "Updates an existing settore"
        permissions = (AccountPermissions.MANAGE_STAFF,)
        error_type_class = StaffError
        error_type_field = "staff_errors"
        model = models.Settore


class SettoreElimina(ModelDeleteMutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a settore to delete.")
    class Meta:
        description = "Deletes a customer."
        model = models.Settore
        permissions = (AccountPermissions.MANAGE_STAFF,)
        error_type_class = StaffError
        error_type_field = "staff_errors"

class FerieRichiedi(ModelMutation):
    class Arguments:
        input = RichiediFerieInput(
            description="Fields required to create a richiesta ferie.", required=True
        )
    class Meta:
        description = "Creates a new ferie."
        permissions = ()
        error_type_class = StaffError
        error_type_field = "staff_errors"
        model = models.Ferie
    @classmethod
    def clean_input(cls, info, instance, data):
        requester = info.context.user
        if requester:
            user = models_account.UserExtra.objects.userExtrafromUser(requester)
            if user and user.is_staff:
                cleaned_input = super().clean_input(info, instance, data)
                cleaned_input["utente"] = user.id
                return cleaned_input
            raise PermissionDenied("il richiedente deve fare parte dello staff")
        raise PermissionDenied()
    @classmethod
    def perform_mutation(cls, root, info, **data):
        user_id = data["utente"]
        user = cls.get_node_or_error(info, user_id, field="id", only_type=type_account.UserExtra)
        response = super().perform_mutation(root, info, **data)
        if not response.errors:
            user.ferie.add(response.ferie)
            response.user = user
        return response

class FerieConferma(ModelMutation):
    class Arguments:
        id = graphene.ID(description="ID of a ferie to update.", required=True)
        input = FerieConfermaInput(
            description="Fields required to update a ferie.", required=True
        )
    class Meta:
        description = "Updates an existing ferie"
        permissions = (AccountPermissions.MANAGE_STAFF,)
        error_type_class = StaffError
        error_type_field = "staff_errors"
        model = models.Ferie
    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = super().clean_input(info, instance, data)
        cleaned_input["approvate"] = True
        return cleaned_input

class FerieCrea(ModelMutation):
    class Arguments:
        input = FerieInput(
            description="Fields required to create a ferie.", required=True
        )
    class Meta:
        description = "Creates a new ferie."
        permissions = ()
        error_type_class = StaffError
        error_type_field = "staff_errors"
        model = models.Ferie
    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = super().clean_input(info, instance, data)
        user = models_account.UserExtra.objects.filter(email=cleaned_input[USER_FIELD]).first()
        if user and user.is_staff:
            return cleaned_input
        raise PermissionDenied("il richiedente deve fare parte dello staff")
    # @classmethod
    # def perform_mutation(cls, root, info, **data):
    #     user_id = data[USER_FIELD]
    #     user = cls.get_node_or_error(info, user_id, field="id", only_type=type_account.UserExtra)
    #     response = super().perform_mutation(root, info, **data)
    #     if not response.errors:
    #         user.ferie.add(response.ferie)
    #         response.user = user
    #     return response

class FerieAggiorna(ModelMutation):
    class Arguments:
        id = graphene.ID(description="ID of a ferie to update.", required=True)
        input = FerieInput(
            description="Fields required to update a ferie.", required=True
        )
    class Meta:
        description = "Updates an existing ferie"
        permissions = (AccountPermissions.MANAGE_STAFF,)
        error_type_class = StaffError
        error_type_field = "staff_errors"
        model = models.Ferie


class FerieElimina(ModelDeleteMutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a ferie to delete.")
    class Meta:
        description = "Deletes a ferie."
        model = models.Ferie
        permissions = (AccountPermissions.MANAGE_STAFF,)
        error_type_class = StaffError
        error_type_field = "staff_errors"

class NotificaCrea(ModelMutation):
    class Arguments:
        input = NotificaCreaInput(
            description="Fields required to create a notifica.", required=True
        )
    class Meta:
        description = "Creates a new notifica."
        permissions = ()
        error_type_class = StaffError
        error_type_field = "staff_errors"
        model = models.Notifica
    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = super().clean_input(info, instance, data)
        user = cleaned_input["mittente"]
        if user and user.is_staff:
            return cleaned_input
        raise PermissionDenied("il richiedente deve fare parte dello staff")
    # @classmethod
    # def perform_mutation(cls, root, info, **data):
    #     user_id = data[USER_FIELD]
    #     user = cls.get_node_or_error(info, user_id, field="id", only_type=type_account.UserExtra)
    #     response = super().perform_mutation(root, info, **data)
    #     if not response.errors:
    #         user.ferie.add(response.ferie)
    #         response.user = user
    #     return response

class NotificaAggiorna(ModelMutation):
    class Arguments:
        id = graphene.ID(description="ID of a notifica to update.", required=True)
        input = NotificaInput(
            description="Fields required to update a notifica.", required=True
        )
    class Meta:
        description = "Updates an existing ferie"
        permissions = (AccountPermissions.MANAGE_STAFF,)
        error_type_class = StaffError
        error_type_field = "staff_errors"
        model = models.Notifica
class NotificaConferma(ModelMutation):
    class Arguments:
        id = graphene.ID(description="ID of a notifica to update.", required=True)
    class Meta:
        description = "Updates an existing ferie"
        permissions = (AccountPermissions.MANAGE_STAFF,)
        error_type_class = StaffError
        error_type_field = "staff_errors"
        model = models.Notifica
    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = super().clean_input(info, instance, data)
        cleaned_input["completata"] = True
        return cleaned_input

class NotificaElimina(ModelDeleteMutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a notifica to delete.")
    class Meta:
        description = "Deletes a notifica."
        model = models.Notifica
        permissions = (AccountPermissions.MANAGE_STAFF,)
        error_type_class = StaffError
        error_type_field = "staff_errors"
