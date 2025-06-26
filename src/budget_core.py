import os
from dataclasses import dataclass
from typing import List

@dataclass
class Eintrag:
    betrag: float
    beschreibung: str
    kategorie: str
    typ: str  # 'Einnahme' oder 'Ausgabe'


def eintrag_hinzufuegen(liste: List[Eintrag], betrag: float, beschreibung: str, kategorie: str, typ: str):
    liste.append(Eintrag(betrag, beschreibung, kategorie, typ))


def berechne_uebersicht(eintraege: List[Eintrag]):
    gesamt_einnahmen = sum(e.betrag for e in eintraege if e.typ == 'Einnahme')
    gesamt_ausgaben = sum(e.betrag for e in eintraege if e.typ == 'Ausgabe')
    saldo = gesamt_einnahmen - gesamt_ausgaben
    return gesamt_einnahmen, gesamt_ausgaben, saldo


def speichere_in_datei(eintraege: List[Eintrag], dateiname: str = "budget_export.txt"):
    ordner = "data"
    if not os.path.exists(ordner):
        os.makedirs(ordner)
    pfad = os.path.join(ordner, dateiname)
    with open(pfad, "w", encoding="utf-8") as f:
        f.write("Einnahmen:\n")
        for e in eintraege:
            if e.typ == 'Einnahme':
                f.write(f"{e.betrag:.2f} € | {e.beschreibung} | Kategorie: {e.kategorie}\n")
        f.write("\nAusgaben:\n")
        for e in eintraege:
            if e.typ == 'Ausgabe':
                f.write(f"{e.betrag:.2f} € | {e.beschreibung} | Kategorie: {e.kategorie}\n") 