import tkinter as tk
import customtkinter as ctk

def create_account(self):
    if self.create_account_window is None or not self.create_account_window.winfo_exists():
            self.create_account_window = ctk.CTkToplevel(self.master)
            self.create_account_window.title("pt1 Lightweight Notes - Create Account")
            self.create_account_window.geometry("500x500")
            self.create_account_window.resizable(False, False)
            self.create_account_window.after(100, self.create_account_window.lift)

            