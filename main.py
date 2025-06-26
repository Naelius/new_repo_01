import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

def main():
    print("Willkommen zum Budget-Manager!")
    print("1. GUI starten")
    print("2. Terminal-Version starten")
    wahl = input("Bitte wählen (1/2): ")
    if wahl == "1":
        import budget_gui
        budget_gui.main()
    elif wahl == "2":
        import budget_cli
        budget_cli.main()
    else:
        print("Ungültige Auswahl.")

if __name__ == "__main__":
    main() 