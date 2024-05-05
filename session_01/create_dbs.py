import argparse
import psycopg2

# Funktion zum Herstellen einer Verbindung zur PostgreSQL-Datenbank
def connect_to_postgres():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="mysecretpassword", # Passwort für den PostgreSQL-Benutzer
            host="localhost",
            port="5432",
            database="postgres"
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Fehler beim Verbinden zur PostgreSQL-Datenbank:", error)

# Funktion zum Erstellen einer Datenbank für einen Benutzer
def create_database_for_user(connection, username, password):
    username = "student"+username
    try:
        cursor = connection.cursor()
        
        # Datenbanknamen erstellen
        dbname = "db_" + username
        
        # Autocommit aktivieren, damit CREATE DATABASE außerhalb einer Transaktion ausgeführt wird
        connection.autocommit = True
        
        # Datenbank für den Benutzer erstellen im Schema "public"
        cursor.execute("CREATE DATABASE {} OWNER {} TEMPLATE template0 ENCODING 'UTF8' LC_COLLATE='en_US.UTF-8' LC_CTYPE='en_US.UTF-8'".format(dbname, username))
        
        # Versuchen, den Benutzer zu erstellen
        try:
            cursor.execute("CREATE USER {} WITH PASSWORD %s".format(username), (password,))
        except psycopg2.errors.DuplicateObject as e:
            print("Benutzer {} existiert bereits.".format(username))
        
        # Berechtigungen setzen
        cursor.execute("GRANT ALL PRIVILEGES ON DATABASE {} TO {}".format(dbname, username))
        
        # Verbindung bestätigen
        connection.commit()
        
        # Autocommit wieder auf False setzen
        connection.autocommit = False
        
        print("Datenbank {} für Benutzer {} erfolgreich erstellt.".format(dbname, username))
        
    except (Exception, psycopg2.Error) as error:
        print("Fehler beim Erstellen der Datenbank für Benutzer {}: ".format(username), error)
# Hauptfunktion
def main():
    # CLI-Parser erstellen
    parser = argparse.ArgumentParser(description="CLI-Tool zum Erstellen von Datenbanken für Benutzer")
    parser.add_argument("credentials_file", type=str, help="Pfad zur Datei mit den Benutzeranmeldeinformationen")
    args = parser.parse_args()

    try:
        # Anmeldeinformationen aus der Datei lesen
        with open(args.credentials_file, 'r') as file:
            credentials = [line.strip().split(", ") for line in file.readlines()]

        # PostgreSQL-Verbindung herstellen
        connection = connect_to_postgres()

        if connection:
            # Datenbanken für jeden Benutzer erstellen
            for username, password in credentials:
                create_database_for_user(connection, username, password)
            
            # Verbindung zur PostgreSQL-Datenbank schließen
            connection.close()
        else:
            print("Fehler beim Herstellen der Verbindung zur PostgreSQL-Datenbank.")
    
    except FileNotFoundError:
        print("Datei mit Benutzeranmeldeinformationen nicht gefunden.")

if __name__ == "__main__":
    main()
