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

# Funktion zum Löschen aller Datenbanken, die mit einem bestimmten Muster beginnen
def drop_databases_with_pattern(connection, pattern):
    try:
        cursor = connection.cursor()
        
        # Autocommit aktivieren, damit DROP DATABASE außerhalb einer Transaktion ausgeführt wird
        connection.autocommit = True
        
        # Alle Datenbanken abrufen
        cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
        databases = cursor.fetchall()
        
        # Datenbanken löschen, die mit dem angegebenen Muster beginnen
        for database in databases:
            if database[0].startswith(pattern):
                cursor.execute("DROP DATABASE IF EXISTS {}".format(database[0]))
        
        # Autocommit wieder auf False setzen
        connection.autocommit = False
        
        print("Alle Datenbanken mit dem Muster '{}' wurden erfolgreich gelöscht.".format(pattern))
        
    except (Exception, psycopg2.Error) as error:
        print("Fehler beim Löschen der Datenbanken:", error)

# Hauptfunktion
def main():
    # PostgreSQL-Verbindung herstellen
    connection = connect_to_postgres()

    if connection:
        # Datenbanken mit dem Muster 'db_' löschen
        drop_databases_with_pattern(connection, "db_")
        
        # Verbindung zur PostgreSQL-Datenbank schließen
        connection.close()
    else:
        print("Fehler beim Herstellen der Verbindung zur PostgreSQL-Datenbank.")

if __name__ == "__main__":
    main()
