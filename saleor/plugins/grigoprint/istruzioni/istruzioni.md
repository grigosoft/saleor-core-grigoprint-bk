# h1 
## h2

codice inline `codice`

``` py
codice
```

# installazione saleor CORE
todo

# Uso git
## init git
git init
git config --global user.email "grig.griganto@gmail.com"
git config --global user.user "grigoprint"
git branch -M master
## uso git
git add .
git commit -a -m "init"
git push origin NOME_BRANCH

per creare branch e spostarsi li `git checkout -b nome`

selezione branch di lavoro `git checkout nome`

merge dopo push completo del brench di lavoro
git checkout master
git merge NOME-BRANCH-LAVORO

# Uso saleor
creazione env `python3 -m venv myvenv` ( fuori dalla cartella di lavoro saleor)
attivazione env `source myvenv/bin/activate` ( fuori dalla cartella di lavoro saleor)
installazione dipendenze `pip install -r requirements.txt`
migrate DB `python manage.py migrate`
run server `python manage.py runserver 0.0.0.0:8000`

# test saleor
install py_dev for install dependencies on venv `sudo dnf install python-devel`
install dependencies for test all saleor `python -m pip install -r requirements_dev.txt`
run test on grigoprint plugins `pytest saleor/plugins/grigoprint`
run test on all saleor `py.test`



## idea di base
### necessità
serve una gestione per i prodotti personalizzati
extra info per l'utente
### soluzione
aggiungo le informazioni alle linee di checout e ordine, cosi da avere delle personalizzazioni uniche legate al prodotto comprato
Estendo classi base e poi le richiamo tramite GraphQL:
Model: | Products --> PrdottoGrigo 
GraphQL: | gql.saleor.products(model.Product) ---> gql.grigo.products(model.PrdottoGrigo)


# Installazione Plugin Grigoprint
### plugin da aggingere a saleor


la prima volta che si compila un app bisogna forzare il nome dell'app per fargli creare la cartella

# librerie da installare

pip install fdb
sudo dnf install libfbclient2
