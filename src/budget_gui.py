import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from budget_core import Eintrag, eintrag_hinzufuegen, berechne_uebersicht, speichere_in_datei
from translations import translations
import os
import json

KAT_FILE = os.path.join("data", "kategorien.json")

class BudgetManagerGUI:
    """
    Hauptklasse für die grafische Oberfläche des Budget-Managers.
    Verwaltet Einträge, Kategorien, Sprache, Export und das Layout.
    """
    def __init__(self, root):
        """
        Initialisiert die GUI, lädt Kategorien, setzt Layout und verbindet Events.
        """
        self.eintraege = []  # Liste von Eintrag-Objekten
        self.sprache = "de"
        self.kategorien, self.kategorien_en = self.lade_kategorien()

        root.title("Budget-Manager")
        root.geometry("540x500")

        # Sprache-Hinweis und Umschalter
        top_frame = ttk.Frame(root)
        top_frame.pack(fill="x", pady=2)
        self.lang_label = ttk.Label(top_frame, text="", font=("Arial", 8, "italic"))
        self.lang_label.pack(side="left", padx=10)
        self.lang_button = ttk.Button(top_frame, text="EN", width=4, command=self.toggle_language)
        self.lang_button.pack(side="right", padx=10)

        main_frame = ttk.Frame(root, padding=10)
        main_frame.pack(fill="both", expand=True)

        # Eingabefelder
        self.eingabe_frame = ttk.LabelFrame(main_frame, text="", padding=10)
        self.eingabe_frame.pack(fill="x", pady=5)

        self.amount_label = ttk.Label(self.eingabe_frame, text="")
        self.amount_label.grid(row=0, column=0, sticky="w")
        self.betrag_entry = ttk.Entry(self.eingabe_frame)
        self.betrag_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        self.desc_label = ttk.Label(self.eingabe_frame, text="")
        self.desc_label.grid(row=1, column=0, sticky="w")
        self.beschreibung_entry = ttk.Entry(self.eingabe_frame)
        self.beschreibung_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        self.cat_label = ttk.Label(self.eingabe_frame, text="")
        self.cat_label.grid(row=2, column=0, sticky="w")
        self.kategorie_var = tk.StringVar(root)
        self.kategorie_var.set(self.kategorien[0])
        self.kategorie_menu = ttk.Combobox(self.eingabe_frame, textvariable=self.kategorie_var, values=self.kategorien, state="readonly")
        self.kategorie_menu.grid(row=2, column=1, sticky="ew", padx=5, pady=2)

        # Buttons für Kategorien
        self.add_cat_btn = ttk.Button(self.eingabe_frame, text="+", width=3, command=self.kategorie_hinzufuegen)
        self.add_cat_btn.grid(row=2, column=2, padx=2)
        self.remove_cat_btn = ttk.Button(self.eingabe_frame, text="-", width=3, command=self.kategorie_entfernen)
        self.remove_cat_btn.grid(row=2, column=3, padx=2)

        self.eingabe_frame.columnconfigure(1, weight=1)

        # Buttons
        self.button_frame1 = ttk.Frame(main_frame)
        self.button_frame1.pack(fill="x", pady=5)
        self.button_frame1.columnconfigure((0,1,2,3,4), weight=1)
        self.add_income_btn = ttk.Button(self.button_frame1, text="", command=self.einnahme_hinzufuegen)
        self.add_income_btn.grid(row=0, column=1, padx=10)
        self.add_expense_btn = ttk.Button(self.button_frame1, text="", command=self.ausgabe_hinzufuegen)
        self.add_expense_btn.grid(row=0, column=2, padx=10)
        self.chart_btn = ttk.Button(self.button_frame1, text="", command=self.zeige_diagramm_fenster)
        self.chart_btn.grid(row=0, column=3, padx=10)

        self.button_frame2 = ttk.Frame(main_frame)
        self.button_frame2.pack(fill="x", pady=5)
        self.button_frame2.columnconfigure((0,1,2,3,4), weight=1)
        self.save_btn = ttk.Button(self.button_frame2, text="", command=self.speichere_in_datei)
        self.save_btn.grid(row=0, column=1, padx=10)
        self.exit_btn = ttk.Button(self.button_frame2, text="Beenden", command=root.destroy)
        self.exit_btn.grid(row=0, column=2, padx=10)

        # Übersicht
        self.uebersicht_label = ttk.Label(main_frame, text="", font=("Arial", 12, "bold"))
        self.uebersicht_label.pack(pady=10)
        self.uebersicht_text = ttk.Label(main_frame, text="")
        self.uebersicht_text.pack()

        # Listbox für Einträge mit Scrollbar
        self.eintraege_frame = ttk.LabelFrame(main_frame, text="", padding=10)
        self.eintraege_frame.pack(fill="x", pady=5)
        self.eintraege_scrollbar = ttk.Scrollbar(self.eintraege_frame, orient="vertical")
        self.eintraege_listbox = tk.Listbox(self.eintraege_frame, width=70, height=5, yscrollcommand=self.eintraege_scrollbar.set)
        self.eintraege_scrollbar.config(command=self.eintraege_listbox.yview)
        self.eintraege_listbox.pack(side="left", fill="both", expand=True)
        self.eintraege_scrollbar.pack(side="right", fill="y")

        self.update_language()

    def lade_kategorien(self):
        """
        Lädt Kategorien aus der JSON-Datei oder legt sie mit Standardwerten an.
        Gibt zwei Listen zurück: Deutsch und Englisch.
        """
        # Standardkategorien mit Übersetzung
        defaults = [
            {"de": "Essen", "en": "Food", "is_default": True},
            {"de": "Freizeit", "en": "Leisure", "is_default": True},
            {"de": "Fixkosten", "en": "Fixed costs", "is_default": True},
            {"de": "Sonstiges", "en": "Other", "is_default": True}
        ]
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(KAT_FILE):
            with open(KAT_FILE, "w", encoding="utf-8") as f:
                json.dump(defaults, f, ensure_ascii=False, indent=2)
        with open(KAT_FILE, "r", encoding="utf-8") as f:
            cats = json.load(f)
        kategorien = [c["de"] for c in cats]
        kategorien_en = [c["en"] for c in cats]
        return kategorien, kategorien_en

    def speichere_kategorien(self):
        """
        Speichert die aktuellen Kategorien (de/en) in die JSON-Datei.
        """
        # Schreibe aktuelle Kategorien in die JSON-Datei
        cats = []
        for i, de in enumerate(self.kategorien):
            # Standardkategorien erkennen
            if de in ["Essen", "Freizeit", "Fixkosten", "Sonstiges"]:
                en = self.kategorien_en[i] if i < len(self.kategorien_en) else de
                cats.append({"de": de, "en": en, "is_default": True})
            else:
                en = self.kategorien_en[i] if i < len(self.kategorien_en) else de
                cats.append({"de": de, "en": en, "is_default": False})
        with open(KAT_FILE, "w", encoding="utf-8") as f:
            json.dump(cats, f, ensure_ascii=False, indent=2)

    def kategorie_hinzufuegen(self):
        """
        Öffnet Dialog(e) zum Hinzufügen einer neuen Kategorie (de/en) und speichert sie.
        """
        t = translations[self.sprache]
        if self.sprache == "de":
            neue_kat = simpledialog.askstring("Kategorie hinzufügen", "Neue Kategorie eingeben:")
            neue_kat_en = simpledialog.askstring("Kategorie hinzufügen", "Englische Übersetzung eingeben:")
            if neue_kat and neue_kat_en:
                neue_kat = neue_kat.strip()
                neue_kat_en = neue_kat_en.strip()
                if neue_kat not in self.kategorien:
                    self.kategorien.append(neue_kat)
                    self.kategorien_en.append(neue_kat_en)
                    self.kategorie_menu.config(values=self.kategorien)
                    self.speichere_kategorien()
        else:
            neue_kat = simpledialog.askstring("Add Category", "Enter new category:")
            neue_kat_de = simpledialog.askstring("Add Category", "Enter German translation:")
            if neue_kat and neue_kat_de:
                neue_kat = neue_kat.strip()
                neue_kat_de = neue_kat_de.strip()
                if neue_kat not in self.kategorien_en:
                    self.kategorien_en.append(neue_kat)
                    self.kategorien.append(neue_kat_de)
                    self.kategorie_menu.config(values=self.kategorien_en)
                    self.speichere_kategorien()

    def kategorie_entfernen(self):
        """
        Entfernt die aktuell gewählte Kategorie (außer Standardkategorien) und speichert die Änderung.
        """
        t = translations[self.sprache]
        aktuelle_kat = self.kategorie_var.get()
        if self.sprache == "de":
            if aktuelle_kat in ["Essen", "Freizeit", "Fixkosten", "Sonstiges"]:
                messagebox.showwarning("Hinweis", "Standardkategorien können nicht entfernt werden.")
                return
            if aktuelle_kat in self.kategorien:
                idx = self.kategorien.index(aktuelle_kat)
                self.kategorien.pop(idx)
                self.kategorien_en.pop(idx)
                self.kategorie_menu.config(values=self.kategorien)
                self.kategorie_var.set(self.kategorien[0])
                self.speichere_kategorien()
        else:
            if aktuelle_kat in ["Food", "Leisure", "Fixed costs", "Other"]:
                messagebox.showwarning("Notice", "Default categories cannot be removed.")
                return
            if aktuelle_kat in self.kategorien_en:
                idx = self.kategorien_en.index(aktuelle_kat)
                self.kategorien_en.pop(idx)
                self.kategorien.pop(idx)
                self.kategorie_menu.config(values=self.kategorien_en)
                self.kategorie_var.set(self.kategorien_en[0])
                self.speichere_kategorien()

    def update_language(self):
        """
        Aktualisiert alle Texte und Labels entsprechend der aktuellen Sprache.
        Ruft auch update_uebersicht und update_eintraege_listbox auf.
        """
        t = translations[self.sprache]
        self.lang_label.config(text=t["language"])
        self.lang_button.config(text="EN" if self.sprache == "de" else "DE")
        self.eingabe_frame.config(text=t["new_entry"])
        self.amount_label.config(text=t["amount"] + ":")
        self.desc_label.config(text=t["description"] + ":")
        self.cat_label.config(text=t["category"] + ":")
        # Kategorien anpassen
        if self.sprache == "de":
            self.kategorie_menu.config(values=self.kategorien)
            if self.kategorie_var.get() not in self.kategorien:
                self.kategorie_var.set(self.kategorien[0])
        else:
            self.kategorie_menu.config(values=self.kategorien_en)
            if self.kategorie_var.get() not in self.kategorien_en:
                self.kategorie_var.set(self.kategorien_en[0])
        self.add_income_btn.config(text=t["add_income"])
        self.add_expense_btn.config(text=t["add_expense"])
        self.chart_btn.config(text=t["show_chart"])
        self.save_btn.config(text=t["save_file"])
        self.exit_btn.config(text="Beenden" if self.sprache == "de" else "Exit")
        self.uebersicht_label.config(text=t["overview"])
        self.eintraege_frame.config(text=t["entries"])
        self.update_uebersicht()
        self.update_eintraege_listbox()

    def toggle_language(self):
        """
        Wechselt zwischen Deutsch und Englisch und aktualisiert die Oberfläche.
        """
        self.sprache = "en" if self.sprache == "de" else "de"
        self.update_language()

    def einnahme_hinzufuegen(self):
        """
        Fügt einen neuen Einnahme-Eintrag hinzu, sofern die Eingabe gültig ist.
        """
        betrag = self.get_betrag()
        beschreibung = self.beschreibung_entry.get().strip()
        kategorie = self.kategorie_var.get()
        # Kategorie ggf. zurückübersetzen
        if self.sprache == "en" and kategorie in self.kategorien_en:
            kategorie = self.kategorien[self.kategorien_en.index(kategorie)]
        if betrag is not None:
            eintrag_hinzufuegen(self.eintraege, betrag, beschreibung, kategorie, "Einnahme")
            self.update_uebersicht()
            self.update_eintraege_listbox()
            self.clear_entries()

    def ausgabe_hinzufuegen(self):
        """
        Fügt einen neuen Ausgabe-Eintrag hinzu, sofern die Eingabe gültig ist.
        """
        betrag = self.get_betrag()
        beschreibung = self.beschreibung_entry.get().strip()
        kategorie = self.kategorie_var.get()
        if self.sprache == "en" and kategorie in self.kategorien_en:
            kategorie = self.kategorien[self.kategorien_en.index(kategorie)]
        if betrag is not None:
            eintrag_hinzufuegen(self.eintraege, betrag, beschreibung, kategorie, "Ausgabe")
            self.update_uebersicht()
            self.update_eintraege_listbox()
            self.clear_entries()

    def get_betrag(self):
        """
        Prüft und gibt den eingegebenen Betrag zurück (nur positive Zahlen).
        """
        t = translations[self.sprache]
        try:
            betrag = float(self.betrag_entry.get())
            if betrag > 0:
                return betrag
            else:
                messagebox.showwarning(t["error"], t["positive_only"])
                return None
        except ValueError:
            messagebox.showwarning(t["error"], t["invalid_number"])
            return None

    def update_uebersicht(self):
        """
        Aktualisiert die Übersicht (Summen, Saldo, Warnung) im GUI.
        """
        t = translations[self.sprache]
        einnahmen, ausgaben, saldo = berechne_uebersicht(self.eintraege)
        text = f"{t['income']}: {einnahmen:.2f}\n{t['expense']}: {ausgaben:.2f}\n{t['saldo']}: {saldo:.2f}"
        if saldo < 0:
            text += f"\n{t['budget_exceeded']}"
        self.uebersicht_text.config(text=text)

    def update_eintraege_listbox(self):
        """
        Aktualisiert die Listbox mit allen Einträgen, übersetzt Kategorien je nach Sprache.
        """
        t = translations[self.sprache]
        self.eintraege_listbox.delete(0, tk.END)
        for e in self.eintraege:
            typ = t["add_income"] if e.typ == "Einnahme" and self.sprache == "en" else (
                t["add_expense"] if e.typ == "Ausgabe" and self.sprache == "en" else e.typ)
            # Kategorie ggf. übersetzen
            kategorie = e.kategorie
            if self.sprache == "en" and kategorie in self.kategorien:
                kategorie = self.kategorien_en[self.kategorien.index(kategorie)]
            eintrag = f"{typ}:   {e.betrag:.2f} €   | {e.beschreibung}   | {t['category']}: {kategorie}"
            self.eintraege_listbox.insert(tk.END, eintrag)

    def zeige_diagramm_fenster(self):
        """
        Öffnet ein neues Fenster mit einem Balkendiagramm für Einnahmen und Ausgaben.
        """
        t = translations[self.sprache]
        fenster = tk.Toplevel()
        fenster.title(t["show_chart"])
        fig, ax = plt.subplots(figsize=(5, 3))
        einnahmen, ausgaben, _ = berechne_uebersicht(self.eintraege)
        werte = [einnahmen, ausgaben]
        labels = [t["income"], t["expense"]]
        farben = ["green", "red"]
        bars = ax.bar(labels, werte, color=farben)
        ax.set_ylabel("€")
        ax.set_title(t["show_chart"])
        for bar, v in zip(bars, werte):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() / 2, f"{v:.2f} €", ha='center', va='center', color='white', fontweight='bold')
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=fenster)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def clear_entries(self):
        """
        Leert die Eingabefelder für Betrag und Beschreibung.
        """
        self.betrag_entry.delete(0, tk.END)
        self.beschreibung_entry.delete(0, tk.END)

    def speichere_in_datei(self):
        """
        Exportiert alle Einträge in eine Textdatei im data-Ordner.
        """
        t = translations[self.sprache]
        try:
            speichere_in_datei(self.eintraege)
            messagebox.showinfo(t["success"], t["saved"])
        except Exception as e:
            messagebox.showerror(t["error"], t["save_error"].format(e=e))

def main():
    """Startet die Tkinter-GUI."""
    root = tk.Tk()
    app = BudgetManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 