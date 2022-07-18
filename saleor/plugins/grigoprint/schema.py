# richiamare in saleor.graphql.api


from .accountGrigo.graphql.mutation import ClienteCrea, ClienteAggiorna, IndirizzoAggiorna, IndirizzoCrea, LoadDataFromDanea, StaffAggiorna, StaffCrea, ContattoCrea, ContattoAggiorna
from .accountGrigo.graphql.schema import AccountQueries
# from .prima_configurazione_saleor import PrimaConfigurazioneSaleor
class GrigoprintQueries(
    AccountQueries
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
    load_data_from_danea = LoadDataFromDanea.Field()
