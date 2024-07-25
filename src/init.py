from tkinter import *
import customtkinter
import subprocess
import os

# Theme of Application
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("yellow")
customtkinter.deactiviate_automatic_dpi_awareness()

def login_screen():
    root = customtkinter.CTk()
    
    # Create Windows for GUI
    root.title("pt1 - Lightweight Notes")
    root.geometry('350x350')
    root.resizable(False, False)
    
    