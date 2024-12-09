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

            seg_backgr = ctk.CTkFrame(self.create_account_window, fg_color="#1a1a1a", width=600, height=400)
            seg_backgr.pack(padx=5, pady=5, expand=True)

            container = ctk.CTkFrame(seg_backgr)
            container.pack(fill="both", expand=True, padx=10, pady=10)

                                                                     


            self.create_account_window.after(100, self.create_account_window.lift)

            