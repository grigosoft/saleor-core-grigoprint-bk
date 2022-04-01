
from django.db import IntegrityError
import fdb

from ....account.models import Address

from .models import UserGrigo


HOST = "192.168.50.150"
PORT = 31976
FILE = "C:\\Users\\Ombrellificio\\Documents\\easyfat\\Archivi\\Ombrellificio.eft"


TABELLA_ANAGRAFICA = '"TAnagrafica"'
COLONNE_ANAGRAFICA = [
                    '"Cliente"',
                    '"CodAnagr"',
                    '"CodiceFiscale"',
                    '"PartitaIva"',
                    '"Nome"',
                    '"Tel"',
                    '"Cell"',
                    '"Fax"',
                    '"CodIvaDefault"',
                    '"Email"',
                    '"Pec"',
                    '"PagamentoDefault"',
                    '"CoordBancarieDefault"',
                    '"AgenteDefault"',
                    '"PortoDefault"',
                    '"VettoreDefault"',
                    '"Extra1"',
                    '"Extra2"',
                    '"FE_RifAmmin"',
                    '"FE_CodUfficio"',
                    '"Nazione"',
                    '"Indirizzo"',
                    '"Cap"',
                    '"Prov"',
                    '"Citta"',
                    ]

QUERY_ANAGRAFICA = "SELECT {0} FROM {1} where "+COLONNE_ANAGRAFICA[1]+" <> '0132'"# salto la metro che sbrocca


def import_anagrafica(id = None):
    #query = "SELECT rdb$field_name FROM rdb$relation_fields WHERE rdb$relation_name='TAnagrafica'"
    query = QUERY_ANAGRAFICA.format(','.join(COLONNE_ANAGRAFICA),TABELLA_ANAGRAFICA)
    # try:
    connessione = fdb.connect(host=HOST, database=FILE, port=PORT, user="SYSDBA", password="masterkey", )

    cursor = connessione.cursor()
    cursor.execute(query)
    # print(cursor.description)
    row = cursor.fetchone()
    n_errori = 0
    n_inserimenti = 0
    while row and n_errori < 1000:
        try:
            # print(row[4], " ",row[9], " --> ", row[0])
            n_inserimenti += save_user(row)
            row = cursor.fetchone()
        except UnicodeDecodeError as err:
            n_errori += 1
            print("errore danea encoding: ", err)
        except IntegrityError as err:
            print("\terrore email: "+row[9]+" db: ", err)
            row = cursor.fetchone() # passo al prossimo
    # except:
    #     print()
    print("inserimenti: ",n_inserimenti)
    print("errori encoding: ",n_errori)
    connessione.close()

def save_user(row):
    '''
    Salva l'utente a datatabase ricevendo in ingresso i dati da DANEA
    prima di creare un nuovo utente controlla:
    solo se cliente
    se c'è gia un id-danea e aggiorna i dati
    se c'è gia un codice fiscale o piva e aggiorna i dati
    se utente nuovo crea l'utente
    '''
    if row[0] == 0: # se cliente
        return 0
    id_danea = row[1]
    cf = row[2]
    piva = row[3]
    email = row[9]
    if not email or email == "":
        print("cliente senza email: ",row[4])
        return 0

    # aggiornamento per email da fare per primo, in quanto nell'eccomerce la mail è legge
    usr = UserGrigo.objects.filter(email=email).first()
    if usr:
        # print("aggiorna tramite email: ", row[4])
        usr.id_danea = id_danea
        usr.cf = cf
        usr.piva = piva
        inserisci_dati_user(usr, row)
        usr.save()
        return 1

    usr = UserGrigo.objects.filter(id_danea=id_danea).first()
    if usr:
        # print("aggiorna tramite id_danea ", row[4])
        usr.cf = cf
        usr.piva = piva
        usr.email = email
        inserisci_dati_user(usr, row)
        usr.save()
        return 1
    
    usr = UserGrigo.objects.filter(cf=cf).first()
    if usr:
        usr = UserGrigo.objects.filter(cf=cf).first()
        # print("aggiorna tramite cf ", row[4])
        usr.id_danea = id_danea
        usr.piva = piva
        usr.email = email
        inserisci_dati_user(usr, row)
        usr.save()
        return 1
    
    usr = UserGrigo.objects.filter(piva=piva).first()
    if usr:
        # print("aggiorna tramite piva ", row[4])
        usr.id_danea = id_danea
        usr.cf = cf
        usr.email = email
        inserisci_dati_user(usr, row)
        usr.save()
        return 1

        
    crea_user(row)
    return 1

def inserisci_dati_user(usr, row):
    # usr.id_danea = row[1], #'"CodAnagr"',
    # usr.cf = row[2], #'"CodiceFiscale"',
    # usr.piva = row[3], #'"PartitaIva"',
    usr.denominazione = row[4] #'"Nome"',
    
    if row[5]:
        usr.tel = row[5] #'"Tel"',
    else:
        usr.tel = ""
    
    if row[6]:
        usr.cell = row[6] #'"Cell"',
    else:
        usr.cell = ""
        
        #  = row[7], #'"Fax"',
    usr.iva = row[8] #'"CodIvaDefault"',
    # usr.email = row[9] #'"Email"',
    usr.pec = row[10] #'"Pec"',
    usr.pagamento = row[11] #'"PagamentoDefault"',
    usr.coordinate_bancarie = row[12] #'"CoordBancarieDefault"',
        #  = row[13], #'"AgenteDefault"',
    usr.porto = row[14] #'"PortoDefault"',
    usr.vettore = row[15] #'"VettoreDefault"',
        #  = row[16], #'"Extra1"',
    usr.listino = row[17] #'"Extra2"',
    usr.rif_ammin = row[18] #'"FE_RifAmmin"',
    usr.sdi = row[19] #'"FE_CodUfficio"',

    # if row[21]: # se è compliata la via do per scontato ci sia l'indirizzo
    #     fatturazione = Address.objects.create(
    #         CountryCode = row[20], #'"Nazione"',
    #         street_address1 = row[21], #'"Indirizzo"',
    #         postal_code = row[22], #'"Cap"',
    #         city_area = row[23], #'"Prov"',
    #         city = row[24], #'"Citta"',
    #         is_default_billing_address = True
    #     )
    #     usr.default_billing_address = fatturazione

def crea_user(row):
    print("crea: ", row[4])
    nazione = row[16]
    if not nazione:
        nazione = "Italia"
    
    usr = UserGrigo.objects.create(
        id_danea = row[1],
        cf = row[2],
        piva = row[3],
        email = row[9]
    )
    inserisci_dati_user(usr, row)
    usr.save()