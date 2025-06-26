from budget_core import Eintrag, eintrag_hinzufuegen, berechne_uebersicht, speichere_in_datei

def main():
    eintraege = []
    kategorien = ["Essen", "Freizeit", "Fixkosten", "Sonstiges"]
    while True:
        print("\n--- Budget-Manager (Terminal) ---")
        print("1. Einnahme hinzufügen")
        print("2. Ausgabe hinzufügen")
        print("3. Übersicht anzeigen")
        print("4. In Datei speichern")
        print("5. Beenden")
        auswahl = input("Bitte wähle eine Option (1-5): ")

        if auswahl in ("1", "2"):
            try:
                betrag = float(input("Betrag: "))
                if betrag <= 0:
                    print("Bitte nur positive Zahlen eingeben!")
                    continue
            except ValueError:
                print("Ungültige Eingabe! Bitte eine Zahl eingeben.")
                continue
            beschreibung = input("Beschreibung: ")
            print("Kategorie wählen:")
            for i, k in enumerate(kategorien, 1):
                print(f"{i}. {k}")
            try:
                k_index = int(input("Nummer der Kategorie: ")) - 1
                kategorie = kategorien[k_index]
            except (ValueError, IndexError):
                print("Ungültige Kategorie. 'Sonstiges' wird verwendet.")
                kategorie = "Sonstiges"
            typ = "Einnahme" if auswahl == "1" else "Ausgabe"
            eintrag_hinzufuegen(eintraege, betrag, beschreibung, kategorie, typ)
            print(f"{typ} hinzugefügt.")
        elif auswahl == "3":
            einnahmen, ausgaben, saldo = berechne_uebersicht(eintraege)
            print(f"\nGesamteinnahmen: {einnahmen:.2f}")
            print(f"Gesamtausgaben: {ausgaben:.2f}")
            print(f"Saldo: {saldo:.2f}")
            if saldo < 0:
                print("Achtung: Budget überschritten!")
        elif auswahl == "4":
            speichere_in_datei(eintraege)
            print("Daten wurden gespeichert.")
        elif auswahl == "5":
            print("Programm beendet.")
            break
        else:
            print("Ungültige Auswahl. Bitte erneut versuchen.")

if __name__ == "__main__":
    main() 