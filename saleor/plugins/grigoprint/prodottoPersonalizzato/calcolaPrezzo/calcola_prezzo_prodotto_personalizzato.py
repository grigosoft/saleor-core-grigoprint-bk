

from .. import models

def calcola_prezzo_prodotto_personalizzato(personalizzazione:models.Personalizzazione):
    slug = personalizzazione.prodotto.slug
    # match slug:
    #     case "bandiera-personalizzata":
    #         return calcola_prezzo_prodotto_bandiera_personalizzata(personalizzazione)
    #     case _:
    #         raise Exception(message="Prodotto '%s' non riconosciuto tra quelli disponibili nel calcola prezzo".format(slug))

def calcola_prezzo_prodotto_bandiera_personalizzata(personalizzazione:models.Personalizzazione):
    "ciao"