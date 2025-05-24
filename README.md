# Projekt-Software-Development: "Mein-WG-Putzplan" (kurz: MWGP)
Repository für die Entwicklung der responsiven Web-Anwendung "Mein-WG-Putzplan" (kurz: "MWGP") mithilfe von Django, Python, HTML, CSS und JavaScript als Prüfungsleistung für den Kurs "Projekt: Software Development", (DLBSEPPSD01_D). Das Projekt wurde vom ehemaligen Tutor Herrn Prof. Dr. Christian Remfert am 03.03.2025 freigegeben.

- **Studierender**: Iosif Gogolos
- **Matrikelnummer**: 42304582
- **Studiengang**: Softwareentwicklung, B.Sc.

## Tech-Stack

- **Backend**: Django (Python)
- **Datenbank**: SQLite
- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Version Control**: Git/GitHub
- **Hosting**: Render
- **Virtuelle Umgebung**: Python venv

## Technische Voraussetzungen

- Python 3.8 oder höher
- Git
- Internetverbindung für Bootstrap CDN

## Lokale Installation

### 1. Terminal/Kommandozeile starten

#### Windows:
- **Eingabeaufforderung**: `Win + R` → `cmd` → Enter
- **Altenativ: PowerShell**: `Win + X` → Windows PowerShell

#### macOS:
- **Terminal**: `Cmd + Space` → "Terminal" → Enter

#### Linux:
- **Terminal**: `Ctrl + Alt + T`
- **Oder**: Über Anwendungsmenü → Terminal

#### Betriebssystem-unabhängig, in der integrierten Entwicklungsumgebung (IDE) "Microsoft Visual Studio Code:
- ** Microsoft Visual Studio Code öffnen**
- **In"Visual Studio Code"**: Im Menü "Terminal -> New Terminal"


### 2. Repository klonen

```bash
git clone https://github.com/iosif-gogolos/MWGP-42304582.git
cd MWGP-42304582
```



### 3. Virtual Environment initialisieren

#### Windows:
```bash
# Virtual Environment erstellen
python -m venv venv

# Virtual Environment aktivieren
venv\Scripts\activate

# Abhängigkeiten installieren
pip install -r requirements.txt

# Datenbank migrieren
python manage.py migrate

# Dummy-Daten laden
python manage.py loaddata initial_data.json

# Development Server starten
python manage.py runserver
```

#### macOS/Linux:
```bash
# Virtual Environment erstellen
python3 -m venv venv

# Virtual Environment aktivieren
source venv/bin/activate

# Abhängigkeiten installieren
pip install -r requirements.txt

# Datenbank migrieren
python manage.py migrate

# Dummy-Daten laden
python manage.py loaddata initial_data.json

# Development Server starten
python manage.py runserver
```

### 4. Admin-Anmeldung

Öffnen Sie Ihren Browser und navigieren Sie zu: `http://127.0.0.1:8000`

**Admin-Login Daten:**
- **Benutzername**: `iu-admin@mwgp.de`
- **Passwort**: `iu-admin-12345`
- **Email**: iosif.gogolos@iu-study.org (dient dazu das Passwort zurückzusetzen)

### 5. Browser-Test

1. Öffnen Sie `http://127.0.0.1:8000` in Ihrem Browser
2. Loggen Sie sich mit den Admin-Daten ein
3. Sie sollten eine **Willkommensnachricht** in einem Modal sehen
4. Das Modal informiert über die Dummy-Daten und fragt nach dem ersten echten Mitbewohner

## Dummy-Daten

Die Anwendung wird mit folgenden Test-Mitbewohnern geladen:

- **Max Mustermitbewohner** (max.mustermann@example.com)
- **Lisa Mustermitbewohnerin** (lisa.mustermann@example.com)

### Zur Überprüfung und zum bewerten
- Benutzername: iu-admin@mwgp.de
- Passwort: iu-admin-12345

## Kalender-Funktionalität

### Putzplan-Rotation
- **Stichtag**: Jeden Sonntag
- **Rotation**: Thorsten → Lisa → Max → (neuer Mitbewohner)
- **Neue Mitbewohner**: Werden ab dem nächsten verfügbaren Sonntag eingeplant

### Kalender-Status
- **Upcoming** (Grün): Kommender Putztag
- **Done** (Grau): Zwei vorherige Sonntage
- **Future** (Blau): Zwei zukünftige Putztage

## Mitbewohner hinzufügen

1. Als Admin anmelden
2. **"Neuen Mitbewohner hinzufügen"** auswählen
3. Formular ausfüllen (`create-user.html`)
4. **Automatische Passwort-Generierung** erfolgt
5. **E-Mail mit Login-Daten** wird versendet
6. Neuer Mitbewohner wird ab nächstem verfügbaren Sonntag eingeplant

## Entwicklung

### Virtual Environment deaktivieren
```bash
deactivate
```

### Neue Abhängigkeiten hinzufügen
```bash
pip install paket-name
pip freeze > requirements.txt
```

### Datenbank zurücksetzen
```bash
# Windows
del db.sqlite3
python manage.py migrate
python manage.py loaddata initial_data.json

# macOS/Linux
rm db.sqlite3
python manage.py migrate
python manage.py loaddata initial_data.json
```

## Deployment auf Render

1. Repository auf GitHub pushen
2. Render-Account erstellen
3. Neuen Web Service verbinden
4. Environment-Variablen setzen:
   - `DJANGO_SETTINGS_MODULE=mwgp.settings.production`
   - `SECRET_KEY=[IHR-GEHEIMER-SCHLÜSSEL]`
   - `DEBUG=False`

## Fehlerbehebung

### Port bereits in Verwendung
```bash
# Anderen Port verwenden
python manage.py runserver 8001
```

### Virtual Environment Probleme
```bash
# Virtual Environment löschen und neu erstellen
# Windows
rmdir /s venv
# macOS/Linux
rm -rf venv

# Neu erstellen (siehe Schritt 3)
```

### Migration Fehler
```bash
python manage.py makemigrations
python manage.py migrate
```

## Browser-Kompatibilität
Das Projekt sollte mit allen modernen/ gängigen Web-Browsern kompatibel sein, z.B.:
- Chrome 
- Firefox 
- Safari 
- Microsoft Edge 

## Support

Bei Problemen:
1. Überprüfen Sie die Konsolen-Ausgabe auf Fehlermeldungen
2. Stellen Sie sicher, dass alle Abhängigkeiten installiert sind
3. Prüfen Sie, ob das Virtual Environment aktiviert ist
4. Kontaktieren Sie mich gerne per Email: iosif.gogolos@iu-study.org

## Lizenz

MIT License - siehe LICENSE-Datei für Details.

---

**Happy Cleaning! 🧹✨**
