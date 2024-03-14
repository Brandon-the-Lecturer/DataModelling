import argparse
import random

import numpy as np
import psycopg2
from faker import Faker

PATH = "student_ids.txt"

fake = Faker()
random.seed(3)

# Einlesen einer txt-Datei als Liste
def read_txt_to_list(txt_file):
    with open(txt_file, 'r') as file:
        data = [line.split()[0] for line in file.readlines()]
        data = [int(f"{random.randint(10,80)}{no}") for no in data]
    return data

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
    return f"{fake.word()}-{fake.word()}-{fake.word()}"

def save_credentials_to_file(student_id, password):
    with open("credentials.txt", "a") as file:
        file.write(f"{student_id}, {password}\n")

def remove_credentials_from_file(student_id):
    # Liste zum Speichern der verbleibenden Zeilen
    remaining_lines = []
    with open("credentials.txt", "r") as file:
        for line in file:
            # Überprüfen, ob die Zeile die Anmeldeinformationen für den aktuellen Studenten enthält
            if not line.startswith(f"{student_id}, "):
                remaining_lines.append(line)
    
    # Schreiben der verbleibenden Zeilen in die Datei, um die Anmeldeinformationen zu aktualisieren
    with open("credentials.txt", "w") as file:
        for line in remaining_lines:
            file.write(line)

# Funktion zum Erstellen eines Benutzers und einer Tabelle für einen Studenten
def create_user_and_table(connection, student_id):
    try:
        cursor = connection.cursor()
        
        # Zufälliges Passwort generieren
        password = generate_password()
    
        # Benutzer anlegen
        cursor.execute("CREATE ROLE student{} WITH LOGIN PASSWORD %s".format(student_id), (password,))
        
        # Tabelle für den Studenten erstellen
        cursor.execute("CREATE TABLE student{}_table (id SERIAL PRIMARY KEY, longitude FLOAT, latitude FLOAT, score FLOAT)".format(student_id))

        # Einträge erstellen
        num_entries = int(student_id)
        for i in range(num_entries):
            # Zufällige longitude und latitude wählen
            longitude = random.uniform(-180, 180)
            latitude = random.uniform(-90, 90)
            # Score aus Normalverteilung generieren
            mean = num_entries
            std = 0.01 * num_entries
            score = int(np.random.normal(mean, std))
            
            # Eintrag in die Tabelle einfügen
            cursor.execute("INSERT INTO student{}_table (longitude, latitude, score) VALUES (%s, %s, %s)".format(student_id), (longitude, latitude, score))

        print(f"In Tabelle 'student{student_id}_table' wurden {num_entries} erfolreich Einträge gemacht.")
        # Berechtigungen setzen, damit der Student nur auf seine Tabelle zugreifen kann
        cursor.execute("GRANT ALL PRIVILEGES ON TABLE student{}_table TO student{}".format(student_id, student_id))
        
        # Verbindung bestätigen und Änderungen speichern
        connection.commit()
        
        # Anmeldeinformationen in die Datei speichern
        save_credentials_to_file(student_id, password)
        
        print("Benutzer für Student {} erfolgreich erstellt.".format(student_id))
        
    except (Exception, psycopg2.Error) as error:
        print("Fehler beim Erstellen von Benutzer und Tabelle für Student {}: ".format(student_id), error)

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

        # Anmeldeinformationen aus der Datei entfernen
        remove_credentials_from_file(student_id)
        
        print("Benutzer und Tabelle für Student {} erfolgreich gelöscht.".format(student_id))
        
    except (Exception, psycopg2.Error) as error:
        print("Fehler beim Löschen von Benutzer und Tabelle für Student {}: ".format(student_id), error)

# CLI-Parser erstellen
def create_cli_parser():
    parser = argparse.ArgumentParser(description="CLI-Tool zum Erstellen und Löschen einer Tabelle mit Einträgen")
    parser.add_argument("--build", action="store_true", help="Erstellt die Tabelle mit Einträgen")
    parser.add_argument("--tear_down", action="store_true", help="Löscht die Tabelle")
    return parser

# Hauptfunktion
def main():
    # CLI-Parser erstellen
    parser = create_cli_parser()
    args = parser.parse_args()

    try:
        student_ids = read_txt_to_list(PATH)
    
    except TypeError:
        print("No file with student ids.")
        exit()
    
    # PostgreSQL-Verbindung herstellen
    connection = connect_to_postgres()

    if connection:
        if args.build:
                # Tabelle mit Einträgen erstellen
                for student_id in student_ids:
                    create_user_and_table(connection, student_id)
                # Verbindung zur PostgreSQL-Datenbank schließen
                connection.close()
        elif args.tear_down:
                # Tabelle löschen
                for student_id in student_ids:
                    drop_user_and_table(connection, student_id)
                # Verbindung zur PostgreSQL-Datenbank schließen
                connection.close()
        else:
            print("Bitte geben Sie entweder --build oder --tear_down an.")
    else:
        print("Fehler beim Herstellen der Verbindung zur PostgreSQL-Datenbank.")

if __name__ == "__main__":
    main()
