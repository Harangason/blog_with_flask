# blog_with_flask

Ein kleiner Flask-Blog mit dateigestuetzter Datenspeicherung in JSON.

## Projektstruktur

- `app.py` - Flask-App mit Routen fuer Anzeigen, Hinzufuegen, Bearbeiten, Loeschen und Liken von Blogbeitraegen
- `templates/`
  - `index.html` - zeigt alle Blogbeitraege an
  - `add.html` - Formular fuer neue Blogbeitraege
  - `update.html` - Formular zum Bearbeiten eines bestehenden Blogbeitrags
- `dictionary/data.json` - gespeicherte Blogdaten
- `static/style.css` - Styling fuer die Seite
- `test_app.py` - Unit-Tests fuer die wichtigsten Funktionen

## Starten der App

```bash
python app.py
```

Die App laeuft standardmaessig auf:

```text
http://127.0.0.1:5000/
```

## Verfuegbare Routen

- `GET /`
  - Zeigt alle Blogbeitraege aus `dictionary/data.json` an.
- `GET /add`
  - Zeigt das Formular zum Erstellen eines neuen Beitrags.
- `POST /add`
  - Speichert einen neuen Beitrag.
- `GET /update/<post_id>`
  - Zeigt das Bearbeitungsformular fuer den Beitrag mit dieser ID.
- `POST /update/<post_id>`
  - Aktualisiert Titel, Autor und Inhalt eines Beitrags.
- `POST /delete/<post_id>`
  - Loescht den Beitrag mit dieser ID. Auch der letzte vorhandene Beitrag kann geloescht werden.
- `POST /like/<post_id>`
  - Erhoeht den Like-Zaehler eines Beitrags.
- `GET /favicon.ico`
  - Gibt `204 No Content` zurueck, wenn kein Favicon vorhanden ist.

## Wichtige Aenderungen

- Die Delete-Route verwendet jetzt `POST` statt `GET`, weil sie Daten veraendert.
- Die Like-Route verwendet jetzt ebenfalls `POST` statt `GET`.
- Das Loeschen funktioniert auch dann, wenn nur ein einziger Blogbeitrag existiert.
- Nicht verwendete Klassen wurden entfernt, damit das Projekt einfacher und uebersichtlicher bleibt.

## JSON-Format

`dictionary/data.json` enthaelt eine Liste von Blogbeitraegen:

```json
[
  {
    "id": 1,
    "author": "John Doe",
    "title": "First Post",
    "content": "This is my first post.",
    "likes": 0
  }
]
```

`id` ist der eindeutige Primaerschluessel eines Beitrags. Neue IDs werden anhand der hoechsten vorhandenen ID erzeugt.

## Tests ausfuehren

```bash
python -m unittest test_app.py
```

Die Tests pruefen unter anderem:

- Anzeigen vorhandener Blogbeitraege
- Bearbeiten eines Beitrags
- Loeschen eines Beitrags
- Loeschen des letzten vorhandenen Beitrags
- Liken eines Beitrags
- `GET` ist fuer Delete und Like nicht erlaubt

## Hinweise

- Neue Blogbeitraege werden in `dictionary/data.json` gespeichert.
- Zum Zuruecksetzen der Daten kann `dictionary/data.json` auf eine leere Liste gesetzt werden:

```json
[]
```
