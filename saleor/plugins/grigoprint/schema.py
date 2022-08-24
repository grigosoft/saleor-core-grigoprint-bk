# richiamare in saleor.graphql.api


from .prodottoPersonalizzato.graphql.schema import ProdottoPersonalizzatoQueries
from .accountGrigo.graphql.mutation import ClienteCrea, ClienteAggiorna, AgisciSuUtenti, IndirizzoAggiorna, IndirizzoCrea, LoadDataFromDanea, StaffAggiorna, StaffCrea, ContattoCrea, ContattoAggiorna
from .accountGrigo.graphql.schema import AccountQueries
from .gestioneAzienda.graphql.mutation import FerieAggiorna, FerieConferma, FerieCrea, FerieElimina, FerieRichiedi, NotificaAggiorna, NotificaConferma, NotificaCrea, NotificaElimina, SettoreCrea, SettoreAggiorna, SettoreElimina
from .gestioneAzienda.graphql.schema import GestioneAziendaQueries
# from .prima_configurazione_saleor import PrimaConfigurazioneSaleor
class GrigoprintQueries(
    AccountQueries,
    GestioneAziendaQueries,
    ProdottoPersonalizzatoQueries
):
    pass


class GrigoprintMutations():
    # prima_configurazione_saleor = PrimaConfigurazioneSaleor.Field()
    cliente_crea = ClienteCrea.Field()
    cliente_aggiorna = ClienteAggiorna.Field()
    staff_crea = StaffCrea.Field()
    staff_aggiorna = StaffAggiorna.Field()
    contatto_crea = ContattoCrea.Field()
    contatto_aggiorna = ContattoAggiorna.Field()
    indirizzo_crea = IndirizzoCrea.Field()
    indirizzo_aggiorna = IndirizzoAggiorna.Field()
    zz_load_data_from_danea = LoadDataFromDanea.Field()
    zz_agisci_su_utenti = AgisciSuUtenti.Field()

    settore_crea = SettoreCrea.Field()
    settore_aggiorna = SettoreAggiorna.Field()
    settore_elimina = SettoreElimina.Field()
    ferie_richiedi = FerieRichiedi.Field()
    ferie_conferma = FerieConferma.Field()
    ferie_crea = FerieCrea.Field()
    ferie_aggiorna = FerieAggiorna.Field()
    ferie_elimina = FerieElimina.Field()
    notifica_crea = NotificaCrea.Field()
    notifica_aggiorna = NotificaAggiorna.Field()
    notifica_conferma = NotificaConferma.Field()
    notifica_elimina = NotificaElimina.Field()
