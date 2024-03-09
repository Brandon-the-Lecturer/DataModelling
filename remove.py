import psycopg2

# Verbindung zur PostgreSQL-Datenbank herstellen
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

# Funktion zum Löschen eines Benutzers und einer Tabelle für einen Studenten
def drop_user_and_table(connection, student_id):
    try:
        cursor = connection.cursor()
        
        # Tabelle löschen
        cursor.execute("DROP TABLE IF EXISTS student{}_table".format(student_id))
        
        # Benutzer löschen
        cursor.execute("DROP ROLE IF EXISTS student{}".format(student_id))
        
        # Verbindung bestätigen und Änderungen speichern
        connection.commit()
        
        print("Benutzer und Tabelle für Student {} erfolgreich gelöscht.".format(student_id))
        
    except (Exception, psycopg2.Error) as error:
        print("Fehler beim Löschen von Benutzer und Tabelle für Student {}: ".format(student_id), error)

# Liste der Matrikelnummern
matrikelnummern = [1001, 1002, 1003, 1004]  # Beispielwerte, ersetzen Sie diese durch Ihre eigene Liste

# PostgreSQL-Verbindung herstellen
connection = connect_to_postgres()

if connection:
    # Benutzer und Tabelle für jeden Studenten löschen
    for student_id in matrikelnummern:
        drop_user_and_table(connection, student_id)
        
    # Verbindung zur PostgreSQL-Datenbank schließen
    connection.close()
else:
    print("Fehler beim Herstellen der Verbindung zur PostgreSQL-Datenbank.")
