import fdb

HOST = "192.168.50.150"
PORT = 31976
FILE = "C:\\Users\\Ombrellificio\\Docuemnts\\Danea Easyfatt\\Archivi\\Ombrellificio.etf"


TABELLA_ANAGRAFICA = '"TAnagrafica"'
COLONNE_ANAGRAFICA = [
                    '"Nome"',
                    '"email"',
                    '""',
                    '""',
                    '""',
                    '""',
                    '""',
                    '""',
                    '""',
                    '""',
                    '""',
                    '""',
                    '""',
                    '""',
                    '""',
                    '""',
                    '""',
                    '""',
                    ]

QUERY_ANAGRAFICA = "SELECT %s FROM %s"


def import_anagrafica(id = None):
    print(id)
    query = QUERY_ANAGRAFICA.format('"Nome"',TABELLA_ANAGRAFICA)
    connessione = fdb.connect(host=HOST, database=FILE, port=PORT, user="SYSDBA", password="masterkey", )

    cursor = connessione.cursor()
    cursor.execute(query)
    row = cursor.fetchone()
    print(row)
    #while row:
    #    print(row)
    #    print(row["Nome"])
    #    row = cursor.fatchone()


