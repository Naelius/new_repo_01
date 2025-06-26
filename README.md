# Budget-Manager

Ein einfaches Python-Tool zur Verwaltung von Einnahmen und Ausgaben – mit grafischer Oberfläche (Tkinter) und Terminal-Menü.

## Features
- Einnahmen und Ausgaben mit Beschreibung und Kategorie erfassen
- Übersicht über Gesamteinnahmen, Gesamtausgaben und Saldo
- Dynamische Kategorien: Eigene Kategorien können hinzugefügt/entfernt werden (werden in `data/kategorien.json` gespeichert)
- Kategorien in Deutsch und Englisch, Sprachumschaltung jederzeit möglich
- Kompakte, moderne GUI mit Scrollbar für Einträge und Beenden-Button
- Professionelles Diagramm (matplotlib)
- Daten werden im Ordner `data/` gespeichert
- GUI (Tkinter) und CLI (Terminal) wählbar

## Installation
1. Python 3.8+ installieren
2. Abhängigkeiten installieren:
   ```
   pip install -r requirements.txt
   ```

## Nutzung
### Starten
Im Projektordner:
```
python main.py
```
Falls du eigene Skripte schreibst, importiere Module aus `src/` (siehe main.py für Beispiel mit sys.path).

### GUI
- Beträge, Beschreibung und Kategorie eingeben
- Eigene Kategorien hinzufügen/entfernen (werden dauerhaft gespeichert)
- Einnahme/Ausgabe hinzufügen
- Übersicht und Einträge werden angezeigt
- Diagramm-Button für grafische Auswertung
- "In Datei speichern" für Export (Datei liegt in `data/`)
- Sprache oben rechts umschaltbar
- Beenden-Button schließt das Programm

### Terminal
- Menü im Terminal bedienen
- Übersicht und Export wie in der GUI

## Projektstruktur
```
/ (Projektwurzel)
│
├── src/                # Hauptcode (Python-Module)
│   ├── budget_core.py
│   ├── budget_gui.py
│   ├── budget_cli.py
│   └── translations.py
│
├── data/               # Für Exportdateien und Kategorien (z. B. budget_export.txt, kategorien.json)
│
├── tests/              # Platz für Unittests
│
├── main.py             # Einstiegspunkt (GUI/CLI-Auswahl)
├── requirements.txt    # Abhängigkeiten
├── README.md           # Kurzanleitung
├── DOKUMENTATION.md    # Ausführliche Doku
└── .gitignore
```

## Hinweise
- Exportierte Dateien und Kategorien findest du immer im `data/`-Ordner.
- Die Imports in main.py sorgen dafür, dass du die Module aus `src/` nutzen kannst.
- Es werden keine externen Übersetzungsdienste genutzt – Kategorien werden manuell in beiden Sprachen eingegeben.

---