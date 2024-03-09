# Grundlagen der Datenmodellierung - Praktische Vorlesungsbegleitung

Dieses Repository enthält Skripte und Anleitungen zur praktischen Vorlesungsbegleitung im Fach "Grundlagen der Datenmodellierung". Das Ziel dieser Vorlesungsbegleitung ist es, den Studierenden praktische Erfahrungen mit der Datenmodellierung und Datenbankmanagementsystemen zu vermitteln. Es gibt insgesamt 9 Vorlesungen, für jede Vorlesung werden ein Setup- und ein Tear-Down-Skript bereitgestellt.

## Architektur

Die Architektur besteht aus einer EC2-Instanz auf AWS, auf der ein PostgreSQL-Docker-Container ausgeführt wird.

### Docker

Nach der Initialisierung soll der Docker-Container nur gestoppt werden. Folgende Befehle werden verwendet:

- **Initialisieren**

        docker run --name postgres-container -e POSTGRES_PASSWORD=<PASSWORD> -d -p <AWS-PORT>:5432 postgres

- **Starten**: 

        docker container start postgres-container

- **Stoppen**:  

        docker container stop postgres-container`

# Aufgaben

### Session 1

- **Thema**: Einführung in SQL und grundlegende SELECT-Abfragen
- **Aufgaben**:
  - Erstellen Sie eine SELECT-Abfrage, um Daten aus einer Tabelle abzurufen: `SELECT .... FROM ....`
  - Verwenden Sie Funktionen wie MAX, MIN, COUNT, AVG in SELECT-Abfragen
  - Verwenden Sie das AS-Schlüsselwort, um Spalten in den Ergebnissen umzubenennen, z.B. "Max Score", "Min Score", "Avg Score", "Number of Scores"

---

Für jede weitere Vorlesung werden ähnliche Informationen bereitgestellt, einschließlich des Themas, der zugehörigen Aufgaben und gegebenenfalls zusätzlicher Anleitungen oder Ressourcen.

**Hinweis:** Bitte stellen Sie sicher, dass Sie vor der Verwendung der Skripte und Anleitungen die entsprechenden Anmeldeinformationen, Portnummern und andere Konfigurationen an Ihre spezifische Umgebung anpassen.

---

Dieses ReadMe-Dokument bietet eine kurze Übersicht über das Repository und die darin enthaltenen Ressourcen. Bitte lesen Sie die einzelnen Skripte und Anleitungen für detaillierte Anweisungen und Hinweise.

Bei Fragen oder Problemen wenden Sie sich bitte an den verantwortlichen Dozenten.

Viel Erfolg bei Ihrer praktischen Arbeit im Fach "Grundlagen der Datenmodellierung"!