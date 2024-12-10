import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk

from init import runpath


def create_account(self):
    if self.create_account_window is None or not self.create_account_window.winfo_exists():
        self.create_account_window = ctk.CTkToplevel(self.master)
        self.create_account_window.title("pt1 Lightweight Notes - Create Account")
        self.create_account_window.geometry("900x600")
        self.create_account_window.resizable(False, False)

        background_image = ctk.CTkImage(Image.open(f"{runpath}\\src\\img\\signup_background.jpg"), size=(900, 600))

        background_label = ctk.CTkLabel(self.create_account_window, image=background_image, text="")
        background_label.place(relwidth=1, relheight=1)

        seg_backgr = ctk.CTkFrame(self.create_account_window, fg_color="#1a1a1a", width=800, height=500)
        seg_backgr.pack(padx=5, pady=5, expand=True)

        container = ctk.CTkFrame(seg_backgr, fg_color="#293133", width=500, height=300)
        container.pack(padx=5, pady=5, fill="both", expand=True)

        # Zeilen und Spalten für Layout konfigurieren
        container.grid_rowconfigure([0, 1, 2, 3, 4], weight=1)  # Zeilen dehnen
        container.grid_columnconfigure(0, weight=1)  # Spalte 0 für Bild
        container.grid_columnconfigure(1, weight=3)  # Spalte 1 für Eingabefelder

        # Bild in Spalte 0 hinzufügen und mittig platzieren
        image_path = f"{runpath}\\src\\img\\user.png"  # Passe den Pfad an
        profile_image = ctk.CTkImage(Image.open(image_path), size=(150, 150))  # Bildgröße anpassen

        image_label = ctk.CTkLabel(container, image=profile_image, text="")  # Kein Text
        image_label.grid(row=0, column=0, rowspan=5, padx=20, pady=20, sticky="n")  # rowspan: über 5 Zeilen

        # Textboxen in Spalte 1
        firstname_label = ctk.CTkLabel(container, text="Vorname:", fg_color="transparent")
        firstname_label.grid(row=0, column=1, padx=20, pady=10, sticky="w")

        firstname_entry = ctk.CTkEntry(container, placeholder_text="Geben Sie Ihren Vornamen ein")
        firstname_entry.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        password_label = ctk.CTkLabel(container, text="Passwort:", fg_color="transparent")
        password_label.grid(row=2, column=1, padx=20, pady=10, sticky="w")

        password_entry = ctk.CTkEntry(container, placeholder_text="Geben Sie Ihr Passwort ein", show="*")
        password_entry.grid(row=3, column=1, padx=20, pady=10, sticky="ew")

        confirm_password_label = ctk.CTkLabel(container, text="Passwort bestätigen:", fg_color="transparent")
        confirm_password_label.grid(row=4, column=1, padx=20, pady=10, sticky="w")

        confirm_password_entry = ctk.CTkEntry(container, placeholder_text="Passwort erneut eingeben", show="*")
        confirm_password_entry.grid(row=5, column=1, padx=20, pady=10, sticky="ew")

        self.create_account_window.after(100, self.create_account_window.lift)



            