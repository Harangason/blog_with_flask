# blog_with_flask

Ein kleiner Flask-Blog mit Datei-gestützter Datenspeicherung (JSON).

## Projektstruktur

- `app.py` – Flask-App mit Routen für `index`, `add`, `update`, `delete`
- `templates/`
  - `index.html` – zeigt Blogeinträge an (dynamisch via `posts`)
  - `add.html` – Formular für neue Beiträge
  - `update.html` – Formular zum Bearbeiten eines bestehenden Beitrags
- `dictionary/data.json` – persistierte Blogdaten
- `static/style.css` – Styling
- `test_app.py` – Unit-Tests für die App

## Starten der App

```bash
cd Codio/Term_3/blog_with_flask
python app.py
```

Standardmäßig läuft die App auf `http://127.0.0.1:5000/`.

## Verfügbare Routen

- `GET /`
  - Zeigt alle Blogbeiträge aus `dictionary/data.json` an.
- `GET /add`
  - Zeigt das Formular zum Erstellen eines Beitrags.
- `POST /add`
  - Speichert einen neuen Beitrag im JSON-Speicher.
- `GET /update/<post_id>`
  - Zeigt das Bearbeitungsformular für den Beitrag mit dieser ID.
- `POST /update/<post_id>`
  - Aktualisiert Titel, Autor und Inhalt dieses Beitrags.
- `POST /delete/<post_id>`
  - Löscht den Beitrag mit der gegebenen ID.
- `POST /like/<post_id>`
  - Erhoeht den Like-Zaehler dieses Beitrags.
- `GET /favicon.ico`
  - Schickt `204`, falls kein Favicon vorhanden ist.

## JSON-Format

`dictionary/data.json` enthält eine Liste von Objekten:

```json
[
  {
    "id": 1,
    "author": "John Doe",
    "title": "First Post",
    "content": "This is my first post."
  }
]
```

`id` ist der Primärschlüssel pro Beitrag.

## Tests ausführen

```bash
cd Codio/Term_3/blog_with_flask
python -m unittest test_app.py
```

Erwartung: `Ran ... OK` bei erfolgreich bestandenen Tests.

## Hinweise

- Neue Beiträge landen in `dictionary/data.json` als JSON-Liste.
- Wenn du den Datenbestand zurücksetzen willst, kannst du die `data.json` manuell leeren:
  - `[]`
- Nach Änderungen an Templates oder Datenlogik empfiehlt sich ein kurzer Testlauf über `unittest`.
