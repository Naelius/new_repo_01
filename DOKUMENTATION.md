# Projektdokumentation: Budget-Manager

## Übersicht
Dieses Dokument beschreibt die Entwicklungsschritte, Designentscheidungen und die Struktur des Budget-Manager-Projekts.

---

## 1. Zielsetzung
Ein flexibles, einfach bedienbares Tool zur Verwaltung von Einnahmen und Ausgaben – sowohl als Terminal- als auch als GUI-Anwendung, mit Export, dynamischen Kategorien, Mehrsprachigkeit und moderner Bedienung.

---

## 2. Entwicklungsschritte

### Schritt 1: Terminal-Version (CLI)
- Grundfunktionen: Einnahmen/Ausgaben erfassen, Übersicht, Schleife, Validierung
- Modularisierung: Funktionen für Eintrag, Übersicht, main()

### Schritt 2: GUI mit Tkinter
- Grundgerüst mit Eingabefeldern, Buttons, Übersicht
- Erweiterung um Listbox für Einträge
- Diagramm (matplotlib) in separatem Fenster

### Schritt 3: Professionalisierung
- Zentrale Kernlogik in budget_core.py ausgelagert
- GUI und CLI nutzen die gleiche Logik
- Projektstruktur mit src/, data/, tests/
- requirements.txt und ausführliche README

### Schritt 4: Erweiterungen
- Sprachumschaltung (Deutsch/Englisch) mit zentralem translations.py
- Export in data/-Ordner, automatisches Anlegen des Ordners
- Dynamische Kategorien: Nutzer kann eigene Kategorien hinzufügen/entfernen, Speicherung in JSON
- Kompakte GUI, Listbox mit Scrollbar, Beenden-Button
- Keine externen Übersetzungsdienste mehr, Kategorien werden manuell in beiden Sprachen eingegeben

---

## 3. Projektstruktur

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
├── DOKUMENTATION.md    # Diese ausführliche Doku
└── .gitignore
```

---

## 4. Designentscheidungen
- **Separation of Concerns:** Logik, GUI, CLI und Übersetzungen sind klar getrennt.
- **Erweiterbarkeit:** Kategorien, Sprachen, Exportziel, weitere Features sind leicht erweiterbar.
- **Benutzerfreundlichkeit:** GUI mit ttk, dynamische Kategorien (JSON), Sprachumschaltung, kompakte Listbox mit Scrollbar, Beenden-Button.
- **Wartbarkeit:** Zentrale Logik, ausführliche Doku, Tests vorgesehen.
- **Datenschutz:** Keine externen Übersetzungsdienste, alle Daten lokal.

---

## 5. Weiteres
- Für Unittests: tests/-Ordner nutzen, z. B. mit pytest.
- Für neue Features: Siehe Vorschläge in README und DOKUMENTATION.md.
- Für Fragen: Siehe README oder Quellcode-Kommentare.

---

**Letzte Aktualisierung:** 2024-06 