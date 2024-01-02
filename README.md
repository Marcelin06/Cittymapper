# Cittymapper
Data base project

Le rapport "rapport_city_mapper.pdf" decrit le contexte

### Comment lancer le programme ###
Pour lancer le programme python "CityMapper.py", il faut configurer d'abord votre environnement de developpement et modifier le script python a la ligne 210 
self.conn = psycopg2.connect(database="name_of_your_data_base", user="your_user_name", host="local_host", password="your_password")


### Comment creer les tables dans la base de donnees et les remplir  ###
Il y a 2 principales: Toulouse et Paris

Aller dans le fichier "Data for Pris"
Creer les tables pour Paris avec le fichier "mytables_p.sql"; commande "\i mytables_p.sql"
Remplir les tables avec tous fichiers "*data.sql"; commande "\i *data.sql"

Aller dans le fichier "Data for Toulouse"
Creer les tables pour Toulouse avec les 3 fichiers "routes_toulouse.sql" "network_nodes.sql" "mytables.sql"; pour les commandes, c'est la meme syntaxe
Remplir les tables avec tous fichiers "*data.sql"; commande "\i *data.sql"

Utiliser la commande "\d" pour verifier si les tables sont bien preentes

### How to install PostgreSQL on Ubuntu/Debian ... ###
1. install postgreSQL: 

       sudo apt install postgresql postgresql-contrib

When you install postgreSQL, it automatically creates a new LINUX user account called "postgres". 




2. create a new postgreSQL user called "mynamehere" (pick your own user name here) by running the postgreSQL command "createuser" as the LINUX user "postgres": 

       sudo -u postgres createuser -P -s -e mynamehere




3. Create a new postgreSQL database called "mynewdb" (pick your own database name here): 

       sudo -u postgres createdb mynewdb




4. Connect to postgreSQL with postgreSQL user "mynamehere" and postgreSQL database "mynewdb":


       psql -U mynamehere -h localhost -d mynewdb 


It is useful to remember the key parameters:

postgreSQL username ("mynamehere" in the above example)
postgreSQL databasename ("mynewdb" in the above example)
postgreSQL port ("localhost" by default)




#### Install Python modules on UBUNTU: ###
---------------------------------
# we suppose that you already have python3
1. For installing "psycopg2" to access psql from Python3: 

      sudo apt install libpq-dev
      sudo apt install python3-pip
      sudo apt install python3-psycopg2


2. For installing "Qt5" to access GUI from Python3:

      sudo apt install python3-qtpy


3. Packages to get maps working in Python3: 

      sudo apt install python3-folium



### Some PostgreSQL commands ###
Within psql, here is a list of useful commands:

Read commands from an external file: 
   \i abc.sql 
To quit:
   \q
To change database: 
   \c nameofdatabasetochangeto
List of tables:
   \d (or \d+)
Information on a table:
   \d nameoftable (or \d+ nameoftable)
List of databases acessible:
   \l 
To delete a table:
   DROP tablename;
