import psycopg2
import random
import string

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

# Funktion zum Generieren eines zufälligen Passworts
def generate_password():
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(10))

# Funktion zum Erstellen eines Benutzers und einer Tabelle für einen Studenten
def create_user_and_table(connection, student_id):
    try:
        cursor = connection.cursor()
        
        # Zufälliges Passwort generieren
        password = generate_password()
        print(f"{student_id}:{password}")
        
        # Benutzer anlegen
        cursor.execute("CREATE ROLE student{} WITH LOGIN PASSWORD %s".format(student_id), (password,))
        
        # Tabelle für den Studenten erstellen
        cursor.execute("CREATE TABLE student{}_table (id SERIAL PRIMARY KEY, data TEXT)".format(student_id))
        
        # Berechtigungen setzen, damit der Student nur auf seine Tabelle zugreifen kann
        cursor.execute("GRANT ALL PRIVILEGES ON TABLE student{}_table TO student{}".format(student_id, student_id))
        
        # Verbindung bestätigen und Änderungen speichern
        connection.commit()
        
        print("Benutzer für Student {} erfolgreich erstellt.".format(student_id))
        
    except (Exception, psycopg2.Error) as error:
        print("Fehler beim Erstellen von Benutzer und Tabelle für Student {}: ".format(student_id), error)

# Liste der Matrikelnummern
matrikelnummern = [1001, 1002, 1003, 1004]  # Beispielwerte, ersetzen Sie diese durch Ihre eigene Liste

# PostgreSQL-Verbindung herstellen
connection = connect_to_postgres()

if connection:
    # Benutzer und Tabelle für jeden Studenten erstellen
    for student_id in matrikelnummern:
        create_user_and_table(connection, student_id)
        
    # Verbindung zur PostgreSQL-Datenbank schließen
    connection.close()
else:
    print("Fehler beim Herstellen der Verbindung zur PostgreSQL-Datenbank.")
